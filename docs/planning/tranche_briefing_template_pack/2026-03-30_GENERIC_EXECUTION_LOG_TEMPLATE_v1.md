# YYYY-MM-DD_<TRANCHE_NAME>_EXECUTION_LOG_v1

Status: active execution log for <tranche>; Gate <N> complete on `main`, Gate <N+1> next

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
- any stop condition that was hit;
- whether the receipt was recorded live or reconstructed after the fact.

## Gate <N> receipts

### LEAF-G<N>-001 — <imperative title>

- Branch: `work/<gate-branch-name>`
- Start commit: `<sha>`
- End commit: `<sha or merged label>`
- Files touched: `<file>`, `<file>`
- Validations run: `<command>`
- Full suite required: <yes/no>
- Exact evidence: <what became true>
- Stop conditions hit: <none or explicit blocker>
- Merge status: <merged to main / not merged>
