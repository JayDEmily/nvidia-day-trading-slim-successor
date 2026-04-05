# 2026-04-05_TARGET_REPO_EVIDENCE_SEMANTIC_REVIEW_AND_DISAGREEMENT_MEMORY_RULES_v1

Status: Gate 202 planning authority; semantic-review worksheet, rejection-memory, and disagreement-capture rules.

## Purpose

Define how later review-governance work will record judgement calls, conflicting interpretations, and rejected readings without mutating canonical evidence or pretending reviewer judgement is raw runtime truth.

## Required worksheet fields

Every later semantic-review worksheet row must record:

- `worksheet_id`
- `reviewed_surface_id`
- `review_context` (`bounded_trace`, `replay_review`, `coverage_review`, or later admitted context)
- `review_evidence_block_id`
- `interpretation_id`
- `judgement_statement`
- `review_outcome`
- `disagreement_state`
- `rejected_interpretation_ids`
- `reason_packet_or_report_anchor`
- `authoring_gate`
- `compatibility_state`

## Allowed disagreement states

- `no_disagreement_recorded`
- `active_disagreement`
- `rejected_interpretation_retained`
- `resolved_with_memory`

## Allowed review outcomes reused from repo-native review law

- `review_not_eligible`
- `review_no_change`
- `bounded_adjustment_request`
- `candidate_replacement_request`
- `research_reset`
- `missing_module_suspicion`

## Memory rules

### Reviewer judgement is supporting review evidence
It may explain how an admitted surface was interpreted, but it does not become raw evidence or market truth.

### Rejected interpretations stay visible
If one reading is rejected, later summaries must retain a pointer to that rejected interpretation and the reason it failed.

### Disagreement resolution must preserve both sides
When disagreement resolves, the final note must keep:
- the accepted interpretation;
- the rejected interpretation or interpretations;
- the evidence block that resolved the disagreement.

### Worksheet memory stays outside runtime outputs
Semantic-review memory may inform later governance and collection decisions, but it must not be merged into runtime packets under `src/` as if it were live deterministic state.

## Review-evidence block expectations

Later semantic-review work must tie every worksheet to a governed evidence block that names:

- the exact evidence family under review;
- the slice being reviewed;
- the scorecard axes that triggered review;
- the related gap-register row when a gap is implicated.

## What later work must not do

- compress disagreement into a single prose verdict without preserving the rejected reading;
- convert reviewer judgement into raw-anchor or derived-packet authority;
- record a review outcome with no linked evidence block;
- allow summaries to erase prior rejected interpretations.
