---
name: code-review
description: Review a GitHub pull request as a senior engineer. Gather the full context, inspect the diff and surrounding code, check CI, run targeted validation when useful, test frontend previews, classify findings as P1/P2/nit, self-critique every finding, and post a concise actionable review. Use when asked to review a PR, check a diff, QA a preview, or look for bugs before merge.
---

# Code Review

Review a pull request like a senior engineer: find real correctness, security, data-loss, and user-impact risks, not a restatement of the diff. Be decisive, evidence-based, and concise.

## Configuration

- `REPOSITORY`: target GitHub repository. Infer it from a PR URL when possible.
- `VALIDATION_COMMANDS`: project-specific format, lint, typecheck, and test commands.
- `PREVIEW_PATTERN`: where frontend preview URLs appear (PR comments, checks, or deployments).
- `REVIEW_DESTINATION`: GitHub PR by default; optionally a linked Slack thread.
- `PR_EXPECTATIONS`: the repository's PR template and required evidence for user-facing changes.

## Phase 1: Understand the change

1. Read the PR title, description, linked issue/spec, commits, checks, and existing review comments.
2. Read the full diff and relevant surrounding code. Never infer that a file still exists from the changed-files list; check whether it was modified, added, renamed, or deleted.
3. Restate the intended behavior in one sentence. Identify the riskiest assumptions before reviewing details.
4. Check PR hygiene against `PR_EXPECTATIONS`. Missing rationale, test plan, or UI evidence can be a finding when it materially blocks review.

## Phase 2: Validate

Use judgment. CI is the source of truth for mechanical checks when it is healthy; do not repeat an expensive full suite without a reason.

- Inspect all CI results and failure logs.
- Run focused tests or a minimal repro when CI is absent, broken, or cannot exercise the risky behavior.
- For frontend changes, find the preview URL and exercise the changed flow in a browser. Check happy path, one failure/empty state, console errors, and responsive layout. Capture evidence when useful.
- For API or data changes, test malformed input, authorization boundaries, retries/idempotency, migrations, and backward compatibility as relevant.

## Phase 3: Bug-hunt checklist

Look especially for:

1. Incorrect behavior at boundaries, empty states, nulls, partial failures, and retries.
2. Authorization, tenancy, secret/PII exposure, unsafe parsing, and injection risks.
3. Destructive or irreversible behavior without confirmation, transactionality, or recovery.
4. Race conditions, stale state, duplicate processing, non-idempotent retries, and cache invalidation.
5. Schema/API compatibility, migration safety, and callers that were not updated.
6. UI flows that look correct but fail at runtime, in the preview, or on small screens.
7. Tests that assert implementation details while missing the actual failure mode.
8. Complexity added at the wrong layer or a new parallel abstraction that will drift.

## Phase 4: Severity

- **P1**: Must fix before merge. Security vulnerability, data loss/corruption, broken critical path, cross-tenant exposure, or highly likely severe production incident.
- **P2**: Should fix before merge. Real bug, meaningful regression, reliability problem, or maintainability flaw likely to cause incorrect behavior.
- **Nit**: Optional polish. Naming, minor clarity, style, or low-impact cleanup. Cap nits at three and collapse them into one short section.

Do not inflate uncertain concerns. If you cannot describe a concrete failure mode and point to evidence, ask a question or omit it.

## Phase 5: Self-critique (mandatory)

Before posting, challenge every P1/P2:

- Did I read the surrounding code and all callers?
- Could the concern already be handled elsewhere?
- Is the file actually present, rather than deleted by this PR?
- Can I state the user/production impact and a plausible trigger?
- Is the proposed fix proportionate and specific?

Remove findings that do not survive this pass.

## Phase 6: Post the review

Default to one concise PR comment, plus inline comments only where a precise line is responsible. Never approve or request changes unless asked.

```markdown
## Review

**Verdict:** <ready / ready after P2s / blocked>

### P1
- **Short title** — `path/file.ts:123`
  Failure mode, impact, and a specific fix.

### P2
- **Short title** — `path/file.ts:456`
  Failure mode, impact, and a specific fix.

### Nits
- Up to three optional items in one compact list.

### Verified
- CI/checks inspected
- Focused tests or preview flows exercised
```

Omit empty severity sections. If `REVIEW_DESTINATION` includes Slack, post only the verdict, counts, and a link to the GitHub review there.

## Anti-patterns

- Summarizing the diff instead of finding risks.
- Treating preferences as correctness bugs.
- Trusting a green build as proof the feature works.
- Assuming another review bot catches mechanical errors.
- Posting speculative findings without reading callers and tests.
- Dumping the full review into multiple destinations.
