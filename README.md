# Adapt Workflows

A curated, open catalog of real workflows you can run with [Adapt](https://adapt.com), the integrated coworker that connects to your company's systems, data, and processes and has its own computer to do real work.

Every workflow here is a self-contained skill (a `SKILL.md` plus any supporting files) that you can:

1. **Add to Adapt directly** by pointing the Skills page at this repo as a GitHub source (`adaptcom/workflows`, path `workflows/`), or
2. **Download as a zip** from [adapt.com/workflows](https://adapt.com/workflows) and upload it into Adapt, or drop it into any other tool that reads the `SKILL.md` format.

These are the same workflows our own team runs internally, generalized so any team can use them.

## Repository layout

```
workflows/
  <workflow-slug>/
    SKILL.md        # the skill itself (name + description frontmatter + instructions)
    catalog.json    # website metadata: department, summary, integrations, cadence
    ...             # any supporting files the skill needs
scripts/
  build.py          # packages each workflow into dist/<slug>.zip + dist/catalog.json
```

`SKILL.md` is the single source of truth for behavior. `catalog.json` only drives the
website listing. Downloadable zips are generated from source (`scripts/build.py`), never
committed, so the download always matches what you can read here.

## Available workflows

| Workflow | Department | What it does |
| --- | --- | --- |
| [code-janitor](workflows/code-janitor) | Engineering | Always-on agent that opens small, safe cleanup PRs behind your CI gates |
| [seo-agent](workflows/seo-agent) | Marketing | Recurring SEO reporting plus a daily rank-progress loop that finds and ships content gaps |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: one folder per workflow, a valid
`SKILL.md` with `name` and `description`, a `catalog.json`, and no company-specific or
sensitive data (secrets, internal repo names, personal handles, customer names).
