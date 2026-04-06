# 2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_SCOPE_NOTE_v1

## Purpose

State the bounded scope of the first slim-successor bootstrap tranche so the cutover, specialised runtime-authority adoption, and substantive test-audit classification work do not blur into runtime mutation or source-repo rerouting.

## In scope

- successor-pack bootstrap from frozen source commit `8f9c706093045a8bb333cc19e93d4021c326f761`;
- retained-surface inventory for what actually moves into the slim repo;
- adoption of the rescoped `07` runtime-surface ledger as a specialised authority surface in the successor repo;
- substantive test-inventory classification and ownership mapping;
- explicit keep / retire / rewrite / move decision law and first-pass decision register;
- successor proof-slice and next-pack handoff planning.

## Out of scope

- opening a new active pack in the source repo;
- source-repo router or gate-map edits that would pretend this successor pack is active there;
- runtime code, packet, schema, DB, or API changes inside this bootstrap pack;
- deleting or rewriting tests during classification;
- reviving historical Gates 211-216 as current canonical execution steps.

## Stop conditions

Stop and emit an updated contradiction report before continuing if:
- the successor cutover cannot name one exact source-cut commit;
- retained-versus-archive boundaries cannot be stated without guessing which surfaces are needed for live execution;
- the rescoped `07` document would need to be treated as a universal front-door doctrine file rather than a specialised latest-state authority;
- a test decision would require hiding disagreement or deleting rejection memory;
- the next execution queue cannot be stated without silently executing runtime changes first.

## Success condition

This tranche succeeds when the successor repo can truthfully say:
- the source-cut commit is frozen;
- retained runtime, doctrine, operator, planning, fixture, and test surfaces are inventoried;
- the updated `07` ledger is adopted as specialised authority;
- the retained test inventory is classified with explicit keep / retire / rewrite / move decisions; and
- the next successor execution pack is queued without reopening the source repo.
