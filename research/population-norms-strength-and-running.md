# Population norms: barbell strength and 10-mile running

Last updated: 2026-11-08

Scope: where this lifter's barbell strength and 10-mile race time sit against
(a) the general population, (b) people who train or race, and (c) performance
standards. The lifter is a 25-year-old man, 181 lb (82 kg), 5'11", about 16.5%
body fat (InBody). His lifts and race are in `data/body-composition.md` §4 and
`data/races.md`. Body-composition norms (height, weight, body fat, FFMI) are
already in `data/body-composition.md` §3 and are not repeated.

Tags: **[Evidence]** peer-reviewed; **[Foundational]** peer-reviewed or
institutional and pre-2016; **[Practitioner]** practitioner or user-submitted
data; **[Primary data]** computed here from raw results.

Method: web search, then the primary page for each figure where it could be
opened. Each item says what was read. ExRx (Kilgore-Rippetoe-Hartman
standards) returned HTTP 403 and is left out.

## KQ1. Strength against the general population (men 20-29)

There is no good population dataset for free-weight 1RMs. Most men do not lift,
and studies test volunteers.

- **[Foundational] Cooper Institute bench-press norms**, 1RM ÷ bodyweight, men
  20-29. From *Physical Fitness Assessments and Norms for Adults and Law
  Enforcement* (Cooper Institute monograph, not peer-reviewed). Table read in
  the ACE reprint,
  https://contentcdn.eacefitness.com/assets/certification/ace-answers/forms/pt/38_Bench-Press_Assessment_Protocol.pdf.
  Percentiles 5 / 20 / 40 / 60 / 80 / 95: 0.72 / 0.88 / 0.99 / 1.14 / 1.32 /
  1.63. The 50th (1.06) comes only from a secondary page citing the 2013
  monograph (https://fitnessnorms.pages.dev/strength/cooper-bench-press/male/age-20-29).
  Caveats: Universal DVR machine, not a barbell, and no study converting one to
  the other was found. Sample: Cooper Clinic patients, likely fitter than
  average. No sample size given.
- **[Foundational] ACSM leg-press norms** (Institute for Aerobics Research
  1994, same machine). Only two cutoffs verified (study-notes page): 2.27 "well
  above average", 2.13 "above average". The often-quoted 50th percentile of
  about 1.91 was not verified. Does not translate to a back squat.
- **Deadlift:** no general-population norm found.
- **[Evidence] Baseline 1RMs of "untrained" young men in training studies.**
  Definitions of untrained vary, and the samples disagree.

| Study | n, bodyweight | Baseline 1RM | Caveat |
|---|---|---|---|
| Mao et al. 2023, *Front Physiol* 14:1301535, https://pmc.ncbi.nlm.nih.gov/articles/PMC10749963/ | 26; 79-82 kg | Bench 69-71 kg (about 0.87x), back squat 111-115 kg (about 1.4x), bent-over row 67-69 kg (about 0.85x) | No resistance training in the past year; some had trained before |
| Yapici et al. 2023, *Front Physiol* 14:1148494, https://pmc.ncbi.nlm.nih.gov/articles/PMC10064218/ | 22; 73-76 kg | Bench 51-53 kg (about 0.70x), squat 60-69 kg (about 0.85x) | Called untrained; exclusion criteria contradict that; equipment not stated |
| Kikuchi & Nakazato 2017, *J Exerc Sci Fit* 15:37, https://pmc.ncbi.nlm.nih.gov/articles/PMC5812864 | 18; 63 kg | Bench 60-61 kg (about 0.95x) | PE students with 1+ year of lifting |

Full texts read via PMC (agent summary; figures as reported there).

## KQ2. Strength against people who train

- **[Evidence] Van den Hoek et al. 2024**, *J Sci Med Sport* 27:734 (809,986
  drug-tested raw powerlifting entries), https://ro.ecu.edu.au/ecuworks2022-2026/4617.
  Men 18-35, 90th percentile: squat 2.83x, bench 1.95x, deadlift 3.25x
  bodyweight. Abstract only; lower percentiles not seen. A highly selected
  group.
- **[Practitioner] Strength Level**, male, 180 lb row,
  https://strengthlevel.com/strength-standards/male/lb (page read). The levels
  mean stronger than 5 / 20 / 50 / 80 / 95% of the site's lifters. Data: 40.1M
  lifts from 27.9M users, 2015-2026. User-submitted, unverified, many
  calculator estimates. Users are probably stronger and more engaged than the
  typical gym-goer.

| Lift (lb) | Beginner (5%) | Novice (20%) | Intermediate (50%) | Advanced (80%) | Elite (95%) |
|---|---|---|---|---|---|
| Squat | 169 | 228 | 298 | 377 | 462 |
| Bench | 127 | 169 | 220 | 277 | 339 |
| Deadlift | 201 | 268 | 348 | 438 | 535 |
| Overhead press | 75 | 104 | 140 | 181 | 226 |
| Bent-over row | 108 | 149 | 198 | 255 | 315 |
| Lat pulldown | 106 | 143 | 189 | 241 | 296 |

Lat pulldown from https://strengthlevel.com/strength-standards/lat-pulldown/lb.

- **[Practitioner] Symmetric Strength**, 180 lb,
  https://symmetricstrength.com/standards (page read). Modelled from Wilks
  scores; the page says they are "not population percentiles". Untrained /
  Novice / Intermediate: squat 135 / 205 / 270, bench 100 / 150 / 200,
  deadlift 155 / 235 / 310, overhead press 65 / 100 / 130.

## KQ3. 10-mile race time against race fields

- **[Primary data] EQT Pittsburgh 10 Miler.** Full results from Race Roster's
  results API (`results.raceroster.com/v2/api/result-events/<id>/sub-events/<sub>/results`;
  2026: 99419/385379, pulled 2026-11-08 and re-checked; 2025: 94253/246884).
  Net (chip) times. 2026 results were still provisional on race day.

| | 2026 | 2025 |
|---|---|---|
| Timed finishers | 3,819 | 3,325 |
| Overall median | 1:36:11 | 1:35:11 |
| Men median (n) | 1:30:15 (1,757) | 1:28:56 (1,575) |
| Men 25-29 median (n) | about 1:27:00 (279-283, by division or by age) | 1:26:39 (228) |

  The lifter's 1:27:35 (2026) beat 69% of all finishers, 56% of men and 49% of
  men 25-29. His 1:28:19 (2025) beat 66%, 52% and 46%.
- **[Primary data] Cherry Blossom 10 Miler 2017**, Washington DC, 17,442
  finishers (OpenIntro `run17`, https://www.openintro.org/data/index.php?data=run17).
  Men median 1:30:43 (n = 6,996); men 25-29 median 1:27:34 (n = 1,170).
  1:27:35 beats 57% of men and sits at the 25-29 median.
- **[Practitioner] RunRepeat, State of Running** (107.9M results 1986-2018),
  https://runrepeat.com/state-of-running. No 10-mile figure. Men's average 10K
  pace 5:51/km (about 58:30 for 10K).
- Race fields are self-selected: people who train for and finish a 10-mile race
  are fitter than the general population. No general-population 10-mile figure
  exists.

## KQ4. Running against performance and fitness standards

- **[Practitioner] Age grading**, Alan Jones MLDR road tables,
  https://github.com/AlanLyttonJones/Age-Grade-Tables (read). Age factor at 25
  is 1.000. Men's 10-mile open standard: 43:15 (2025 tables, current), 43:45
  (2020), 44:00 (2015), 44:24 (2010). Age grade of 1:27:35: **49.4%** on the
  2025 tables (50.7% on the 2010 ones). Common bands (1989 WAVA; secondary
  calculator sites only): 60% local class, 70% regional, 80% national, 90%
  world class. On the 2025 tables, 60% at 25 is about 1:12:05.
- **[Foundational] Daniels & Gilbert 1979 VDOT equations.** 1:27:35 for
  10 miles gives VDOT 37.6 (2025: 37.2). Equivalents: 5K about 25:24, 10K about
  52:40, half marathon about 1:57.
- **[Evidence] FRIEND registry**, Kaminsky et al. 2015, *Mayo Clin Proc*
  90(11):1515-1523, https://pmc.ncbi.nlm.nih.gov/articles/PMC4919021/ (read).
  Treadmill VO2max, men 20-29 (n = 513), percentiles 5 / 10 / 25 / 50 / 75 / 90
  / 95: 29.0 / 32.1 / 40.1 / 48.0 / 55.2 / 61.8 / 66.3 mL/kg/min.
  **[Evidence] FRIEND 2022 update**, Kaminsky et al., *Mayo Clin Proc*
  97(2):285-293 (paywalled; secondary copies only, and they conflict: 50th
  percentile 46.5 or 45.4, likely different RER cutoffs). Standards are
  1.5-4.6 lower than 2015.
- **[Evidence] Scudamore, Barry & Coons 2018**, *J Strength Cond Res*
  32(4):1137-1143 (abstract). VDOT underestimated lab VO2max, more so in
  recreational runners (d = 3.44) than collegiate athletes (d = 1.75). So VDOT
  37.6 falls at about the 20th-25th percentile of FRIEND, and that is a floor:
  a low-mileage runner's measured VO2max is probably higher.

## Inferences for this lifter (2026-11-08)

| Area | Where he sits | Basis |
|---|---|---|
| Body composition | Leaner than about 80-85% of men his age; FFMI 21.1 vs median 18.9 | `data/body-composition.md` §3 |
| Squat, now 191 lb (1.06x) | About 10th percentile of Strength Level users; between the untrained samples | KQ1, KQ2 |
| Squat, 2024 best 291 lb (1.61x) | About 45th percentile of Strength Level users; above all three untrained samples | KQ1, KQ2 |
| Bench, 133 lb (0.73x), same in 2024 | About 5th percentile of Cooper (machine norms); about 7th of Strength Level users; similar to the weakest untrained sample | KQ1, KQ2 |
| Deadlift, 185 lb (1.02x), same in 2024 | Below Strength Level's Beginner cutoff | KQ2 |
| Overhead press, 84 lb (0.46x) | About 10th percentile of Strength Level users | KQ2 |
| Lat pulldown, 161 lb | About 30th percentile of Strength Level users | KQ2 |
| 10-mile race | Middle of the men's field (beat 56%); at the median for men 25-29 at two races | KQ3 |
| Running standard | Age grade about 49%; VDOT about 20th-25th percentile of lab VO2max (a floor) | KQ4 |

- **Muscle is ahead of strength.** Lean mass is well above average while every
  lift except the 2024 squat sits low against people who train. Strength
  depends on practice of the specific lift as well as muscle. The lifter has
  about 60 lifting sessions logged in total, March 2024 to now, at about 2 a week in active weeks.
  So the gap is mostly skill and exposure, not a ceiling. Inference.
- **The deadlift has never been pushed.** 10 sessions, best set 155 lb (70.3 kg)
  x 6, and it trails the squat. Lifters usually deadlift more than they squat.
  It is the lift with the most room. The caution phase to 9 Jan 2027
  (`templates/progression-tracks.md` §5.2) still applies.
- **Bench and press have been flat since 2024**, at about 2 sessions a week and
  low per-muscle volume. That fits the volume evidence
  (`research/frequency-volume-intensity-evidence.md`), not a talent limit.
- **Running is average for a race field and above the general population.** The
  bodyweight gain since 2025 penalises every per-kilogram running measure.
- **Week types.** Nothing here changes the rules. 5-6-day weeks give each main
  lift 2-3 exposures and more weekly sets, which is how lagging lifts catch up.
  3-day weeks keep each lift at 2 exposures and hold the line.

## Gaps

- No population norm for free-weight squat or deadlift; Cooper bench is a
  machine.
- Strength Level and Symmetric Strength are not population samples.
- FRIEND 2022 tables not read in the original.
- Age-grade category bands seen only on secondary sites.
