Status: proposed on `testing`; not active on `main` until Gate 94 promotes the pack into the repo control surfaces

# 2026-03-30_TESTING_MODULE_GATES_v1.md

## Purpose

Define the bounded testing-module tranche that follows Gate 93. This pack converts the repo's testing doctrine into executable sequential gates, starting with planning/control-surface promotion and Phase 0 closeout, then moving through the ordered testing phases frozen in `docs/TESTING_AND_PROMOTION.md`.

## Why this pack exists

The repo now has substantial contract and gate-specific coverage, but the testing surface is still shaped by the sequential build history. The next bounded tranche must explicitly target the real bug surface of a deterministic cognition runtime: stage-boundary drift, lawful-output violations, threshold/precedence defects, and transition bugs that only appear across adjacent snapshots.

## Scope

In scope:
- promotion of the testing doctrine and Phase 0 workbook audit into the active planning stack;
- closeout of the Phase 0 workbook-viability verdict on `main`;
- one canonical prepared-runtime full-chain harness;
- invariant/lawful-output tests;
- targeted threshold-edge tests;
- adjacent-snapshot and event-window transition tests;
- bounded scenario-matrix expansion using checked-in deterministic fixtures.

Out of scope:
- inventing missing raw signals;
- changing normative trading law or widening mutable runtime surfaces;
- introducing a large unconstrained scenario zoo;
- replay-wide model retuning or coefficient search;
- pretending the workbook is a lawful raw runtime bundle when Phase 0 has already proved otherwise.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `AGENTS.md`
- `PLANS.md`
- `docs/TESTING_AND_PROMOTION.md`
- `docs/planning/2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.md`
- `docs/planning/2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.json`
- `fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json`
- `fixtures/replay/gate_f_replay_regression_fixture_pack.json`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/real_data_loader.py`
- `src/nvda_desk/services/chain_to_cognition.py`
- `src/nvda_desk/services/temporal_context.py`
- `src/nvda_desk/services/state_conditioned_modifier.py`
- `src/nvda_desk/services/playbook_eligibility.py`
- `src/nvda_desk/services/review_explanation.py`
- `src/nvda_desk/services/replay_compare.py`

## Testing-module authority notes

- `docs/TESTING_AND_PROMOTION.md` is the testing doctrine authority. This gate pack operationalises it; it does not override it.
- Phase 0 already concluded that the workbook is a doctrine and signal-catalog artefact, not a lawful raw runtime bundle.
- Later gates may use the checked-in prepared-runtime fixture pack as the canonical deterministic ingress surface where the doctrine explicitly allows prepared-runtime inputs.
- No gate may claim true raw-ingress coverage until the missing raw truth identified in Phase 0 is supplied.

## Workflow placement

This tranche is post-Gate-93 testing hardening.

It is not a new trading feature pack.
It is the first repo-native testing pack whose sole purpose is to tighten evidence against hidden deterministic-runtime bugs.

## Gate sequencing summary

### Gate 94 sequencing summary
1. Promote the testing doctrine and testing-module planning pack into the active planning control surfaces.
2. Add anti-drift tests proving Gate 94 closeout and Gate 95 activation.

### Gate 95 sequencing summary
1. Promote the Phase 0 workbook-audit artefacts onto `main`.
2. Freeze the fail/pass verdict honestly in planning and test surfaces.

### Gate 96 sequencing summary
1. Build one canonical prepared-runtime harness.
2. Run one full cognition pass from that canonical harness.
3. Freeze deterministic output and lineage expectations.
4. Do not broaden to many scenarios before one lawful single-run harness is stable.

### Gate 97 sequencing summary
1. Add lawful-output invariants across canonical scenarios.
2. Add lineage-order and veto-surface invariants.

### Gate 98 sequencing summary
1. Add targeted threshold-edge tests.
2. Add bounded precedence/edge monotonicity checks.

### Gate 99 sequencing summary
1. Add adjacent-snapshot transition tests for the canonical prepared-runtime sequence.
2. Add ordered event-window transition tests.

### Gate 100 sequencing summary
1. Expand to a bounded scenario matrix using checked-in deterministic fixtures.
2. Close the testing-module pack honestly across the planning control surfaces and package the repo.

## Gates

### Gate 94: Testing-module pack promotion and planning-control activation

**Objective**
- Promote the testing doctrine, the testing-module planning pair, and the active-control pointers so the repo has one explicit post-Gate-93 testing authority.

**Definition of done**
- `docs/TESTING_AND_PROMOTION.md` and the new testing-module planning pair are present on `main`;
- `PLANS.md`, the gate map, the active leaf ledger, and the active execution log all point to the testing-module pack together;
- anti-drift tests prove Gate 94 is complete and Gate 95 is next.

### Gate 95: Phase 0 workbook-viability closeout on `main`

**Objective**
- Promote the Phase 0 workbook audit and freeze its verdict honestly on `main`.

**Definition of done**
- the Phase 0 audit artefacts exist on `main`;
- tests prove the workbook verdict remains `fail_missing_raw_truth` until real raw capture is supplied;
- the testing-module control surfaces point from Gate 94 closeout to Gate 95 closeout and Gate 96 next.

### Gate 96: Canonical prepared-runtime full-chain harness

**Objective**
- Build one explicit canonical prepared-runtime harness that runs a full cognition pass from a checked-in prepared snapshot plus explicit companion regime/inventory truth.

**Definition of done**
- one canonical harness helper exists;
- one canonical snapshot runs end-to-end through `DeskCognitionRuntime.run(...)` deterministically;
- the frozen expected outputs and packet lineage are asserted in tests.

### Gate 97: Lawful-output and invariant testing

**Objective**
- Add invariant tests that prove runtime law, not just one hand-picked example.

**Definition of done**
- blocked or vetoed states cannot silently retain fresh deployable capital or active execution paths;
- packet/stage lineage order is asserted;
- invariant tests run across at least the stressed fixture, the supportive fixture, and the canonical prepared-runtime harness.

### Gate 98: Targeted threshold-edge and precedence tests

**Objective**
- Attack threshold edges where example-driven tests are thin, without turning this tranche into repo-wide property-testing theatre.

**Definition of done**
- bounded parametrized tests cover at least event-window edge transitions and gamma-pressure or comparable modifier-sensitive thresholds;
- the tests assert monotonic or non-illegal transitions rather than only single exact values.

### Gate 99: Transition and adjacent-snapshot sequence tests

**Objective**
- Catch deterministic bugs that only appear when the runtime moves from one state to the next.

**Definition of done**
- the canonical prepared-runtime sequence is tested in order across adjacent snapshots;
- ordered event-window transitions are tested for lawful allow -> derisk -> block progression where applicable;
- the tests assert non-illegal sideways behaviour.

### Gate 100: Controlled scenario-matrix expansion and honest closeout

**Objective**
- Expand beyond one canonical harness to a bounded deterministic scenario matrix, then close the testing-module pack honestly.

**Definition of done**
- the initial expansion set stays bounded and deterministic;
- materially different scenario states are frozen by tests rather than prose;
- `PLANS.md`, the gate map, the active leaf ledger, and the active execution log all point to testing-pack closeout together;
- a full-history zip exists from the exact green repo state.


## Gate 95 closeout note

Gate 95 is complete on `main` once the Phase 0 workbook-audit artefacts are present on `main`, the audit script reproduces the checked-in JSON verdict, the testing-module control surfaces move together to Gate 96 next, and the repo continues to record the workbook verdict as `fail_missing_raw_truth` until new raw capture is supplied.
