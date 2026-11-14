"""Keeps Hevy and the repo in step.

`main` on GitHub is the source of truth. Two rules follow, and the tools
enforce them instead of trusting each session to remember:

1. Hevy only ever gets what is on `origin/main`. A session whose loads or week
   are not published cannot change the routines.
2. A session that cannot write to `main` cannot sync at all. (A cloud session
   without the repository attached can still clone it read-only; before this
   guard such sessions synced, pushed routines from private state and lost
   their commits.)

Standard library and the `git` command only. Every check is skipped outside a
git checkout, and with WORKOUT_NO_GIT=1 (tests, offline use).
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMOTE = "origin"
MAIN = "main"

# What a sync or a week change may write. Nothing else is committed by the tools.
OWNED = [
    "data/history.csv", "data/hevy-state.json", "data/tracks.json", "data/track-state.md",
    "data/track-log.md", "data/week.json", "data/weekly-plan.md", "data/hevy-exercise-map.json",
    "data/exercise-muscles.json", "dashboard/index.html", "dashboard/data.json",
    "data/checkins", "data/manual-log.csv",
]


def git(*args, cwd=ROOT, timeout=120):
    """Run git; return (returncode, combined output)."""
    try:
        p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)
    return p.returncode, (p.stdout + p.stderr).strip()


def enabled(cwd=ROOT):
    if os.environ.get("WORKOUT_NO_GIT"):
        return False
    rc, out = git("rev-parse", "--is-inside-work-tree", cwd=cwd)
    return rc == 0 and out.strip() == "true"


def fetch_main(cwd=ROOT):
    """Refresh origin/main. Returns (ok, message)."""
    rc, out = git("fetch", "--quiet", REMOTE, MAIN, cwd=cwd)
    return rc == 0, out


def behind_main(cwd=ROOT):
    """Commits on origin/main that HEAD does not have."""
    rc, out = git("rev-list", "--count", f"HEAD..{REMOTE}/{MAIN}", cwd=cwd)
    return int(out) if rc == 0 and out.isdigit() else 0


def can_publish(cwd=ROOT):
    """Can this session write to main? A dry-run push: authenticates, changes
    nothing. Returns (ok, reason)."""
    rc, out = git("push", "--dry-run", REMOTE, f"HEAD:{MAIN}", cwd=cwd)
    if rc == 0:
        return True, ""
    last = out.splitlines()[-1] if out else "push refused"
    if "403" in out or "denied" in out.lower() or "not in this session" in out:
        return False, ("this session cannot write to the repository (" + last + "). "
                       "In a scheduled run the repository is not attached to the task: "
                       "see coach/README.md, \"When the repo is read-only\".")
    if "non-fast-forward" in out or "fetch first" in out or "rejected" in out:
        return False, "main has moved on; merge it first: git merge --ff-only origin/main (or git merge origin/main)."
    return False, last


def differs_from_main(paths, cwd=ROOT):
    """Of `paths` (relative to the repo root), those whose working-tree content
    is not what origin/main holds."""
    out = []
    for p in paths:
        rc, _ = git("diff", "--quiet", f"{REMOTE}/{MAIN}", "--", p, cwd=cwd)
        if rc != 0:
            out.append(p)
            continue
        # a file that exists here but not on main shows no diff above; catch it
        rc, listed = git("ls-tree", "--name-only", f"{REMOTE}/{MAIN}", "--", p, cwd=cwd)
        if os.path.exists(os.path.join(cwd, p)) and not listed.strip():
            out.append(p)
    return out


def commit(paths, message, cwd=ROOT):
    """Commit whichever of `paths` changed. Returns the short hash, or None if
    there was nothing to commit."""
    existing = [p for p in paths if os.path.exists(os.path.join(cwd, p))]
    git("add", "--", *existing, cwd=cwd)
    rc, _ = git("diff", "--cached", "--quiet", "--", *existing, cwd=cwd)
    if rc == 0:
        return None
    rc, out = git("commit", "--quiet", "-m", message, "--", *existing, cwd=cwd)
    if rc != 0:
        raise RuntimeError("git commit failed: " + out)
    return git("rev-parse", "--short", "HEAD", cwd=cwd)[1]


def publish(cwd=ROOT, retries=3):
    """Push HEAD to main (fast-forward only), and to the session branch when
    HEAD is on another branch. Returns (ok, message)."""
    import time
    out = ""
    for attempt in range(retries):
        rc, out = git("push", "--quiet", REMOTE, f"HEAD:{MAIN}", cwd=cwd)
        if rc == 0:
            break
        if "non-fast-forward" in out or "rejected" in out or "403" in out or "denied" in out.lower():
            return False, out.splitlines()[-1] if out else "push refused"
        time.sleep(2 ** (attempt + 1))
    else:
        return False, out.splitlines()[-1] if out else "push failed"
    rc, branch = git("rev-parse", "--abbrev-ref", "HEAD", cwd=cwd)
    if rc == 0 and branch not in (MAIN, "HEAD"):
        git("push", "--quiet", "-u", REMOTE, branch, cwd=cwd)
    git("fetch", "--quiet", REMOTE, MAIN, cwd=cwd)
    return True, ""


def preflight(cwd=ROOT):
    """Before a sync changes anything: is this checkout current, and can it
    publish? Returns a list of problems (empty when clear)."""
    if not enabled(cwd):
        return []
    ok, out = fetch_main(cwd)
    if not ok:
        return [f"could not fetch origin/main ({out.splitlines()[-1] if out else 'no output'})"]
    n = behind_main(cwd)
    if n:
        return [f"this checkout is {n} commit(s) behind origin/main; run `git merge --ff-only origin/main` "
                "(or `git merge origin/main` on a session branch) and start again"]
    ok, why = can_publish(cwd)
    return [] if ok else [why]


def unpublished(paths, cwd=ROOT):
    """For the routine push: which of its inputs are not on origin/main."""
    if not enabled(cwd):
        return []
    fetch_main(cwd)
    return differs_from_main(paths, cwd)
