# Progression tracks for the main lifts

Last updated: 2026-11-10 (section 9: busy-gym substitutes; a missed top set moves to the V exposure; row and pulldown variants count; a substitute caps the gap modifier at a hold). Earlier: 2026-11-06 (effective RPE and reps above the target, unrated top sets, re-anchor, regain phase, deadlift caution, calibration rep-out: sections 3, 5, 5.1-5.3, 8, 10). Earlier: 2026-10-21 (units switched to pounds the same day)

This file holds the exact progression rules for the six main lifts (squat, bench press, deadlift, overhead press, barbell row, pull-up or pulldown) and the accessory rule the templates use. `guide/04-periodization-and-progression.md` explains the options and the evidence; this file states the one scheme this program runs. `guide/03-flexible-scheduling.md` says when each exposure happens.

Design: each lift has **one track**. The track's state is a top-set load (row and pull-up: a track load), a rep target, a miss counter, the date of its last exposure, and an e1RM history. The track updates at the lift's **heavy (H) exposure** and is read by its **volume (V) exposure**. Day count never touches the track: every 3- to 6-day week contains exactly one H and one V exposure per lift.

Units: pounds. The smallest plate is 2.5 lb, so every barbell load is a multiple of 5 lb. Increments: 5 lb for squat and deadlift; 5 lb after every second successful exposure for bench and press (no fractional plates). Earlier versions of this file ran in kilograms (2.5 kg squat and deadlift, 1 kg bench and press); the pound rules keep the same weekly pace.

---

## 1. The six tracks at a glance

| Lift | H exposure (slot) | V exposure (slot) | H structure, split session | H structure, merged session | V structure, split / merged | Increment after a successful H |
|---|---|---|---|---|---|---|
| Squat | L1 | L3 | 1 x 4 top set @ RPE 8, then 3 x 4 at -7% | top set, then 2 x 4 at -7% | 4 x 6 / 3 x 6 at 90% of the top-set load | +5 lb |
| Bench press | U1 | U3 | 1 x 4 @ 8, then 3 x 4 at -7% | top set, then 2 x 4 | 4 x 6 / 3 x 6 at 90% | +5 lb every second success |
| Deadlift | L2 | L3 | 1 x 4 @ 8, then 2 x 4 at -7% | top set, then 2 x 4 | 3 x 4 / 2 x 4 at 90% | +5 lb |
| Overhead press | U2 | U3 | 1 x 4 @ 8, then 3 x 4 at -7% | top set, then 2 x 4 | 3 x 5 / 2 x 5 at 90% | +5 lb every second success |
| Barbell row | U1 | U3 | 4 x 6-8 @ RPE 8 (double progression) | 3 x 6-8 | 3 x 8-10 / 3 x 8-10 at 90% of the track load | +5 lb when every set reaches 8 |
| Pull-up or pulldown | U2 | U3 | 4 x 5-8 @ RPE 8 (double progression) | 3 x 5-8 | 3 x 6-8 / 2 x 6-8 with load reduced to RPE 7 | +5 lb (one pin, or added load) when every set reaches 8 |

RPE scale: RPE 10 = 0 reps in reserve, 9 = 1, 8 = 2, 7 = 3 (Zourdos, Helms et al. 2016; `research/frequency-volume-intensity-evidence.md`, Q4). Estimates are reliable within about one rep when you are 0-3 reps from failure: trained lifters missed by 0.65 reps on average at 1 and 3 RIR on the bench (Refalo et al. 2024), and a meta-analysis found people underpredict reps to failure by about 0.95 reps, more accurately close to failure and in later sets (Halperin et al. 2022). That is why the top set is anchored at RPE 8 and not 6 or 7. The squat is rated less accurately than the bench (Helms et al. 2017; Hermann et al. 2025). Because the typical error is underprediction, a logged "RPE 8" top set is more often a true RPE 7 than a 9, which makes the increment rule conservative, not aggressive. Three further points (`research/effort-ratings-and-progression-without-rpe.md`, KQ1): the direction flips at a true max (a 1RM is rated 9.35-9.86; Ormsbee 2019; Helms 2017); long sets are rated much worse (2.05 reps of error at a called RPE 9 on 16-rep squat sets; Zourdos 2021); and training status did not change accuracy in the meta-analysis (Halperin 2022). Accuracy is best on heavy, low-rep sets near failure, which is why only the top set is rated (section 10). The rating error (about 0.5-1 rep) is larger than the 0.5-RPE bins in section 5, so the half steps carry little real information.

Why 4 reps at RPE 8: the spine's strength window is 3-6 reps at about 75-90% 1RM with 1-2 reps in reserve. A 4-rep set with 2 in reserve is a 6-rep max effort: 83.7% 1RM on Tuchscherer's RPE chart (Reactive Training Manual, as reproduced; the original chart image was not read), which matches the ~83% Epley estimate. Tuchscherer calls the chart a rough guide, "not to attempt to derive a max", and his original RPE 8 meant "2-4 reps left"; the strict 1 RPE = 1 RIR mapping is Zourdos et al. 2016. Convention, not evidence (`research/periodization-and-progression.md`, addendum 2026-10-21).

Why -7% for back-offs: the research note's RPE-anchored design puts back-offs at 5-8% below the top set (`research/flexible-frequency-programming.md`, KQ4 inference); Reactive Training Systems calls a 5% fatigue drop "fairly average" (`research/periodization-and-progression.md`, Q2, convention). The back-offs land at about RPE 7 and drift toward 8 as fatigue builds. Stop back-offs early if a set reaches RPE 9 (RPE stop; a 12-powerlifter thesis found volume "can be effectively autoregulated using RPE stops," KQ4; still unverified at the primary source, which sits behind a reCAPTCHA).

Why 90% for V sets: 90% of the 4 @ 8 load is 90% x 83.7% = about 75% 1RM. By Tuchscherer's chart, a single set of 6 at 75% is about RPE 6.5-7 for squat and bench, rising somewhat over the later sets as fatigue builds (hard, not grinding); a set of 4 for the deadlift is at or below RPE 6, and a set of 5 for the press about RPE 6 (practice and volume, low fatigue cost). These are lighter than the RPE 7-8 and 6-7 first assumed; the 90% rule itself is unchanged. The V exposure exists because strength rises with frequency, with diminishing returns (Pelland et al. 2026, Sports Med), and the chapter 01 rule wants every main lift twice a week.

---

## 2. Starting loads

Pick one method per lift, in this order of preference. Start low; the first two exposures correct an undershoot, and an overshoot costs a wasted week (Barbell Medicine coaching reply: a single session "has little impact on your trajectory," `research/flexible-frequency-programming.md`, KQ4).

| You have | Top-set starting load (4 reps @ RPE 8) | Notes |
|---|---|---|
| A true 5RM from the last 8 weeks | **95% of the 5RM** | A 4 @ 8 is a 6RM effort: 83.7% vs 86.3% 1RM for a 5RM on Tuchscherer's chart, so about 0.97 x 5RM. 95% is about 2.5% conservative, on purpose. Rounded down. |
| A 1RM from the last 8 weeks | **80% of the 1RM** | Deliberately about 4% under the chart's 83.7% (and the ~83% Epley estimate). |
| Neither | **Work up on the first H exposure**: after the warm-up ramp, add 5-10% per set until 4 reps feel like RPE 8. Log that load as the track load. | Expect to add another step at exposure two. |
| Coming back after > 4 weeks off | 85-90% of the last logged top-set load, first exposure at RPE 6-7 | Section 8. |

Row: the load for 4 x 6-8 at RPE 8 on the first set (about what you could row for 9-10 once). Pull-up: added load for 4 x 5-8 at RPE 8; if you cannot do 5 clean bodyweight pull-ups, use the lat pulldown with the same rule and switch to the bar when a pulldown set at about bodyweight reaches 8 reps.

For comparison, not for copying: 5/3/1 starts from a training max of 85-90% of 1RM and its heaviest week tops out at 95% of that; GZCLP restarts a stalled lift at about 85% of a fresh 5RM (author-partnered page); Greyskull starts at a weight you can lift 8-10 times (unverified) (`research/periodization-and-progression.md`, Q2; `research/splits-and-named-programs.md`, KQ2-KQ3). All three start lighter than the lifter wants to. So does this program.

---

## 3. The H exposure, step by step

1. **General warm-up** (3-5 min easy movement, optional in a warm gym) and dynamic mobility for the day's patterns. Static holds, if any, under 30 s per muscle (`research/exercise-selection-and-session-design.md`, KQ5).
2. **Ramp on the first compound only:** empty bar x 5; 80% of the top set x 2-3; then the top set. Once the top set is 225 lb or more, add 60% x 3 between the bar and the 80% set; that step is coaching convention, not evidence. Round to the plate, never below the bar. Later main lifts in the same session need one feeder set at 60-70% (in 40 trained men, one warm-up set of 6 at 80% of the training load gave faster squat bar speed than one at 40%, and in the bench the two-set 40%/80% warm-up did best; few reps at low loads were not enough. Ribeiro et al. 2020, KQ5 and its 2026-10-21 addenda).
3. **Top set:** 4 reps at the planned load. If rep 4 was clearly easy, keep going, 6 reps at most, and stop at the first slow rep; log the reps you did. Rate it immediately with one tap: **7** easy (3 left), **8** on target (2 left), **9** hard (1 left), **10** nothing left. Only the top set needs a rating. In Hevy, the RPE field on the set; if it is hidden, turn on RPE tracking in the app's workout settings. Hevy pre-fills the planned 4 reps: change the number whenever you did more or fewer, above all when you missed a rep. An unedited 4 reads as a success. Rest 3-4 min (deadlift 3-5 min).
4. **Back-offs:** load x 0.93, rounded to the plate. 3 x 4 in a split session, 2 x 4 in a merged session (deadlift: 2 x 4 in both). Rest 2-3 min. If a back-off set reaches RPE 9, stop the back-offs there.
5. **Log** load, reps, RPE for every set (section 10) and write the next planned top-set load from section 5 before you leave the rack.

In a merged session the second and third main lifts are not fresh. Judge their top sets by RPE, not by whether the planned load was made: a planned 4 @ 8 that comes in at 4 @ 9.5 is logged as "hold," not as a miss, and does not count toward the stall rule (`guide/03-flexible-scheduling.md`, section 5).

---

## 4. The V exposure

- Load = 90% of the lift's **current** top-set load (the load the track says you will attempt at the next H), rounded to the nearest loadable weight. Not 90% of what you did last time if the track has moved since.
- Squat and bench: 4 x 6 (3 x 6 merged). Deadlift: 3 x 4 (2 x 4 merged). Press: 3 x 5 (2 x 5 merged). Row: 3 x 8-10 at 90% of the row track load. Pull-up: 3 x 6-8 (2 x 6-8 merged) with the added load reduced, or bodyweight, so the sets land at RPE 7.
- Rest 2-3 min; no set past RPE 9. If the **last** set of a squat or bench V is RPE 6 or lower two exposures running, the track is stale: take the next increment at the H exposure even if the top set was RPE 8.5. Caveat: by Tuchscherer's chart the first V set is expected near RPE 6.5-7 and the last a little higher after fatigue, so this threshold sits only 0.5-1 RPE under the expected value and is a weaker signal than first assumed. Underprediction (section 1) pushes logged RPEs up, so in practice the rule should fire rarely (inference). Check it against your own logged V sets before relying on it; the threshold is unchanged. When V sets are unrated the rule cannot fire; the calibration rep-out (section 5.3) does its job.
- The V exposure does not change the track load. It counts as an exposure for the gap clock (section 8), and its sets go in the log.

---

## 5. Increment, hold, miss

Decide the next H load from the top set only. Back-off performance never changes the track, except through the calibration rep-out (section 5.3).

**Effective RPE at the rep target** (added 2026-11-06; `research/effort-ratings-and-progression-without-rpe.md` KQ5, inference). The table below reads the effort at rep 4, not at the last rep done:

- **Rated top set:** effective RPE = logged RPE minus the reps done above the target. 4 @ 8 reads 8; 5 @ 8 reads 7; 6 @ 8 reads 6; 5 @ 10 reads 9 (four reps were made at RPE 9, so a hold, not a miss).
- **Unrated top set:** assume the set ended at RPE 9, one rep left, because lifters underpredict by about one rep (Halperin 2022: 0.95 reps), so this under-credits on average. Effective RPE = 9 minus the reps above the target: 5 reps reads 8, 6 reads 7, 7 reads 6. An unrated set of exactly 4 carries no information: treat it as 8, flag it, and count it toward the rep-out trigger (section 5.3). Every unrated decision is flagged in `data/track-log.md` with the assumption used.

| Top set result (effective RPE at rep 4) | Next H top-set load | Miss counter |
|---|---|---|
| 5 or lower (for example 7 @ 8, 6 @ 7, or 8+ unrated reps) | **Re-anchor:** e1RM / 1.2 (section 10), rounded down to 5 lb; at least the big step, at most +10% of the load lifted. Capped further in the regain phase and for the deadlift (sections 5.1, 5.2) | reset to 0 |
| 7 or lower | +10 lb squat and deadlift, +5 lb bench and press at once, clearing the step counter (one-off; if it happens at two consecutive H exposures the start load was too low, keep taking the big step until it stops) | reset to 0 |
| 7.5-8 | **+5 lb squat and deadlift. Bench and press: +5 lb on every second such result; the first holds the load and counts 1 on the step counter** | reset to 0 |
| 8.5-9 | **Hold** the load | unchanged |
| 9.5-10, or 3 reps or fewer | **Hold** the load | +1 |
| Two misses in a row at the same load | **Stall**: section 6 | reset after the reset |

Worked examples from the log: bench 105 x 6 @ 8 on 27 Oct reads 6, the big step to 110, which is what the hand amendment did. Squat 155 x 5 unrated on 5 Nov reads 8, a step, but the 19-day gap (section 8) held it first. Re-anchor: squat 155 x 8 @ 8 gives e1RM 207, / 1.2 = 172, so 170 (+15, inside the +10% cap; the regain-phase cap would make it 165).

The divisor 1.2 is the program's own e1RM value for 4 @ 8 (a 6-rep effort). It and the RPE-9 assumption for unrated sets are conventions, not tested values.

The step counter (`step_counter` in `data/tracks.json`) counts successful bench and press top sets at RPE 7.5-8. Holds and misses leave it as it is; an increment, a big step or a stall reset sets it back to 0.

Expected pace: squat and deadlift about +5 lb per week (the Texas Method's weekly pace, `research/periodization-and-progression.md`, Q2), bench and press about +5 lb per two weeks (the Texas Method's fortnightly 5 lb). A lifter who makes every top set for 12 weeks adds 60 lb to the squat top set; nobody does, which is what the hold and stall rules are for.

Row and pull-up (double progression, `guide/04-periodization-and-progression.md`, section 2.2): fixed load; add reps each H exposure until every set reaches the top of the range (8) at RPE 8 or less; then +5 lb (one pin on the pulldown stack) and back to the bottom of the range (6 for the row, 5 for the pull-up). A merged session runs 3 sets instead of 4; the rule still applies to the sets done. If the first set cannot reach the bottom of the range, hold the load and count a miss; two misses, drop 5% and rebuild.

### 5.1 Regain phase (a lift coming back from a long layoff)

Added 2026-11-06. Source: `research/retraining-after-layoff.md` (KQ1-KQ5; the rule itself is inference). Strength came back to the old peak in about 5-8 weeks in every retraining study found, after breaks of 3-32 weeks (Staron 1991, older; Taaffe 1997, older; Blocquiaux 2020; Seaborne 2018). Size is lost faster than strength and retained skill is the best-supported reason (Räntilä/Halonen 2025). Tendon stiffness lags: it rose only after 2-3 months of training and responds only to loads above about 70% of maximum (Kubo 2010, 2012, older; Bohm 2015). Coaches differ on the climb: +10 lb a week (Renaissance Periodization), ride out +5 (Wendler), novice-style 5-10 lb a week after a year or more off (Stronger By Science).

**Who is in it.** A main lift that came back after more than 8 weeks off with its latest e1RM below 90% of its pre-layoff best. `data/tracks.json` holds the threshold per lift (`regain`). On 6 Nov 2026 that is the **squat** (e1RM 191 of 292 lb, 2024 best 250 x 5; exit at 263, about 220 x 4 @ 8) and the **row** (e1RM 90 of 142 lb, 2024 best 115 x 7; exit at 128, a track load of about 95). Bench (95-100% of 2024), press (about 90%) and deadlift (88%, and its 2024 sets were never pushed) run the normal rules.

| Item | During the regain phase |
|---|---|
| Top set | As section 3: 4 reps, up to 6 if rep 4 is clearly easy |
| Steps | Section 5 as written, with the effective RPE: +10 lb when the top set reads 7 or lower (5 @ 8, 6 @ 8, 4 @ 7, or 6 unrated reps); +5 lb at 4 @ 8 or an unrated 4 or 5 |
| Cap | **+10 lb per H exposure** on the squat, however easy the set (re-anchor included). At +10 a week the squat reaches the exit line in about 6-7 qualifying exposures, inside the 5-8-week retraining window |
| Bench and press (if in the phase) | +5 lb on every success, no second-success wait |
| Row | +10 lb (two pins) when every set reaches 8 at a logged RPE 7 or lower, or the first set reaches 11 or more reps; otherwise section 5 as written |
| Gaps | A gap of 8-14 days does not block the step (section 8). 15 days or more: section 8 as written |
| Back-offs and V | Unchanged: -7% and 90% of the new track load. No sets added or removed |

**Exit**, whichever comes first; the lift then runs section 5 unchanged:
1. The top-set e1RM reaches the threshold in `data/tracks.json` (squat 263, row 128).
2. The first top set reading 8.5 or higher at the planned load, or the first miss. A later lift in a merged session does not end the phase this way, because it is not fresh.
3. 9 January 2027, 12 weeks after the restart on 17 October 2026.

**Week types.** Step sizes do not change with the day count: every 3- to 6-day week has one H per lift. In merged sessions (3-day weeks) only the first heavy lift is fresh, so the later lifts are less likely to earn a big step; nothing else changes. After two or more 2-day weeks, H exposures land every 7-14 days, which is why the 8-14-day gap waiver matters. Coaching judgment, not engine rule: in the first week back at 5-6 days after two or more 2-day weeks, take normal steps only.

**Where this differs from the research note.** The note asked for a logged RPE before any regain-phase big step. This program also accepts 6 unrated reps (section 5, unrated rule), because the reps are observed and the RPE-9 assumption under-credits on average; the +10 lb cap limits the cost of a wrong call. The deadlift keeps the stricter form (5.2).

### 5.2 Deadlift caution until 9 January 2027

Source: `research/retraining-after-layoff.md` KQ3-KQ5 (inference). The posterior chain had about 18 months without heavy loading, the deadlift carries the heaviest loads in the program, and its 2024 benchmark is soft (sets of 6-8 that were never pushed), so it behaves more like a novice lift than a regain lift.

- The +10 lb big step needs a **logged** RPE (effective 7 or lower) and is **never taken at two H exposures in a row**. Otherwise the step is +5. A re-anchor is capped at +10.
- Work-up sets and V sets never count as evidence for a step.
- Any low-back pain during or after the deadlift: hold the load. If it persists past a few days, see a physical therapist or physician (`guide/06-recovery-nutrition-cardio.md` section 8). This is general training guidance, not medical advice.

### 5.3 Calibration rep-out

Source: `research/effort-ratings-and-progression-without-rpe.md` KQ2, KQ5 (inference; the reading bands rest on Tuchscherer's chart and RTS's 5% fatigue figure, both conventions). Repeated sets close to failure cut rating error by 0.4-2.3 reps over 6 sessions in one study and changed nothing in another (Wiedenmann 2026; Remmert 2023), so this is a check, not a training method.

- **When:** after two unrated H exposures in a row at exactly 4 reps on a lift, the next H exposure of that lift gets a rep-out (`rep_out_due` in `data/tracks.json`; the routine note says so). Once ratings are logged, one rep-out per lift per block is enough (for example the week before the deload). At most 2 per session. In a merged session, only on the first main lift; postpone a later lift's rep-out to the next session where it comes first. Skip in a deload, on the first exposure after a gap of 22 days or more, on any lift with joint pain, and in race weeks.
- **Which set:** the **last back-off** (top-set load x 0.93), never the top set. Keep going after rep 4 until one more rep would be a grind (about RPE 9), 10 reps at most. Squat and bench inside the rack with the safeties set; deadlift: stop at the first rep where back position or bar path changes. Log the reps.
- **What to expect:** after a true 4 @ 8 top set, about 5-7 reps (expected about 5.7). Each point of top-set RPE moves it by about one rep. The first two rep-outs on each lift become that lift's own baseline.

| Rep-out reps | Read the top set as | Decision for an unrated top set |
|---|---|---|
| 3 or fewer | RPE 9 or harder, or high fatigue | Hold (not a miss) |
| 5-7 | About RPE 8 | Normal rule |
| 8 or more | RPE 7 or easier | Big step (subject to the caps in 5.1 and 5.2) |

A back-off of exactly 4 when a rep-out was due is read as "not done" and the rep-out stays due. For a rated top set, both are logged; if the rep-out and the rating disagree by 2 or more reps, the track log says which way the ratings drift.

Row, pull-up and accessories already progress on reps. Unrated sets there are treated as meeting the RPE condition; a grind shows up as missed reps next time.

---

## 6. Stall and reset

A stall is two consecutive misses at the same top-set load (or, for row and pull-up, two consecutive exposures where the first set fails to reach the bottom of the range).

1. **First stall on a lift:** before resetting, check the three recovery inputs for the previous two weeks: sleep, calories and bodyweight trend (`guide/04-periodization-and-progression.md`, section 5). If one is obviously off, fix it and hold the load one more exposure. Otherwise **reset the top-set load by 7.5%** (round down) and rebuild at the normal increment. You pass the stall load again in 3-4 weeks (squat, deadlift) or 5-6 weeks (bench, press), with more volume behind you. Range of reset sizes in the sources: Starting Strength 5-10%, StrongLifts 10%, Stronger By Science 10-15%, 5/3/1 training max to 90% (`research/periodization-and-progression.md`, Q2, Q5; all conventions).
2. **Second stall on the same lift within 12 weeks:** reset 7.5% again **and change the rep zone** for one block: top set 1 x 6 @ RPE 8 with back-offs 3 x 6 at -7% (2 x 6 merged); the V exposure keeps 4 x 6 at 90% and will feel easy, which is intended. Return to 4s at the next block. Changing the relative-intensity zone is the best-supported plateau move after a load reset (`guide/04-periodization-and-progression.md`, section 5).
3. **Third stall, or no e1RM progress across a full block plus deload:** reduce the H exposure to the top set plus one back-off for a block (the Texas Method fix of cutting volume on the heaviest day when the top set stalls), or change the variant for a block at a block boundary only (pause squat, close-grip bench, deficit deadlift, seated press). Only after that, change the scheme (for example, a percentage wave off a training max in the 5/3/1 style, described in chapter 04). Program-hopping before the stall rule has fired is the error, not the stall.

Resets never touch the other lifts. A squat stall does not change the deadlift track.

Optional block-level variation for lifters who want it even without a stall: alternate 4s and 6s block to block. Periodized loading beats non-periodized loading for 1RM by a small margin (Moesgaard 2022, ES 0.31, volume-equated; Williams 2017, ES 0.43, 0.23 without outliers). Undulating beats linear for strength in trained lifters (Moesgaard 2022, ES 0.61, CI lower bound 0.00; untrained ES 0.06), and neither periodization nor its style changes hypertrophy. The weekly H (4s at RPE 8) and V (6s at 90%) pair is already a daily-undulating structure, which this evidence supports; alternating 4s and 6s by block stays optional.

---

## 7. Deload

Every 4-6 passes (for 3- to 6-day weeks, every 4-6 calendar weeks), or sooner on two or more readiness red flags for a week (`guide/03-flexible-scheduling.md`, section 4.5), run one deload pass:

- **Top sets at RPE 6-7:** the current track load x 0.90-0.92, same 4 reps. The track does not advance; after the deload the next H attempts the pre-deload planned load.
- **One back-off set** per H exposure. **V exposures 2 sets.** Row and pull-up 2 sets at the track load.
- **Accessories 1-2 sets**, isolation light.
- **Keep every session and every main lift.** A full week off mid-block probably cost lower-body strength gains in the one RCT on trained lifters (Coleman et al. 2024; posterior probability 0.85 for squat 1RM, 0.92 for isometric strength). A reduced-volume, reduced-frequency deload (once a week, 2 sets) did not hinder muscle thickness or 10RM in untrained men (Pancar et al. 2026). Coaches keep frequency and cut volume and effort (Bell et al. 2023 Delphi), and surveyed athletes deload for about 6.4 days every 5.6 weeks with frequency kept, which supports "every 4-6 passes" (Rogerson et al. 2024). All: `research/periodization-and-progression.md`, Q3 and addendum 2026-10-21.
- **The set cuts above (roughly halving the sets) are convention** (Renaissance Periodization style), not a tested dose: S&C coaches most often cut volume by 0-25% (De Marco et al. 2024, a different population), and no trial compares deload sizes.

Do not run two deloads within four weeks. A 3-day week is not a deload unless you declare it one.

---

## 8. Gap modifiers (days since the lift was last trained)

Each lift's clock counts days since its last exposure of either type. Apply at the next H exposure; the V exposure then reads 90% of the resulting load.

| Days since last exposure | Top-set load | Back-offs |
|---|---|---|
| 0-7 | Normal rule (section 5) | Normal |
| 8-14 | **Hold** the last load; take the increment next time if this one comes in at RPE 7.5 or lower | Normal |
| 15-21 | **Hold**; one fewer back-off set | One fewer |
| 22-28 | **Reduce 5%**; first exposure capped at RPE 7; normal rules from the second exposure | Normal count |
| > 28 | **Reduce 10%**; first exposure RPE 6-7, second RPE 7-8, then normal | Normal count |

Apply the table at an H exposure. If a V exposure is the first thing a lift does after a gap of 8 or more days, do it as written (it is already at 90% of the track load); it resets the clock and the H that follows runs the normal rule. **Regain phase (5.1):** for a lift in the regain phase, the 8-14-day row does not apply; take the planned load.

This table is an inference from peer-reviewed detraining studies, mostly older, of complete cessation. Two weeks without training gave no significant 1RM loss in trained lifters (Hortobágyi et al. 1993, bench -1.7%, squat -0.9%; Hwang et al. 2017, leg press); strength holds for up to about 3 weeks and decays faster after that (McMaster et al. 2013, elite rugby and football players); 4 weeks of cessation cut maximal strength 6-9% (Izquierdo et al. 2007). A 1-week break can still blunt strength gains relative to continuous training (Coleman et al. 2024). These studies stopped all training; one lift going 8-21 days unexposed while the rest of the program continues is milder, so the 8-21-day hold is a conservative convention (an RPE check on a stale skill), not a response to a measured loss. The > 28-day row adapts Nippard's comeback guidance (compounds at RPE 5 or lower, about 50-60% of the old 1RM, in the first weeks after a multi-week or multi-month layoff); its RPE 6-7 first exposure is less conservative than that source. No source quantifies progression adjustments by days since exposure (`research/flexible-frequency-programming.md`, KQ3, KQ6, gaps and addendum 2026-10-21). A pattern-matched substitute logged during the gap caps the modifier at a hold (section 9): the lifter has not stopped training the muscle, but no study tests a substitute alone against barbell detraining, so it earns no increment.

---

## 9. Rounding and equipment

- **Plates.** The smallest plate is 2.5 lb, so every barbell load is a multiple of 5 lb. Squat and deadlift step 5 lb per success; bench and press step 5 lb every second success (section 5).
- **Every computed load is rounded to the nearest 5 lb before it is written down.** That covers back-offs (x 0.93), V sets (x 0.90), warm-up ramps, deloads (x 0.90-0.92), gap reductions (5-10%) and stall resets (7.5%). An exact half-step (for example 112.5) rounds up; stall resets round down. No load goes below the 45-lb bar. Record the loaded weight, not the computed one. No plan, brief or log shows a load that is not a multiple of 5 lb.
- **Dumbbells** come in 2.5 lb steps. Every dumbbell load in this program is the **total of the dumbbells in your hands**, the way the log records it (two 20-lb dumbbells = 40 lb; a one-arm row or a one-dumbbell overhead extension is that dumbbell). A two-dumbbell load is a multiple of 5 lb, a one-dumbbell load a multiple of 2.5 lb (convention set 2026-11-06 to match the lifter's Hevy history). **Machines and cable stacks:** the nearest pin. A plan or brief names one load, never a range.
- **Substitutes for squat, bench, deadlift and press** (travel, equipment, or a station still taken after one reorder; `guide/03-flexible-scheduling.md`, section 4.3, "Station taken") do **not** update the track. Strength is modality- and range-specific (Haugen 2023; Pallares 2020; `research/exercise-selection-and-session-design.md`, KQ7 and addendum 2026-11-10). Each substitute keeps its own load in `data/tracks.json` (`accessories`) and progresses by double progression. Revised 2026-11-10 for a busy gym:
  - **The top set moves.** A heavy slot logged without the barbell lift sets `h_owed` on the track. The lift's next V exposure then runs as the top set plus 2 back-offs at the planned load, judged by RPE (4 @ 9.5 is a hold, not a miss), and the track updates there. `tools/update_tracks.py` reads a V-slot top set within 3% of the planned load as that heavy exposure; plain volume sets do not clear it. The next H slot clears it in any case.
  - **Gap clock (section 8).** A substitute logged after the last barbell exposure caps the gap modifier at a hold: the days count from the substitute, never below 8. No back-off is lost and no reduction applies while substitutes cover the gap; no increment is taken either.
  - Keep the barbell lift itself at least once a week.
- **Row and pull-up variants count** (revised 2026-11-10). Any row in `rotation.json` `substitutes.row` (two-arm or one-arm dumbbell row, chest-supported row, cable row, machine row) or a machine pulldown, logged in the row or pull-up slot when the main exercise is absent, is that exposure. It runs the same double progression on its own load (`data/tracks.json`, `tracks.<lift>.variants`); the regain phase and the e1RM history stay with the main exercise. These two tracks are kept for back size, where the implement does not matter (Haugen 2023; Lehman 2004).
- Dumbbell bench runs at roughly 35-40% of the barbell load per hand (70-80% as a total); treat any substitute as a new baseline and progress it by double progression.

---

## 10. Logging

**Per set:** exercise, load, reps, a note on technique or pain. **One rating per main lift: the top set** (7, 8, 9 or 10, section 3). Ratings on other sets are optional; they never change the track. Example line: `2026-11-03 L1 squat H 275x4 @8 | 255x4, 255x4, 255x4`.

**Per lift (the track state), updated at each H exposure:**

| Field | Example |
|---|---|
| Top-set load (planned for next H) | 280 |
| Rep target | 4 |
| Miss counter | 0 |
| Last exposure date (H or V) | 2026-11-07 (V) |
| e1RM history (last 6 H exposures) | 306, 312, 318, 320, 324, 330 |

**e1RM:** from the top set, `e1RM = load x (1 + (reps + RIR) / 30)`, where RIR = 10 - RPE. Unrated: RIR 2 for a set at the rep target, RIR 1 for a set above it (the section 5 assumption). Example: 275 x 4 @ 8 gives 275 x (1 + 6/30) = 330. This is an Epley-style convention; any consistent formula serves, because the quantity that matters is the trend. Use heavy, low-rep, RPE 8+ sets only; RIR ratings from long sets are less accurate (Russo et al. 2025). Barbell Medicine recomputes e1RM each workout from the most accurate set and sets back-offs from it (`research/periodization-and-progression.md`, Q2, Q7; convention).

**Per session:** bodyweight, sleep hours, a 1-5 readiness score. **Per week:** hard sets per muscle group (half credit for indirect work; tallies at the bottom of each template).

**Judging a block:** average the e1RM of the last three H exposures and compare with the first three. The block worked if e1RM rose at matched RPE, or reps rose at the same load, or RPE fell at the same load. If none of those happened after a full block plus deload, run the stall procedure in section 6 even if no formal stall fired. Single-session changes are mostly noise ("most of what gets called a stall is impatience with the noise floor," Barbell Medicine podcast, convention).

---

## 11. Accessory progression (every exercise that is not a main-lift exposure)

- **Double progression.** Fix the load. Add reps each exposure until every set hits the top of the rep range at RPE 9 or less. Then add the smallest increment (5 lb on a barbell or stack pin; 5 lb total on a two-dumbbell exercise, which is 2.5 lb per dumbbell where the rack allows, otherwise one dumbbell step each; 2.5 lb on a one-dumbbell exercise) and drop to the bottom of the range. The last set of an isolation exercise may go to failure; compounds stay at 1-3 RIR (`guide/01-training-principles.md`, section 5).
- **Starting load:** one you can lift for the bottom of the range with 2-3 reps in reserve.
- **Dynamic variant** for lifters who log set by set: increase load on a specific set only if that set exceeded the range last time (Helms' Muscle and Strength Pyramid description, `research/periodization-and-progression.md`, Q2).
- **Short weeks** skip some sets of an accessory; they never reset its load.
- **Stall:** two exposures without a rep gained at a load, drop one step (5 lb on a barbell, one pin on a stack, 5 lb total on two dumbbells or 2.5 lb on one) and rebuild, or swap to a same-length alternative (seated curl for lying curl, overhead for neutral triceps) at a block boundary. Rotate accessories every 4-8 weeks or when they stall, not session to session (`guide/05-exercise-selection.md`, section 8).
- Triple progression (reps, then sets, then load) is available for accessories you train in every week type, but the extra set is the first thing a short week removes, so it is not the default.

---

## 12. Named-program rules, for orientation only

These are described so you can see where this program's rules come from. They are not reproduced as tables, and the books they come from are paid (`research/splits-and-named-programs.md`, KQ9).

| Program | Rule this program borrows | Rule it does not |
|---|---|---|
| Barbell Medicine templates, Helms RPE work | RPE-anchored top set, back-offs as a percentage of it, e1RM recomputed each session (RPE vs percentage: Helms 2018, +17.05 vs +13.91 kg squat, not significant; Hickmott 2022, SMD 0.21, not significant) | Their specific percentages and set counts |
| 5/3/1 (Wendler) | "Never increase on a miss"; reset to about 90% when progress stops; the cycle stretches with fewer days (5+ weeks at 3 days per week) | Training-max percentage waves; AMRAP top sets |
| Texas Method | One load step per week on squat and deadlift, slower on bench and press; cut volume on the heavy day when the top set stalls | Fixed Monday/Wednesday/Friday roles |
| GZCLP / GZCL | Per-exposure progression | Rep-scheme ladders (5x3, 6x2, 10x1) and the restart after the ladder fails (rest 2-3 days, retest the 5RM, restart at 85% of it; author-partnered page). Not its tier priority either: LeFever calls T1 and T2 "mandatory" and T3 "the most important part" of the pyramid by volume, and when cutting back he trims main-lift volume first and frequency last. This program's cut order (keep the main lift, trim the second, drop accessories) rests on the maintenance evidence (Spiering 2021; Izquierdo 2007), not on GZCL |
| Starting Strength / StrongLifts / Greyskull | Reset size 5-10% on a lift that stalls; the stall is counted in exposures, not weeks | Per-session increments every exposure |
| Reactive Training Systems | Fatigue-percent framing of back-offs (about 5% as the average drop) | Working up to RPE 9-10 |

---

## 13. Flags

- The RPE-to-percentage conversions behind "95% of a 5RM" and "80% of a 1RM" are conventions. Tuchscherer's chart, as reproduced (4 @ 8 = 83.7%, 5RM = 86.3%), puts both about 2.5-4% under the estimate, consistent with "start low"; he calls the chart only a guide (`research/periodization-and-progression.md`, addendum 2026-10-21).
- The -7% back-off and 90% V figures are design choices inside the 5-8% range the research note inferred, not tested values.
- The gap-modifier table is an inference from peer-reviewed detraining studies (mostly older) of complete cessation.
- Two RCTs found adding reps at a fixed load about as good as adding load at fixed reps, for strength and hypertrophy, over 8-10 weeks (Plotkin et al. 2022, trained; Chaves et al. 2024, untrained), which supports double progression for the row, pull-up and accessories. Double vs triple progression is still untested, and no trial tests RPE-stop volume over a block (Hickmott 2022 found none).
- No peer-reviewed validation of the e1RM-trend method as a predictor of long-term progress exists (`research/periodization-and-progression.md`, Q7 gaps).
- The effective-RPE arithmetic, the RPE-9 assumption for unrated sets, the re-anchor divisor and the rep-out bands are untested inferences (`research/effort-ratings-and-progression-without-rpe.md`, KQ5). No trial tests a three-level rating or any method in lifters returning from a layoff. Autoregulated and fixed loading give similar or slightly better strength results (Hickmott 2022, SMD 0.21, not significant; Zhang 2021) and no hypertrophy difference.
- The regain-phase thresholds rest on 2024 e1RMs from unrated sets; the +10 lb squat cap and the deadlift caution are judgments from tendon data, not injury data in lifters (`research/retraining-after-layoff.md`, KQ5 gaps).

---

## Sources

- `research/effort-ratings-and-progression-without-rpe.md` (2026-11-06): KQ1 (rating accuracy: Halperin 2022; Refalo 2024; Hackett 2017; Zourdos 2021; Ormsbee 2019; Helms 2017), KQ2 (calibration: Wiedenmann 2026; Remmert 2023), KQ3-KQ4 (rep-based and autoregulated progression: Mann 2010; Hickmott 2022; Zhang 2021; Nuzzo 2024), KQ5 (effective RPE, unrated rule, re-anchor, rep-out; sections 3, 5, 5.3, 10).
- `research/retraining-after-layoff.md` (2026-11-06): KQ1-KQ2 (Staron 1991; Taaffe 1997; Blocquiaux 2020; Seaborne 2018; Psilander 2019; Räntilä/Halonen 2025), KQ3 (Kubo 2010, 2012; Bohm 2015; Gabbett 2016; Impellizzeri 2020, 2021), KQ4 (practitioner ramps), KQ5 (sections 5.1, 5.2, 8).
- `research/periodization-and-progression.md`: Q2 (linear and double progression rules; 5/3/1 training max and reset; GZCLP ladder and restart; Texas Method pace and stall fix; RPE loading, RTS fatigue percents, Barbell Medicine e1RM; Helms 2018; Hickmott 2022), Q3 (deloads: Coleman 2024; Bell 2022; Bell 2023; Pancar 2026; Rogerson 2024; De Marco 2024), Q5 (plateau order; named stall rules), Q6 (reactive loading), Q7 (logging, e1RM, block criteria; Russo 2025); addendum 2026-10-21 (Tuchscherer chart values; RPE accuracy: Halperin 2022, Refalo 2024, Helms 2017, Hermann 2025; load vs rep progression: Plotkin 2022, Chaves 2024; Moesgaard and Williams re-read).
- `research/flexible-frequency-programming.md`: KQ3 (detraining timelines; addendum 2026-10-21: Hortobágyi 1993, Hwang 2017, Izquierdo 2007, McMaster 2013), KQ4 (RPE-anchored top sets, RPE stops, Barbell Medicine forum reply, Nippard comeback RPE), KQ6 (exposure-indexed progression; days-since-exposure modifier, flagged as inference).
- `research/frequency-volume-intensity-evidence.md`: Q1 (frequency benefit for strength: Pelland et al. 2026), Q4 (RIR-based RPE: Zourdos et al. 2016; proximity to failure: Robinson et al. 2024), Q6 (minimum effective dose: Androulakis-Korakakis 2020/2021).
- `research/exercise-selection-and-session-design.md`: KQ5 (warm-up ramp: Ribeiro et al. 2020; Behm et al. 2016), KQ7 (modality-specific strength: Haugen et al. 2023; Pallares 2020).
- `research/splits-and-named-programs.md`: KQ2, KQ3 (program increments and resets; GZCLP restart per the addendum), KQ9 (copyright status). `research/flexible-frequency-programming.md` addendum 2026-10-21 for LeFever's tier priorities.
- Key primary citations: Helms et al. 2018 (Front Physiol, [PMC5877330](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5877330/)); Hickmott et al. 2022 (Sports Med Open, [PMC8762534](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8762534/)); Zourdos et al. 2016 (JSCR 30:267, [AUT repository](https://openrepository.aut.ac.nz/items/efef3b25-6701-4fb5-bb82-55fcd2a26027/full)); Russo et al. 2025 (Physical Therapy Reviews, doi:10.1080/10833196.2025.2564026, [PDF](https://dspace.uevora.pt/rdpc/bitstream/10174/39438/1/2025%20Russo%20et%20al.%20Factors%20influencing%20the%20accuracy%20of%20the%20repetition%20in%20reserve%20scale%20in%20resistance%20training%20%20a%20systematic%20review.pdf)); Coleman et al. 2024 ([PeerJ 16777](https://peerj.com/articles/16777), [PMC10809978](https://pmc.ncbi.nlm.nih.gov/articles/PMC10809978/)); Bell et al. 2023 (Sports Med Open 9:87, [PMC10511399](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10511399/)); Moesgaard et al. 2022 (Sports Med 52(7):1647-1666, [PubMed 35044672](https://pubmed.ncbi.nlm.nih.gov/35044672/)); Pelland et al. 2026 (Sports Med 56(2):481-505, [doi:10.1007/s40279-025-02344-w](https://doi.org/10.1007/s40279-025-02344-w)); Williams et al. 2017 (Sports Med 47:2083-2100, [PubMed 28497285](https://pubmed.ncbi.nlm.nih.gov/28497285/)); Halperin et al. 2022 (Sports Med 52:377-390, [PubMed 34542869](https://pubmed.ncbi.nlm.nih.gov/34542869/)); Refalo et al. 2024 (JSCR 38(3):e78-e85, [PubMed 37967832](https://pubmed.ncbi.nlm.nih.gov/37967832/)); Helms et al. 2017 (JSCR 31(10):2938-2943, [PubMed 28933716](https://pubmed.ncbi.nlm.nih.gov/28933716/)); Hermann et al. 2025 (MSSE 57(9):2021-2031, [PubMed 40249908](https://pubmed.ncbi.nlm.nih.gov/40249908/)); Plotkin et al. 2022 (PeerJ 10:e14142, [PubMed 36199287](https://pubmed.ncbi.nlm.nih.gov/36199287/)); Chaves et al. 2024 (Int J Sports Med 45(7):504-510, [PubMed 38286426](https://pubmed.ncbi.nlm.nih.gov/38286426/)); Pancar et al. 2026 (Sci Rep 16:10299, [PMC13031491](https://pmc.ncbi.nlm.nih.gov/articles/PMC13031491/)); Rogerson et al. 2024 (Sports Med Open 10:26, [PMC10948666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10948666/)); De Marco et al. 2024 (JSCR 38(12):2099-2106, [PubMed 39446750](https://pubmed.ncbi.nlm.nih.gov/39446750/)); Hortobágyi et al. 1993, older (MSSE 25(8):929-935, [PubMed 8371654](https://pubmed.ncbi.nlm.nih.gov/8371654/)); Hwang et al. 2017 (JSCR 31(4):869-881, [PubMed 28328712](https://pubmed.ncbi.nlm.nih.gov/28328712/)); Izquierdo et al. 2007, older (JSCR 21(3):768-775, [PubMed 17685721](https://pubmed.ncbi.nlm.nih.gov/17685721/)); McMaster et al. 2013, older (Sports Med 43(5):367-384, [PubMed 23529287](https://pubmed.ncbi.nlm.nih.gov/23529287/)); Spiering et al. 2021 ([PubMed 33629972](https://pubmed.ncbi.nlm.nih.gov/33629972/)); Ribeiro et al. 2020 ([PubMed 32971729](https://pubmed.ncbi.nlm.nih.gov/32971729/)); Haugen et al. 2023 ([DOAJ](https://doaj.org/article/a7282dba5e674176bde2a8239832d2f7)). Program-author and coaching sources: Jim Wendler, [5/3/1 for Hardgainers](https://www.jimwendler.com/blogs/jimwendler-com/5-3-1-for-hardgainers); Starting Strength, [The Reset](https://startingstrength.com/article/the-reset-why-and-how) and [Texas Method intensity day](https://startingstrength.com/article/understanding-the-texas-method-intensity-day); thefitness.wiki, [GZCLP](https://thefitness.wiki/routines/gzclp/); Cody LeFever, [The GZCL Method for Powerlifting](https://swoleateveryheight.blogspot.com/2012/11/the-gzcl-method-for-powerlifting.html) (2012, older); Mike Tuchscherer, [RPE chapter](https://elitefts.com/blogs/training/rate-of-perceived-exertion-rpe) (EliteFTS); Stronger By Science, [novice tips](https://www.strongerbyscience.com/making-your-novice-strength-training-routine-more-effective-two-quick-tips/); EliteFTS, [Reactive Training Manual overview](https://elitefts.com/education/a-reactive-training-manual-overview); Barbell Medicine forum, [e1RM in the templates](https://forum.barbellmedicine.com/t/e1rm-calculation-in-the-templates/664) and [using RPE or adjusting the schedule](https://forum.barbellmedicine.com/t/using-rpe-or-adjusting-the-training-schedule/19074); AUT repository, [RPE volume autoregulation thesis](https://openrepository.aut.ac.nz/bitstream/10292/12177/2/RPE%20volume%20autoregulation.pdf); Jeff Nippard, [training after a break](https://jeffnippard.com/blogs/news/how-to-get-your-gains-back-after-a-training-break).
