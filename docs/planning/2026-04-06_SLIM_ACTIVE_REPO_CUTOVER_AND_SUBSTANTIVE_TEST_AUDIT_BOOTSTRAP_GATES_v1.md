# 2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1

Status: closed slim-successor planning pack through Gate 221 on `work/gate-221-successor-proof-slice-and-handoff-20260406`; no active pack is currently routed. This pack is **not** active in the source repo.

## Purpose

Create the first slim-repo planning pack after Gate 210 so the successor repo can:
1. verify that the cutover was taken from the frozen post-Gate-210 source commit;
2. freeze the retained-versus-archive surface boundary;
3. integrate the rescoped specialised runtime-surface authority ledger;
4. perform the first substantive test-audit classification work; and
5. hand the slim repo a truthful successor execution queue without reopening the source repo's closed workflow-hardening pack.

## Scope

In scope:
- slim-repo bootstrap and source-cut parity verification;
- retained-surface inventory for runtime, doctrine, operator, planning, test, and fixture surfaces that actually move into the slim repo;
- replacement of the successor repo's `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` with the rescoped rewrite, plus the matching `AGENTS.md` read-trigger update;
- substantive test-audit classification work for the retained test inventory;
- explicit keep / retire / rewrite / move decision law and first-pass decision register for test families;
- successor proof-order and handoff boundaries for the next execution pack inside the slim repo.

Out of scope:
- reopening or rerouting a new active pack in the source repo;
- changing runtime behaviour under `src/nvda_desk/` during this bootstrap pack;
- packet, schema, DB, API, Alembic, or service-law rewrites unless a later explicit successor execution pack is opened for them;
- pretending the substantive test-audit has already executed before the successor repo exists;
- reviving historical Gate 212-style multi-repo packaging or any other dual-repo convergence endpoint.

## Supersession and active authority

- This document is the canonical gate authority surface for the slim successor bootstrap pack only.
- It does not reopen the source repo's closed workflow-hardening and active-repo reset foundation pack.
- It does not supersede any active pack in the source repo because repo-root `PLANS.md` there truthfully routes no active pack.
- The source repo remains the archive/evidence host for closed planning packs, receipts, contradiction reports, scope notes, salvage matrices, and older historical planning artefacts.
- The cutover brief and Gate 202 governance surfaces are evidence inputs to this pack, not the structural template for it.

## Governing inputs

Frozen doctrine and process inputs:
- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/TESTING_AND_PROMOTION.md`
- `AGENTS.md`
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`

Source-repo control and evidence inputs that justify this successor pack:
- source-repo `PLANS.md`
- source-repo `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- source-repo `docs/planning/2026-04-06_GATE210_SLIM_ACTIVE_REPO_CUTOVER_ENTRY_CRITERIA.md`
- source-repo `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md`
- source-repo `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json`
- source-repo `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md`
- source-repo `docs/planning/2026-04-05_GATE202_TARGET_REPO_COVERAGE_REVIEW_AND_DISAGREEMENT_PLANNING.md`
- source-repo `docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_COVERAGE_SCORECARD_AND_GAP_REGISTER_v1.md`
- source-repo `docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_REDUNDANCY_AND_COVERAGE_STRENGTHENING_RULES_v1.md`
- source-repo `docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_REVIEW_GOVERNANCE_PROOF_SLICE_v1.md`
- source-repo `docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_SEMANTIC_REVIEW_AND_DISAGREEMENT_MEMORY_RULES_v1.md`
- `07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER_RESCOPED_v2.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/planning/tranche_briefing_template_pack/*`

## Workflow placement

This tranche sits between:
1. the source repo closed through Gate 210 with no active pack routed; and
2. the first successor-repo execution pack that will actually mutate retained test surfaces after the audit decisions are frozen.

The chosen gate count is five because the successor work has five materially different jobs that should not be blurred together:
1. bootstrap the successor pack and freeze the cutover source truth;
2. install the rewritten `docs/07...` ledger plus the matching `AGENTS.md` read-trigger and then inventory retained surfaces against that successor doctrine baseline;
3. classify the retained test inventory against repo-native bug-surface and ownership law;
4. freeze keep / retire / rewrite / move decision law and the first-pass decision register;
5. define the proof slice and successor execution queue for the next active pack inside the slim repo.

The rescoped `07` work is folded into the first two gates rather than given a standalone gate because it is a specialised authority-carryover task that must land before the audit can classify runtime-surface tests truthfully. It is not a separate runtime implementation tranche.

## Intent and workflow anchor

The governing repo lens remains:
- one active pack at a time;
- GitHub branch, commit, and merge history as the default routine execution ledger;
- control surfaces must move together;
- runtime/latest-state authority must not be inferred from duplicated compatibility carriage;
- the slim repo becomes the active execution host, while the source repo remains the archive/evidence host.

This pack therefore establishes the successor repo as a truthful live execution home without letting the cutover blur into runtime mutation or letting the test audit become an improvised one-off review.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical in the successor repo
- the frozen doctrine stack (`docs/01` through `docs/06`, `docs/TESTING_AND_PROMOTION.md`)
- `AGENTS.md`
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
- repo-root `PLANS.md`
- the successor canonical gate map
- `src/`, `tests/`, `fixtures/`, and other runtime-supporting repo-native surfaces actually retained by the cutover
- `CHANGELOG.jsonl`
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_07_SOURCE_DIFF_AND_AGENTS_READ_TRIGGER_NOTE_v1.md`
- the tranche template pack under `docs/planning/tranche_briefing_template_pack/`

### Retire from authority in the successor repo
- the source repo's full historical planning tree as active material
- source-repo closeout receipts and closed pack artefacts except where one is intentionally retained as evidence input
- historical standalone gate numbers 211-216 as reusable canonical numbering inside the successor repo

### Mandatory amendments during execution
- successor-repo `PLANS.md`
- successor canonical gate map
- active successor leaves ledger
- active successor execution log
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
- any test-audit decision register or proof-slice doc introduced by this pack

### New additions
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1.md`
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json`
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md`
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_SCOPE_NOTE_v1.md`
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_CONTRADICTION_REPORT_v1.md`
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_RETAINED_SURFACE_MANIFEST_AND_CUTOVER_RULES_v1.md`
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_RUNTIME_SURFACE_AUDIT_READ_TRIGGER_AND_AUTHORITY_ADOPTION_v1.md`
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_INVENTORY_CLASSIFICATION_AND_DECISION_RULES_v1.md`
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_AUDIT_PROOF_SLICE_AND_SUCCESSOR_HANDOFF_v1.md`
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_07_SOURCE_DIFF_AND_AGENTS_READ_TRIGGER_NOTE_v1.md`

## Vocabulary discipline

- The active vocabulary authority must be read before introducing any new durable planning or runtime labels.
- This tranche should reuse existing terms where possible: `active pack`, `closed pack`, `retained surface`, `archive/evidence host`, `compatibility surface`, `workflow packet`, `stage packet`, `downstream reader`, and `proof slice`.
- `slim successor repo` is permitted here as an execution-host label, but it must not silently outrank existing repo-law terms.
- Do not invent new test classes when existing doctrine already names the bug surface, ordered testing phases, or leaf-specific validation classes.

## Packet / contract discipline

- `docs/03_DOMAIN_MODEL.md` remains the baseline packet/data contract authority.
- The rescoped `07` ledger becomes the specialised latest-state authority for runtime surface ownership, compatibility-carriage law, downstream reader law, and prohibited inference law in the successor repo.
- This bootstrap pack is governance and classification work only. It must not silently change schema shape, packet carriage, lineage contracts, API contracts, or DB contracts.
- If the test audit discovers a genuine contract mismatch, record it as a successor execution-pack requirement instead of folding runtime change into this bootstrap pack.

## Contradiction scan and state-integrity rules

The contradiction report for this pack is:
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_CONTRADICTION_REPORT_v1.md`

This pack freezes the following invariants:
- `completed_leaf_ids` and `remaining_leaf_ids` are disjoint;
- every referenced leaf id exists in the leaves ledger;
- active successor routing must point to exactly one active gate after import;
- no source-repo control surface is rewritten to pretend that this successor pack is active there;
- keep / retire / rewrite / move decisions for tests must preserve explicit evidence anchors and disagreement memory.

## Document-touch checklist

The checklist for this tranche is:
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_DOCUMENT_TOUCH_CHECKLIST_v1.md`

## Testing and promotion discipline

- Repo-local environment remains `.venv` via `make install` (`uv sync --extra dev`) in the successor repo.
- Minimum validation slice for this bootstrap pack:
  - `python -m pytest -q tests/test_gate217_slim_successor_pack_planning.py`
  - `python -m pytest -q tests/test_gate218_retained_surface_inventory_and_runtime_authority.py`
  - `python -m pytest -q tests/test_gate219_test_inventory_classification.py`
  - `python -m pytest -q tests/test_gate220_test_audit_decision_register.py`
  - `python -m pytest -q tests/test_gate221_successor_test_audit_handoff.py`
- Full-suite proof is not the default closeout path for this pack unless the cutover implementation or test-migration execution expands the blast radius into runtime/shared code.
- A gate is not complete until:
  - the declared targeted tests ran green;
  - successor `PLANS.md`, the successor canonical gate map, the active successor leaves ledger, and the active successor execution log moved together;
  - GitHub branch/commit/merge receipts were recorded in the successor repo; and
  - a full-history zip exists only if the operator explicitly requested backup, offline handoff, or sandbox transfer packaging.

## Gates

### Gate 217: Successor bootstrap and cutover-source freeze

**Objective**
- Create and route the first slim-repo planning pack, freeze the exact source-cut commit and cutover contradiction set, install the rewritten `docs/07...` ledger plus its `AGENTS.md` read-trigger during pack opening, and define the retained-surface manifest rules without pretending runtime work already moved cleanly.

**In-scope surfaces**
- successor `PLANS.md`
- successor canonical gate map
- new Gate 217 pack quartet and support artefacts
- successor `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
- successor `AGENTS.md`
- retained-surface manifest rules
- `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_07_SOURCE_DIFF_AND_AGENTS_READ_TRIGGER_NOTE_v1.md`
- targeted planning tests for Gate 217

**Definition of done**
- the new successor pack artefacts exist and are import-ready;
- the successor router/gate map truthfully route Gate 217 as the active gate;
- the exact source-cut commit `8f9c706093045a8bb333cc19e93d4021c326f761` is frozen as the only lawful bootstrap source; and
- the successor repo carries the rewritten `docs/07...` plus an `AGENTS.md` read-trigger that matches the rewrite's specialised-authority posture.

### Gate 218: Retained-surface inventory and runtime-authority verification

**Objective**
- Record exactly which runtime, doctrine, planning, operator, fixture, and test surfaces were retained in the successor repo, then verify that the rewritten `docs/07...` ledger and matching `AGENTS.md` read-trigger are present and are constraining downstream test classification correctly.

**In-scope surfaces**
- retained-surface manifest
- successor `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
- successor `README.md` or pack-local read-trigger note if needed
- targeted Gate 218 audit tests

**Definition of done**
- the successor repo has a retained-surface inventory rather than a vague “slim” label;
- the rewritten `07` ledger is present in the successor repo and its `AGENTS.md` read-trigger matches the specialised-authority posture;
- no claim is made that `07` runtime semantics changed merely because the doctrine carryover landed.

### Gate 219: Canonical retained-test inventory and ownership mapping

**Objective**
- Build the first canonical successor-repo test inventory, then map every retained test family to bug-surface doctrine, authoritative inputs, runtime owners, and downstream consumers.

**In-scope surfaces**
- retained test inventory baseline
- ownership/classification rules
- Gate 219 planning tests
- pack-local execution log and leaves updates

**Definition of done**
- the slim repo has one explicit retained test inventory baseline;
- every retained test family is classified against repo-native doctrine rather than file-name guesswork;
- orphan, duplicate, stale-planning, and successor-required tests are visible as explicit states.

### Gate 220: Keep / retire / rewrite / move decision law and first-pass decision register

**Objective**
- Apply explicit repo-native decision law to the retained test inventory and freeze a first-pass keep / retire / rewrite / move register with evidence anchors and disagreement memory.

**In-scope surfaces**
- test decision rules
- first-pass decision register fields
- Gate 220 planning tests
- pack-local execution log and leaves updates

**Definition of done**
- the successor repo has governed decision outcomes for retained tests;
- every rejected or deferred decision preserves explicit memory, not just a prose verdict;
- no test is moved, deleted, or rewritten yet under the false claim that classification equals execution.

### Gate 221: Proof slice, successor handoff, and next-pack queue

**Objective**
- Freeze the bounded proof slice for executing the classified test decisions, then hand the successor repo a truthful next-pack queue for actual keep / retire / rewrite / move execution.

**In-scope surfaces**
- successor proof-slice and handoff doc
- next-pack boundary note
- successor router/gate map closeout state for this bootstrap pack
- Gate 221 planning tests

**Definition of done**
- the successor repo has a deterministic proof order for the first execution pack after the audit;
- the next active pack boundary is explicit inside the successor repo;
- this bootstrap pack closes without reopening the source repo or claiming the execution tranche already ran.
