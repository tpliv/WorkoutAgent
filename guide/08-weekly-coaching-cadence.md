# 08. Weekly coaching cadence: Sunday check-in and night-before workouts

Last updated: 2026-10-21

This chapter turns the program into a coach's routine. Every Sunday evening there is a short conversation that plans the week. The evening before each training day, a brief arrives with that session's exact workout. The rules don't change: this chapter only sets *when* the existing rules get applied and *what* you are told. The agent runbooks that carry it out are in `coach/`. The evidence is in `research/coaching-check-ins.md`.

## 1. The rhythm

| When | What happens | You do | Claude does |
|---|---|---|---|
| **Sunday, 6:47 pm ET** | Check-in conversation, about 5 minutes | Answer five questions (section 2) | Recaps the week, applies the start-of-week procedure (`guide/03` §4.1), writes the plan, sends Monday's workout if Monday is a training day |
| **Mon-Sat, 7:47 pm ET** | Night-before brief, only when tomorrow is a training day | Read it; after training, reply with the top sets or log them in Hevy | Folds in today's results, updates the tracks and the pointer, sends tomorrow's session |
| **Training day** | You train | Log every set in Hevy under the routine named after the slot (L1, U1, ..., Full A/B/C), with RPE on top sets | Nothing |

Both runs arrive as push notifications from a Claude session, and you can reply in that session. On a rest day the nightly run ends without messaging you.

**Why this cadence.** Directly supervised training gave larger strength gains than unsupervised training in Mazzetti 2000 (foundational, pre-2016). It also did in the 2022 meta-analysis by Fisher et al. (strength effect 0.40, 95% CI 0.06-0.74). Neither found a body-composition (hypertrophy) effect. Those studies tested in-person coaching. That remote check-ins help is an inference from the mechanisms the authors suggest: progression gets applied, effort holds up, and sessions get done (`research/coaching-check-ins.md`, KQ3).

## 2. The Sunday check-in

### 2.1 The five questions

1. **Last week:** anything the log won't show? Skipped sessions, substitutions, pain, how the top sets felt.
2. **Readiness, 1-5 each:** sleep, soreness, stress, joint pain. 5 is best for all four, so 5 on joint pain means none.
3. **Bodyweight** (morning, lb).
4. **Days available this week, and which days.** If you're unsure between two numbers, give the lower one (`guide/03` §4.1 step 1).
5. **Anything to plan around:** travel, a different gym, a late night, illness.

The readiness items are the Hooper set (sleep, stress, fatigue, soreness), with joint pain in place of fatigue. Your logged reps and RPE at a known load already measure fatigue, and they are the stronger signal (`research/coaching-check-ins.md`, KQ1).

### 2.2 What Claude does with the answers

In order, using only existing rules:

| Step | Rule source |
|---|---|
| Recap: sessions done vs planned, each main lift's top set and RPE, misses, the pointer | `data/track-state.md`; the Hevy log |
| Update each track from last week's H exposures (increment, hold, miss, stall reset) | `templates/progression-tracks.md` §5-6 |
| Pick the template from the day count: merges = 6 minus days | `templates/README.md`; `guide/03` §4.1 steps 2-3 |
| Lay the sessions onto your days, starting from the pointer | `guide/03` §4.1 step 3; each template's "Placement" line |
| Apply the gap clock to each lift | `templates/progression-tracks.md` §8 |
| Decide whether this is a deload week | `guide/03` §4.5 |
| Place cardio | `guide/03` §7 |
| Write the week plan and the check-in record | `data/weekly-plan.md`; `data/checkins/` |

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

1. Back squat (squat H)   warm-up 45x10, 55x8, 80x5, 110x3
   135 x 4 @ RPE 8, then 2 x 4 @ 125        rest 3-4 min, then 2-3
2. Bench press (bench H)   feeder 60 x 5
   95 x 4 @ RPE 8, then 2 x 4 @ 90          rest 3-4 min, then 2-3
3. Barbell row (row H)     3 x 6-8 @ 70, RPE 8 every set
4. Seated leg curl         3 x 10-15 @ <logged load>, RPE 8-9
5a/5b Lateral raise 4 x 12-20 @ 15 / OH triceps ext 3 x 10-15 @ 25
6. Standing calf raise     3 x 8-12
Short on time: cut calves to 2, triceps to 2, lateral raise to 3.
After: log in Hevy as "Full A", or reply with the top sets and RPE.
```

Rules for the brief:

- Loads in pounds. The smallest plate is 2.5 lb, so every barbell load is a multiple of 5 lb, warm-ups included (`templates/progression-tracks.md` §9). Back-offs are the top set x 0.93 and V sets are 90% of the track load, both rounded to the nearest 5 lb. Dumbbell and machine work gets one load, never a range.
- **The planned load is a plan. The RPE decides on the day.** If the top set is above RPE 8 at the planned load, follow §3-5 of the tracks file. Claude reads the result the next night.
- The warm-up ramp is for the first compound only (bar x 10, 40% x 8, 60% x 5, 80% x 2-3). Each later main lift gets one feeder set at 60-70%.
- One line, "why anything changed", names any rule that fired: gap hold, miss, stall reset, deload, or substitution.
- One line, "short on time", gives the template's own cut order (`guide/03` §4.3).

### 3.2 When the week changes

| What happened | What the next brief does |
|---|---|
| You trained as planned | Tracks updated after each H exposure; pointer advanced; next session as planned |
| You missed a session | The pointer stays. The next training day does the owed session. No reshuffle, no make-up (`templates/README.md`, "Missed session") |
| A day dropped out | Claude recounts the remaining days and the remaining half-sessions and re-applies the merge rule to what is left (`guide/03` §4.1, "If days change mid-week"). Merging moves to the remaining sessions; top sets are never removed |
| A day was added | The extra day takes the next half-session from the pointer as a split session (`guide/03` §4.1 step 1) |
| You got ill | Claude asks before sending anything. An illness week is a deload week (`guide/03` §4.5); the brief switches to the deload form |
| A top set missed (RPE 9.5-10 or under 4 reps) | Logged as a miss. The next H holds the load; two misses in a row trigger the 7.5% reset (`templates/progression-tracks.md` §5-6) |

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

- **Default: Hevy Pro API.** Both runs pull new workouts with `tools/hevy_pull.py`. That needs the Hevy key stored as a network secret for `api.hevyapp.com` (or as `HEVY_API_KEY`); never put it in the repo or the chat. Name each Hevy workout after its slot so a workout maps onto the rotation.
- **Fallback: tell Claude.** When there is no key, or a pull fails, Claude asks for the top sets in the conversation. It records them in `data/manual-log.csv`, which uses the columns of `templates/log-template.csv` and is in pounds. `tools/analyze_history.py --history data/manual-log.csv` reads it.
- **What is written:** `data/track-state.md` (tracks and pointer), `data/weekly-plan.md` (this week), `data/checkins/YYYY-MM-DD.md` (one record per Sunday). The scheduled sessions commit and push these, so the next run starts from them.

## 5. Flags

- No study has tested remote or AI check-ins, or a written pre-session brief. Section 1 is an inference from in-person supervision trials.
- The Hooper index's original scoring was not checked against the 1995 paper. The 1-5 scale here matches this program's existing session readiness score.
- The two-Sundays rule for a low readiness item (section 2.3) is a convention set by this guide. It counts toward the existing two-flag deload trigger and adds no new trigger.

## Sources

- `research/coaching-check-ins.md`: KQ1 (Saw, Main & Gastin 2016, *Br J Sports Med* 50:281; Hooper & Mackinnon 1995, *Sports Med* 20:321), KQ2 (Zourdos et al. 2016, *JSCR* 30:267; Helms et al. 2016, *Strength Cond J* 38(4):42), KQ3 (Mazzetti et al. 2000, *MSSE* 32:1175; Fisher et al. 2022, *Int J Strength Cond* 2(1)).
- `guide/03-flexible-scheduling.md` §4.1-4.6 for the weekly procedure, merges, missed sessions, and deloads.
- `templates/progression-tracks.md` §3-10 for every load decision.
- `guide/07-tracking-and-apps.md` §3.2 and §4 for the Hevy loop.
