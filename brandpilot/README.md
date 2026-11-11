# BrandPilot by Alvin's Club

Plan and run social media content for yourself or your brand across X, LinkedIn, TikTok, YouTube Shorts, Instagram
and Hashnode from one brief, right in Claude.

Start by saying: "Draft a week of posts for my brand with BrandPilot." Give your website or the social profile you
post from. BrandPilot drafts your brief, shows example posts written for you, then helps you connect your accounts,
approve posts and choose how they publish, all in the chat.

## What is in this plugin

- `.mcp.json`: the remote BrandPilot connector, https://studio.alvinsclub.ai/brandpilot/mcp (OAuth sign-in on
  studio.alvinsclub.ai; you can connect first and add your email later).
- `skills/plan-social-content`: how Claude runs the first setup and everyday requests.

It contains Markdown instructions and JSON configuration only: no local executables, hooks, install scripts or
package launchers, and no credentials.

## Data it sends

Tool calls send what the request needs to BrandPilot's hosted service: the brief you approve (name, website or
profile link, audience, goals), the platforms you choose to connect, edits to draft posts, the posts you approve,
the publishing mode you choose and report requests.
Connecting a social account happens on that platform's own consent page through a one-time link. Posts publish
according to the publishing mode you choose (automatic by default, after your review, or a week at a time).

- Documentation: https://studio.alvinsclub.ai/brandpilot/mcp-guide
- Privacy policy: https://studio.alvinsclub.ai/privacy
- Terms: https://studio.alvinsclub.ai/terms
- Support: service@alvinsclub.ai

Alvin's Club is a brand of EchoooMall E-commerce Pte. Ltd., operated by FUTUREVERSE TECHNOLOGIES LLC under license.
