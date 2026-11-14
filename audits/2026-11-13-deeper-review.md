# Deeper review: engine, content, dashboard, data, privacy

Last updated: 2026-11-13 (America/New_York). Follows `audits/2026-11-13-tech-debt-and-drift.md`, which covered tooling and process only. Four reviewers worked from a read-only snapshot of `main` at `235ebd3`. V = verified by running or reading the source, I = inferred. "Fixed" means fixed on `main` the same night, with tests where it is code.

## 1. Why the files kept disagreeing

| Finding | Evidence | Status |
|---|---|---|
| The two scheduled coaching tasks have no repository attached. Their sessions could read a copy but not push (HTTP 403). Every run synced Hevy from private state and lost its commits | Transcripts of the 13 Nov runs; a probe task created the same way could not clone or push (V) | **Needs the owner**: attach `tpliv/WorkoutAgent` to both tasks (`PORTABILITY.md`, "Scheduled tasks"). Until then the tools refuse to sync from such a session, so it can do no harm |
| On 13 Nov three sessions pushed three different weekends to Hevy within 70 minutes | Same transcripts (V) | Fixed for that weekend (Sat U2, Sun Full C, as the lifter confirmed). Prevented from now on: Hevy only gets what is on `origin/main` |
| GitHub's default branch is `claude/ecstatic-bardeen-tc62l0`, a commit from October, 47 behind `main` | `git ls-remote --symref origin HEAD` (V) | **Needs the owner**: Settings, General, Default branch, `main`. Then the 21 merged `claude/*` branches can be deleted |
| The repository is public | Repository listing reports `visibility: public` (V) | **Needs the owner** (section 6) |

## 2. Progression engine against the written rules

Reviewer ran each rule in `templates/progression-tracks.md` against `tools/update_tracks.py` and the routine renderer.

| # | Defect | Example | Status |
|---|---|---|---|
| 1 | Deload sessions moved the tracks (section 7 says they do not) | Squat 155, deload 140 x 4 @ 6.5, track became 150 | Fixed |
| 2 | A flagged stall could never be reset: the reset needed a new session | `--reset-on-stall` printed "No new heavy exposures" | Fixed (`stall_pending`) |
| 3 | A gap "hold" could raise the load above the plan | After a reset to 140 with 155 last lifted: 8 days gave 155 | Fixed |
| 4 | Bodyweight pull-ups logged in U2 set the pulldown load to 0 | Next routine: lat pulldown 4 x 5-8 at 0 lb | Fixed (counted as the exposure, load unchanged) |
| 5 | The track followed the heaviest set, not the top set | 155 x 4 @ 8 then 165 x 2 read as a miss at 165 | Fixed (top-set selection written down in `tools/README.md`) |
| 6 | Ordinary 5- or 6-rep back-offs were read as rep-outs and cleared the count that arms the real one | All five real heavy exposures | Fixed |
| 7 | Block week never restarted after a deload | Would read 11 by January | Fixed |

Still open, because they need a rule decision or more work:

| # | Open item | Why it matters | Suggested resolution |
|---|---|---|---|
| A | **Increments and caps are measured from the load lifted, not the load planned.** A deliberate choice (a test is named for it), but under the deadlift caution it gave +20 over plan in one session: planned 150, lifted 160 x 5 @ 8, next 170 | The caution reads "+10 only with a logged RPE 7 or easier, and not twice in a row" | Decide: cap the next load at planned + the allowed step (160 here), or keep it. **This is the current deadlift load** |
| B | Section 8 (the gap table) is applied when rendering, not when the session is processed | A 19-day-gap squat 155 x 5 would move the track to 160; the log held it by hand | Apply the gap rule in the update |
| C | A merged session trained by halves advances the pointer past the half not trained | "Full B" with only the deadlift moves the pointer to L3 and marks the press "top set moved (station taken)" | Advance only past halves with a logged main lift. The week check now flags "planned X, logged Y" when the title differs, which covers the usual case |
| D | Moved-top-set detection uses the lower of planned and last lifted | A plain volume day can be read as the heavy exposure | Use the planned load, as section 9 says |
| E | Accessories are never updated by the tool, though each note promises double progression | 12 Nov front squat 95 x 6 x 3 is logged; its entry is still blank | Either apply double progression to accessories or change the note. Loads can be set with `update_tracks.py --set` |
| F | Double-progression stall counts non-consecutive misses; one heavier set rewrites the track | Row 70 to 85 from a single set of 8 | Tighten with the rule text |
| G | Routine notes contradict the rules in two places | Rep-out printed for a later lift of a merged session; "keep going to 6" beside a "cap at RPE 7" note | Suppress per section 5.3 and when a cap note is present |

Rules with no test at all are listed in the reviewer's report: sections 4 (stale V), 5.1 exit, 5.2 cap, 5.3 skips, 6 second stall, 8 edges, 9 fractional loads, 11.

Ambiguous rule text, where two agents would implement differently: whether "hold", "+10" and the caps are measured from planned or lifted (item A); whether a hold leaves the miss counter "consecutive"; which set is the top set (now defined); whether section 8 covers the row and pull-up; whether double-progression lifts progress in a deload.

## 3. Guide and templates

Both guide reviewers spot-checked claims against primary sources (PubMed, PMC). **18 of 20 checked claims were supported.** Two were not: Held 2026 is labelled "not significant" where the abstract prints p < 0.001 (`guide/06`), and "an RPE 8 is more often a true 7" is overstated for 4-rep top sets (Halperin 2022, Refalo 2024). One could not be verified (Hopper 2026, sauna SMD 0.12).

Contradictions inside the program, ranked by how much they change what the lifter does:

| # | Contradiction | Where |
|---|---|---|
| 1 | The same step and miss rule is stated three ways. Canonical: effective RPE 7 or lower +10, 9.5-10 a miss. Briefs and `guide/03`: "RPE 8 or lower +5; RPE 10 a miss" | `progression-tracks.md` section 5 vs the four day templates, `guide/03` section 5 |
| 2 | Two consecutive misses trigger three different actions | `guide/04` (early deload), `guide/03` (deload on two flags), `progression-tracks.md` section 6 (stall, 7.5% reset) |
| 3 | A "readiness flag" is defined four ways, so the same week can and cannot call for a deload | `guide/03`, `guide/06`, `guide/07`, `guide/08` |
| 4 | Rating: RPE on every set in 0.5 steps, vs one whole-number tap on the top set. With one tap, the 7.5, 8.5 and 9.5 thresholds can never occur | `guide/07`, `templates/README.md` vs `progression-tracks.md` |
| 5 | "Hard sets" are defined as 0-3 reps in reserve, but volume (V) sets at RPE 6-7 are counted in the weekly tallies. Without them the 3-day week has 6 quad and 6 chest hard sets, not 9 | `guide/01`, the template tallies |
| 6 | Weekly targets called binding are missed by every template for some muscles: side and rear delts, biceps and calves in the 6-day week; calves in the 3-day week | `guide/01`, `guide/03`, templates |
| 7 | The deload top set is "RPE 6-7" at 0.90-0.92 of the track, which on the program's own chart is about RPE 5 | `progression-tracks.md` section 7 |
| 8 | Gap rule: `guide/03` holds a regain-phase lift at 8-14 days; the tracks file exempts it | `guide/03` section 4.4 |
| 9 | Cross-block 3-day weeks have no leg curl and no calves | `templates/3-day-week.md`, `rotation.json` |
| 10 | "Design spine" is cited 23 times as the authority for the binding numbers. No such document exists or ever did | `guide/00`-`06`, `progression-tracks.md` |

Unsourced numbers: the 4-, 5- and 6-day weekly set bands; the merged-session cap of 22 sets and 75 minutes; the readiness gate "under 6 hours' sleep"; "no two deloads within four weeks".

Selective use of evidence: the ACSM 2026 position stand is cited as agreeing with the guide's rules, but it found strength unaffected by rest between sets and no effect of periodization on hypertrophy; neither is mentioned.

Audience: `guide/00` addresses an intermediate lifter "in their 30s to 50s". The lifter is 25, returning from 18 months off, in a 300-400 kcal deficit. The age cautions do not apply and "still builds" ignores the deficit.

Nutrition safety: no bodyweight has been recorded since 21 Oct, so none of the calorie rules can fire, yet the plan and fueling grams are computed from that one weight. The "cut 150 kcal" rule had no floor (now added, with a professional-advice line). `guide/06` allowed up to 1% bodyweight loss a week beside a 500 kcal/day cap.

A separate agent is aligning the day templates and guide restatements with `rotation.json` and `progression-tracks.md` and applying the factual and safety corrections above. Its changes and the items it leaves for the owner are in `CHANGELOG.md`.

## 4. Dashboard

Recomputed independently for the last six trained weeks: sessions, days, sets, reps, tonnage and all 19 best-e1RM cells match.

| Defect | Status |
|---|---|
| Two gap clocks on one page disagreed (row: "Hold, 8 days" and "Normal, 3 days") | Fixed: one clock, the routine renderer's |
| Assisted sets counted in tonnage (type string misspelt) | Fixed |
| "Sets that week" wrong in 64 of 95 cells | Fixed |
| Target band follows days trained so far, not days planned: mid-week it shows muscles "Above" target | Open |
| Trend labels are artifacts: the same 105 x 6 reads "down 5.3%" with and without an RPE; heavy and volume days are mixed | Open |
| About 45 pre-October ramp sets are counted as working sets, so 2024 and 2026 volume are not comparable | Open |
| Phone: the lifts table shows 2 of 7 columns; tooltips need hover; the track section is half the page | Open |
| `dashboard/data.json` duplicates the data inside `index.html` and nothing reads it | Open (stop committing it) |

What it should lead with instead: the next session and its loads, the week as planned and done, whether Hevy matches the repo, progress of the heavy top sets toward the regain targets, and a bodyweight and waist trend.

## 5. Data files

- History is clean: 773 rows, 58 workouts, no duplicates, no impossible values. RPE is logged on 7 sets in total.
- There is no bodyweight or waist log, though every adjustment rule depends on one. Suggested: `data/bodyweight.csv`, written by the check-in.
- The InBody reference scan (18 Nov) needs the two days before it free of lifting; the plan allows L1 on the 17th. The scan date belongs in the week file.
- Derived tables had gone stale (current e1RMs in `body-composition.md`); now marked as a snapshot with a pointer to the generated table.

## 6. Privacy and portability

- The repository is public. A stranger gets: body composition and calorie plan, two years of race results with times and city (enough to find a name in public results), planned future gym days and times, a work trip, 58 workout start times, and the work GitHub handle in `PORTABILITY.md` and four commits. No secrets, no employer name, no email, no calendar id in any of the 108 commits.
- Recommendation: make it private. Nothing needs public reads, and deleting files would not remove them from history.
- `PORTABILITY.md` followed literally used to fail on the old repo URL, the default branch, "Scheduled tasks: None yet", and the dashboard page. Rewritten on 13 Nov.
