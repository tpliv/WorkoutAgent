# 03. Flexible scheduling: one program for 3-day and 6-day weeks

Last updated: 2026-10-21

**The question this chapter answers:** "How do I run one program when some weeks I have 3 days and other weeks 5-6?"

**The short answer:** the program is a rotation of six half-sessions. In a 6-day week each half-session is its own workout. In a 3-day week you merge them in pairs into three full-body workouts. In between, you merge some and split some. Every week from 3 to 6 days completes exactly one pass of the rotation, so every main lift gets the same two exposures and its load advances at the same pace. What changes with the day count is accessory volume and back-off sets, never the top-set loads.

This chapter owns the weekly layouts, the rotation pointer, the merge and cut rules, the resume-after-a-gap rules, and how the mesocycle is counted. The per-lift progression rules are in `templates/progression-tracks.md`; the full session tables are in `templates/`. Other chapters refer here and do not prescribe their own layouts (design spine).

Units: kilograms throughout (2.5 kg is about 5 lb; 1 kg is about 2 lb).

---

## 1. The rotation

### 1.1 Six half-sessions, three blocks

| Slot | Name | Main-lift work (track exposure) | Other work |
|---|---|---|---|
| L1 | Lower A | **Squat: heavy (H)** | Romanian deadlift, leg press or split squat, seated leg curl, calves, core |
| U1 | Upper A | **Bench: heavy (H)**, **Row: heavy (H)** | Incline DB press, lateral raise, overhead triceps extension, face pull |
| L2 | Lower B | **Deadlift: heavy (H)** | Front or hack squat, lunge or split squat, seated leg curl, calves, back extension or anti-rotation core |
| U2 | Upper B | **Overhead press: heavy (H)**, **Pull-up or pulldown: heavy (H)** | Flat DB press or dips, reverse pec deck, lateral raise, incline DB curl |
| L3 | Lower C | **Squat: volume (V)**, **Deadlift: volume (V)** | Seated leg curl, leg extension, calves, core |
| U3 | Upper C | **Bench: volume (V)**, **Overhead press: volume (V)**, **Row: volume (V)**, **Pull-up: volume (V)** | Lateral raise, triceps pushdown, curl |

- **Block A** = L1 + U1. **Block B** = L2 + U2. **Block C** = L3 + U3.
- Merging a block's two halves into one workout gives **Full A**, **Full B**, **Full C**.
- The order never changes: L1, U1, L2, U2, L3, U3, then back to L1. Lower and upper always alternate, so on consecutive training days different muscles do the heavy work (recovery: `guide/06-recovery-nutrition-cardio.md`, section 1).
- **H exposure** = work up to one top set of 4 at RPE 8, then back-off sets 7% lighter. **V exposure** = straight sets at 90% of the lift's current top-set load, no top set. Exact numbers: `templates/progression-tracks.md`.

### 1.2 Main-lift exposures per pass

| Main lift | Heavy exposure | Volume exposure | Exposures per pass |
|---|---|---|---|
| Squat | L1 | L3 | 2 |
| Bench press | U1 | U3 | 2 |
| Deadlift | L2 | L3 | 2 |
| Overhead press | U2 | U3 | 2 |
| Barbell row | U1 | U3 | 2 |
| Pull-up / pulldown | U2 | U3 | 2 |

Because every 3- to 6-day week is one pass, **every main lift is trained twice a week in every week type**, and its progression track advances once per week (at the H exposure) whether the week had 3 sessions or 6. That satisfies the "main lifts 2x even in short weeks" rule in `guide/01-training-principles.md`, section 3, and the one-track-per-lift rule in the design spine.

### 1.3 How the four week types map onto the rotation

```
Rotation:  L1 -> U1 -> L2 -> U2 -> L3 -> U3 -> (L1 ...)

6 days:    L1 | U1 | L2 | U2 | L3 | U3            (0 merges)
5 days:    L1 | U1 | L2 | U2 | [L3+U3 = Full C]    (1 merge)
4 days:    [L1+U1 = Full A] | L2 | U2 | [Full C]   (2 merges)
3 days:    [Full A] | [Full B] | [Full C]          (3 merges)
```

**Rule: merges this week = 6 minus the days you have.** Merge block C first, then A, then B. Block C merges cheapest because its exposures are all volume sets with no top sets; blocks A and B carry the heavy top sets and are merged only when you must.

### 1.4 The rotation pointer

The pointer is the next half-session you owe. It is the only state the schedule needs.

- A split session advances the pointer by one. A merged session advances it by two.
- After a complete 3- to 6-day week the pointer is back at L1. It only drifts when you miss a session or train fewer than 3 days.
- **Never skip ahead.** Whatever the calendar says, the next time you train you do the half-session the pointer names (or merge it with the one after it). The pointer, not the weekday, is the authority (practitioner consensus: RP's floating split, GZCLP, 5/3/1 on 3 days; `research/flexible-frequency-programming.md`, KQ1, KQ5).

---

## 2. Why a rotation, and why merging works

### 2.1 Frequency does not matter when weekly volume is equated

With weekly sets held constant, how many sessions they are spread over has no detectable effect on hypertrophy and only a small, diminishing effect on strength.

| Finding | Source |
|---|---|
| 25 studies, 836 participants: frequency "does not significantly or meaningfully impact muscle hypertrophy when volume is equated" | Schoenfeld, Grgic & Krieger 2019 (`research/frequency-volume-intensity-evidence.md`, Q1) |
| 67 studies: +0.32% size per extra training day with volume in the model (95% CrI -0.14 to 0.82%), "compatible with negligible effects"; for strength a positive frequency effect with diminishing returns (1 to 2 days helps more than 3 to 4) | Pelland et al. 2025/26 (Q1) |
| Trained men, 3x vs 6x per week with identical weekly work: similar strength and body composition | Colquhoun et al. 2018 (Q1, Q7) |
| Trained lifters, 2 vs 4 sessions per week, equal volume: no differences in lean mass, muscle thickness, or 1RM; spreading volume may lower per-session RPE | Hamarsland et al. 2022; Johnsen & van den Tillaar 2021 (Q1) |
| Volume-equated frequency comparisons for strength: no significant effect (Grgic 2018, p = 0.421; Ralston 2018, ES 0.03) | Q1 |

So three full-body sessions that carry the same main-lift exposures as six split sessions lose nothing per set. The 3-day week in this program is not a compromise on quality; it is a cut in quantity.

### 2.2 The per-session ceiling is why more days buy more volume

Per-session hypertrophy returns become undetectable beyond about 11 fractional sets per muscle (Remmert et al. 2025, preprint; the 11 / 2 figures are from a Biolayne summary, **secondary, unverified**), and older set-count work plateaus around 4-6 sets per exercise (Krieger 2009-2010, **older**). The spine plans at 8-10 hard sets per muscle per session. A 6-day week can hold 14-20 weekly sets per muscle under that ceiling; a 3-day week cannot, so it runs 8-12. The 3-day week is deliberately lower in volume, not a compressed 6-day week (`research/frequency-volume-intensity-evidence.md`, Q2, Q7).

### 2.3 Maintenance evidence says the short week is not a lost week

| Finding | Source |
|---|---|
| Young adults kept myofiber hypertrophy for 32 weeks on 1/3 or 1/9 of their prior training dose; the 1/3 dose built additional muscle. Older adults (60-75) did not maintain. | Bickel, Cross & Bamman 2011 (**older**; Q6) |
| Size and strength maintained up to 32 weeks on 1 session and 1 set per exercise per week "as long as exercise intensity (relative load) is maintained"; older people likely need 2 sessions and 2-3 sets | Spiering et al. 2021 (Q6) |
| ~3-6 heavy sets of 1-5 per week at >80% 1RM maintained or improved 1RM in powerlifters | Androulakis-Korakakis 2021 (Q6) |

A 3-day week in this program runs about 50-55% of the 6-day week's sets at the same top-set loads. That is well above the maintenance floor, so it should still build. **Intensity is the lever to protect; volume is the lever to cut.**

Age flag (spine): the maintenance data come from 20-35-year-olds. A lifter in their late 40s or 50s should keep short weeks at the one-half end (do not drop the optional sets in the 3-day template) and should not run two 3-day weeks in a row without good reason.

### 2.4 Caveats

- No study has tested alternating 3-day and 6-day weeks within one program; the design is assembled from volume-equated frequency trials plus maintenance data (Q7 gaps; `research/flexible-frequency-programming.md`, KQ3 gaps).
- No peer-reviewed or coach-published test of merged versus separate sessions exists; the merge rules below are synthesised from the per-session ceiling and practitioner practice (KQ5 gaps).
- The 8-21-day and >21-day load modifiers in section 4.4 are inferences from detraining timelines, not from a study that quantified them (KQ6 gaps).

---

## 3. Volume and frequency by available days

| Available days | Sessions this week (in order) | Per-muscle frequency | Weekly hard sets per large muscle group | Main-lift exposures | Session length |
|---|---|---|---|---|---|
| 2 (emergency) | Full A, Full B (main lifts only, see 4.6) | 2x | 4-6 | 1 per lift (squat, bench, row, deadlift, press, pull-up) | 45-55 min |
| 3 | Full A, Full B, Full C | 3x for large muscles; 2x direct for small muscles | 8-12 (calves and arms 5-8 direct plus indirect credit) | 2 per lift | 65-75 min |
| 4 | Full A, L2, U2, Full C | 3x | 10-14 | 2 per lift | Full sessions 65-75 min; split sessions 55-65 min |
| 5 | L1, U1, L2, U2, Full C | 3x | 14-17 | 2 per lift | Split 55-65 min; Full C 65-75 min |
| 6 | L1, U1, L2, U2, L3, U3 | 3x | 15-20 | 2 per lift | 55-65 min |

Notes. "Hard sets" counts direct sets plus half credit for indirect work (a pressing set counts 0.5 for triceps; a row 0.5 for biceps and rear delts), as in `guide/01-training-principles.md`, section 1. Session lengths use the time budget in `guide/05-exercise-selection.md` (a compound set with 2-3 min rest costs about 3 min; an isolation set about 2 min; paired accessories about 2.25 min per set; plus about 5-6 min warm-up; the ranges below were set with the earlier 8-min warm-up, so sessions may run 2-3 min shorter). Exact per-muscle tallies are at the bottom of each template.

Why frequency reads "3x" everywhere: every block contains every muscle, and every 3- to 6-day week does all three blocks. The spine's minimum (2x in a 3-day week, 2-3x in a 5-6-day week) is met with margin. Small muscles get two direct exposures in a 3-day week plus indirect credit from the compounds.

---

## 4. The rules

### 4.1 Start-of-week decision procedure

Do this once, before the first session of the week. It takes two minutes.

1. **Count the days you can actually train this week.** If unsure between two numbers, plan the lower one; an extra day can be added at the end of the week as a split session without harm (see step 6).
2. **Pick the template:** 3 days = `templates/3-day-week.md`; 4 = `4-day-week.md`; 5 = `5-day-week.md`; 6 = `6-day-week.md`. 2 days: section 4.6. 7 days: train 6, the seventh is cardio or rest.
3. **Read the pointer.** If it says L1, the template applies as written. If it points elsewhere (you missed a session last week, or ran a 2-day week), write down the next six half-sessions starting from the pointer, then apply the merge count for your day number: merges = 6 minus days. Merge consecutive pairs, preferring L3+U3, then L1+U1, then L2+U2; if the pointer sits mid-block, cross-block pairs (U1+L2, U2+L3, U3+L1) are allowed, because consecutive half-sessions are always one lower and one upper (merge rule, 4.2).
4. **Check each main lift's days since its last exposure** (any H or V exposure counts). Apply the modifier in 4.4 to its planned top-set load.
5. **Write the planned loads into the log** from the tracks (`templates/progression-tracks.md`). Planned, not promised: the RPE cap on the top set decides on the day.
6. **Decide whether this is a deload week** (4.5). If it is, apply the deload version of whichever template you picked. A deload week is a week type, not a day count.
7. **Place cardio** (section 7).

If days change mid-week: recount the remaining days and the remaining half-sessions in the pass and re-apply step 3 to what is left. A week that cannot finish its pass just leaves the pointer where it stops.

### 4.2 Merging two rotation workouts into one

A merged workout is one lower half plus one upper half, done in one session. The rule set is exact.

1. **Keep every main-lift exposure from both halves.** Cut back-offs, not top sets: an H exposure runs its top set plus **2 back-offs** in a merged session instead of 3 (deadlift: top set plus 2 in both forms, because it already runs fewer). A V exposure runs **3 sets** instead of 4 (deadlift and press V: 2 sets instead of 3; row V stays at 3; pull-up V 2 instead of 3). The row and pull-up H exposures run 3 sets instead of 4.
2. **Order:** the heavy lower lift first, then the heavy press, then the heavy pull, then accessories. In Full C (all volume): squat, bench, deadlift, press, row, pull-up, alternating lower and upper so that you can run adjacent lifts as alternating paired sets when two stations are free.
3. **Keep two or three accessories, 3 sets each,** chosen so that across the week each undertrained muscle (side and rear delts, hamstrings via a curl, calves, biceps, triceps long head, upper chest; `guide/05-exercise-selection.md`, section 1) gets at least one direct exposure. The templates make the choice for you. Pair accessories as supersets with 60 s between exercises and 2 min between pairs.
4. **Cap the session at about 22 hard sets and about 8 sets per muscle**, and at about 75 minutes. Anything from either half that does not fit is **dropped, not postponed**. It comes back next week when the day count allows.
5. **Never merge two lower halves or two upper halves.** Consecutive half-sessions in the rotation are always one of each, so this only arises if you reorder, which you do not.
6. **Never put more than two half-sessions in one day.** A 2-day week does two merged sessions and leaves the pointer at L3 (4.6).

Support: the merge rule follows the "keep the main compound, drop accessories and conditioning first; merge only compatible sessions; never two heavy lower sessions in one day" consensus in `research/flexible-frequency-programming.md`, KQ5, and the per-session ceiling in `research/frequency-volume-intensity-evidence.md`, Q2. No trial has tested merged against separate sessions (KQ5 gaps).

### 4.3 What to drop first (the priority stack)

When a session must shrink, whether because the week shrank or because today is short, cut from the bottom of this list and stop as soon as it fits. Never cut above line 2.

| Priority | Keep or cut | What it is |
|---|---|---|
| 1 (never cut) | Keep | Top set of each main lift in the session. This is the progression track and the intensity signal the maintenance evidence depends on. |
| 2 (cut last) | Keep | Second exposure of a main lift (the V sets) down to 2 sets; row and pull-up H sets down to 3; first back-off set. |
| 3 | Cut fourth | The hamstring curl, the side-delt raise, and the one upper-chest exposure of the week (the direct work for the muscles compounds miss). |
| 4 | Cut third | Accessory compounds: leg press, lunge, incline DB press, flat DB press, front squat. |
| 5 | Cut second | Second and third back-off sets; fourth set of any accessory; rear-delt, biceps and triceps isolation down to 2 sets. |
| 6 | Cut first | Core work, calves below 2 sets, any exercise that trains a muscle already hit directly in the same session, and conditioning done in the same session. |

Why in this order: intensity on the main lifts is what maintenance studies hold constant (Spiering 2021); strength is cheap in volume, so one or two heavy direct sets carry most of the strength signal (Remmert 2025, secondary; Androulakis-Korakakis 2021); the undertrained-muscle isolations are the reason the program is not compounds-only (`guide/05-exercise-selection.md`, section 1); everything else is volume that the next longer week restores. The priority order matches the GZCL tier logic (keep T1, trim T2, drop T3), which `research/flexible-frequency-programming.md` KQ2 flags as an inference from the tier structure, not a quoted Lefever rule.

**Readiness gate for a single bad day** (`research/flexible-frequency-programming.md`, KQ4): if you slept under 6 hours, are unusually sore, or the work-up sets feel a full RPE heavier than planned, keep the top set (the RPE cap sets the load), cut back-offs and accessories by about one-third **for that session only**, and change nothing else in the block. "What you do in a single session has little impact on your trajectory" (Barbell Medicine coaching reply, forum source).

### 4.4 A session skipped mid-rotation, and days since a lift was last trained

**Skipped session.** The pointer does not move. The next time you train, do the half-session it names. Do not reshuffle the remaining week to make it "balanced"; the rotation balances itself over passes, and the next time you plan a week you count days and merge from the pointer (4.1, step 3). If you want to catch up, merge the owed half-session with the next one (4.2) rather than doing an extra day. A single week with one missed session costs nothing measurable (`guide/01-training-principles.md`, section 7).

**Gap modifier per main lift.** Each lift carries its own clock: days since its last exposure of any kind (H or V). Apply the modifier to the planned top-set load at the next H exposure; V exposures then inherit 90% of whatever load the modifier produced.

| Days since the lift was last trained | What to do with the top-set load | Back-offs | Why |
|---|---|---|---|
| 0-7 | Normal rule: take the planned increment if the last top set earned it | Normal | Inside the normal exposure spacing; one week off costs 3-7% strength that returns in 1-2 sessions (detraining summaries, FFP KQ3, secondary) |
| 8-14 | **Hold.** Repeat the last top-set load; no increment this exposure. If it comes in at RPE <= 7.5, take the increment next exposure | Normal | Detraining is not yet measurable but the skill is slightly stale; hold, let the RPE confirm |
| 15-21 | **Hold** the last load; one fewer back-off set | One fewer | Approaching the ~3-week line where strength loss becomes noticeable (Nippard; FFP KQ3) |
| 22-28 | **Reduce 5%.** First exposure capped at RPE 7; resume normal rules from the second exposure | Normal count | A 4-week layoff cut 1RM about 6-9% in trained men (BarBend summary, secondary) |
| > 28 | **Reduce 10%.** First exposure at RPE 6-7 (3-4 RIR), second at RPE 7-8, then normal rules | Normal count | Comeback guidance: compounds at RPE <= 5-6 in the first week back, avoid soreness (Nippard) |

"Hold" versus "reduce": hold the load for gaps of 8-21 days; reduce it for gaps over 21 days. The modifier is applied at an H exposure. If a V exposure is the first thing a lift does after a gap of 8 or more days, do it as written (it is already at 90% of the track load) and it resets the clock, so the H exposure that follows runs the normal rule; the V sets are the re-greasing the gap needs. This table is an inference from detraining timelines; no source quantifies progression adjustments by days since exposure (`research/flexible-frequency-programming.md`, KQ6 gaps). The RPE cap on the top set makes the table self-correcting: if the held load is easy, the next increment follows; if it is hard, you hold again.

If the whole program stopped for more than 3 weeks (illness, travel), treat the first week back as a 3-day week with the modifiers above, whatever your day count, and do not count it toward the block (section 5).

### 4.5 When a short week is a deload, and when it is not

A 3-day week is **not** a deload by default. It keeps the top sets at RPE 8, advances every track, and runs about half the 6-day volume, which the maintenance evidence says still builds. Calling it a deload would throw away the intensity the short week exists to protect.

Treat a week (short or long) as a deload when **any** of these holds:

1. It is the scheduled deload week: week 5, 6 or 7 of the block (section 5).
2. Two or more readiness red flags have persisted for a week: reps down or RPE up at the same load on two consecutive exposures of a lift; mood or perceived recovery worse on most days; sleep efficiency down; joint pain that does not clear between sessions (`guide/06-recovery-nutrition-cardio.md`, section 2; `guide/04-periodization-and-progression.md`, section 3).
3. The short week is caused by illness.

A deload week in this program (spine item 5; Bell 2023 Delphi; Coleman 2024):

- **Keep the frequency** of the week you have (3, 4, 5 or 6 sessions). Do not take the week off: a full week of rest mid-block cost lower-body strength in the only RCT (Coleman 2024).
- **Top sets at RPE 6-7**: about 8-10% below the current track load, same reps. The track does not advance; after the deload resume at the pre-deload load.
- **Halve the sets:** one back-off instead of 2-3; V exposures 2 sets; accessories 1-2 sets; isolation kept light.
- **Keep every main lift in** so the strength expression does not detrain.

Timing rule: a deload is planned to land on a 3-day week when the calendar allows, because that is the cheapest week to lose volume in. A 3-day week that falls elsewhere in the block **counts toward the block** (the block clock is passes, section 5) and does not postpone or replace the planned deload. Do not run two deloads within four weeks of each other; if a reactive deload fires in week 3, the next planned one moves to week 8 or 9.

### 4.6 Two-day weeks, seven-day weeks, doubling

- **2 days (emergency):** do Full A and Full B with main lifts only (top set plus 1 back-off per H lift; row and pull-up 3 sets) plus one lower and one upper accessory each. The pointer ends at L3; next week starts with Full C or L3. One heavy set per pattern at full load is above the maintenance floor (Spiering 2021; Bickel 2011; `research/flexible-frequency-programming.md`, KQ3 inferences).
- **7 days:** do not add a seventh lifting session. Use the day for cardio or rest. Weekly volume is already at the top of the range in a 6-day week; trained lifters pushed to 60 sets per week showed no extra size and a deadlift penalty (Räntilä 2026).
- **Two sessions in one day:** only as a merge (4.2), never two heavy lower halves, and never as a way to "get ahead" of the pointer.
- **Consecutive days:** fine. The rotation alternates lower and upper, so a heavy muscle group gets about 48 h before its next hard exposure (`guide/06-recovery-nutrition-cardio.md`, section 1). A 4-day week on Mon/Tue/Thu/Fri puts Full A (squat H) and L2 (deadlift H) on consecutive days; that is acceptable because the patterns differ and the RPE cap sets the load, but Mon/Wed/Thu/Sat is preferred.

---

## 5. Progression stays on one track per lift

Each main lift has one track (`templates/progression-tracks.md`): a current top-set load, a rep target, an exposure counter, a miss counter, and an e1RM history.

- **The track updates at the H exposure.** If the top set hits 4 reps at RPE <= 8, the load rises for the next H exposure (+2.5 kg squat and deadlift; +1 kg bench and press, or +2.5 kg every second successful exposure without fractional plates). RPE 8.5-9: hold. Missed reps or RPE 10: hold and count a miss. Two misses in a row at one load: stall rule (reset 7.5% and rebuild, with a rep-zone change on a second stall).
- **The V exposure reads from the track.** Its sets are 90% of the current top-set load. It does not change the load, but it is an exposure for the gap clock and its sets are logged for the e1RM trend.
- **Day count never touches the track.** A 3-day week and a 6-day week each contain exactly one H and one V exposure per lift, so loads advance at one step per week in both. The only main-lift variables that change with the day count are the number of back-off sets (3 in a split session, 2 in a merged one) and the number of V sets (4 versus 3).
- **Exposure count, not calendar, is the unit** (`research/flexible-frequency-programming.md`, KQ6; 5/3/1 stretches its 4-week cycle to 5+ weeks at 3 days per week; GZCLP progresses per completed session). If a pass spills across two calendar weeks because a session was missed, the lift's track simply advances when its H exposure happens.
- **The block clock is counted in passes.** A block is 4-6 passes plus a deload pass. For any 3- to 6-day week a pass equals a calendar week, so "week 5 of the block" means the same thing on the calendar and in the log. A 2-day week or a missed session stretches a pass, and the block stretches with it. (This is the counting rule `guide/04-periodization-and-progression.md`, section 4, defers to; because every 3- to 6-day week completes a pass, a 3-day week does not take two calendar weeks to finish an exposure wave in this program.)
- **Accessories** progress by double progression within their rep range (reps up to the top of the range on all sets, then load up and reps back down), whatever week type they appear in. A 3-day week does not reset an accessory's load; it only skips some of its sets.

How a missed rep target is handled (the question `guide/05-exercise-selection.md`, section 3, points here): a main lift placed later in a merged session may miss a rep at a load it made last week. That counts as a miss for the stall rule only if the top set was taken fresh in the usual slot. In a merged session, the top set of the second and third main lifts is judged by RPE: if it reaches RPE 9-10 for 4 reps, log it as "hold," not as a miss, and do not count it toward the stall rule.

---

## 6. Worked example: four weeks alternating 3-day and 6-day weeks

Starting tracks (top-set loads for 4 reps at RPE 8, or the row and pull-up track loads): squat 120 kg, bench 85 kg, deadlift 150 kg, overhead press 55 kg, barbell row 70 kg (4 x 6-8), pull-up bodyweight + 10 kg (4 x 5-8). V loads are 90% of the lift's **current** track load (the load the next H will attempt), rounded to the nearest weight you can load (2.5 kg steps for squat and deadlift, 0.5 kg steps for bench and press with fractional plates). Week 3 is a planned 3-day week in which illness takes Wednesday and Friday, to show the pointer and the gap rule at work.

| Day | Week type | Session | Pointer after | Squat | Bench | Deadlift | Press | Row | Pull-up |
|---|---|---|---|---|---|---|---|---|---|
| W1 Mon | 3-day | Full A | L2 | H: 120 x 4 @8 -> track 122.5 | H: 85 x 4 @8 -> track 86 | | | H: 70 x 8, 8, 7 -> hold | |
| W1 Wed | 3-day | Full B | L3 | | | H: 150 x 4 @8.5 -> hold 150 | H: 55 x 4 @8 -> track 56 | | H: +10 x 7, 6, 5 -> hold |
| W1 Fri | 3-day | Full C | L1 | V: 3 x 6 @ 110 (90% of 122.5) | V: 3 x 6 @ 77.5 | V: 2 x 4 @ 135 | V: 2 x 5 @ 50.5 | V: 3 x 8-10 @ 62.5 | V: 2 x 6-8 @ +5 |
| W2 Mon | 6-day | L1 | U1 | H: 122.5 x 4 @8 -> track 125 | | | | | |
| W2 Tue | 6-day | U1 | L2 | | H: 86 x 4 @7.5 -> track 87 | | | H: 70 x 8, 8, 8, 8 -> track 72.5 | |
| W2 Wed | 6-day | L2 | U2 | | | H: 150 x 4 @8 -> track 152.5 | | | |
| W2 Thu | 6-day | U2 | L3 | | | | H: 56 x 4 @9 -> hold 56 | | H: +10 x 8, 7, 6, 6 -> hold |
| W2 Fri | 6-day | L3 | U3 | V: 4 x 6 @ 112.5 | | V: 3 x 4 @ 137.5 | | | |
| W2 Sat | 6-day | U3 | L1 | | V: 4 x 6 @ 78.5 | | V: 3 x 5 @ 50.5 | V: 3 x 8-10 @ 65 | V: 3 x 6-8 @ +5 |
| W3 Mon | 3-day (planned) | Full A | L2 | H: 125 x 4 @8 -> track 127.5 | H: 87 x 4 @8.5 -> hold 87 | | | H: 72.5 x 8, 7, 7 -> hold | |
| W3 Wed | **missed** (ill) | - | L2 | | | | | | |
| W3 Fri | **missed** (ill) | - | **L2** (pass incomplete) | | | | | | |
| W4 Mon | 6-day | **L2** (owed) | U2 | | | H: **held at 150** (10 days since the W2 Fri V exposure; rule 8-14 days). 150 x 4 @7.5 -> track 152.5 | | | |
| W4 Tue | 6-day | U2 | L3 | | | | H: **held at 56** (10 days since W2 Sat). 56 x 4 @8 -> track 57 | | H: **held** (10 days). +10 x 8, 8, 7, 6 -> hold |
| W4 Wed | 6-day | L3 | U3 | V: 4 x 6 @ 115 (9 days since W3 Mon: a V is done as written and resets the clock) | | V: 3 x 4 @ 137.5 | | | |
| W4 Thu | 6-day | U3 | L1 | | V: 4 x 6 @ 78.5 (10 days: done as written, clock reset) | | V: 3 x 5 @ 51.5 | V: 3 x 8-10 @ 65 | V: 3 x 6-8 @ +5 |
| W4 Fri | 6-day | L1 | U1 | H: 127.5 x 4 @8 -> track 130 (2 days since the V: normal rule) | | | | | |
| W4 Sat | 6-day | U1 | **L2** | | H: 87 x 4 @8 -> track 88 | | | H: 72.5 x 8, 8, 8, 8 -> track 75 | |

What the example shows:

- **Loads advance at the same pace in both week types.** Squat top set: 120, 122.5, 125, 127.5, with 130 planned, one step per H exposure, whether the exposure sat inside a 3-day Full A or a 6-day L1. Bench: 85, 86, 87, 87 (held on an RPE 8.5), 88 planned. The day count never entered the arithmetic.
- **Both exposures per lift happened in every complete week** (one H, one V) in weeks 1, 2 and 4. Week 3 gave squat, bench and row their H exposure and nothing else; the pass stopped at L2.
- **The pointer did the scheduling in week 4.** Week 4 started at L2, the half-session owed from week 3, and ran L2, U2, L3, U3, L1, U1: six half-sessions, one complete pass, shifted by two. Week 5 starts at L2 again; as a 3-day week it would be Full B, Full C, Full A. Nothing was skipped and nothing was done twice.
- **The gap modifier fired three times** on the first two days of week 4: deadlift, press and pull-up had their last exposures (the V sets of W2 Fri and Sat) ten days earlier, so each held its load instead of taking the planned step. All three came in at RPE 8 or lower, so their increments resume at the next H. That one held step is the entire cost of the lost week for those lifts.
- **Squat, bench and row were trained in week 3**, so their next exposures (the W4 Wed and Thu V sets) fell 9-10 days after the last one. A V exposure is done as written (it is already at 90%) and resets the clock, so the H exposures on Friday and Saturday ran the normal rule and took their steps.
- **V loads follow the track, not the last top set.** The W2 Fri squat V used 112.5 (90% of the 125 the track planned) even though the last top set performed was 122.5.
- **Row progression is double progression:** 70 kg held until all four sets reached 8 in W2, moved to 72.5, held in the 3-set merged session (7, 7 on the last two sets), moved again in W4.

---

## 7. Where cardio goes

Spine item 8: 2-3 sessions per week toward 150 min moderate; lift before cardio in the same session or separate by 3 or more hours; prefer cycling or incline walking to running on heavy leg weeks. Evidence and doses: `guide/06-recovery-nutrition-cardio.md`, section 5.

| Week type | Placement |
|---|---|
| 3-day | Four non-lifting days exist. Put cardio there, about 24 h away from Full A and Full B. This is the week to accumulate most of the weekly minutes. |
| 4-day | Non-lifting days first; otherwise after U2 (the one pure upper day). |
| 5-day | After U1 or U2 (upper-body days), 20-30 min, cycling or incline walking; or on the two rest days. Never before a lower session; keep 3+ h from L1, L2 and Full C. |
| 6-day | After U1, U2 or U3 only (these are the upper-body days), 20-30 min each. Cut to the health floor (about 75 min vigorous or 150 min moderate) if recovery markers slip. |

---

## 8. Checklist

- One rotation: L1, U1, L2, U2, L3, U3. Blocks A, B, C. Merged blocks are Full A, Full B, Full C.
- Merges this week = 6 minus days. Merge C, then A, then B.
- Every 3- to 6-day week is one pass: every main lift twice, one heavy and one volume exposure; tracks advance once per week.
- Pointer rules: split +1, merged +2, never skip ahead, finish what is owed.
- Cut from the bottom of the priority stack; never cut a top set.
- Gap clock per lift: hold the load at 8-21 days; reduce 5-10% beyond 21.
- A short week is not a deload unless it is the scheduled week, two red flags persist, or you are ill. A deload keeps frequency, halves sets, and runs top sets at RPE 6-7.
- Block clock counts passes; for 3- to 6-day weeks that is calendar weeks.

---

## Sources

Research notes (the only evidence base used):

- `research/frequency-volume-intensity-evidence.md`: Q1 (frequency with volume equated: Schoenfeld, Grgic & Krieger 2019; Pelland et al. 2025/26; Hamarsland et al. 2022; Colquhoun et al. 2018; Johnsen & van den Tillaar 2021; Grgic et al. 2018; Ralston et al. 2018), Q2 (weekly volume and per-session ceiling: Schoenfeld 2017; Baz-Valle 2022; Remmert et al. 2025 preprint, secondary figures; Krieger 2009-2010), Q6 (maintenance: Bickel, Cross & Bamman 2011; Spiering et al. 2021; Androulakis-Korakakis 2020/2021), Q7 (3 vs 6 sessions; Räntilä & Ahtiainen 2026).
- `research/flexible-frequency-programming.md`: KQ1 (rotation pattern: RP floating split, GZCLP, A/B programs, forum consensus on missed days), KQ2 (5/3/1 cycle stretching; GZCL tier priority inference), KQ3 (maintenance and detraining timelines, per-session ceiling conflict), KQ4 (RPE-anchored top sets, RPE stops, readiness gate; Barbell Medicine forum), KQ5 (merge and cut rules, skipped-session rule), KQ6 (exposure-indexed progression and the days-since-exposure modifier, flagged as inference), KQ7 (no published 3-to-6-day program), consolidated rule table.
- `research/periodization-and-progression.md`: Q2 (RPE vs percentage: Helms 2018; Hickmott 2022; double progression), Q3 (deloads: Coleman et al. 2024; Bell et al. 2022; Bell et al. 2023 Delphi), Q4 (mesocycle counting), Q7 (logging and e1RM trend).
- `research/recovery-nutrition-cardio.md`: KQ1 (24-72 h recovery; consecutive days), KQ2 (readiness red flags; functional overreaching resolves in about a week), KQ5 (cardio placement: Schumann et al. 2022; Murlasits et al. 2018; Wilson et al. 2012; WHO 2020).
- `research/exercise-selection-and-session-design.md`: KQ1 (undertrained muscles), KQ3 (exercise order: Nunes et al. 2021), KQ6 (session time budget and supersets: Weakley et al. 2024/25).
- `research/splits-and-named-programs.md`: KQ1 (full-body and upper/lower frequency and session lengths), KQ7 (programs whose unit is a workout in a rotation).

Key primary citations: Schoenfeld, Grgic & Krieger 2019 (J Sports Sci 37:1286); Pelland et al. 2025/26 (Sports Med, DOI 10.1007/s40279-025-02344-w; [SportRxiv 460](https://sportrxiv.org/index.php/server/preprint/view/460)); Hamarsland et al. 2022 (Front Physiol, [PMC8766679](https://pmc.ncbi.nlm.nih.gov/articles/PMC8766679)); Colquhoun et al. 2018 (JSCR); Johnsen & van den Tillaar 2021 ([PeerJ 10781](https://peerj.com/articles/10781)); Grgic et al. 2018 (Sports Med 48:1207); Ralston et al. 2018 (Sports Med Open 4:36); Remmert et al. 2025 ([SportRxiv 537](https://sportrxiv.org/index.php/server/preprint/view/537), figures via Biolayne REPS 36, secondary); Bickel, Cross & Bamman 2011 (MSSE, [PubMed 21131862](https://pubmed.ncbi.nlm.nih.gov/21131862/)); Spiering et al. 2021 (JSCR 35:1449, [PubMed 33629972](https://pubmed.ncbi.nlm.nih.gov/33629972/)); Androulakis-Korakakis et al. 2021 ([Frontiers](https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2021.713655/epub)); Räntilä & Ahtiainen 2026 ([JYX](https://jyx.jyu.fi/handle/123456789/112971)); Coleman et al. 2024 ([PeerJ 16777](https://peerj.com/articles/16777)); Bell et al. 2023 (Sports Med Open 9:87, [PMC10511399](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10511399/)); Helms et al. 2018 ([PMC5877330](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5877330/)); Schumann et al. 2022 (Sports Med 52:601); Murlasits, Kneffel & Thalib 2018 (J Sports Sci 36:1212); Nunes et al. 2021 (Eur J Sport Sci 21:149); Weakley et al. 2024/25 ([PMC12011898](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12011898/)). Practitioner sources: RP Strength, [Dr. Mike's floating split](https://rpstrength.com/blogs/video-guides/dr-mikes-exact-training-split-to-get-to-6-body-fat); Muscle & Strength, [5/3/1 on 3 days](https://www.muscleandstrength.com/node/4458); thefitness.wiki, [GZCLP](https://thefitness.wiki/routines/gzclp/); Barbell Medicine forum, [using RPE or adjusting the schedule](https://forum.barbellmedicine.com/t/using-rpe-or-adjusting-the-training-schedule/19074); Jeff Nippard, [training after a break](https://jeffnippard.com/blogs/news/how-to-get-your-gains-back-after-a-training-break).

Flags carried from the notes: Remmert per-session thresholds (11 fractional / 2 direct sets) are secondary and unverified; detraining percentages (3-7% after one week, 6-9% after four) are from secondary summaries; the gap-modifier table and the merge rules are inferences; no study has tested oscillating 3/6-day weeks or merged versus separate sessions.
