# Alvin's Club Channel

Decide what to post next from your own results, then publish with your approval: TikTok, Instagram, YouTube Shorts,
X, LinkedIn and Pinterest, right in Claude. Start by saying: "Connect my social accounts in Alvin's Club Channel."

## What is in this plugin

- `.mcp.json`: the remote Channel connector, https://studio.alvinsclub.ai/channel/mcp (OAuth sign-in on
  studio.alvinsclub.ai; you can connect first and add your email later).
- `skills/get-started`: how Claude analyzes your history, drafts copy and publishes only after your approval.

It contains Markdown instructions and JSON configuration only: no local executables, hooks, install scripts or
package launchers, and no credentials.

## Data it sends

Tool calls send what the request needs to Channel's hosted service: the platforms you connect (through each
platform's own consent page and a one-time link), the account and post history you ask it to analyze, draft captions
and the exact posts you approve for publishing. Nothing is published without your explicit approval of that post.

- Documentation: https://studio.alvinsclub.ai/channel/mcp-guide
- Privacy policy: https://studio.alvinsclub.ai/privacy
- Terms: https://studio.alvinsclub.ai/terms
- Support: service@alvinsclub.ai

Alvin's Club is a brand of EchoooMall E-commerce Pte. Ltd., operated by FUTUREVERSE TECHNOLOGIES LLC under license.
