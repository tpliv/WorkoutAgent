#!/usr/bin/env python3
"""One command for the whole loop. Run it after training, after changing the
week, or whenever Hevy and the repo should agree.

    1. check   this checkout is up to date with origin/main and may write to it
    2. pull    new Hevy workouts into data/history.csv
    3. apply   templates/progression-tracks.md -> data/tracks.json, track-state, track-log
    4. week    mark logged sessions done in data/week.json; regenerate the plan tables
    5. build   the dashboard (only when the data changed)
    6. commit  the changed data files, and publish them to origin/main
    7. push    the routines to Hevy, only the ones that differ, each read back

The order is the point. `main` is the source of truth, so the repo is
published before Hevy is touched: Hevy can then never hold something the repo
does not. If step 1 fails nothing is changed anywhere. If step 6 fails Hevy is
not pushed. If step 7 fails the repo is right and Hevy is stale; re-run this
command, or `python3 tools/hevy_push_routines.py`.

Usage:
    python3 tools/hevy_sync.py                 # everything above
    python3 tools/hevy_sync.py --dry-run       # show what would happen; writes nothing here, on GitHub or in Hevy
    python3 tools/hevy_sync.py --check         # is Hevy the same as the repo? read-only
    python3 tools/hevy_sync.py --no-pull       # skip step 2 (after a week change, when nothing was trained)
    python3 tools/hevy_sync.py --no-push       # stop after step 6
    python3 tools/hevy_sync.py --reset-on-stall
    python3 tools/hevy_sync.py --full          # full re-pull instead of incremental
    python3 tools/hevy_sync.py --no-git        # no checks, no commit: leaves the changes for you to commit,
                                               # and the Hevy push will refuse until they are on main
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import gitguard  # noqa: E402

DASHBOARD = ["dashboard/index.html", "dashboard/data.json"]


def run(script, *flags, capture=False):
    cmd = [sys.executable, os.path.join(HERE, script), *flags]
    print(f"\n$ python3 {os.path.relpath(cmd[1])} {' '.join(flags)}".rstrip(), flush=True)
    if not capture:
        return subprocess.call(cmd), ""
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(p.stdout, end="")
    print(p.stderr, end="", file=sys.stderr)
    return p.returncode, p.stdout


def changed(paths):
    """Of `paths`, those that differ from HEAD (or are new)."""
    rc, out = gitguard.git("status", "--porcelain", "--", *paths)
    return [line[3:].strip().strip('"') for line in out.splitlines() if line.strip()] if rc == 0 else []


def commit_and_publish(message):
    """Commit the tool-owned files that changed and publish to main.
    Returns True when origin/main now holds this checkout's data."""
    try:
        sha = gitguard.commit(gitguard.OWNED, message)
    except RuntimeError as e:
        sys.exit(str(e))
    if sha:
        print(f"\nCommitted {sha}: {message.splitlines()[0]}")
    else:
        print("\nNothing to commit.")
    ok, why = gitguard.publish()
    if not ok:
        sys.exit(f"Could not publish to origin/main ({why}). The commit is local only and Hevy was NOT pushed. "
                 "Fix the push (usually `git merge origin/main`, then re-run) so main stays the source of truth.")
    if sha:
        print("Published to origin/main.")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true", help="only compare Hevy with the repo")
    ap.add_argument("--no-pull", action="store_true", help="skip the pull (use the committed history.csv)")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--no-git", action="store_true", help="skip the checks, the commit and the publish")
    ap.add_argument("--deload", action="store_true", help="deload rendering for this push (a planned deload week belongs in data/week.json: tools/week.py deload on)")
    ap.add_argument("--reset-on-stall", action="store_true")
    ap.add_argument("--full", action="store_true", help="full re-pull instead of incremental")
    ap.add_argument("-m", "--message", help="commit message (default: built from the track decisions)")
    args = ap.parse_args(argv)

    if args.check:
        sys.exit(run("hevy_push_routines.py", "--check")[0])

    use_git = not args.no_git and not args.dry_run and gitguard.enabled()
    if use_git:
        problems = gitguard.preflight()
        if problems:
            sys.exit("Sync not started; nothing was changed here, on GitHub or in Hevy.\n  - " + "\n  - ".join(problems))

    full = ["--full"] if args.full else []
    hist = []
    if args.dry_run and not args.no_pull:
        # A dry run must not touch the repo: pull into a temp copy of the
        # history and state, and point the track update at that copy.
        tmp = tempfile.mkdtemp(prefix="hevy-dry-")
        for name in ("history.csv", "hevy-state.json"):
            shutil.copy(os.path.join(ROOT, "data", name), tmp)
        out = os.path.join(tmp, "history.csv")
        if run("hevy_pull.py", *full, "--out", out, "--state", os.path.join(tmp, "hevy-state.json"), "--raw", os.path.join(tmp, "raw.jsonl"))[0]:
            sys.exit("Pull failed; stopping.")
        hist = ["--history", out]
    elif not args.no_pull:
        if run("hevy_pull.py", *full)[0]:
            sys.exit("Pull failed; stopping. Nothing else was changed.")

    upd = ["--write-md"] + (["--reset-on-stall"] if args.reset_on_stall else []) + (["--dry-run"] if args.dry_run else []) + hist
    rc, upd_out = run("update_tracks.py", *upd, capture=True)
    if rc:
        sys.exit("Track update failed; stopping. History was pulled; tracks and routines are unchanged.")
    decisions = [line.strip() for line in upd_out.split("Decisions:")[1].split("\n\n")[0].splitlines() if line.strip()] if "Decisions:" in upd_out else []

    if run("week.py", *(["--dry-run"] if args.dry_run else []), *hist, "reconcile")[0]:
        sys.exit("Week update failed; stopping.")

    dash_failed = False
    if not args.dry_run:
        data_changed = changed([p for p in gitguard.OWNED if p not in DASHBOARD]) if gitguard.enabled() else ["?"]
        if data_changed or not all(os.path.exists(os.path.join(ROOT, p)) for p in DASHBOARD):
            dash_failed = bool(run("build_dashboard.py")[0])
            if dash_failed:
                print("Dashboard build failed; continuing.")
        else:
            print("\nNo new data: dashboard left as built.")

    if use_git:
        message = args.message or ("Sync: " + "; ".join(decisions)[:180] if decisions else "Sync: week or state update")
        commit_and_publish(message)
    elif not args.dry_run and gitguard.enabled():
        left = changed(gitguard.OWNED)
        if left:
            print("\n--no-git: these are changed and not committed: " + ", ".join(left))

    if not args.no_push:
        push = (["--deload"] if args.deload else []) + (["--dry-run"] if args.dry_run else [])
        if run("hevy_push_routines.py", *push)[0]:
            sys.exit("Hevy push failed or incomplete: the repo is right and published, Hevy is stale. "
                     "Re-run `python3 tools/hevy_push_routines.py`; do not re-apply the rules by hand.")
        if args.dry_run:
            print("\n(dry run: routine payloads use the committed tracks.json, before the decisions shown above)")
        elif use_git and changed(gitguard.OWNED):
            # the push recorded new Hevy routine ids
            commit_and_publish("Record new Hevy routine ids")
    if dash_failed:
        sys.exit("Sync finished, but the dashboard build failed.")
    if not args.dry_run:
        print("\nSync complete. Republish dashboard/index.html to the dashboard page if it was rebuilt (tools/README.md, \"Progress dashboard\").")


if __name__ == "__main__":
    main()
