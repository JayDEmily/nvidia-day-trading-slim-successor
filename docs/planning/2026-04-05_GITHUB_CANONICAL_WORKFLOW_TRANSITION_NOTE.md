# 2026-04-05_GITHUB_CANONICAL_WORKFLOW_TRANSITION_NOTE

## Purpose

Freeze the repo's governance transition to a GitHub-native execution workflow while preserving repo-native planning and closeout authority.

## Transition point

GitHub is now canonical from Gate 201 milestone state.

## Routine zip retirement

Routine full-history zip handoff is retired for normal gate execution.
Zip remains allowed when the operator needs backup, offline transfer, sandbox transfer, or an explicit handoff artefact.

## What GitHub replaces

GitHub replaces routine execution logging through branch, commit, review, and merge history for normal gate work.

## What GitHub does not replace

GitHub does not replace repo-root `PLANS.md`, the canonical gate map, the active leaves ledger, the active execution log, or gate closeout receipts under `docs/planning/`.

## Operational consequence for Gate 202 onward

1. branch from canonical main.
2. Execute the gate on that branch.
3. Update planning and control surfaces together.
4. Merge the completed branch back to `main`.
5. use zip only when actually needed.
