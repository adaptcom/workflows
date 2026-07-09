# Reproduction and fix playbook

## Strong-repro categories

- **Frontend rendering/state:** run the app or preview, follow exact steps, inspect console/network, capture before/after screenshots.
- **Pure logic:** write a minimal failing unit test or input/output script.
- **HTTP/API:** replay a sanitized request, verify status/body, trace validation/auth/side effects.
- **Build/type errors:** run the narrow command that demonstrates the failure and capture the exact output.
- **Data shape:** use read-only queries against sanitized or test data; identify the violated invariant.

## Weak-repro categories

Intermittent infrastructure failures, external-provider outages, production-only races, and permission-dependent bugs may be impractical to reproduce locally. File an investigation when the evidence is credible and the missing observation is clear.

## Time-boxing

- Spend enough time to identify the responsible area and one plausible hypothesis.
- Stop when further work needs unavailable access, unsafe production mutation, or a large environment build.
- Record commands, inputs, logs, and paths checked.

## Immediate-fix gate

Fix now only when all are true:

- Root cause is understood.
- Scope fits `FIX_BUDGET`.
- A regression test or deterministic validation exists.
- The change does not require a product decision or risky migration.
- Repository checks can run before the PR is opened.
