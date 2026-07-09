---
name: code-janitor
description: An always-on code-hygiene agent that scans a repository for small, safe, high-confidence improvements (dead code, lint and style violations, comment overuse, easy tracked issues), keeps a durable Git-based memory of what it has already seen and fixed, and opens one small pull request at a time behind your existing CI gates. Use to set up or run a recurring "janitor" that keeps a codebase clean without human babysitting.
---

# Code Janitor

An always-on agent that continuously improves a codebase through small, safe, high-confidence pull requests. It is deliberately conservative: it only ships changes it is confident about, only one open PR at a time, and always behind your own lint, type-check, and test gates. The goal is a steady stream of low-risk cleanups with a very high merge rate, not large refactors.

## What it does

On each run it:
1. Reads its own memory to recall its mission and everything it has already seen or fixed.
2. Scans the target repository for small issues in these categories:
   - Blatant bugs
   - Easy, small-scope issues from your issue tracker
   - Unused or dead code
   - Style violations against your project's coding conventions
   - Comment overuse (comments longer than ~2 lines unless truly needed, and obvious comments that just restate what the code already says)
3. Logs every new issue to memory with a severity, an effort estimate, estimated lines added/removed, and whether it can be split into smaller PRs.
4. Picks one issue it estimates it can fix in under 300 added lines, fixes it, and runs your quality checks locally.
5. Opens at most one pull request, and notifies you.
6. Marks fixed issues in memory so it never re-attempts them.


## Configuration

Set these when you install the workflow:

- `TARGET_REPO` = the repository to clean up, e.g. `[your-org/your-repo]`.
- `MEMORY_REPO` = a repo the janitor owns for memory, e.g. `[your-org/janitor-memory]`.
- `CADENCE` = how often it runs, e.g. `hourly` (`0 * * * *`) or `daily` (`0 9 * * *`).
- `NOTIFY` = where to notify on a new PR, e.g. a Slack DM or `[#your-channel]`.
- `ISSUE_TRACKER_SCOPE` = which team/project/label counts as "easy", or leave off.
- `MAX_PR_LINES` = hard cap on added lines per PR (default 500; target under 300).
- `QUALITY_CHECKS` = the commands that must pass before a PR, e.g. `lint`, `typecheck`, `test` (scoped to touched packages), dead-code check.

## Setup: create the recurring task

Before the janitor can run, you set up its memory repo. The `memory-template/` folder in
this skill is a TEMPLATE, not the live memory. You turn it into a real repo once:

1. **Create the memory repo.** Make a new, empty GitHub repository (can be private), e.g.
   `[your-org/janitor-memory]`. This becomes `MEMORY_REPO`.
2. **Seed it from the template.** Copy the contents of `memory-template/` into that repo and
   commit them as the initial commit. Then replace the `[TARGET_REPO]`, `[ISSUE_TRACKER_SCOPE]`,
   `[MAX_PR_LINES]`, and `[NOTIFY]` placeholders in `MISSION.md` with your values, and delete
   the example issue in `issues/open/`. From now on `MISSION.md` is the purpose every run reads back.
3. **Verify access.** Confirm your GitHub can read/write `MEMORY_REPO` and push branches / open
   PRs on `TARGET_REPO`.
4. **Create the recurring Adapt task** on your `CADENCE` that executes the run loop below.

## The run loop

1. **Load memory.** Read `MISSION.md`, `STATE.md`, `index.md`, and `issues/` to recall purpose, the current in-flight PR, and prior state.
2. **Scan.** Clone a fresh `main` of `TARGET_REPO` and look for issues in the categories above.
3. **Log.** Record every new issue (deduped against `index.md` and `issues/fixed/`) with found-timestamp, category, severity, effort, estimated lines, and whether it is splittable. Commit to the memory repo.
4. **PR guardrail: at most one open auto-fix PR at a time.**
   - If an auto-fix PR is already open, do NOT open another. Instead check its CI status and any review comments, address them, and push.
   - If none is open, pick an issue you estimate under 300 added lines, fix it on a fresh `main`, and run `QUALITY_CHECKS`.
5. **Ship or abandon.** If the fix ends up over `MAX_PR_LINES`, abandon it, record what you learned in `issues/wontfix/`, and move on. Otherwise push a branch `auto-fix/<issue-id>-<slug>`, open a lightweight PR against `main`, and send `NOTIFY`.
6. **Remember.** Move fixed issues to `issues/fixed/` and update `index.md` so they are never retried.

## Memory repo layout

This skill ships a ready-to-use starter in `memory-template/`. Copy it into `MEMORY_REPO`
on setup. It contains:

```
README.md              what this repo is and how a run uses it
MISSION.md             purpose, mission, goals, the run loop, and rules (edit placeholders)
STATE.md               last run timestamp, in-flight PR, counters
index.md               master table: id | title | category | severity | effort | est lines | splittable | status | found | fixed
issues/
  ISSUE-TEMPLATE.md    copy this per new issue
  open/                one file per open issue (seeded with an example ISSUE-0001)
  fixed/               moved here once fixed, so it is never re-fixed
  wontfix/             abandoned (over the line cap) with learnings
runs/                  one journal entry per run (YYYY-MM-DDTHH.md)
```

The `index.md` plus the `issues/fixed/` folder are the dedup mechanism that stops the
agent from re-finding and re-fixing the same thing. Delete the seeded example issue after
your first real run.

## Guardrails and philosophy

- One open PR at a time. This keeps the review queue sane at any cadence.
- Small and safe only. Under 300 lines targeted, hard-capped at 500. Big changes are logged and left for a human.
- Never merge its own PRs. A human always reviews and merges.
- Your CI is the real gate. The agent runs checks locally, but the PR's status checks are the source of truth.

## Customizing

- Tighten or loosen the categories to match what your team wants automated.
- Point it at a monorepo package or a single service instead of the whole repo.
- Adjust cadence: hourly is aggressive and best for large, active codebases; daily is calmer.
