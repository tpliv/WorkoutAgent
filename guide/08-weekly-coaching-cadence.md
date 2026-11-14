# 08. Weekly coaching cadence: Sunday check-in and night-before workouts

Last updated: 2026-11-13 (section 4: one sync command that publishes to `main` before it updates Hevy, `tools/week.py` for the week, the lifter's dates, and the manual log as it is really handled; section 3.1: the sample brief obeys its own warm-up and set rules; section 2.2 names the full rule set). Earlier: 2026-11-10 (brief's "rack taken" line names the substitute and its load); 2026-11-06 (check-in asks for waist, drinks and races). Earlier: 2026-10-26 (data flow uses `tools/hevy_sync.py`; short warm-up ramp)

This chapter turns the program into a coach's routine. Every Sunday evening there is a short conversation that plans the week. The evening before each training day, a brief arrives with that session's exact workout. The rules don't change: this chapter only sets *when* the existing rules get applied and *what* you are told. The agent runbooks that carry it out are in `coach/`. The evidence is in `research/coaching-check-ins.md`.

## 1. The rhythm

| When | What happens | You do | Claude does |
|---|---|---|---|
| **Sunday, 6:47 pm ET** | Check-in conversation, about 5 minutes | Answer five questions (section 2) | Recaps the week, applies the start-of-week procedure (`guide/03` §4.1), writes the plan, sends Monday's workout if Monday is a training day |
| **Mon-Sat, 7:47 pm ET** | Night-before brief, only when tomorrow is a training day | Read it; after training, reply with the top sets or log them in Hevy | Folds in today's results, updates the tracks and the pointer, sends tomorrow's session |
| **Training day** | You train | Log every set in Hevy under the routine named after the slot (L1, U1, ..., Full A/B/C), with RPE on top sets | Nothing |

Both runs arrive as push notifications from a Claude session, and you can reply in that session. The nightly run syncs every night. Before a rest day it ends with one line that names the next session (`coach/nightly-brief.md`).

**Why this cadence.** Directly supervised training gave larger strength gains than unsupervised training in Mazzetti 2000 (foundational, pre-2016). It also did in the 2022 meta-analysis by Fisher et al. (strength effect 0.40, 95% CI 0.06-0.74). Neither found a body-composition (hypertrophy) effect. Those studies tested in-person coaching. That remote check-ins help is an inference from the mechanisms the authors suggest: progression gets applied, effort holds up, and sessions get done (`research/coaching-check-ins.md`, KQ3).

## 2. The Sunday check-in

### 2.1 The five questions

1. **Last week:** anything the log won't show? Skipped sessions, substitutions, pain, how the top sets felt.
2. **Readiness, 1-5 each:** sleep, soreness, stress, joint pain. 5 is best for all four, so 5 on joint pain means none.
3. **Bodyweight** (morning, lb), waist if measured, and **drinks last week** (count and which nights). Measurement protocol: `data/body-composition.md` §6.1; alcohol rules: `guide/06` §4.4.
4. **Days available this week, and which days.** If you're unsure between two numbers, give the lower one (`guide/03` §4.1 step 1).
5. **Anything to plan around:** travel, a different gym, a late night, illness, a race or long run (race weeks: `guide/03` §4.7).

The readiness items are the Hooper set (sleep, stress, fatigue, soreness), with joint pain in place of fatigue. Your logged reps and RPE at a known load already measure fatigue, and they are the stronger signal (`research/coaching-check-ins.md`, KQ1).

### 2.2 What Claude does with the answers

In order, using only existing rules:

| Step | Rule source |
|---|---|
| Recap: sessions done vs planned, each main lift's top set and RPE, misses, the pointer | `data/track-state.md`; the Hevy log |
| Update each track from last week's H exposures (step, big step, re-anchor, hold, miss; regain phase and deadlift caution; a stall is flagged, and reset after the recovery check) | `templates/progression-tracks.md` §5, §5.1-5.3, §6 |
| Pick the template from the day count: merges = 6 minus days | `templates/README.md`; `guide/03` §4.1 steps 2-3 |
| Lay the sessions onto your days, starting from the pointer | `guide/03` §4.1 step 3; each template's "Placement" line |
| Apply the gap clock to each lift | `templates/progression-tracks.md` §8 |
| Decide whether this is a deload week | `guide/03` §4.5 |
| Place cardio | `guide/03` §7 |
| Write the week with `python3 tools/week.py plan`, then the reasoning and the check-in record, then run the sync | `data/week.json`; `data/weekly-plan.md`; `data/checkins/`; section 4 |

Then Claude shows the plan in one table and asks you to confirm or change it, and sends Monday's workout.

### 2.3 How the readiness scores are used

- **One low week is a note, not a trigger.** Deload triggers stay as written in `guide/03` §4.5: the scheduled block week, two readiness flags that persist for a week, or illness.
- **A score of 1-2 on the same item two Sundays running counts as one flag.** Reps down or RPE up at the same load on two consecutive exposures counts as another (`guide/07` §1.2). Two flags make a deload week.
- **Loads are not cut in advance for a low score.** The RPE cap on the top set handles a bad day (`research/coaching-check-ins.md`, KQ2).
- **Joint pain at 1-2, or pain that changes how you move:** Claude swaps in the template's substitution for the affected lift and suggests you see a physiotherapist or physician. This guide gives general training guidance only.

## 3. The night-before brief

### 3.1 Format

```
Tomorrow (Tue 27 Oct): Full A = L1 + U1   ~70 min   pointer L1 -> L2
Why anything changed: nothing; all tracks normal.

1. Back squat (squat H)   warm-up 45 x 5, 110 x 2
   135 x 4 @ RPE 8, then 2 x 4 @ 125        rest 3-4 min, then 2-3
2. Bench press (bench H)   feeder 60 x 3
   95 x 4 @ RPE 8, then 2 x 4 @ 90          rest 3-4 min, then 2-3
3. Barbell row (row H)     3 x 6-8 @ 70, RPE 8 every set
4. Seated leg curl         3 x 10-15 @ <logged load>, RPE 8-9
5a/5b Lateral raise 4 x 12-20 @ 15 / OH triceps ext 3 x 10-15 @ 25
6. Standing calf raise     3 x 8-12
Short on time: cut calves to 2, triceps to 2, lateral raise to 3.
Rack taken: bench and row first, then squat. Still taken: Smith squat @ <load>, 3 x 6-10; the squat top set moves to Full C.
After: log in Hevy as "Full A", or reply with the top sets and RPE.
```

Rules for the brief:

- Loads in pounds. The smallest plate is 2.5 lb, so every barbell load is a multiple of 5 lb, warm-ups included (`templates/progression-tracks.md` §9). Back-offs are the top set x 0.93 and V sets are 90% of the track load, both rounded to the nearest 5 lb. Dumbbell and machine work gets one load, never a range.
- **The planned load is a plan. The RPE decides on the day.** If the top set is above RPE 8 at the planned load, follow §3-5 of the tracks file. Claude reads the result the next night.
- The warm-up ramp is for the first compound only (bar x 5, 80% x 2-3; add 60% x 3 between them once the top set is 225 lb or more; `guide/05` §5.1). Each later main lift gets one feeder set at 60-70%. In the sample: 80% of 135 is 108, so 110 x 2; the bench feeder is 65% of 95, so 60 x 3, as the Hevy routine shows it.
- The numbers come from `python3 tools/week.py brief`, which renders the session with the same code as the Hevy routine. Claude adds the lines the tool does not print and never recomputes a load.
- A substitute runs the planned number of working sets: 3 in Full A (top set plus 2 back-offs), 4 in a split L1 (`guide/03` §4.3, "Station taken", step 3).
- One line, "why anything changed", names any rule that fired: gap hold, miss, stall reset, deload, or substitution.
- One line, "short on time", gives the template's own cut order (`guide/03` §4.3).
- One line, "rack taken", names the order to fall back to when the first main lift's station is busy, then the first substitute and its load (`guide/03` §4.3, "Station taken"; `guide/05` §7.4).

### 3.2 When the week changes

| What happened | What the next brief does |
|---|---|
| You trained as planned | Tracks updated after each H exposure; pointer advanced; next session as planned |
| You missed a session | The pointer stays. The next training day does the owed session. No reshuffle, no make-up (`templates/README.md`, "Missed session") |
| A day dropped out | Claude recounts the remaining days and the remaining half-sessions and re-applies the merge rule to what is left (`guide/03` §4.1, "If days change mid-week"). Merging moves to the remaining sessions; top sets are never removed |
| A day was added | The extra day takes the next half-session from the pointer as a split session (`guide/03` §4.1 step 1) |
| You got ill | Claude asks before sending anything. An illness week is a deload week (`guide/03` §4.5); the brief switches to the deload form |
| A top set missed (effective RPE 9.5-10, or 3 reps or fewer) | Logged as a miss. The next H holds the load. Two misses in a row at one load is a stall: Claude flags it, checks sleep, calories and bodyweight with you, then applies the 7.5% reset (`templates/progression-tracks.md` §5-6) |

### 3.3 How it scales with the days you have

| Days this week | Briefs you get | Sessions | Typical length |
|---|---|---|---|
| 3 | 3 (including the Sunday one if Monday is a training day) | Full A, Full B, Full C | 65-75 min |
| 4 | 4 | Full A, L2, U2, Full C | 55-75 min |
| 5 | 5 | L1, U1, L2, U2, Full C | 55-75 min |
| 6 | 6 | L1, U1, L2, U2, L3, U3 | 55-65 min |
| 2 (emergency) | 2 | Full A, Full B, main lifts only; next week starts from L3 | 45-55 min |

The Sunday check-in itself does not change with the day count. Only the number of briefs and the template change.

## 4. Where the data comes from

`main` on GitHub is the source of truth. Hevy and the dashboard page are projections of it. The runbooks are in `coach/`; the tools are described in `tools/README.md`.

- **One command: `python3 tools/hevy_sync.py`.** Both runs use it, the nightly run every night. It is the only way anything reaches GitHub or Hevy. In order:

  | Step | What it does |
  |---|---|
  | 1. Check | The checkout is current with `main` and can write to it. If not: `Sync not started`, and nothing changes anywhere |
  | 2. Pull | New workouts from Hevy into `data/history.csv` |
  | 3. Apply | The progression rules; the tracks, the pointer and the track log |
  | 4. Week | Marks logged sessions done in `data/week.json`; regenerates the tables in `data/weekly-plan.md` |
  | 5. Build | The dashboard, only when data changed |
  | 6. Commit, publish | The changed data files, to `main`. If this fails, Hevy is not touched |
  | 7. Push | Updates only the Hevy routines that differ (the 12 rotation routines and the dated copies in the folder "This Week") and reads each back |

- **The repo is published before Hevy is touched**, so the app never shows something the repo does not hold. The output ends with the week and its Checks (order, spacing, unlogged or unplanned sessions) and a push summary (updated, in step, skipped with the reason, failed). A non-zero exit means something is not in step: Claude says so in the message and runs the command again.
- **A run that cannot save changes nothing.** If the session cannot write to `main`, the sync does not start. Claude sends a read-only message with what the repo already holds and says that today's training is not folded in (`coach/README.md`, "When the repo is read-only").
- **The week lives in `data/week.json`** and is changed only with `python3 tools/week.py` (`plan`, `set`, `add`, `drop`, `deload`), followed by the sync. The loads in a plan or a brief come from `python3 tools/week.py show` or `brief`, which use the same code as the Hevy routines. Claude never computes a load in the chat.
- **Dates are yours, not the server's.** A workout's date, and "today" for the week, the push and the gap clock, is the calendar day in America/New_York (`tools/localtime.py`), not the UTC date. The 7:47 pm brief and an evening session are dated that evening.
- **The key.** The Hevy key is normally a network secret for `api.hevyapp.com` (header `api-key`; the proxy adds it). The alternative is the `HEVY_API_KEY` environment variable. Never put it in the repo or the chat.
- Start each workout from the day's routine so its title names the slot. That is how a logged workout maps onto the rotation and marks the planned session done.
- **Fallback: tell Claude.** When the Hevy API is down or a pull fails, Claude asks for the top sets in the conversation and appends them by hand to `data/manual-log.csv` (the columns of `templates/log-template.csv`, with the load in pounds). **No tool reads that file.** Claude applies `templates/progression-tracks.md` §5 itself and enters each changed value as a logged amendment:

  ```
  python3 tools/update_tracks.py --set bench.top_set_lb=115 --reason "chat: 110 x 4 @ 7.5 on 10 Nov"
  python3 tools/hevy_sync.py --no-pull
  ```

  The amendment is written to `data/track-log.md`. When the API is back the workout is pulled as usual, and Claude checks the track log so the session is not counted twice.
- **What is written, and by what:**

  | File | Written by |
  |---|---|
  | `data/history.csv`, `data/tracks.json`, `data/track-log.md`, the generated tables in `data/track-state.md` and `data/weekly-plan.md`, `dashboard/` | The sync |
  | `data/week.json` | `tools/week.py` |
  | The reasoning in `data/weekly-plan.md`, `data/checkins/YYYY-MM-DD.md` (one record per Sunday), `data/manual-log.csv` | By hand |

  The sync commits and publishes all of these, so the next run starts from them.

## 5. Flags

- No study has tested remote or AI check-ins, or a written pre-session brief. Section 1 is an inference from in-person supervision trials.
- The Hooper index's original scoring was not checked against the 1995 paper. The 1-5 scale here matches this program's existing session readiness score.
- The two-Sundays rule for a low readiness item (section 2.3) is a convention set by this guide. It counts toward the existing two-flag deload trigger and adds no new trigger.

## Sources

- `research/coaching-check-ins.md`: KQ1 (Saw, Main & Gastin 2016, *Br J Sports Med* 50:281; Hooper & Mackinnon 1995, *Sports Med* 20:321), KQ2 (Zourdos et al. 2016, *JSCR* 30:267; Helms et al. 2016, *Strength Cond J* 38(4):42), KQ3 (Mazzetti et al. 2000, *MSSE* 32:1175; Fisher et al. 2022, *Int J Strength Cond* 2(1)).
- `guide/03-flexible-scheduling.md` §4.1-4.6 for the weekly procedure, merges, missed sessions, and deloads.
- `templates/progression-tracks.md` §3-10 for every load decision.
- `guide/07-tracking-and-apps.md` §3.2 and §4 for the Hevy loop.
