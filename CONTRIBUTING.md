# Contributing a workflow

Thanks for adding to the catalog. Every workflow is a skill folder under `workflows/`.

## 1. Create the folder

```
workflows/<your-slug>/
  SKILL.md
  catalog.json
```

Use a short, lowercase, hyphenated `slug` (e.g. `code-janitor`).

## 2. Write SKILL.md

`SKILL.md` must start with YAML frontmatter containing at least `name` and `description`:

```markdown
---
name: your-workflow
description: One or two sentences on what this workflow does and when to use it. This is what the agent reads to decide when to load the skill, so be specific.
---

# Your Workflow

Instructions the agent follows...
```

Keep the body practical: what it does, how it works, prerequisites/integrations,
configuration placeholders, and the exact steps or prompts to run.

## 3. Add catalog.json

This drives the website card. Example:

```json
{
  "slug": "your-workflow",
  "name": "Your Workflow",
  "department": "Engineering",
  "summary": "One-line pitch shown on the card.",
  "integrations": ["GitHub", "Slack"],
  "cadence": "Recurring (daily)",
  "outputs": ["Pull requests", "Slack updates"]
}
```

Departments in use: `Engineering`, `Marketing`, `Sales`, `Finance`, `Operations`,
`Leadership`, `Product`. Add a new one only if none fit.

## 4. Scrub before you submit

This repo is public. Do not include:

- Secrets, API keys, tokens, passwords, or auth of any kind
- Internal or private repository names, service names, or infrastructure identifiers
- Personal GitHub handles, emails, Slack user IDs, or channel IDs
- Customer or prospect names
- Anything you would not put on the public website

Replace real values with clearly-marked placeholders like `[your repo]`,
`[target keyword]`, `[your team's Slack channel]`.

## 5. Test the build

```
python3 scripts/build.py
```

This validates every workflow and writes `dist/<slug>.zip` and `dist/catalog.json`.
Open a PR once it passes.
