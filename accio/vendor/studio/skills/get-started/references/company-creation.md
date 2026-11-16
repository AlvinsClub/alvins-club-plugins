# Shared company creation workflow

Use the original authorized company workspace and creation draft for complex scripts,
material roles and multi-field editing. Never move a company task into a personal
workflow or make a personal/simple request require a company. Read the current draft
before editing, preserve unrelated inputs, and apply only the user's requested changes.
A conflict means reload and reconcile, never overwrite. Use current catalog choices
and original attachment references; never invent identities or change wallet/roles.

Reuse the same draft and original operation after saving, returning or reconnecting.
Only the service response proves what was saved or accepted; a redirect, closed panel
or a spoken “done” is not confirmation. Opening or saving does not start production.
Browser permission only permits navigation or the agreed input, not payment or
execution. Without browser assistance, offer the original returned link for manual
input; do not invent an editor URL. Cancellation keeps the draft. Wrong-account errors
require the correct account, not another draft or copied credentials.

Keep preparation, business confirmation and accepted work distinct. Use the host's
original confirmation path, and never duplicate an approval already in its form.
Do not transfer a session grant or allowance between hosts. Query the original receipt
after uncertainty; do not start another order to discover its status. Acceptance is
not completion: report actual progress, videos, failure and settlement in plain language.

Company creation from the assistant (when available)
- Use `get_creation_workspaces` to choose an authorized company; `open_company_creation_form` returns its saved draft and form link. Use a stable `request_key` to create, or the original `draft_id` to reopen. Keep its `company_id`, `draft_id` and `browser_url`; opening retries reuse that key.
- Fill the draft in the conversation: `get_company_creation_options` lists the merchants and, for one merchant, its products and presenters; `update_company_creation_draft` saves the chosen merchant, product, presenter, brief and settings at the draft's current revision. Ask only for what is missing; never invent product facts.
- A product photo is needed before a quote. `add_company_creation_photo` adds one from a public https link. A photo or file that exists only on the user's computer is added on the form: offer `browser_url` for that step (same Studio account; put no credentials in links). Opening a browser only permits navigation, not payment or execution. Then read the draft again with `get_company_creation_draft`. Do not assume native URL elicitation exists.
- When the inputs are complete, `quote_company_creation` returns the exact cost in company credits. Say what will be made and that cost, and wait for a clear yes. Then `confirm_company_creation` with that cost starts exactly the quoted video and holds it from the company budget; `decision="reject"` declines it. A refusal about company credits or a budget is the company's, never the user's personal balance: relay it as written.
- After a timeout or an unclear result, call `get_company_creation_draft` for that SAME company and draft and read its operations; never quote or confirm again to recover an uncertain order. Do not transfer internal approvals or allowances.
- Missing tools retain the older advanced quote workflow; do not fabricate a form URL. Company drafts are separate from personal product `plan_ref` records and cannot replace or convert them.
- Company videos after production: `list_company_review_videos` shows the videos this member may see with their review state, classification and current revision (a sub-account sees only its own). `classify_company_videos` gives a batch one mutually exclusive classification: a sub-account may only choose discard or submit for review; the main account, after approving, chooses "we may publish it ourselves (not for the merchant)" or "for the merchant", and discards a video by disapproving it with a reason in `review_company_video`. A classification or an approval only records the decision: nothing is sent, delivered or published. Use one new `operation_key` per decision and reuse it only to retry that same decision.
- A product defect in one part of a finished company advanced video: `inspect_company_video`, then `quote_company_video_repair` (nothing held) and, after a clear yes to its credits, `repair_company_video`. It is held and charged on the company budget, never the personal balance; relay a company credit or budget refusal as written.
