# 00. Overview: what this guide is and the ten rules that matter

Last updated: 2026-10-21

## What this guide is

This guide turns the research notes in `research/` into a strength-and-hypertrophy program for an intermediate lifter in their 30s to 50s who trains with barbells, dumbbells, cables, and machines. The defining constraint is a schedule that changes week to week: some weeks allow 5-6 sessions, others only 3.

The program is therefore a **rotation of workouts, not a weekday-locked split**. You do the next workout in the sequence whenever you train. Loads and progression stay the same whether the week has 3 or 6 sessions; only the volume of accessory work changes. The concrete layouts live in `guide/03-flexible-scheduling.md` and `templates/`.

Every rule below points to the research note that supports it. Where the research notes flag a number as unverified, the guide flags it the same way.

## The ten rules

| # | Rule | The numbers | Why (evidence) |
|---|------|-------------|----------------|
| 1 | **Do enough weekly volume, then stop.** | Hypertrophy: 10-20 hard sets per muscle per week. 3-day week 8-12; 4-day week 10-14; 5-6-day week 14-20. Strength: 2-6 heavy direct sets per main lift per session. | Growth rises with weekly sets but flattens (Schoenfeld 2017: 10+ sets beat <5; Baz-Valle 2022: 12-20 sets optimal in trained men; Pelland 2025/26: +0.24% size per added weekly set, diminishing). Strength saturates far sooner. See `research/frequency-volume-intensity-evidence.md`, Q2. |
| 2 | **Train every muscle at least twice a week; frequency is how you distribute volume, not a stimulus in itself.** | Every muscle 2x in a 3-day week, 2-3x in a 5-6-day week. Main lifts 2x even in short weeks. | With volume equated, frequency adds nothing detectable for hypertrophy (Schoenfeld 2019; Hamarsland 2022; Pelland 2025/26) and a small, diminishing benefit for strength (Pelland). Per-session ceiling makes 2x necessary once weekly sets exceed ~10. Q1, Q7. |
| 3 | **Lift heavy for strength; any hard load builds muscle.** | Main-lift strength work: 3-6 reps at ~75-90% 1RM. Hypertrophy work: 6-12 reps, up to 15-20 on isolation, as long as sets are hard. | 1RM strength is load-specific (Lopez 2021; Schoenfeld 2017 JSCR); hypertrophy is similar from ~30-85% 1RM when sets approach failure. Q4. |
| 4 | **Stop 0-3 reps short of failure.** | 1-2 reps in reserve (RIR) on compounds by default; last set of an isolation exercise may go to failure. | Closer to failure helps hypertrophy modestly, not strength (Robinson 2024); failure vs not shows no overall difference (Grgic 2022) and a small strength edge for non-failure. RIR estimates are only accurate within ~0-3 reps of failure (Zourdos 2016). Q4. |
| 5 | **Rest long enough to keep your reps.** | 2-3 min on compounds; 60-90 s on isolation. | Rest >60 s gives a small hypertrophy benefit; no further benefit past ~90 s (Singer 2024). 3 min beat 1 min for strength in trained men (Schoenfeld 2016). Q5. |
| 6 | **Progress by rule, one track per lift.** | Accessories: double progression within a rep range. Main lifts: RPE-capped linear or wave scheme (top set + back-offs) with written stall rules. Each lift advances per exposure, regardless of which session it appeared in or how many days the week had. | Periodized, progressive loading beats static loading for strength by a small margin (Moesgaard 2022, ES 0.31; Williams 2017, ES 0.43, ~0.23 after bias correction). Exact rules: `templates/progression-tracks.md`; evidence: chapter 04. |
| 7 | **Deload every 4-6 weeks or when readiness says so, but keep lifting.** | Keep frequency, halve sets, keep some heavy-but-easy work (top sets at RPE 6-7). | A full week off mid-block cost lower-body strength with no hypertrophy benefit (Coleman 2024). Coaches converge on 5-7 days every 4-6 weeks, cutting volume and effort while keeping frequency (Bell 2022; Bell 2023 Delphi). Chapter 04. |
| 8 | **When the week shrinks, keep intensity and the main-lift progression; cut accessory and back-off volume first.** | A 3-day week at one-third to one-half of peak volume maintains and usually still builds. Never skip ahead in the rotation; resume with the missed workout. | Muscle and strength were maintained for 32 weeks on 1/3 or even 1/9 of prior volume in young adults when load was kept (Bickel 2011; Spiering 2021). Intensity is the maintenance lever. Q6, Q7; chapter 03. |
| 9 | **Recover on purpose.** | Cardio 2-3 sessions per week toward 150 min moderate; lift before cardio in the same session or separate by at least 3 h, 6 h where possible; prefer cycling or incline walking to running on heavy leg weeks. Sleep, bodyweight, and food are inputs to check before blaming the program. | Design spine item 8; details and sources in chapter 06. |
| 10 | **Track what you did, not how you felt about it.** | Per set: exercise, load, reps, RPE/RIR. Per session: bodyweight, sleep, 1-5 readiness. Per week: hard sets per muscle. Judge a block by the e1RM trend over 3-4 weeks, not by one session. | Logged e1RM and RIR-based RPE are practical, reliable monitoring tools (Helms 2020); single-session changes are mostly noise (Barbell Medicine). `research/periodization-and-progression.md`, Q7; chapter 07. |

Age flag: the maintenance data behind rule 8 come from adults aged 20-35. Adults aged 60-75 did not maintain on reduced doses in Bickel 2011, and Spiering 2021 suggests older adults need about 2 sessions and 2-3 sets per exercise. A lifter in their late 40s or 50s should plan short weeks at the one-half end of the range rather than one-third.

## Reading map

| Chapter | File | What it covers |
|---------|------|----------------|
| 01 | `guide/01-training-principles.md` | The science behind rules 1-5 and 8: volume, frequency, intensity, proximity to failure, rest, maintenance dose. Weekly set tables for 3-day vs 5-6-day weeks. Strength and hypertrophy separated. |
| 02 | `guide/02-program-structures.md` | Catalog of splits and named programs by days per week, with a "tolerates variable weeks?" verdict for each, and why this repository uses a rotation instead. |
| 03 | `guide/03-flexible-scheduling.md` | The rotation itself: how a 3-day week and a 6-day week run on the same program, what to cut, how to resume after a missed session. Owns the weekly layouts. |
| 04 | `guide/04-periodization-and-progression.md` | Periodization evidence, exact progression schemes, deload rules, mesocycle structure, plateaus, training age, and what to log. |
| 05 | `guide/05-exercise-selection.md` | Exercise selection and session design: which exercises cover which muscles, session order, substitutions. |
| 06 | `guide/06-recovery-nutrition-cardio.md` | Recovery, fatigue management, sleep, nutrition, and cardio: recovery between sessions, cardio placement, protein and energy intake. |
| 07 | `guide/07-tracking-and-apps.md` | Tracking and apps: what to log, how to compute e1RM, which apps support a rotation. |
| Templates | `templates/` | Concrete 3/4/5/6-day layouts with exercises, sets, reps, and `templates/progression-tracks.md` for the per-lift progression rules. |

Start with chapter 03 and a template if you want to train today; read 01 and 04 when you want to know why.

## Sources

- `research/frequency-volume-intensity-evidence.md`: Q1 (frequency), Q2 (weekly volume and per-session ceiling), Q4 (load and proximity to failure), Q5 (rest), Q6 (maintenance dose), Q7 (3-day vs 6-day redistribution).
- `research/periodization-and-progression.md`: Q1 (periodization evidence), Q2 (progression schemes), Q3 (deloads), Q7 (tracking).
- `research/flexible-frequency-programming.md`: KQ1 (rotation pattern), KQ3 (maintenance weeks), KQ6 (exposure-indexed progression).
- Key primary citations: Schoenfeld, Ogborn & Krieger 2017 (J Sports Sci); Baz-Valle et al. 2022 (J Hum Kinet, [PMC8884877](https://pmc.ncbi.nlm.nih.gov/articles/PMC8884877/)); Pelland et al. 2025/26 (Sports Med, [SportRxiv 460](https://sportrxiv.org/index.php/server/preprint/view/460)); Schoenfeld, Grgic & Krieger 2019 (J Sports Sci); Hamarsland et al. 2022 (Front Physiol, [PMC8766679](https://pmc.ncbi.nlm.nih.gov/articles/PMC8766679)); Lopez et al. 2021 (MSSE); Robinson et al. 2024 (Sports Med); Grgic et al. 2022 (J Sport Health Sci); Singer et al. 2024 (Front Sports Act Living); Schoenfeld et al. 2016 (JSCR); Bickel, Cross & Bamman 2011 (MSSE, [PubMed 21131862](https://pubmed.ncbi.nlm.nih.gov/21131862/)); Spiering et al. 2021 (JSCR, [PubMed 33629972](https://pubmed.ncbi.nlm.nih.gov/33629972/)); Moesgaard et al. 2022 (Sports Med, [PubMed 35044672](https://pubmed.ncbi.nlm.nih.gov/35044672/)); Williams et al. 2017 (Sports Med); Coleman et al. 2024 (PeerJ, [PeerJ 16777](https://peerj.com/articles/16777)); Bell et al. 2023 (Sports Med Open, [PMC10511399](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10511399/)); Helms et al. 2020 (J Hum Kinet).
