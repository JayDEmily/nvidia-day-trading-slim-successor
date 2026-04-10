# Worked Example Skeleton: Controlled Continuity Execution Pack

## What this is

This is not an active repo brief.
It is a skeleton showing how the generic template should be populated for a post-audit execution pack that must finish bounded cleanup work without forcing operator relay after every internal gate.

## Example scenario

Assume the repo has already completed:
- the retained-surface audit;
- the retained-test inventory;
- the first-pass decision register; and
- the handoff queue for execution families.

The next pack now needs to:
- move archive-only historical tests out of the active test tree;
- retire duplicates;
- rewrite successor-boundary tests;
- retarget kept test families to successor-native authority; and
- close with no active pack routed so the repo is ready for later architecture work.

## Planning-thread framing

Assume you are a planning thread writing for a coding thread.
Your job is to read the repo first, then write a brief that tells the coding thread exactly:
- which decision rows belong to Gate 1, Gate 2, and Gate 3;
- which files each leaf owns;
- which fallout repairs are allowed;
- which proof slices close each gate;
- which stop conditions end the run immediately; and
- what the final router state must be after the last gate.

## Controlled continuity requirements the gate master must answer

1. What is the exact authorised gate sequence?
2. What pack-install proof must pass before the first gate opens?
3. Does each gate have to merge to `main` before the next gate opens? If yes, say so explicitly.
4. What exact stop conditions end the run?
5. What broad proof is explicitly excluded?
6. What must the final router state be after the last gate?

## Example gate cluster

### Gate A: Archive-only moves and duplicate retirements
- owned decision rows: archive-only planning receipts, archive-only closeout receipts, duplicate replay rows
- allowed fallout: move manifests, archive destination tree, direct test imports broken only by those moves
- stop if: archive destination would require source-repo mutation, or an archive-only test is still needed by a live family without a lawful replacement

### Gate B: Successor-boundary rewrite and light retarget
- owned decision rows: successor-boundary rewrite, compatibility wrapper retarget, replay-authority retarget
- allowed fallout: direct helper updates only where those exact tests need them
- stop if: rewrite would require runtime/service/schema mutation rather than test-surface retargeting

### Gate C: Broader retained-family retarget and closeout
- owned decision rows: review/trace retarget, runtime-contract retarget, invariant/lawful-output retarget, final keep-as-is confirmation
- allowed fallout: bounded repair only where the declared kept families are touched directly
- stop if: proof widening would jump into unrelated execution families or require a new pack

## Example leaf emphasis

A good leaf for this kind of execution pack should explicitly say:
- which exact decision rows it owns;
- which exact files it may touch;
- which fallout it may repair;
- which fallout it must not repair;
- which proof slice is authoritative; and
- whether the next gate may open automatically after merge or whether the run must stop.

## Closeout rule

The pack is successful only if:
- each gate closes truthfully;
- each gate merges back to `main` when the pack requires that;
- the router quartet moves together at every gate closeout; and
- the last gate returns the repo to the exact final router state declared in the gate master.
