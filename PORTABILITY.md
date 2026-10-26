# Portability

Last updated: 2026-10-21

How to move this project off work accounts (Claude and GitHub) without losing
anything. The rule that makes it possible: **the GitHub repository is the only
source of truth.** The Claude account holds only settings that can be
recreated from this file. The repo itself moves to a personal GitHub account
with its full history (see "Moving the GitHub repo").

## What lives where

| Item | Lives in | Moves with the repo? | What to do on a move |
| --- | --- | --- | --- |
| Research, guide, templates, tools, `CLAUDE.md` | GitHub repo `tlee-ui/WorkoutTrainer` (work GitHub account) | Yes | Copy the repo to a personal GitHub account (below) |
| Training log and track state (`data/`) | GitHub repo | Yes | Same |
| Link between Claude and GitHub | Claude account (GitHub connection and Claude GitHub App) | No | Connect GitHub from the new Claude account |
| Cloud environment: network access, Hevy secret | Claude account (environment settings) | No | Recreate from the spec below |
| Hevy API key | Hevy account, plus a copy in the old environment | Key: yes. Copy: no | Regenerate the key, store it in the new environment |
| Session transcripts, artifacts, scheduled tasks, memory | Claude account | No | Nothing to move if the rules below are followed |
| `Claude-Session:` links in commit messages | Claude account | No | None. They stop opening from another account; the commits are unaffected |

## Environment spec

Recreate this in the new account's cloud environment settings (the environment
menu in a session's title bar, then Edit).

| Setting | Value |
| --- | --- |
| Repository | `tlee-ui/WorkoutTrainer` (change to the personal copy once it exists) |
| Network access | Allow `api.hevyapp.com`. Research sessions also need web search and fetch. |
| Hevy credential | A network secret for `api.hevyapp.com` that sends the key in the `api-key` header. Alternative: an environment variable named `HEVY_API_KEY`. `tools/hevy_pull.py` works with either. |
| Setup script | None. The tools are Python 3 standard library only. |
| Connectors | None. The project does not use Gmail, Calendar, Drive, or any other connector. |

Never paste the key into a chat, a file in the repo, or a commit.

## Moving the GitHub repo

Commits are authored as `Claude <noreply@anthropic.com>`, and no credentials
are committed, so the history can be copied as is.

1. Create a personal GitHub account with a personal email.
2. Copy the repo with every branch and commit, into a **private** repo:
   - Without a command line: `https://github.com/new/import`, source URL
     `https://github.com/tlee-ui/WorkoutTrainer.git`.
   - Or from any computer with git:
     `git clone --mirror https://github.com/tlee-ui/WorkoutTrainer.git`, then
     in that folder `git push --mirror https://github.com/<you>/WorkoutTrainer.git`.
3. To keep working from the work Claude account during the transition: on the
   personal repo, invite the work GitHub user `tlee-ui` as a collaborator, and
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
   and give the Claude GitHub App access to `tlee-ui/WorkoutTrainer`.
3. In Hevy, generate a new API key at `https://hevy.com/settings?developer`.
4. Create the cloud environment from the spec above and add the new key.
5. Start a session and check the link:
   `python3 tools/hevy_pull.py --inspect` should print one workout.
6. Recreate any scheduled tasks you still want (list them in the old account
   first; their prompts are not stored in the repo).
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

None yet.

## Running without Claude

The repo works on any machine with Python 3:

```bash
git clone https://github.com/tlee-ui/WorkoutTrainer.git
cd WorkoutTrainer
HEVY_API_KEY=... python3 tools/hevy_pull.py
python3 tools/analyze_history.py
```
