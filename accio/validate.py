"""Check a built Accio Work plugin folder against Accio's listing rules.

Covers the machine-checkable parts of "01 Plugin上架规范", the "02 Plugin技术接入规范" pre-publish checklist and
the first layer of "03 Plugin自测流程与标准". Usage: python3 accio/validate.py accio/dist/<plugin-id> [...]
"""

from __future__ import annotations

import json
import re
import struct
import sys
import tempfile
import zipfile
from pathlib import Path

from plugins import CATEGORIES, LOCALES

BRAND = "Alvin's Club"
MIS_SPELLINGS = ("Alvins Club", "Alvin’s Club", "Alvin's club", "alvin's club", "AlvinsClub ")
ANTHROPOMORPHIC = re.compile(r"\b(assistant|helper|bot|agent|expert|copilot)\b|助手|助理|小助理|管家", re.IGNORECASE)
PLUGIN_WORD = re.compile(r"\bplugin\b|插件", re.IGNORECASE)
SECRET_PATTERNS = (
    re.compile(r"\bsk-(live|test|proj|ant)?-?[A-Za-z0-9]{20,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(api[_-]?key|secret|password|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}", re.IGNORECASE),
)
SUMMARY_MAX = {"zh": 40, "zh-TW": 40, "ja": 40, "ko": 40}
SUMMARY_MAX_DEFAULT = 60
SKILL_FIELDS = ("name", "displayName", "displayDescription", "description")
TEXT_SUFFIXES = {".json", ".md", ".txt", ".js"}


def png_size(data: bytes) -> tuple[int, int]:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "-")):
            value = value.strip()
            fields[key.strip()] = json.loads(value) if value.startswith('"') else value
    return fields


def _load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing file: {path.name}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path.name}: {exc}")
    return None


def _check_name(label: str, value: str, errors: list[str]) -> None:
    if ANTHROPOMORPHIC.search(value):
        errors.append(f"{label} is anthropomorphic: {value!r}")
    if PLUGIN_WORD.search(value):
        errors.append(f"{label} must not contain the word plugin: {value!r}")
    if value[:1].islower():
        errors.append(f"{label} must start with a capital letter: {value!r}")


def _check_brand(label: str, value: str, errors: list[str]) -> None:
    for wrong in MIS_SPELLINGS:
        if wrong in value:
            errors.append(f"{label} uses brand spelling {wrong!r}; use {BRAND!r}")


def check_manifest(pkg: Path, errors: list[str]) -> dict | None:
    manifest = _load_json(pkg / "plugin.json", errors)
    if manifest is None:
        return None
    for field in ("id", "name", "displayName", "description", "version", "author", "icon", "category", "tags"):
        if not manifest.get(field):
            errors.append(f"plugin.json missing {field}")
    author = manifest.get("author")
    if author and not (isinstance(author, dict) and author.get("name")):
        errors.append("plugin.json author must be an object with a name")
    tags = manifest.get("tags") or []
    if not isinstance(tags, list) or not all(isinstance(t, str) and t.strip() for t in tags):
        errors.append("plugin.json tags must be a list of non-empty strings")
    for entry in manifest.get("mcpServers", []):
        _check_brand("plugin.json mcpServers", json.dumps(entry, ensure_ascii=False), errors)
    _check_brand("plugin.json tags", " ".join(map(str, tags)), errors)
    for field in ("name", "displayName"):
        if manifest.get(field):
            _check_name(f"plugin.json {field}", manifest[field], errors)
    if manifest.get("category") not in CATEGORIES:
        errors.append(f"category {manifest.get('category')!r} is not a standard Accio category")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", manifest.get("id", "")):
        errors.append("plugin id must be lowercase words joined by hyphens")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")):
        errors.append("version must be semantic (x.y.z)")
    summary = manifest.get("summary", "")
    if len(summary) > SUMMARY_MAX_DEFAULT:
        errors.append(f"summary is {len(summary)} characters; keep it to one short line")
    display = manifest.get("displayName", "")
    if display and display not in manifest.get("description", ""):
        errors.append("description must name the brand exactly as displayName")
    for field in ("name", "displayName", "summary", "description"):
        _check_brand(f"plugin.json {field}", str(manifest.get(field, "")), errors)
    return manifest


def check_icons(pkg: Path, manifest: dict, connector_ids: list[str], errors: list[str]) -> None:
    icon_path = pkg / "resources" / manifest.get("icon", "")
    if not icon_path.is_file():
        errors.append(f"icon file missing: {manifest.get('icon')}")
        return
    icon = icon_path.read_bytes()
    if icon_path.suffix == ".png" and png_size(icon) != (240, 240):
        errors.append(f"icon PNG must be 240x240, got {png_size(icon)}")
    for connector_id in connector_ids:
        connector_icon = pkg / "resources" / f"{connector_id}{icon_path.suffix}"
        if not connector_icon.is_file() or connector_icon.read_bytes() != icon:
            errors.append(f"connector icon {connector_icon.name} must be the same file as the plugin icon")


def check_connectors(pkg: Path, errors: list[str]) -> list[str]:
    data = _load_json(pkg / "connectors" / "connectors.json", errors)
    if data is None:
        return []
    servers = data.get("mcpServers", {})
    if not servers:
        errors.append("connectors.json declares no mcpServers")
    for name, server in servers.items():
        if not str(server.get("url", "")).startswith("https://"):
            errors.append(f"MCP server {name} needs an https url")
    return list(servers)


def check_skills(pkg: Path, errors: list[str]) -> list[str]:
    skill_ids = []
    for skill_md in sorted((pkg / "skills").glob("*/SKILL.md")):
        meta = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        for field in SKILL_FIELDS:
            if not meta.get(field):
                errors.append(f"{skill_md.parent.name}/SKILL.md frontmatter missing {field}")
        if meta.get("name") and meta["name"] != skill_md.parent.name:
            errors.append(f"skill folder {skill_md.parent.name} does not match its name {meta['name']}")
        _check_brand(f"{skill_md.parent.name}/SKILL.md", skill_md.read_text(encoding="utf-8"), errors)
        description = meta.get("description", "")
        if description[:1] in (">", "|"):
            errors.append(f"{skill_md.parent.name}/SKILL.md description must be a single-line string")
        skill_ids.append(meta.get("name", skill_md.parent.name))
    if not skill_ids:
        errors.append("no skills/<name>/SKILL.md found")
    return skill_ids


def check_i18n(pkg: Path, skill_ids: list[str], errors: list[str]) -> None:
    data = _load_json(pkg / "resources" / "i18n.json", errors)
    if data is None:
        return
    entries = data.get("entries")
    if not isinstance(entries, dict):
        errors.append("i18n.json must use the entries format")
        return
    default = data.get("defaultLocale")
    if default not in LOCALES:
        errors.append(f"defaultLocale {default!r} is not a supported language")
    required = ["plugin.displayName", "plugin.description"]
    required += [f"skill.{s}.{f}" for s in skill_ids for f in ("name", "description")]
    for key in required:
        if key not in entries:
            errors.append(f"i18n.json missing {key}")
    wanted = set(LOCALES) - {default}
    for key, values in entries.items():
        missing = sorted(wanted - set(values))
        if missing:
            errors.append(f"i18n {key} missing languages: {', '.join(missing)}")
        for locale, text in values.items():
            if not str(text).strip():
                errors.append(f"i18n {key} is empty for {locale}")
            _check_brand(f"i18n {key} [{locale}]", str(text), errors)
            if key == "plugin.displayName":
                _check_name(f"i18n {key} [{locale}]", str(text), errors)
            if key == "plugin.summary":
                limit = SUMMARY_MAX.get(locale, SUMMARY_MAX_DEFAULT)
                if len(text) > limit:
                    errors.append(f"i18n plugin.summary [{locale}] is {len(text)} characters (max {limit})")
        brand_text = entries.get("plugin.displayName", {})
        if key == "plugin.description":
            for locale, text in values.items():
                brand = brand_text.get(locale)
                if not brand or brand not in text:
                    errors.append(f"i18n plugin.description [{locale}] must name the brand")


def check_prompt(pkg: Path, errors: list[str]) -> None:
    prompt = pkg / "prompt.md"
    if prompt.is_file():
        _check_brand("prompt.md", prompt.read_text(encoding="utf-8"), errors)


def check_secrets(pkg: Path, errors: list[str]) -> None:
    for path in sorted(pkg.rglob("*")):
        if path.suffix not in TEXT_SUFFIXES or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible hardcoded secret in {path.relative_to(pkg)}")
                break


def validate_package(pkg: Path) -> list[str]:
    errors: list[str] = []
    manifest = check_manifest(pkg, errors)
    connector_ids = check_connectors(pkg, errors)
    skill_ids = check_skills(pkg, errors)
    if manifest:
        check_icons(pkg, manifest, connector_ids, errors)
    check_i18n(pkg, skill_ids, errors)
    check_prompt(pkg, errors)
    check_secrets(pkg, errors)
    return errors


def validate_zip(archive: Path) -> list[str]:
    """Validate the archive that is uploaded: one top-level <plugin-id>/ folder holding a valid package."""
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(archive) as zf:
            tops = {Path(name).parts[0] for name in zf.namelist()}
            if tops != {archive.stem}:
                return [f"zip must hold exactly one folder named {archive.stem}, found {sorted(tops)}"]
            zf.extractall(tmp)
        return validate_package(Path(tmp) / archive.stem)


def validate_path(path: Path) -> list[str]:
    if path.is_dir():
        return validate_package(path)
    if path.suffix == ".zip" and path.is_file():
        return validate_zip(path)
    return [f"not a plugin folder or .zip: {path}"]


def main(argv: list[str]) -> int:
    if not argv:
        sys.stdout.write("usage: validate.py <plugin folder or .zip> [...]\n")
        return 2
    failed = False
    for arg in argv:
        errors = validate_path(Path(arg))
        status = "OK" if not errors else f"{len(errors)} problem(s)"
        sys.stdout.write(f"{arg}: {status}\n")
        for error in errors:
            sys.stdout.write(f"  - {error}\n")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
