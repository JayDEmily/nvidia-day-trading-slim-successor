# 2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_07_SOURCE_DIFF_AND_AGENTS_READ_TRIGGER_NOTE_v1

## Purpose

Freeze the exact doctrine-level delta between the source repo's current `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` and the attached rescoped rewrite, then state the minimum `AGENTS.md` update required so Codex does not lose the document during successor-pack installation.

## Observed source-versus-rewrite diff

Observed against the source repo's current `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` and the attached `07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER_RESCOPED_v2.md`:

1. the rewrite adds a new **Section 0: Classification and read-trigger**;
2. the rewrite expands **Section 1** with an explicit narrow-purpose bullet set;
3. the rewrite adds **Section 1.1: Relation to the wider doc stack**; and
4. the rewrite adds **Section 1.2: Maintenance law**.

No additional content delta was observed in Sections 2-6 in the diff inspected for this planning pass.

## Why this matters before the longer successor audit pack runs

- The new Section 0 changes how the document is meant to be consumed: specialised authority, not universal front-door doctrine.
- The added read-trigger is the missing behavioural instruction Codex needs so runtime-surface, replay, bounded-trace, and compatibility-wrapper work reads `docs/07...` at the right time.
- Without an explicit `AGENTS.md` bridge, the successor repo could carry the rewritten `docs/07...` text but still behave as if the file were invisible except by operator memory.

## Required successor-repo action in Gate 217 pack install

Gate 217 pack installation must do all of the following in the slim successor repo:

1. replace `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` with the attached rescoped rewrite;
2. amend `AGENTS.md` so it explicitly says `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` is a **specialised runtime authority ledger**, not a baseline front-door read for every task; and
3. add a behavioural read-trigger in `AGENTS.md` telling Codex to read `docs/07...` whenever work touches:
   - runtime surface ownership;
   - stage packet versus workflow packet authority;
   - compatibility surface or compatibility carriage law;
   - downstream runtime reader permissions;
   - replay, bounded-trace, or review seam interpretation; or
   - API compatibility wrappers that preserve older read shapes over newer canonical runtime truth.

## What this action must not claim

- It must not claim runtime behaviour changed merely because the doctrine text was rewritten.
- It must not move `docs/07...` into the top-level frozen reading order for unrelated planning-only tasks.
- It must not reopen the source repo or pretend the source repo's closed Gate 210 pack already executed this rewrite.

## Gate 218 successor verification result

Gate 218 verified that the installed successor-repo `docs/07...` file matches the rescoped rewrite rather than the older source-repo text by checking for the new Section 0 classification/read-trigger and the added Sections 1.1 and 1.2.

Gate 218 also verified that the installed successor-repo `AGENTS.md` carries the matching specialised-authority posture and the required runtime-domain read-trigger.

This verification freezes how the later test audit must read `docs/07...` and `AGENTS.md` together. It does not claim that runtime semantics changed during Gate 218.
