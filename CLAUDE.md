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
  appear anywhere outside .git, changelog history, and the project docs CLAUDE.md
  and PLAN.md (which reference upstream repo names by necessity).
- Internal seren-named files and symbols (seren.py, serenMonitor.py, the
  ico/fanart/logo/poster-seren-3 image assets, class names such as SerenPlayer)
  keep their names until plan step 6, which is deliberately deferred until after
  Phase A testing. Do not rename them earlier.
- No en dashes or em dashes in any documentation or commit messages.

## Workflow

- One commit per plan step. Show the full diff and wait for approval before committing.
- Commit messages in English, imperative mood, matching existing history style.
- After any rename or id change, verify with:
  `grep -rn "plugin\.video\.seren\|context\.seren" . --exclude-dir=.git --exclude=CLAUDE.md --exclude=PLAN.md`
- Versions are per addon: bump `version=` only for addons whose content changed in
  a release. Every plugin release updates BOTH changelog.txt AND the `<news>` block in
  addon.xml with the same entry (Kodi's "what's new" dialog reads `<news>`, not the file).
  Unchanged addons keep their version (context.axiom stays put when untouched).
- Commit message convention: single-change releases may use the inherited "Changelog X.Y.Z"
  style; multi-commit releases use descriptive imperative messages per fix, with the version
  bump and release metadata in the final commit. Release commits in the repository.axiom
  repo are always "Release Axiom X.Y.Z".
