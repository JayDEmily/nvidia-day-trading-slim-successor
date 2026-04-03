# 2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_GATES_v1

Status: active options-trace integrity repair pack from Gate 182 on `main`
Purpose: repair the confirmed options-trace integrity defects, add the bounded surface-anchor divergence feature, and close the pack with truthful proofs and router updates.
Authority: subordinate to `docs/01_NORMATIVE.md`, `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`, and repo-root `PLANS.md`.
Vocabulary authority for this pack: `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
Packet/data contract authority for this pack: `docs/03_DOMAIN_MODEL.md`

## Why this tranche exists

A bounded findings-verification pass against the current repo confirmed three immediate repair targets and one bounded feature gap:

- F1 is a confirmed bug: implied-volatility units are inconsistent across real-data fixtures, runtime preparation, and standalone options-context tests.
- F2 is a confirmed architectural defect: the persisted/API option-surface contract is weaker than the richer replay/runtime option-quote contract used by the real-data loader.
- F4 is a confirmed bug: dominant-strike and strike-cluster ranking become order-dependent when weighting truth is absent or zero.
- F3 is not confirmed as a defect in current behaviour, but it is a real capability gap: the packet cannot express surface-anchor divergence versus live spot, so the current classifier cannot represent that desk-visible translation fact.

F5 from the findings report is intentionally out of scope for this tranche. Workbook doctrine remains evidence input only and is not to be treated as a replacement raw runtime bundle.

## Intent and workflow anchor

This pack is a feature-and-integrity tranche. It sits after the closed Gate 180 master/child integration pack and before any wider options/playbook expansion. The pack must:

1. freeze one canonical options-field unit contract;
2. align persisted/API raw option surfaces with the richer runtime chain contract where the repo claims to expose raw rows;
3. fail closed when weighting truth for pinning/cluster inference is absent;
4. add one bounded derived feature for surface-anchor divergence and thread it through the options-flow path without inventing a second playbook engine;
5. close with truthful proof slices, router updates, and a fresh full-history zip.

## In scope

- options IV unit contract and ingress normalisation
- raw option-surface DB/API parity for fields the runtime consumes
- dominant-strike / cluster weighting fail-closed semantics
- one bounded surface-anchor divergence feature carried from prepared snapshot through options cognition/classification
- targeted runtime, schema, service, and planning proofs needed to close the tranche honestly

## Out of scope

- workbook replacement for raw runtime truth
- unrelated parallel-risk lane expansion
- unbounded options classifier redesign
- new playbook families
- UI/reporting changes beyond what is needed for truthful packet/API/schema exposure

## Retain / retire-from-authority / amend / add matrix

### Retain
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/planning/tranche_briefing_template_pack/*`
- `docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_*`
- current real-data fixtures as evidence input until a later gate explicitly amends them

### Retire from active authority
- no active pack currently routed statement in repo-root `PLANS.md`
- current active-gate marker of `none` in the canonical gate map

### Amend
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- this pack's leaves ledger and execution log as execution proceeds
- packet/schema/service/test surfaces named gate-by-gate below

### Add
- active options-trace integrity repair gates/leaves/execution-log/checklist/scope-note surfaces
- Gate 181 bootstrap receipt
- one planning-pack proof file for this tranche
- later gate receipts for Gates 182-186

## Gate structure

### Gate 181 — Options-trace integrity repair pack bootstrap
Purpose: install the planning quartet and scope note, classify findings truthfully, and route the repo to Gate 182 on `main`.

Primary outputs:
- active planning quartet and scope note
- Gate 181 receipt
- planning-pack proof test

### Gate 182 — Canonical IV unit contract and ingress normalisation
Purpose: freeze one canonical IV unit contract, normalise or reject percent-style ingress, and align standalone tests with the real-data path.

Primary repo surfaces:
- `src/nvda_desk/services/options_flow_context.py`
- `src/nvda_desk/services/real_data_loader.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/schemas/dataset.py`
- `tests/test_options_flow_context.py`
- any packet/docs/tests that must state the unit contract explicitly

Definition of done:
- one canonical IV unit is declared and enforced at ingress or schema boundary
- standalone options-context tests use the same unit contract as the real-data path
- proof shows classification no longer flips because of mixed decimal-versus-percent test inputs

### Gate 183 — Raw option-surface persistence and API parity
Purpose: align the persisted/API raw option-surface contract with the runtime option-quote contract for fields the runtime actually consumes.

Primary repo surfaces:
- `src/nvda_desk/db/models.py`
- `src/nvda_desk/schemas/options.py`
- `src/nvda_desk/services/market_state.py`
- `src/nvda_desk/schemas/dataset.py`
- migrations or compatibility surfaces if needed
- API/storage tests covering raw row truth versus reduced views

Definition of done:
- any surface that claims to expose raw chain rows can lawfully carry the fields required by the runtime options-preparation path, including IV/gamma and related per-row fields
- reduced payloads, if retained, are explicit reduced views rather than silent raw-row substitutes
- proof covers persistence/API retrieval truth

### Gate 184 — Dominant-strike and cluster fail-closed weighting semantics
Purpose: stop pinning/cluster inference from collapsing to row order when weighting truth is absent.

Primary repo surfaces:
- `src/nvda_desk/services/real_data_loader.py`
- packet/schema surfaces carrying dominant-strike or cluster outputs if semantics change
- targeted tests for zero-weight and missing-weight paths

Definition of done:
- dominant strike is absent or explicitly non-actionable when no lawful weighting signal exists
- cluster ranking does not silently depend on source ordering when weights are empty
- proofs cover zero/empty weight edge cases directly

### Gate 185 — Surface-anchor divergence feature and options-flow threading
Purpose: add one bounded derived feature representing surface-anchor divergence versus live spot and carry it end-to-end through prepared snapshots, cognition input, and options-flow classification.

Primary repo surfaces:
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` if new canonical naming is required
- `src/nvda_desk/schemas/dataset.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/real_data_loader.py`
- `src/nvda_desk/services/chain_to_cognition.py`
- `src/nvda_desk/services/options_flow_context.py`
- prepared/runtime fixtures and targeted proofs

Definition of done:
- one bounded derived feature is named canonically and carried through the runtime packet chain
- the feature is computed from lawful near-spot option-row evidence rather than screenshots or chat description
- options-flow output can distinguish ordinary balanced flow from materially anchored-away surface conditions without becoming an unbounded new engine

### Gate 186 — End-to-end proof, router closeout, and packaging
Purpose: prove the repaired options path honestly, close the pack, and package the exact green repo state.

Primary repo surfaces:
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- this pack's leaves ledger and execution log
- Gate 186 closeout receipt
- any final fixture/test updates required by Gates 182-185

Definition of done:
- selective and wider proofs required by the leaves ledger are green
- router/control surfaces agree on the active/closed state
- a fresh full-history zip is produced from the exact green repo state

## Document-touch checklist requirement

Execution must maintain the active planning quartet together:
1. repo-root `PLANS.md`
2. canonical gate map
3. active leaves ledger
4. active execution log

The bounded-scope note is also mandatory for this pack because the incoming findings report contains mixed categories: confirmed bugs, one capability gap, and one doctrine-only caution.

## Contradiction scan and state-integrity rules

Contradiction scan result before pack creation:
- no material contradiction exists between the repo routing surfaces; the repo is cleanly on `main` with no active pack currently routed
- the findings report itself is opinionated rather than authoritative, so this pack carries an explicit findings-truth split instead of treating every finding as a bug

State-integrity rules for this pack:
- `completed_leaf_ids` and `remaining_leaf_ids` must remain disjoint
- every named leaf id must exist in the leaves map
- multi-gate operator requests do not waive per-gate sequencing, validation, routing updates, or closeout
- Gate 186 closeout tests must permit the later lawful state where the Gate 180 pack remains closed evidence while this pack becomes the active or latest closed pack
