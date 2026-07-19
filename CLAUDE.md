# Axiom

Standalone continuation of the Kodi addon Seren, based on Goldenfreddy0703/Prism 4.0.1
(commit cd37c7e), pinned BEFORE Prism's Simkl/anime pivot of July 14, 2026.
Trakt remains the core sync service. Owner: enghausen.

Task plan and full context: @PLAN.md

## Layout

- `plugin.video.axiom/` - main addon (Python, Kodi 21/22)
- `context.axiom/` - context menu addon, calls plugin://plugin.video.axiom/ internally
- Top-level `addon.xml` is a pointer file used by the repo generator, not a real manifest

## Rules

- NEVER merge or pull from the `prism` remote past cd37c7e. Upstream changes are
  cherry-picked selectively after human review, never merged wholesale.
- Trakt is the sync backend. Do not introduce Simkl or remove Trakt functionality.
- Do not use `extended=min` on Trakt watched endpoints (incompatible response shape).
- All Trakt watched/ endpoints must be paginated (get_all_pages_json). Never assume
  one request returns the full history.
- Keep LICENSE (GPL-3.0) and existing copyright notices untouched.
- The addon id is `plugin.video.axiom`. The string `plugin.video.seren` must not
  appear anywhere outside .git and changelog history.
- No en dashes or em dashes in any documentation or commit messages.

## Workflow

- One commit per plan step. Show the full diff and wait for approval before committing.
- Commit messages in English, imperative mood, matching existing history style.
- After any rename or id change, verify with:
  `grep -rn "plugin\.video\.seren\|context\.seren" . --exclude-dir=.git`
- Bump `version=` in both addon.xml files together and add a changelog.txt entry
  for every release.
