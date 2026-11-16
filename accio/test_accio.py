"""Tests for the Accio Work plugin build and its listing-rule validator.

Run from the repo root: python3 -m unittest discover -s accio -v
"""

import copy
import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

import build
import validate
from plugins import LOCALES, PLUGINS


class BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.dist = build.build_all(cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def test_builds_one_package_and_zip_per_plugin(self):
        for plugin in PLUGINS:
            pkg = self.dist / plugin["id"]
            self.assertTrue((pkg / "plugin.json").is_file(), pkg)
            archive = self.dist / f"{plugin['id']}.zip"
            self.assertTrue(archive.is_file(), archive)
            with zipfile.ZipFile(archive) as zf:
                self.assertIn(f"{plugin['id']}/plugin.json", zf.namelist())

    def test_every_built_package_passes_the_validator(self):
        for plugin in PLUGINS:
            errors = validate.validate_package(self.dist / plugin["id"])
            self.assertEqual(errors, [], f"{plugin['id']}: {errors}")

    def test_connector_points_at_the_hosted_mcp(self):
        for plugin in PLUGINS:
            data = json.loads((self.dist / plugin["id"] / "connectors" / "connectors.json").read_text())
            server = data["mcpServers"][plugin["connector_id"]]
            self.assertEqual(server["url"], plugin["mcp_url"])
            self.assertTrue(server["url"].startswith("https://studio.alvinsclub.ai/"))

    def test_skills_carry_accio_frontmatter_and_no_other_host_wording(self):
        for plugin in PLUGINS:
            skill = self.dist / plugin["id"] / "skills" / plugin["skill"]["id"] / "SKILL.md"
            text = skill.read_text()
            meta = validate.parse_frontmatter(text)
            self.assertEqual(meta["name"], plugin["skill"]["id"])
            self.assertIn("displayName", meta)
            self.assertIn("displayDescription", meta)
            for banned in ("Connectors tab", "from Claude", "claude mcp add", "ChatGPT"):
                self.assertNotIn(banned, text, f"{plugin['id']}: {banned}")

    def test_icon_is_240px_png_and_shared_with_connector(self):
        for plugin in PLUGINS:
            res = self.dist / plugin["id"] / "resources"
            icon = (res / "icon.png").read_bytes()
            self.assertEqual(validate.png_size(icon), (240, 240))
            self.assertEqual((res / f"{plugin['connector_id']}.png").read_bytes(), icon)

    def test_i18n_covers_every_locale_for_every_entry(self):
        for plugin in PLUGINS:
            data = json.loads((self.dist / plugin["id"] / "resources" / "i18n.json").read_text())
            self.assertEqual(data["defaultLocale"], "en")
            for key, values in data["entries"].items():
                self.assertEqual(set(values), set(LOCALES) - {"en"}, key)


class ValidatorTest(unittest.TestCase):
    """Each listing rule from Accio's 01/02/03 docs must actually be enforced."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.dist = build.build_all(cls.tmp)
        cls.good = cls.dist / PLUGINS[0]["id"]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def mutate(self, edit):
        pkg = Path(tempfile.mkdtemp()) / "pkg"
        shutil.copytree(self.good, pkg)
        self.addCleanup(shutil.rmtree, pkg.parent)
        edit(pkg)
        return validate.validate_package(pkg)

    def edit_json(self, pkg, rel, change):
        path = pkg / rel
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data, ensure_ascii=False))

    def assert_flags(self, errors, needle):
        self.assertTrue(any(needle in e for e in errors), f"expected '{needle}' in {errors}")

    def test_rejects_anthropomorphic_name(self):
        errors = self.mutate(lambda p: self.edit_json(
            p, "plugin.json", lambda d: d.update(displayName="Alvin's Club Studio Assistant")))
        self.assert_flags(errors, "anthropomorphic")

    def test_rejects_plugin_word_in_name(self):
        errors = self.mutate(lambda p: self.edit_json(
            p, "plugin.json", lambda d: d.update(name="Alvin's Club Studio Plugin")))
        self.assert_flags(errors, "plugin")

    def test_rejects_unknown_category(self):
        errors = self.mutate(lambda p: self.edit_json(
            p, "plugin.json", lambda d: d.update(category="productivity")))
        self.assert_flags(errors, "category")

    def test_rejects_missing_locale(self):
        def drop(data):
            first = next(iter(data["entries"].values()))
            first.pop("vi")
        errors = self.mutate(lambda p: self.edit_json(p, "resources/i18n.json", drop))
        self.assert_flags(errors, "vi")

    def test_rejects_flat_i18n_format(self):
        errors = self.mutate(lambda p: (p / "resources" / "i18n.json").write_text(
            json.dumps({"en": {"plugin.displayName": "x"}})))
        self.assert_flags(errors, "entries")

    def test_rejects_hardcoded_secret(self):
        errors = self.mutate(lambda p: (p / "prompt.md").write_text(
            "api_key = sk-live-abcdefghijklmnopqrstuvwxyz123456"))
        self.assert_flags(errors, "secret")

    def test_rejects_inconsistent_brand_spelling(self):
        errors = self.mutate(lambda p: self.edit_json(
            p, "plugin.json", lambda d: d.update(description="Alvins Club Studio makes videos.")))
        self.assert_flags(errors, "brand")

    def test_rejects_connector_icon_that_differs_from_plugin_icon(self):
        def swap(pkg):
            connector_icon = next(f for f in (pkg / "resources").glob("*.png") if f.name != "icon.png")
            connector_icon.write_bytes(connector_icon.read_bytes() + b"x")
        errors = self.mutate(swap)
        self.assert_flags(errors, "icon")

    def test_rejects_long_summary(self):
        errors = self.mutate(lambda p: self.edit_json(
            p, "plugin.json", lambda d: d.update(summary="x" * 80)))
        self.assert_flags(errors, "summary")

    def test_rejects_missing_tags(self):
        errors = self.mutate(lambda p: self.edit_json(p, "plugin.json", lambda d: d.pop("tags")))
        self.assert_flags(errors, "tags")

    def test_rejects_author_without_name(self):
        errors = self.mutate(lambda p: self.edit_json(p, "plugin.json", lambda d: d.update(author={"url": "x"})))
        self.assert_flags(errors, "author")

    def test_rejects_brand_misspelling_in_prompt(self):
        errors = self.mutate(lambda p: (p / "prompt.md").write_text("Use Alvins Club Studio tools."))
        self.assert_flags(errors, "prompt.md")

    def test_rejects_description_missing_brand_when_display_name_locale_missing(self):
        def drop(data):
            data["entries"]["plugin.displayName"].pop("fr")
        errors = self.mutate(lambda p: self.edit_json(p, "resources/i18n.json", drop))
        self.assert_flags(errors, "[fr] must name the brand")

    def test_validates_the_uploaded_zip(self):
        archive = self.dist / f"{PLUGINS[0]['id']}.zip"
        self.assertEqual(validate.validate_path(archive), [])

    def test_rejects_zip_with_wrong_top_folder(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        archive = tmp / f"{PLUGINS[0]['id']}.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            zf.writestr("other/plugin.json", "{}")
        self.assert_flags(validate.validate_path(archive), "exactly one folder")

    def test_cli_fails_on_missing_path(self):
        self.assertEqual(validate.main(["/nonexistent/accio-package"]), 1)

    def test_rejects_missing_skill_frontmatter_field(self):
        def strip(pkg):
            skill = next((pkg / "skills").glob("*/SKILL.md"))
            skill.write_text(skill.read_text().replace("displayName:", "label:", 1))
        errors = self.mutate(strip)
        self.assert_flags(errors, "displayName")


class ConfigTest(unittest.TestCase):
    def test_copy_loader_rejects_a_missing_language(self):
        import plugins

        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        data = json.loads((plugins.COPY_DIR / f"{PLUGINS[0]['id']}.json").read_text())
        data["description"].pop("th")
        (tmp / "x.json").write_text(json.dumps(data))
        original = plugins.COPY_DIR
        plugins.COPY_DIR = tmp
        try:
            with self.assertRaisesRegex(ValueError, "th"):
                plugins.load_copy("x")
        finally:
            plugins.COPY_DIR = original

    def test_descriptions_make_no_ranking_promise(self):
        for plugin in PLUGINS:
            for locale, text in plugin["copy"]["description"].items():
                self.assertNotIn("排名上不去", text, f"{plugin['id']} [{locale}]")

    def test_plugin_ids_and_skill_ids_are_unique(self):
        ids = [p["id"] for p in PLUGINS]
        skills = [p["skill"]["id"] for p in PLUGINS]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(skills), len(set(skills)))

    def test_config_is_not_mutated_by_a_build(self):
        before = copy.deepcopy(PLUGINS)
        tmp = Path(tempfile.mkdtemp())
        try:
            build.build_all(tmp)
        finally:
            shutil.rmtree(tmp)
        self.assertEqual(PLUGINS, before)


if __name__ == "__main__":
    unittest.main()
