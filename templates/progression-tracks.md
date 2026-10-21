# Progression tracks for the main lifts

Last updated: 2026-10-21

This file holds the exact progression rules for the six main lifts (squat, bench press, deadlift, overhead press, barbell row, pull-up or pulldown) and the accessory rule the templates use. `guide/04-periodization-and-progression.md` explains the options and the evidence; this file states the one scheme this program runs. `guide/03-flexible-scheduling.md` says when each exposure happens.

Design: each lift has **one track**. The track's state is a top-set load (row and pull-up: a track load), a rep target, a miss counter, the date of its last exposure, and an e1RM history. The track updates at the lift's **heavy (H) exposure** and is read by its **volume (V) exposure**. Day count never touches the track: every 3- to 6-day week contains exactly one H and one V exposure per lift.

Units: kilograms. Increments: 2.5 kg for squat and deadlift; 1 kg for bench and press (0.5 kg plates), or 2.5 kg every second successful exposure without fractional plates.

---

## 1. The six tracks at a glance

| Lift | H exposure (slot) | V exposure (slot) | H structure, split session | H structure, merged session | V structure, split / merged | Increment after a successful H |
|---|---|---|---|---|---|---|
| Squat | L1 | L3 | 1 x 4 top set @ RPE 8, then 3 x 4 at -7% | top set, then 2 x 4 at -7% | 4 x 6 / 3 x 6 at 90% of the top-set load | +2.5 kg |
| Bench press | U1 | U3 | 1 x 4 @ 8, then 3 x 4 at -7% | top set, then 2 x 4 | 4 x 6 / 3 x 6 at 90% | +1 kg |
| Deadlift | L2 | L3 | 1 x 4 @ 8, then 2 x 4 at -7% | top set, then 2 x 4 | 3 x 4 / 2 x 4 at 90% | +2.5 kg |
| Overhead press | U2 | U3 | 1 x 4 @ 8, then 3 x 4 at -7% | top set, then 2 x 4 | 3 x 5 / 2 x 5 at 90% | +1 kg |
| Barbell row | U1 | U3 | 4 x 6-8 @ RPE 8 (double progression) | 3 x 6-8 | 3 x 8-10 / 3 x 8-10 at 90% of the track load | +2.5 kg when every set reaches 8 |
| Pull-up or pulldown | U2 | U3 | 4 x 5-8 @ RPE 8 (double progression) | 3 x 5-8 | 3 x 6-8 / 2 x 6-8 with load reduced to RPE 7 | +2.5 kg added load when every set reaches 8 |

RPE scale: RPE 10 = 0 reps in reserve, 9 = 1, 8 = 2, 7 = 3 (Zourdos, Helms et al. 2016; `research/frequency-volume-intensity-evidence.md`, Q4). Estimates are reliable within about one rep when you are 0-3 reps from failure, which is why the top set is anchored at RPE 8 and not 6 or 7.

Why 4 reps at RPE 8: the spine's strength window is 3-6 reps at about 75-90% 1RM with 1-2 reps in reserve. A 4-rep set with 2 in reserve is a 6-rep max effort, roughly 83% 1RM by the Epley estimate (convention; the RPE-to-percentage tables were not retrievable, `research/periodization-and-progression.md`, Q2 gaps).

Why -7% for back-offs: the research note's RPE-anchored design puts back-offs at 5-8% below the top set (`research/flexible-frequency-programming.md`, KQ4 inference); Reactive Training Systems calls a 5% fatigue drop "fairly average" (`research/periodization-and-progression.md`, Q2, convention). The back-offs land at about RPE 7 and drift toward 8 as fatigue builds. Stop back-offs early if a set reaches RPE 9 (RPE stop; a 12-powerlifter thesis found volume "can be effectively autoregulated using RPE stops," KQ4).

Why 90% for V sets: 90% of a 6RM-equivalent load is about 75% 1RM, which gives 6 reps at roughly RPE 7-8 for squat and bench (hard, not grinding) and 4-5 reps at roughly RPE 6-7 for deadlift and press (practice and volume, low fatigue cost). The V exposure exists because strength shows a small independent frequency benefit (Pelland et al. 2025/26) and the chapter 01 rule wants every main lift twice a week.

---

## 2. Starting loads

Pick one method per lift, in this order of preference. Start low; the first two exposures correct an undershoot, and an overshoot costs a wasted week (Barbell Medicine coaching reply: a single session "has little impact on your trajectory," `research/flexible-frequency-programming.md`, KQ4).

| You have | Top-set starting load (4 reps @ RPE 8) | Notes |
|---|---|---|
| A true 5RM from the last 8 weeks | **95% of the 5RM** | A 4 @ 8 is about a 6RM; 5RM x 0.95-0.97 estimates it. Rounded down. |
| A 1RM from the last 8 weeks | **80% of the 1RM** | Deliberately under the ~83% Epley estimate. |
| Neither | **Work up on the first H exposure**: after the warm-up ramp, add 5-10% per set until 4 reps feel like RPE 8. Log that load as the track load. | Expect to add another step at exposure two. |
| Coming back after > 4 weeks off | 85-90% of the last logged top-set load, first exposure at RPE 6-7 | Section 8. |

Row: the load for 4 x 6-8 at RPE 8 on the first set (about what you could row for 9-10 once). Pull-up: added load for 4 x 5-8 at RPE 8; if you cannot do 5 clean bodyweight pull-ups, use the lat pulldown with the same rule and switch to the bar when a pulldown set at about bodyweight reaches 8 reps.

For comparison, not for copying: 5/3/1 starts from a training max of 85-90% of 1RM and its heaviest week tops out at 95% of that; GZCLP restarts a stalled lift at about 85% of a fresh 5RM; Greyskull starts at a weight you can lift 8-10 times (`research/periodization-and-progression.md`, Q2; `research/splits-and-named-programs.md`, KQ2-KQ3). All three start lighter than the lifter wants to. So does this program.

---

## 3. The H exposure, step by step

1. **General warm-up** (3-5 min easy movement, optional in a warm gym) and dynamic mobility for the day's patterns. Static holds, if any, under 30 s per muscle (`research/exercise-selection-and-session-design.md`, KQ5).
2. **Ramp on the first compound only:** empty bar x 5; 80% of the top set x 2-3; then the top set. Once the top set is 102.5 kg (225 lb) or more, add 60% x 3 between the bar and the 80% set; that step is coaching convention, not evidence. Round to the plate, never below the bar. Later main lifts in the same session need one feeder set at 60-70% (Ribeiro et al. 2020: a two-set 40%/80% warm-up beat six light sets on bench, and an 80% warm-up beat a 40% one on squat; few reps at low loads were not enough. KQ5 and its 2026-10-21 addendum).
3. **Top set:** 4 reps at the planned load. Rate it immediately: RPE 8 means you could have done 2 more. Rest 3-4 min (deadlift 3-5 min).
4. **Back-offs:** load x 0.93, rounded to the plate. 3 x 4 in a split session, 2 x 4 in a merged session (deadlift: 2 x 4 in both). Rest 2-3 min. If a back-off set reaches RPE 9, stop the back-offs there.
5. **Log** load, reps, RPE for every set (section 10) and write the next planned top-set load from section 5 before you leave the rack.

In a merged session the second and third main lifts are not fresh. Judge their top sets by RPE, not by whether the planned load was made: a planned 4 @ 8 that comes in at 4 @ 9.5 is logged as "hold," not as a miss, and does not count toward the stall rule (`guide/03-flexible-scheduling.md`, section 5).

---

## 4. The V exposure

- Load = 90% of the lift's **current** top-set load (the load the track says you will attempt at the next H), rounded to the nearest loadable weight. Not 90% of what you did last time if the track has moved since.
- Squat and bench: 4 x 6 (3 x 6 merged). Deadlift: 3 x 4 (2 x 4 merged). Press: 3 x 5 (2 x 5 merged). Row: 3 x 8-10 at 90% of the row track load. Pull-up: 3 x 6-8 (2 x 6-8 merged) with the added load reduced, or bodyweight, so the sets land at RPE 7.
- Rest 2-3 min; no set past RPE 9. If the **last** set of a squat or bench V is RPE 6 or lower two exposures running, the track is stale: take the next increment at the H exposure even if the top set was RPE 8.5.
- The V exposure does not change the track load. It counts as an exposure for the gap clock (section 8), and its sets go in the log.

---

## 5. Increment, hold, miss

Decide the next H load from the top set only. Back-off performance never changes the track.

| Top set result | Next H top-set load | Miss counter |
|---|---|---|
| 4 reps at RPE 7 or lower | +5 kg squat and deadlift, +2 kg bench and press (one-off; if it happens at two consecutive H exposures the start load was too low, keep taking the big step until it stops) | reset to 0 |
| 4 reps at RPE 7.5-8 | **+2.5 kg squat and deadlift, +1 kg bench and press** | reset to 0 |
| 4 reps at RPE 8.5-9 | **Hold** the load | unchanged |
| 4 reps at RPE 9.5-10, or 3 reps or fewer | **Hold** the load | +1 |
| Two misses in a row at the same load | **Stall**: section 6 | reset after the reset |

Expected pace: squat and deadlift about +2.5 kg per week (about 5 lb; the Texas Method's weekly pace, `research/periodization-and-progression.md`, Q2), bench and press about +1 kg per week (about half the Texas Method's fortnightly 5 lb). A lifter who makes every top set for 12 weeks adds 30 kg to the squat top set; nobody does, which is what the hold and stall rules are for.

Row and pull-up (double progression, `guide/04-periodization-and-progression.md`, section 2.2): fixed load; add reps each H exposure until every set reaches the top of the range (8) at RPE 8 or less; then +2.5 kg and back to the bottom of the range (6 for the row, 5 for the pull-up). A merged session runs 3 sets instead of 4; the rule still applies to the sets done. If the first set cannot reach the bottom of the range, hold the load and count a miss; two misses, drop 5% and rebuild.

---

## 6. Stall and reset

A stall is two consecutive misses at the same top-set load (or, for row and pull-up, two consecutive exposures where the first set fails to reach the bottom of the range).

1. **First stall on a lift:** before resetting, check the three recovery inputs for the previous two weeks: sleep, calories and bodyweight trend (`guide/04-periodization-and-progression.md`, section 5). If one is obviously off, fix it and hold the load one more exposure. Otherwise **reset the top-set load by 7.5%** (round down) and rebuild at the normal increment. You pass the stall load again in 3-4 weeks (squat, deadlift) or 5-6 weeks (bench, press), with more volume behind you. Range of reset sizes in the sources: Starting Strength 5-10%, StrongLifts 10%, Stronger By Science 10-15%, 5/3/1 training max to 90% (`research/periodization-and-progression.md`, Q2, Q5; all conventions).
2. **Second stall on the same lift within 12 weeks:** reset 7.5% again **and change the rep zone** for one block: top set 1 x 6 @ RPE 8 with back-offs 3 x 6 at -7% (2 x 6 merged); the V exposure keeps 4 x 6 at 90% and will feel easy, which is intended. Return to 4s at the next block. Changing the relative-intensity zone is the best-supported plateau move after a load reset (`guide/04-periodization-and-progression.md`, section 5).
3. **Third stall, or no e1RM progress across a full block plus deload:** reduce the H exposure to the top set plus one back-off for a block (the Texas Method fix of cutting volume on the heaviest day when the top set stalls), or change the variant for a block at a block boundary only (pause squat, close-grip bench, deficit deadlift, seated press). Only after that, change the scheme (for example, a percentage wave off a training max in the 5/3/1 style, described in chapter 04). Program-hopping before the stall rule has fired is the error, not the stall.

Resets never touch the other lifts. A squat stall does not change the deadlift track.

Optional block-level variation for lifters who want it even without a stall: alternate 4s and 6s block to block. Periodized loading beats static loading for 1RM by a small margin in trained lifters (Moesgaard 2022, ES 0.31), with no difference between undulating styles.

---

## 7. Deload

Every 4-6 passes (for 3- to 6-day weeks, every 4-6 calendar weeks), or sooner on two or more readiness red flags for a week (`guide/03-flexible-scheduling.md`, section 4.5), run one deload pass:

- **Top sets at RPE 6-7:** the current track load x 0.90-0.92, same 4 reps. The track does not advance; after the deload the next H attempts the pre-deload planned load.
- **One back-off set** per H exposure. **V exposures 2 sets.** Row and pull-up 2 sets at the track load.
- **Accessories 1-2 sets**, isolation light.
- **Keep every session and every main lift.** A full week off mid-block cost lower-body strength in the one RCT (Coleman et al. 2024); coaches keep frequency and cut volume and effort (Bell et al. 2023 Delphi). Both: `research/periodization-and-progression.md`, Q3.

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

Apply the table at an H exposure. If a V exposure is the first thing a lift does after a gap of 8 or more days, do it as written (it is already at 90% of the track load); it resets the clock and the H that follows runs the normal rule.

This table is an inference from detraining timelines (one week off: 3-7% strength dip that returns in 1-2 sessions; noticeable loss from about 3 weeks; about 6-9% 1RM loss after a 4-week layoff, all secondary summaries), and from Nippard's comeback guidance of compounds at RPE 5 or lower in the first week back. No source quantifies progression adjustments by days since exposure (`research/flexible-frequency-programming.md`, KQ3, KQ6 and gaps).

---

## 9. Rounding and equipment

- Squat and deadlift: 2.5 kg steps. Bench and press: 1 kg steps with 0.5 kg plates; without them, 2.5 kg every second successful exposure.
- Back-off and V loads: compute, then round to the nearest loadable weight. Record the loaded weight, not the computed one.
- If a session must use a substitute for a main lift (travel, equipment), the substitute does **not** update the track and does not count as an exposure for the gap clock. Strength is modality- and range-specific (Haugen 2023; Pallares 2019; `research/exercise-selection-and-session-design.md`, KQ7); keep the barbell lift itself at least once a week.
- Dumbbell bench runs at roughly 35-40% of the barbell load per hand; treat any substitute as a new baseline and progress it by double progression.

---

## 10. Logging

**Per set:** exercise, load, reps, RPE, a note on technique or pain. Example line: `2026-11-03 L1 squat H 125x4 @8 | 117.5x4 @7, @7.5, @8`.

**Per lift (the track state), updated at each H exposure:**

| Field | Example |
|---|---|
| Top-set load (planned for next H) | 127.5 |
| Rep target | 4 |
| Miss counter | 0 |
| Last exposure date (H or V) | 2026-11-07 (V) |
| e1RM history (last 6 H exposures) | 142, 144, 147, 147, 150, 153 |

**e1RM:** from the top set, `e1RM = load x (1 + (reps + RIR) / 30)`, where RIR = 10 - RPE. Example: 125 x 4 @ 8 gives 125 x (1 + 6/30) = 150. This is an Epley-style convention; any consistent formula serves, because the quantity that matters is the trend. Use heavy, low-rep, RPE 8+ sets only; RIR ratings from long sets are less accurate (Russo et al. 2025). Barbell Medicine recomputes e1RM each workout from the most accurate set and sets back-offs from it (`research/periodization-and-progression.md`, Q2, Q7; convention).

**Per session:** bodyweight, sleep hours, a 1-5 readiness score. **Per week:** hard sets per muscle group (half credit for indirect work; tallies at the bottom of each template).

**Judging a block:** average the e1RM of the last three H exposures and compare with the first three. The block worked if e1RM rose at matched RPE, or reps rose at the same load, or RPE fell at the same load. If none of those happened after a full block plus deload, run the stall procedure in section 6 even if no formal stall fired. Single-session changes are mostly noise ("most of what gets called a stall is impatience with the noise floor," Barbell Medicine podcast, convention).

---

## 11. Accessory progression (every exercise that is not a main-lift exposure)

- **Double progression.** Fix the load. Add reps each exposure until every set hits the top of the rep range at RPE 9 or less. Then add the smallest increment (2.5 kg on a barbell or stack, one dumbbell step) and drop to the bottom of the range. The last set of an isolation exercise may go to failure; compounds stay at 1-3 RIR (`guide/01-training-principles.md`, section 5).
- **Starting load:** one you can lift for the bottom of the range with 2-3 reps in reserve.
- **Dynamic variant** for lifters who log set by set: increase load on a specific set only if that set exceeded the range last time (Helms' Muscle and Strength Pyramid description, `research/periodization-and-progression.md`, Q2).
- **Short weeks** skip some sets of an accessory; they never reset its load.
- **Stall:** two exposures without a rep gained at a load, drop 5% and rebuild, or swap to a same-length alternative (seated curl for lying curl, overhead for neutral triceps) at a block boundary. Rotate accessories every 4-8 weeks or when they stall, not session to session (`guide/05-exercise-selection.md`, section 8).
- Triple progression (reps, then sets, then load) is available for accessories you train in every week type, but the extra set is the first thing a short week removes, so it is not the default.

---

## 12. Named-program rules, for orientation only

These are described so you can see where this program's rules come from. They are not reproduced as tables, and the books they come from are paid (`research/splits-and-named-programs.md`, KQ9).

| Program | Rule this program borrows | Rule it does not |
|---|---|---|
| Barbell Medicine templates, Helms RPE work | RPE-anchored top set, back-offs as a percentage of it, e1RM recomputed each session (RPE vs percentage: Helms 2018, +17.05 vs +13.91 kg squat, not significant; Hickmott 2022, SMD 0.21, not significant) | Their specific percentages and set counts |
| 5/3/1 (Wendler) | "Never increase on a miss"; reset to about 90% when progress stops; the cycle stretches with fewer days (5+ weeks at 3 days per week) | Training-max percentage waves; AMRAP top sets |
| Texas Method | One load step per week on squat and deadlift, slower on bench and press; cut volume on the heavy day when the top set stalls | Fixed Monday/Wednesday/Friday roles |
| GZCLP / GZCL | Per-exposure progression; tier priority when cutting (keep the main lift, trim the second, drop accessories; an inference from the tier structure) | Rep-scheme ladders (5x3, 6x2, 10x1) |
| Starting Strength / StrongLifts / Greyskull | Reset size 5-10% on a lift that stalls; the stall is counted in exposures, not weeks | Per-session increments every exposure |
| Reactive Training Systems | Fatigue-percent framing of back-offs (about 5% as the average drop) | Working up to RPE 9-10 |

---

## 13. Flags

- The RPE-to-percentage conversions behind "95% of a 5RM" and "80% of a 1RM" are Epley-based conventions; the published RPE tables were not retrievable (`research/periodization-and-progression.md`, Q2 gaps).
- The -7% back-off and 90% V figures are design choices inside the 5-8% range the research note inferred, not tested values.
- The gap-modifier table is an inference from secondary detraining summaries.
- No controlled trial compares linear, double and triple progression, or RPE-stop volume over a block (Hickmott 2022 found none).
- No peer-reviewed validation of the e1RM-trend method as a predictor of long-term progress exists (`research/periodization-and-progression.md`, Q7 gaps).

---

## Sources

- `research/periodization-and-progression.md`: Q2 (linear and double progression rules; 5/3/1 training max and reset; GZCLP ladder and restart; Texas Method pace and stall fix; RPE loading, RTS fatigue percents, Barbell Medicine e1RM; Helms 2018; Hickmott 2022), Q3 (deloads: Coleman 2024; Bell 2022; Bell 2023), Q5 (plateau order; named stall rules), Q6 (reactive loading), Q7 (logging, e1RM, block criteria; Russo 2025).
- `research/flexible-frequency-programming.md`: KQ3 (detraining timelines), KQ4 (RPE-anchored top sets, RPE stops, Barbell Medicine forum reply, Nippard comeback RPE), KQ6 (exposure-indexed progression; days-since-exposure modifier, flagged as inference).
- `research/frequency-volume-intensity-evidence.md`: Q1 (frequency benefit for strength: Pelland et al. 2025/26), Q4 (RIR-based RPE: Zourdos et al. 2016; proximity to failure: Robinson et al. 2024), Q6 (minimum effective dose: Androulakis-Korakakis 2020/2021).
- `research/exercise-selection-and-session-design.md`: KQ5 (warm-up ramp: Ribeiro et al. 2020; Behm et al. 2016), KQ7 (modality-specific strength: Haugen et al. 2023; Pallares 2019).
- `research/splits-and-named-programs.md`: KQ2, KQ3 (program increments and resets), KQ9 (copyright status).
- Key primary citations: Helms et al. 2018 (Front Physiol, [PMC5877330](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5877330/)); Hickmott et al. 2022 (Sports Med Open, [PMC8762534](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8762534/)); Zourdos et al. 2016 (JSCR 30:267, [AUT repository](https://openrepository.aut.ac.nz/items/efef3b25-6701-4fb5-bb82-55fcd2a26027/full)); Russo et al. 2025 ([PDF](https://dspace.uevora.pt/rdpc/bitstream/10174/39438/1/2025%20Russo%20et%20al.%20Factors%20influencing%20the%20accuracy%20of%20the%20repetition%20in%20reserve%20scale%20in%20resistance%20training%20%20a%20systematic%20review.pdf)); Coleman et al. 2024 ([PeerJ 16777](https://peerj.com/articles/16777)); Bell et al. 2023 (Sports Med Open 9:87, [PMC10511399](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10511399/)); Moesgaard et al. 2022 (Sports Med, [PubMed 35044672](https://pubmed.ncbi.nlm.nih.gov/35044672/)); Pelland et al. 2025/26 ([SportRxiv 460](https://sportrxiv.org/index.php/server/preprint/view/460)); Ribeiro et al. 2020 ([PubMed 32971729](https://pubmed.ncbi.nlm.nih.gov/32971729/)); Haugen et al. 2023 ([DOAJ](https://doaj.org/article/a7282dba5e674176bde2a8239832d2f7)). Program-author and coaching sources: Jim Wendler, [5/3/1 for Hardgainers](https://www.jimwendler.com/blogs/jimwendler-com/5-3-1-for-hardgainers); Starting Strength, [The Reset](https://startingstrength.com/article/the-reset-why-and-how) and [Texas Method intensity day](https://startingstrength.com/article/understanding-the-texas-method-intensity-day); thefitness.wiki, [GZCLP](https://thefitness.wiki/routines/gzclp/); Stronger By Science, [novice tips](https://www.strongerbyscience.com/making-your-novice-strength-training-routine-more-effective-two-quick-tips/); EliteFTS, [Reactive Training Manual overview](https://elitefts.com/education/a-reactive-training-manual-overview); Barbell Medicine forum, [e1RM in the templates](https://forum.barbellmedicine.com/t/e1rm-calculation-in-the-templates/664) and [using RPE or adjusting the schedule](https://forum.barbellmedicine.com/t/using-rpe-or-adjusting-the-training-schedule/19074); AUT repository, [RPE volume autoregulation thesis](https://openrepository.aut.ac.nz/bitstream/10292/12177/2/RPE%20volume%20autoregulation.pdf); Jeff Nippard, [training after a break](https://jeffnippard.com/blogs/news/how-to-get-your-gains-back-after-a-training-break).
