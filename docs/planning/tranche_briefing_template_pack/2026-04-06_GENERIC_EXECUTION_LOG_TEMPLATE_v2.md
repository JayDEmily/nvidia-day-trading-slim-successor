# YYYY-MM-DD_<TRANCHE_NAME>_EXECUTION_LOG_v2

Status: active execution log for <tranche>; Gate <N> active on `work/<gate-branch-name>`; later gates are either planned or explicitly authorised by the active pack's continuity model.

## Purpose

Carry pack-install receipts, sequential gate receipts, and terminal closeout state only.

## Pack-install / router-activation receipt

Record this once when the pack becomes active.

- activation branch or direct-main install commit: `<sha>`
- environment fact: `<exact interpreter or environment statement>`
- router proof command(s): `<command>`
- observed result(s): `<exact result text>`
- router state after install: `<active pack and active gate>`
- continuity model after install: `<default stop-after-gate | controlled continuity with named gate sequence>`

## Receipt rules

For every completed gate record:
- gate id;
- branch name;
- start commit;
- branch closeout commit;
- merge commit on `main` where relevant;
- merge type where relevant;
- exact files touched;
- exact validation commands;
- observed results;
- whether the full suite was required;
- any stop condition or contradiction report that was hit;
- whether the state-integrity checks passed;
- whether the next gate opened or the run stopped;
- whether the receipt was recorded live or reconstructed after the fact.

GitHub branch, commit, and merge history is the default routine execution ledger.
A full-history zip is only required when the operator explicitly requests backup, offline handoff, or sandbox transfer packaging.

## Gate <N> receipts

### LEAF-G<N>-001 — <imperative title>

- gate id: `Gate <N>`
- leaf id: `LEAF-G<N>-001`
- branch name: `work/<gate-branch-name>`
- start commit: `<sha>`
- branch closeout commit: `<sha>`
- merge commit on `main`: `<sha or not yet merged>`
- merge type: `<non-fast-forward | fast-forward | not yet merged>`
- exact files touched: `<file>`, `<file>`
- exact validation commands: `<command>`
- observed results: `<exact result text>`
- full suite required: `<true|false>`
- stop condition or contradiction report hit: `<none or explicit blocker>`
- state-integrity checks passed: `<true|false or explicit defect>`
- next gate opened or stopped: `<opened Gate <N+1> | stopped>`
- receipt recorded: `<live closeout receipt on work branch | reconstructed after the fact>`

## Gate <N> closeout summary

- final gate status: `<complete | stopped | blocked>`
- final `main` head after merge: `<sha or not yet merged>`
- router state after gate closeout: `<exact active gate or stop state>`

## Final pack closeout

When the last authorised gate closes, record:
- final router state: `<no active pack currently routed | exact next routed pack>`
- whether continuity completed as authored: `<true|false>`
- any declared stop condition that ended the run: `<none or explicit blocker>`
