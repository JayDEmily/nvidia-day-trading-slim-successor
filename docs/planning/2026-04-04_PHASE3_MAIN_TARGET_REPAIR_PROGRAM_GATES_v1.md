# 2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_GATES_v1

Status: active Phase 3 main-target repair planning pack on `work/gate-192-phase3-main-target-repair-pack-20260404`
Purpose: convert the executed Phase 2B defect harvest into one disciplined, evidence-backed repair programme for the main target repo without collapsing unrelated bug families into one vague repair blob.
Authority: subordinate to `docs/01_NORMATIVE.md`, `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`, and repo-root `PLANS.md`.
Vocabulary authority for this pack: `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
Packet/data contract authority for this pack: `docs/03_DOMAIN_MODEL.md`

## Why this tranche exists

The repo now has a complete report-first harvest of the main-target defect surface. That harvest is already normalised into nine defect families and seven Phase 3 repair tranches. The missing work is no longer discovery. The missing work is a disciplined repair programme that preserves repo law, guardrails, workflow order, and truthful closeout.

This pack exists to:

1. bridge the executed Phase 2B defect harvest into repo-native gate and leaf execution law;
2. preserve the distinction between runtime-semantic repair, governance/control repair, vocabulary repair, and static-quality repair;
3. keep every repair slice bounded enough that green proof and closeout can stay honest; and
4. package the repair programme gate by gate rather than letting a coding thread wander across the whole repo.

## Intent and workflow anchor

This pack sits after the external Phase 2B audit/reconciliation programme and before any new expansion of modules, stages, or tuning logic. It is a corrective and stabilisation tranche, not an architecture-expansion tranche.

The pack must:

1. route the repo into an active repair programme beginning at Gate 192;
2. carry forward the executed defect families without relabelling warnings or blockers as hard runtime failures;
3. repair vocabulary truth surfaces before runtime-semantic drift so the runtime tranche does not chase text drift;
4. keep control-surface truth separate from runtime-semantics truth;
5. keep static-quality work separate from behaviour repairs unless a later proof slice requires coupling; and
6. close with truthful proofs, router updates, and a fresh full-history zip from the exact green repo state.

## In scope

- active Phase 3 planning-pack bootstrap and truthful routing
- external-evidence baseline that freezes the executed Phase 2B defect harvest as the repair input set
- vocabulary generator versus committed artifact reconciliation
- repo-wide vocabulary hygiene leakage reconciliation
- control-surface router and gate-map reconciliation
- bounded runtime-semantic reconciliation for options-flow harness expectations and higher-order context stress law
- concentrated financial-calendar typing seam repair
- typed helper pressure reduction for strict test contexts
- late static hygiene and Alembic warning cleanup required to close the programme honestly

## Out of scope

- new module or stage expansion
- coefficient redesign or tuning changes
- side-repo B/C packaging blockers from the earlier handoff unless they are later proven to block a main-target repair gate
- UI or review-surface redesign beyond what is strictly required to keep the repair slices truthful
- re-running Phase 2B as a rediscovery exercise instead of using it as a repair input
- any effort to mix runtime-semantic repair with broad static cleanup in the same gate unless a later contradiction report proves they are inseparable

## Supersession and active authority

- This document becomes the active gate authority for Gates 192-199.
- It supersedes the repo-root `PLANS.md` statement that no active pack is currently routed.
- It supersedes the canonical gate-map current-active-gate marker of `none`.
- The latest closed capital-deployment authority pack remains evidence input only; it is not the structural template for this tranche.
- The external Phase 2B audit reports are evidence input only; they are not themselves the repo-native execution router.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- `PLANS.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/TESTING_AND_PROMOTION.md`
- `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_EVIDENCE_BASELINE_v1.md`
- `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SCOPE_NOTE_v1.md`
- the repo-native workflow surfaces implicated by the seven repair tranches, including vocabulary generation, planning/router control surfaces, runtime harnesses, higher-order context law, financial-calendar typing surfaces, helper typing surfaces, and static-quality surfaces

## Workflow placement

This tranche is downstream corrective work over an already-built deterministic stack. It is neither upstream import authority nor a new workflow-stage admission pack. It is a repair programme over existing authorities.

The chosen gate count preserves granularity because it separates:
- pack bootstrap and routing;
- vocabulary generator truth;
- vocabulary hygiene leakage;
- governance/control-surface truth;
- runtime-semantic drift;
- concentrated typing-seam repair;
- helper typing pressure; and
- late static hygiene plus warning cleanup.

This is more truthful than one giant repair gate and more practical than making every failing test its own gate.

## Retain / retire-from-authority / amend / add matrix

### Retain
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/planning/tranche_briefing_template_pack/*`
- `docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_*`
- the current normative stack and guardrail surfaces
- the Phase 2B defect families as frozen evidence inputs only

### Retire from active authority
- repo-root `PLANS.md` statement that no active pack is currently routed
- canonical gate-map current-active-gate marker of `none`

### Amend
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- this pack's leaves ledger and execution log as execution proceeds
- the vocabulary authority when vocabulary tranches lawfully close
- the specific runtime/control/static surfaces named gate by gate below

### Add
- active Phase 3 gates/leaves/execution-log/checklist/scope/evidence-baseline surfaces
- Gate 192 pack-bootstrap receipt
- later gate receipts for Gates 193-199
- any contradiction report required if execution uncovers a control-surface disagreement this pack did not start with

## Vocabulary discipline

- Existing vocabulary authority must be read before writing any new planning term, file name, class name, field name, or gate title.
- No new repair label may be invented when an existing canonical term already covers the surface.
- If a new term is absolutely required during execution, it must be proposed narrowly and admitted lawfully before merge.

## Packet / contract discipline

- `docs/03_DOMAIN_MODEL.md` is mandatory reading for any leaf that changes envelope shape, carriage, lineage, or compatibility.
- Runtime-semantic repair must not silently reshape packet contracts while claiming to be only a behaviour fix.
- Static-quality tranches must not smuggle contract changes through typing cleanup.

## Contradiction scan and state-integrity rules

Contradiction scan result before pack creation:
- no material contradiction exists between the repo routing surfaces inside the target repo: the repo was cleanly closed through Gate 191 with no active pack routed;
- the external Phase 2B audit identified defect families and tranche candidates but did not claim to become the repo-native execution router;
- H v2 is compatible with repo-native planning law because it shapes repair-entry truth without starting repair work.

State-integrity rules for this pack:
- `completed_leaf_ids` and `remaining_leaf_ids` must remain disjoint;
- every named leaf id must exist in the leaves ledger;
- `active_gate = none` is lawful only when `remaining_leaf_ids` and `pending_gate_ids` are empty;
- multi-gate operator requests do not waive per-gate sequencing, validation, routing updates, or closeout;
- Gate 199 closeout proofs must permit the later lawful state where the capital-deployment pack remains closed evidence and this Phase 3 pack becomes the latest closed corrective pack.

## Document-touch checklist requirement

Execution must maintain the active planning quartet together:
1. repo-root `PLANS.md`
2. canonical gate map
3. active leaves ledger
4. active execution log

This pack also requires:
- a bounded-scope note because runtime repairs must remain separate from static cleanup and side-repo blockers;
- an evidence-baseline note because the repair programme begins from an external but already-executed defect harvest.

## Testing and promotion discipline

- Repo-local environment required: `.venv`
- Minimum validation slice per repair gate:
  - targeted pytest covering the repaired family
  - any leaf-specific integrity or hygiene tests named in the leaves ledger
- Wider validation required when blast radius reaches runtime semantics, router/control truth, or gate closeout.
- A gate is not complete until:
  - tests ran green in the exact repo-local environment;
  - `PLANS.md`, the gate map, the active leaves ledger, and the active execution log all moved together;
  - a new full-history zip was created from the exact green repo state when the gate closes.

## Gate structure

### Gate 192 — Phase 3 repair pack bootstrap and evidence bridge
Purpose: install the active Phase 3 planning quartet, freeze the evidence baseline and bounded scope truthfully, and route the repo to Gate 193 without changing runtime behaviour yet.

Primary outputs:
- active Phase 3 planning quartet plus scope/evidence notes
- Gate 192 bootstrap receipt
- planning-pack proof test

### Gate 193 — Vocabulary generator and artifact truth reconciliation
Purpose: decide and repair the lawful truth between the vocabulary generator output and the committed vocabulary artifact, then re-anchor dependent vocabulary-governance expectations.

Primary repo surfaces:
- vocabulary generator surfaces
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- dependent vocabulary-governance tests and any tightly coupled fixtures
- Gate 193 receipt and targeted recheck proof

Definition of done:
- generator truth and committed artifact no longer disagree
- dependent vocabulary-governance failures for this family recheck green
- no unrelated runtime-semantic or static-quality work is mixed into the gate

### Gate 194 — Repo-wide vocabulary hygiene leakage reconciliation
Purpose: remove or explicitly admit residual banned/stale vocabulary leakage after Gate 193 settles the generator/artifact truth seam.

Primary repo surfaces:
- hygiene tests and allowlist/governance text
- integration tests or docs carrying the residual leaked phrase surfaces
- Gate 194 receipt and targeted recheck proof

Definition of done:
- residual vocabulary leakage for the admitted family is resolved honestly
- allowlists and tests agree on the same truth
- no generator-semantics work is reopened unless Gate 193 evidence proves coupling

### Gate 195 — Control-surface router and gate-map reconciliation
Purpose: repair current-state truth drift across `PLANS.md`, the canonical gate map, and associated closeout/control text.

Primary repo surfaces:
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- any affected closeout or control text named by the executed failures
- Gate 195 receipt and targeted/widened planning integrity proof

Definition of done:
- routing and gate-map surfaces tell one coherent current-state truth
- planning/control tests for the affected surfaces are green
- no runtime-semantic fixes are bundled into the gate

### Gate 196 — Runtime semantic drift reconciliation
Purpose: reconcile the admitted runtime semantics for options-flow harness expectations and stressed higher-order context compression-state law.

Primary repo surfaces:
- options-flow clustering semantics and harness expectation surfaces
- higher-order context detector surfaces and Gate 31 stress-behaviour contract
- any directly coupled runtime schema or fixture surfaces required to keep the repair lawful
- Gate 196 receipt and targeted runtime plus widened downstream proof

Definition of done:
- the options-flow harness family and higher-order context family converge on one admitted truth
- targeted runtime proofs and any required wider proofs are green
- static cleanup, vocabulary hygiene, and router repairs remain out of scope unless a contradiction report proves coupling

### Gate 197 — Financial-calendar typing seam reconciliation
Purpose: clear the concentrated typing seam around the financial-calendar schema family without smuggling wider semantic change.

Primary repo surfaces:
- `src/nvda_desk/schemas/financial_calendar.py`
- adjacent financial-calendar services and tests
- Gate 197 receipt and targeted mypy/pytest proof

Definition of done:
- the concentrated financial-calendar typing seam is repaired as a coherent slice
- related mypy errors for this seam clear or narrow honestly
- runtime semantic change outside the typing seam does not enter the gate

### Gate 198 — Typed helper pressure reduction
Purpose: reduce strict-typing failures caused by untyped helpers in tests without rewriting runtime-domain behaviour.

Primary repo surfaces:
- helper functions used across strict test contexts
- typed-safe helper return shapes and related fixtures
- Gate 198 receipt and targeted mypy proof

Definition of done:
- helper typing debt is reduced truthfully
- strict test contexts stop failing for the bounded helper family repaired in this gate
- runtime-domain semantics remain untouched

### Gate 199 — Static hygiene, Alembic warning cleanup, and Phase 3 closeout
Purpose: close the remaining static-quality tranche, clear or consciously retain the warning-only Alembic constraint, and package the exact green repo state.

Primary repo surfaces:
- `ruff` findings still retained after earlier gates
- Alembic configuration surface for the `path_separator` warning
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- this pack's leaves ledger and execution log
- Gate 199 closeout receipt

Definition of done:
- remaining static debt and warning-only constraints are handled honestly
- targeted and widened closeout proofs are green
- router/control surfaces agree on the active/closed state
- a fresh full-history zip is produced from the exact green repo state
