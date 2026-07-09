---
name: triage-bugs
description: Triage an inbound bug report end to end. Parse the report and attachments, search the issue tracker for duplicates, investigate the code, attempt a time-boxed reproduction, then decide whether to fix it now, file a bug or investigation ticket, link it to an existing issue, or decline it with evidence. Use for bug-intake channels, pasted bug reports, screenshots, error traces, and requests to investigate or file a bug.
---

# Bug Triage

Turn a vague bug report into the right engineering outcome, not merely another backlog item. Investigate first, prefer a safe small fix when practical, and file a ticket only when tracking is genuinely needed.

## Configuration

- `INTAKE_CHANNEL`: Slack channel or other source where bug reports arrive.
- `TARGET_REPO`: codebase to investigate and fix.
- `ISSUE_TRACKER`: Linear, Jira, or GitHub Issues.
- `ISSUE_PROJECT`: destination team/project for bugs and investigations.
- `LABELS`: existing labels and area taxonomy. Do not create new labels automatically.
- `ROUTING`: optional map from product area to repository path and reviewer/owner.
- `REPRO_ENV`: local app, staging environment, PR preview, or production read-only checks.
- `FIX_BUDGET`: maximum scope/time for an immediate safe fix.

## When it runs

Use when a new top-level report arrives in `INTAKE_CHANNEL`, or when a person asks to triage, investigate, reproduce, deduplicate, fix, or file a bug. Do not restart the full flow for ordinary replies inside an already-triaged thread unless they describe a separate issue.

## Default posture: prefer a fix over a ticket

A safe, well-understood fix within `FIX_BUDGET` is usually more valuable than a backlog item. Do not force a PR when the behavior is unconfirmed, destructive, security-sensitive, broad, or dependent on a product decision.

## The 7-step flow

### 1. Parse the report

Capture:

- Reporter and source link
- Expected vs. actual behavior
- Steps, environment, URL, account/tenant, browser/device, timestamp
- Error text, screenshots, videos, traces, request IDs, and relevant files
- Whether the impact is cosmetic, blocked workflow, data integrity, security, or outage

Ask at most the one or two questions needed to unblock investigation. Do not make the reporter rewrite information already in the thread or attachments.

### 2. Search the issue tracker first

Search open and recently closed issues using symptoms, error strings, component names, and affected flows.

- Exact duplicate: add the new evidence and source link to the existing issue; do not file another.
- Related but materially different: cross-link it and continue.
- A prior issue marked fixed: verify whether this is a regression before reopening or filing.

### 3. Investigate and attempt reproduction

Read the relevant code paths before reproducing. Follow the time-boxing and category guidance in `repro-and-fix-playbook.md`.

Strong reproduction evidence includes:

- A minimal failing test
- Browser steps with console/network evidence
- A curl request with response/status
- A deterministic input/output pair for a pure function
- A data query that demonstrates the inconsistent state

Never use real customer data in a public ticket or test fixture. Redact secrets and personally identifiable information.

### 4. Decide the path

Choose exactly one primary outcome:

- **Fix now**: root cause is clear, change is safe and inside `FIX_BUDGET`, validation is available.
- **File bug**: confirmed or high-confidence defect that needs tracked work.
- **File investigation**: real signal, but root cause/repro is not yet known.
- **Link duplicate**: already tracked; append evidence.
- **Decline / working as designed**: explain the verified behavior and any workaround.
- **Needs product decision**: frame the decision and route it to the appropriate owner rather than calling it a bug.

### 5. Fix or file

If fixing:

1. Branch from fresh main.
2. Add the narrowest regression test that proves the failure.
3. Implement the smallest complete fix.
4. Run relevant formatting, linting, typechecks, tests, and runtime QA.
5. Open a draft or ready PR according to repository policy and link the source report.

If filing, use the templates in `templates/`. Include only evidence you verified. Attach media directly to the tracker when supported rather than leaving it trapped behind a private Slack link.

### 6. Reply at the source

Reply in the original thread/channel with a concise disposition:

```markdown
**Triage:** <fixed / filed / investigation / duplicate / working as designed>
**What I found:** <one or two evidence-based sentences>
**Next:** <PR or issue link, owner, workaround, or what is still needed>
```

Do not paste a long investigation log into Slack. Put durable detail in the PR or issue.

### 7. Follow up

- Re-check CI and reviewer feedback on a PR you opened.
- When a fix ships, close/link the issue and update the reporter.
- If reproduction fails, record what was tried so another engineer does not repeat the same dead ends.

## Routing and labels

Use existing labels from `LABELS`. The generic templates deliberately avoid organization-specific teams, people, and packages. If `ROUTING` is configured, use it to suggest an owner; never fabricate ownership.

## Anti-patterns

- Filing from the first sentence without searching or investigating.
- Creating duplicate issues.
- Treating an ambiguous product expectation as a confirmed bug.
- Claiming reproduction without evidence.
- Exposing customer data, secrets, private URLs, or internal identifiers.
- Opening a speculative large PR to avoid filing an investigation.
- Creating new issue labels or projects without approval.
