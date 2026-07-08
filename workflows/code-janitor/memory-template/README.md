> **This folder is a TEMPLATE, not a live memory store.**
> To set up the Code Janitor you must create a SEPARATE, empty GitHub repository
> (it can be private) and copy the contents of this `memory-template/` folder into
> it as the initial commit. That new repo, not this folder, is what the janitor
> reads from and writes to on every run. The copy inside the skill never changes.
>
> Setup in three steps:
> 1. Create a new empty GitHub repo, e.g. `your-org/janitor-memory` (private is fine).
> 2. Copy everything under `memory-template/` into it and commit.
> 3. Fill in the placeholders in `MISSION.md` and delete the example issue.

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
