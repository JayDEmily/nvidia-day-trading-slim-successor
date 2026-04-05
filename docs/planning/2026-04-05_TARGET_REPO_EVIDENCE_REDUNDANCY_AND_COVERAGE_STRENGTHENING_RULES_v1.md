# 2026-04-05_TARGET_REPO_EVIDENCE_REDUNDANCY_AND_COVERAGE_STRENGTHENING_RULES_v1

Status: Gate 202 planning authority; redundancy rejection and coverage-strengthening law for later evidence proposals.

## Purpose

Freeze the decision rules that later gates must use when deciding whether a proposed evidence surface should be admitted, rejected as redundant, or accepted only as a bounded strengthening of existing coverage.

## Core decision outcomes

Every later proposal must end in one of these governed outcomes:

- `reject_duplicate`
- `reject_unproven_lineage`
- `reject_consumer_orphan`
- `accept_strengthening_existing_family`
- `accept_new_slice_within_existing_family`
- `accept_new_family`
- `defer_pending_gap_priority`

## Redundancy tests

A proposal is redundant and must be rejected when any of the following are true:

1. it reproduces an existing anchor or derivative without adding a new governed slice;
2. it follows the same derivation path and produces the same consumer effect as an existing checked-in artefact;
3. it adds prose commentary without adding a new governed review surface or disagreement record;
4. it mirrors a replay/report surface already present with no change in reviewed ruleset, horizon, or scenario family.

## Strengthening tests

A proposal may strengthen coverage only when it does at least one of the following:

1. adds a new event, regime, or session slice inside an already-governed evidence family;
2. improves lineage completeness for a class currently marked partial;
3. binds an existing orphaned review surface to a governed consumer or closeout receipt;
4. exposes disagreement or rejection memory that is currently hidden;
5. upgrades a thin class toward adequate coverage without redefining class boundaries.

## New-family tests

A proposal is a new family only when it introduces a governed evidence class that is not already represented in the Gate 201 inventory baseline.
It must then name:

- exact anchor;
- producer path;
- authority surface;
- downstream consumers;
- why existing classes cannot serve the same purpose.

## Mandatory rejection memory fields

When a proposal is rejected or deferred, later governance surfaces must record:

- `proposal_id`
- `evaluated_against_surface_ids`
- `decision_outcome`
- `rejection_or_deferral_reason`
- `missing_requirement`
- `would_become_valid_if`
- `recorded_in_gate`

## Explicit repo-native rules

### Raw anchor versus derivative
A derivative can strengthen consumer relevance or review depth, but it cannot close a missing raw-anchor gap.

### Replay versus sibling review
Replay may strengthen chronology or horizon comparison, but it cannot substitute for disagreement memory or human semantic review evidence.

### Market-persisted state
A market table snapshot may strengthen consumer relevance, but it must be rejected as a broad-coverage claim if provenance remains partial.

### Review worksheet material
A review worksheet or disagreement note is not redundant merely because it references existing evidence. It becomes admissible only when it records a new governed judgement boundary, disagreement, or rejection reason.

## What later work must not do

- auto-admit any new artefact because it is more recent;
- accept duplicate derivation paths as if they added breadth;
- reject a proposal without recording why it failed;
- claim strengthening when the proposal adds no new slice, no lineage completeness, and no governed review memory.
