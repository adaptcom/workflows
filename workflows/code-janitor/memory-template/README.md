# Janitor memory

This repository is the Code Janitor's durable, file-system-based memory. It is NOT
application code and it is NOT the Adapt knowledge base. Every janitor run reads this
repo to recall its purpose and prior state, then writes back what it found and did.

Read on each run: `MISSION.md`, `STATE.md`, `index.md`, and `issues/`.

Layout:

```
MISSION.md             purpose, mission, goals, the run loop, and rules
STATE.md               last run, in-flight PR, counters
index.md               master table of every issue and its status
issues/open/           one file per open issue (ISSUE-XXXX.md)
issues/fixed/          issues that have been fixed (never re-attempted)
issues/wontfix/        issues abandoned as too large, with learnings
runs/                  one journal entry per run (YYYY-MM-DDTHH.md)
```

`index.md` plus `issues/fixed/` are the dedup mechanism: they stop the janitor from
re-finding and re-fixing something it already handled.
