# YYYY-MM-DD_<TRANCHE_NAME>_EXECUTION_LOG_v1

Status: active execution log for <tranche>; Gate <N> active on `work/<gate-branch-name>`, Gate <N+1> planned until Gate <N> closes

## Purpose

Carry sequential execution receipts only.

## Receipt rules

For every completed leaf record:
- gate id;
- leaf id;
- branch name;
- start commit;
- end commit or merged main commit;
- exact files touched;
- exact validation commands;
- observed results;
- whether the full suite was required;
- any stop condition or contradiction report that was hit;
- whether the state-integrity checks passed;
- whether the receipt was recorded live or reconstructed after the fact.

GitHub branch, commit, and merge history is the default routine execution ledger.
A full-history zip is only required when the operator explicitly requests backup, offline handoff, or sandbox transfer packaging.

## Gate <N> receipts

### LEAF-G<N>-001 — <imperative title>

- gate id: `Gate <N>`
- leaf id: `LEAF-G<N>-001`
- branch name: `work/<gate-branch-name>`
- start commit: `<sha>`
- end commit or merged main commit: `<sha or merged label>`
- exact files touched: `<file>`, `<file>`
- exact validation commands: `<command>`
- observed results: `<exact result text>`
- full suite required: `<true|false>`
- stop condition or contradiction report hit: `<none or explicit blocker>`
- state-integrity checks passed: `<true|false or explicit defect>`
- receipt recorded: `<live closeout receipt on work branch | reconstructed after the fact>`
