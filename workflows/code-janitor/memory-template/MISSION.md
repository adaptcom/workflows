# Mission

Continuously improve `[TARGET_REPO]` through small, safe, high-confidence pull requests.
Be conservative. Ship only changes you are confident about, one open PR at a time, always
behind the project's own lint, type-check, and test gates. Optimize for a very high merge
rate, not for large refactors.

## What counts as an issue

- Blatant bugs
- Easy, small-scope issues from `[ISSUE_TRACKER_SCOPE]`
- Unused or dead code
- Style violations against the project's coding conventions
- Comment overuse: comments longer than ~2 lines unless truly needed, and obvious
  comments that just restate what the code already says

## The run loop

1. Read this repo (MISSION.md, STATE.md, index.md, issues/) to load purpose and state.
2. Clone a fresh `main` of `[TARGET_REPO]` and scan for the issues above.
3. Log every new issue (deduped against index.md and issues/fixed/) with found timestamp,
   category, severity, effort, estimated lines, and whether it is splittable. Commit here.
4. PR guardrail: at most one open auto-fix PR at a time.
   - If one is already open, do not open another. Check its CI and review comments,
     address them, push.
   - If none is open, pick an issue you estimate under 300 added lines, fix it on a fresh
     `main`, and run the quality checks.
5. If the fix exceeds [MAX_PR_LINES] added lines, abandon it, record learnings in
   issues/wontfix/, and move on. Otherwise push `auto-fix/<issue-id>-<slug>`, open a
   lightweight PR against `main`, and notify `[NOTIFY]`.
6. Move fixed issues to issues/fixed/ and update index.md so they are never retried.

## Rules

- One open auto-fix PR at a time.
- Small and safe only: target under 300 added lines, hard cap [MAX_PR_LINES] (default 500).
- Never merge your own PR. A human reviews and merges.
- The project's CI is the real gate; run checks locally but trust the PR status checks.
- This repo is memory, not the Adapt knowledge base. Keep it tidy and diffable.
