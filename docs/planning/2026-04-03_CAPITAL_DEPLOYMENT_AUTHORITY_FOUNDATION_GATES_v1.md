# 2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_GATES_v1

Status: closed capital-deployment authority foundation pack through Gate 191 on `main`
Purpose: create the lawful planning pack and bounded implementation path for a first downstream `CapitalDeploymentAuthorityService` that decides whether an already-formed opening candidate deserves fresh capital now, and if so how much.
Authority: subordinate to `docs/01_NORMATIVE.md`, `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`, and repo-root `PLANS.md`.
Vocabulary authority for this pack: `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
Packet/data contract authority for this pack: `docs/03_DOMAIN_MODEL.md`

## Why this tranche exists

The repo now carries a lawful deterministic spine for temporal, regime, options-flow, posture, eligibility, execution, review, and the independent parallel-risk lane. It does not yet carry a bounded downstream consumer that decides whether the already-formed opening candidate deserves fresh capital now based on available capital and the already-computed opportunity/risk surfaces.

This pack exists to add that missing downstream capital-deployment decision slice without inventing a second cognition engine, without introducing close-position logic, and without pretending a full portfolio arbiter already exists.

## Intent and workflow anchor

This pack sits after the closed options-trace integrity repair pack and before any later held-position or close-position lifecycle work. The pack must:

1. freeze the scope and authority boundary for the first `CapitalDeploymentAuthorityService` slice;
2. admit the new naming through the vocabulary workflow in a later implementation leaf rather than smuggling terms into code silently;
3. define one bounded contract for the service input, decision output, and current-capital read path;
4. implement the service against the existing runtime result plus current capital snapshot only;
5. integrate the service into the lawful downstream seam without creating broker execution, recommendation memory, or position-close behaviour;
6. close with truthful proofs, router updates, and a fresh full-history zip.

## In scope

- planning-pack bootstrap and truthful routing
- bounded scope note and document-touch law
- vocabulary admission leaf for `CapitalDeploymentAuthorityService` and any directly-required companion terms
- one typed decision contract for capital deployment authority
- reading current capital from the repo-native capital snapshot path
- a first service that authorises deployment amount or stand-down for new opening recommendations only
- bounded runtime integration and targeted proofs needed to close the tranche honestly

## Out of scope

- close-position recommendations or lifecycle exits
- recommendation-history memory or last-five-recommendations logic
- broker synchronisation, fills, P&L accounting, or profit-aware sizing
- a full portfolio arbiter that reasons over all held exposures and cross-book interactions
- coefficient redesign, playbook-family redesign, or a second cognition spine
- UI/reporting changes beyond truthful schema/review carriage if needed for the bounded slice

## Retain / retire-from-authority / amend / add matrix

### Retain
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/planning/tranche_briefing_template_pack/*`
- `docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_*`
- existing capital snapshot and execution-record surfaces as current repo-native capital-read evidence

### Retire from active authority
- repo-root `PLANS.md` statement that no active pack is currently routed
- current active-gate marker of `none` in the canonical gate map

### Amend
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- this pack's leaves ledger and execution log as execution proceeds
- vocabulary authority if the new naming is admitted
- packet/schema/service/test surfaces named gate-by-gate below

### Add
- active capital-deployment authority foundation gates/leaves/execution-log/checklist/scope-note surfaces
- Gate 187 bootstrap receipt
- one planning-pack proof test for this tranche
- later gate receipts for Gates 188-191

## Gate structure

### Gate 187 — Capital-deployment authority pack bootstrap
Purpose: install the planning quartet and scope note, classify the bounded first slice truthfully, and route the repo to Gate 188.

Primary outputs:
- active planning quartet and scope note
- Gate 187 receipt
- planning-pack proof test

### Gate 188 — Authority boundary, vocabulary admission, and decision contract
Purpose: freeze the first-slice boundary, admit the required naming lawfully, and define one typed contract for capital-deployment authority input/output using existing runtime and capital-read surfaces.

Primary repo surfaces:
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/03_DOMAIN_MODEL.md` if a new canonical downstream decision surface or packet carriage is required
- `docs/04_TECHNICAL_ARCHITECTURE.md` if workflow placement must be made explicit
- `src/nvda_desk/schemas/cognition.py` and/or a new dedicated schema surface if the typed decision contract lands in code
- `tests/test_gate188_capital_deployment_authority_contract.py`

Definition of done:
- the first-slice boundary is explicit and excludes close logic, recommendation memory, and full-portfolio arbitration
- required naming is admitted through the vocabulary workflow instead of appearing ad hoc in code
- one typed service contract names the minimum lawful inputs and outputs

### Gate 189 — Current-capital read path and standalone service implementation
Purpose: implement `CapitalDeploymentAuthorityService` against the existing runtime result plus current capital snapshot only.

Primary repo surfaces:
- `src/nvda_desk/services/execution_records.py` if a small read helper or adapter is required
- `src/nvda_desk/services/capital_deployment_authority.py` or equivalent repo-native service path
- `src/nvda_desk/db/models.py` only if a compatibility-safe capital-read refinement is required
- bounded fixtures/tests covering buying power, stand-down, and capped deployment sizing
- `tests/test_gate189_capital_deployment_authority_service.py`

Definition of done:
- the service reads current capital from the repo-native capital snapshot path
- the service consumes the already-computed runtime result and returns a bounded deploy/stand-down decision without inventing upstream cognition
- a simple controlled capital bootstrap for proof data exists without creating a second ledger architecture

### Gate 190 — Downstream seam integration and review carriage
Purpose: thread the capital-deployment authority decision into the lawful downstream seam and make its bounded output visible to the appropriate consumer surfaces.

Primary repo surfaces:
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/schemas/dmp_v2.py` only if carriage is required by the admitted contract
- `src/nvda_desk/services/review_explanation.py` or equivalent review carriage surface if needed
- `tests/test_gate190_capital_deployment_authority_integration.py`

Definition of done:
- runtime integrates the new service after the already-formed opening candidate exists and before any future broker/execution consequence layer
- the decision surface is bounded to new opening capital authorisation only
- proof shows the module does not become a second posture engine or full arbiter

### Gate 191 — End-to-end proof, router closeout, and packaging
Purpose: prove the new bounded downstream slice honestly, close the pack, and package the exact green repo state.

Primary repo surfaces:
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- this pack's leaves ledger and execution log
- Gate 191 closeout receipt
- final targeted proof surfaces required by Gates 188-190

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

The bounded-scope note is also mandatory for this pack because the first slice deliberately excludes several tempting future responsibilities and must keep those exclusions explicit.

## Contradiction scan and state-integrity rules

Contradiction scan result before pack creation:
- no material contradiction exists between the repo routing surfaces; the repo is cleanly on `main` with no active pack currently routed
- repo law already separates the independent parallel-risk lane from any future arbiter, so this pack stays in the narrower `CapitalDeploymentAuthorityService` lane and does not relitigate the lane's purpose

State-integrity rules for this pack:
- `completed_leaf_ids` and `remaining_leaf_ids` must remain disjoint
- every named leaf id must exist in the leaves map
- multi-gate operator requests do not waive per-gate sequencing, validation, routing updates, or closeout
- Gate 191 closeout tests must permit the later lawful state where the Gate 186 pack remains closed evidence while this pack becomes the active or latest closed pack
