# Audit: tech debt and drift

Last updated: 2026-11-13 (America/New_York). Audited commit: `6622ca6` on `main`.

Four read-only audits: Hevy push path, date handling, source of truth, general
debt. Nothing was changed in the repo or in Hevy. V = verified by running or
observing, I = inferred from reading code.

## State that needs reconciling before the next sync or push

| Item | Detail |
|---|---|
| Thursday 12 Nov workout | Started 19:22 ET from a routine titled "L2 Lower B (Fri 13 Nov)": deadlift 160 x 5 @ 8, front squat, reverse lunge. The repo says Thursday was Full B, state "planned". Not yet in `data/history.csv`. A pull will date it 2026-11-13 and move the pointer L2 to U2, while the plan has L3 Saturday, U3 Sunday. (V) |
| Hevy is ahead of `main` | Live routines were rewritten 2026-11-14 03:43Z with deadlift 170 (H) and 155 (V). `main` has deadlift 150 and `last_push` 2026-11-13T00:18Z. Likely source: the scheduled "Sunday training check-in", which fired 03:40Z and whose run is marked FAILED; its turn 1 syncs and pushes before any commit. (push V, source I) |
| `data/weekly-plan.md` | Block week says 2 of 6 (tracks.json says 3); lines 42-46 and 60-61 carry residue of the withdrawn Fri-Sun plan; line 82 says routines were "pushed" when the commit says the push was pending. (V) |

## Root causes

### 1. No time zone anywhere in `tools/`

| Finding | Evidence | |
|---|---|---|
| Workout date is the UTC date of `start_time` | `hevy_api.py:258`, `hevy_pull.py:125` | V |
| "Today" is the container's UTC date | `hevy_push_routines.py:538`, `update_tracks.py:560`, `build_dashboard.py:363`, `analyze_history.py:82` | V |
| Raw `start_time` is not stored, so dates cannot be re-derived offline | `history.csv` has no timestamp column | V |
| Date-based dedup can skip a second session with the same stored date | `update_tracks.py:470` (`date <= processed_through`) | I |
| Tests assert the UTC slice as correct | `test_tools.py:668-679` | V |
| Only `coach/README.md:26` and `nightly-brief.md:11` use the Eastern date, then call tools that use UTC | | V |

Since 1 Nov, 7 pm ET is 00:00 UTC. The nightly brief runs at 7:47 pm ET, so
every run lands on the next UTC date. Seven stored workouts (2024) are dated a
day late; none changes a week bucket. The pull cursor (`last_pull`) and the
dashboard JavaScript are sound.

### 2. Pushes can be skipped without a message and are never checked

| Finding | Evidence | |
|---|---|---|
| "This Week" sessions dated before UTC today are skipped silently | `hevy_push_routines.py:513` | V |
| `this_week` in `data/hevy-state.json` is written only by hand; `coach/*.md` never mention it | grep | V |
| No read-back after a PUT; "Updated" means HTTP 200 only | `:517`, `:582` | V |
| `last_push` is one global timestamp, also written after `--only` runs that skip `this_week` | `:589-592` | V |
| An error on one routine aborts the rest; dated routines go last | `:578-597` | I |
| A deload decided on Sunday never reaches the push; `last_push_deload` is read nowhere | | I |
| `hevy_sync.py --dry-run` still pulls and rewrites `history.csv` and `last_pull` | `hevy_sync.py:42-44` | V |
| The push dry-run never renders `this_week` | `:541-546` | V |
| Saving a workout back to its routine in the app overwrites it; the tool never notices | routine `a1de5676` | V |

Units are correct on push and pull. No orphan or duplicate routines: 16 live,
all known to the state file.

### 3. Each fact has several hand-maintained copies

| Fact | Copies | Read by code |
|---|---|---|
| Loads, pointer, block week | `data/tracks.json`, `track-state.md` (hand prose plus generated table), `weekly-plan.md`, `this_week` notes, `body-composition.md`, dashboard | `tracks.json` |
| This week's schedule | `weekly-plan.md`, `hevy-state.json` `this_week`, check-ins, calendar holds | `hevy-state.json` |
| Session contents | `templates/rotation.json`, four day templates, liftoscript, `templates/README.md` | `rotation.json` |
| Progression rules | `progression-tracks.md`, constants in update, push and dashboard code, template briefs, guide/03, guide/07, guide/08 | code constants |
| e1RM | `tracks.json` (unrated = 2 RIR), dashboard (unrated = 0 RIR) | two formulas |

Disagreements found (all V):

- `tracks.json` is not reproducible. Replaying `history.csv` gives squat 160
  (live 155), pulldown 100 (live 125), block start 2026-11-10 (live 2026-10-27).
  Hand amendments: `f3d4de5`, `5dbda5e`, `9062b79`, `94065d8`.
- `track-state.md:11` says pointer L1, `:21` says L2; `:12` says block week 1.
- Thursday's deadlift: plan note says 150 x 4, the renderer gives 145 x 4.
- Squat e1RM is 191, 180.8 or 186 depending on the file; deadlift 174 or 157.5.
- Gap table exists three times with two behaviours (dashboard says hold squat,
  push renders the planned 155).
- Miss rule: RPE 9.5-10 in `progression-tracks.md` and code, RPE 10 in the four
  template briefs and guide/03.
- `rotation.json` vs day templates: L2 lunge variant, L3 leg extension sets,
  leg curl and calf supersets, pull-up V prescription.
- Liftoscript unchanged since 26 Oct, in kg, without the November rules.
- `history-summary.md` stale since 21 Oct. `manual-log.csv` is read by no tool.

Only the `track-state.md` table carries a "generated" marker.

### 4. Scheduled runs and process

| Finding | |
|---|---|
| Sunday check-in turn 1 runs the full sync (pushes to Hevy) and ends without a commit; no reply means Hevy and `main` diverge | V |
| No commit in 105 matches the runbook formats `Check-in <date>:` or `Brief <date>:`; the scheduled runs appear not to commit | V / I |
| A third task, "Sunday workout hold planning", is undocumented, fires 47 minutes before the check-in, uses the work calendar, and tells the agent to trust live Hevy over the repo | V |
| `PORTABILITY.md` says no scheduled tasks exist and still points at the old repo name | V |
| Runs commit straight to `main` with no rebase or conflict rule; `dashboard/index.html` is one 49k-character line, so any two syncs conflict | V |
| No atomic writes; a crash mid-write truncates `tracks.json` | V |
| "Nine routines" in CLAUDE.md, README, coach and guide/07; the tool pushes 12 plus dated copies | V |
| 21 merged `claude/*` remote branches not pruned; seven commits exist only to record `last_pull` or `last_push` | V |
| Untested: `hevy_pull.py`, `hevy_sync.py`, API retry, `push_this_week`. Tests read live data files | V |

No secrets found in the tracked tree. 62 tests pass.

## Recommended order of work

1. **Time zone.** One `tools/localtime.py` (`TRAINING_TZ`, default
   America/New_York) with `local_today()` and `local_date()`. Store
   `start_time` in `history.csv`. Dedup on `workout_id`. One full pull to
   re-date. Tests at 00:22Z and 23:30Z.
2. **Push that reports and verifies.** Print every skip with its reason, push
   `this_week` first, continue past per-routine errors, read back and diff,
   exit non-zero on mismatch, record per-routine push state. Real `--dry-run`.
3. **One schedule file.** Move `this_week` to `data/week.json` with a tool
   command to set it; generate the weekly-plan tables from it; call it from
   the Sunday and nightly runbooks.
4. **`tracks.json` as the only load store.** Hand amendments go in an
   overrides file so a replay reproduces it. Generate all state in
   `track-state.md`. One gap function, one e1RM function, one constants block.
5. **Scheduled tasks.** Sync commits its own outputs before the turn ends.
   Merge or remove the hold-planning task. Record all tasks in
   `PORTABILITY.md`. Add a rebase-and-regenerate rule.
6. **Clean-up.** Generate or delete the template session tables and
   liftoscript, drop `manual-log.csv` or ingest it, fix "nine routines",
   atomic writes, shared `tools/common.py`, prune branches.
