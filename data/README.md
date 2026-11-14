# Data

The training log and the live state of the program. Everything here except
`raw/` is committed so agents in later sessions can read it.

| File | What it is | Kind | Changed by |
|---|---|---|---|
| `tracks.json` | In pounds. The six progression tracks (planned next heavy load, last lifted load, rep target, counters, last exposure, e1RM history, phases), the pointer, block week, accessory loads, and `amendments` (hand changes, logged). **The only place a load is stored.** | state | `tools/hevy_sync.py`; a hand change only through `tools/update_tracks.py --set ... --reason` |
| `week.json` | This week's sessions: date, slot, state, time, note, Hevy routine id; the deload flag; the plan's status. **The only place the schedule is stored.** | state | `tools/week.py` |
| `weekly-plan.md` | The week for people: Status and Sessions tables (generated between the `week:` markers from `week.json` and `tracks.json`), then the reasoning, race and cardio notes and the list of changes (hand-written) | generated block + notes | `tools/week.py`; notes by the coaching runs |
| `track-state.md` | The tracks for people: the table and accessory loads (generated between the `tracks:` markers) and notes on each lift (hand-written) | generated block + notes | `tools/update_tracks.py --write-md` |
| `track-log.md` | Every decision the engine made and every hand amendment, with the reason. Newest at the bottom | append-only log | `tools/update_tracks.py`; a few hand-written notes from before `--set` existed |
| `history.csv` | Set-level log, one row per set (format in `tools/README.md`). Loads in kg as the Hevy API returns them; `date` is the lifter's calendar day, `start_time` the raw UTC timestamp | log | `tools/hevy_pull.py` only |
| `manual-log.csv` | Sets reported in the chat when Hevy has no record (`templates/log-template.csv` columns, pounds). No tool reads it; the tracks are amended by hand from it | log | by hand |
| `checkins/YYYY-MM-DD.md` | One record per check-in: answers, flags, decisions, rules that fired | log | Sunday check-in |
| `hevy-state.json` | Hevy folder ids, routine ids per rotation slot, the pool of dated routines, and the pull cursor | state | pull and push |
| `hevy-exercise-map.json` | Program exercise name to Hevy exercise template id | cache | `hevy_push_routines.py --resolve`; by hand when a match is wrong |
| `exercise-muscles.json` | Hevy exercise title to muscle groups and exercise type, for the dashboard | cache | `build_dashboard.py --refresh-muscles` |
| `history-summary.md` | Per-exercise e1RM history and the starting loads proposed on 21 Oct 2026. A snapshot from when the tracks were seeded; not kept current | snapshot | `tools/analyze_history.py`, once |
| `body-composition.md` | Body-composition baseline, population comparison, calorie and macro plan, adjustment rules, scan log | notes | by hand after each scan |
| `races.md` | Race results with splits and heart rate, year-on-year comparison | log | by hand after each race |
| `raw/` | Raw API JSON and app exports | scratch | gitignored |

Three rules:

- A fact has one home. Loads are in `tracks.json`, the schedule in `week.json`. Other files that show them are generated; prose files point to them and do not restate numbers.
- State files are changed by a tool, never by editing. The tool logs the change.
- `python3 tools/hevy_sync.py` is what publishes any of this to GitHub and to Hevy.

The API key is never written here. It is a network secret for
`api.hevyapp.com` in the cloud environment, or the `HEVY_API_KEY` environment
variable (`tools/README.md`, Setup).
