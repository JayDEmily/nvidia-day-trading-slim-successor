# 2026-04-02_GATE173_CHILD_PLANNING_REFERENCE_DATA_MERGE

## Purpose

Merge the child planning, workbook-governance, vocabulary, and reference-data surfaces into master without claiming runtime lane implementation.

## Merged surfaces in this gate

### Frozen-law surfaces

- `docs/01_NORMATIVE.md` now admits the first-class co-resident independent parallel risk lane without creating an eighth stage.
- `docs/02_OPERATING_MODEL.md` now places the lane alongside the serial runtime and forbids silent duplication of arbiter or playbook-internal logic.
- `config/README.md` now carries the governed signal-workbook lineage section.

### Workbook/reference-data surfaces

- imported canonical governed workbook: `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`
- imported workbook-governance law: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`
- predecessor workbook remains archive evidence only: `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx`

### Generator/vocabulary surfaces

- `scripts/build_canonical_vocabulary.py` now maps `raw_primitive` and `derived_feature` to the canonical workbook path
- `scripts/build_canonical_vocabulary.py` now admits `independent_parallel_risk_lane` and `signal_coefficient_reference_workbook`
- generated `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` rebuilt from the updated generator

### Child planning-pack import surfaces

- imported the closed child planning pack quartet and gate receipts
- imported child planning-guard tests as historical continuity evidence

## Workbook promotion/demotion law applied here

1. the canonical governed workbook is the file under `data/reference/signal_workbooks/`
2. the predecessor workbook under `docs/planning/` remains archive evidence only
3. active lineage surfaces must point to the canonical workbook
4. archive/test evidence may continue to mention the predecessor workbook explicitly when the historical context requires it

## Active-lineage rewires completed here

- `docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md`
- `docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json`

## What Gate 173 does not claim

- no `src/` runtime lane implementation yet
- no arbiter
- no DMP v2 schema-core redesign
- no blanket rewrite of archive-phase workbook evidence
