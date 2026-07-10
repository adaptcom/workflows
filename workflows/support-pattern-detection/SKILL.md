---
name: support-pattern-detection
description: Analyze a recent window of customer-support tickets, cluster repeated symptoms into meaningful patterns, compare them with the previous matching window, and deliver a concise evidence-linked report with impact, severity, and recommended action. Use for daily support trend detection, emerging-issue monitoring, ticket spike analysis, and deciding what support, product, or engineering should investigate.
---

# Support Pattern Detection

Turn a noisy support queue into a small set of evidence-backed signals. Review recent tickets, identify repeated customer problems or sudden changes, and tell the team what deserves attention. Do not summarize every ticket and do not manufacture a trend from isolated cases.

## Configuration

- `TICKET_SYSTEM`: Zendesk, Intercom, another support platform, or an exported ticket dataset.
- `LOOKBACK_WINDOW`: recent period to analyze (default: last 24 hours).
- `COMPARISON_WINDOW`: immediately preceding matching period (default: prior 24 hours).
- `MIN_PATTERN_SIZE`: minimum related tickets required for a pattern (default: 3).
- `SPIKE_THRESHOLD`: optional percentage/absolute increase that makes a pattern notable.
- `SEVERITY_RULES`: project-specific rules for low, medium, high, and critical.
- `DELIVERY_DESTINATION`: Slack channel, email, document, or dashboard.
- `ESCALATION_DESTINATION`: optional issue-tracker project or engineering channel.
- `EXCLUSIONS`: spam, test tickets, internal requests, known automation, or categories to omit.

## Core principles

1. **Patterns, not anecdotes.** Ignore one-off issues unless they meet a critical severity rule.
2. **Evidence before interpretation.** Every pattern must link to its supporting tickets.
3. **Symptoms before presumed causes.** Cluster what customers experience; do not claim a root cause without technical evidence.
4. **Compare like with like.** Use equal windows and explain incomplete or unusual data.
5. **Prefer silence to noise.** If no meaningful patterns exist, say so in one sentence.
6. **Protect customer data.** Summarize symptoms without exposing secrets, personal information, or private message text in broad channels.

## The workflow

### 1. Collect and normalize tickets

Pull all tickets created or updated during `LOOKBACK_WINDOW`, plus the previous matching `COMPARISON_WINDOW`.

For each ticket, normalize:

- Ticket ID and source link
- Created/updated timestamp and current status
- Subject and sanitized problem description
- Product area, tags, form, channel, plan/tier, or account segment when available
- Priority and escalation state

Apply `EXCLUSIONS`. Deduplicate by the ticket system's stable ticket ID. If the API paginates, verify that pages do not overlap and compare the final distinct count with the platform's count endpoint when available.

### 2. Identify candidate patterns

Cluster tickets by shared customer-visible symptom, affected workflow, error text, product area, or integration. Use metadata only as supporting evidence; the actual ticket descriptions should drive the grouping.

Good pattern labels describe the experience:

- "Password resets never arrive"
- "Mobile checkout freezes after payment"
- "CSV exports omit recent records"

Avoid vague labels such as "Technical issue" or unsupported root-cause labels such as "Database outage."

A candidate becomes reportable when it:

- Meets `MIN_PATTERN_SIZE`, or
- Exceeds `SPIKE_THRESHOLD`, or
- Meets a high/critical `SEVERITY_RULE`, even with fewer tickets.

Do not count the same ticket in multiple patterns unless it clearly contains distinct issues; disclose overlap when it exists.

### 3. Compare with the previous window

For each reportable pattern, calculate:

- Current distinct ticket count
- Previous-window distinct ticket count
- Absolute change
- Percentage change when the previous count is greater than zero
- Trend: new, increasing, stable, or decreasing

When the previous count is zero, label the pattern **new** rather than claiming an infinite percentage increase. Flag partial windows, outages in the ticket API, or unusually low total volume.

### 4. Assess impact and severity

Describe what customers are unable to do, what is degraded, or what is confusing. Assign severity using `SEVERITY_RULES`, not ticket volume alone.

Suggested default:

- **Critical:** widespread outage, security/data-loss risk, or a core workflow broadly unavailable.
- **High:** repeated blockers with no reliable workaround, or rapidly increasing severe failures.
- **Medium:** material friction affecting multiple customers with a workaround or limited scope.
- **Low:** recurring confusion or minor defect that does not block the workflow.

State uncertainty. If the evidence only shows symptoms, say "Possible product issue" rather than claiming a confirmed bug.

### 5. Recommend one next action

Choose the most appropriate action:

- **Monitor:** pattern is small/stable and impact is low.
- **Update support guidance:** repeated confusion is answerable with existing knowledge.
- **Investigate:** meaningful signal exists but the cause is unclear.
- **Escalate to product/engineering:** likely defect, serious impact, or rapid spike.
- **Notify incident response:** critical severity or outage-like evidence.

If `ESCALATION_DESTINATION` is configured and the action requires it, create or update an issue only after checking for duplicates. Link the evidence and avoid pasting private ticket content.

### 6. Deliver the report

Use this format:

```markdown
## Support patterns — <window>

### <Pattern label> — <severity> — <trend>
- **Volume:** <current> tickets (previous: <previous>, change: <absolute / percentage or "new">)
- **Customer impact:** <one or two sentences>
- **Evidence:** <ticket links or IDs>
- **Recommended action:** <monitor / guidance / investigate / escalate / incident response>
- **Why:** <brief rationale and uncertainty>

_No other meaningful patterns met the reporting threshold._
```

Order patterns by severity first, then strength of evidence and rate of change. Keep the top-level report concise; link to tickets for detail.

## Quality checks

Before sending:

- Every ticket is counted once per pattern.
- Each pattern meets a configured threshold or severity exception.
- Current and comparison windows are equal and clearly stated.
- Ticket links/IDs support the stated symptom.
- Root-cause language is not stronger than the evidence.
- No secrets, PII, or private ticket excerpts are exposed.
- The recommended action is singular and proportionate.

## Anti-patterns

- Producing a ticket-by-ticket digest.
- Reporting generic categories rather than concrete customer symptoms.
- Treating three unrelated tickets as a pattern because they share a tag.
- Reporting percentage change without the underlying counts.
- Automatically escalating every cluster to engineering.
- Inventing a cause, workaround, or documentation recommendation.
- Hiding an empty result by lowering the threshold after analysis.
