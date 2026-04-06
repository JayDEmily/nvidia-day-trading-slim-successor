# 2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_SCOPE_NOTE_v1

## Why this pack exists

The closed bootstrap pack already did the thinking work.
This pack is the execution work.

The operator objective is to end the retained-test cleanup loop fast enough that the repo can return to architecture and bounded real-data progress.

## Controlled continuity rule

Codex is pre-authorised to continue from Gate 222 through Gate 225 in one continuous run **only if**:
- each gate starts from `main`;
- each gate gets its own branch;
- each gate closes truthfully before the next one starts;
- each gate merges back to `main`;
- no gate-local stop condition fires.

If any proof slice fails or any stop condition fires, continuity ends immediately.

## What this pack is allowed to do

- move archive-only tests out of active `tests/`;
- retire duplicate tests;
- rewrite the single successor-boundary test classified for rewrite;
- retarget kept families to successor-native doctrine;
- repair only the fallout caused by those changes.

## What this pack is not allowed to do

- mutate the source/archive repo;
- invent a new architecture tranche inside the cleanup pack;
- widen into repo-wide blind execution by default;
- silently treat keep-as-is families as rewrite targets without a declared fallout reason.
