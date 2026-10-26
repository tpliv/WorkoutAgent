# Lifting Splits and Named Training Programs, Organized by Days per Week

Last updated: 2026-10-21 (primary-source verification addendum at the end)

Research notes for the WorkoutTrainer program designer. Method note: in this environment WebFetch could not resolve any host (thefitness.wiki, stronglifts.com, jimwendler.com, liftosaur.com, liftvault.com, startingstrength.com, strongerbyscience.com, boostcamp.app all returned DNS/proxy errors), so every finding below comes from search-result snippets of the linked pages rather than full page reads. Numbers were only recorded when a snippet stated them; anything I could not confirm is listed under Gaps rather than guessed. Primary-author pages are cited where the search surfaced them; otherwise the best available mirror (Boostcamp, Lift Vault, Liftosaur, Jefit) is cited and labelled as secondary.

---

## Key Question 1: How do the generic splits compare (full body, upper/lower, PPL, PPL+UL hybrids, bro split, Arnold split) on per-muscle frequency and session length?

### Takeaway
Per-muscle frequency is set almost entirely by how many days you train and which split you pick: full body hits everything every session (2-4 days), upper/lower gives ~2x/week on 4 days, PPL gives 1x/week on 3 days and 2x/week on 6 days, the Arnold split gives 2x/week on 6 days, and a classic one-body-part-per-day "bro" split gives 1x/week. The research base (Schoenfeld 2016 and the 2019 volume-equated update, as read by Stronger By Science) favors at least 2x/week per muscle, but the volume-equated advantage of higher frequency is small.

### Cited Findings
**Full body**
- Full-body training suits 2 to 4 days a week, trains each muscle every session, runs about 45-70 minutes per session, with 2-6 sets per muscle per session — [GetFitCraft](https://getfitcraft.com/guides/full-body-vs-split-workout)
- Beginners often start with full body; upper/lower suits four-day schedules — [Arvo training splits](https://arvo.guru/resources/training-splits)

**Upper/lower (4 days)**
- The usual 4-day upper/lower layout hits each muscle about twice weekly; sessions run about 45-60 minutes — [FindYourEdge U/L](https://www.findyouredge.app/news/upper-lower-split-for-beginners-uk-2026)
- Upper/lower is described as the default four-day choice — [Speediance](https://www.speediance.com/blogs/strength-programming/upper-lower-vs-ppl-4-day)

**Push/pull/legs (3 or 6 days)**
- PPL usually needs 6 days to reach twice-weekly frequency; on 3 days each muscle is trained once a week — [FindYourEdge PPL vs full body](https://www.findyouredge.app/news/push-pull-legs-vs-full-body-beginners-uk-2026)
- PPL fits lifters who can train 5 or 6 days and want more volume per muscle; sessions typically 40-60 minutes — [GetFitCraft](https://getfitcraft.com/guides/full-body-vs-split-workout); another source gives 45-75 minutes — [FindYourEdge U/L](https://www.findyouredge.app/news/upper-lower-split-for-beginners-uk-2026)

**Arnold split (6 days) and bro split**
- With the Arnold split you work out six days per week and train each muscle group twice per week; common layout Mon Chest/Back, Tue Shoulders/Arms, Wed Legs, Thu Chest/Back, Fri Shoulders/Arms, Sat Legs, Sun off; a variant inserts a rest day after legs making an eight-day cycle — [Muscle Evo](https://muscleevo.net/arnold-split/); [Fitbod](https://fitbod.me/blog/arnold-split/); [FitnessVolt Arnold vs PPL](https://fitnessvolt.com/arnold-split-vs-ppl/)
- Sources call it advanced; one says it should only be done by lifters training at least two years; beginners may do each of the three workouts once per week (3 days, each muscle 1x) as a modification — [Muscle Evo](https://muscleevo.net/arnold-split/); [Fitbod](https://fitbod.me/blog/arnold-split/)
- An "Arnold x Upper Lower" 5-day variant exists for late-intermediate/advanced lifters — [FitnessVolt Arnold vs PPL](https://fitnessvolt.com/arnold-split-vs-ppl/)
- Classic Bodybuilding.com body-part programs: Jim Stoppani's Shortcut to Size is listed as 4 workouts/week, 45-60 min per workout, level "beginner" — [Bodybuilding.com 10 most popular](https://bodybuilding.com/fun/our-10-most-popular-workout-programs.html); a third-party review describes it as a 4-day body-part split in three 4-week phases — [Lift Vault Shortcut to Size](https://liftvault.com/programs/bodybuilding/shortcut-to-size-program-spreadsheet/)

**Frequency evidence**
- Stronger By Science reads Schoenfeld's 2016 frequency meta-analysis as favoring training a muscle at least twice a week over once, with too little evidence about higher frequencies — [Stronger By Science, frequency](https://www.strongerbyscience.com/frequency/)
- SBS's own hypertrophy-specific pooled analysis: overall effect trivial (d = 0.113; CI 0.07-0.16); lower-frequency groups grew 0.42%/week vs 0.58%/week for higher-frequency groups — [Stronger By Science, frequency-muscle](https://www.strongerbyscience.com/frequency-muscle/)
- Secondary write-ups of the 2019 Schoenfeld/Grgic/Krieger update: when weekly sets were matched, higher frequency still gave somewhat more growth but the difference was smaller — [Bony to Beastly](https://bonytobeastly.com/how-often-should-you-train-each-muscle-group/); [Bodybuilding.com](https://amp.bodybuilding.com/content/the-science-of-training-frequency.html)
- A 2019 pooled analysis of volume-matched studies found no significant hypertrophy difference between low and high frequencies (secondary source) — [GetFitCraft](https://getfitcraft.com/guides/full-body-vs-split-workout)
- PHUL's and PHAT-style twice-weekly layouts are justified by their authors on the idea that muscle protein synthesis stays elevated up to ~48 hours after training — [Hevy PHUL](https://www.hevyapp.com/phul-power-hypertrophy-upper-lower/); [Liftosaur PHAT](https://www.liftosaur.com/programs/phat)

### Inferences
- Frequency table a designer can use (derived from the cited layouts): Full body 2x/wk = each muscle 2x; Full body 3x = 3x; Upper/Lower 4x = 2x; PPL 3x = 1x; PPL 6x = 2x; PPL + Upper/Lower 5x = ~2x (every muscle hit once in the PPL block and once in the U/L block); Arnold 6x = 2x; one-body-part-per-day bro split 5x = 1x.
- Session length rises as frequency falls for the same weekly volume: full-body days must carry every muscle's sets (so 45-70 min at modest per-session volume), while PPL/U-L days can be shorter per session but need more days. For a time-boxed app, cap full-body sessions by limiting per-muscle sets per session (2-6 per the GetFitCraft figure) rather than by cutting muscles.

### Gaps
- I found no primary-source definition or session-length data for the PPL + Upper/Lower 5-day hybrid; its 2x/week frequency is derived, not cited.
- No source gave a canonical exercise list or set/rep scheme for a generic "bro split"; only the Bodybuilding.com-type programs above are documented.
- The Arnold Blueprint (Bodybuilding.com) did not appear in results; days per week unconfirmed.

---

## Key Question 2: What can I do with 2-3 days per week? (Full-body linear progressions and 3-day strength programs)

### Takeaway
The 3-day slot is dominated by full-body barbell linear progressions (Starting Strength, StrongLifts 5x5, Greyskull LP, GZCLP run 3x) for novices and by the Texas Method / Madcow 5x5 for intermediates; 5/3/1 has official 2-day and 3-day templates, and Reddit PPL and the Arnold split can be run as 3-day/1x-frequency fallbacks.

### Cited Findings
**Starting Strength (Mark Rippetoe; book "Starting Strength: Basic Barbell Training", 3rd ed.) — 3 days, full body, novice strength**
- Two alternating full-body workouts, 3 days a week: squat every session (3x5), pressing alternates bench and overhead press (3x5), deadlift is a single heavy set of 5; add weight every workout — [Barbell Logic Novice LP](https://barbell-logic.com/starting-strength-novice-linear-progression/) / [FitnessVolt Starting Strength](https://fitnessvolt.com/powerlifting/programs/starting-strength/)
- Increments cited: add 5 lb every session to squat, bench and press; 10 lb per session to deadlift while it advances, dropping to 5 lb as progress slows; another guide gives 2.5-5 kg per session for squat and deadlift — [FitnessVolt SS calculator](https://fitnessvolt.com/rpe-training/programs/starting-strength/); [FitnessVolt SS LP](https://fitnessvolt.com/starting-strength-lp/)
- Stall rule as summarized: after failing all reps at the same weight 3 sessions in a row, reset that lift ~10% and build back up — [FitnessVolt SS LP](https://fitnessvolt.com/starting-strength-lp/)
- Phases: one guide describes four phases (foundations/technique; power cleans added; chin-ups added with gradually rising intensity, the longest phase; an advanced-novice stage with a lighter squat session plus heavy squats twice a week); phase boundaries are not standardized across sources — [FitnessVolt SS LP](https://fitnessvolt.com/starting-strength-lp/)
- Book wording quoted on the official forum: after two or three more weeks, chin-ups can be added as "the only really useful assistance exercise"; a forum poster quoting the 3rd edition says Phase 3 adds chin-ups after power cleans on day B — [Starting Strength forum, Phase 2 chin-ups](https://startingstrength.com/resources/forum/general-programming/89979-phase-2-chin-ups-addition.html); Liftosaur's Phase 3 instead alternates deadlift and power clean (5x3) with chin-ups 3x10 — [Liftosaur SS3](https://www.liftosaur.com/programs/ss3) (conflict; the book is primary)
- Duration: one review puts the novice program at about 12-16 weeks, low volume, high intensity — [FitnessVolt SS LP](https://fitnessvolt.com/starting-strength-lp/)
- Status: paid book; official program page exists at [startingstrength.com/get-started/programs](https://startingstrength.com/get-started/programs) (could not be read in this environment).

**StrongLifts 5x5 (Mehdi, stronglifts.com) — 3 days, full body, novice strength**
- Workout A: squat, bench press, barbell row, all 5x5. Workout B: squat 5x5, overhead press 5x5, deadlift 1x5. Alternate A/B across three sessions a week — [FitnessVolt StrongLifts](https://fitnessvolt.com/rpe-training/programs/stronglifts-5x5/); [Boostcamp StrongLifts copy](https://www.boostcamp.app/users/JYFbC3-stronglifts-5x5-assistance-work)
- Progression: +2.5 kg per workout for upper body, +5 kg for deadlift ([LiftStrong app listing](https://apps.apple.com/app/id6761501280)); FitnessVolt gives +5 lb every workout and +10 lb on deadlift ([FitnessVolt StrongLifts](https://fitnessvolt.com/rpe-training/programs/stronglifts-5x5/)). 2.5 kg and 5 lb are the same increment; the deadlift increment (5 kg vs 10 lb) is the real discrepancy.
- Deload: if you fail three workouts in a row at the same weight, reduce that exercise by 10%; only the failed lift is deloaded — [Boostcamp StrongLifts copy](https://www.boostcamp.app/users/JYFbC3-stronglifts-5x5-assistance-work); [Lowyat forum](https://forum.lowyat.net/topic/3240638)
- Status: free program; official app (stronglifts.com) — paid-tier details not retrieved.

**Greyskull LP (John Sheaffer) — 3 days, full body, novice strength/size**
- Mon/Wed/Fri; Press and Squat on Mon and Fri, Bench and Deadlift on Wed; the "1x5+" top set is the trademark (do at least five quality reps); start with a weight you can lift for 8-10 reps; +2.5 lb per session upper, +5 lb lower; Greyskull Reset = 10% reduction next session — [Powerlifting Technique, Greyskull LP](https://powerliftingtechnique.com/greyskull-lp/)
- Phrak's Greyskull variant: 3 non-consecutive days, two alternating A/B workouts — [Liftosaur Phrak's Greyskull](https://www.liftosaur.com/programs/phrakgreyskull)
- Status: book ("The Greyskull LP"); Phrak's variant free on r/Fitness.

**GZCLP (Cody Lefever) — 3 or 4 days, novice strength** (details in KQ3; run on 3 days by rotating the four workouts)
- Boostcamp hosts the Cody-partnered GZCLP — [Boostcamp GZCLP](https://www.boostcamp.app/coaches/cody-lefever/gzcl-program-gzclp)

**Texas Method (Glenn Pendlay / Mark Rippetoe, "Practical Programming") — 3 days, full body, early intermediate strength**
- Three-day weekly template: high-volume 5x5 day, light recovery day, intensity day aiming for a new 5-rep PR; progress is weekly, not per session — [Powerlifting Technique, TM vs Madcow](https://powerliftingtechnique.com/texas-method-vs-madcow-5x5/); [Barbell Logic, TM explained](https://barbell-logic.com/the-texas-method-explained/)
- The intensity day is balanced with a cluster of 5-rep sets on Monday (think 5x5) at about a 10% reduction in load — [Starting Strength, TM intensity day](https://startingstrength.com/article/understanding-the-texas-method-intensity-day)
- Increments: ~5 lb/week on squat; ~5 lb per PR session on bench and press (each every 2 weeks since they alternate) — [Powerlifting Technique](https://powerliftingtechnique.com/texas-method-vs-madcow-5x5/)
- Stall handling: when weekly 5 lb jumps can't be sustained on volume day, change 5x5 to 6x4 or 8x3 — [Barbell Logic](https://barbell-logic.com/the-texas-method-explained/); on intensity day, cycle 2x3, 3x2, 2x2, 5 singles, then return to a new 5RM — [Barbell Logic](https://barbell-logic.com/the-texas-method-explained/) / [Starting Strength article](https://startingstrength.com/article/understanding-the-texas-method-intensity-day); Liftosaur suggests trimming Monday 5x5 to 4x5 or 3x5 before dropping volume-day weight — [Liftosaur Texas Method](https://www.liftosaur.com/programs/texasmethod)
- Status: book (Practical Programming for Strength Training); widely reproduced for free.

**Madcow 5x5 (forum user "Madcow", based on Bill Starr) — 3 days, full body, intermediate strength**
- Ramping sets rather than straight sets; default set interval 12.5% between ramp sets — [StrongLifts Madcow guide](https://stronglifts.com/madcow-5x5/workout-guide); [StrongLifts Madcow interval](https://stronglifts.com/madcow-5x5/interval)
- Monday ramps to a top 5x5; Wednesday is lighter (Squat 4x5 with a deadlift variant 4x5 in the StrongLifts table; another source says only two sets of 5 at 75%); Friday "Workout C" Squat 4x5, 1x3, 1x8 (ramp to a top triple PR plus a back-off 8) — [StrongLifts Madcow guide](https://stronglifts.com/madcow-5x5/workout-guide); [FitnessVolt Madcow](https://fitnessvolt.com/madcow-5x5/)
- Madcow uses more total sets across the week than the Texas Method — [Powerlifting Technique](https://powerliftingtechnique.com/texas-method-vs-madcow-5x5/)
- Top set is scaled from 1RM at ~87.5% (a typical 5RM) in generators — [FitnessVolt Madcow](https://fitnessvolt.com/madcow-5x5/)
- Review warns many online write-ups oversimplify Madcow — [Character Strength review](https://characterstrength.co.uk/?p=4336)
- Status: free (originally a forum post / geocities page).

**5/3/1 on 2 or 3 days (Jim Wendler)**
- Wendler's "Training Templates" eBook contains 14 templates including "3 Days Per Week (The origin of 5/3/1)" and "The Twice A Week" — [EliteFTS, Training Templates by Jim Wendler](https://elitefts.com/products/training-templates-by-jim-wendler-ebook)
- On a 3-day version you rotate the 4 core workouts; a mesocycle lasts 4 weeks at 4 days/week and 5+ weeks at 3 days/week — [Muscle & Strength 5/3/1 guide](https://www.muscleandstrength.com/node/4458)
- A 2-day user layout: bench + squat on one day, press + deadlift on the other — [Starting Strength forum, Wendler 2-day](https://startingstrength.com/resources/forum/general-programming/57773-5-3-1-a.html)
- Boostcamp hosts a 3-day "5/3/1 Full Body 1000% Awesome" template — [Boostcamp 5/3/1 full body](https://www.boostcamp.app/users/h6oNsc-531-full-body-1000percent-awesome)
- Core 5/3/1 numbers are in KQ3.

**Reddit PPL as a 3-day program** — "Can't train 6 days: run it as a 3-day program (Pull, Push, Legs)" — [Liftosaur Metallicadpa PPL](https://www.liftosaur.com/programs/metallicadpappl)

**Sheiko intermediate cycles — 3 days** (details in KQ3/KQ6): community app pages list the intermediate versions at 3 training days per week — [Boostcamp Sheiko intermediate medium load](https://www.boostcamp.app/users/N2vPAO-sheiko-intermediate-medium-load)

### Inferences
- For a 3-day app template, the cleanest novice option is an A/B full-body alternation (SS/SL/Greyskull pattern: 2 workouts, 3 slots/week, so each workout appears 3 times per fortnight); the cleanest intermediate option is a role-per-day week (volume / recovery / intensity, TM pattern) because it ties progression to the calendar week rather than to each session.
- 5/3/1 on 3 days behaves as a 4-workout rotation across a 5+ week cycle; the app must track "workout index" independently of calendar week.

### Gaps
- Official Starting Strength program text (startingstrength.com/get-started/programs) could not be read; phase definitions above are from secondary guides and one forum quote of the book.
- StrongLifts' rule for switching to 3x5 / 3x3 / 1x5 after repeated deloads was not found in any result.
- Madcow's weekly progression percentage (commonly stated as 2.5%/week) was not confirmed by any source surfaced; only the 12.5% ramp interval was.
- The exact Texas Method prescription (e.g., Monday 5x5 at 90% of Friday, Wednesday 2x5 at ~80%) was not stated in snippets beyond the "about a 10% reduction" line from Starting Strength.
- Wendler's exact 2-day template contents (and whether the "I don't have a set schedule" wording is from Beyond 5/3/1 or 5/3/1 Forever) were not found; see KQ7.

---

## Key Question 3: What can I do with 4 days per week? (Upper/lower and 4-day strength programs)

### Takeaway
Four days is the richest slot: 5/3/1 (one main lift per day, including Boring But Big and the Forever leader/anchor system), GZCLP's native 4-workout layout, nSuns 4-day, PHUL, Lyle McDonald's Generic Bulking Routine, Candito's 6-week program, the Juggernaut Method base template, and Nippard's Fundamentals upper/lower track all live here.

### Cited Findings
**5/3/1 core (Jim Wendler; books "5/3/1", "Beyond 5/3/1", "5/3/1 Forever") — 4 days, one main lift per day (squat, bench, deadlift, press), intermediate+ strength**
- Four-week wave from a training max: Week 1 65%/75%/85% x 5/5/5+; Week 2 70%/80%/90% x 3/3/3+; Week 3 75%/85%/95% x 5/3/1+; Week 4 deload 40%/50%/60% x 5, no AMRAP; last set of weeks 1-3 is AMRAP — [Lift Vault 5/3/1 calculator](https://liftvault.com/resources/531-calculator/); [thefitness.wiki 5/3/1 primer](https://thefitness.wiki/5-3-1-primer/); [GymNote 5/3/1 percentages](https://www.gymnoteplus.com/blog/531-workout-program)
- Training max default 90% of true 1RM; most variants use 85% or 90% — [Strength Insider 5/3/1](https://strengthinsider.com/workout-programs/531-program/)
- After each cycle add 5 lb to upper-body training maxes and 10 lb to lower-body — [Hardy app, start 5/3/1](https://hardy.app/guides/start-531-program)
- When you consistently miss prescribed minimum reps, cut the training max 10% and rebuild — [Strength Insider](https://strengthinsider.com/workout-programs/531-program/)
- The deload week is treated as optional by some — [Ironmaster 5/3/1](https://ironmaster.com/blog/2026/03/25/the-5-3-1-program)

**5/3/1 Boring But Big (supplemental template)**
- BBB = 5 sets of 10 reps with a lighter weight after the main lift; on squat day the 5x10 can be deadlift and vice versa ("flip side") — [Jim Wendler, Boring But Big](https://www.jimwendler.com/blogs/jimwendler-com/101077382-boring-but-big)
- BBB 3-Month Challenge: 50% of TM for cycle 1, 60% in month 2, 70% in month 3 — [Jim Wendler, BBB 3 Month Challenge](https://jimwendler.com/blogs/jimwendler-com/boring-but-big-3-month-challenge)
- Other Wendler posts give 50-60% of TM for the 5x10 ("the whole goal is to get 5 sets of 10"), a cycle 1 at 30-50% of TM, and advise beginners to start around 30% of TM — [Jim Wendler, BBB and Really Sore](https://www.jimwendler.com/blogs/jimwendler-com/101082438-boring-but-big-and-really-sore); [Jim Wendler, Boring But Big](https://www.jimwendler.com/blogs/jimwendler-com/101077382-boring-but-big)
- Boring But Strong (BBS) variant exists on Wendler's site — [Jim Wendler, Boring But Strong challenge](https://www.jimwendler.com/2014/07/boring-but-strong-challenge/); [Lift Vault BBS](https://liftvault.com/resources/boring-but-strong/)

**5/3/1 Forever (leader/anchor)**
- Listed at 4 days/week; a leader block typically runs as two three-week waves of higher-volume supplemental work (e.g., BBB), an anchor block is one three-week wave of higher-intensity work (e.g., First Set Last, Widowmaker) — [LiftProof 5/3/1 Forever](https://www.liftproof.app/programs/531-forever/)
- The book contains over 50 templates — [AbeBooks listing, 5/3/1 Forever](https://www.abebooks.com/Title-531-Forever-Simple-Effective-Programming/31945876298/bd)
- A common community pairing: Leader = 5s PRO + BBB, Anchor = 3/5/1 + 5x5 FSL — [Dr Workout 5/3/1 spreadsheets](https://www.drworkout.fitness/531-excel-spreadsheets/)
- Running Forever templates on 2 days: forum advice is to go heavy on 2 lifts and do supplemental work for the other 2, swapping the next week; others ran the 4 lifts over 9 days — [T-Nation, Forever templates 2 days a week](https://t-nation.com/t/leader-anchor-4-day-forever-templates-2-days-a-week/275860)
- Status: books are paid (5/3/1 Forever, Beyond 5/3/1, Training Templates eBook); core percentages are free on jimwendler.com and widely mirrored.

**GZCLP (Cody Lefever) — 4 workouts (A1/A2/B1/B2), run 3 or 4 days, novice strength**
- T1 ladder: 5x3+ → 6x2+ → 10x1+, staying at the same weight between stages; on a miss you don't lower the weight, you move to the next stage; last set AMRAP; minimum reps 15 / 12 / 10 per stage — [Massiv GZCLP progression](https://massiv.app/blog/gzclp-progression/); [GymNote GZCLP](https://www.gymnoteplus.com/blog/gzclp-workout-program); [RepCheck GZCLP guide](https://repcheckapp.com/blog/gzclp-guide)
- After failing 10x1+, sources diverge: test a new 5RM and restart at ~85-90% of it; or take the last clean 5x3 weight + 5-15 lb; or deload 15% and restart 5x3+ — [Massiv](https://massiv.app/blog/gzclp-progression/); [GymNote](https://www.gymnoteplus.com/blog/gzclp-workout-program); [Virtus GZCLP](https://virtusapp.ai/blog/gzclp-program-guide/) (conflict noted)
- T2 ladder: 3x10 → 3x8 → 3x6; after a 3x6 failure reset to 3x10 at a little more than the last 3x10 weight — [Massiv](https://massiv.app/blog/gzclp-progression/)
- T3 volume listed as 45+ total reps in the GZCLP table — [r/gzcl wiki mirror](https://reddit.sudovanilla.org/r/gzcl/wiki/GZCL)
- Official hosted version — [Boostcamp GZCLP (Cody Lefever)](https://www.boostcamp.app/coaches/cody-lefever/gzcl-program-gzclp); Cody's current writing is at [gzcl.substack.com](https://gzcl.substack.com/p/p-zero)
- Status: free.

**nSuns 531 LP 4-day (Reddit user nSuns) — 4 days, upper/lower-ish, late-novice/intermediate strength**
- Variants: 4 days/week (best for those new to nSuns), 5 days/week (after 2-3 months of nSuns), 6-day squat- or deadlift-focus versions; the 4-day version is essentially an upper/lower split; training max ~90% of 1RM — [Boostcamp nSuns guide](https://boostcamp.app/nsuns-531-powerlifting-program)
- The 6-day squat and deadlift versions program that lift 3 times per week instead of 2 — [Lift Vault nSuns spreadsheets](https://liftvault.com/programs/powerlifting/n-suns-lifting-spreadsheets/)
- Progression by reps on the T1 "1+" set: 0-1 reps no increase, up to >5 reps = +10-15 lb to training max — [Muscle Evo nSuns](https://muscleevo.net/nsuns-program/); typical 2-3 reps → +5 lb/week; T2 +5 lb upper / +10 lb lower; if stuck at 1 rep or failing, reduce 1RM 10% and rebuild — [Liftosaur nSuns](https://www.liftosaur.com/programs/nsuns)
- Status: free spreadsheets (Lift Vault) and free on Boostcamp.

**PHUL — Power Hypertrophy Upper Lower (Brandon Campbell, published on Muscle & Strength) — 4 days, upper/lower, intermediate powerbuilding**
- Created by Brandon Campbell — [Hevy PHUL](https://www.hevyapp.com/phul-power-hypertrophy-upper-lower/); original — [Muscle & Strength PHUL](https://www.muscleandstrength.com/workouts/phul-workout)
- Layout: Upper Power, Lower Power, rest, Upper Hypertrophy, Lower Hypertrophy, two rest days (Mon/Tue power, Thu/Fri hypertrophy) — [Hevy](https://www.hevyapp.com/phul-power-hypertrophy-upper-lower/); [Liftosaur PHUL](https://www.liftosaur.com/programs/phul)
- Power days: heavy compounds 3-5 reps; hypertrophy days 8-12 reps ([Liftosaur](https://www.liftosaur.com/programs/phul)) or 8-15 reps with isolation work ([Lift Vault PHUL](https://liftvault.com/programs/bodybuilding/phul-spreadsheet/)); each muscle 2x/week; main lifts squat, bench, deadlift, OHP plus isolation (leg extensions, leg curls, seated calf raises at 8-15) — [Boostcamp PHUL](https://www.boostcamp.app/coaches/brandon-campbell/phul-4-day-split)
- Status: free.

**Lyle McDonald Generic Bulking Routine — 4 days upper/lower, intermediate hypertrophy**
- Mon/Tue/Thu/Fri; intermediate (1-3 years); 6-8 week cycles ending with a 2-week deload; target gain ~0.5-1 lb/week; first weekly session of each half 3-5x5 (strength), second 3x8-12 (hypertrophy); a recovery option uses 2-3x6-8 compounds and 1-2x10-12 secondaries; set counts flexible within range — [Liftosaur Lyle GBR](https://www.liftosaur.com/programs/lylegenericbulking); [Lift Vault Lyle GBR](https://liftvault.com/programs/bodybuilding/lyle-mcdonald-bulking-workout-routine-spreadsheet/)
- Status: free (forum post).

**Candito 6-Week Strength Program (Jonnie Candito) — 4 days nominal, frequency varies by week, intermediate powerlifting**
- Runs 6 weeks, medium-high volume, medium to peak intensity, 4 training days/week; hypertrophy phase → strength phase → peaking — [FitnessVolt Candito 6-week](https://fitnessvolt.com/powerlifting/programs/candito-6-week/)
- Weeks 1-2 "muscular conditioning" with five sessions/week and loads near 80%; weeks 3-4 low volume, high intensity strength emphasis; week 4 heavy acclimatization/explosiveness; week 5 "intense strength" with reduced volume and three sessions; week 6 deload or max test, with a 7th deload week recommended if testing — [Powerlifting To Win Candito review](https://www.powerliftingtowin.com/candito-6-week-strength-program/); [FitnessVolt Candito programs](https://fitnessvolt.com/candito-training-programs/); [BarBend](https://barbend.com/?p=156141)
- Status: free spreadsheet; also on [Boostcamp](https://www.boostcamp.app/jonnie-candito/candito-6-week-strength-program).

**Juggernaut Method base template (Chad Wesley Smith) — 4 days (one main lift per day), intermediate strength**
- 16 weeks in four 4-week waves (10s, 8s, 5s, 3s), each wave = Accumulation, Intensification, Realization, Deload; Realization ends in an all-out AMRAP — [Lift Vault Juggernaut](https://liftvault.com/programs/strength/juggernaut-method-base-template-spreadsheet/); [Coachway Juggernaut](https://coachway.io/articles/chad-wesley-smith-juggernaut-method-for-coaches/)
- Accumulation loads: 10s wave 4x10 + 1x10+ at 60%; 8s wave 4x8 + 1x8+ at 65%; 5s wave 4x5 + 1x5+ at 70%; realization tops out at 75/80/85% respectively; training max ~90% of 1RM — [Lift Vault Juggernaut](https://liftvault.com/programs/strength/juggernaut-method-base-template-spreadsheet/); JTS gives realization back-downs 75/80/85/90% across the four waves — [JTS, Going Heavy on the Juggernaut Method](https://www.jtsstrength.com/going-heavy-on-the-juggernaut-method); 3s wave ~80-92.5% of TM — [Arvo Juggernaut](https://arvo.guru/resources/methods/juggernaut-method)
- Reps beaten on the realization top set bump the training max before the next wave (more reps = larger jump) — [Coachway](https://coachway.io/articles/chad-wesley-smith-juggernaut-method-for-coaches/)
- Status: book (The Juggernaut Method 2.0); base template spreadsheet free on Lift Vault.

**Jeff Nippard Fundamentals Hypertrophy Program — includes a 4-day Upper/Lower track** (see KQ6) — [jeffnippard.com Fundamentals](https://jeffnippard.com/products/fundamentals-hypertrophy-program)

**Jim Stoppani Shortcut to Size — 4-day body-part split** — [Bodybuilding.com](https://bodybuilding.com/fun/our-10-most-popular-workout-programs.html)

### Inferences
- 5/3/1 and Juggernaut share the "one main lift per day, percentage of a training max, AMRAP drives progression" architecture; an app that implements one can implement the other by swapping the percentage tables and the TM-bump rule.
- GZCLP's 4 workouts on 4 days give each T1 lift once weekly and each T2 lift once weekly; on 3 days the same four workouts rotate across the week, which is why GZCLP is listed in both the 3-day and 4-day slots.

### Gaps
- nSuns' exact T1 9-set and T2 8-set percentage tables were not retrievable (the Boostcamp table was garbled in the extract). Verify from the Lift Vault spreadsheet before coding.
- The exact 5/3/1 BBB 3-day vs 4-day layouts and the "BBB not for very new beginners or very advanced lifters" claim came only from low-quality aggregator pages and are not cited.
- PHUL's per-exercise set counts (commonly 3-4) were not stated in any snippet; only rep ranges were.
- Juggernaut's exact TM-increase formula (lb per rep over target) was not given.

---

## Key Question 4: What can I do with 5 days per week? (PHAT, nSuns 5-day, PPL+UL hybrids, body-part splits, Nippard 5-day)

### Takeaway
The 5-day slot is mostly powerbuilding/hypertrophy: PHAT (2 power + 3 hypertrophy days), nSuns 5-day, Nippard's 5-day body-part track, Bodybuilding.com's LiveFit, the "Arnold x Upper Lower" hybrid, and the generic PPL + Upper/Lower hybrid. These are long sessions (PHAT is listed at 90 minutes).

### Cited Findings
**PHAT — Power Hypertrophy Adaptive Training (Layne Norton) — 5 days, powerbuilding, intermediate+**
- Layout: Day 1 Upper Body Power, Day 2 Lower Body Power, Day 3 rest, Day 4 Back & Shoulders Hypertrophy, Day 5 Lower Body Hypertrophy, Day 6 Chest & Arms Hypertrophy, Day 7 rest; meant to be followed for three months = three 4-week cycles — [FitnessVolt PHAT](https://fitnessvolt.com/phat-workout/); [StrengthLog PHAT](https://www.strengthlog.com/phat-workout-routine/)
- Power days: 3 sets of 3-5 reps, starting around 70-80% of 1RM — [Lift Vault PHAT](https://liftvault.com/programs/bodybuilding/phat/)
- Upper Body Power example: Pendlay rows 3x3-5, weighted pull-ups 2x6-10, inverted rows 2x6-10, bench press 3x3-5, overhead press 3x6-10, EZ bar curls 3x6-10, skull crushers 3x6-10 — [FitnessVolt PHAT](https://fitnessvolt.com/phat-workout/)
- Hypertrophy days repeat the movements at lower intensity and higher volume, typically 6-10 reps near failure — [FitnessVolt PHAT](https://fitnessvolt.com/phat-workout/)
- Stop 1-2 reps short of failure when starting; deload every 6-12 weeks — [Lift Vault PHAT](https://liftvault.com/programs/bodybuilding/phat/)
- Suitability: "beginner and intermediate" per FitnessVolt but it recommends 12-18 months of consistent training first because sessions are long and demanding, plus a caloric surplus — [FitnessVolt PHAT](https://fitnessvolt.com/phat-workout/)
- Session length 90 min — [Boostcamp PHAT (Layne Norton)](https://www.boostcamp.app/coaches/layne-norton/phat)
- Origin conflict: originally published on SimplyShredded in 2011 and later updated on Biolayne ([Liftosaur PHAT](https://www.liftosaur.com/programs/phat)) vs. "around since 2008" ([Hevy PHAT](https://www.hevyapp.com/phat-workout/))
- Status: free article; official version on Boostcamp.

**nSuns 531 LP 5-day** — for lifters with 2-3 months of nSuns behind them — [Boostcamp nSuns guide](https://boostcamp.app/nsuns-531-powerlifting-program); user-built Jefit copies estimate ~87 min for a bench/OHP day — [Jefit nSuns 5-day](https://www.jefit.com/routines/51216/nsuns-531-lp-5-day)

**Jeff Nippard Fundamentals — 5-day Bodypart Split track** — "the Bodypart Split will have you in the gym 5 days per week"; program is $39.99; beginner-to-intermediate; three separate 8-week splits — [jeffnippard.com Fundamentals](https://jeffnippard.com/products/fundamentals-hypertrophy-program)
- Nippard's free "Essentials" program is on Boostcamp in 2x, 3x and 5x/week versions — [Boostcamp Essentials 5x](https://www.boostcamp.app/users/oRI0tP-jeff-nippards-essentials-program5x); [Boostcamp Essentials 3x](https://www.boostcamp.app/users/ApMnqS-jeff-nippards-essentials-3xweek); [Boostcamp Essentials 2x](https://www.boostcamp.app/users/logFsy-jeff-nippards-the-essentials-program-2x)

**Jamie Eason LiveFit 12-Week Trainer (Bodybuilding.com classic)** — 12 weeks, 5 workouts/week, intermediate, aimed at fat loss / muscle shaping — [Bodybuilding.com LiveFit](https://bodybuilding.com/workout-plans/about/jamie-easons-livefit-trainer-your-12-week-transformation-plan?page=3); [Bodybuilding.com 10 most popular](https://bodybuilding.com/fun/our-10-most-popular-workout-programs.html)

**Arnold x Upper Lower (5 days)** — late-intermediate/advanced hypertrophy — [FitnessVolt Arnold vs PPL](https://fitnessvolt.com/arnold-split-vs-ppl/)

**Sheiko 4-day variants** — the methodology page says individual programs run 3 to 4 sessions per week — [Boostcamp Sheiko methodology](https://www.boostcamp.app/methodology/sheiko)

### Inferences
- A 5-day week built as PPL + Upper + Lower is the standard way to get ~2x/week frequency without 6 sessions; no primary author "owns" it, so a designer can define it freely (PPL 1x + U/L 1x = every muscle twice).
- PHAT and PHUL share the power/hypertrophy duality; PHAT adds a fifth day by splitting the upper hypertrophy day in two (back/shoulders vs chest/arms), which is the simplest 4→5 day expansion rule for an app.

### Gaps
- No source documented a canonical PPL+Upper/Lower 5-day program with set/rep numbers.
- Kris Gethin 12-Week Trainer days per week not found (listed only as "Advanced, gain weight/build muscle").
- Nippard's Powerbuilding System day count and price were not confirmed from an official page (only an unverified third-party PDF saying 4-6 days).

---

## Key Question 5: What can I do with 6 days per week? (Reddit PPL, Arnold split, nSuns 6-day, RP 6-day)

### Takeaway
Six days is the natural home of PPL run twice (Reddit PPL) and the Arnold split, both giving 2x/week per muscle; nSuns' 6-day variants push one lift to 3x/week. These are for lifters who recover well and can spend 6 sessions; volume per session is lower than on 3-4 day plans.

### Cited Findings
**Reddit PPL (u/Metallicadpa, r/Fitness 2015) — 6 days, PPL x2, novice/early-intermediate strength+size**
- Created by Reddit user /u/metallicadpa, posted to r/Fitness in 2015; Pull/Push/Legs run over six days with two sessions of each; a linear-progression PPL aimed at beginners; fallback: run as 3-day — [Liftosaur Metallicadpa PPL](https://www.liftosaur.com/programs/metallicadpappl)
- Compound lifts: deadlift, bench press, squat, barbell row, overhead press; pull-ups swappable for pulldowns or chin-ups — [Liftosaur Metallicadpa PPL](https://www.liftosaur.com/programs/metallicadpappl)
- Last set of each main compound is AMRAP with at least 5 reps; don't AMRAP bench and OHP on the same day; face pulls 5x15-20; push days superset triceps pushdowns/overhead extensions with lateral raises — [Jefit Reddit PPL copy](https://www.jefit.com/routines/212519/reddit-metallicadpas-beginner-ppl)
- Warm-up: empty bar x10, then 50% x10, 75% x5, 90% x3 of working weight — [Jefit Reddit PPL copy](https://www.jefit.com/routines/212519/reddit-metallicadpas-beginner-ppl)
- Status: free (Reddit post r/Fitness 37ylk5; Boostcamp/Liftosaur mirrors).

**Arnold split — 6 days** — see KQ1 (each muscle 2x/week; Chest/Back, Shoulders/Arms, Legs repeated; advanced) — [Muscle Evo](https://muscleevo.net/arnold-split/); [Fitbod](https://fitbod.me/blog/arnold-split/)

**nSuns 6-day squat / 6-day deadlift** — for lifters who can handle five+ days; the focus lift is programmed 3x/week — [Boostcamp nSuns guide](https://boostcamp.app/nsuns-531-powerlifting-program); [Lift Vault nSuns](https://liftvault.com/programs/powerlifting/n-suns-lifting-spreadsheets/); a user-built 6-day squat copy estimates 135 min per session — [Jefit nSuns 6-day squat](https://www.jefit.com/my-jefit/workouts/36462/nsuns-531-lp-6-day-squat)

**Renaissance Periodization physique templates** — male and female physique templates can be used from 3 to 6 days per week; simplified templates 2-4 days (low-quality source; verify) — [RP template aggregator page](https://chw.dhis2.org/template/rp-training-templates-free.html)

### Inferences
- At 6 days, Reddit PPL and the Arnold split are functionally the same frequency (2x) with different pairings: PPL groups by movement pattern (push/pull/legs), Arnold by antagonist muscle pairs (chest+back, shoulders+arms). For an app, the PPL grouping maps more cleanly onto exercise tags.

### Gaps
- Reddit PPL's exact set/rep scheme per lift (commonly cited as deadlift 1x5+, bench/OHP 5x5 → 1x5+, squat 3x5, rows 4x5/1x5+, accessories 3x8-12) was NOT confirmed by any retrieved snippet; the Jefit copies only confirm the AMRAP rule and the face-pull prescription. Verify against the original Reddit post before copying numbers.
- Reddit PPL progression increments (2.5 kg upper / 5 kg lower per session) and deload rule were not surfaced.

---

## Key Question 6: Multi-frequency frameworks that scale across 1-6 days (GZCL method, Nuckols 28 programs, Sheiko, RP/Israetel, Helms, Nippard)

### Takeaway
Several sources are frameworks rather than fixed day-counts: GZCL's tier rules, Nuckols' 28 programs (1/2/3 days per lift), RP's volume landmarks and 3-6-day templates, Helms' pyramid, and Nippard's 3/4/5-day Fundamentals. These are the best fit for an app that must generate a week from a day count, because their rules are expressed per muscle or per lift rather than per calendar slot.

### Cited Findings
**GZCL Method (Cody Lefever) — framework**
- T1 (primary compound): 85-100% of training max or goal weight, 10-15 total reps per workout, typically 1-3 reps per set — [r/gzcl wiki mirror](https://reddit.sudovanilla.org/r/gzcl/wiki/GZCL); [Boostcamp GZCL methodology](https://www.boostcamp.app/methodology/gzcl)
- T2 (secondary/variation): 65-85%, 20-30 total reps, usually sets of 5-8 — [r/gzcl wiki mirror](https://reddit.sudovanilla.org/r/gzcl/wiki/GZCL); [Bodybuilding.com, Squat Bigger with GZCL](https://bodybuilding.com/fun/squat-bigger-with-the-gzcl-method.html)
- T3 (accessory/isolation): under 65% of a 2-3RM, usually 8+ reps per set, 30+ reps (GZCLP table says 45+) — [FitnessVolt GZCL](https://fitnessvolt.com/gzcl-method/); [r/gzcl wiki mirror](https://reddit.sudovanilla.org/r/gzcl/wiki/GZCL)
- 1:2:3 rule: for every rep in T1, ~2 reps in T2 and ~3 in T3, framed as a weekly balance rather than per session — [Boostcamp GZCL methodology](https://www.boostcamp.app/methodology/gzcl); [FitnessVolt GZCL](https://fitnessvolt.com/gzcl-method/)
- The percentages and rep ranges are "soft" rules; GZCLP is the structured entry program, and the broader method offers more flexible programs (e.g., UHF 5-week, Jacked & Tan 2.0) — [Set For Set GZCLP](https://www.setforset.com/blogs/news/gzclp-beginner-linear-progression-strength-program); [Liftosaur GZCL UHF 5 weeks](https://www.liftosaur.com/programs/gzcl-uhf-5-weeks)
- Status: free (blog/Substack/r/gzcl wiki).

**Greg Nuckols' 28 Free Programs (Stronger By Science)**
- Free in exchange for an email address; covers squat, bench and deadlift with beginner, intermediate and advanced templates at 1, 2 or 3 training days per week per lift; 3 lifts x 3 levels x 3 frequencies = 27, plus a 4th deadlift variation (low/medium/high volume in addition to the standard beginner version) = 28 — [Lift Vault, Nuckols 28 Programs](https://liftvault.com/programs/strength/greg-nuckols-28-programs-spreadsheet/)
- Every program runs on a 4-week cycle with a 1RM test at the end; intermediate/advanced versions add variations (e.g., front squat), beginner versions stick to the big three — [Lift Vault, Nuckols 28 Programs](https://liftvault.com/programs/strength/greg-nuckols-28-programs-spreadsheet/)
- Separate from the newer SBS Program Bundle: six 21-week autoregulated programs, also free with signup — [Lift Vault, Nuckols 28 Programs](https://liftvault.com/programs/strength/greg-nuckols-28-programs-spreadsheet/)

**Sheiko (Boris Sheiko) — 3-4 days, high volume submaximal, intermediate-advanced powerlifting**
- Programs run 3 to 4 sessions per week; most of the cycle at 68-80% of 1RM — [Boostcamp Sheiko methodology](https://www.boostcamp.app/methodology/sheiko)
- #29 = preparation, #30 = highest-volume cycle, #31 = heavier, #32 = peaking; rated intermediate to advanced (1+ years of consistent barbell training) — [Liftosaur Sheiko 29-32](https://www.liftosaur.com/programs/sheiko-29-32); Boostcamp calls #29 and #37 intermediate-friendly starting points — [Boostcamp best Sheiko](https://www.boostcamp.app/best/sheiko)
- Intermediate app versions list 3 days/week and 70-130 minute sessions; a combined #37/#30/#32 "u80" listing says 3 days/week with 180-minute sessions — [Boostcamp Sheiko intermediate medium load](https://www.boostcamp.app/users/N2vPAO-sheiko-intermediate-medium-load); [Boostcamp Sheiko u80](https://www.boostcamp.app/users/sheiko-u80)
- One secondary listing gives 981 working reps across #29 and 1,110 across #37 — [Boostcamp Sheiko intermediate large load](https://www.boostcamp.app/users/1l4raI-sheiko-intermdiate-large-load-2) (single source; approximate)
- Status: original numbered cycles are free (forum/spreadsheets); books and the Sheiko app are paid.

**Renaissance Periodization / Mike Israetel — volume landmarks and templates**
- MEV = lowest weekly set count that still drives growth; MAV = most productive zone; MRV = recoverable ceiling; popularized by Israetel/RP — [Arvo RP training](https://arvo.guru/resources/methods/rp-training)
- Example numbers vary by source: MEV ~4-8, MAV 12-20, MRV 18-30 sets/week for intermediates ([FitnessVolt volume tracker](https://fitnessvolt.com/rpe-training/volume-tracker/)); chest MEV 10, MAV 14-18, MRV 22 ([Arvo volume training](https://arvo.guru/resources/volume-training))
- Weekly frequency per muscle 2-4x, 2-3x typical, per a third-party reference card citing "Scientific Principles of Hypertrophy Training" (unverified against the book) — [skills.cat Israetel reference](https://skills.cat/skills/borisghidaglia/science-based-lifter/israetel-training)
- RP-style mesocycle: start near MEV, add ~1 set per muscle per week over 4-6 weeks, then deload (~1 week at ~50% volume) — [Arvo RP training](https://arvo.guru/resources/methods/rp-training); a forum user describes novice RP templates progressing from 3 RIR to 1 RIR over a 6-week mesocycle followed by a deload — [TexAgs forum](https://texags.com/forums/48/topics/3361390/replies/64326804)
- Physique templates usable 3-6 days/week; simplified templates 2-4 days (low-quality aggregator; verify on rpstrength.com) — [RP template aggregator](https://chw.dhis2.org/template/rp-training-templates-free.html)
- RP recommends reading Helms' Muscle and Strength Pyramids before its own "Scientific Principles of Hypertrophy" book — [Performative Bafflement hypertrophy guide](https://performativebafflement.substack.com/p/a-comprehensive-guide-to-hypertrophy)
- Status: paid (templates, books, RP Hypertrophy app); free content on RP YouTube/blog.

**Eric Helms — The Muscle and Strength Pyramid: Training (3rd ed.)**
- Framework levels: Adherence; Volume, Intensity and Frequency; Progression; Exercise Selection; Rest Periods and Tempo; Warming Up; the first level plans workout frequency with adherence in mind — [RippedBody, how to build training programs (sample chapter)](https://rippedbody.com/how-to-build-training-programs/)
- Status: paid book; sample chapter free at RippedBody.

**Jeff Nippard — Fundamentals Hypertrophy Program**
- $39.99 (sale price listed), beginner-to-intermediate, three separate 8-week splits: Full Body 3 days/week, Upper/Lower 4 days/week, Bodypart 5 days/week; needs a rack, barbell, bench and ideally dumbbells — [jeffnippard.com Fundamentals](https://jeffnippard.com/products/fundamentals-hypertrophy-program)
- Free "Essentials" program on Boostcamp in 2x/3x/5x week versions — [Boostcamp Essentials 3x](https://www.boostcamp.app/users/ApMnqS-jeff-nippards-essentials-3xweek)

### Inferences
- The frameworks converge on the same generator logic: pick weekly sets per muscle (RP landmarks / Helms volume), pick frequency 2-3x (SBS evidence, RP), then divide sets across the available days. GZCL adds the per-session shape (one heavy T1, one moderate T2, high-rep T3s with 1:2:3 rep balance).
- Nuckols' "days per lift" design is the only cited system that explicitly decouples per-lift frequency from the weekly day count (a 3-day week can run squat 1x, bench 3x, deadlift 1x), which is useful for user-chosen priorities.

### Gaps
- Helms' concrete numbers (weekly sets per muscle, rep ranges, frequency) were not stated in any snippet; only the framework's level names were. Do not quote "10-20 sets" to Helms without checking the book/sample chapter.
- RP's official template day-counts and prices were not confirmed from rpstrength.com.
- Israetel's exact per-muscle landmark tables could not be verified; the values above are third-party approximations and differ by site.

---

## Key Question 7: Which programs explicitly support flexible or variable training days?

### Takeaway
Explicit flexibility is rarer than assumed: 5/3/1 has official 2-day and 3-day templates and a rotating 4-workout structure; GZCLP/GZCL and Reddit PPL state 3- or 4-/6-day options; Nuckols' 28 programs offer 1/2/3 days per lift; RP templates span 3-6 days; Nippard sells 3/4/5-day tracks. The specific Wendler phrase "I don't have a set schedule" could not be located in any retrieved source.

### Cited Findings
- 5/3/1: official templates include "3 Days Per Week" and "The Twice A Week" — [EliteFTS Training Templates eBook](https://elitefts.com/products/training-templates-by-jim-wendler-ebook); on 3 days you rotate the 4 core workouts and the cycle stretches to 5+ weeks — [Muscle & Strength 5/3/1](https://www.muscleandstrength.com/node/4458); Wendler has crafted variations for frequencies as low as twice per week — [Lift Vault 5/3/1 spreadsheet](https://liftvault.com/programs/powerlifting/jim-wendlers-531-spreadsheet/); 5/3/1 Forever includes 50+ templates — [AbeBooks 5/3/1 Forever](https://www.abebooks.com/Title-531-Forever-Simple-Effective-Programming/31945876298/bd); community practice of running the 4 lifts over 9 days — [T-Nation thread](https://t-nation.com/t/leader-anchor-4-day-forever-templates-2-days-a-week/275860)
- GZCL: "a framework rather than a fixed program"; percentages/rep ranges are soft rules; GZCLP for beginners, flexible programs for those past that phase — [Set For Set GZCLP](https://www.setforset.com/blogs/news/gzclp-beginner-linear-progression-strength-program); [FitnessVolt GZCL](https://fitnessvolt.com/gzcl-method/)
- Reddit PPL: "Can't train 6 days: run it as a 3-day program" — [Liftosaur Metallicadpa PPL](https://www.liftosaur.com/programs/metallicadpappl)
- Arnold split: beginners do each workout once per week (3 days), experienced lifters twice (6 days) — [Fitbod Arnold split](https://fitbod.me/blog/arnold-split/)
- Nuckols 28: templates at 1, 2 or 3 days per week per lift, mixable across lifts — [Lift Vault Nuckols 28](https://liftvault.com/programs/strength/greg-nuckols-28-programs-spreadsheet/)
- nSuns: 4-, 5- and 6-day variants — [Boostcamp nSuns](https://boostcamp.app/nsuns-531-powerlifting-program)
- Nippard Fundamentals: 3-, 4- and 5-day splits sold as one product — [jeffnippard.com Fundamentals](https://jeffnippard.com/products/fundamentals-hypertrophy-program); Essentials free in 2x/3x/5x — [Boostcamp Essentials 2x](https://www.boostcamp.app/users/logFsy-jeff-nippards-the-essentials-program-2x)
- RP physique templates 3-6 days, simplified 2-4 (weak source) — [RP template aggregator](https://chw.dhis2.org/template/rp-training-templates-free.html)
- Boostcamp has a reschedule feature for when the week doesn't go to plan — [Boostcamp 5/3/1 full body](https://www.boostcamp.app/users/h6oNsc-531-full-body-1000percent-awesome)
- Lyle McDonald GBR: set counts flexible within the prescribed range by feel — [Liftosaur Lyle GBR](https://www.liftosaur.com/programs/lylegenericbulking)
- Candito 6-week varies sessions per week by phase (5 in weeks 1-2, 3 in week 5) — [Powerlifting To Win Candito](https://www.powerliftingtowin.com/candito-6-week-strength-program/); [FitnessVolt Candito programs](https://fitnessvolt.com/candito-training-programs/)

### Inferences
- The programs that tolerate a variable week best are those whose unit is a "workout in a rotation" rather than a "day of the week": 5/3/1 (4 workouts), GZCLP (A1/A2/B1/B2), SS/SL/Greyskull (A/B), Reddit PPL (P/P/L). A designer can make any of these day-count-agnostic by storing a rotation pointer and stretching the cycle length (as Muscle & Strength describes for 5/3/1 on 3 days).
- Programs with fixed weekly roles (Texas Method, Madcow, PHUL, PHAT, Candito) assume specific day spacing (volume → recovery → intensity; power → hypertrophy) and degrade when days are dropped.

### Gaps
- The Wendler "I don't have a set schedule" template (from Beyond 5/3/1 or 5/3/1 Forever) was not found in any search result; the search budget ran out before a targeted follow-up. Its contents (commonly described as rotating the four lifts through whatever days are available) remain unverified here.

---

## Key Question 8: Typical session durations by layout/program

### Takeaway
Cited figures: full body 45-70 min; upper/lower 45-60; PPL 40-75; PHAT 90 min; nSuns ~60-135 min depending on accessory volume; Sheiko 70-180 min; Shortcut to Size 45-60. Most other programs publish no official duration.

### Cited Findings
- Full body 45-70 min; PPL 40-60 min — [GetFitCraft](https://getfitcraft.com/guides/full-body-vs-split-workout)
- Upper/lower 45-60 min; PPL 45-75 min — [FindYourEdge U/L](https://www.findyouredge.app/news/upper-lower-split-for-beginners-uk-2026)
- PHAT: session length 90 min — [Boostcamp PHAT](https://www.boostcamp.app/coaches/layne-norton/phat); PHAT sessions described as long and demanding — [FitnessVolt PHAT](https://fitnessvolt.com/phat-workout/)
- nSuns user-built copies: 87 min (8 exercises, bench/OHP day), 135 min (6-day squat variant), 57-61 min (trimmed versions) — [Jefit nSuns 5-day](https://www.jefit.com/routines/51216/nsuns-531-lp-5-day); [Jefit nSuns 6-day squat](https://www.jefit.com/my-jefit/workouts/36462/nsuns-531-lp-6-day-squat); [Jefit nSuns LP](https://www.jefit.com/routines/36439/nsuns-531-lp)
- Sheiko intermediate app versions 70-130 min; u80 combined listing 180 min — [Boostcamp Sheiko intermediate medium load](https://www.boostcamp.app/users/N2vPAO-sheiko-intermediate-medium-load); [Boostcamp Sheiko u80](https://www.boostcamp.app/users/sheiko-u80)
- Shortcut to Size 45-60 min per workout — [Bodybuilding.com 10 most popular](https://bodybuilding.com/fun/our-10-most-popular-workout-programs.html)

### Inferences
- Duration tracks total sets plus rest: percentage-based strength programs with many heavy sets and long rests (nSuns 9+8 sets of main work, Sheiko) run longest; A/B novice programs with 3 lifts per day should sit at the low end of the 45-70 min full-body band even though no official figure was cited.

### Gaps
- No source gave official durations for 5/3/1 (the "45 minutes" folk figure), GZCLP, Reddit PPL, Starting Strength, StrongLifts, Texas Method, Madcow, PHUL, Juggernaut or Candito.

---

## Key Question 9: Copyright / paywall status summary

### Takeaway
Most community strength programs are free; author-brand programs (Wendler books, Rippetoe books, Helms, RP, Nippard Fundamentals, Juggernaut book, Greyskull book) are paid, usually with the core method freely described online.

### Cited Findings
- Free: GZCLP/GZCL ([Boostcamp GZCLP](https://www.boostcamp.app/coaches/cody-lefever/gzcl-program-gzclp)); nSuns ([Lift Vault](https://liftvault.com/programs/powerlifting/n-suns-lifting-spreadsheets/)); Reddit PPL ([Liftosaur](https://www.liftosaur.com/programs/metallicadpappl)); PHUL ([Muscle & Strength](https://www.muscleandstrength.com/workouts/phul-workout)); PHAT ([Boostcamp](https://www.boostcamp.app/coaches/layne-norton/phat)); Candito 6-week ([Boostcamp](https://www.boostcamp.app/jonnie-candito/candito-6-week-strength-program)); Lyle GBR ([Lift Vault](https://liftvault.com/programs/bodybuilding/lyle-mcdonald-bulking-workout-routine-spreadsheet/)); Nuckols 28 (free for email) and SBS Bundle (free with signup) ([Lift Vault](https://liftvault.com/programs/strength/greg-nuckols-28-programs-spreadsheet/)); Nippard Essentials ([Boostcamp](https://www.boostcamp.app/users/ApMnqS-jeff-nippards-essentials-3xweek)); 5/3/1 core percentages and BBB posts ([jimwendler.com](https://www.jimwendler.com/blogs/jimwendler-com/101077382-boring-but-big)); Juggernaut base template spreadsheet ([Lift Vault](https://liftvault.com/programs/strength/juggernaut-method-base-template-spreadsheet/)).
- Paid: 5/3/1 Forever and Training Templates eBook ([EliteFTS](https://elitefts.com/products/training-templates-by-jim-wendler-ebook); [AbeBooks](https://www.abebooks.com/Title-531-Forever-Simple-Effective-Programming/31945876298/bd)); Nippard Fundamentals $39.99 ([jeffnippard.com](https://jeffnippard.com/products/fundamentals-hypertrophy-program)); Helms' Muscle and Strength Pyramid book, sample chapter free ([RippedBody](https://rippedbody.com/how-to-build-training-programs/)); Starting Strength / Practical Programming books ([Starting Strength programs page](https://startingstrength.com/get-started/programs)); Greyskull LP book ([Powerlifting Technique](https://powerliftingtechnique.com/greyskull-lp/)).

### Inferences
- For an app, the safest sources to reproduce verbatim are the community programs (GZCLP, nSuns, Reddit PPL, PHUL, PHAT, Lyle GBR, Candito, Nuckols 28 with attribution). Book-based programs (5/3/1 templates, SS phases, Juggernaut, Helms, RP) should be implemented as original parameterizations of the published method with attribution rather than copied tables.

### Gaps
- RP template and RP Hypertrophy app prices were not confirmed from an official page.
- StrongLifts app free-vs-paid tier split was not retrieved (stronglifts.com unreachable).

---

## Quick index: days per week → documented options

- **2 days:** 5/3/1 "Twice A Week" template (paid eBook); Nippard Essentials 2x (free); RP simplified templates 2-4 days (weak source); Nuckols 28 at 1-2 days per lift (free).
- **3 days:** Starting Strength (book); StrongLifts 5x5 (free); Greyskull LP / Phrak's (book / free); GZCLP 3-day rotation (free); 5/3/1 3-day rotation (free core); Texas Method (book, widely mirrored); Madcow 5x5 (free); Reddit PPL 3-day fallback (free); Arnold split 1x (free); Sheiko intermediate 3-day (free numbered cycles); Nippard Fundamentals full-body / Essentials 3x (paid / free); Nuckols 28 at 3 days per lift (free).
- **4 days:** 5/3/1 standard, BBB, Forever leader/anchor (free core / paid books); GZCLP native (free); nSuns 4-day (free); PHUL (free); Lyle McDonald GBR (free); Candito 6-week (free); Juggernaut Method base (book / free spreadsheet); Nippard Fundamentals U/L (paid); Shortcut to Size (Bodybuilding.com, free); Sheiko 4-day (free cycles).
- **5 days:** PHAT (free); nSuns 5-day (free); Nippard Fundamentals bodypart / Essentials 5x (paid / free); LiveFit (free); Arnold x Upper Lower (free description); generic PPL + U/L hybrid (no canonical source).
- **6 days:** Reddit PPL (free); Arnold split (free description); nSuns 6-day squat / deadlift (free); RP physique templates up to 6 days (paid).

---

## Addendum 2026-10-21: primary-source verification

**Method.** Second pass with open internet access. Pages were fetched directly with curl and WebFetch and read in full: jimwendler.com, jeffnippard.com, rpstrength.com (14 muscle guides and the landmarks article), stronglifts.com, strongerbyscience.com, Boostcamp pages that are officially partnered with the program author, biolayne.com, Cody Lefever's blog, rippedbody.com, elitefts.com and PubMed (E-utilities abstracts). Some sources could not be reached. startingstrength.com, muscleandstrength.com and strengthlog.com returned Cloudflare 403 to curl; StrengthLog was later read once through WebFetch. reddit.com (bot wall) and web.archive.org (connection reset) were also unreachable, as were thefitness.wiki through curl and the legacy bodybuilding.com pages, which now redirect to a 404 on shop.bodybuilding.com. Items that depend on those sources stay unverified. Labels: **[PR]** peer-reviewed; **[P1]** practitioner, the program author's own site or an author-partnered page; **[P2]** practitioner, a secondary site or mirror; **(older)** published before 2016. Copyrighted programs are described, not reproduced. Prices are as listed on 2026-10-21, in USD.

| # | Claim (section) | Original status | Verified result | Source |
|---|---|---|---|---|
| 1 | Schoenfeld 2016 meta-analysis favors >= 2x/week per muscle (KQ1) | Via SBS (secondary) | **Confirmed.** 10 studies. Higher frequency ES 0.49 +/- 0.08 vs 0.30 +/- 0.07 (p = 0.002). The authors' own conclusion is that major muscles should be trained at least twice a week; 3x vs 2x undetermined. Hypertrophy outcome. | [PR] **(older)** Schoenfeld, Ogborn & Krieger 2016, *Sports Med* 46(11):1689-1697, doi:10.1007/s40279-016-0543-8, [PubMed 27102172](https://pubmed.ncbi.nlm.nih.gov/27102172/) |
| 2 | 2019 update: with sets matched, higher frequency "still gave somewhat more growth" (KQ1, Bony to Beastly / Bodybuilding.com) | Secondary | **Corrected.** 25 studies. On a volume-equated basis there was **no significant difference**. Only non-volume-equated studies favoured higher frequency, and only modestly. The authors conclude frequency can be chosen by preference when volume is equal. Hypertrophy outcome. | [PR] Schoenfeld, Grgic & Krieger 2019, *J Sports Sci* 37(11):1286-1295, doi:10.1080/02640414.2018.1555906, [PubMed 30558493](https://pubmed.ncbi.nlm.nih.gov/30558493/) |
| 3 | 2019 pooled analysis: no significant difference when volume-matched (KQ1, GetFitCraft) | Secondary | **Confirmed** against the abstract (row 2). | as row 2 |
| 4 | SBS pooled analysis d = 0.113 (CI 0.07-0.16); 0.42 vs 0.58 %/week (KQ1) | SBS page | **Confirmed.** Author Greg Nuckols; page metadata 2018-08-10. This is a blog analysis, not peer-reviewed. Citation fix: `strongerbyscience.com/frequency/` 301-redirects to `/frequency-muscle/`, so the note's two SBS links reach the same article. | [P1] [SBS, frequency-muscle](https://www.strongerbyscience.com/frequency-muscle/) |
| 5 | Nippard Fundamentals: $39.99 "sale price"; 3 tracks of 8 weeks at 3 / 4 / 5 days; beginner-intermediate (KQ4, KQ6) | Official page via snippet | **Confirmed, with one wording fix.** $39.99 is the regular price (the store's compare-at price equals the price), not a sale. The FAQ gives full body 3 days, upper/lower 4 days and bodypart 5 days, 8 weeks each, linear progression. The 5-day "modified body part split" trains legs twice (legs/abs appears on two days). | [P1] [jeffnippard.com Fundamentals](https://jeffnippard.com/products/fundamentals-hypertrophy-program) |
| 6 | Nippard Powerbuilding System day count and price (KQ4 Gap) | Gap (third-party PDF said 4-6 days) | **Gap filled.** $49.99 (a $99.99 bundle variant also exists). 10 weeks. Two versions: 4x/week and 5-6x/week. It alternates a full-body week with an upper/lower week, uses high-effort top sets with RPE plus %1RM, and ends with a max test. Aimed at intermediate-advanced lifters; the FAQ says beginners in their first 1-2 years should run Fundamentals first. | [P1] [jeffnippard.com Powerbuilding](https://jeffnippard.com/products/the-powerbuilding-system) |
| 7 | Nippard "Essentials" is free on Boostcamp in 2x / 3x / 5x versions (KQ4, KQ6, KQ7, KQ9, Quick index) | Boostcamp user pages | **Corrected.** Essentials is a **paid** jeffnippard.com product at $39.99. It comes in **2x, 3x, 4x and 5x** per-week versions, keeps sessions under 45 min, and has three 4-week blocks. Layouts: 2x full/full; 3x full/upper/lower; 4x upper/lower twice; 5x upper/lower/push/pull/legs. The cited Boostcamp pages are under `/users/`, i.e. community uploads (one is credited to a user, "Tyler Chase"), not author-partnered. jeffnippard.com carries a notice warning against unauthorized "free program" copies. | [P1] [jeffnippard.com Essentials](https://jeffnippard.com/products/the-essentials-program); [P2] [Boostcamp community copy](https://www.boostcamp.app/users/ApMnqS-jeff-nippards-essentials-3xweek) |
| 8 | RP volume-landmark definitions MV / MEV / MAV / MRV (KQ6) | Third-party (Arvo) | **Confirmed** on RP's own pages. The muscle guides add MAV\*P and MRV\*P, values for when a muscle is given primary priority. | [P1] RP, [Training Volume Landmarks for Muscle Growth](https://rpstrength.com/blogs/articles/training-volume-landmarks-muscle-growth) (page dated 2017-01-04); [RP chest guide](https://rpstrength.com/blogs/articles/chest-hypertrophy-training-tips) |
| 9 | Israetel per-muscle landmark values (KQ6 Gap; FitnessVolt MEV 4-8 / MAV 12-20 / MRV 18-30; Arvo chest MEV 10 / MAV 14-18 / MRV 22) | Third-party approximations | **Gap filled; the third-party values are superseded and the conflict is recorded.** RP's muscle guides (Dr. Mike Israetel; pages dated 2023-12-29 to 2024-01-04) give weekly sets as MV / MEV / MAV / MRV. Chest 2-4 / 4-6 / 6-16 / 16-24. Back 2-6 / 6-8 / 8-20 / 20-26 (from an image table). Biceps 6-8 / 8-10 / 14-20 / 20-26. Triceps 0-4 / 4-6 / 6-16 / 16-20. Quads 2-4 / 4-6 / 6-14 / 14-18. Hamstrings 0-2 / 2-4 / 2-8 / 8-14. Glutes 2-6 / 6-8 / 8-24 / 24-30. Side delts 2-6 / 6-8 / 8-24 / 24-30. Rear delts 0-4 / 0-4 / 4-12 / 12-20. Front delts 0-2 / 0-2 / 4-8 / 8-12. Calves 2-4 / 4-6 / 6-16 / 16-24. Traps 0-4 / 0-4 / 4-12 / 12-20. Abs 0-4 / 0-4 / 4-12 / 12-20. Forearms 0-4 / 0-8 / 8-24 / 24-30. RP labels these as averages for intermediates training mostly whole-body for 3-7 years, lower for beginners. **Conflicts:** (a) RP's landmarks article says MV is "~6 sets per week" for any muscle trained >= 2x/week, which is higher than most muscle-guide MVs (0-4). (b) Arvo's chest MEV 10 / MRV 22 does not match RP's current chest 4-6 / 16-24. (c) The biceps page's own TL;DR ("8-20 sets", frequency 3-6x) differs from its table. (d) The widely circulated older RP chest values (MV 8 / MEV 10 / MAV 12-20 / MRV 22) could not be checked because web.archive.org was unreachable. | [P1] rpstrength.com `/blogs/articles/<muscle>-hypertrophy-training-tips` for chest, back, biceps, triceps, quad, hamstring, glute, side-delt, rear-delt, front-delt, calves, trap, ab, forearm; [P2] [Arvo](https://arvo.guru/resources/volume-training) |
| 10 | Weekly frequency per muscle 2-4x, 2-3x typical (KQ6, via skills.cat) | Unverified | **Corrected (muscle-dependent).** RP chest guide: 2-4x/week; triceps: 2-4 sessions/week; biceps guide: 3-6x/week. There is no single RP figure. | [P1] RP chest, triceps and biceps guides (row 9) |
| 11 | RP mesocycle: start near MEV, add ~1 set per muscle per week over 4-6 weeks, deload ~1 week at ~50% volume (KQ6, Arvo) | Third-party | **Corrected.** RP's example climbs from MEV 12 to 20 sets in **+2-set** steps over 5 weeks. Its feedback table adds 2-3 sets when recovery and stimulus scores are low. The deload drops to **MV levels** (6 sets in the example, about 30% of the peak), then a new mesocycle restarts at MEV. | [P1] [RP landmarks article](https://rpstrength.com/blogs/articles/training-volume-landmarks-muscle-growth) |
| 12 | RP physique templates usable 3-6 days; simplified templates 2-4 days; prices unconfirmed (KQ5, KQ6, KQ9) | Low-quality aggregator | **Corrected.** rpstrength.com now lists a **Simple Training Template**: $119.99, male or female, **2, 3 or 4 days**. Its Q&A says the day count chosen at purchase is fixed. The old male-physique-template URL redirects to the templates collection, which no longer lists 3-6-day physique templates, and RP's Q&A says the app is "the next iteration" of those templates. RP also offers free 3-day and 4-day full-body templates. The cited aggregator (chw.dhis2.org) failed to connect (proxy 502) and looks unrelated to RP; drop it. | [P1] [RP Simple Training Template](https://rpstrength.com/products/simple-training-templates); [RP free templates](https://rpstrength.com/pages/hypertrophy-training-templates) |
| 13 | RP Hypertrophy app price (KQ9 Gap) | Gap | **Gap filled.** $34/month billed monthly, or $299.99 billed yearly (advertised as "$24/month"). | [P1] [RP app page](https://rpstrength.com/pages/hypertrophy-app) |
| 14 | 5/3/1 four-week wave (65/75/85 x 5/5/5+; 70/80/90 x 3/3/3+; 75/85/95 x 5/3/1+; deload 40/50/60 x 5), TM 90%, +5 lb upper / +10 lb lower per cycle, 3 or 4 days (KQ3) | Mirrors | **Confirmed** in Wendler's own 2009 article. It states "three or four days a week", one core lift per workout, and percentages of 90% of the 1RM. Strength outcome. | [P1] **(older)** Wendler, "5/3/1: How to Build Pure Strength", T Nation (repost: [t-nation.com](https://t-nation.com/t/5-3-1-how-to-build-pure-strength/281694)) |
| 15 | TM 85%; "if you can't hit 5 reps at 95%, wrong TM" | Guide/04 from Wendler site | **Confirmed**, stated inside the "5/3/1 for Hardgainers" template (4 days, TM 85%). | [P1] [jimwendler.com Hardgainers](https://www.jimwendler.com/blogs/jimwendler-com/5-3-1-for-hardgainers) (2016-06-30) |
| 16 | Cut TM 10% when prescribed minimum reps are repeatedly missed (KQ3, Strength Insider) | Secondary | **Still unverified.** Not found on jimwendler.com. Wendler's site does host "The Training Max: What You Need to Know" (2016-12-03), which quotes forum moderator Kevin Deweese describing "5 forward / 3 back" resets: three cycles up, then the TM drops by three increments. Those are not Wendler's own words. | [P1/P2] [jimwendler.com Training Max](https://www.jimwendler.com/blogs/jimwendler-com/101082310-the-training-max-what-you-need-to-know) |
| 17 | BBB = 5x10 after the main lift; the 5x10 can be the same lift or its opposite ("flip side") (KQ3) | Wendler page via snippet | **Confirmed.** Two example layouts: same lift, or opposite lift (press/bench and squat/deadlift swapped). "Best used in a 3 or 4 day training program." Deload week: keep the 5x10 or cut to 3x10. | [P1] **(older)** [Wendler, Boring But Big](https://www.jimwendler.com/blogs/jimwendler-com/101077382-boring-but-big) (2013-05-20) |
| 18 | BBB loads "50-60% of TM ('the whole goal is to get 5 sets of 10')", cycle 1 at 30-50%, beginners ~30% (KQ3) | Wendler pages via snippet | **Corrected.** The BBB article's progression is **cycle 1 at 30% of TM, cycle 2 at 45%, cycle 3 at 60%, then 60% for all later cycles** (the TM rises, so the load does too). It also shows ascending, descending and up/down 30-70% patterns as examples. The phrase "the whole goal is to get 5 sets of 10" was not found; the closest wording is "the important thing is to perform the 5x10 work". "30-50%" comes from a different post, "BBB and Really Sore" (2015-10-14), a squat-only variant that climbs from 5x10 to 5x12, 5x15 and 5x20 at 30-50% of TM, run on the book's 3-day/week alternating program and "not on a 4 day/week program". | [P1] **(older)** BBB article (row 17); [Wendler, BBB and Really Sore](https://www.jimwendler.com/blogs/jimwendler-com/101082438-boring-but-big-and-really-sore) |
| 19 | BBB 3-Month Challenge 50% / 60% / 70% of TM (KQ3) | Wendler page via snippet | **Confirmed**, with a detail the note lacked: in the challenge the 5/3/1 last sets are **not** AMRAP ("only do the required reps"). The 5x10 is done with the opposite lift. Assistance is one push, one pull and one ab movement at 25-30 total reps each. | [P1] [Wendler, BBB 3-Month Challenge](https://www.jimwendler.com/blogs/jimwendler-com/boring-but-big-3-month-challenge) (2017-01-11) |
| 20 | Boring But Strong page on Wendler's site (KQ3) | Cited URL | **Corrected (citation).** `jimwendler.com/2014/07/boring-but-strong-challenge/` 301-redirects to the BBB 3-Month Challenge, so BBS is not documented at that URL. | curl redirect check |
| 21 | Training Templates eBook: 14 templates incl. "3 Days Per Week (The origin of 5/3/1)" and "The Twice A Week"; used as evidence of official 5/3/1 2- and 3-day templates (KQ2, KQ7) | Store page via snippet | **List confirmed; interpretation corrected.** EliteFTS, $29.95, 24 pages, "originally produced as a softcover manual" of powerlifting templates. Most entries are not 5/3/1 (e.g. Dave Tate Express, Bob Youngs' Beginner Program). "The Twice A Week" is one entry in this older manual; nothing on the page says it is a 5/3/1 template. Better primary evidence for 5/3/1's 2/3/4-day support is in rows 22-25. | [P1] [EliteFTS Training Templates](https://elitefts.com/products/training-templates-by-jim-wendler-ebook) |
| 22 | 5/3/1 officially supports 2, 3 or 4 days (KQ7) | Lift Vault | **Confirmed.** 5/3/1 2nd Edition eBook ($22, 133 pp.): "Flexible enough to fit any schedule — 2, 3, or 4 days per week". Beyond 5/3/1 eBook ($25, 131 pp.) lists "2-day/week templates". | [P1] [5/3/1 2nd Ed.](https://www.jimwendler.com/products/5-3-1-second-edition-ebook); [Beyond 5/3/1](https://www.jimwendler.com/products/beyond-5-3-1-ebook) |
| 23 | Wendler "I don't have a set schedule" template (KQ2, KQ7 Gap) | Not found | **Content confirmed; exact phrase still not found.** Wendler's "Training for Inconsistent and Busy Men" (2023-04-17) is the variable-schedule template. Days per week are up to you; some weeks 2, others 4; the goal is at least 2 sessions. One main lift per day, no exceptions, so consecutive days are allowed. A pull assistance movement (50-100 total reps) is done every session. With more time, add a push or single-leg/core movement and then a third. On a bad day, use the 5's Progression. This matches the note's "rotate the four lifts through whatever days are available" description. | [P1] [Wendler, Training for Inconsistent and Busy Men](https://www.jimwendler.com/blogs/jimwendler-com/training-for-inconsistent-and-busy-men) |
| 24 | On 3 days the 4 workouts rotate and a cycle takes 5+ weeks (KQ2, KQ7, Muscle & Strength) | Secondary | **Still unverified.** muscleandstrength.com returned 403. Wendler's BBB-and-Sore post refers to "the 3 day/week training program outlined in the book (alternating upper and lower body)" without detail. | [P1] row 18 post |
| 25 | 2-day 5/3/1: bench + squat one day, press + deadlift the other (KQ2, SS forum) | Forum | **Partly confirmed.** A reader letter published on Wendler's site (2016-11-10) describes "two days a week doing two lifts per day" on Wendler's advice; the pairings are not stated. A separate Wendler 2-day plan, Krypteia 2 Days/Week (2021-10-06), uses **one** main lift per day (2 per week, all 4 every 2 weeks) with 5's PRO + 5x5 FSL. | [P1] [Training 2 Days/Week](https://jimwendler.com/blogs/jimwendler-com/training-2-days-week-lifting-through-med-school-or-how-busy-taxpayers-find-balance); [Krypteia 2 Days/Week](https://www.jimwendler.com/blogs/jimwendler-com/krypteia-2-days-week) |
| 26 | 5/3/1 Forever: paid; "over 50 templates"; leader/anchor structure (KQ3) | AbeBooks / LiftProof | **Paid status confirmed with detail:** paperback $40; jimwendler.com states no authorized eBook or PDF exists. The page does not give a template count or describe leader/anchor; those stay unverified (row-level note in "Still unverified"). | [P1] [jimwendler.com 5/3/1 Forever](https://www.jimwendler.com/products/5-3-1-forever-book) |
| 27 | GZCLP rules; three-way conflict on the restart after 10x1+ fails (KQ3) | Conflict across mirrors | **Corrected (conflict resolved).** On the author-partnered Boostcamp page: T1 starts at 85% of 5RM, 5x3, +5 lb (2.5 kg) bench/OHP and +10 lb (5 kg) squat/deadlift each workout. On a miss, keep the weight and go to 6x2, then 10x1. After 10x1 fails, rest 2-3 days, test a new 5RM, and restart 5x3 at **85%** of it. T2: 3x10, then 3x8, then 3x6; after 3x6 fails, restart 3x10 about **20 lb (10 kg)** above the last 3x10 weight. T3: 3x15, last set AMRAP; add the smallest increment at 25 reps; if 3x15 fails, lower 10-15%. 3 days/week for beginners, 4 for more experienced lifters. Free; listed as 12 weeks. thefitness.wiki [P2] agrees on 85% and gives T2 +15-20 lb. The "last 5x3 + 5-15 lb" and "deload 15%" variants are not the author's. | [P1] [Boostcamp GZCLP (Cody Lefever)](https://www.boostcamp.app/coaches/cody-lefever/gzcl-program-gzclp); [P2] [thefitness.wiki GZCLP](https://thefitness.wiki/routines/gzclp/) (read via WebFetch) |
| 28 | GZCL method tiers: T1 85-100% for 10-15 reps; T2 65-85% for 20-30; T3 <65% for 30+; 1:2:3 "framed as a weekly balance" (KQ6) | Mirrors | **Numbers confirmed; two nuances corrected.** Lefever's 2012 post defines the percentages against a **goal weight**; training maxes appear in his 2016 post, which gives T1 "base 10 peak 15 at 85-100%". The 1:2:3 rule is stated as tier volume (e.g. 10 T1 reps → at least 20 T2 and 30 T3) without saying "weekly"; the weekly framing comes from secondary sites. | [P1] **(older)** [Lefever 2012, The GZCL Method for Powerlifting](https://swoleateveryheight.blogspot.com/2012/11/the-gzcl-method-for-powerlifting.html); [P1] [Lefever 2016, GZCL Applications & Adaptations](https://swoleateveryheight.blogspot.com/2016/02/gzcl-applications-adaptations.html) |
| 29 | StrongLifts increments: +2.5 kg upper per workout; deadlift "+5 kg vs +10 lb is the real discrepancy" (KQ2) | App listing / FitnessVolt | **Corrected.** The official default is **+5 lb (2.5 kg) per workout on squat, bench, OHP and row**. Men can add 10 lb (about 5 kg) per workout on the deadlift until it gets hard, then 5 lb. Women do better with 2.5 lb jumps on bench and OHP. 5 kg and 10 lb are the same practical increment, so there is no real discrepancy. Squat is +5 lb, not an upper-body-only figure. | [P1] [StrongLifts, Progress](https://stronglifts.com/stronglifts-5x5/progress/) |
| 30 | StrongLifts: fail 3 workouts at a weight → reduce that lift 10% (KQ2) | Mirrors | **Confirmed.** Repeat the weight; if it still fails after three attempts, "reduce the weight by about 10%" (the app does this automatically). | [P1] [StrongLifts, Failure](https://stronglifts.com/stronglifts-5x5/failure/) |
| 31 | StrongLifts switch to 3x5 / 3x3 / 1x5 after repeated deloads (KQ2 Gap) | Gap | **Still unverified, and probably retired.** The current official plateau and failure pages do not contain it. They advise microloading (2.5 lb or less), adding weight every 3 workouts instead of every workout, top/back-off sets, fewer squat sessions, more exercise variety and bench volume, or switching to StrongLifts 5x5 Intermediate or Madcow. | [P1] [StrongLifts, Plateaus](https://stronglifts.com/stronglifts-5x5/plateaus/) |
| 32 | StrongLifts app free vs paid tier (KQ9 Gap) | Gap | **Partly filled.** The app is a free download with a paid "Stronglifts Pro" tier (the newsletter offers 10% off Pro). The Pro price is not shown on stronglifts.com. | [P1] [StrongLifts app](https://stronglifts.com/app/) |
| 33 | Madcow ramp interval 12.5% (KQ2) | StrongLifts | **Confirmed** (default 12.5% between ramp sets). | [P1 for the StrongLifts version] [StrongLifts, Madcow interval](https://stronglifts.com/madcow-5x5/interval/) |
| 34 | Madcow weekly progression 2.5%/week (KQ2 Gap) | Gap | **Still unverified against the original; conflict recorded.** StrengthLog says "every week, all the weights above increase by 2.5%" and gives Wednesday as squat 2x5 at 65% 1RM, OHP and deadlift x5 at 80%. StrongLifts' version instead adds a **fixed 5 lb** to the Monday (Workout A) top set each week the top set is completed, and lists Wednesday as squat 4x5. The original Madcow page (geocities, lost in 2009) was not reachable. | [P2] [StrengthLog Madcow](https://www.strengthlog.com/madcow-5x5/) (via WebFetch); [P2] [StrongLifts Madcow guide](https://stronglifts.com/madcow-5x5/workout-guide/) |
| 35 | Texas Method: light day ~80% of Monday; volume-day stall → 6x4 or 8x3; intensity day cycles 2x3, 3x2, 2x2, 5 singles, then a new 5RM (KQ2) | Snippets | **Confirmed** by a full read of Barbell Logic. Monday 5x5 at about 90% of the 5RM is from Rippetoe's article, seen **only as a search snippet** (startingstrength.com 403). | [P2] [Barbell Logic, Texas Method explained](https://barbell-logic.com/the-texas-method-explained/) |
| 36 | Starting Strength layout, increments, phases, stall rule (KQ2) | Secondary | **Still unverified.** startingstrength.com (programs page, articles, PDFs) returned a Cloudflare 403. A search-engine summary of the official programs page gives A = squat 3x5, press 3x5, deadlift 1x5 and B = squat 3x5, bench 3x5, power clean 5x3. It says most healthy men about 18-35/40 can add **10 lb** to the squat for the first few sessions, which is larger than the note's +5 lb. Unconfirmed until the page can be read. | search snippet only |
| 37 | Reddit PPL set/rep scheme, increments and deload (KQ5 Gap) | Gap | **Still unverified against the original post** (reddit.com 403). The Liftosaur mirror [P2] gives deadlift 1x5+; bench, OHP and row 4x5 + 1x5+; squat 2x5 + 1x5+; accessories 3x8-12 (face pulls and lateral raises 15-20); +5 lb per session on bench, OHP, row and squat and +10 lb on the deadlift; 10% deload after 3 consecutive failed sessions. | [P2] [Liftosaur Metallicadpa PPL](https://www.liftosaur.com/programs/metallicadpappl) |
| 38 | PHUL per-exercise set counts (KQ3 Gap) | Gap | **Gap filled.** Boostcamp (officially partnered with Brandon Campbell), week 1: mostly 3 sets per exercise (OHP, curls and skull crushers 2; seated calf raise 4), with an optional extra set shown as "3-4". Power days 3-5 reps on the main lifts and 6-10 on accessories. Hypertrophy days 8-12 (leg press, leg extension and leg curl 10-15). All sets around RPE 9 (about 1 RIR). Add weight or reps every workout while at RPE 8-9. About 60 min; 12 weeks; free; 6-18 months of training suggested. | [P1] [Boostcamp PHUL (Brandon Campbell)](https://www.boostcamp.app/coaches/brandon-campbell/phul-4-day-split) |
| 39 | PHAT: hypertrophy days at 6-10 reps near failure; power days start at 70-80% 1RM; run as three 4-week cycles (KQ4) | FitnessVolt / Lift Vault | **Corrected.** Norton's own article: power days use 3-5 working sets of 3-5 reps on one compound per pattern (accessories 6-10). Hypertrophy days **open with speed work, 6-8 sets of 3 at 65-70% of the 3-5RM** (<= 90 s rest), then bodybuilding work at **8-20 reps** with 1-2 min rest and about 50-75% more volume than power days. No failure in the first 2-4 weeks; later only the last 1-2 sets. Deload every 6-12 weeks for 1-3 weeks at 60-70% of normal loads. The 70-80% start and the "three 4-week cycles" do not appear in Norton's text. Boostcamp lists 5 days, ~90 min, intermediate-advanced, free. | [P1] [Norton, PHAT (biolayne.com)](https://biolayne.com/articles/training/phat-power-hypertrophy-adaptive-training/); [P1] [Boostcamp PHAT](https://www.boostcamp.app/coaches/layne-norton/phat) |
| 40 | PHAT origin date (2008 vs SimplyShredded 2011) (KQ4) | Conflict | **Still unverified.** The biolayne page carries datePublished 2016-05-30, which is a repost date. | [P1] as row 39 |
| 41 | Juggernaut realization back-downs "75/80/85/90% across the four waves" attributed to JTS (KQ3) | JTS snippet | **Corrected (attribution).** The JTS article ("Going Heavy on the Juggernaut Method", Chad Wesley Smith, 2013-01-16) does not give those figures; it explains how to add heavy 5/3/2/1-rep sets. Its 5s-wave example shows accumulation as "up to 6x5 at 70%", which conflicts with Lift Vault's 4x5 + 1x5+ at 70%. The 75/80/85/90% realization AMAP loads (10s/8s/5s/3s), intensification at 67.5/72.5/77.5/82.5%, deload at 40/50/60% and TM at 90% come from Lift Vault's rebuild of the base template [P2]. | [P1] **(older)** [JTS](https://www.jtsstrength.com/going-heavy-on-the-juggernaut-method/); [P2] [Lift Vault Juggernaut](https://liftvault.com/programs/strength/juggernaut-method-base-template-spreadsheet/) |
| 42 | Juggernaut TM-increase formula (KQ3 Gap) | Gap | **Still unverified.** Lift Vault says only that more reps above the target give a larger TM increase. | [P2] as row 41 |
| 43 | nSuns: start on 4 days, move to 5 days after 2-3 months; AMRAP-based TM increase (KQ3, KQ4) | Mirrors | **Confirmed** (Lift Vault). TM increase by reps on the "1+" set: 0-1 reps +0; 2-3 reps +5 lb; 4-5 reps +5-10 lb; 6+ reps +10-15 lb. There is also a 6-day PPL variant. The original is a Reddit spreadsheet, not reachable. | [P2] [Lift Vault nSuns](https://liftvault.com/programs/powerlifting/n-suns-lifting-spreadsheets/) |
| 44 | nSuns T1 / T2 percentage tables (KQ3 Gap) | Gap | **Still unverified.** The tables are inside the spreadsheets, not on the page. | — |
| 45 | Candito 6-week: 6 weeks, free, sessions vary by week (KQ3, KQ7) | Secondary | **Confirmed** on Boostcamp (officially partnered with Candito; free, with in-app donation). Week 1 shows 5 sessions (days 1, 2, 4, 5, 6). Phases: conditioning, hypertrophy, linear max OT, heavy/explosive, intense strength, deload/test. The Boostcamp header's "7 days/week" looks like a listing error. Candito's own site URL returned 404. | [P1] [Boostcamp Candito](https://www.boostcamp.app/coaches/jonnie-candito/candito-6-week-strength-program) |
| 46 | Nuckols 28 programs: free for email; squat, bench, deadlift; by level and days per week (KQ6) | Lift Vault | **Confirmed.** SBS: "28 one-lift routines for squat, bench, and deadlift with variations for your skill level and the number of days per week you want to train", free with newsletter signup. | [P1] [SBS newsletter / free resources](https://www.strongerbyscience.com/newsletter/) |
| 47 | SBS Program Bundle: six 21-week autoregulated programs, free with signup (KQ6) | Lift Vault | **Confirmed, with a new detail relevant to KQ7:** "Options for training 2x, 3x, 4x, 5x, and 6x per week". It includes strength, hypertrophy, linear-progression and novice-hypertrophy versions plus a program builder, and is "completely free". | [P1] [SBS Program Bundle](https://www.strongerbyscience.com/program-bundle/) |
| 48 | Helms Pyramid concrete numbers (KQ6 Gap) | Gap | **Gap filled** from the 3rd-edition sample chapter (Helms, Morgan & Valdez; page first published 2019-02-26, modified 2026-01-08), Table 7.3. Hypertrophy: minimum ~4 sets/muscle/week; "practical" **10-20**; maximum ~30; ~4-30RM loads; frequency >= 1x/muscle/week; above 11 weekly sets, raise frequency so **no session exceeds ~11 fractional sets per muscle**. Strength: 3-5 sets/lift/week short-term, 5-10 sets/muscle long-term, 1-8RM, 2-6x/lift/week. Text: "For ~90% of lifters, train 3-5 days per week with a muscle/movement frequency of 2-4 times per week." Practitioner book, not peer-reviewed. | [P1] [RippedBody sample chapter](https://rippedbody.com/how-to-build-training-programs/) |
| 49 | Arnold Blueprint days per week (KQ1 Gap) | Gap | **Still unverified at the primary source** (bodybuilding.com URLs now 404). A secondary write-up (T3) describes 6 days/week, 8 weeks in two 4-week phases, chest+back / shoulders+arms / legs twice. | [P2] [T3](https://www.t3.com/features/arnold-schwarzenegger-8-week-strength-bulk-workout-plan) |
| 50 | Kris Gethin 12-Week Trainer days per week (KQ4 Gap) | Gap | **Still unverified.** A search snippet of the bodybuilding.com listing says 5 workouts/week, advanced, about 60 min; the page itself is now 404. | snippet only |
| 51 | Shortcut to Size (4/week, 45-60 min) and LiveFit (5/week, 12 weeks) via Bodybuilding.com (KQ1, KQ4, KQ8) | Bodybuilding.com pages | **Still unverified now.** Every cited bodybuilding.com URL (10 most popular, LiveFit, Squat Bigger with GZCL) redirects to a 404 on shop.bodybuilding.com, so these figures can no longer be checked at source. | curl redirect check |
| 52 | Other cited mirrors | — | **Corrected (dead or unreliable links).** `reddit.sudovanilla.org/r/gzcl/wiki/GZCL` returns 404 (use the Lefever posts in row 28). The RP aggregator `chw.dhis2.org` would not connect (row 12). `amp.bodybuilding.com` would not connect. | curl checks |
| 53 | Lyle McDonald GBR details (KQ3) | Secondary | **Still unverified.** The original bodyrecomposition.com forum post was not found (guessed URL 404). | — |
| 54 | Greyskull LP rules (8-10 rep start, +2.5 / +5 lb, 10% reset) (KQ2) | Secondary | **Still unverified.** No author or publisher page was found. | — |
| 55 | Sheiko cycle descriptions and session lengths (KQ2, KQ6) | Boostcamp / Liftosaur | **Still unverified.** Not re-checked in this pass. | — |

**Counts:** 55 claims checked. **23 confirmed** (gaps filled included): rows 1, 3, 4, 6, 8, 13, 14, 15, 17, 19, 22, 23, 25, 26, 30, 33, 35, 38, 43, 45, 46, 47, 48. **16 corrected:** rows 2, 5, 7, 9, 10, 11, 12, 18, 20, 21, 27, 28, 29, 39, 41, 52. **16 still unverified:** rows 16, 24, 31, 32, 34, 36, 37, 40, 42, 44, 49, 50, 51, 53, 54, 55.

### Corrections

1. **Schoenfeld, Grgic & Krieger 2019** found no significant hypertrophy difference between frequencies when volume was equated. The note's KQ1 line saying higher frequency "still gave somewhat more growth" with sets matched is wrong. The benefit appears only in non-volume-equated studies. [PR]
2. **Nippard Essentials is paid** ($39.99) and comes in 2x/3x/4x/5x versions. The Boostcamp "Essentials" pages are community uploads of a paid product, not free official versions. This affects KQ4, KQ6, KQ7, KQ9 and the Quick index (2-day, 3-day and 5-day lines).
3. **Nippard Essentials 5x is upper / lower / push / pull / legs.** A named author therefore does publish the PPL + upper/lower 5-day hybrid (paid; numbers not public). This corrects the KQ1 and KQ4 statements that no primary source defines it. Session-length data is still absent, apart from Essentials' "under 45 minutes".
4. **Fundamentals $39.99 is the regular price**, not a sale price.
5. **RP's landmark values:** RP publishes its own per-muscle tables (row 9). The third-party figures in KQ6 (FitnessVolt and Arvo chest MEV 10 / MRV 22) do not match RP's current chest values (MV 2-4 / MEV 4-6 / MAV 6-16 / MRV 16-24). RP's frequency advice is muscle-specific (chest 2-4x, biceps 3-6x).
6. **RP mesocycle:** RP's own example adds about 2 sets per week, not about 1. It deloads to MV (about 6 sets), not "~50% volume".
7. **RP templates:** the current product is the 2/3/4-day Simple Training Template at $119.99, with the day count fixed at purchase. 3-6-day physique templates are no longer listed, and the app ($34/month or $299.99/year) is RP's stated successor. Drop the chw.dhis2.org citation.
8. **BBB loading:** Wendler's BBB article gives 30% → 45% → 60% of TM over the first three cycles, then 60%. "50-60%" and "the whole goal is to get 5 sets of 10" were not found. "30-50%" belongs to the squat-only "BBB and Really Sore" variant (5x10 → 5x20, 3 days/week only). The 3-Month Challenge (50/60/70%) drops the AMRAP on the main lift.
9. **Wendler Training Templates eBook** is an older powerlifting manual, not a set of 5/3/1 2- and 3-day templates. Cite the 5/3/1 2nd Edition ("2, 3, or 4 days per week"), Beyond 5/3/1 ("2-day/week templates"), Krypteia 2 Days/Week and "Training for Inconsistent and Busy Men" instead.
10. **Boring But Strong URL** redirects to the BBB 3-Month Challenge.
11. **GZCLP restart rule** (author-partnered): retest the 5RM after 2-3 rest days and restart at 85%. T2 restarts about 20 lb (10 kg) above the last 3x10 weight. T3 drops 10-15% on failure. The other two KQ3 variants are not the author's.
12. **GZCL tiers** were defined against goal weight in 2012, and the 1:2:3 rule is not framed as weekly in the original.
13. **StrongLifts increments:** the default is +5 lb (2.5 kg) per workout on all lifts including squat, with the deadlift at +10 lb (about 5 kg) for men until it slows. The "5 kg vs 10 lb discrepancy" in KQ2 is not a discrepancy.
14. **PHAT** (Norton): hypertrophy days are speed work (6-8 x 3 at 65-70% of 3-5RM), then 8-20 reps. They are not "6-10 reps near failure". Deload every 6-12 weeks for 1-3 weeks at 60-70%.
15. **Juggernaut:** the 75/80/85/90% realization figures come from Lift Vault's rebuild, not JTS. JTS's own 5s-wave example (6x5 at 70%) conflicts with Lift Vault's 4x5 + 1x5+.
16. **SBS citation:** `/frequency/` and `/frequency-muscle/` are one article (redirect).
17. **Dead links:** all bodybuilding.com citations, the reddit.sudovanilla.org GZCL wiki mirror, and chw.dhis2.org.

### Still unverified

- Starting Strength program text, increments and phases (startingstrength.com behind Cloudflare). A search snippet suggests early squat jumps of 10 lb for most young men, which conflicts with the note's +5 lb.
- Reddit PPL original post: scheme, increments and deload (reddit.com blocked; only the Liftosaur mirror was read).
- Madcow's original weekly progression: 2.5%/week (StrengthLog) vs fixed +5 lb/week (StrongLifts' version).
- 5/3/1: the 3-day rotation and "5+ week" cycle wording (Muscle & Strength 403); a 10% TM cut as Wendler's rule; *5/3/1 Forever*'s template count and leader/anchor details (book only); the exact phrase "I don't have a set schedule" (its content is confirmed, row 23).
- StrongLifts Pro price; the old 3x5 / 3x3 / 1x5 switch rule (absent from current official pages).
- Juggernaut TM formula; nSuns percentage tables; PHAT origin year; Lyle GBR original; Greyskull LP rules; Sheiko details.
- Arnold Blueprint, Kris Gethin 12-Week, Shortcut to Size and LiveFit figures (bodybuilding.com pages gone).
- Older RP chest landmarks (MV 8 / MEV 10 / MAV 12-20 / MRV 22) and RP's session-count MRV statement (web.archive.org unreachable).

### Implications for the guide

The guide and templates were not edited in this pass. Suggested changes:

1. **`guide/02-program-structures.md` §2 "Jeff Nippard Essentials ..." (lines ~153-160), §4 "Fundamentals body-part track and Essentials 5x" (~275) and §7 table row "Nippard Essentials / Fundamentals ... Free / $39.99" (~363).** Change "Essentials is free on Boostcamp in 2-, 3-, and 5-day versions" and "Essentials free" to: paid, $39.99, 2/3/4/5 days, sessions under 45 min, three 4-week blocks. Note that the Boostcamp copies are unofficial uploads. In the table, make Free? read "Paid ($39.99 each)". Optionally add Powerbuilding: $49.99, 10 weeks, 4x or 5-6x versions, alternating full-body and upper/lower weeks; **Partly** (fixed per block).
2. **`guide/02` §4 "Generic PPL + upper/lower hybrid" (~287), §7 row "PPL + U/L hybrid ... n/a" (~373), and `templates/5-day-week.md` Sources line (~159) "the PPL + U/L hybrid has no primary author".** Replace with: Nippard's Essentials 5x uses upper / lower / push / pull / legs (paid; numbers not reproduced). The repository's 5-day template remains its own parameterisation.
3. **`guide/02` §2 "5/3/1 on 2 or 3 days" (~91, ~96).** Replace the Training Templates eBook as evidence (it is a pre-5/3/1 powerlifting manual) with the 5/3/1 2nd Edition "2, 3, or 4 days", Beyond 5/3/1's 2-day templates, and Krypteia 2 Days/Week (one lift per day, all four lifts every two weeks). Replace "'I don't have a set schedule' template could not be located (unverified)" with a citation to Wendler's "Training for Inconsistent and Busy Men" (2023): 2-4 days, varying week to week; one main lift per session; a pull every session. This is the strongest named-author support for the repository's rotation design, and it also strengthens §8.
4. **`guide/02` §3 5/3/1 Layout (~178).** Change "Boring But Big adds 5x10 ... at 50-60% of TM" to Wendler's BBB progression: 30% → 45% → 60% of TM over three cycles, then 60%. Add that the 3-Month Challenge (50/60/70%) uses no AMRAP on the main sets.
5. **`guide/02` §2 GZCLP Progression (~82).** Replace the three-way "(conflict noted)" with the author-partnered rule: retest the 5RM and restart at 85%; T2 restart about 20 lb above the last 3x10 weight; T3 -10-15% on failure. The Weaknesses line "stall rule conflicts across mirrors" can go. `guide/04` lines ~107 and ~219 already match.
6. **`guide/02` §2 StrongLifts (~49) and `guide/04-periodization-and-progression.md` table row (~66).** Replace "deadlift +5 kg or +10 lb depending on the source (the real discrepancy)" with: +5 lb (2.5 kg) per workout on every lift; deadlift +10 lb for men until it slows. Replace "switch to 3x5 / 3x3 / 1x5 ... (unverified)" with the current official plateau advice (microload, slower progression, top/back-off sets, fewer squat days, or move to an intermediate program).
7. **`guide/02` §2 Madcow (~115) and §7 row "Per week (2.5% unverified)" (~359).** State the conflict: StrengthLog 2.5%/week vs StrongLifts' fixed +5 lb/week on the Monday top set. The original is unverified.
8. **`guide/02` §3 PHUL (~205-207).** Replace "Per-exercise set counts not stated in any snippet" and "not specified by the author" with: 2-4 sets per exercise (3-4 with the optional set), about RPE 9, add weight or reps each session; about 60 min (author-partnered Boostcamp).
9. **`guide/02` §4 PHAT (~260-262).** Change "Power days ~3 sets of 3-5 at 70-80% 1RM; hypertrophy days ... at 6-10 reps near failure" to Norton's text: power 3-5 sets of 3-5; hypertrophy days speed work 6-8 x 3 at 65-70% of 3-5RM, then 8-20 reps with 1-2 min rest. Replace "deload every 6-12 weeks" with "deload every 6-12 weeks for 1-3 weeks at 60-70%". "Three 4-week cycles" is FitnessVolt's, not Norton's.
10. **`guide/02` §3 Juggernaut (~238).** Attribute "75/80/85/90%" realization loads to the Lift Vault rebuild [P2], not JTS. Note that JTS's own example lists 5s-wave accumulation as 6x5 at 70%.
11. **`guide/02` §5 RP entry (~321-322) and §7 row "RP templates / app | 3-6" (~376).** Replace "physique templates are sold in 3- to 6-day versions" with: Simple Training Template, 2/3/4 days, $119.99, day count fixed at purchase; the app ($34/month or $299.99/year) supersedes the physique templates; free 3- and 4-day templates. Change "add roughly a set per muscle per week ... deload at ~50% volume" to RP's example: about +2 sets/week, deload to MV.
12. **`guide/02` §6 framework table, Helms row (~341).** Replace "Concrete numbers not retrieved" with the sample-chapter figures: 10-20 sets/muscle/week practical (minimum ~4, maximum ~30); >= 1x/muscle/week; no session above ~11 fractional sets per muscle; 3-5 days with 2-4x frequency for most lifters. The same ~11-set cap independently supports **`guide/03-flexible-scheduling.md` §2.2 (~87)**, which currently rests on a secondary, unverified Remmert summary. Cite Helms as a practitioner corroboration.
13. **`guide/02` §8 / §7 footer (~378), "No commercially published program formally scales 3 to 6 days inside one plan".** Still true as worded, but add the day-count-selectable families: SBS Program Bundle (free, 2-6x options), Nippard Essentials (2-5x) and Powerbuilding (4 or 5-6x). All are chosen per block. Wendler's "Inconsistent and Busy" article is the one named-author plan that floats week to week.
14. **`guide/01-training-principles.md` §1 RP landmarks paragraph (~69) and table row "RP chest example" (~88)** (sourced from the FVI note, flagged here because it conflicts). "The only official per-muscle example is chest, at MV ~4-6, MEV ~6, MRV ~20 sets at 2 sessions and ~25 at 3" does not match RP's current pages. RP publishes tables for 14 muscles, and chest is MV 2-4 / MEV 4-6 / MAV 6-16 / MRV 16-24 with no session-count MRV statement. The cited URL `rpstrength.com/chest-training-tips-hypertrophy/` now redirects to the new chest guide. The "~8-10 set per-session ceiling" inference drawn from it needs a different basis (e.g. Helms' ~11, implication 12). `guide/04` line ~176 already quotes RP's current chest values correctly.
15. **`guide/04` 5/3/1 bullet (~94).** "5 forward, 3 back" can be cited to jimwendler.com's "The Training Max" (2016), noting that it quotes forum moderator Kevin Deweese, not Wendler.
16. **`templates/progression-tracks.md` (~47).** "GZCLP restarts a stalled lift at about 85% of a fresh 5RM" and "5/3/1 TM 85-90%, top week 95%" are confirmed at author sources. "Greyskull starts at a weight you can lift 8-10 times" is still unverified.
