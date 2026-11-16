# Finish an edit to an existing personal video

Establish which delivered video the user means and what should change. Reuse the
current video reference or the existing authorized video list/history; if several
match, show recognizable names and ask which one. Do not pick by recency alone,
ask for internal IDs, or create a replacement order just to open an editor.

Use the timeline for trimming, rearranging footage, subtitles and audio. Changing
how a scene looks through AI is a separate repair task with its existing costs and
confirmation. Scripts and outfit forms are not the timeline. For visual or several
related choices, get_video_editor returns the original editor and saved inputs.
Keep source_id and source_kind from the existing result: video is the default;
exact, marketing and edit use their original references. Do not guess conversions.
Company results use the company editor, not a personal account workaround.

Internally use the same editor in the conversation sidebar. Externally offer the
returned browser link, and assist in the browser only with the user's permission.
If access is refused, keep the current work and offer the manual link. Browser
permission is not permission to upload, export, spend, repair, approve or publish.
Older hosts without the tool may offer an existing verified editor link; do not
invent a URL or claim that an unsupported action succeeded.

Preview the affected scene/sound, choose Save editing project, then read the SAME
source again. Summarize what was saved in ordinary language. source=unsaved means
there is no confirmed server draft. A browser-only change is not saved: do not
claim success from navigating or typing. Conflicts keep local input; open the
current server draft separately to compare before retrying, never overwrite it or
silently switch videos. Account/source changes require reopening in the intended
account. Saving retains the original media's availability period, not unlimited
storage.

Saving is not exporting. If the user asks for an export, use the original editor's
explicit action and retain its job_id and original status/result link. Read that
child with source_kind=edit; its root identifies the original source, while its
saved draft is independent. After a lost export response, inspect the original
export history/status before submitting again. Deliver the actual result/link;
exporting is not generation, business approval or publication.
