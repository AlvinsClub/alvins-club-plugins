# Finish an edit to an existing company video

First establish which delivered video and what change the user wants. Reuse the
current result reference; otherwise use list_company_editor_videos in the intended
company and show recognizable names when several match. Do not pick by recency
alone, ask the user for internal identifiers, or create a replacement video to edit.

Use the timeline for trimming, ordering clips, adding existing footage, captions
and audio. Creation scripts and outfit forms do not perform these edits. For a
small supported edit, use the existing direct action; for visual or multi-field
choices, get_company_video_editor opens the original timeline and reads its saved
project. If that tool is unavailable, explain the missing bridge and offer an
existing verified result link; never invent a URL or claim browser edits are saved.

The internal host presents the same editor in a sidebar. An external assistant
uses the returned browser link after the user's browser permission, or offers it
for manual use. Reuse the signed-in company account; navigation permission does
not authorize uploads, exports, AI repairs, review, payment or publication. Help
with the requested edit when allowed; preview the affected scene and sound.

Choose Save project before returning. Read the SAME company and video again and
summarize the saved changes in ordinary language. A saved revision proves inputs
were persisted; source=unsaved means only browser changes may exist. Another
member's private saved project is not the current actor's draft. Conflicts or
failures keep local inputs: compare the original saved project before retrying,
never discard edits or silently replace them with another video.

Saving is not exporting. If the user requests an export, use the original editor's
explicit export action and keep its returned child video reference. Check that
video with get_company_video_editor: its parent_version_id links to the original.
Present the original result page and actual review state; an exported or approved
video is not a published video. After a lost response, inspect the original video
list and receipt before exporting again. Keep AI generation/repair and publication
as separate actions with their existing confirmations and costs.
