"""Accio Work listing config for the four Alvin's Club plugins.

One entry per plugin. English is the default locale and lives in plugin.json / SKILL.md; every other
locale goes to resources/i18n.json. Rules come from Accio's "01 Plugin上架规范" and "02 Plugin技术接入规范".
User-facing copy for every language lives in copy/<plugin-id>.json so a native speaker can review it there.
"""

import json
from pathlib import Path

LOCALES = ("en", "zh", "zh-TW", "ja", "ko", "it", "fr", "de", "es", "pt", "ru", "ar", "th", "vi")

# Standard category keys from Accio's "2.3 Plugin分类清单".
CATEGORIES = (
    "e-commerce-marketplaces",
    "marketing-advertising",
    "social-media",
    "communication-collaboration",
    "productivity-knowledge",
    "business-operations",
    "creative-design",
    "payments-finance",
    "logistics-fulfillment",
    "developer-data-tools",
    "events-programs",
    "others",
)

AUTHOR = {
    "name": "FUTUREVERSE TECHNOLOGIES LLC",
    "email": "service@alvinsclub.ai",
    "url": "https://www.alvinsclub.ai/",
}

ICON_SOURCE = "channel/assets/icon.png"  # the shared Alvin's Club app icon used by every plugin

ACCIO_SIGN_IN = (
    "ask the user to connect it under App authorization on this plugin's page; "
    "sign-in happens on studio.alvinsclub.ai, never in chat"
)

UNVERIFIED_APP_OLD = "tell the user to do that step from Claude or the Alvin's Club website."
UNVERIFIED_APP_NEW = "tell the user to do that step on the Alvin's Club website."

STUDIO = {
    "id": "alvins-club-studio",
    "name": "Alvin's Club Studio",
    "category": "creative-design",
    "homepage": "https://studio.alvinsclub.ai/",
    "connector_id": "alvins-club-studio",
    "mcp_url": "https://studio.alvinsclub.ai/studio/mcp",
    "tags": ["product video", "ecommerce video", "tiktok video", "reels", "lookbook", "ai video"],
    "skill": {
        "id": "studio-get-started",
        "source": "accio/vendor/studio/skills/get-started",
        "replacements": [
            (
                "Connect the bundled Alvin's Club Studio MCP connector before calling its tools. If it is "
                "disconnected, direct the user to the plugin's Connectors tab and its hosted OAuth flow; "
                "credentials belong on studio.alvinsclub.ai, not in chat.",
                "Connect Alvin's Club Studio before calling its tools. If it is disconnected, "
                + ACCIO_SIGN_IN + ".",
            ),
        ],
    },
}

SOCIAL = {
    "id": "alvins-club-social",
    "name": "Alvin's Club Social",
    "category": "social-media",
    "homepage": "https://social.alvinsclub.ai/",
    "connector_id": "alvins-club-social",
    "mcp_url": "https://studio.alvinsclub.ai/brandpilot/mcp",
    "tags": ["social media", "content calendar", "content plan", "post scheduling", "brand matrix"],
    "skill": {
        "id": "plan-social-content",
        "source": "brandpilot/skills/plan-social-content",
        "replacements": [
            (
                "Use the bundled Social connector. If it is not connected, ask the user to connect it from this "
                "plugin's\nConnectors tab; sign-in happens on studio.alvinsclub.ai, never in chat.",
                "Use Alvin's Club Social. If it is not connected, " + ACCIO_SIGN_IN + ".",
            ),
            (
                "this skill was\ninstalled without its connector. Tell the user to add the hosted Social MCP server,\n"
                "`https://studio.alvinsclub.ai/brandpilot/mcp` (streamable HTTP, OAuth sign-in, no token), and "
                "continue once it is added:\n"
                "- Claude Code: `claude mcp add --transport http brandpilot https://studio.alvinsclub.ai/brandpilot/mcp`, "
                "then `/mcp`\n  to sign in.\n"
                "- Claude or ChatGPT: add Social from the app's connector directory.\n"
                "- Other MCP clients: add the URL as a remote (HTTP) MCP server and sign in when asked.",
                "Alvin's Club Social is not connected yet: " + ACCIO_SIGN_IN + ", and continue once it is connected.",
            ),
        ],
    },
}

SEO = {
    "id": "alvins-club-seo-geo",
    "name": "Alvin's Club SEO & GEO",
    "category": "marketing-advertising",
    "homepage": "https://seo.alvinsclub.ai/",
    "connector_id": "alvins-club-seo-geo",
    "mcp_url": "https://studio.alvinsclub.ai/seo/mcp",
    "tags": ["seo", "seo audit", "geo", "ai visibility", "google search console", "shopify seo"],
    "skill": {
        "id": "seo-geo-get-started",
        "source": "seo/skills/get-started",
        "replacements": [(UNVERIFIED_APP_OLD, UNVERIFIED_APP_NEW)],
    },
}

CHANNEL = {
    "id": "alvins-club-channel",
    "name": "Alvin's Club Channel",
    "category": "social-media",
    "homepage": "https://studio.alvinsclub.ai/channel/connect",
    "connector_id": "alvins-club-channel",
    "mcp_url": "https://studio.alvinsclub.ai/channel/mcp",
    "tags": ["social media analytics", "captions", "post scheduling", "tiktok", "youtube shorts", "publishing"],
    "skill": {
        "id": "channel-get-started",
        "source": "channel/skills/get-started",
        "replacements": [(UNVERIFIED_APP_OLD, UNVERIFIED_APP_NEW)],
    },
}

COPY_DIR = Path(__file__).resolve().parent / "copy"
COPY_FIELDS = ("summary", "description", "skill_name", "skill_description")


def load_copy(plugin_id: str) -> dict[str, dict[str, str]]:
    """User-facing text for one plugin in every locale, from copy/<plugin-id>.json."""
    data = json.loads((COPY_DIR / f"{plugin_id}.json").read_text(encoding="utf-8"))
    for field in COPY_FIELDS:
        missing = [locale for locale in LOCALES if not data.get(field, {}).get(locale)]
        if missing:
            raise ValueError(f"copy/{plugin_id}.json {field} missing: {', '.join(missing)}")
    return data


PLUGINS = tuple({**plugin, "copy": load_copy(plugin["id"])} for plugin in (STUDIO, SOCIAL, SEO, CHANNEL))

# Applied to every built skill so the brand reads the same everywhere a user can see it.
BRAND_REWRITES = (("SEO & GEO by Alvin's Club", "Alvin's Club SEO & GEO"),)
