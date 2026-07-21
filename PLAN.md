# Axiom, project plan

Axiom is a standalone continuation of the Kodi addon Seren, based on Goldenfreddy0703/Prism
version 4.0.1 (commit cd37c7e, March 2026), pinned BEFORE Prism's pivot to Simkl/anime
(July 14, 2026 onward). Repo: https://github.com/enghausen/Axiom

Motivation: full ownership of the code, no automatic updates from third party repos,
Trakt stays the core sync service.

## Remotes

- origin: git@github.com:enghausen/Axiom.git (master, pinned at cd37c7e at start)
- prism: https://github.com/Goldenfreddy0703/Prism (upstream, NEVER merge past cd37c7e)
- spongehead: https://github.com/MrSpongeHead/plugin.video.seren (one-line Trakt fix, superseded by step 3)
- inb4after: https://github.com/inb4after/plugin.video.seren (alternative Trakt fix, superseded by step 3)
- nixgates: https://github.com/nixgates/plugin.video.seren (original, dead since Nov 2024, reference only)

## Commit plan (one commit per step, in order, review diff between each)

### 1. Rename to Axiom
- Folder plugin.video.seren -> plugin.video.axiom, context.seren -> context.axiom
- addon.xml in both: id, name="Axiom", provider-name="enghausen"
- context.axiom: all internal plugin://plugin.video.seren/ calls -> plugin.video.axiom
- Dependency in plugin.video.axiom/addon.xml: context.seren -> context.axiom
- Top-level addon.xml (pointer file for the repo generator): update path
- Verify: `grep -rn "plugin\.video\.seren\|context\.seren" . --exclude-dir=.git` returns 0 hits
  (changelog.txt history entries excepted)
- No other changes in this commit

### 2. Remove anime features (from Prism 4.0.1)
- Remove the Discover Anime home menu entry in resources/lib/gui/homeMenu.py
- Remove anime routes in resources/lib/modules/router.py
- Delete resources/lib/gui/animeMenus.py, the anime home menu icon
  (resources/images/icons/anime.png) and language strings 30658-30717 in all locales.
  Decision: remove the feature completely instead of leaving dead code. Rationale:
  no upstream we would cherry-pick from contains the anime code, so the merge
  friction argument does not apply, and mixed upstream commits can be cherry-picked
  partially anyway.
- Keep the metadataHandler genre label (string 30494), the getSources isanime
  scraper hint and resources/images/genres/anime.png: playback and genre plumbing,
  not the feature
- Verify: py_compile on touched files; repo-wide case-insensitive grep for anime
  returns only the genre label and scraper hint (changelog history excepted);
  Kodi home menu shows no anime entries, no ImportError in log

### 3. Trakt API fix (changes enforced by Trakt on June 30, 2026: forced pagination + new extended semantics)
File: resources/lib/database/trakt_sync/activities.py

Line ~307, sync_watched_episodes, replace:
    trakt_watched = self.trakt_api.get_json("sync/watched/shows", extended="full")
with a paginated call:
    trakt_watched = [
        show
        for page in self.trakt_api.get_all_pages_json(
            "sync/watched/shows", extended="progress", limit=100, ignore_cache=True
        )
        for show in page
    ]

Line ~230, sync_watched_movies, replace:
    trakt_watched = self.trakt_api.get_json("/sync/watched/movies", extended="full")
with:
    trakt_watched = [
        movie
        for page in self.trakt_api.get_all_pages_json(
            "/sync/watched/movies", limit=250, ignore_cache=True
        )
        for movie in page
    ]

Rationale: extended=full is now ignored (no season data -> Next Up breaks), extended=progress
is required and capped at 100/page, unpaginated calls return only the first 100 items.
get_all_pages_json already exists in resources/lib/indexers/trakt.py and stops correctly
on the X-Pagination-Page-Count header.
IMPORTANT: extended=min must NOT be used (different response shape, see SpongeHead's revert).
No changes to trakt.py itself.
Fallback experiment if show metadata comes back incomplete during testing:
try extended="full,progress" (inb4after's variant) instead of "progress".

### 4. README and .gitignore
- New README: Axiom description, attribution (Seren by nixgates, continued by Goldenfreddy0703,
  Trakt fix informed by MrSpongeHead and inb4after), GPL-3.0 note. LICENSE file untouched.
- .gitignore: __pycache__/, *.pyc, .idea/, .DS_Store, zips/

### 5. Version bump
- plugin.video.axiom/addon.xml: version 4.1.0 (marks the independent line)
- context.axiom/addon.xml: corresponding bump
- changelog.txt: new entry describing rename, anime removal and Trakt fix

### 6. Complete internal rename (DEFERRED until after Phase A testing)
- Rename seren.py -> axiom.py including the library= reference in addon.xml
- Rename serenMonitor.py -> axiomMonitor.py including all imports
- Rename the image assets (ico-seren-3.png, fanart-seren-3.jpg, logo-seren-3.png,
  poster-seren-3.png) in both addons including the addon.xml asset references
- Rename internal symbols (SerenPlayer, SerenMonitor, SEREN_ADDON_ID and similar)
  and the Seren mentions in skin XML comments
- Deliberately deferred so rename risk is not mixed into the Trakt verification
  of Phase A. Execute only after all Phase A checks pass.

### 7. Own API identities and artwork (after step 6)
- Register own API applications so the addon stops authenticating with inherited
  Seren credentials, which depend on upstream registrations that could be revoked
  or rate-limited:
  - Trakt: create an application named Axiom (app.trakt.tv Settings, Apps section,
    redirect URI urn:ietf:wg:oauth:2.0:oob, scrobble permission enabled).
    Note: the trakt.clientid / trakt.secret settings already exist and override the
    hardcoded defaults, so new keys can be tested via settings before changing code.
  - Debrid providers: register an Axiom app in their API/app sections, swap the
    hardcoded client ids in the source to the new defaults
  - Audit the source for any other hardcoded inherited credentials
- New original Axiom artwork: icon.png, fanart, and skin images
- User-facing consequence: all devices must re-authenticate when keys change,
  so ship this as one clean cutover release
- After this step the only remaining Seren traces are LICENSE and README attribution, by design.

## Verification

### Phase A: direct zip install (no repository needed)
Status: PASSED 2026-07-21. All checks green on a Kodi 21 test install; watched/collection
counts verified exactly against the Trakt API including libraries above the 100-item
page cap. Known inherited issues logged for later: hang on Kodi exit (service shutdown
handling), one remaining resumetime/setResumePoint deprecation warning.
1. Zip the addon folders (folder must be the top level entry inside the zip)
2. Install via "Install from zip file" on a test device, context.axiom first,
   then plugin.video.axiom (new addon id means a fresh configuration)
3. Checks:
   - Full Trakt sync / rebuild database without errors
   - Next Up shows correct episodes
   - Watched show and movie counts match the Trakt profile (verifies pagination,
     critical for libraries above 100 items)
   - Shows have title/artwork/metadata (extended=progress returns a minimal show
     object, milling must fill in the rest)
   - Playback and scrobble back to Trakt work
   - Context menu (context.axiom) works on an arbitrary item
   - kodi.log: no exceptions/tracebacks from plugin.video.axiom

### Phase B: own repository (update channel)
1. New GitHub repo: repository.axiom (empty, public). The repository serves Axiom as the
   main addon and can host future helper addons alongside it.
2. Local layout in a sibling folder to this repo: the repository.axiom addon
   (xbmc.addon.repository extension), _repo_generator.py downloaded from
   https://raw.githubusercontent.com/Goldenfreddy0703/repository.hooty/master/_repo_generator.py
   (GPL, the drinfernoo template lineage), and a build step that copies the two addon
   folders from the Axiom source repo before generating, so the addon source stays
   single-homed in the Axiom repo. Output in repo/zips/.
3. repository.axiom addon.xml with info/checksum/datadir pointing at
   https://enghausen.github.io/repository.axiom/repo/zips/
4. Run generator, commit, enable GitHub Pages (master, root)
5. Verify the update flow: bump the version, regenerate, push, "Check for updates"
   in Kodi, confirm the update is offered and installs
6. Later: GitHub Action in the Axiom repo that builds and pushes to repository.axiom automatically

## Must NOT happen

- No merging of prism/master past cd37c7e (Simkl pivot, anime expansion, Prism rename)
- No extended=min on watched endpoints
- LICENSE (GPL-3.0) and existing copyright notices remain untouched
- No en dashes or em dashes in documentation
