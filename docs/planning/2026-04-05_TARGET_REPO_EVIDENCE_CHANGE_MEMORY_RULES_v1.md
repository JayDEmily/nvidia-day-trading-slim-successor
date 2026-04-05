# 2026-04-05_TARGET_REPO_EVIDENCE_CHANGE_MEMORY_RULES_v1

Status: Gate 201 planning authority; change-control, supersession, and authority-downgrade memory rules for later evidence governance.

## Purpose

Define how future gates will record evidence movement across authority states so the repo can retire, supersede, or downgrade evidence surfaces without losing historical traceability.

## Mandatory change-memory fields

Every future change-memory row or supersession note must record:

- `surface_id`
- `evidence_class`
- `prior_authority_state`
- `new_authority_state`
- `reason_for_change`
- `effective_gate`
- `effective_branch_or_main_state`
- `successor_surface_id` (or explicit `none` when there is no successor)
- `supporting_receipt_or_doc`
- `compatibility_window` (if compatibility-only carriage remains)
- `deletion_status` (`retained`, `compatibility_only`, `retired_from_authority`, or `deleted_with_receipt`)

## Allowed authority states

- `canonical_authority`
- `admitted_derived`
- `review_or_replay_evidence`
- `market_persisted_reference_state`
- `compatibility_only`
- `retired_from_authority`
- `superseded_retained`
- `deleted_with_receipt`

## Change-memory rules

### Retire from authority is not delete from repo
A surface may leave authority while staying in the repo for traceability.

Required behaviour:
- record the downgrade explicitly;
- name the reason;
- name the successor when one exists.

### Delete requires a receipt
If a future gate removes a checked-in evidence surface, the deletion must cite:
- the exact deleted surface;
- the successor or rationale for no successor;
- the gate and receipt that approved deletion.

### Compatibility-only means carriage without authority
Use this state when a surface remains to support historical tests, parsers, or references but may no longer govern new work.

### Evidence-only standalone docs may not regain authority silently
This rule exists because the old standalone Gates 200-212 were demoted to evidence-only.
Any later reuse must cite the repo-native successor doc that re-admits the idea.

## Required downgrade patterns

### Raw anchor superseded by stronger raw anchor
- prior raw anchor becomes `superseded_retained`
- new raw anchor becomes `canonical_authority`
- both anchors remain referenceable

### Derived artefact regenerated against the same anchor
- old derivative becomes `superseded_retained` or `deleted_with_receipt`
- new derivative remains `admitted_derived`
- exact upstream anchor and producing service must be recorded

### Historical planning surface retired from authority
- old planning surface becomes `retired_from_authority` or `compatibility_only`
- successor repo-native planning surface becomes `canonical_authority`
- reason must name the contradiction or sequencing defect that forced the downgrade

## What later work must not do

- delete historical evidence merely to hide drift;
- mark a surface retired without naming the successor or stating that no successor exists;
- let evidence-only standalone materials regain canonical authority by implication;
- mutate the raw/derived boundary without an explicit state-change record.
