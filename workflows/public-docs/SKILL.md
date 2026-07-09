---
name: public-docs
description: Keep public documentation and the changelog in sync with shipped product behavior. Verify the implementation against source code, decide which docs surfaces need updates, write concise user-facing content, update links and media, open a draft docs pull request, and report back to the release source. Use when a feature ships or when asked to write or edit help articles, API docs, onboarding guides, feature pages, announcements, or changelog entries.
---

# Docs & Changelog

Close the loop between shipped code and public documentation. The workflow verifies what actually shipped, updates every affected docs surface together, and opens a reviewable draft PR rather than publishing unsupported claims.

## Configuration

- `SOURCE_REPO`: product repository that contains implementation truth.
- `DOCS_REPO`: repository containing public documentation.
- `DOCS_URL`: public docs base URL.
- `DOCS_PLATFORM`: Mintlify, Docusaurus, custom MDX, or another system.
- `CHANGELOG_PATH`: directory or collection for changelog entries.
- `SHIP_SOURCE`: release channel, merged PR, release webhook, or direct request.
- `VOICE_RULES`: project-specific terminology, tone, formatting, and prohibited claims.
- `DOCS_STRUCTURE`: map of product areas to docs paths.

## Writing standards

### Voice and tone

- Lead with what the reader can now do.
- Use plain language, short sentences, active voice, and present tense.
- Be specific about behavior, limits, roles, and prerequisites.
- Do not use hype, implementation jargon, or claims the code does not support.
- Follow `VOICE_RULES` for names, capitalization, and product vocabulary.

### Formatting

- Use one H1 per page and descriptive H2/H3 headings.
- Prefer numbered steps for procedures and bullets for requirements/options.
- Put UI labels, commands, file paths, fields, and code in the appropriate formatting.
- Use descriptive link text and valid absolute docs paths.
- Add alt text and captions that explain why a screenshot matters.

### Verify before writing

Documentation must reflect shipped behavior, not roadmap intent.

1. Read the source PR/release and linked issue/spec.
2. Inspect the actual implementation in `SOURCE_REPO`, including defaults, permissions, errors, feature flags, and UI labels.
3. Check tests and runtime evidence for edge cases.
4. Search `DOCS_REPO` for every existing reference that may now be stale.
5. When evidence conflicts, ask the shipper rather than guessing.

## Document types

### Changelog entry

A short release-facing explanation:

```markdown
---
title: <Outcome-oriented title>
date: YYYY-MM-DD
---

<One paragraph: what readers can now do and why it matters.>

## How it works

- Concrete capability
- Important limit or permission
- Where to find it

## Try it

1. First step
2. Second step
3. Expected result

[Learn more](/docs/relevant-page)
```

### Help article

```markdown
# <Complete a task>

<What this guide helps the reader accomplish.>

## Prerequisites

- Required role, connection, plan, or access

## Steps

1. Navigate to the exact location.
2. Choose the exact UI action.
3. Verify the expected result.

## Troubleshooting

Common failure modes and fixes.

## Related

- [Related guide](/docs/related-guide)
```

### API documentation

Include authentication, endpoint/method, parameters, complete request/response examples, errors, idempotency/retry behavior, and limits. Examples must be valid and sanitized.

### Feature page or announcement

Explain who it is for, the job it solves, how it works, prerequisites, limits, and a concrete getting-started path. Keep announcements concise; link to durable docs for detail.

## Ship workflow

### 1. Parse the trigger

Extract:

- Feature/outcome
- Source PR, issue, release, or announcement
- Shipper/owner
- Release date and environment
- Candidate docs and changelog surfaces

If the change is internal-only, anti-abuse/security-sensitive, experimental, or not actually in production, confirm whether public documentation is appropriate before writing.

### 2. Research implementation truth

Clone/update `SOURCE_REPO` and `DOCS_REPO`. Inspect changed files and surrounding behavior, not just the PR summary. Verify the exact UI names, roles, configuration, defaults, errors, and limitations.

Search the docs for:

- Old terminology
- Screenshots that no longer match
- Duplicate or conflicting instructions
- Links affected by moved/renamed pages
- Onboarding, API, troubleshooting, and reference pages touched by the change

### 3. Plan the docs delta

Choose only the needed surfaces:

- New or updated durable docs page
- Changelog entry
- API/reference update
- Screenshot/media replacement
- Navigation/index update
- Redirect or link fix

Prefer updating an existing canonical page over creating a duplicate.

### 4. Write and validate

- Follow `VOICE_RULES` and the templates above.
- Validate links, frontmatter, code examples, and docs-platform build/lint commands.
- Ensure changelog links resolve against the website where the entry renders.
- Never include secrets, internal URLs, private customer information, or unsupported future claims.

### 5. Open a draft PR

Open a draft PR in `DOCS_REPO` with:

```markdown
## Why?

What shipped and why these docs must change.

## Demo

Screenshots or preview links for user-facing docs changes.

## Optional Context

Source PR/release, validation run, and any review questions.
```

Attribute the initiating source and link back to it. Keep the PR concise; the diff is the detailed change log.

### 6. Report back

Reply at `SHIP_SOURCE` with the draft PR link, one sentence on what changed, and any questions that need the shipper's confirmation. Do not auto-publish unless the team's process explicitly allows it.

## Review checklist

- Verified against shipped code
- Correct product names, labels, roles, defaults, and limits
- Durable docs and changelog updated together where needed
- Internal links resolve at their final public URL
- Examples run or validate
- No secrets, private data, or internal-only details
- Draft PR includes source attribution and preview/evidence
