# 2026-04-02_GATE179_REPO_WIDE_VOCABULARY_HYGIENE

Status: complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`

## Purpose

Run a whole-repo vocabulary and workbook-path hygiene pass after the master/child merge so the repo ends in one coherent language state rather than two adjacent dialects.

Gate 179 explicitly uses the existing canonical vocabulary dictionary rather than inventing fresh wording.

## Canonical vocabulary dictionary used

Source surfaces:

- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `scripts/build_canonical_vocabulary.py`

Relevant canonical entries used in this gate:

### `independent_parallel_risk_lane`

- canonical label: **Independent Parallel Risk Lane**
- allowed aliases: `parallel risk pipeline`, `co-resident risk lane`, `parallel_risk_pipeline`
- disallowed phrases: `step_1_1`, `step_8`, `eighth_stage`

### `signal_coefficient_reference_workbook`

- canonical label: **Signal-Coefficient Reference Workbook**
- canonical contract/path: `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`
- allowed aliases: `signal workbook`, `coefficient register workbook`, `live reference workbook`
- disallowed phrases: `runtime authority workbook`, `normative workbook`

## Whole-repo scan performed

Gate 179 scanned the repo for:

- canonical workbook path usage;
- predecessor workbook path usage;
- allowed lane aliases;
- disallowed lane-numbering phrases;
- active authority surfaces versus historical evidence surfaces.

## Findings

### 1. Canonical workbook path is correct in active authority surfaces

The canonical workbook path is present in active authority surfaces including:

- `docs/01_NORMATIVE.md`
- `config/README.md`
- `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`
- `scripts/build_canonical_vocabulary.py`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md`
- `docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json`

### 2. Predecessor workbook path remains only as classified historical evidence

The predecessor workbook path
`docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx`
remains in the repo, but Gate 179 classifies those occurrences as one of:

- archive/test evidence from earlier workbook audits;
- closed-pack historical evidence from coefficient or policy packs that predate the promotion;
- explicit predecessor/archive wording in workbook-lineage and authority receipts;
- or changelog continuity.

Gate 179 does **not** treat those residual references as active authority drift.

### 3. Allowed aliases are contained

The allowed alias `parallel risk pipeline` remains confined to vocabulary/governance/test surfaces rather than spreading into active runtime naming.

The allowed alias `co-resident risk lane` remains dictionary/governance-only.

### 4. Disallowed numbered-stage phrases are present only as negative-governance surfaces

`step_1_1`, `step_8`, and `eighth_stage` remain present only where the repo is explicitly forbidding that interpretation:

- canonical vocabulary generator / generated dictionary;
- normative/governance receipts;
- bounded runtime note fields and tests that prove the lane is **not** a numbered stage.

Gate 179 found no evidence that those phrases are being used as active runtime naming doctrine.

## Hygiene rule frozen by Gate 179

From this gate onward:

1. the canonical runtime/prose term is **Independent Parallel Risk Lane**;
2. allowed aliases are tolerated only where the vocabulary dictionary explicitly permits them;
3. the canonical workbook reference is the **Signal-Coefficient Reference Workbook** at `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`;
4. predecessor workbook references are acceptable only as classified historical evidence, not as live authority;
5. any new drift must be fixed against the dictionary, not against chat memory.

## Definition of done recorded by Gate 179

Gate 179 is complete because:

- the whole-repo scan was run against the existing canonical dictionary;
- active authority surfaces use the canonical workbook path;
- alias and disallowed-phrase use is classified rather than ambient;
- and the repo ends this tranche with one explicit vocabulary and workbook-path rule set.
