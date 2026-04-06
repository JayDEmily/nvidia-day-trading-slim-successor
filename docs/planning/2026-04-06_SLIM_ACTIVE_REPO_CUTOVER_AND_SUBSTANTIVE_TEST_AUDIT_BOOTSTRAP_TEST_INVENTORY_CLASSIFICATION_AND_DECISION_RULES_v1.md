# 2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_INVENTORY_CLASSIFICATION_AND_DECISION_RULES_v1

## Purpose

Freeze how the slim successor repo will classify retained tests and decide whether each test family is kept, retired, rewritten, or moved after the cutover.

## Required inventory fields

Every retained-test row must record:
- `test_id`
- `path`
- `historical_gate_lineage`
- `test_family`
- `bug_surface_class`
- `testing_phase_alignment`
- `authoritative_inputs`
- `runtime_owner_or_planning_owner`
- `downstream_consumer_or_control_surface`
- `current_truth_dependency`
- `status_candidate`
- `decision_outcome`
- `evidence_anchor`
- `disagreement_state`
- `next_action_pack`
- `notes`

## Allowed test families

- `planning_governance`
- `control_surface_integrity`
- `runtime_contract`
- `runtime_scenario`
- `invariant_or_lawful_output`
- `compatibility_wrapper`
- `review_or_trace`
- `replay_regression`
- `data_path_or_fixture`
- `repo_hygiene`
- `migration_or_closeout_guard`

## Allowed decision outcomes

- `keep_as_is`
- `keep_but_retarget_authority`
- `rewrite_for_successor_truth`
- `move_to_archive_evidence_repo`
- `retire_duplicate`
- `retire_unproven_or_orphaned`
- `defer_requires_new_anchor_or_runtime_change`

## Classification rules

### 1. Testing doctrine first
Classify against `docs/TESTING_AND_PROMOTION.md` bug-surface and phase law before using file-name heuristics.

### 2. Runtime authority first
If a test touches runtime surface ownership or compatibility-carriage law, classify it against the adopted `07` ledger plus `docs/03_DOMAIN_MODEL.md`.

### 3. Planning guards are not automatically runtime guards
A source-repo planning test may remain useful, but it must not be auto-kept as a successor runtime guard merely because it is green today.

### 4. Historical closeout strings are weak evidence
A test whose primary truth surface is a closed source-repo active/closed string must usually be rewritten for successor truth or moved back to the archive/evidence repo.

### 5. Duplicate derivation paths are not breadth
If multiple tests assert the same narrow control-surface outcome with no new bug surface, the later one is a redundancy candidate.

### 6. Orphan rule
A retained test that no longer maps cleanly to a current successor authority surface, runtime owner, or downstream consumer is an orphan and must not be silently kept.

### 7. Disagreement memory rule
If reviewers disagree on whether a test is stale, the decision register must preserve the rejected reading and the evidence that resolved it.

## What later work must not do

- keep a test only because it has a high gate number;
- retire a test only because it references an older planning pack;
- claim “rewrite” without naming the new authoritative inputs;
- move a test out of the slim repo without proving it is genuinely archive-only;
- hide deferred decisions in prose without a decision-register row.
