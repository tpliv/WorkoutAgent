# Portability

Last updated: 2026-11-13 (scheduled tasks recorded with their prompts; the default-branch and repository-attachment checks; old repo URLs replaced). Earlier: 2026-10-26 (the repo now lives at `tpliv/WorkoutAgent`)

How to move this project off work accounts (Claude and GitHub) without losing
anything. The rule that makes it possible: **the GitHub repository is the only
source of truth.** The Claude account holds only settings that can be
recreated from this file. The repo itself moves to a personal GitHub account
with its full history (see "Moving the GitHub repo").

## What lives where

| Item | Lives in | Moves with the repo? | What to do on a move |
| --- | --- | --- | --- |
| Research, guide, templates, tools, `CLAUDE.md` | GitHub repo `tpliv/WorkoutAgent` (personal; moved from `tlee-ui/WorkoutTrainer`) | Yes | Copy the repo to a personal GitHub account (below) |
| Training log and track state (`data/`) | GitHub repo | Yes | Same |
| Link between Claude and GitHub | Claude account (GitHub connection and Claude GitHub App) | No | Connect GitHub from the new Claude account |
| Cloud environment: network access, Hevy secret | Claude account (environment settings) | No | Recreate from the spec below |
| Hevy API key | Hevy account, plus a copy in the old environment | Key: yes. Copy: no | Regenerate the key, store it in the new environment |
| Scheduled tasks | Claude account | No | Recreate from "Scheduled tasks" below, **with the repository attached** |
| Progress dashboard page | Claude account (a private page; URL in `tools/README.md`) | No | Publish `dashboard/index.html` as a new page from the new account and replace the URL in `tools/README.md` |
| Session transcripts, other artifacts, memory | Claude account | No | Nothing to move if the rules below are followed |
| `Claude-Session:` links in commit messages | Claude account | No | None. They stop opening from another account; the commits are unaffected |

## Environment spec

Recreate this in the new account's cloud environment settings (the environment
menu in a session's title bar, then Edit).

| Setting | Value |
| --- | --- |
| Repository | `tpliv/WorkoutAgent`. On GitHub the **default branch must be `main`** (Settings, General, Default branch). A new session checks out the default branch; on 2026-11-13 it was still `claude/ecstatic-bardeen-tc62l0`, a commit from October, so new sessions started three weeks stale until they switched to `main`. |
| Network access | Allow `api.hevyapp.com`. Research sessions also need web search and fetch. |
| Hevy credential | A network secret for `api.hevyapp.com` that sends the key in the `api-key` header. Alternative: an environment variable named `HEVY_API_KEY`. `tools/hevy_pull.py` works with either. |
| Time zone | Optional environment variable `TRAINING_TZ` (IANA name). Default `America/New_York`, set in `tools/localtime.py`. Needs no package: Python's `zoneinfo` with the system tz database. |
| Setup script | None. The tools are Python 3 standard library only. |
| Connectors | Optional: Google Calendar, only to place workout holds on a calendar named "Workouts" when the lifter asks (90-min holds, shown as free). Nothing in the repo reads the calendar; `data/weekly-plan.md` is the record. The connector in use on 2026-11-06 is the lifter's work Google account; in a new account, create a "Workouts" calendar on a personal Google account or skip holds. No Gmail, Drive, or other connector. |

Never paste the key into a chat, a file in the repo, or a commit.

## Moving the GitHub repo

Commits are authored as `Claude <noreply@anthropic.com>`, and no credentials
are committed, so the history can be copied as is.

1. Create a personal GitHub account with a personal email.
2. Copy the repo with every branch and commit, into a **private** repo:
   - Without a command line: `https://github.com/new/import`, source URL
     `https://github.com/tpliv/WorkoutAgent.git`.
   - Or from any computer with git:
     `git clone --mirror https://github.com/tpliv/WorkoutAgent.git`, then
     in that folder `git push --mirror https://github.com/<you>/WorkoutAgent.git`.
3. To keep working from another Claude account during a transition: on the
   new repo, invite that account's GitHub user as a collaborator, and
   install the Claude GitHub App on the personal repo
   (`https://github.com/apps/claude/installations/select_target`). Work
   sessions then push to the personal repo. Cutting the work side off later is
   one click: remove the collaborator.
4. Update the repo name in this file and start new sessions on the personal
   repo. Archive or delete the copy under the work account.

## Migration checklist

1. Confirm everything is pushed: `git status` is clean and every branch you
   want is on GitHub. Merge working branches into the default branch.
2. In the new Claude account, connect GitHub at `https://claude.ai/connect-github`
   and give the Claude GitHub App access to the repository.
3. In Hevy, generate a new API key at `https://hevy.com/settings?developer`.
4. Create the cloud environment from the spec above and add the new key.
5. Start a session and check the link:
   `python3 tools/hevy_pull.py --inspect` should print one workout.
6. Recreate the scheduled tasks from "Scheduled tasks" below, each with the
   repository attached, and run each once to confirm it can sync (it prints
   `Sync complete`, not `Sync not started`).
7. In the old account: delete the environment (removes the old key copy),
   delete scheduled tasks, and disconnect GitHub or remove the repo from the
   Claude GitHub App's access. Revoking the old Hevy key is optional once the
   new one works.

Steps 2 to 5 are the whole move. Expect about 15 minutes.

## Rules that keep it portable

- Anything worth keeping goes in the repo and is pushed. Not in an artifact, a
  chat, memory, or only a scheduled task's prompt.
- If a scheduled task is worth keeping, record its schedule and prompt in
  `PORTABILITY.md` under "Scheduled tasks".
- Credentials come from the environment, never from files in the repo.
- No dependency on work connectors or work systems.
- New setup steps (packages, hosts, secrets) are added to the environment spec
  above in the same commit that needs them.

## Scheduled tasks

Two tasks run the coaching cadence (`coach/README.md`). Times are America/New_York.

**Each task needs the repository `tpliv/WorkoutAgent` attached with write access.** Check this first when a run misbehaves. A task that an agent creates from inside a session gets no repository (verified 2026-11-13: its sessions cannot clone or push, and have no tool to attach one). From late October to 13 Nov 2026 both tasks ran that way: every run synced Hevy from its own copy, could not push, and lost its commits, which is how Hevy, the plan and `main` came to disagree. Two ways to give a task the repository:

- Create or edit it in the Claude app (scheduled tasks or routines) and select the repository there.
- Or bind it to one long-lived session that was started on the repository (an agent can do this: a session created with the repository as its source can push, verified the same day). Every run then lands in that one conversation.

Since 2026-11-13 the tools refuse to sync from a session that cannot write to `main`, so a task without the repository does no harm; it sends a read-only message that says so.

| Task | Schedule | New session each run | Phone notification |
|---|---|---|---|
| Sunday training check-in | `CRON_TZ=America/New_York 47 18 * * 0` | yes | yes |
| Tomorrow's workout | `CRON_TZ=America/New_York 47 19 * * 1-6` | yes | yes |

Prompt, Sunday training check-in:

```
You are my strength coach running the weekly Sunday check-in for the WorkoutAgent repo (tpliv/WorkoutAgent).

Setup: work in the tpliv/WorkoutAgent checkout, on main. The checkout may start on another branch, so run `git fetch origin main && git checkout main && git merge --ff-only origin/main`. If the repo isn't checked out and you have an add_repo tool, attach tpliv/WorkoutAgent with push access and clone it.

Read `coach/README.md`, then follow `coach/sunday-checkin.md` exactly. `python3 tools/hevy_sync.py` is the only way anything is saved or sent to Hevy: it checks access, folds in my logged workouts, commits, publishes to main and updates my Hevy routines. You have my permission to let it commit and push the coaching state files to main and update my routines, even if your session names a different branch. Change the week only with `python3 tools/week.py`. Don't change any other files, and don't open a pull request.

If the sync prints "Sync not started", this session can't write to the repo: change nothing, and follow "When the repo is read-only" in `coach/README.md`.

Turn 1: sync, then send the recap and the five check-in questions as your final message and wait for my reply. Turn 2, after I answer: plan the week by the repo's rules with `tools/week.py`, sync again, and send the week plan plus Monday's workout. Loads in pounds, taken from the tools' output. Never invent results I haven't logged or told you.
```

Prompt, Tomorrow's workout:

```
You are my strength coach sending tomorrow's workout for the WorkoutAgent repo (tpliv/WorkoutAgent).

Setup: work in the tpliv/WorkoutAgent checkout, on main. The checkout may start on another branch, so run `git fetch origin main && git checkout main && git merge --ff-only origin/main`. If the repo isn't checked out and you have an add_repo tool, attach tpliv/WorkoutAgent with push access and clone it.

Read `coach/README.md`, then follow `coach/nightly-brief.md` exactly. `python3 tools/hevy_sync.py` is the only way anything is saved or sent to Hevy: it checks access, folds in my logged workouts, commits, publishes to main and updates my Hevy routines. You have my permission to let it commit and push the coaching state files to main and update my routines, even if your session names a different branch. Change the week only with `python3 tools/week.py`. Don't change any other files, and don't open a pull request.

If the sync prints "Sync not started", this session can't write to the repo: change nothing, and follow "When the repo is read-only" in `coach/README.md`.

Work out whether tomorrow (America/New_York) is a training day. If it is, your final message is tomorrow's full workout in the format of guide/08-weekly-coaching-cadence.md section 3.1, with the numbers from `python3 tools/week.py brief`. If it isn't, your final message is one line naming the next session. Never invent results I haven't logged or told you. If I reply, handle it as the runbook's "Replies" section says.
```

A third task exists in the account and is **not** part of the repo's cadence: "Sunday workout hold planning" (one-off, re-armed each week for Sunday 6:00 pm, bound to its own session). It asks which days to train and writes 90-minute holds on a "Workouts" calendar in a work Google account. It overlaps the check-in's question 4, runs 47 minutes before it, and reads the plan from Hevy rather than from `data/week.json`. If holds are still wanted, the cleaner shape is: the check-in plans the week, and the hold task (or the lifter) copies the sessions from `data/week.json` to the calendar afterwards. It uses a work connector, which the rules below rule out for a personal account.

## Running without Claude

The repo works on any machine with Python 3:

```bash
git clone https://github.com/tpliv/WorkoutAgent.git
cd WorkoutAgent
HEVY_API_KEY=... python3 tools/hevy_pull.py
python3 tools/analyze_history.py
```
