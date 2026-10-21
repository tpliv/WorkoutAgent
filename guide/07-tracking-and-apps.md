# 07. Tracking and apps

Last updated: 2026-10-21 (Hevy section revised the same day after the API schema was verified)

**The question this chapter answers:** "Which mobile tracker can run this rotation, and how do the agents in this repo read my training data back?"

**The short answer:** log load, reps and RPE for every set. Use **Liftosaur** if you want the app itself to run the progression tracks (an agent writes a Liftoscript file in this repo, you paste it in). Use **Hevy Pro** if you want an agent to push routines and pull your history over an API (the agent then does the progression arithmetic, because Hevy has none); this repo ships that loop in `tools/`. Use **Boostcamp** (free, manual entry) or **Strong** (manual entry, CSV out) if you want a conventional tracker. Whatever you use, the eight-column CSV in section 5 is the interchange format this repo reads.

Evidence base: `research/mobile-workout-trackers.md` (2026-10-21). That note could not open liftosaur.com, api.hevyapp.com or apps.apple.com (DNS failures), so most app facts come from search summaries, help-centre pages and competitor blogs. Anything the note marks **(unverified)** is marked the same way here. The Hevy API items were verified later the same day against the official OpenAPI document (note addendum of 2026-10-21) and are no longer flagged. Re-check prices in the app before paying. The logging rules themselves come from `templates/progression-tracks.md` (section 10) and `guide/04-periodization-and-progression.md` (section 7).

How this changes with available days: it does not. Every week type logs the same fields; only the `session` value changes (L1 ... U3 in split weeks, Full A/B/C in merged weeks). Where an app's free tier caps routines or templates, the day count decides whether you need the paid tier (sections 3.2 and 3.3).

---

## 1. What to log

### 1.1 The record

| Level | Fields | Why |
|---|---|---|
| **Set** | exercise, load (kg), reps, RPE in 0.5 steps, short note (technique, pain, substitute) | Every metric below is derived from load, reps and RPE |
| **Session** | date, session slot (L1, U1, L2, U2, L3, U3, Full A, Full B, Full C), bodyweight, sleep hours, readiness 1-5 | The slot places each set in the rotation; readiness drives the reactive deload (`guide/03-flexible-scheduling.md`, section 4.5) |
| **Lift (track state)** | planned top-set load for the next H, rep target, miss counter, date of last exposure (H or V), e1RM history (last 6 H exposures) | The state an agent updates after every H exposure (`templates/progression-tracks.md`, section 10) |
| **Week** | hard sets per muscle group, indirect work at half credit; the pointer after the last session | Checks the week against the template tally; the pointer is the only schedule state |

RPE scale: 10 = 0 reps in reserve, 9 = 1, 8 = 2, 7 = 3 (Zourdos et al. 2016, via `templates/progression-tracks.md`, section 1).

### 1.2 Derived metrics

| Metric | Rule | Where it is defined |
|---|---|---|
| **e1RM** | From the **best heavy set** of the session: the top set, 4 reps at RPE 8 or higher. `e1RM = load x (1 + (reps + RIR) / 30)`, RIR = 10 - RPE. Example: 125 x 4 @ 8 gives 125 x (1 + 6/30) = **150**. Back-offs and V sets are logged but do not enter the e1RM history; RIR from long sets is less accurate (Russo et al. 2025). | `templates/progression-tracks.md`, section 10 |
| **e1RM trend** | Judge over **3-4 weeks**, never one session. Block test: mean e1RM of the last three H exposures against the first three. The block worked if e1RM rose at matched RPE, or reps rose at the same load, or RPE fell at the same load. | `templates/progression-tracks.md`, section 10; `guide/04-periodization-and-progression.md`, sections 5 and 7 |
| **RPE drift** | RPE at the same load across consecutive exposures. Reps down or RPE up at the same load on two consecutive exposures of a lift = one readiness red flag; two flags for a week = reactive deload. | `guide/03-flexible-scheduling.md`, section 4.5 |
| **Weekly hard sets per muscle** | Direct sets plus 0.5 per indirect set (a press counts 0.5 for triceps; a row 0.5 for biceps and rear delts). Targets: 8-12 per large muscle in a 3-day week, 14-20 in a 5-6-day week. | Tallies at the bottom of each template; `guide/03-flexible-scheduling.md`, section 3 |
| **Gap clock per lift** | Days since the lift's last exposure of either type. 0-7 normal; 8-14 hold the top-set load; 15-21 hold and one fewer back-off; 22-28 reduce 5%; over 28 reduce 10%. Applied at the next H exposure. | `templates/progression-tracks.md`, section 8 |
| **Miss counter and stall** | Miss = top set at RPE 9.5-10 or fewer than 4 reps (in a merged session, a later lift's 4 @ 9.5 is a hold, not a miss). Two misses in a row at the same load = stall: reset 7.5%. | `templates/progression-tracks.md`, sections 5-6 |
| **Pointer** | Next half-session owed. Split session +1, merged session +2. | `guide/03-flexible-scheduling.md`, section 1.4 |

Which set is the "best heavy set" when an agent parses a log: in an H session, the heaviest set of that lift with 4 or fewer reps and RPE 8 or higher. If the top set came in at RPE 7.5 or lower, it still counts (the e1RM is just lower); if the lifter stopped at 3 reps, use it with its RPE and count the miss.

---

## 2. The apps compared

Columns follow the research note. "Not stated" means the note found nothing either way; "none found" means the note looked and found nothing, which is not proof of absence. Prices are USD as reported in 2026 sources, several of them competitor blogs.

| App | Platforms | Price (as reported) | Custom-program import path | Export / API | Any-order rotation | RPE / RIR logging | Watch | Verdict for this program |
|---|---|---|---|---|---|---|---|---|
| **Liftosaur** | PWA with thin iOS and Android wrappers; web editor; offline-capable; AGPL-3.0 | Free download; Premium exists, **price not retrieved** (unverified) | Paste a Liftoscript text snippet or open a share link; web editor for desktop | API behind Premium with a personal key (third-party claim, **unverified**); history export format **unverified** | Sequence-driven: finishing a workout advances to the next program day whatever the calendar | Native: `@8` targets, `+` logs the actual RPE; can compute load from RPE | Apple Watch shipped 2026-02-05; Health Connect sync; Wear OS asked 2026-07-24, no reply | **First choice.** The only candidate whose scripted progression can run the tracks inside the app |
| **Hevy** | iOS and Android (inferred from Apple Health and Health Connect support) plus a web app at hevy.com | Free: unlimited logging, 4 routines, 7 custom exercises, ~3 months of graphs. Pro **$2.99/mo, $23.99/yr, $74.99 lifetime** (some sources $3.99/mo; regional pricing varies) | REST API (Pro) creates and updates routines and routine folders; in-app CSV import is Strong-format **history** only | In-app CSV export; API JSON for workouts (per-set RPE confirmed), exercise history, events since a timestamp, body measurements; no webhooks in the published spec | Routines are unscheduled: tap Start Routine in any order; folders group them | Per-set RPE, 6-10 in 0.5 steps (API schema, verified) | Apple Watch (help pages document sync fixes); Apple Health, Health Connect, Strava | **Second choice, and the one this repo implements.** Best API loop; no progression engine, so the repo's tools recompute loads. A 9-routine rotation exceeds the free cap |
| **Strong** | iPhone, Apple Watch, Android | Free: unlimited workouts, 3 templates. PRO **$4.99/mo, $29.99/yr, $99.99 one-time** | None found; manual entry | CSV export of all history; no API found | Templates are schedule-free | RPE supported | Apple Watch; recurring sync complaints 2024-2026 (aggregator sentiment ~59% positive / 29% negative) | **Third choice (b).** Best CSV-out path; nothing in |
| **Boostcamp** | iOS and Android apps (Android confirmed); web program builder | Free: tracker, RPE/RIR, rest timers, limited custom programs. Pro **$59.99/yr** (7-day trial) or **$14.99/mo** (one page says $11.99/mo; conflicting) | Web program builder; private share link (human-to-human, not agent-writable) | **None found** (absence of evidence; unverified) | Program days; starting a day out of order **unconfirmed** | RPE and RIR on every set, free | Not stated | **Third choice (a).** Best free manual option; no data path back to the agent |
| **Alpha Progression** | iOS and Android (Android confirmed) | Premium **$12.99/mo or $79.99/yr** (one page lists $14.99/mo; conflicting) | None; its generator asks days per week and periodizes for you; plans can be built from scratch in-app | CSV export on the free tier; whether it includes RPE/RIR **unverified**; no API found | Programs "stable, structured", tied to days per week | RPE/RIR analysis Premium-only | Not stated | No: its own periodization engine competes with the tracks |
| **JEFIT** | Not stated | Elite **~$12.99/mo or $69.99/yr**, no lifetime; free tier ad-supported | None found | None found in 2026 sources | Not stated | Not stated | Not stated | No |
| **Setgraph** | iOS, Android, Apple Watch | Pro reportedly **$4.99/mo** (low-quality source, unverified) | None found | None found | Not stated | Not stated | Apple Watch | No |
| **KeyLifts** | iOS only | Free with in-app purchase (Pro) | 5/3/1 templates only | None found | Built around 5/3/1 cycles | Not stated | Apple Health on Pro | No: 5/3/1-specific |
| **Gravitus** | iOS with Apple Watch companion | Pro monthly or yearly, **amounts not stated** | None found | No CSV export found | Not stated | Not stated | Apple Watch (live heart rate) | No |
| **RepCount** | iOS | Free; Premium in-app purchases **$4.99-$29.99** | None found | None found | Not stated | Not stated | Not stated | No |
| **FitNotes** | Android only | Free | None | CSV export for spreadsheets (not a restorable backup) | Not stated | Not stated | None | Android CSV fallback |
| **Fitbod** | Not stated | **~$15.99/mo or $95.99/yr** (one user review; no official page retrieved) | AI-generated workouts; no import | None found | App-driven | Not stated | Not stated | No |
| **RP Hypertrophy** | iOS app and web app | **$299.99/yr** (competitor comparison) | In-app meso builder; no import | None found | App-driven mesocycles | Not stated | Not stated | No: own periodization, 4-15x the cost of a tracker |
| **JuggernautAI** | Not stated | **$34.99/mo or $349.99/yr**, 2-week trial, no free tier | Program generator, not a custom-program runner | None found | App-driven | Not stated | Not stated | No |
| **Open-source: Liftlog, openGym, GymRoutines** | Liftlog: not stated; openGym: self-hosted PWA (Docker) plus Android APK; GymRoutines: Android (F-Droid), data on device | Free | None documented | GymRoutines: data export and `adb backup`; openGym: your own server | Not stated | Not stated | None | Maximum data ownership, no watch, no import path |

What the table says (the note's inferences, KQ1-KQ3):

- Only **Liftosaur** (text DSL) and **Hevy** (REST API) have a machine-writable input path. Boostcamp's share link is human-to-human.
- **Hevy and Strong** store programs as unscheduled routines, so any order works by construction. **Liftosaur** advances through a defined sequence when a workout is finished, which is exactly what the pointer does. The coach and AI apps (Alpha Progression, RP, JuggernautAI, Fitbod) run their own periodization and are poor fits for an externally maintained program.
- For RPE-driven autoregulation **inside** the app (load computed from RPE), Liftosaur is unique; the others record RPE at best.
- Watch and Health sync is the dominant reliability complaint for Strong and Hevy (KQ4). A lifter who logs on the phone avoids most reported issues.

---

## 3. The recommended three

### 3.1 Liftosaur: the app runs the tracks

**Why.** Liftoscript expresses what the program needs: per-set RPE targets (`@8`), `+` to log the actual RPE, percentages, `kg`/`lb` number types, and `progress:` rules (`lp()` linear, `dp()` double progression, `custom()` for anything else). Programs are plain text, so an agent can render them from the markdown templates and commit them. The app advances to the next program day when a workout is finished, not by weekday, so a 3-day week and a 6-day week both work. Offline, open source, Apple Watch since February 2026.

**Workflow.**

1. An agent renders `templates/liftosaur/rotation.liftoscript` from `templates/6-day-week.md` and `templates/progression-tracks.md`, with your starting loads (section 2 of the tracks file). The current rendering and its README are in that folder.
2. You open the Liftosaur web editor or the app, paste the text (the App Store listing: "You can add this text snippet to the app"), or open a share link the app generates. Exercise names must match the app's library or be created as custom exercises.
3. Train. Finishing L1 advances the program to U1, and so on. In a merged week, do two consecutive program days in one visit and skip the sets the merged template drops (section 3.4 below and the README).
4. Each block (4-6 passes plus deload), or after any stall, reset or gap event, the agent re-renders the file from your logged data and you re-import it. Between renders the app's `lp()` steps do the weekly increments.

**Caveats (all from the note's gaps).** The official grammar for `dp()`, `sum()`, week/day blocks and the share-link URL pattern could not be read; verify at https://www.liftosaur.com/docs. History export format and Premium price are unverified; getting data **out** may mean exporting from the app by hand or keeping the CSV log in section 5 in parallel. `lp()` as described advances on completed reps, not on RPE, so the program's "hold at RPE 8.5-9" rule needs either a `custom()` block (grammar unverified) or a manual override. Wear OS is unconfirmed. Self-hosting the backend is impractical.

### 3.2 Hevy Pro: the agent runs the tracks

**Why.** Hevy has a documented REST API (`api.hevyapp.com`, `api-key` header with a per-account key issued to Pro subscribers at `https://hevy.com/settings?developer`, docs at `https://api.hevyapp.com/docs/`). The official OpenAPI document (read 2026-10-21, note addendum) lists: list, create and update routines and routine folders; list and create exercise templates; list, create and update workouts; workout events since a timestamp; exercise history per template; body measurements. Workout sets carry RPE; routine sets carry load, reps or a rep range, set type and rest, but no RPE. There is no webhook and no delete endpoint. Routines are unscheduled, so the lifter starts whichever one the pointer names. Hevy's pricing is the lowest of the mainstream trackers in the note (KQ4).

**Workflow (implemented in `tools/`, details in `tools/README.md`).**

1. Buy Pro ($23.99/yr or $74.99 lifetime as reported). Generate an API key at hevy.com/settings?developer and store it as the `HEVY_API_KEY` environment secret; never commit it.
2. `python3 tools/hevy_push_routines.py` creates a routine folder named for the program version (`Rotation 2026-10`, from `templates/rotation.json`) and **nine routines** in it: L1 Lower A, U1 Upper A, L2 Lower B, U2 Upper B, L3 Lower C, U3 Upper C, Full A, Full B, Full C. Each exercise carries its sets with the planned load from `data/tracks.json` (warm-up ramp, top set, back-offs at 93%, V sets at 90%, rep ranges for row, pull-up and accessories), the rest timer, and a note with the RPE target and the rule. The free tier's 4-routine cap blocks this, which is why Pro is required.
3. You open the Workout tab, start the routine the pointer names (`data/tracks.json` or the top of `data/track-state.md`), and log load, reps and RPE per set. Hevy's set RPE field is what the API returns.
4. After each pass (weekly), `python3 tools/hevy_sync.py` pulls new workouts (`GET /workouts/events?since=`), applies the track rules in `templates/progression-tracks.md` (section 4 below), rewrites `data/tracks.json`, `data/track-state.md` and `data/track-log.md`, and updates the nine routines in place with the new loads. `--dry-run` shows the decisions without writing. A deload week is pushed with `--deload`. There is no webhook, so the sync is run by hand or on a schedule.

**Caveats.** Hevy has **no progression engine**; every increment, hold, reset and gap modifier is computed by `tools/update_tracks.py` and written back as routine loads. Routine sets have no RPE field, so targets live in the exercise notes. Rate limits are not documented; Hevy asks that scheduled pulls avoid the top of the hour. Hevy says the API may change or be withdrawn. Data lives on Hevy's servers; an unsaved active workout is lost if the app is uninstalled. Apple Health and Watch sync failures are documented in Hevy's own help centre and do not backfill.

### 3.3 Boostcamp (free, manual in, nothing out) or Strong (manual in, CSV out)

**Boostcamp.** Free tier includes the tracker, RPE and RIR on every set, auto-start rest timers per exercise and a limited number of custom programs; Pro ($59.99/yr) lifts the cap. The web program builder saves straight to the app, and a program can be shared by private link. Workflow: use `templates/6-day-week.md` (or the 3-day file) as the entry checklist, build the six half-sessions once in the web builder, train from the app, and keep the private link somewhere private (not in a public repo). Limitation: **no export was found**, so the agent cannot read anything back; you keep the CSV log in section 5 for the main lifts, or send screenshots. Out-of-order starting of program days is unconfirmed; Fortune 2026 named it the best free option.

**Strong.** Templates are schedule-free, RPE is supported and the full history exports as CSV, which is the input an agent parses. The free version has 3 templates, which covers exactly Full A, Full B and Full C (a 3-day-only setup; inference from the cap); the six split sessions plus the three merged forms need PRO ($29.99/yr or $99.99 one-time). Workflow: enter the templates from the markdown, train, export CSV after each pass or block, drop the file in the repo, and the agent analyses it. Hevy imports Strong-format CSV, so a later move to Hevy keeps the history. Downsides: no program import, and the most-reported Watch-sync instability of the group.

### 3.4 Decision guide

| If you... | Use | Because |
|---|---|---|
| Want the app to apply the progression itself and are willing to check a few lines against the docs | **Liftosaur** | Only app with a scriptable progression engine; import by pasting text; works offline |
| Want an agent to do everything over an API and do not mind $24/yr | **Hevy Pro** | Routines and folders writable; workouts (with RPE) and exercise history readable as JSON; the loop is already built in `tools/` |
| Want zero subscription and do not need data back in the repo | **Boostcamp** free, or **Liftosaur** free | Boostcamp: RPE/RIR and timers free. Liftosaur: text import appears to be in the free app (Premium is tied to the API in the note; unverified) |
| Already use Strong and want to keep it | **Strong** + CSV export | Agent parses the CSV; Hevy accepts the same CSV if you move later |
| Train on Android with no watch and want to own the data | **Liftosaur**, **FitNotes** (CSV) or **GymRoutines** (export) | Open or exportable; no sync layer to break |
| Need Apple Watch logging | **Liftosaur** (shipped Feb 2026), **Hevy** or **Strong** | Expect the sync complaints the note records for Hevy and Strong |
| Only train 3 days a week, always | **Strong** free (3 templates = Full A/B/C) or **Liftosaur** | The 3-template cap stops mattering |

Not recommended for this program: Alpha Progression, RP Hypertrophy, JuggernautAI, Fitbod (their own periodization), KeyLifts (5/3/1 only), JEFIT, Setgraph, Gravitus, RepCount (no import or export found).

---

## 4. How agents use the logged data

The loop is the same whichever app you choose; only the first and last steps change.

| Step | What happens | Liftosaur | Hevy Pro | Strong / Boostcamp / manual |
|---|---|---|---|---|
| **1. Export** | Get the sets since the last run into the repo | App export or API (Premium; format **unverified**), else the CSV log | `tools/hevy_pull.py` (`GET /workouts/events?since=` after the first full pull); or the in-app CSV export through `tools/hevy_csv_import.py` | Strong CSV export; Boostcamp: the CSV log (no export found); manual: the CSV or sheet in section 5 |
| **2. Normalise** | Map to the eight columns in section 5; tag each main-lift set as H top set, H back-off, V or substitute from the session slot and the template | Exercise names from the Liftoscript file | Routine title gives the slot (`tools/update_tracks.py`) | `session` column gives the slot |
| **3. Analyse** | Per lift: e1RM from the best heavy set of each H session; e1RM trend (last 3 vs first 3 H exposures, 3-4 weeks); RPE at matched load across exposures (drift); miss counter; days since last exposure (gap clock); weekly hard sets per muscle vs the template tally; readiness flags from the session fields | same | same | same |
| **4. Apply the rules** | From `templates/progression-tracks.md`: increment / hold / miss (section 5); stall after two misses: check sleep, calories, bodyweight first, then reset 7.5% (section 6); second stall: reset and switch to 6s for a block; deload every 4-6 passes or on two readiness flags: top sets x 0.90-0.92, one back-off, V and accessories cut (section 7); gap modifiers (section 8); stale-track rule when the last V set is RPE 6 or lower twice running (section 4); accessories: double progression, drop 5% after two exposures without a rep gained (section 11) | same | same | same |
| **5. Update the program** | Write the new planned loads into the track-state table and the program artefact | Re-render `templates/liftosaur/rotation.liftoscript` with the new starting loads (and the deload or 6-rep variant when one applies) | `tools/update_tracks.py` rewrites `data/tracks.json`; `tools/hevy_push_routines.py` updates each routine in place (`PUT /routines/{id}`) | Update the markdown track table; user edits the app templates by hand |
| **6. Re-import** | Get the update into the app | User pastes the file or opens the share link | Automatic (`tools/hevy_sync.py` does all three steps) | Manual |

Cadence: step 4 runs after every pass (one calendar week for any 3- to 6-day week); the Liftosaur re-render is needed only when the in-app `lp()` steps diverge from the rules (a hold, a miss, a gap, a reset, a deload) or at a block boundary. The agent must never advance a load on a miss or during a deload, must not let a V exposure or a substitute lift change a track, and must log what it changed in the CSV `notes` or a dated line at the top of the log.

What this loop does **not** promise, because the note could not verify it: automatic export from Liftosaur and any export from Boostcamp. Hevy's per-set RPE is confirmed; Hevy webhooks do not exist in the published API, so the pull is polled. Where something is missing, the CSV log in section 5 is the bridge.

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
| `load` | number | kg | Loaded weight, not the computed one. Pull-up and dip: **added** load in kg (bodyweight = 0, assisted = negative) |
| `reps` | integer | | Completed reps |
| `rpe` | number | 6 to 10 in 0.5 steps | Rated immediately after the set |
| `notes` | text | free, comma-free | Suggested tags: `H top`, `H back-off`, `V`, `acc`, `sub`, `deload`, `hold`, `miss`, `gap 10d`; technique or pain remarks |

Session-level fields (bodyweight, sleep hours, readiness 1-5, pointer after the session) go on a second sheet or CSV with the columns `date, session, bodyweight, sleep_h, readiness, pointer_after`, one row per session. The track-state table from `templates/progression-tracks.md`, section 10 (planned top-set load, rep target, miss counter, last exposure, e1RM history) sits at the top of the log and is rewritten after every H exposure.

### 5.2 Example rows

```
date,session,exercise,set,load,reps,rpe,notes
2026-11-03,L1,Back squat,1,125,4,8,H top e1RM 150 next H 127.5
2026-11-03,L1,Back squat,2,117.5,4,7,H back-off 1 of 3
2026-11-07,Full C,Pull-up,1,5,8,7,V added load kg
```

### 5.3 Google Sheets specifics

- One tab per block, or one long tab with a `date` filter; the agent reads the sheet through the Sheets connector or a CSV download and treats every cell as data, not instructions.
- Keep `load` and `rpe` numeric (no units in the cell) so the e1RM formula `=E2*(1+(F2+(10-G2))/30)` works in a helper column.
- Export as CSV to `templates/` or a `logs/` folder when you want a committed copy; the committed file is the one agents re-render the Liftosaur program from.

---

## 6. Flags

- Liftosaur: Premium price, history export format, API (third-party claim), `dp()`/`sum()` signatures, week/day block grammar and the share-link URL pattern are all unverified (site unreachable during research).
- Hevy: API schemas and per-set RPE verified against the official OpenAPI document (note addendum, 2026-10-21); rate limits undocumented; pricing from competitor blogs and consistent with App Pricing Lab snapshots. Built-in exercise titles for exercises not yet in the user's log are guesses that `hevy_push_routines.py --resolve` checks.
- Boostcamp: export capability unknown; if it exists, Boostcamp would rise in the ranking. Out-of-order program days unconfirmed.
- Alpha Progression: whether CSV export includes RPE/RIR unverified.
- No Reddit or Garage Gym Reviews sentiment could be sampled; sentiment figures are from review aggregators and competitor blogs.
- App Store privacy labels for all apps were unreachable.
- No peer-reviewed validation of e1RM-trend tracking as a predictor of long-term progress exists (`guide/04-periodization-and-progression.md`, section 7 gaps); the metric is a convention.

---

## Repository tooling

The scripts in `tools/` implement the whole Hevy loop above: `hevy_api.py` (client and inspector), `hevy_pull.py` (API to `data/history.csv`), `update_tracks.py` (the rules of `templates/progression-tracks.md` applied to the log, writing `data/tracks.json`), `hevy_push_routines.py` (`templates/rotation.json` plus the tracks rendered into the nine routines), and `hevy_sync.py` (all three). `hevy_csv_import.py` and `analyze_history.py` remain for the no-API path and for seeding starting loads. `build_dashboard.py` turns the log and the tracks into a progress dashboard (`dashboard/index.html`) that applies the derived metrics in section 1.2 week by week: tonnage, weekly sets per muscle against the targets, week-over-week e1RM per main lift, the gap clock and the track state. See `tools/README.md`.

## Sources

- `research/mobile-workout-trackers.md` (2026-10-21): KQ1 (per-app profiles, prices, export), KQ2 (Liftoscript syntax; Hevy API operations), KQ3 (any-order rotation; RPE/RIR logging), KQ4 (sentiment, sync complaints), KQ5 (top-3 recommendation and integration paths).
- `templates/progression-tracks.md`, sections 4-8 and 10-11 (what to log, e1RM, increment/hold/miss, stall, deload, gap clock, accessory progression); `guide/04-periodization-and-progression.md`, sections 5 and 7 (e1RM trend over 3-4 weeks, block criteria, Russo et al. 2025); `guide/03-flexible-scheduling.md`, sections 1.4, 4.4 and 4.5 (pointer, gap modifiers, readiness flags).
- Key URLs from the research note: Liftosaur [GitHub README](https://github.com/astashov/liftosaur), [docs](https://www.liftosaur.com/docs), [Liftoscript doc](https://www.liftosaur.com/doc/liftoscript), [new program editor blog](https://www.liftosaur.com/blog/posts/new-experimental-program-editor), [Apple Watch discussion #118](https://github.com/astashov/liftosaur/discussions/118), [App Store listing mirror](https://apps.appfollow.io/ios/liftosaur-scriptable-workouts/1661880849?country=td), [Wellness Project integration page](https://wellnessproject.ai/fr/integrations/liftosaur) (third-party, unverified); Hevy [API docs](https://api.hevyapp.com/docs/), [developer settings](https://hevy.com/settings?developer), [hevy-py README](https://github.com/ewright3/hevy-py), [apis.io auth profile](https://apis.io/security/hevy/hevy-authentication/), [help: export and Strong CSV import](https://help.hevyapp.com/hc/en-us/articles/38001424401943-How-to-Import-Strong-App-CSV-Files-and-Export-Your-Data-in-Hevy), [help: build a program](https://help.hevyapp.com/hc/en-us/articles/34953606698903-Build-a-Workout-Program-Create-Organize-Routines), [help: data on uninstall](https://help.hevyapp.com/hc/en-us/articles/38223672272791-What-will-happen-to-my-information-if-I-uninstall-and-reinstall-the-Hevy-app), [SensAI Hevy review 2026](https://www.sensai.fit/blog/hevy-review-2026) (competitor); Strong [SensAI review](https://www.sensai.fit/es/blog/strong-app-review-2026) (competitor), [App Pricing Lab](https://apppricinglab.com/iap/apple/464254577), [justuseapp reviews](https://justuseapp.com/en/app/464254577/strong-workout-tracker-gym-log/reviews); Boostcamp [custom program builder](https://boostcamp.app/custom-program), [is it free](https://www.boostcamp.app/is-boostcamp-free), [Pro](https://www.boostcamp.app/pro), [RPE/RIR](https://www.boostcamp.app/best/rpe-rir); Alpha Progression [guide](https://alphaprogression.com/en/blog/alpha-progression-guide); FitNotes [Play listing mirror](https://www.bluestacks.com/campaign/com.github.jamesgay.fitnotes/en); GymRoutines [F-Droid](https://f-droid.org/es/packages/com.noahjutz.gymroutines/); openGym [mirror](https://gitea.com/estebanfak/openGym); Fortune [best weightlifting apps](https://www.fortune.com/article/best-weightlifting-apps/).
