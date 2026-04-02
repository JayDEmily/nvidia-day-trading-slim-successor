# 2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_SCOPE_NOTE_v1

Status: active bounded-scope note for the coefficient architecture consolidation pack on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`

## Purpose

Freeze the exact architectural intent and boundaries for the coefficient architecture consolidation pack before any later coding or promotion work starts.

This note exists so later gates do not silently widen from the approved Workstreams 1-4 brief into unrelated runtime redesign.

## Governing evidence traced before this note

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/2026-04-02_STAGE_LOCAL_HANDOFF_CORRECTIVE_SUCCESSOR_GATES_v1.md`
- `docs/planning/2026-04-02_GATE151_FIELD_LEVEL_OWNERSHIP_AND_CONSUMER_MIGRATION.md`
- `docs/planning/2026-04-02_GATE152_STAGE5_STAGE6_AUTHORITY_REPLAN.md`
- `docs/planning/2026-04-02_GATE153_OVERLAY_TERMINAL_FINAL_JOIN_AUTHORITY_REPLAN.md`
- `docs/planning/2026-04-02_GATE154_DOWNSTREAM_CONSUMER_RECONCILIATION_REPLAN.md`
- `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx`
- `config/README.md`
- `config/coefficient_authority.v1.yaml`
- `config/coefficients_registry.example.yaml`
- `src/nvda_desk/config_models.py`
- `src/nvda_desk/domain/temporal_state.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/schemas/state_policy.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/playbook_eligibility.py`
- `src/nvda_desk/services/execution_expression.py`
- `src/nvda_desk/services/posture_risk.py`
- `src/nvda_desk/services/risk_gateway.py`
- `src/nvda_desk/services/review_explanation.py`
- `src/nvda_desk/services/state_conditioned_modifier.py`

## Approved workstreams for this pack

1. **Freeze the target architecture in plain English** using repo-native vocabulary first.
2. **Collapse to one live coefficient world** without promoting workbook or salvage artefacts into runtime truth.
3. **Make owner-stage truth real** by reconciling declared owner stage, actual consumer, and activation state.
4. **Split opportunity shaping from caution shaping** without multiplying live knobs or pretending the parallel risk lane already exists.

## Refined cross-work verdicts that this pack must preserve

### Workstream 1
The architecture is already substantially present in repo doctrine and the signal workbook. The missing job is consolidation, not invention.

### Workstream 2
The repo already distinguishes governed runtime authority from salvage/reference material. The workbook adds a practical coefficient-universe ledger. The missing job is a repo-native status inventory and migration law.

### Workstream 3
Owner-stage truth is not just a label question. Each admitted mutable surface also needs activation-state truth: governed-and-active, governed-but-baseline-only, deferred, or reference-only.

### Workstream 4
The current live dynamic scheme is still mainly posture / execution caution-and-envelope shaping. Upstream opportunity improvement is more likely to come first from richer primitives, derived features, and playbook-family routing than from simply adding more coefficient surfaces.

## Workbook gold that must not be left behind

- `Runtime_Surface_Drivers` and `Coeff_Universe_Index` already behave like a migration-grade coefficient ledger.
- `Raw_Primitives_Catalog` and `Derived_Features_Catalog` impose a raw-first / derived-second architecture that later coefficient work must not violate.
- `Temporal_Step1_Framework` already freezes stage-purity rules for Step 1 and forbids leakage from downstream derived outputs.
- `Playbook_Module_Audit`, `Options_Chain_Raw_Spec`, `Volume_Baseline_Raw_Spec`, and `Derived_Features_Catalog` show that richer opportunity shaping is already emerging through input design and playbook routing, not just through dynamic coefficients.

## Explicitly out of scope for this pack

- implementing the independent parallel risk lane or final arbiter;
- portfolio-aware replacement logic;
- broad runtime refactors that are not forced by Workstreams 1-4;
- widening the admitted live coefficient surface set beyond what the repo already governs;
- treating the workbook as runtime authority;
- code changes that attempt to solve caution stacking by hand-waving rather than explicit owner / consumer law.

## Candidate descriptive phrases that are not governed vocabulary yet

The following phrases may appear in planning prose during this pack, but they are **not** governed vocabulary until a later gate proves admission is required and updates the canonical vocabulary authority:

- coefficient world status
- activation state
- opportunity shaping
- caution shaping
- upstream opportunity branch
- coefficient-status inventory

## Success condition for the pack

The pack is good only if a later coding thread can answer, from repo artefacts alone:

- what is live runtime coefficient authority;
- what is workbook/reference/provenance only;
- which stage truly owns each mutable surface;
- whether that surface is dynamically active or merely admitted;
- where opportunity shaping belongs;
- where caution shaping belongs;
- and which bigger architecture questions remain reserved for the independent risk lane thread.
