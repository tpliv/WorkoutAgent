# 07. Tracking and apps

Last updated: 2026-11-13 (Hevy loop described as it runs now: 12 routines plus the dated This Week copies, one sync command that publishes to `main` before it updates Hevy and reads each routine back, `tools/week.py` for the week, the lifter's dates, the key as a network secret; Liftosaur rendering marked unmaintained; logging and rule restatements matched to `templates/progression-tracks.md`). Earlier: 2026-11-10 (section 4: row and pulldown variants count; moved top sets); 2026-10-21 (Hevy section revised the same day after the API schema was verified; units switched to pounds the same day; app facts revised again the same day after the official-source check)

Revision 2026-10-21: prices, platforms, watch apps, Premium gates, export formats and the Liftosaur API re-checked against vendor sites, US App Store and Google Play listings and the Liftosaur docs and source. Source: `research/mobile-workout-trackers.md`, section "Addendum 2026-10-21: official-source verification (open internet)". Settled items lost their **(unverified)** flags; the ones still open keep them.

**The question this chapter answers:** "Which mobile tracker can run this rotation, and how do the agents in this repo read my training data back?"

**The short answer:** log load and reps for every set, and an RPE on the top set of each main lift. Use **Liftosaur** if you want the app itself to run the progression tracks (an agent writes a Liftoscript file in this repo, you paste it in). Use **Hevy Pro** if you want an agent to push routines and pull your history over an API (the agent then does the progression arithmetic, because Hevy has none); this repo ships that loop in `tools/`, and it is the one the lifter runs. The Liftosaur file in this repo is from October 2026 and is not maintained (section 3.1). Use **Boostcamp** (free, manual entry) or **Strong** (manual entry, CSV out) if you want a conventional tracker. Whatever you use, the eight-column CSV in section 5 is the interchange format this repo reads.

Evidence base: `research/mobile-workout-trackers.md` (2026-10-21). The note's first pass could not open liftosaur.com, api.hevyapp.com or apps.apple.com, so it leaned on search summaries and competitor blogs. Two addenda of the same day replaced most of that with primary sources: the Hevy API was checked against the official OpenAPI document, and an official-source pass checked vendor sites, US App Store and Google Play listings, the Liftoscript doc and the Liftosaur source on GitHub. Prices below are US App Store or vendor prices checked 2026-10-21; they vary by country, so re-check in the app before paying. Anything still marked **(unverified)** is an item the addenda could not settle. The logging rules themselves come from `templates/progression-tracks.md` (section 10) and `guide/04-periodization-and-progression.md` (section 7).

How this changes with available days: it does not. Every week type logs the same fields; only the `session` value changes (L1 ... U3 in split weeks; Full A/B/C, or a cross-block pair such as U1 + L2, in merged weeks). Where an app's free tier caps routines or templates, the day count decides whether you need the paid tier (sections 3.2 and 3.3).

---

## 1. What to log

### 1.1 The record

| Level | Fields | Why |
|---|---|---|
| **Set** | exercise, load (lb, the program's unit), reps, short note (technique, pain, substitute). **RPE: one rating per main lift, on the top set** (7, 8, 9 or 10; Hevy also takes half steps). Ratings on other sets are optional and never change a track | Every metric below is derived from load, reps and the top-set RPE (`templates/progression-tracks.md`, sections 3 and 10) |
| **Session** | date (the lifter's calendar day), session slot (L1, U1, L2, U2, L3, U3, Full A, Full B, Full C, or a cross-block merge U1 + L2, U2 + L3, U3 + L1), bodyweight, sleep hours, readiness 1-5 | The slot places each set in the rotation; readiness drives the reactive deload (`guide/03-flexible-scheduling.md`, section 4.5) |
| **Lift (track state)** | planned top-set load for the next H, rep target, miss counter, date of last exposure (H or V), e1RM history (last 6 H exposures) | The state an agent updates after every H exposure (`templates/progression-tracks.md`, section 10) |
| **Week** | hard sets per muscle group, indirect work at half credit; the pointer after the last session | Checks the week against the template tally; the pointer is the only schedule state |

RPE scale: 10 = 0 reps in reserve, 9 = 1, 8 = 2, 7 = 3 (Zourdos et al. 2016, via `templates/progression-tracks.md`, section 1).

### 1.2 Derived metrics

| Metric | Rule | Where it is defined |
|---|---|---|
| **e1RM** | From the **top set** of the H session. `e1RM = load x (1 + (reps + RIR) / 30)`, RIR = 10 - RPE. Unrated: RIR 2 for a set at the rep target, RIR 1 for a set above it. Example: 125 x 4 @ 8 gives 125 x (1 + 6/30) = **150**. Back-offs and V sets are logged but do not enter the e1RM history; RIR from long sets is less accurate (Russo et al. 2025). | `templates/progression-tracks.md`, section 10 |
| **e1RM trend** | Judge over **3-4 weeks**, never one session. Block test: mean e1RM of the last three H exposures against the first three. The block worked if e1RM rose at matched RPE, or reps rose at the same load, or RPE fell at the same load. | `templates/progression-tracks.md`, section 10; `guide/04-periodization-and-progression.md`, sections 5 and 7 |
| **RPE drift** | RPE at the same load across consecutive exposures. Reps down or RPE up at the same load on two consecutive exposures of a lift = one readiness red flag; two flags for a week = reactive deload. | `guide/03-flexible-scheduling.md`, section 4.5 |
| **Weekly hard sets per muscle** | Direct sets plus 0.5 per indirect set (a press counts 0.5 for triceps; a row 0.5 for biceps and rear delts). Targets: 8-12 per large muscle in a 3-day week, 14-20 in a 5-6-day week. | Tallies at the bottom of each template; `guide/03-flexible-scheduling.md`, section 3 |
| **Gap clock per lift** | Days since the lift's last exposure of either type. 0-7 normal; 8-14 hold the top-set load; 15-21 hold and one fewer back-off; 22-28 reduce 5%; over 28 reduce 10%. Applied at the next H exposure. A regain-phase lift skips the 8-14-day hold; a substitute caps the modifier at a hold. | `templates/progression-tracks.md`, sections 8 and 9 |
| **Miss counter and stall** | Miss = top set at an effective RPE of 9.5-10, or 3 reps or fewer (in a merged session, a later lift's 4 @ 9.5 is a hold, not a miss). Two misses in a row at the same load = stall: flagged, then reset 7.5% after the recovery check. | `templates/progression-tracks.md`, sections 5-6 |
| **Pointer** | Next half-session owed. Split session +1, merged session +2. | `guide/03-flexible-scheduling.md`, section 1.4 |

Which set is the top set when an agent parses a log: in an H session, the heaviest working set of that lift (`tools/README.md`, "How the rules are applied"). It is planned as 4 reps and may run to 6 when rep 4 is clearly easy. The decision reads its effective RPE at rep 4: the logged RPE minus the reps above 4. With no rating, a set above 4 reps is assumed to have ended at RPE 9, and a set of exactly 4 is read as 8 and flagged (`templates/progression-tracks.md`, section 5). If the lifter stopped at 3 reps, use the set with its RPE and count the miss.

---

## 2. The apps compared

Columns follow the research note. "Not stated" means the note found nothing either way; "none found" means the note looked and found nothing, which is not proof of absence. Prices are USD from the US App Store or the vendor's own site, checked 2026-10-21 (research note addendum); FitNotes and the open-source rows were not re-checked.

| App | Platforms | Price (USD, checked 2026-10-21) | Custom-program import path | Export / API | Any-order rotation | RPE / RIR logging | Watch | Verdict for this program |
|---|---|---|---|---|---|---|---|---|
| **Liftosaur** | PWA with thin iOS and Android wrappers; web editor; offline-capable; AGPL-3.0 | Free: programs and the editor, Liftoscript, logging, history, sharing, import and export. Premium **$4.99/mo, $39.99/yr, $99.99 lifetime** (14-day trial on monthly and yearly; bought in the iOS or Android app, unlocks all platforms). Premium gates the Apple Watch app, graphs, plates per side, rest-timer notifications, Week Insights, the API and the MCP server | Paste Liftoscript text in the web editor or the app; share link `liftosaur.com/p/<id>` (a frozen snapshot; Me → Program → Import); Liftosaur CSV, Hevy CSV and JSON imports | Free in-app export: JSON backup, history CSV with one row per set (required and completed reps, weight and RPE), all programs as Liftoscript text. Official REST API (Premium, personal `lftsk_` key): programs and history read and write, a syntax error returns 422 with line numbers, `POST /playground` runs a day and returns the updated program without saving. Official MCP server (Premium). Rate limits undocumented | Sequence-driven: finishing a workout runs the progressions and advances to the next program day whatever the calendar | Native: `@8` targets, `+` logs the actual RPE; can compute load from RPE | Apple Watch app (watchOS 10.6+) **needs Premium**; no Wear OS app; Apple Health and Health Connect sync | **First choice on features.** The only candidate whose scripted progression can run the tracks inside the app. The rendering committed here is unmaintained (section 3.1) |
| **Hevy** | iOS, Android, Apple Watch, Wear OS, web app at hevy.com | Free: unlimited logging, 4 routines, 7 custom exercises, 3 months of graphs. Pro **$2.99/mo, $23.99/yr, $74.99 lifetime** (the App Store also lists a $3.99 monthly SKU) | REST API (Pro) creates and updates routines and routine folders; in-app CSV import is Strong-format **history** only | In-app CSV export (workouts or measurements); API JSON for workouts (per-set RPE confirmed), exercise history, events since a timestamp, body measurements; no webhooks in the published spec | Routines are unscheduled: tap Start Routine in any order; folders group them | Per-set RPE, 6-10 in 0.5 steps (API schema, verified) | Apple Watch (watchOS 9+) and Wear OS; Apple Health, Health Connect, Strava | **Second choice, and the one this repo implements and the lifter runs.** Best API loop; no progression engine, so the repo's tools recompute loads. The 12 rotation routines (plus the dated This Week copies) exceed the free cap |
| **Strong** | iPhone, Apple Watch, Android | Free: unlimited workouts, 3 templates (help article last updated 2021). PRO **$4.99/mo, $29.99/yr, $99.99 one-time** (older SKUs also listed) | None found; manual entry | CSV export of all history (by email); no API found | Templates are schedule-free | RPE supported | Apple Watch (watchOS 10+); no Wear OS app; recurring sync complaints 2024-2026 (aggregator sentiment ~59% positive / 29% negative) | **Third choice (b).** Best CSV-out path; nothing in |
| **Boostcamp** | iOS and Android apps; web program builder | Free: tracker, RPE/RIR, rest timers, custom programs with **no cap**. Pro **$59.99/yr** (7-day trial) or **$14.99/mo** (vendor page, October 2026; other App Store SKUs $11.99, $48.99 offer, $69.99, $79.99) | Web program builder; private share link (human-to-human, not agent-writable) | **No self-serve export** on the official pages; the privacy policy offers a machine-readable copy on request through support. A third-party Chrome extension scrapes the web history (unofficial) | Program days; starting a day out of order **unconfirmed** | RPE and RIR on every set, free | No Apple Watch or Wear OS app; iOS Live Activities | **Third choice (a).** Best free manual option; Pro adds Auto Progression (hit your reps and the load goes up next session; not scriptable, no RPE condition stated); no data path back to the agent |
| **Alpha Progression** | iOS and Android (Android confirmed) | Premium **$12.99/mo or $79.99/yr** (App Store; $14.99/mo is not a listed SKU) | None; its generator asks days per week and periodizes for you; plans can be built from scratch in-app | CSV export on the free tier; whether it includes RPE/RIR **unverified**; no API found | Programs "stable, structured", tied to days per week | RPE/RIR analysis Premium-only | No Apple Watch app | No: its own periodization engine competes with the tracks |
| **JEFIT** | Not stated | Elite **$12.99/mo or $69.99/yr** (App Store; other yearly SKUs $34.99 and $35.99), no lifetime; free tier ad-supported | None found | None found in 2026 sources | Not stated | Not stated | Apple Watch (watchOS 10+) | No |
| **Setgraph** | iOS, Android, Apple Watch | Pro **$4.99/mo, $29.99/yr, $199.99 lifetime** (App Store) | None found | None found | Not stated | Not stated | Apple Watch (watchOS 9.6+) | No |
| **KeyLifts** | iOS only | Pro **$4.99/mo, $29.99/yr, $99.99 lifetime** (App Store) | 5/3/1 templates only | None found | Built around 5/3/1 cycles | Not stated | Apple Watch (watchOS 10+); Apple Health on Pro | No: 5/3/1-specific |
| **Gravitus** | iOS with Apple Watch companion | "Gravitus Pro" SKUs at **$7.99, $9.99, $11.49, $12.99, $59.99 and $79.99** (App Store; durations not labelled) | None found | No CSV export found | Not stated | Not stated | Apple Watch (live heart rate) | No |
| **RepCount** | iOS | Free; Premium in-app purchases **$4.99-$39.99** (seven SKUs) | None found | None found | Not stated | Not stated | None listed on the App Store | No |
| **FitNotes** | Android only | Free | None | CSV export for spreadsheets (not a restorable backup) | Not stated | Not stated | None | Android CSV fallback |
| **Fitbod** | Not stated | **$15.99/mo or $95.99/yr** (App Store; also $12.99/mo and $79.99/yr SKUs) | AI-generated workouts; no import | None found | App-driven | Not stated | Apple Watch (watchOS 10+) | No |
| **RP Hypertrophy** | iOS app and web app | **$299.99/yr or $34.99/mo** (App Store) | In-app meso builder; no import | None found | App-driven mesocycles | Not stated | No Apple Watch app | No: own periodization, 4-15x the cost of a tracker |
| **JuggernautAI** | Not stated | **$34.99/mo** (App Store); $349.99/yr **unverified** (not among the listed purchases); 2-week trial, no free tier | Program generator, not a custom-program runner | None found | App-driven | Not stated | No Apple Watch app | No |
| **Open-source: Liftlog, openGym, GymRoutines** | Liftlog: not stated; openGym: self-hosted PWA (Docker) plus Android APK; GymRoutines: Android (F-Droid), data on device | Free | None documented | GymRoutines: data export and `adb backup`; openGym: your own server | Not stated | Not stated | None | Maximum data ownership, no watch, no import path |

What the table says (the note's inferences, KQ1-KQ3):

- Only **Liftosaur** (text DSL) and **Hevy** (REST API) have a machine-writable input path. Boostcamp's share link is human-to-human.
- **Hevy and Strong** store programs as unscheduled routines, so any order works by construction. **Liftosaur** advances through a defined sequence when a workout is finished, which is exactly what the pointer does. The coach and AI apps (Alpha Progression, RP, JuggernautAI, Fitbod) run their own periodization and are poor fits for an externally maintained program.
- For RPE-driven autoregulation **inside** the app (load computed from RPE), Liftosaur is unique; the others record RPE at best. The only other in-app progression engine found is Boostcamp Pro's Auto Progression, which is reps-based and not scriptable.
- Watch and Health sync is the dominant reliability complaint for Strong and Hevy (KQ4). A lifter who logs on the phone avoids most reported issues. Of the three recommended apps, only Hevy has a Wear OS app, and Liftosaur's Apple Watch app needs Premium.

---

## 3. The recommended three

### 3.1 Liftosaur: the app runs the tracks

**Status, 2026-11-13: the committed rendering is an unmaintained alternative.** The lifter runs the program in Hevy (section 3.2). `templates/liftosaur/rotation.liftoscript` was rendered on 2026-10-21, last touched on 2026-10-26, and no longer matches the program. Nothing re-renders it.

| What | The committed file | The program today |
|---|---|---|
| Units and loads | Kilograms, worked-example loads | Pounds, the lifter's loads in `data/tracks.json` |
| Steps | 2.5 kg and 1 kg on every success | +5 lb; bench and press on every second success |
| November rules | None | Effective RPE, big step, re-anchor, regain phase, deadlift caution, rep-out, busy-gym substitutes (`templates/progression-tracks.md`, sections 5, 5.1-5.3, 9) |
| Sessions | Six split sessions | 12 in `templates/rotation.json`, with the merged forms |
| Exercises | Plain lunge; pull-up with added load | Reverse lunge; lat pulldown |

The workflow below describes how the Liftosaur path works. Before using it, re-render the file from `templates/rotation.json` and `templates/progression-tracks.md`. The full list of differences is at the top of `templates/liftosaur/README.md`.

**Why.** Liftoscript expresses what the program needs: per-set RPE targets (`@8`), `+` to log the actual RPE, percentages, `kg`/`lb` number types, and `progress:` rules (`lp()` linear, `dp()` double progression, `custom()` for anything else). Programs are plain text, so an agent can render them from the markdown templates and commit them. The app advances to the next program day when a workout is finished, not by weekday, so a 3-day week and a 6-day week both work. Offline and open source. Programs, the editor, import and export are free; the Apple Watch app (since February 2026), graphs, plates per side and rest-timer notifications need Premium ($4.99/mo, $39.99/yr or $99.99 lifetime).

**Workflow.**

1. An agent renders `templates/liftosaur/rotation.liftoscript` from `templates/rotation.json` and `templates/progression-tracks.md`, with your starting loads (section 2 of the tracks file). The rendering in that folder dates from October 2026 (status above); its README records the syntax checks.
2. You open the Liftosaur web editor or the app and paste the text, or import a share link (Me → Program → Import; a public link `https://www.liftosaur.com/p/<id>` is a frozen snapshot, so a re-render needs a new link). The file uses names from Liftosaur's built-in exercise list, with the equipment after a comma where the default differs (`Romanian Deadlift, Barbell`).
3. Train. Finishing L1 advances the program to U1, and so on. In a merged week, do two consecutive program days in one visit and skip the sets the merged template drops (section 3.4 below and the README).
4. Each block (4-6 passes plus deload), or after any stall, reset or gap event, the agent re-renders the file from your logged data and you re-import it. Between renders the app's `lp()` steps do the weekly increments. No scheduled run does this today; ask for a re-render.

**Caveats.** The Liftoscript grammar is now confirmed from the official doc and the grammar file (research note addendum): `# Week` / `## Day` headers, `lp()`, `dp()`, `sum()`, `custom()`, `progress: none`, exercise labels, warm-up and rest syntax. Two traps it settled: `//` is a description **shown to the lifter**, not a code comment (`///` is the hidden note, and nothing may follow an exercise on its line); and a progression belongs to the exercise across the whole program, so a second day with a different rule is an error and the V copies need a label to stay off the H track. `lp()` advances on completed reps and has no RPE argument, so the program's "hold at RPE 8.5-9" rule, and every rule that reads the effective RPE (big step, re-anchor, miss), needs either a `custom()` block (documented, with `completedRPE`; not yet written or tested in this repo) or a manual override. Getting data **out** without Premium means the free in-app export by hand (history CSV, JSON backup); the API needs Premium. No Wear OS app. Still **(unverified)** in official text: whether an `lp()` step rewrites the weight on every day the exercise appears, how `dp()` treats sets written as a rep range, and API rate limits. A local run of Liftosaur's own open-source evaluator answered the first two (yes; and a range collapses), so the rendered file labels its V lines and writes double progression at the bottom of the range; details in `templates/liftosaur/README.md`. Self-hosting the backend is impractical.

**A Liftosaur API loop is possible, not built.** The official REST API (`https://www.liftosaur.com/api/v1`, Premium, a personal key starting `lftsk_` sent as `Authorization: Bearer`) could run the same loop as the Hevy tools: `PUT /programs/:id` to push the re-rendered Liftoscript (a syntax error comes back as 422 with line numbers), `GET /history` to pull logged sets, and `POST /playground` to validate a program and simulate a day's progressions without saving. It would need Premium and a separate key, handled under the same secret rules as the Hevy key (a network secret or an environment variable, never in chat or a file). Nothing in `tools/` implements it yet.

### 3.2 Hevy Pro: the agent runs the tracks

**Why.** Hevy has a documented REST API (`api.hevyapp.com`, `api-key` header with a per-account key issued to Pro subscribers at `https://hevy.com/settings?developer`, docs at `https://api.hevyapp.com/docs/`). The official OpenAPI document (read 2026-10-21, note addendum) lists: list, create and update routines and routine folders; list and create exercise templates; list, create and update workouts; workout events since a timestamp; exercise history per template; body measurements. Workout sets carry RPE; routine sets carry load, reps or a rep range, set type and rest, but no RPE. There is no webhook and no delete endpoint. Routines are unscheduled, so the lifter starts whichever one the pointer names. Hevy's pricing is the lowest of the mainstream trackers in the note (KQ4).

**Workflow (implemented in `tools/`, details in `tools/README.md`).**

1. Buy Pro ($2.99/mo, $23.99/yr or $74.99 lifetime on the US App Store, 2026-10-21). Generate an API key at hevy.com/settings?developer. Give it to sessions as a **network secret** for `api.hevyapp.com` (header `api-key`; the proxy adds it and the key never enters the session). The alternative is the `HEVY_API_KEY` environment variable. Never commit the key or paste it into a chat (`tools/README.md`, Setup step 2).
2. The first `python3 tools/hevy_sync.py` creates a routine folder named for the program version (`Rotation 2026-10`, from `templates/rotation.json`) and the **12 rotation routines** in it:

   | Kind | Routines |
   |---|---|
   | Six half-sessions | L1 Lower A, U1 Upper A, L2 Lower B, U2 Upper B, L3 Lower C, U3 Upper C |
   | Three merged blocks | Full A, Full B, Full C |
   | Three cross-block merges (weeks that start mid-block) | U1 + L2, U2 + L3, U3 + L1 |

   It also keeps **dated copies of the current week's sessions** in a second Hevy folder, "This Week". The week's schedule lives in `data/week.json` and is changed only with `python3 tools/week.py` (`plan`, `set`, `add`, `drop`, `deload`); the dated routines take their titles, loads and notes from it. Each exercise carries its sets with the planned load in pounds from `data/tracks.json` (warm-up ramp, top set, back-offs at 93%, V sets at 90%, rep ranges for row, pull-up and accessories), the rest timer, and a note with the RPE target and the rule. The free tier's 4-routine cap blocks this, which is why Pro is required.
3. You open the Workout tab, start the day's dated routine in the "This Week" folder (or the rotation routine the pointer names; `python3 tools/week.py show` prints the week and the pointer), and log load and reps per set and the RPE of each main lift's top set. Hevy's set RPE field is what the API returns. It is off by default: Profile tab → gear icon → Workouts → **RPE Tracking** on; an RPE column (6-10) then appears next to Reps in a live workout, and can be left blank ([Hevy, workout settings](https://www.hevyapp.com/features/workout-settings/)). The lifter turned it on 2026-11-10.
4. After training is logged, and after any change to the week or the tracks, run **one command**: `python3 tools/hevy_sync.py`. `main` on GitHub is the source of truth; Hevy and the dashboard are projections of it. The command runs these steps in order (`tools/README.md`):

   | Step | What it does | If it fails |
   |---|---|---|
   | 1. Check | The checkout is current with `origin/main` and may write to it (`gitguard.py`) | `Sync not started`; nothing changes anywhere |
   | 2. Pull | New workouts (`GET /workouts/events?since=`) into `data/history.csv` | Stops |
   | 3. Apply | `templates/progression-tracks.md` to the tracks (section 4 below); `data/tracks.json`, the table in `data/track-state.md`, `data/track-log.md` | Stops |
   | 4. Week | Marks logged sessions done in `data/week.json`; regenerates the tables in `data/weekly-plan.md` | Stops |
   | 5. Build | The dashboard, only when data changed | Reported at the end |
   | 6. Commit, publish | The changed data files, to `origin/main` | Stops; Hevy is not touched |
   | 7. Push | Compares every routine with what Hevy holds, updates only the ones that differ, and reads each back | Exit code 1; the repo is right, Hevy is stale; run it again |

   The repo is published **before** Hevy is touched, so Hevy never holds something the repo does not. The push prints each skipped session with its reason and carries on past a failed routine. With no news the command changes nothing and commits nothing. `--dry-run` writes nothing in the repo, on GitHub or in Hevy. `--check` only compares Hevy with the repo. Do not commit the data files or push to Hevy any other way. There is no webhook, so the sync is run by hand or on a schedule.

   | To change | Use | Then |
   |---|---|---|
   | This week's sessions, or the deload flag | `python3 tools/week.py plan`, `set`, `add`, `drop`, `deload on` | `python3 tools/hevy_sync.py --no-pull` |
   | A load, a counter or the pointer, by hand | `python3 tools/update_tracks.py --set PATH=VALUE --reason "..."` (logged in `data/track-log.md`) | `python3 tools/hevy_sync.py --no-pull` |

   Never edit `data/tracks.json` or `data/week.json` in an editor.
5. **Dates are the lifter's, not the server's.** A workout's date, and "today" for the push, the gap clock and the dashboard, is the calendar day in the lifter's time zone (`TRAINING_TZ`, default America/New_York; `tools/localtime.py`), never the UTC date. In winter a session started after 7 pm Eastern is already on the next UTC date; it is still dated that evening.

**Caveats.** Hevy has **no progression engine**; every increment, hold and reset is computed by `tools/update_tracks.py`, the gap modifier by `tools/hevy_push_routines.py` at push time, and both are written back as routine loads. Routine sets have no RPE field, so targets live in the exercise notes. Rate limits are not documented; Hevy asks that scheduled pulls avoid the top of the hour. Hevy says the API may change or be withdrawn. Data lives on Hevy's servers; an unsaved active workout is lost if the app is uninstalled. Apple Health and Watch sync failures are documented in Hevy's own help centre and do not backfill.

### 3.3 Boostcamp (free, manual in, nothing out) or Strong (manual in, CSV out)

**Boostcamp.** Free tier includes the tracker, RPE and RIR on every set, auto-start rest timers per exercise and custom programs with no cap on how many you build or run. Pro ($59.99/yr or $14.99/mo) adds Auto Progression: hit your reps and the load goes up next session. That is a reps-only rule, so it cannot express the hold and miss rules; leave it off for the main lifts. The web program builder saves straight to the app, and a program can be shared by private link. Workflow: use `templates/6-day-week.md` (or the 3-day file) as the entry checklist, build the six half-sessions once in the web builder, train from the app, and keep the private link somewhere private (not in a public repo). Limitation: **no self-serve export** on Boostcamp's official pages (the privacy policy offers a machine-readable copy on request through support; a third-party browser extension that scrapes the web history is unofficial), so the agent cannot read anything back routinely; you keep the CSV log in section 5 for the main lifts, or send screenshots. No Apple Watch or Wear OS app. Out-of-order starting of program days is unconfirmed; Fortune 2026 named it the best free option.

**Strong.** Templates are schedule-free, RPE is supported and the full history exports as CSV (sent by email), which is the input an agent parses. The free version has 3 templates (Strong's help article, last updated 2021), which covers exactly Full A, Full B and Full C (a 3-day-only setup; inference from the cap); the six split sessions plus the three merged forms need PRO ($4.99/mo, $29.99/yr or $99.99 one-time). Workflow: enter the templates from the markdown, train, export CSV after each pass or block, drop the file in the repo, and the agent analyses it. Hevy imports Strong-format CSV, so a later move to Hevy keeps the history. Downsides: no program import, no Wear OS app, and the most-reported Watch-sync instability of the group.

### 3.4 Decision guide

| If you... | Use | Because |
|---|---|---|
| Want the app to apply the progression itself and are willing to check a few lines against the docs | **Liftosaur** | Only app with a scriptable progression engine; import by pasting text; works offline |
| Want an agent to do everything over an API and do not mind $24/yr | **Hevy Pro** | Routines and folders writable; workouts (with RPE) and exercise history readable as JSON; the loop is already built in `tools/` |
| Want zero subscription and do not need data back in the repo | **Boostcamp** free, or **Liftosaur** free | Boostcamp: RPE/RIR, timers and unlimited custom programs free. Liftosaur: programs, Liftoscript, import and export are free; no graphs, watch app, plates per side or API without Premium |
| Already use Strong and want to keep it | **Strong** + CSV export | Agent parses the CSV; Hevy accepts the same CSV if you move later |
| Train on Android with no watch and want to own the data | **Liftosaur**, **FitNotes** (CSV) or **GymRoutines** (export) | Open or exportable; no sync layer to break |
| Need Apple Watch logging | **Hevy**, **Strong**, or **Liftosaur** with Premium | Liftosaur's watch app shows "Premium Required" on the free tier. Expect the sync complaints the note records for Hevy and Strong |
| Need Wear OS logging | **Hevy** | Liftosaur, Strong and Boostcamp have no Wear OS app |
| Only train 3 days a week, always | **Strong** free (3 templates = Full A/B/C) or **Liftosaur** | The 3-template cap stops mattering |

Not recommended for this program: Alpha Progression, RP Hypertrophy, JuggernautAI, Fitbod (their own periodization), KeyLifts (5/3/1 only), JEFIT, Setgraph, Gravitus, RepCount (no import or export found).

---

## 4. How agents use the logged data

The loop is the same whichever app you choose; only the first and last steps change.

| Step | What happens | Liftosaur | Hevy Pro | Strong / Boostcamp / manual |
|---|---|---|---|---|
| **1. Export** | Get the sets since the last run into the repo | Free in-app export (Me → Import / Export): history CSV, one row per set with required and completed reps, weight and RPE; or the API (`GET /history`, Premium); else the CSV log | `tools/hevy_pull.py` (`GET /workouts/events?since=` after the first full pull); or the in-app CSV export through `tools/hevy_csv_import.py` | Strong CSV export; Boostcamp: the CSV log (no self-serve export); manual: the CSV or sheet in section 5 |
| **2. Normalise** | Map to the eight columns in section 5; tag each main-lift set as H top set, H back-off, V or substitute from the session slot and the template | Exercise names from the Liftoscript file; the CSV's Day Name column gives the slot | Routine title gives the slot (`tools/update_tracks.py`) | `session` column gives the slot |
| **3. Analyse** | Per lift: e1RM from the best heavy set of each H session; e1RM trend (last 3 vs first 3 H exposures, 3-4 weeks); RPE at matched load across exposures (drift); miss counter; days since last exposure (gap clock); weekly hard sets per muscle vs the template tally; readiness flags from the session fields | same | same | same |
| **4. Apply the rules** | From `templates/progression-tracks.md`, which is the only place the rules are written in full: effective RPE, increment, big step, re-anchor, hold, miss (section 5); regain phase, deadlift caution, rep-out (sections 5.1-5.3); stall after two misses: check sleep, calories, bodyweight first, then reset 7.5% (section 6); second stall: reset and switch to 6s for a block; deload every 4-6 passes or on two readiness flags: top sets x 0.90-0.92, one back-off, V and accessories cut (section 7); gap modifiers (section 8); busy-gym substitutes and the moved top set (section 9); stale-track rule when the last V set is RPE 6 or lower twice running (section 4); accessories: double progression, drop one load step after two exposures without a rep gained (section 11) | same | same | same |
| **5. Update the program** | Write the new planned loads into the track-state table and the program artefact | Re-render `templates/liftosaur/rotation.liftoscript` with the new starting loads (and the deload or 6-rep variant when one applies). Not done since October 2026 (section 3.1) | `tools/update_tracks.py` rewrites `data/tracks.json`; the sync commits it and publishes it to `main` | Update the markdown track table; user edits the app templates by hand |
| **6. Re-import** | Get the update into the app | User pastes the file or opens the share link | Automatic: the last step of `tools/hevy_sync.py` updates the routines that differ (`PUT /routines/{id}`) and reads each back | Manual |

Cadence: step 4 runs after every pass (the Sunday check-in and the nightly brief in `guide/08-weekly-coaching-cadence.md` run it on a schedule) (one calendar week for any 3- to 6-day week); the Liftosaur re-render is needed only when the in-app `lp()` steps diverge from the rules (a hold, a miss, a gap, a reset, a deload) or at a block boundary. The agent must never advance a load on a miss or during a deload, must not let a V exposure or a squat, bench, deadlift or press substitute change a track (row and pulldown variants update their own load and count as the exposure; a missed top set moves to the lift's next V exposure: `templates/progression-tracks.md` §9), and must log what it changed: `data/track-log.md` in the Hevy loop, the CSV `notes` or a dated line at the top of the log otherwise.

What this loop does **not** promise: automatic export from Liftosaur without Premium (the free export is a manual step in the app; the API that would automate it needs Premium and is not built here), and any self-serve export from Boostcamp. Hevy's per-set RPE is confirmed; Hevy webhooks do not exist in the published API, so the pull is polled. Where something is missing, the CSV log in section 5 is the bridge.

---

## 5. Manual fallback: Google Sheets or a CSV in this repo

A spreadsheet or a committed CSV is enough to run the program and is the common format every path above normalises to. The note found no lifting-specific Sheets template with progression logic, so the layout here is this repo's own. A blank copy with example rows is `templates/log-template.csv`.

### 5.1 Set log (one row per set)

| Column | Type | Values | Notes |
|---|---|---|---|
| `date` | ISO date | `2026-11-03` | Session date |
| `session` | text | `L1`, `U1`, `L2`, `U2`, `L3`, `U3`, `Full A`, `Full B`, `Full C` | The rotation slot. This is what tells an agent whether a squat set is an H or a V exposure and whether the merged back-off count applies |
| `exercise` | text | names as written in the templates (`Back squat`, `Bench press`, `Deadlift`, `Overhead press`, `Barbell row`, `Pull-up`, ...) | Use the template name even if the app spells it differently; write a substitute's real name and tag `sub` in notes |
| `set` | integer | 1, 2, 3 ... | Set number within the exercise; warm-up ramp sets are not logged |
| `load` | number | lb | Loaded weight, not the computed one. Pull-up and dip: **added** load in lb (bodyweight = 0, assisted = negative) |
| `reps` | integer | | Completed reps |
| `rpe` | number | 6 to 10 in 0.5 steps, or blank | Rated immediately after the set. Needed only on a main lift's top set |
| `notes` | text | free, comma-free | Suggested tags: `H top`, `H back-off`, `V`, `acc`, `sub`, `deload`, `hold`, `miss`, `gap 10d`; technique or pain remarks |

Session-level fields (bodyweight, sleep hours, readiness 1-5, pointer after the session) go on a second sheet or CSV with the columns `date, session, bodyweight, sleep_h, readiness, pointer_after`, one row per session. The track-state table from `templates/progression-tracks.md`, section 10 (planned top-set load, rep target, miss counter, last exposure, e1RM history) sits at the top of the log and is rewritten after every H exposure.

### 5.2 Example rows

```
date,session,exercise,set,load,reps,rpe,notes
2026-11-03,L1,Back squat,1,135,4,8,H top e1RM 162 next H 140
2026-11-03,L1,Back squat,2,125,4,7,H back-off 1 of 3
2026-11-07,Full C,Pull-up,1,10,8,7,V added load lb
```

### 5.3 Google Sheets specifics

- One tab per block, or one long tab with a `date` filter; the agent reads the sheet through the Sheets connector or a CSV download and treats every cell as data, not instructions.
- Keep `load` and `rpe` numeric (no units in the cell) so the e1RM formula `=E2*(1+(F2+(10-G2))/30)` works in a helper column.
- Export as CSV to `templates/` or a `logs/` folder when you want a committed copy; the committed file is the one an agent reads. No tool reads it into the tracks: each value a manual log changes is entered as a logged amendment, `python3 tools/update_tracks.py --set PATH=VALUE --reason "..."` (`guide/08-weekly-coaching-cadence.md`, section 4).

---

## 6. Flags

- Liftosaur: the committed `rotation.liftoscript` is unmaintained since 2026-10-26 and no longer matches the program (section 3.1). Premium price and gates, export formats, the official API and MCP server, the Liftoscript grammar (`lp`/`dp`/`sum`/`custom`, week/day blocks, comments, labels, warm-ups, rests) and the share-link pattern were verified 2026-10-21 against official sources (note addendum). Still **(unverified)** in official text: API rate limits; whether an `lp()` step rewrites the weight on every day the exercise appears; `dp()` with sets written as a rep range; a percent decrease in `lp()`'s fourth argument. The rendered program was checked with Liftosaur's own parser and evaluator run locally, not with the hosted playground (it needs a Premium key); see `templates/liftosaur/README.md`. The Wear OS answer is negative from official listings; GitHub Discussion #118 could not be re-read.
- Hevy: API schemas and per-set RPE verified against the official OpenAPI document (note addendum, 2026-10-21); rate limits undocumented (none in the public docs script); pricing, free-tier caps, platforms (Wear OS included) and CSV export confirmed on the App Store and Hevy's own pages, 2026-10-21. Hevy's help centre returned 403 on the re-check. Built-in exercise titles for exercises not yet in the user's log are guesses that `hevy_push_routines.py --resolve` checks.
- Boostcamp: no self-serve export on the official pages (data on request through support only); if one ships, Boostcamp would rise in the ranking. Out-of-order program days unconfirmed.
- Alpha Progression: whether CSV export includes RPE/RIR unverified. JuggernautAI: the $349.99/yr price unverified.
- No Reddit or Garage Gym Reviews sentiment could be sampled; sentiment figures are from review aggregators and competitor blogs.
- App Store privacy labels were not checked. FitNotes, GymRoutines, openGym and Liftlog were not re-checked in the official-source pass.
- No peer-reviewed validation of e1RM-trend tracking as a predictor of long-term progress exists (`guide/04-periodization-and-progression.md`, section 7 gaps); the metric is a convention.

---

## Repository tooling

The scripts in `tools/` implement the whole Hevy loop above.

| Script | Role |
|---|---|
| `hevy_sync.py` | The one command: check, pull, apply, week, build, commit and publish, push |
| `hevy_api.py` | Client and read-only inspector |
| `hevy_pull.py` | API to `data/history.csv` |
| `update_tracks.py` | The rules of `templates/progression-tracks.md` applied to the log; writes `data/tracks.json`. `--set PATH=VALUE --reason "..."` is the only hand amendment |
| `week.py` | The week's schedule, `data/week.json`: plan, change, check order and spacing, print the brief's numbers |
| `build_dashboard.py` | The progress dashboard |
| `hevy_push_routines.py` | `templates/rotation.json` and the week rendered with the tracks into the 12 rotation routines and the dated This Week copies; updates the ones that differ and reads each back |
| `gitguard.py` | A sync starts only from a checkout that is current with `main` and can write to it |
| `localtime.py` | The lifter's time zone (America/New_York by default); every date comes from it, not from UTC |

`hevy_csv_import.py` and `analyze_history.py` remain for the no-API path and for seeding starting loads. `build_dashboard.py` turns the log and the tracks into a progress dashboard (`dashboard/index.html`) that applies the derived metrics in section 1.2 week by week: tonnage, weekly sets per muscle against the targets, week-over-week e1RM per main lift, the gap clock and the track state. See `tools/README.md`.

## Sources

- `research/mobile-workout-trackers.md` (2026-10-21): KQ1 (per-app profiles, prices, export), KQ2 (Liftoscript syntax; Hevy API operations), KQ3 (any-order rotation; RPE/RIR logging), KQ4 (sentiment, sync complaints), KQ5 (top-3 recommendation and integration paths).
- `templates/progression-tracks.md`, sections 4-8 and 10-11 (what to log, e1RM, increment/hold/miss, stall, deload, gap clock, accessory progression); `guide/04-periodization-and-progression.md`, sections 5 and 7 (e1RM trend over 3-4 weeks, block criteria, Russo et al. 2025); `guide/03-flexible-scheduling.md`, sections 1.4, 4.4 and 4.5 (pointer, gap modifiers, readiness flags).
- Official sources from the 2026-10-21 addendum: Liftosaur [Premium](https://www.liftosaur.com/features/premium), [REST API doc](https://www.liftosaur.com/doc/api), [API feature page](https://www.liftosaur.com/features/api), [MCP doc](https://www.liftosaur.com/doc/mcp), [Import and Export](https://www.liftosaur.com/features/import-export), [Sharing Programs](https://www.liftosaur.com/features/sharing-programs), [Apple Watch](https://www.liftosaur.com/features/apple-watch), [Health sync](https://www.liftosaur.com/features/health-sync), [grammar file](https://github.com/astashov/liftosaur/blob/master/src/pages/planner/plannerExercise.grammar), [exercise list](https://github.com/astashov/liftosaur/blob/master/src/models/exercise.ts), [App Store](https://apps.apple.com/us/app/id1661880849), [Google Play](https://play.google.com/store/apps/details?id=com.liftosaur.www.twa); Hevy [vs Strong](https://www.hevyapp.com/compare/strong/), [tutorial](https://www.hevyapp.com/hevy-tutorial/), [App Store](https://apps.apple.com/us/app/id1458862350); Strong [strong.app](https://www.strong.app/), [help: templates](https://help.strongapp.io/article/105-about-templates), [App Store](https://apps.apple.com/us/app/id464254577); Boostcamp [Pro](https://www.boostcamp.app/pro), [pricing](https://www.boostcamp.app/pricing), [privacy policy](https://www.boostcamp.app/privacy-policy); App Store listings for JEFIT, Alpha Progression, Setgraph, KeyLifts, Gravitus, RepCount, Fitbod, RP Hypertrophy and JuggernautAI (URLs in the note's verification table).
- Key URLs from the research note: Liftosaur [GitHub README](https://github.com/astashov/liftosaur), [docs](https://www.liftosaur.com/docs), [Liftoscript doc](https://www.liftosaur.com/doc/liftoscript), [new program editor blog](https://www.liftosaur.com/blog/posts/new-experimental-program-editor), [Apple Watch discussion #118](https://github.com/astashov/liftosaur/discussions/118), [App Store listing mirror](https://apps.appfollow.io/ios/liftosaur-scriptable-workouts/1661880849?country=td), [Wellness Project integration page](https://wellnessproject.ai/fr/integrations/liftosaur) (third-party; superseded by the official API doc); Hevy [API docs](https://api.hevyapp.com/docs/), [developer settings](https://hevy.com/settings?developer), [hevy-py README](https://github.com/ewright3/hevy-py), [apis.io auth profile](https://apis.io/security/hevy/hevy-authentication/), [help: export and Strong CSV import](https://help.hevyapp.com/hc/en-us/articles/38001424401943-How-to-Import-Strong-App-CSV-Files-and-Export-Your-Data-in-Hevy), [help: build a program](https://help.hevyapp.com/hc/en-us/articles/34953606698903-Build-a-Workout-Program-Create-Organize-Routines), [help: data on uninstall](https://help.hevyapp.com/hc/en-us/articles/38223672272791-What-will-happen-to-my-information-if-I-uninstall-and-reinstall-the-Hevy-app), [SensAI Hevy review 2026](https://www.sensai.fit/blog/hevy-review-2026) (competitor); Strong [SensAI review](https://www.sensai.fit/es/blog/strong-app-review-2026) (competitor), [App Pricing Lab](https://apppricinglab.com/iap/apple/464254577), [justuseapp reviews](https://justuseapp.com/en/app/464254577/strong-workout-tracker-gym-log/reviews); Boostcamp [custom program builder](https://boostcamp.app/custom-program), [is it free](https://www.boostcamp.app/is-boostcamp-free), [Pro](https://www.boostcamp.app/pro), [RPE/RIR](https://www.boostcamp.app/best/rpe-rir); Alpha Progression [guide](https://alphaprogression.com/en/blog/alpha-progression-guide); FitNotes [Play listing mirror](https://www.bluestacks.com/campaign/com.github.jamesgay.fitnotes/en); GymRoutines [F-Droid](https://f-droid.org/es/packages/com.noahjutz.gymroutines/); openGym [mirror](https://gitea.com/estebanfak/openGym); Fortune [best weightlifting apps](https://www.fortune.com/article/best-weightlifting-apps/).
