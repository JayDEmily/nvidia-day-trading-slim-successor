# 2026-04-05_TARGET_REPO_EVIDENCE_COVERAGE_SCORECARD_AND_GAP_REGISTER_v1

Status: Gate 202 planning authority; coverage scorecard and gap-register baseline for later evidence expansion.

## Purpose

Define how later evidence proposals will be judged against the current admitted evidence portfolio so the repo can tell the difference between broader coverage, stronger coverage, and redundant carriage.

## Coverage scorecard axes

The scorecard must stay repo-native and must reuse the frozen stability/review vocabulary where it fits.
Every later evidence proposal must be scored across these axes before admission:

| Axis | Question answered | Allowed states | Evidence classes touched now |
|---|---|---|---|
| `anchor_class_coverage` | Does the proposal add a missing evidence class or only repeat one already present? | `missing`, `thin`, `adequate`, `broad` | raw anchor, derived pack, sibling review pack, replay pack, market-persisted reference state |
| `lineage_completeness` | Can the proposal name its exact upstream anchor, producer path, and downstream consumers? | `missing`, `partial`, `complete` | all classes |
| `slice_coverage` | Does the proposal add event, regime, or session slices not already represented? | `none`, `narrow`, `meaningful` | raw, sibling, replay, review-report |
| `consumer_relevance` | Does the proposal support a live repo consumer or only create orphan evidence? | `orphaned`, `review_only`, `consumer_bound` | review/replay/runtime/planning consumers |
| `review_depth` | Does the proposal support governed review outcomes or merely restate current summaries? | `none`, `bounded`, `material` | sibling, replay, review-report |
| `novelty_strength` | Is the proposal new information, a stronger variant of current information, or an unchanged duplicate? | `duplicate`, `adjacent`, `strengthening`, `new_family` | all classes |
| `disagreement_visibility` | If the proposal conflicts with current review truth, does it preserve explicit disagreement memory? | `hidden`, `stated`, `resolved_with_memory` | review/report/worksheet surfaces |

## Gap-register fields

Every later gap register row must record:

- `gap_id`
- `missing_surface_or_axis`
- `related_evidence_class`
- `why_current_portfolio_is_insufficient`
- `collection_or_derivation_candidate`
- `blocking_consumer_or_review_need`
- `priority_state` (`defer`, `watch`, `next_tranche`, `urgent_for_planned_gate`)
- `evidence_of_gap`
- `disallowed_shortcuts`

## Current portfolio scorecard baseline

| Current evidence family | anchor_class_coverage | lineage_completeness | slice_coverage | consumer_relevance | review_depth | novelty_strength | disagreement_visibility |
|---|---|---|---|---|---|---|---|
| canonical raw runtime anchor | thin | complete | narrow | consumer_bound | bounded | new_family | stated |
| prepared runtime derivative | thin | complete | narrow | consumer_bound | bounded | strengthening | stated |
| bounded sibling trace pack | thin | complete | narrow | review_only | material | new_family | stated |
| bounded trace report | thin | complete | narrow | review_only | material | strengthening | stated |
| replay regression pack | thin | partial | narrow | review_only | bounded | new_family | stated |
| replay expected report | thin | partial | narrow | review_only | bounded | strengthening | stated |
| market-persisted reference state | thin | partial | meaningful | consumer_bound | none | new_family | hidden |

## Current explicit gaps

| Gap id | Missing surface or axis | Why it is a real gap now | Candidate next work family |
|---|---|---|---|
| `GAP-RAW-002` | second admitted raw anchor | one raw runtime bundle is insufficient to prove event/regime/session breadth | Gate 203 snapshot and real-anchor planning |
| `GAP-SLICE-001` | governed event/regime/session score summary | current inventory names classes but does not yet expose a frozen slice-coverage scorecard | Gate 202 closeout / later evidence-governance execution |
| `GAP-REVIEW-001` | semantic-review worksheet memory | bounded review exists, but no canonical worksheet/disagreement memory surface exists yet | Gate 202 closeout / later review-governance execution |
| `GAP-MARKET-001` | persisted market provenance dossier | market tables exist, but seeding/capture provenance is not yet recorded as a governed dossier | Gate 203 snapshot/collection planning |
| `GAP-REDUNDANCY-001` | explicit novelty/redundancy decision record | the repo has no frozen rejection memory for duplicate evidence proposals yet | Gate 202 closeout / later review-governance execution |

## Scorecard rules

- coverage must stay visible by class and by slice so thin sampling is not mistaken for breadth;
- a stronger derivative does not erase a raw-anchor gap;
- replay evidence may strengthen review depth, but it does not become a fresh raw anchor;
- persisted market state may improve consumer relevance while still remaining weak on provenance until its seeding source is governed explicitly.

## What later work must not do

- declare coverage broad when only one anchor exists for a class;
- treat a regenerated derivative as a new evidence family;
- hide portfolio gaps in prose without a gap-register row;
- confuse market persistence with admitted raw-anchor breadth.
