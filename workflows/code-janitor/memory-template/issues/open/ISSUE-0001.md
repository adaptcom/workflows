# ISSUE-0001: Example: remove dead helper `formatLegacy`

- category: dead-code
- severity: low
- effort: S
- estimated_lines: -22
- splittable: no
- status: open
- found: 2026-01-01T09:00
- fixed:

## Description

`formatLegacy()` in `src/util/format.ts` has no remaining call sites (verified with a
repo-wide search). It duplicates `format()` and only existed for a migration that is done.

## Proposed fix

Delete the function and its unit test. Confirm dead-code check and tests stay green.

## Notes / learnings

This file is an EXAMPLE seeded with the template. Replace or delete it on your first real run.
