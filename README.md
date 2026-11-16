# Alvin's Club plugins

Plugin bundles for Claude, Claude Code, Cursor, Gemini CLI and other agents. Each folder holds one plugin: manifest,
README, license, icon, the remote MCP connector URL and skills. No service code lives here.

- `brandpilot/`: Social, an AI social media manager that runs inside ChatGPT and Claude: plans, drafts and
  publishes posts for a person or a brand.
- `channel/`: Alvin's Club Channel, analyze results, draft captions and publish with approval.
- `seo/`: SEO & GEO by Alvin's Club, SEO audit and AI visibility for your website.

## Install Social

Social is a hosted MCP server, `https://studio.alvinsclub.ai/brandpilot/mcp` (streamable HTTP). It signs in with
OAuth on studio.alvinsclub.ai the first time it is used: no API key, token or local install.

### Claude and ChatGPT

Add Social from the app's connector directory, or see https://social.alvinsclub.ai/.

### Claude Code plugin

```bash
/plugin marketplace add AlvinsClub/alvins-club-plugins
/plugin install brandpilot@alvins-club
```

Then run `/mcp` and sign in to `brandpilot`. The same marketplace also lists `alvins-club-channel` and
`alvins-club-seo`.

Connector only, without the plugin:

```bash
claude mcp add --transport http brandpilot https://studio.alvinsclub.ai/brandpilot/mcp
```

### Skill only (`npx skills`)

```bash
npx skills add AlvinsClub/alvins-club-plugins --skill plan-social-content
```

This installs the `plan-social-content` skill into your agent. Add the hosted MCP server above as well: the skill
tells the agent how if the Social tools are missing.

### Gemini CLI extension

```bash
gemini extensions install https://github.com/AlvinsClub/alvins-club-plugins
```

The extension (`gemini-extension.json`) adds the hosted Social MCP server and the Social instructions.
Gemini CLI opens a browser to sign in on first use; run `/mcp auth brandpilot` to sign in again.

### Qwen Code

Qwen Code installs Claude Code marketplaces directly:

```bash
qwen extensions install AlvinsClub/alvins-club-plugins:brandpilot
```

### Cursor plugin

The Cursor plugin manifest is `brandpilot/.cursor-plugin/plugin.json` (listed in `.cursor-plugin/marketplace.json`)
with the hosted server in `brandpilot/mcp.json`. For a local install:

```bash
git clone https://github.com/AlvinsClub/alvins-club-plugins.git
ln -s "$(pwd)/alvins-club-plugins/brandpilot" ~/.cursor/plugins/local/brandpilot
```

Then reload the Cursor window and sign in to Social from Cursor's MCP settings.

### Any other MCP client

Add `https://studio.alvinsclub.ai/brandpilot/mcp` as a remote (HTTP) MCP server and sign in when asked.

Alvin's Club is a brand of EchoooMall E-commerce Pte. Ltd., operated by FUTUREVERSE TECHNOLOGIES LLC under license.
