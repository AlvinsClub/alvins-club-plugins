# Accio Work packages

Builds the four Alvin's Club plugins for the Accio Work plugin market: Alvin's Club Studio, Alvin's Club Social,
Alvin's Club SEO & GEO and Alvin's Club Channel. Each package points at the same hosted MCP server and reuses the
same skill as the Claude plugin, rewritten only where the skill names another app.

```bash
python3 accio/build.py                         # writes accio/dist/<id>/ and accio/dist/<id>.zip, then validates
python3 accio/validate.py accio/dist/*         # check folders and the zips you upload against the listing rules
python3 -m unittest discover -s accio -v       # tests (macOS: the build resizes the icon with sips)
```

| Package | Category | MCP server | Skill source |
| --- | --- | --- | --- |
| `alvins-club-studio` | creative-design | `/studio/mcp` | `vendor/studio` (copy of ecn-muse `plugin/claude`, see `vendor/studio/SOURCE`) |
| `alvins-club-social` | social-media | `/brandpilot/mcp` | `brandpilot/skills/plan-social-content` |
| `alvins-club-seo-geo` | marketing-advertising | `/seo/mcp` | `seo/skills/get-started` |
| `alvins-club-channel` | social-media | `/channel/mcp` | `channel/skills/get-started` |

Copy for every language (summary, description, skill name and description) is in `copy/<plugin-id>.json`, one
file per plugin, for native-speaker review. English is the default locale and goes into `plugin.json` and
`SKILL.md`; the other 13 Accio languages go to `resources/i18n.json` (Accio's 02 doc: the default locale is not
repeated in `entries`). Descriptions must not claim more than the skill and tools do: Accio rejects that.

What `validate.py` enforces (from Accio's "01 Plugin上架规范", "02 Plugin技术接入规范" and the first layer of
"03 Plugin自测流程与标准"): no anthropomorphic names (Assistant, Helper, Agent, 助手 ...) and no "plugin" in names;
one standard category; one brand spelling, "Alvin's Club", everywhere a user can see it; the brand named in every
description; a 240x240 icon that is the same file for the plugin and its connector; `entries`-format i18n covering
all 14 languages; complete skill frontmatter; no hardcoded secrets.

When a source skill changes, rebuild. If a sentence the build rewrites has changed, the build stops and names it:
update the replacement in `plugins.py`. To refresh Studio's skill, copy `plugin/claude/skills/get-started` from
ecn-muse `origin/main` into `vendor/studio/skills/get-started` and update `SOURCE`.

Open with Accio: whether a plain `connectors.mcpServers` http entry with the server's own OAuth shows the
"应用授权" card, or whether a full `oauth` connector definition is needed. Confirm on Accio Work 0.20.0+ with
"插件 → 导入本地插件" before submitting.
