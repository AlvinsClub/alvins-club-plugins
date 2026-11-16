# Plan an outfit video around the user's intended scene

Separate garments changing in order are an outfit rotation. A main garment and
accessories worn together are one styling combination. Clarify that distinction
only when the request is ambiguous; keep known products, colours and presenter.
Use current options for supported categories, look counts, length and price.
Do not silently replace an unavailable model or turn a template remake into an
exact face/voice replica. Reference rights require the user's own confirmation.

Simple choices stay in conversation. If the user wants to arrange many products,
compare photos or edit detailed directions, recommend the existing outfit form;
open it only after they choose it. `open_advanced_creation_form` accepts
`composition_mode: rotation` or `styling` when that host provides this capability.
Omitting the optional mode keeps the script/photo form. Company work stays in its
authorized company form, not a new personal draft.

Find and reopen a known draft before creating another. Keep its original draft_id,
selected material, product order and saved photos. After a disconnect or lost
response, reopen that same record. A new request key must not be used to guess
whether earlier work succeeded. Internal assistants use the returned sidebar;
external assistants use the original browser link and the host's granted browser
permission. Opening permission does not imply saving or production permission.

Help the user finish the task: verify the main garment, ordered looks or factual
accessory categories, presenter and creative direction. Show the practical changes
before saving. Incomplete drafts may be saved without starting a video. Preserve
inputs on failure or conflict, compare the same saved draft and retry only the
intended save. Never describe browser-only edits as stored by the service.

After saving, use `get_advanced_creation_draft` to verify the same record. Summarize
the actual garments, order, photos and remaining choices; do not show internal IDs,
revisions or execution JSON. Saving and returning to chat are not production
approval. Review the current total and confirm creation separately in the original
form. Follow its original submission receipt after an uncertain result; do not send
the saved inputs into a second creation tool or another draft.
