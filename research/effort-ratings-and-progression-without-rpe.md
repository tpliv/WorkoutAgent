# Effort ratings and progression without RPE: rating accuracy, calibration, and rep-based fallbacks

Last updated: 2026-11-06

**Scope.** The progression engine (`templates/progression-tracks.md` §5, `tools/update_tracks.py`) sets every main-lift load from the RPE of one heavy top set of 4 reps (target RPE 8). RPE 7 or easier earns a big step. RPE 9.5 or harder, or fewer than 4 reps, counts as a miss. The lifter has logged no RPE on any set since 27 Oct 2026, so every decision since then has assumed RPE 8 (`data/track-log.md`). The one time he did report a rating (bench 105 x 6 @ 8 on a 4-rep target), the right call was a big step. The engine missed it because it does not credit reps above the target. This note asks five questions. KQ1: how accurate are RIR/RPE ratings? KQ2: can accuracy be trained or calibrated? KQ3: what can replace ratings? KQ4: does autoregulation change outcomes? KQ5 (inference): what is the smallest input that keeps the engine working? It extends `research/frequency-volume-intensity-evidence.md` (KQ4 and its addendum), `research/periodization-and-progression.md` (KQ2, KQ7 and the 2026-10-21 addendum) and `research/coaching-check-ins.md` (KQ2). It does not rewrite their conclusions. Where it refines one of their statements, it says so in the last section.

**Method.** Abstracts and metadata came from PubMed (E-utilities) and Crossref. Open full texts came from Europe PMC (Wiedenmann 2026, Nuzzo 2024) and the authors' accepted manuscript of Graham & Cleather 2021 (St Mary's University repository). Practitioner and vendor pages were fetched directly: Stronger By Science, Barbell Medicine, Bryan Mann's APRE article in *Training & Conditioning*, and Hevy's own pages. Each finding says what was read: **full text**, **abstract**, or **secondary** (a search-engine or third-party summary). Russo et al. 2025 could not be opened: the University of Évora repository failed TLS through the proxy and then returned 503, and the publisher returned 403. It is described from its indexed summary only. Tags: **[Evidence]** = peer-reviewed; **[Practitioner]** = coach, program-author or well-cited practitioner site; **[Vendor]** = app maker; **[Convention]** = coaching practice. **(foundational)** = pre-2016. S = strength outcome, H = hypertrophy outcome.

Direction of error, as used throughout:
- **Underpredict** means the lifter thought fewer reps were left than there were. A true RPE 7 gets called an 8.
- **Overpredict** means the lifter thought more reps were left than there were.

---

## KQ1. How accurate are RIR/RPE ratings, and what changes the accuracy?

### Takeaway

- On submaximal sets, people underpredict reps to failure by about one rep on average: 0.95 reps (95% CI 0.17-1.73) across 12 studies (Halperin 2022). The spread is wide.
- Error shrinks closer to failure, with fewer reps per set (12 or fewer), with heavier loads, and in later sets.
- Training experience mostly does not matter. Bench is rated more accurately than squat or leg press in most studies that compared them.
- The engine's top set sits near the best case measured: 4 reps at about 84% 1RM, about 2 RIR. The expected absolute error there is about 0.5-1 rep.
- Near a true max the error flips. Lifters rate a real 1RM as 9.35-9.86, so they think a rep is left when none is.

### Cited findings

**Syntheses**

- **[Evidence] Halperin, Malleron, Har-Nir, Androulakis-Korakakis, Wolf, Fisher & Steele 2022**, *Sports Med* 52(2):377-390, [PubMed 34542869](https://pubmed.ncbi.nlm.nih.gov/34542869/). Scoping review and exploratory multilevel meta-analysis: 13 publications (12 studies), 414 participants, 262 effects. Abstract.
  - Underprediction 0.95 reps (0.17-1.73). Heterogeneity was very high: I² = 97.9%.
  - Closer to failure: slightly more accurate (β = -0.025, CI -0.05 to 0.0014).
  - Reps to failure ≤ 12: β = 0.06 (0.04-0.09). Reps to failure > 12: β = 0.47 (0.44-0.49).
  - Later sets: trivially more accurate (β = -0.07 reps per set, CI -0.14 to -0.005).
  - Training status: no effect (β = -0.006, CI -0.02 to 0.007). Upper minus lower body: -0.58 reps (CI -2.32 to 1.16).
  - Between-participant SD 1.45 reps (0.99-2.12).
  - The authors conclude that accuracy is better closer to failure, with heavier loads and in later sets. The abstract gives no coefficient for load.
- **[Evidence] Russo, Marconcin, Gomes, Peralta, Flôres & Casanova 2025**, *Physical Therapy Reviews*, [doi:10.1080/10833196.2025.2564026](https://doi.org/10.1080/10833196.2025.2564026). Systematic review: 520 records screened, 26 studies included, quality rated on the Newcastle-Ottawa Scale. Accuracy was higher closer to failure, "particularly in exercises involving the upper limbs". It fell as reps per set rose and as %1RM fell. **Secondary** (indexed summary). Full text unreachable.
- **[Evidence] Bastos, Machado & Teixeira 2024**, *Percept Mot Skills* 131(3):940-970, [PMC11127506](https://pmc.ncbi.nlm.nih.gov/articles/PMC11127506/). Scoping review of 31 studies (N = 855, mostly men). RIR scales were feasible and useful for setting intensity. Predictions should be made close to failure. Abstract.

**Primary studies (free weights and machines)**

| Study | Sample | Task | Accuracy | Direction | Read |
|---|---|---|---|---|---|
| **[Evidence] Refalo et al. 2024**, *JSCR* 38(3):e78-e85, [PubMed 37967832](https://pubmed.ncbi.nlm.nih.gov/37967832/) | 24 trained (12 M, 12 F) | Bench at 75% 1RM, 2 sets to failure, 2 sessions; called 1 and 3 RIR | Absolute error 0.65 ± 0.78 reps. Within ±1 rep (equivalence) for 1 vs 3 RIR, set 1 vs 2, and session 1 vs 2. Not related to sex, years trained or relative strength | Raw -0.17 ± 1.00: slight underprediction | Abstract |
| **[Evidence] Zourdos et al. 2021**, *JSCR* 35(S1):S158-S165, [PubMed 30747900](https://pubmed.ncbi.nlm.nih.gov/30747900/) | 25 trained men (training age 4.7 ± 3.2 y) | Squat at 70% 1RM to failure (16 ± 4 reps); called RPE 5, 7, 9 | Error 2.05 ± 1.73 reps at a called 9; 3.65 ± 2.46 at 7; 5.15 ± 2.92 at 5. Reps per set predicted error at 5 (r = 0.65) and 7 (r = 0.56), not at 9 (r = 0.01). Training age did not predict error | Underprediction | Abstract |
| **[Evidence] Hackett, Cobley, Davies, Michael & Halaki 2017**, *JSCR* 31(8):2162-2168, [PubMed 27787474](https://pubmed.ncbi.nlm.nih.gov/27787474/) | 81 adults (53 M, 28 F), mixed experience | Up to 10 sets of 10: chest press at 70%, leg press at 80% | About 1 rep of error at 0-5 reps to failure; more than 2 at 7-10. Error ≤ 1 rep over 0-5 reps for the chest press, but only over 0-3 for the leg press. Men more accurate on the leg press at some points. Experience had no effect | — | Abstract |
| **[Evidence, foundational] Hackett, Johnson, Halaki & Chow 2012**, *J Sports Sci* 30(13):1405-13, [PubMed 22873691](https://pubmed.ncbi.nlm.nih.gov/22873691/) | 17 male bodybuilders | 5 x 10 at 70%, bench and squat | Estimated vs actual reps to failure r ≥ 0.93. Accurate in sets 3-5 (ES 0.37 to 0.0). ICC ≥ 0.92; 95% limits of agreement ≤ 0.63 reps. Borg RPE at failure was below maximal | — | Abstract |
| **[Evidence] Steele, Endres, Fisher, Gentil & Giessing 2017**, *PeerJ* 5:e4105, [PubMed 29204323](https://pubmed.ncbi.nlm.nih.gov/29204323/) | 141 trainees | Full-body session, single sets to failure, reps predicted beforehand | SEM 2.64 (2.36-2.99) to 3.38 (3.02-3.83) reps. "Tendency towards improved accuracy with greater experience" | Underprediction | Abstract |
| **[Evidence] Armes et al. 2020**, *Front Psychol* 11:565416, [PubMed 33424678](https://pubmed.ncbi.nlm.nih.gov/33424678/) | ≥ 1 y trained; n = 14 and 24 | Knee extension at 70% 1RM or 70% MVC; deception design | Pooled underprediction 2.0 reps (0.0-4.0) | Underprediction | Abstract |
| **[Evidence] Remmert, Laurson & Zourdos 2023a**, *Percept Mot Skills* 130(3):1239-54, [PubMed 37036795](https://pubmed.ncbi.nlm.nih.gov/37036795/) | 27 M, 31 F, trained and untrained | Curl, pushdown and seated row at 72.5% 1RM, 4 sets to failure | More accurate closer to failure and in later sets. No effect of exercise (p = 0.688), sex, experience, or experience with RIR. The Stronger By Science summary quotes mean errors of 1.2 reps at 5 RIR and 0.46 at 1 RIR, and 0.96 (set 1) vs 0.71 (set 3) | — | Abstract; numbers secondary |
| **[Evidence] Mansfield, Peiffer, Hughes & Scott 2020**, *JSCR* (online ahead of print), [PubMed 32881842](https://pubmed.ncbi.nlm.nih.gov/32881842/) | 20 trained men | Bench and prone row, 3 sets at 80% and at 60% | Set-1 estimates below actual RIR (ES 1.30-2.89). Accuracy improved from set 1 to set 3. Knowing the load made no difference (randomised, blinded vs informed) | Underprediction | Abstract |
| **[Evidence] Ruiz-Alias et al. 2025**, *Sports Health* 17(5):1007-12, [PubMed 39382146](https://pubmed.ncbi.nlm.nih.gov/39382146/) | 26 recreationally trained (12 F, 14 M) | Bench to failure at 65, 75 and 85%; free weight vs Smith | At 65% only: women -1.2 reps (-1.7 to -0.6) vs men -0.1 (-0.6 to 0.3); free weight -1.1 (-1.5 to -0.6) vs Smith -0.2 (-0.6 to 0.2). No differences at 75% or 85% | Underestimation at the light load | Abstract |
| **[Evidence] Helms, Brown, Cross, Storey, Cronin & Zourdos 2017a**, *JSCR* 31(10):2938-43, [PubMed 28933716](https://pubmed.ncbi.nlm.nih.gov/28933716/) | 12 powerlifters | Chose loads for 8 @ 8, 2 @ 8, 3 @ 9 over 3 weeks | Mean absolute deviation from target 0.33 ± 0.28 RPE (range 0.22-0.44). On 8 @ 8 sets, bench was closer to target than squat (0.14 ± 0.44 vs -0.19 ± 0.21). Bench was closer at 3 @ 9 than at 2 @ 8. This is the lifter's own rating vs the target, not a check against failure | — | Abstract |
| **[Evidence] Helms et al. 2017b**, *JSCR* 31(2):292-7, [PubMed 27243918](https://pubmed.ncbi.nlm.nih.gov/27243918/) | 15 powerlifters | Worked up to a 1RM | RPE given at a true 1RM: squat 9.6 ± 0.5, bench 9.7 ± 0.4, deadlift 9.6 ± 0.5. %1RM vs RPE r = 0.88-0.91 | At max: rated below 10 (overpredicts reserve) | Abstract |
| **[Evidence] Ormsbee et al. 2019**, *JSCR* 33(2):337-45, [PubMed 28301439](https://pubmed.ncbi.nlm.nih.gov/28301439/) | 27 college men; experienced (4.7 ± 2.0 y) vs novice (1.1 ± 0.6 y) benchers | Bench 1RM, singles at 60/75/90%, 8 reps at 70% | RPE at 1RM 9.86 ± 0.14 (experienced) vs 9.35 ± 0.36 (novice), p = 0.011. No group difference at the other loads. Velocity vs RPE r = 0.85 in both groups | At max: novices overpredict reserve more | Abstract |
| **[Evidence] Hermann et al. 2025**, *MSSE* 57(9):2021-31, [PubMed 40249908](https://pubmed.ncbi.nlm.nih.gov/40249908/) | 42 trained, 8-week single-set training study | RIR estimation tested in bench and squat | Bench rated more accurately than squat. Accuracy improved over the 8 weeks, "particularly for the bench press". Magnitudes not in the abstract | — | Abstract |
| **[Evidence] Wiedenmann et al. 2026**, *BMC Sports Sci Med Rehabil* 18:375, [PMC13499321](https://pmc.ncbi.nlm.nih.gov/articles/PMC13499321/) | 13 younger (33 ± 7 y, 9 F) and 13 older adults | Bench and leg press at 75-85%; called 4 and 2 RIR, then to failure | Session-1 mean absolute error, younger adults: bench 1.6 reps at 2 RIR and 2.4 at 4 RIR; leg press 2.9 and 4.6. More accurate at 2 RIR than 4 RIR, and on the bench than the leg press | Both groups underestimated | Full text |
| **[Evidence] Droguett et al. 2026**, *J Hum Kinet* 102:145-158, [PubMed 42211811](https://pubmed.ncbi.nlm.nih.gov/42211811/) | 16 adults: 8 with ≥ 18 months of training, 8 with less | Smith squat at 70%; 3 RIR and 1 RIR sets | No accuracy difference between experience groups (p > 0.05) | — | Abstract |
| **[Evidence] Lovegrove et al. 2022**, *JSCR* 36(10):2696-2700, [PubMed 36135029](https://pubmed.ncbi.nlm.nih.gov/36135029/) | 15 novice-trained young men (17.3 y) | Worked up to a load felt as 1 RIR for 3, 5 and 8 reps; deadlift and bench | Test-retest reliability of the chosen load: deadlift ICC 0.95-0.99 (CV 2.7-5.7%); bench ICC 0.97-0.99 (CV 3.8-6.2%). Loads chosen for 1 RIR at 3/5/8 reps: deadlift 88.2/84.3/79.2% 1RM; bench 93.0/87.3/79.6% | Not tested against failure | Abstract |
| **[Evidence] Hackett & Sabag 2022**, *Sports* 10(2):27, [PMC8877029](https://pmc.ncbi.nlm.nih.gov/articles/PMC8877029/) | 20 trained men | 5 x 10 at 70%, bench and squat | High local muscular endurance went with more error in set 1. Strength level was not related to error | — | Abstract |
| **Retracted:** Hughes, Peiffer & Scott 2020, *JSCR*, [PubMed 33337690](https://pubmed.ncbi.nlm.nih.gov/33337690/), retraction *JSCR* 2021;35(3):585 | — | — | It reported 2-RIR calls accurate at 85% 1RM and increasingly underestimated at 75% and 65%. **Not used as evidence.** | — | Abstract and retraction notice |

**Factors, summarised**

| Factor | Effect on accuracy | Main sources |
|---|---|---|
| Proximity to failure | Closer is more accurate | Halperin 2022; Zourdos 2021; Hackett 2017; Remmert 2023a; Wiedenmann 2026; Russo 2025 |
| Reps per set | Fewer is more accurate. Sets of more than 12 reps are much worse | Halperin (β 0.06 vs 0.47); Zourdos 2021 (r 0.65, 0.56); Remmert 2023b (more reps, more underestimation) |
| Load | Heavier is more accurate. Underestimation clusters at 60-65% 1RM | Halperin (conclusion); Ruiz-Alias 2025; Hackett 2017. Against: Mansfield 2020 (%1RM did not change the estimate) |
| Set number | Later sets slightly more accurate | Halperin (β -0.07); Mansfield 2020; Hackett 2018; Remmert 2023a. Against: Refalo 2024 (set 1 = set 2) |
| Exercise | Bench or upper body is usually more accurate than squat or leg press. The meta-analysis is inconclusive | For: Helms 2017a; Hermann 2025; Hackett 2017; Wiedenmann 2026; Russo 2025. Against: Halperin (-0.58, CI -2.32 to 1.16); Remmert 2023a (no difference on machines) |
| Training experience | Mostly no effect | No effect: Halperin; Zourdos 2021; Hackett 2017; Remmert 2023a; Refalo 2024; Droguett 2026. Effect: Steele 2017 (trend); Ormsbee 2019 (only at a 1RM) |
| Sex | Small effect: women underestimated at 65% bench | Ruiz-Alias 2025; Hackett 2017 (leg press). Refalo 2024: none |
| Direction | Submaximal sets: underprediction of 0.2-2 reps. At a true max: ratings of 9.35-9.86 | Halperin; Armes; Steele; Refalo; Helms 2017b; Ormsbee 2019 |

### Inferences

- **The top set is the best-rated set in the session.** It has few reps, a heavy load (about 84% 1RM) and ends about 2 reps from failure. The comparable data give about 0.5-1 rep of absolute error: Refalo 0.65 at 75% bench, and Hackett 2017 at about 1 rep for 0-5 reps to failure. As the lift's first work set, it carries the small first-set penalty.
- **Squat and deadlift ratings deserve less trust than bench and press ratings.** No barbell deadlift study tested RIR against true failure.
- **A logged "8" more often hides a 7 than a 9.** This confirms the statement in `templates/progression-tracks.md` §1. The exception is at the top of the scale: a true max is often logged as 9.5. That supports keeping 9.5 as a miss.
- **The engine's 0.5-RPE bins are finer than the error** (about 0.65-1 rep, which is about 0.65-1 RPE). A coarser three-level rating loses little real information (KQ5).
- **3-day vs 5-6-day weeks.** No study rated a lift done second or third in a session, after other heavy lifts, which is the merged-session case in 3-day weeks. "Later sets are rated better" refers to sets of the same exercise, not to later exercises. Treat ratings of later lifts in merged sessions as at least as noisy as first-lift ratings.

### Gaps

- Russo 2025 full text not read. Two related Évora-group papers (Casanova et al. 2025, "Accuracy in predicting repetitions in reserve during resistance training"; Ferrari et al. 2026 preprint, doi:10.21203/rs.3.rs-8899476/v1) were found but not read.
- No study checked barbell deadlift RIR against true failure. Lovegrove 2022 measured how reliably lifters chose a load, not accuracy against failure.
- Every study had the rating given during or right after the set. No study tested a rating typed into an app after rest.
- Halperin's load moderator appears in its conclusions, but no coefficient is in the abstract.

---

## KQ2. Does accuracy improve with practice or feedback? Which calibration methods have evidence?

### Takeaway

- The evidence is mixed.
- Taking sets to failure while predicting, repeated over several sessions, improved accuracy in one 6-session study: mean absolute error fell by 0.4-2.3 reps, significantly from session 4. It also improved over 8 weeks in another study (Hermann 2025), more for the bench than the squat.
- A 6-week bench study with 18 failure sets found no change in absolute error. One extra session changes little. Knowing the load does not help.
- Individual velocity profiles beat subjective estimates mainly in early sets and at lighter loads. They need sets to failure to build, and they failed in one deadlift variant.
- Practitioners advise occasional sets to failure on safe exercises, and assuming about one rep of underprediction.

### Cited findings

- **[Evidence] Wiedenmann et al. 2026** (full text, [PMC13499321](https://pmc.ncbi.nlm.nih.gov/articles/PMC13499321/)). One familiarisation session, then 6 sessions over 6 weeks. Each session: 3 sets each of bench and leg press at random 75-85% 1RM, calling 4 and 2 RIR, then continuing to concentric failure. Participants "received no additional explicit feedback regarding their performance or estimation error".
  - Younger adults, mean absolute error from session 1 to session 6: bench 1.6 → 0.8 reps (2 RIR) and 2.4 → 1.5 (4 RIR); leg press 2.9 → 1.4 (2 RIR) and 4.6 → 2.3 (4 RIR).
  - Older adults: bench 1.2 → 0.8 and 2.1 → 1.5; leg press 2.5 → 1.7 and 4.6 → 2.5.
  - Error was significantly lower than session 1 from session 4 onward. Age made no difference.
  - The authors' explanation: reaching failure gave "intrinsic, self-generated information about estimation error".
  - Limits: small sample, mostly women in the younger group, no barbell squat or deadlift.
- **[Evidence] Remmert et al. 2023b**, *Percept Mot Skills* 130(5):2139-60, [PubMed 37436724](https://pubmed.ncbi.nlm.nih.gov/37436724/). 9 trained men, bench 3 times a week for 6 weeks, last set of each session to failure, calling 4 and 1 RIR. No significant change in absolute error. The raw error drifted toward underestimation: -0.077 reps per session, and -0.404 per extra rep in the set. The authors declared that they work as coaches and writers. Abstract.
- **[Evidence] Hermann et al. 2025** (above): accuracy improved over 8 weeks, especially for the bench. Abstract only.
- **[Evidence] Hackett, Cobley & Halaki 2018**, *JSCR* 32(5):1352-59, [PubMed 29337829](https://pubmed.ncbi.nlm.nih.gov/29337829/). 48 recreational lifters, 3 x 10 (chest press at 70%, leg press at 80%), each set continued to failure. Two sessions 48 h apart. Abstract.
  - Error in set 1 vs set 3, session 1: chest press 2.0 vs 0.6 reps; leg press 3.1 vs 1.6.
  - Session 2: no change for the chest press; leg press set 1 fell from 3.1 to 1.9. "Improvement in the accuracy of ERF after a single training bout is minimal."
  - Estimated reps to failure tracked actual reps (r = 0.59-0.87) much better than Borg RPE did (r = 0.32 to -0.42).
- **[Evidence] Helms 2017a** (above). Squat 2 @ 8 accuracy moved from -0.46 ± 0.69 RPE in week 1 to 0.08 ± 0.29 in week 3. The authors: squat power-type sets "may take 3 weeks to reach peak accuracy". Abstract.
- **[Evidence] Mansfield 2020** (above). Telling lifters the load did not improve accuracy. Abstract.
- **[Evidence] Refalo 2024** (above). Accuracy was equivalent in session 1 and session 2. Abstract.
- **Velocity as an objective check** (all with linear transducers, not phone apps; abstracts):
  - **[Evidence] Morán-Navarro et al. 2019**, *JSCR* 33(6):1496-1504, [PubMed 29944141](https://pubmed.ncbi.nlm.nih.gov/29944141/). 30 men, 4 exercises at 65/75/85% to failure. The velocity at which a set stops with 2, 4, 6 or 8 RIR was similar across loads, with high reliability (CV 4.4-8.0%), and did not differ by training level.
  - **[Evidence] Hickmott, Butcher & Chilibeck 2024**, *JSCR* 38(7):1206-12, [PubMed 38595310](https://pubmed.ncbi.nlm.nih.gov/38595310/). 18 M and 18 F, bench, 3 sets to failure at 75, 80 and 85%. An individual last-rep velocity-RIR profile was more accurate than subjective 4- and 2-RIR calls in sets 1-2 and at 75-80% 1RM.
  - **[Evidence] Jukic, Prnjak, Helms & McGuigan 2024**, *Physiol Rep* 12:e15955, [PMC10901726](https://pmc.ncbi.nlm.nih.gov/articles/PMC10901726/). 46 trained, free-weight back squat. Individual RIR-velocity relationships from session 1 predicted RIR in session 2 with mean error under 2 reps at any load. General (group) relationships did not.
  - **[Evidence] Chen et al. 2026**, *JSCR* 40(11):1335-41, [PubMed 42328880](https://pubmed.ncbi.nlm.nih.gov/42328880/). 19 well-trained men, hexagonal-bar deadlift, 4 sets to failure at 65% or 85%. No condition met all three criteria: median absolute error ≤ 2 reps, ≥ 75% of estimates acceptable, and ≥ 75% probability that the target velocity occurred. Accuracy depended on load, model and set number.
- **[Practitioner] Stronger By Science**, Pak Androulakis-Korakakis, ["Reps in reserve"](https://www.strongerbyscience.com/reps-in-reserve) (no date on the page; read 2026-11-06).
  - "Assume that you may be underpredicting RIR by approximately one repetition."
  - Do an extra rep and reassess.
  - Safely take the last set of some exercises to failure while predicting, to calibrate each exercise. Do not chase reps on squats without a spotter.
  - "Mostly opting for sets below 12 repetitions may also make your ability to predict RIR better."
- **[Practitioner] Barbell Medicine**, Hassan Mansour, ["What is RPE in Lifting?"](https://www.barbellmedicine.com/blog/autoregulation-and-rpe-part-i/) (updated 22 Jun 2024; read).
  - "Trainees can implement RPE to a reasonable degree of accuracy within the span of a few weeks." Early ratings may be "a little wide of the mark".
  - RPE charts give rough estimates only. Data from one rep range should not set loads for a very different one.
  - No calibration protocol is given.
- **[Practitioner] Wendler** (in `research/periodization-and-progression.md` KQ2): 5/3/1 plus sets are AMRAP "but not to grinding failure".

### Inferences

- **One calibration method has some evidence:** predicting during sets that end at or very near failure, repeated over several sessions. The gains were largest where the error was largest (leg press, 4 RIR). They were small for bench at 2 RIR (0.4-0.8 reps).
- **Logging RPE without ever checking it against failure has no evidence of improving accuracy.** A rating that is never checked cannot be calibrated.
- **A calibration set must end close to failure.** That is where the prediction error is smallest (KQ1), so it gives the cleanest reference.
- **Velocity does not save the rep-outs.** An individual profile is built from sets to failure first (Jukic 2024, Hickmott 2024), and the lifter would need a device.
- **3-day vs 5-6-day weeks.** Calibration is a per-lift event. Every 3- to 6-day week holds one H exposure per lift, so "one rep-out per lift every second H" is the same count in any week type. What changes is where it can go: it needs a fresh lift (KQ5).

### Gaps

- No RCT compared explicit feedback (telling the lifter the error) with none.
- No study tested how often to calibrate to keep accuracy.
- No study tested whether a failure set on a machine improves barbell ratings.
- Hermann 2025's accuracy numbers were not read.

---

## KQ3. Progression without RPE: rep-based rules, e1RM from rep-outs, velocity apps, fixed rules

### Takeaway

- Three families can replace ratings or back them up.
- **Rep-based rules.** AMRAP or "plus" sets (5/3/1, GZCLP, nSuns) and APRE set the next load from reps done at a known load. APRE has the only controlled evidence: Mann 2010 (foundational), and the APRE subgroup of Zhang 2021 (ES 0.78).
- **e1RM from a rep-out.** The formulas agree within a few percent at 4-10 reps. Individuals differ by about ±2.5 reps at 80% 1RM, so a person's own data beat a table. Keep rep-outs to 10 reps or fewer.
- **Phone velocity apps.** Qwik VBT matched a linear transducer in powerlifts. Metric VBT and MyLift did not, except Metric on the bench. 1RM estimates from load-velocity profiles run high: +3.7% on average, SEE about 9.8%.
- For a lifter who will not type numbers, the rep count he already logs is the cheapest signal.

### Cited findings

**Rep-based programs**

- **[Practitioner, program authors] 5/3/1, GZCLP, nSuns, BBR**, as recorded in `research/periodization-and-progression.md` KQ2 and `research/splits-and-named-programs.md` KQ2-KQ3 (row 43):
  - 5/3/1: plus sets "not to grinding failure". If you cannot get 5 reps at 95% of the training max, the training max is too high. Never raise the training max after a miss.
  - GZCLP: last T1 set is AMRAP. The stage changes when the base reps are not reached.
  - nSuns raises the training max by reps on the "1+" set: 0-1 reps +0; 2-3 reps +5 lb; 4-5 reps +5-10 lb; 6+ reps +10-15 lb.
  - BBR: +5/10 lb if the AMRAP passes 10 reps.
- **[Practitioner, program author] APRE**, Bryan Mann, ["Understanding APRE, Part 1"](https://training-conditioning.com/article/understanding-apre-part-1/), *Training & Conditioning*, 3 Nov 2017. Page read; the chart is printed as a grid, and the fetch tool inferred a few row alignments.
  - 6RM version: set 1 = 10 reps at 50% of the 6RM; set 2 = 6 at 75%; set 3 = max reps at the 6RM; set 4 = max reps at an adjusted load.
  - "The number of repetitions in set four determines the starting weight for the subsequent training session."
  - 6RM chart (set-4 reps → load change): 0-2 → -5 to -10 lb; 3-4 → 0 to -5; 5-7 → no change; 8-12 → +5 to +10; 13+ → +10 to +15.
  - 3RM chart: 1-2 → -5 to -10; 3-4 → no change; 5-6 → +5 to +10; 7+ → +10 to +15.
- **[Evidence, foundational] Mann, Thyfault, Ivey & Sayers 2010**, *JSCR* 24(7):1718-23, [PubMed 20543732](https://pubmed.ncbi.nlm.nih.gov/20543732/). 23 Division I football players (2.65 ± 0.8 training years), 6 weeks, APRE (n = 12) vs linear periodization (n = 11). S only. Abstract.
  - Bench 1RM: +93.4 ± 103 N vs -0.40 ± 49.6 N (p = 0.02).
  - Estimated squat 1RM: +192.7 ± 199 N vs +37.2 ± 155 N (p = 0.05).
  - Reps at 225 lb: +3.17 vs -0.09.

**e1RM formulas and rep-max tables**

| Reps to failure | Epley, 1/(1 + r/30) | Brzycki, (37 - r)/36 | Tuchscherer chart, RPE 10 column | NSCA textbook table (Nuzzo Table 1) |
|---|---|---|---|---|
| 4 | 88.2% | 91.7% | 89.2% | 90% |
| 6 | 83.3% | 86.1% | 83.7% | 85% |
| 8 | 78.9% | 80.6% | 78.6% | 80% |
| 10 | 75.0% | 75.0% | 73.9% | 75% |

- Formula values are computed here from the published formulas. The Tuchscherer values are the reproduced chart already used in `templates/progression-tracks.md` (FitnessVolt reproduction, re-read 2026-11-06; the RPE 8 column gives 4 reps = 83.7% and 6 reps = 78.6%) [Convention, foundational, 2009].
- In the 4-8-rep zone, one rep at fixed effort is worth about 2.7-2.9% of load by Epley, 3.1-3.4% by Brzycki and 3.1-3.4% on the Tuchscherer chart. On Nuzzo's bench estimates (below) it is about 2% (90% → about 4 reps, 80% → about 9).
- **[Evidence, foundational] LeSuer, McCormick, Mayhew et al. 1997**, *JSCR* 11(4):211-213. Seven equations, 67 untrained college students (40 M, 27 F), bench, squat and deadlift. Predicted and actual 1RM correlated at r > 0.95. All equations underestimated the deadlift. Secondary sources disagree on which equation did best for the squat (Epley or Wathen). **Secondary only**; not in PubMed, not read.
- **[Evidence, foundational] Reynolds, Gordon & Robergs 2006**, *JSCR* 20(3):584-92, [PubMed 16937972](https://pubmed.ncbi.nlm.nih.gov/16937972/). Abstract.
  - 70 subjects (34 M, 36 F, aged 18-69), bench (chest press) and plate-loaded leg press, tested at 1, 5, 10 and 20RM.
  - Load fell nonlinearly as reps rose. The 5RM predicted best. R² for 5/10/20RM: chest press 0.993/0.976/0.955; leg press 0.974/0.933/0.915.
  - Chest press 1RM = 1.1307 x 5RM + 0.6999 kg (SEE 2.98 kg). Leg press SEE 16.16 kg.
  - "No more than 10 repetitions should be used in linear equations to estimate 1RM."
- **[Evidence] Roberts et al. 2025**, *JSCR* 39(2):e96-e105, [PubMed 39495260](https://pubmed.ncbi.nlm.nih.gov/39495260/). 18 published equations cross-validated against reps to failure at 80% 1RM: 43 recreationally active men on the leg extension, 39 of them on the bench. The best equations still needed their constant error subtracted. The authors recommend loads that give 4-10 reps to failure. Abstract.
- **[Evidence] Nuzzo, Pinto, Nosaka & Steele 2024**, *Sports Med* 54(2):303-321, [PMC10933212](https://pmc.ncbi.nlm.nih.gov/articles/PMC10933212/). Meta-regression of 952 reps-to-failure tests: 7,289 people, 269 studies. Full text (the tables are figures, so the values below are from the text). Two authors previously worked for Vitruvian, an equipment maker (declared).
  - Between-person SD of reps: 2.51 at 80% 1RM, 4.36 at 60%.
  - Sex, age and training status changed the relationship little.
  - Bench: about 4, 9 and 14 reps at 90, 80 and 70%. Leg press: about 9, 13 and 19. General model: about 5 reps at 90% and 15 at 70%.
- **[Practitioner] Barbell Medicine**: compute e1RM from the most accurate set (`research/periodization-and-progression.md` KQ7). Mansour 2024 (above): charts are rough, and one rep range should not set loads for a very different one.

**Phone velocity apps** (abstracts)

| Study | App(s) | Sample and lifts | Result |
|---|---|---|---|
| **[Evidence] Renner, Mitter & Baca 2024**, *PLoS One* 19:e0313919, [PMC11575817](https://pmc.ncbi.nlm.nih.gov/articles/PMC11575817/) | Qwik VBT, Metric VBT, MyLift (vs RepOne transducer and Vicon) | 20 competitive powerlifters (14 M, 6 F); squat, bench, deadlift up to 90% of competition best; 589 reps | Qwik VBT and RepOne were valid: standardized mean bias 0-0.21, RMSE 0.01-0.04 m/s. Metric and MyLift were weaker (SMB -0.28 to 0.14, RMSE 0.04-0.14 m/s), except Metric on the bench (SMB 0.07, RMSE 0.04). Metric missed 52 reps and MyLift missed 175 |
| **[Evidence] Trowell et al. 2024**, *PeerJ* 12:e17789, [PMC11283170](https://pmc.ncbi.nlm.nih.gov/articles/PMC11283170/) | Metric VBT (vs Vicon), 5 camera angles | 24 participants; squat and bench | Detected more than 95% of reps. Mean-velocity limits of agreement for squats 0.03 to 0.25 m/s; "significant accuracy concerns". Useful for counting reps. The authors' university has a non-financial link with the developer (declared). The abstract's bench velocity limits repeat the range-of-motion figures, an apparent typo; not used |
| **[Evidence] Grossi et al. 2026**, *J Funct Morphol Kinesiol* 11(2):197, [PubMed 42200903](https://pubmed.ncbi.nlm.nih.gov/42200903/) | Metric VBT vs Vitruve transducer | 18 trained men; Smith-machine bench 1RM | Mean velocity ICC 0.612, limits of agreement -0.07 to 0.04 m/s. Did "not meet the reliability criteria" |
| **[Evidence] Balsalobre-Fernández et al. 2018**, *J Sports Sci* 36(1):64-70, [PubMed 28097928](https://pubmed.ncbi.nlm.nih.gov/28097928/) | PowerLift (now My Lift) vs transducer | 10 powerlifters; bench at 75-100% | r = 0.94 (SEE 0.028 m/s), ICC 0.965. App-estimated 1RM r = 0.98, mean difference 5.5 ± 9.6 kg |
| **[Evidence] Balsalobre-Fernández et al. 2023**, *JSCR* 37(12):e640-e645, [PubMed 38015739](https://pubmed.ncbi.nlm.nih.gov/38015739/) | My Jump Lab (AI) vs GymAware | 27 sport-science students; bench at 50% and 75% | r 0.90-0.92; bias -0.010 and -0.026 m/s. CV app 8.17% and 13.55% vs transducer 6.52% and 12.10% |

- **[Evidence] Greig et al. 2023**, *Sports Med* 53(9):1693-1708, [PMC10432349](https://pmc.ncbi.nlm.nih.gov/articles/PMC10432349/). Individual-participant-data meta-analysis: 26 studies (137 models); 20 studies and 434 participants pooled. Abstract.
  - 1RM from load-velocity profiles: SEE 9.8% (7.4-12.2%).
  - Systematic overestimation: 4.5 kg (1.5-7.4), or 3.7% of 1RM (0.5-6.9%).
  - Using more than two loads, or individual vs group velocity thresholds, changed little.
- **[Evidence] LeMense et al. 2024**, *JSCR* 38(3):612-619, [PubMed 38416447](https://pubmed.ncbi.nlm.nih.gov/38416447/). The back-squat minimum-velocity-threshold method overestimated 1RM (ES 0.53, CI 0.19-0.87; 4 studies, 71 subjects): "not a viable option". Abstract.
- **[Vendor] Hevy.**
  - RPE is entered per set during a live workout after turning on "RPE Tracking" (Profile → Settings → Workouts).
  - The picker accepts values from 6 to 10. Sets may be left blank.
  - Hevy defines 10 = "couldn't do any more reps", 9 = one more, 8 = two more, 7 = three more, 6 = four more. It describes 7.5, 8.5 and 9.5 as "maybe" values.
  - Sources: [Hevy, how to calculate RPE](https://www.hevyapp.com/features/how-to-calculate-rpe/) and [Hevy RPE scale](https://www.hevyapp.com/rpe-scale/), read 2026-11-06.

### Inferences

**What each option costs and gives, per H exposure**

| Method | What the lifter does | Information gained | Error | Burden |
|---|---|---|---|---|
| One RPE tap on the top set | One tap, one choice from 6-10 | Effort at the target | About 0.5-1 rep (KQ1) | Lowest that still measures effort |
| Three-level tap (7 / 8 / 9) | Same tap, three choices | Effort in three bins | Same; the bins are no coarser than the error | Lowest |
| Reps above target, no tap | Edit the rep count when he does more than 4 (he already does: 105 x 6, 155 x 5, 135 x 5) | A lower bound on RIR at rep 4 | ±1 RPE (unknown end-of-set RIR) | None beyond the edit |
| Rep-out on the last back-off | Keep going to about RPE 9, edit the rep count | A calibration check | ±1-1.5 reps (fatigue, table) | One edited number every two weeks per lift |
| Phone velocity app | Phone on a stand every set, a second app; data do not reach Hevy | Bar speed | Qwik VBT good; Metric and MyLift weaker; 1RM estimates run +3.7% | High |
| Default "no rating = RPE 8" (status quo) | Nothing | No effort information; misses only | — | None |

- **The cheapest information already exists: reps.** Within one set, reps above target convert to RIR by arithmetic, not by a table: RIR at rep 4 = RIR at the end of the set + (reps - 4). A rep-max table is needed only to turn the surplus into load. In the 4-8-rep zone each rep is worth about 2-3.4% of load, so two surplus reps are worth about 4-7%. That is about the size of the existing big step: +10 lb on a 155-lb squat is 6.5%; +5 lb on a 110-lb bench is 4.5%; +5 lb on a 70-lb press is 7.1%.
- **The engine's e1RM already credits extra reps.** 105 x 6 @ 8 gives 105 x (1 + 8/30) = 133, against 126 for 4 @ 8. Only the §5 decision table ignores them.
- **Velocity apps are not a minimum-effort tool.** Only one app (Qwik VBT) matched a transducer in powerlifts. Data stay outside Hevy. Load-velocity 1RMs run high. Skip them unless the lifter wants one.
- **APRE is the closest evidence-backed version of "reps at a known load set the next load".** Its bands are 3-5 reps wide. That fits the ±1-rep measurement error better than the engine's 0.5-RPE bins do.

### Gaps

- LeSuer 1997 and Mayhew 1995 were not read. This pass found no peer-reviewed validation of Epley or Brzycki against a measured barbell squat or deadlift 1RM in trained lifters. A 2014 thesis (DiStasio) is cited by secondary sources at 2.7-3.1 kg squat error; not read.
- The APRE chart was read from the author's magazine article. A few row alignments were inferred.
- Not checked: whether Hevy pre-fills reps from the routine. If it does, a logged "4" may mean "did not edit" rather than "did 4".
- Not checked: whether Hevy's picker offers the half steps that its scale page describes.
- Qwik VBT between-day reliability and platform availability were not checked.

---

## KQ4. Outcomes: autoregulated vs fixed-percentage progression

### Takeaway

- **Strength.** Autoregulated loading is at least as good as fixed percentages. Pooled estimates run from no significant difference (Hickmott 2022, SMD 0.21) to a moderate edge in athletes (Zhang 2021, ES 0.64).
- The clearest wins come when the comparison group's loads did not follow strength. In Graham & Cleather 2021, the fixed group used percentages of the pre-test 1RM for all 12 weeks.
- Rep-based APRE ranks first in two syntheses, but it rests on few, small, short studies.
- **Hypertrophy.** No difference where it was measured (Helms 2018, muscle thickness).
- **The engine without ratings is not "fixed loading".** It still adds load after every non-miss. Losing ratings mainly costs the big steps and the early detection of slack.

### Cited findings

| Study | Design and population | Comparison | Strength (S) | Hypertrophy (H) | Read |
|---|---|---|---|---|---|
| **[Evidence] Helms et al. 2018**, *Front Physiol* 9:247, [PMC5877330](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5877330/) | 8 weeks, 21 trained men (RPE n = 10, %1RM n = 11), DUP squat and bench 3x/week | RPE-chosen loads vs %1RM | Squat +17.05 vs +13.91 kg; bench +10.70 vs +9.64 kg; not significant. Magnitude-based inference gave RPE a small edge | Muscle thickness rose similarly | Repo addendum (verified) |
| **[Evidence] Graham & Cleather 2021**, *JSCR* 35(9):2451-56, [accepted manuscript](https://research.stmarys.ac.uk/3067/3/Graham-Cleather-Autoregulation-Repetitions-in-Reserve.pdf), [PubMed 31009432](https://pubmed.ncbi.nlm.nih.gov/31009432/) | 12 weeks, 2x/week; 31 trained men (> 2 y; 15 AR, 16 FL); block periodization (3 x 10, 4 x 5, 3 x 3) | RIR targets (4, 3, 2, 1 per block; last block 2, 1, 0, max) vs fixed % of pre-test 1RM; volume matched | Front squat +11.7% vs +8.3% (p = 0.004, ηp² 0.255); back squat +10.8% vs +7.1% (p = 0.006, ηp² 0.233). The AR group trained heavier: front squat 83.2% vs 80.4% of pre-test 1RM. The authors credit the higher intensity. FL loads never updated | Not measured | Full text |
| **[Evidence, foundational] Mann et al. 2010** (KQ3) | 6 weeks; 23 D-I football players | APRE vs linear periodization | Bench +93 N vs -0.4 N; squat +193 N vs +37 N | Not measured | Abstract |
| **[Evidence] Shattock & Tee 2022**, *JSCR* 36(3):641-48, [PubMed 32058357](https://pubmed.ncbi.nlm.nih.gov/32058357/) | Randomised crossover, 2 x 6-week blocks; 20 amateur rugby players | Velocity targets vs RPE targets; volume matched | Squat +7.5% vs +3.5%; bench +7.7% vs +3.8%. Velocity "likely" better for the squat (3.7%) and "possibly" for the bench (magnitude-based decisions) | Not measured | Abstract |
| **[Evidence] Zhang et al. 2021**, *Front Physiol* 12:651112, [PMC7994759](https://pmc.ncbi.nlm.nih.gov/articles/PMC7994759/) | Meta-analysis: 8 studies (2010-2020), 166 athletes, 5-10 weeks | APRE, RPE and VBT vs fixed loading | Overall ES 0.64 (P < 0.001, I² 0%). APRE ES 0.78. ≤ 8 weeks ES 0.87 vs 8-10 weeks 0.32. The squat and bench subgroup "effect sizes" of 4.64 and 3.21 look like kg mean differences | Not pooled | Abstract |
| **[Evidence] Hickmott et al. 2022**, *Sports Med Open* 8:9, [PMC8762534](https://pmc.ncbi.nlm.nih.gov/articles/PMC8762534/) | Meta-analysis, 15 studies in trained people | Load autoregulation (RPE or velocity) vs %1RM | MD 2.07 kg (-0.32 to 4.46), SMD 0.21, not significant | Velocity-loss thresholds above 25% grew more cross-sectional area | Repo addendum (verified) |
| **[Evidence] Larsen et al. 2021**, *PeerJ* 9:e10663, [PMC7810043](https://pmc.ncbi.nlm.nih.gov/articles/PMC7810043/) | Systematic review: 14 studies, 30 groups, 356 participants; no pooling | All autoregulation methods | Every autoregulation protocol raised 1RM (small to large ES) | — | Abstract |
| **[Evidence] Huang et al. 2025**, *J Exerc Sci Fit* 23(4):360-369, [PMC12336695](https://pmc.ncbi.nlm.nih.gov/articles/PMC12336695/) | Network meta-analysis | APRE, RPE, velocity, %-based | Probability of ranking best (SUCRA). Squat: APRE 93.0%, RPE 66.8%, velocity 27.0%, %-based 13.2%; no moderate or large effects. Bench: APRE 97.1%, velocity 57.1%, RPE 29.9%, %-based 15.9%. Bench, %-based vs APRE: SMD -0.83 (-1.22 to -0.44) | — | Abstract; the repo already rates it weak |

### Inferences

- **The evidence does not show that ratings themselves cause better gains.** It shows that loads which follow current ability beat loads which do not. Ratings, rep-outs (APRE) and velocity are three ways to make loads follow ability.
- **Without ratings, the engine follows ability in one direction only.** It adds 5 lb after each non-miss and catches overshoot through misses. It cannot speed up.
- **For this lifter, too slow is the likely error.** He is regaining after an 18-month layoff, and he has already chosen loads above plan: squat 155 x 5 against a planned 135 x 4; press 70 x 4 against 60; bench 105 x 6 on a 4-rep target (`data/track-log.md`). Whatever replaces the rating must be able to trigger the big step.
- **Hypertrophy:** no difference is expected either way. The choice affects only the pace of strength gain.
- **3-day vs 5-6-day weeks:** no difference. Every trial trained each lift 2-3 times a week, which matches the program's one H and one V exposure per lift.

### Gaps

- No trial compared RPE-based top sets with rep-based (AMRAP) top sets head to head in trained lifters.
- No trial tested any autoregulation method in lifters returning from a layoff.
- In Graham & Cleather the fixed group used the pre-test 1RM for all 12 weeks. The gap may shrink against a percentage program that re-tests.

---

## KQ5. Applied (inference): the smallest effort input that keeps the engine working

Everything in this section is inference from KQ1-KQ4. No study tested these rules.

### Takeaway

- The best minimum input is one rating, on the top set only. Three values are enough: 7 (easy), 8 (on target), 9 (hard).
- When there is no rating, the engine should read the reps:
  - Credit reps above the target by subtraction.
  - Assume an unrated set ended at about RPE 9.
  - Treat an unrated set of exactly 4 as RPE 8, for at most two H exposures in a row on a lift.
- Check the defaults with a rep-out on the **last back-off set**. While ratings are missing, do it every second H exposure per lift. Once ratings return, do it once per block.

### 5.1 Why one rating, on the top set

- The top set is the set the engine uses. It is also the best-rated set: few reps, heavy, near failure (KQ1).
- Back-off ratings change nothing in the track (§5: "back-off performance never changes the track"), so asking for them adds burden without information.
- Six taps a week covers every decision: one per lift per H exposure. That count is the same in a 3-day week (two per Full session) and a 6-day week (one or two per split session).

### 5.2 A three-level tap

| Tap (Hevy value) | Hevy's own wording | Engine bin (§5) |
|---|---|---|
| 7: easy | "could have done three more reps" | ≤ 7: big step |
| 8: on target | "could have done two more reps" | 7.5-8: step (bench and press: every second one) |
| 9: hard | "could have done one more rep" | 8.5-9: hold |
| 10: nothing left (or a missed rep) | "couldn't do any more reps" | ≥ 9.5: miss |

- The engine loses only the half steps. Those are smaller than the measured error (about 0.65-1 rep), so little real information is lost.
- Hackett 2012 and 2018 found that "reps left" estimates track true reps to failure better than Borg-style exertion ratings. Hevy's wording is in reps left, which suits this.

### 5.3 Crediting reps above the target

**Rule A: a rated top set.** Effective RPE at the target = logged RPE - (reps done - rep target). Use the effective RPE in the §5 table. This is within-set arithmetic. The only uncertainty is the rating itself (about 0.5-1 RPE).

| Logged (4-rep target) | Effective RPE at rep 4 | Decision |
|---|---|---|
| 4 @ 8 | 8 | Step (unchanged) |
| 5 @ 8 | 7 | Big step |
| 6 @ 8 | 6 | Big step (the 27 Oct bench case) |
| 5 @ 9 | 8 | Step |
| 6 @ 9 | 7 | Big step |
| 5 @ 10 | 9 | **Hold, not a miss** (four reps were made at RPE 9; the current table scores this as a miss) |
| 6 @ 10 | 8 | Step |
| 7 @ 8 or 8 @ 9 | 5 | Re-anchor (5.4) |

**Rule B: an unrated top set.** Assume the set ended at about RPE 9 (one rep left). Effective RPE at rep 4 = 9 - (reps - 4). The plausible range assumes he really stopped somewhere between RPE 8 and 10.

| Reps logged, no RPE | Assumed RPE at rep 4 | Plausible range | Decision |
|---|---|---|---|
| ≤ 3 | — | — | Miss (unchanged) |
| 4 | No information: treat as 8 | 6-10 | Step (unchanged); count one "unrated" exposure (5.5) |
| 5 | 8 | 7-9 | Step |
| 6 | 7 | 6-8 | Big step |
| 7 | 6 | 5-7 | Big step |
| 8 or more | ≤ 5 | ≤ 6 | Re-anchor (5.4) |

Why assume the set ended at 9 rather than 8:
- Lifters underpredict by about one rep (KQ1). A lifter who stops "with a rep or two left" usually has 2-3 left. Assuming one left under-credits him on average, which is the conservative error.
- It makes an unrated 5-rep set equal to a 4 @ 8 at the same load. One extra rep never earns more than the normal step; two extra reps earn the big step.
- The rule gives the same answers if the assumed end point is anywhere from 8.5 to 9, because §5 already lumps 7.5 with 8.
- Cost if he actually went to failure: "6 reps → big step" is one step too much (5-10 lb). The next exposure's hold or miss rule catches it.

Merged sessions (3-day weeks): Rules A and B apply unchanged. The existing rule stays: a later lift at 4 @ 9.5 is a hold, not a miss.

### 5.4 Re-anchoring after a large surplus (effective RPE ≤ 5)

- Next load = e1RM / 1.2, rounded down to 5 lb.
- e1RM is the engine's formula: load x (1 + (reps + RIR)/30), where RIR = 10 - logged RPE, or 1 if the set is unrated.
- Never less than the big step. Never more than +10% of the current load. The cap guards against a rating error.
- Examples:
  - Bench 105 x 6 @ 8: e1RM 133, and 133 / 1.2 = 110.8 → 110. Same as the hand amendment of 27 Oct.
  - Squat 155 x 8 @ 8: e1RM 206.7, and 206.7 / 1.2 = 172 → 170 (+15). The +10% cap would allow up to 170.
- The divisor 1.2 is the engine's own Epley-style value for 4 @ 8 (a 6-rep effort). It is a convention, not a tested value.

### 5.5 The calibration rep-out

**Which set.** The last back-off of the H exposure (top-set load x 0.93), not the top set. Reasons:
- The decision set stays a 4-rep set, and its e1RM series stays comparable.
- Later sets are rated slightly better (Halperin 2022; Hackett 2018; Mansfield 2020).
- The load is lower, so a grind is less risky.
- The fatigue state is about the same each time, so this set's count can be compared from exposure to exposure.

**How.**
- After rep 4, keep going until one more rep would be a grind (about RPE 9). Stop at 10 reps at most: Reynolds 2006 and Roberts 2025 support e1RM estimates only up to about 10 reps.
- Squat and bench inside a rack with the safeties set.
- Deadlift: stop at the first rep where back position or bar path changes.
- Never take squat or deadlift to failure without safeties (Stronger By Science's caution, KQ2).
- Log the reps. Tap a rating only if he is willing.

**What to expect.** The table below uses the Tuchscherer chart plus a 5% fatigue drop by the last back-off (RTS's "fairly average" figure; both are conventions, `research/periodization-and-progression.md` KQ2).

| True top-set RPE at 4 reps | Top set %1RM | Back-off %1RM (x 0.93) | Reps to failure, fresh | Reps to failure after 5% fatigue | Expected rep-out to about RPE 9 |
|---|---|---|---|---|---|
| 9 | 86.3 | 80.3 | about 7.3 | about 5.7 | about 4.7 |
| 8 | 83.7 | 77.8 | about 8.3 | about 6.7 | about 5.7 |
| 7 | 81.1 | 75.4 | about 9.3 | about 7.7 | about 6.7 |
| 6 | 78.6 | 73.1 | about 10.3 | about 8.7 | about 7.7 |

Each point of top-set RPE moves the rep-out by about one rep. The noise is about ±1 rep: RTS's fatigue tiers (3-7%) shift it by about ±0.7 rep, and the stopping judgment by about ±0.5-1. People also differ (SD 2.51 reps at 80% 1RM, Nuzzo 2024), and Nuzzo's bench data sit about one rep above the chart. So the first two rep-outs on each lift become that lift's own baseline. After that, judge each rep-out against his own numbers, not the table.

**How to read it.**

| Rep-out reps (to about RPE 9) | Read the top set as | Decision for an unrated top set |
|---|---|---|
| ≤ 4 | RPE 9 or harder, or high fatigue | Hold (not a miss) |
| 5-7 | About RPE 8 | Normal rule |
| ≥ 8 | RPE 7 or easier | Big step |

- **For an unrated top set, the rep-out decides.**
- **For a rated top set, log both.** If they disagree by 2 or more reps on two exposures of the same lift, tell the lifter which way his ratings drift. This is the only feedback the KQ2 evidence supports: a check against near-failure performance.

**How often, by week type.**

| | 3-day weeks (merged Full sessions) | 5-6-day weeks (split sessions) |
|---|---|---|
| While ratings are missing | Every second H exposure per lift (each week has one H per lift, so every two weeks), but **only on the first main lift of a session**. A later lift is pre-fatigued and its rep-out under-reads. Postpone its rep-out to the next session where it comes first, or to the next split week | Every second H exposure per lift, on the scheduled lift. Each lift's H is first or second in its session |
| Back-off sets available | 2 (deadlift 2); rep out on the 2nd | 3 (deadlift 2); rep out on the last |
| Cap | At most 2 rep-outs per session | At most 2 rep-outs per session |
| Once ratings return | One per lift per block (for example, the week before the deload) | Same |
| Skip | Deload weeks; the first exposure after a gap of 22 days or more (§8 caps the RPE); any lift with joint pain | Same |

- **Unrated 4s.** After two unrated 4-rep H exposures in a row on a lift, the next H exposure of that lift gets a rep-out. Its result overrides the "treat as 8" default for that exposure.
- **Cost.** One set per lift every two weeks goes to about RPE 9 instead of 7-8. Strength gains vary little across a wide range of proximity to failure (Robinson 2024, `research/frequency-volume-intensity-evidence.md` KQ4). The added fatigue is one set.

### 5.6 Double progression and V exposures without ratings

- **Row, pull-up and accessories** already progress on reps (every set at the top of the range). The "at RPE 8 or less" (row, pull-up) and "RPE 9 or less" (accessories) conditions cannot be checked when unrated. Keep treating unrated as meeting them. A grind shows up as missed reps on the next exposure.
- **The V "stale" rule** (last squat or bench V set at RPE ≤ 6 on two exposures in a row, §4) cannot fire without ratings. While ratings are missing, the rep-out does its job.

### 5.7 Worked examples from `data/track-log.md`

| Logged | Engine did | Under Rules A/B and 5.5 |
|---|---|---|
| 27 Oct bench 105 x 6 @ 8 | Hold (success 1 of 2), then amended by hand to a big step to 110 | Rule A: 6 @ 8 → effective 6 → big step to 110. Unrated it would be the same: 6 reps → 7 → big step |
| 29 Oct deadlift 145 x 4, no RPE | +5 to 150, treated as 8 | Same, and the deadlift counts 1 unrated exposure |
| 4 Nov press 70 x 4, no RPE (planned 60) | Success 1 of 2, step counter 1 | Same, press unrated count 1. If the next press H is again an unrated 4, the one after it gets a rep-out |
| 5 Nov squat 155 x 5, no RPE (planned 135), 19 days after the last barbell squat | Hold (§8, 15-21-day row) | Rule B: 5 reps → effective 8 → step, but §8 holds first. Same result |

### 5.8 Proposed changes to `templates/progression-tracks.md` (inference; for the guide author to accept or reject)

1. **§3 step 3 and §10.** Rate the top set only. One tap: 7 = easy (3 left), 8 = on target (2 left), 9 = hard (1 left), 10 = nothing left. Other sets need no rating. In Hevy, turn on Settings → Workouts → RPE Tracking.
2. **§3 step 3, optional.** If rep 4 was clearly easy, he may continue to 6 at most, stopping at the first slow rep. Log the actual reps. This gives rep data on days with no rating. The cap keeps the top set near RPE 9 or easier at a correctly planned load.
3. **§5, new first line.** Effective RPE at the rep target = logged RPE - (reps done - rep target). Use the effective RPE in the table (Rule A). This also turns 5 @ 10 into a hold instead of a miss.
4. **§5, new "no rating" rule** (Rule B table). Each unrated decision is flagged in `data/track-log.md` with the assumption used.
5. **§5, re-anchor** for an effective RPE ≤ 5 (5.4).
6. **New §5.1, calibration rep-out** (5.5): the set, the stop rule, the reading bands, the frequency by week type, the skip list.
7. **§4 stale rule.** When V sets are unrated, the rep-out replaces this rule.
8. **§1 accuracy paragraph.** Add three points. Near a true max, ratings run low (9.35-9.86 at a 1RM). Squat is rated less accurately than bench. Accuracy is best on heavy, low-rep sets near failure, which is why only the top set is rated.
9. **Tools** (not changed by this note). `tools/update_tracks.py` would need: Rule A and Rule B, an unrated-exposure counter per lift in `data/tracks.json`, and a "rep-out due" flag for the session brief. `templates/rotation.json` and the routine notes would carry the rating instruction and the rep-out set. Per CLAUDE.md, a template change also changes the JSON and pushes the routines again.

### Gaps

- Every rule above is untested. In particular:
  - The end-of-set RPE 9 assumption for unrated sets.
  - The rep-out bands. They rest on two conventions: the Tuchscherer chart and RTS's 5% fatigue figure.
  - The two-exposure limit on unrated 4s.
- No study tested a three-level effort input. The closest is the Feeling Scale: ratings after every rep predicted proximity to failure with R² 0.66-0.85 in 20 trained people (Emanuel, Rozen Smukas & Halperin 2021, *IJSPP* 16(1):135-144, [PubMed 32781441](https://pubmed.ncbi.nlm.nih.gov/32781441/); abstract). That is a different scale used in a different way.
- Whether the lifter edits the rep count every time he overshoots is unknown (KQ3 Gaps, Hevy pre-fill).

---

## Conflicts

| Question | One side | Other side | How this note handles it |
|---|---|---|---|
| Does training experience improve accuracy? | Steele 2017 (n = 141, a trend); Ormsbee 2019 (only at a 1RM: 9.86 vs 9.35) | Halperin 2022 (β -0.006); Zourdos 2021; Hackett 2017; Remmert 2023a; Refalo 2024; Droguett 2026 | Treat experience as no protection. The intermediate lifter's ratings get no extra trust |
| Can accuracy be trained? | Wiedenmann 2026 (error down 0.4-2.3 reps over 6 sessions, no explicit feedback); Hermann 2025 (8 weeks, bench more); Helms 2017a (squat, about 3 weeks) | Remmert 2023b (6 weeks, 18 failure sets, no change in absolute error); Hackett 2018 (minimal after one session); Refalo 2024 (session 1 = session 2) | Use repeated near-failure checks (the only method with any support), and judge the lifter against his own baseline |
| Upper vs lower body | Helms 2017a; Hermann 2025; Hackett 2017; Wiedenmann 2026; Russo 2025: bench or upper body is more accurate | Halperin 2022: -0.58 reps, CI -2.32 to 1.16 (inconclusive); Remmert 2023a: no difference between exercises (machines) | Trust squat and deadlift ratings less, and lean on rep-outs for them |
| Direction of error | Submaximal sets: underprediction by 0.2-2 reps (Halperin; Armes; Steele; Refalo; Wiedenmann) | At a true max, ratings of 9.35-9.86 (Helms 2017b; Ormsbee 2019); raw error moved from over- to under-prediction across sessions (Remmert 2023b) | A logged 8 is more likely a 7. A logged 9.5 is still treated as a miss |
| Does load matter? | Halperin 2022 (heavier is better); Ruiz-Alias 2025 (error only at 65%); Hackett 2017 | Mansfield 2020 (%1RM did not change the estimate); Hughes 2020 is retracted and not counted | Rate only the heaviest set |
| Velocity vs feel | Morán-Navarro 2019; Hickmott 2024; Jukic 2024: velocity at least as good, better in early sets and at lighter loads | Chen 2026: not accurate enough for the hex-bar deadlift. Phone apps vary (Renner 2024: Qwik good, Metric and MyLift weaker; Trowell 2024 and Grossi 2026: Metric poor) | Velocity is optional, not the minimum |
| Does autoregulation beat fixed loading for strength? | Zhang 2021 (ES 0.64; APRE 0.78); Graham & Cleather 2021; Mann 2010; Huang 2025 (rankings only) | Hickmott 2022 (SMD 0.21, not significant); Helms 2018 (not significant) | The benefit comes from loads that follow ability. The engine keeps that with reps and rep-outs. Hypertrophy: no difference in either camp |

---

## Relation to the existing notes (pointers, not edits)

- **`research/frequency-volume-intensity-evidence.md`, addendum, "Still unverified: Zourdos-attributed ±1 rep at 0-3 RIR".** Other papers now support the claim for heavy, low-rep sets: Hackett 2017 (about 1 rep at 0-5 reps to failure) and Refalo 2024 (0.65 ± 0.78 reps at 1 and 3 RIR). It does not hold for long sets: Zourdos 2021 found 2.05 reps of error at a called RPE 9 in 16-rep squat sets. The attribution to Zourdos 2016 remains wrong, as that addendum says.
- **`research/periodization-and-progression.md`, 2026-10-21 addendum (Halperin, Refalo, Remmert, Hermann, Hickmott 2024).** Every figure there matches the abstracts re-read here. This note adds Wiedenmann 2026, which partly conflicts with Remmert 2023b's "practice did not improve absolute accuracy". Both are recorded above.
- **`templates/progression-tracks.md` §1** ("a logged RPE 8 top set is more often a true RPE 7 than a 9"). Supported for submaximal sets. Near a max the direction reverses (Helms 2017b; Ormsbee 2019).
- **`research/coaching-check-ins.md` KQ2** ("the RPE cap decides on the day"). That rule needs a rating. Without one, the rep rules and rep-outs in KQ5 stand in for it.
- **Hughes, Peiffer & Scott 2020 is retracted.** No note in the repo cites it. Do not add it.
- **Russo 2025** is still unread in full (TLS failure and 503 today, as in the earlier addendum).

## Addendum 2026-11-06 (later): the lifter's Hevy pre-fills reps

The lifter believes Hevy pre-fills each set with the routine's reps (asked 6 Nov; not tested). The routines carry 4 reps on every top set and back-off; rows, pull-ups and accessories carry no reps, so this applies to the four top-set lifts only. Routine sets have no RPE field, so a logged RPE is always a deliberate entry.

Implications (inference):
- An unrated top set of exactly 4 may be a set left as pre-filled. KQ5 already treats it as "no information" (RPE 8 assumed, counted toward the rep-out). That stays.
- The error that matters is a missed rep left at 4: it would read as a success. Extra reps left at 4 only under-credit, which is the conservative error.
- A logged count other than 4 was typed, so reps above or below the target are reliable data.
- A back-off of exactly 4 when a rep-out was due is read as "not done" (KQ5), which fits a pre-filled set.
- Rule added to the program: change the reps whenever they differ from the plan, above all when a rep is missed (`templates/progression-tracks.md` §3; routine notes).
