---
name: seo-agent
description: An end-to-end SEO agent that runs recurring performance reporting and a daily ranking-progress loop across Google Search Console, Google Analytics, and a backlink tool, then finds content gaps and helps ship them. Use to set up weekly SEO reporting plus a daily "rank #1 for [target keyword]" tactic-and-measure loop that does the reporting, finds the gaps, and ships the gaps.
---

# SEO Agent

An SEO teammate that runs on a schedule. It covers the full loop: do the reporting, find the gaps, ship the gaps. It pulls live data from your analytics and backlink tools, turns it into decisions, and can draft and publish the content those decisions call for.

## What it does

Two recurring workflows that work together:

1. **Weekly performance report** that tells you what is working, what is slipping, and what to do about it.
2. **Daily ranking-progress loop** focused on a single target keyword: one concrete tactic per day plus an honest measurement of whether you moved forward or backward in the last 24 hours.

## Prerequisites and data sources

- **Google Search Console** for queries, clicks, impressions, and positions.
- **Google Analytics** for traffic, sources, and page performance.
- **A backlink / competitive tool** (e.g. Ahrefs) for backlinks and competitor link sources.
- **Call transcripts** (optional, e.g. from your meeting recorder) to mine emerging topics your audience is actually asking about.
- **Your CMS** (optional) if you want the agent to draft and publish content, not just recommend it.
- **Slack or email** for delivery.

## Configuration

- `TARGET_KEYWORD` = the phrase you want to rank #1 for, e.g. `[your target keyword]`.
- `COMPETITORS` = a short list of competitor domains to benchmark against.
- `REPORT_DELIVERY` = where reports land, e.g. a Slack channel or email.
- `REPORT_TIME` = when to send, e.g. Monday 7am.
- `TACTIC_TIME` = when the daily tactic runs, e.g. every day at 8am.
- `CMS` = your content platform, if you want auto-drafting.

## Workflow 1: Weekly performance report

Create a recurring task (default: Monday `REPORT_TIME`) that produces a report covering:

- Top performing pages over the last 7 days
- What is declining over the last 7 and 30 days
- What is picking up over the last 7 and 30 days
- What to do to reverse the declines and accelerate the gains
- The top 20 traffic sources last week, and any new sources of traffic
- What new sites `COMPETITORS` are getting backlinks from, and what you should do to get on those sites too
- Based on the last 7 days of call transcripts, any emerging topics worth writing about for your audience
- If yes, whether any of those ideas map to existing or emerging keywords
- Anything else notable: insights and things to keep an eye on this week

Deliver to `REPORT_DELIVERY`.

## Workflow 2: Daily rank-progress loop

Create a recurring task (default: daily `TACTIC_TIME`) with this goal:

> Your goal is to rank #1 for `TARGET_KEYWORD`. Every morning, tell us one tactic we can take to get closer to that goal, and measure whether we made positive or negative progress in the last 24 hours.

Each run should: check the current position for `TARGET_KEYWORD`, compare to yesterday, state the delta plainly, and recommend exactly one high-leverage tactic for today.

## Ship the gaps

The reports and the daily loop surface content gaps and keyword opportunities. When you want to act on one, the agent can:

- Draft the page or post targeting the identified keyword, in your brand voice.
- Load it into your `CMS` as a draft and assign an author for review.
- Write a supporting blog post with example prompts and demo outputs when documenting a new play.

Keep a human in the loop on publish: the agent drafts and stages, a person approves.

## Customizing

- Swap the backlink tool or analytics source to match your stack.
- Track multiple target keywords by cloning Workflow 2 per keyword.
- Tune the report sections to the questions your team actually asks each week.
