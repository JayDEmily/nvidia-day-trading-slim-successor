# 2026-04-02_GATE158_TARGET_ARCHITECTURE_AND_STAGE_PURITY_CONSOLIDATION

Status: complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`

## Purpose

Consolidate Workstream 1 into one repo-native planning receipt.

Gate 158 does not invent a new architecture. It gathers the repo's existing doctrine, stage grammar, workbook structure, and vocabulary discipline into one explicit statement that later coding can follow without leaning on chat memory or improvised renaming.

## Scope boundary

Gate 158 is planning-only.

It may:
- consolidate the target coefficient architecture in plain English using existing canonical vocabulary first;
- freeze the workbook's raw-versus-derived ordering and Step 1 stage-purity law as pack constraints;
- decide whether any new governed vocabulary is actually required.

It may not:
- widen the live mutable-surface set;
- promote workbook tabs into runtime authority;
- change runtime packet meaning;
- or smuggle Workstream 5 risk-lane scope into Workstream 1 architecture prose.

## Repo-native target architecture statement

The current repo can already express the coefficient architecture without admitting new governed terms.

### The architecture in repo-native layers

| Descriptive bucket used in this pack | Existing repo-native authority or term | What it means in repo reality | Primary evidence |
|---|---|---|---|
| invariant substrate | invariant surface, stable cognition grammar, raw market facts | clock facts, calendar truth, event identity, stage order, raw facts, playbook membership, review lineage do not become coefficients | `docs/01_NORMATIVE.md`; workbook `Bounds_Method`; workbook `README` |
| governed coefficient authority | baseline coefficient, state-conditioned modifier, effective coefficient | runtime may deform admitted surfaces only from a governed baseline through bounded policy law | `docs/01_NORMATIVE.md`; `config/coefficient_authority.v1.yaml`; `src/nvda_desk/config_models.py` |
| state-policy deformation plane | Stage 4.5 state-policy / modifiers | lawful upstream deformation of downstream effective coefficients, not fuzzy runtime reinvention | workbook `Repo_Stage_Summary`; `src/nvda_desk/schemas/state_policy.py`; `src/nvda_desk/services/state_conditioned_modifier.py` |
| stage-local consumption surfaces | playbook eligibility, execution expression, posture/risk permission | downstream stages consume governed or effective surfaces without collapsing stage ownership into one blob | Gate 151; Gate 152; `src/nvda_desk/services/playbook_eligibility.py`; `src/nvda_desk/services/execution_expression.py`; `src/nvda_desk/services/posture_risk.py` |
| review-visible lineage | review lineage, review packet, bounded trace | review reconstructs and exposes why a surface moved; review does not itself create authority | `docs/01_NORMATIVE.md`; `src/nvda_desk/services/review_explanation.py` |

### Plain-English architecture law

1. **Invariant truths stay fixed.** Clock facts, event identity, raw market facts, stage order, and review lineage are not coefficients. The workbook already states this in `Bounds_Method`, and the normative doctrine already states it in the coefficient ontology.
2. **Derived state is not the same thing as a coefficient.** The workbook separates raw primitives from derived features, and Stage 1 is forbidden from consuming Step 2/3 derived outputs. Later coefficient work must preserve that ordering.
3. **Runtime authority begins with admitted surfaces only.** The governed runtime authority remains the admitted baseline-plus-bounds subset, not the full workbook or salvage universe.
4. **State-policy deformation is a lawful middle layer.** The repo already names this as the state-policy / modifier seam. It is upstream of expression but downstream of invariant truth.
5. **Stage-local consumers remain distinct.** Stage 5 admissibility, Stage 6 execution expression, posture permission, and later review each have different jobs and must not be collapsed for convenience.
6. **Review is explanatory, not authoritative.** Review-visible lineage exists to reconstruct the effective path, not to create new runtime truth.

## Workbook-derived raw-versus-derived ordering law

Gate 158 freezes the workbook's ordering discipline as a pack constraint.

### Observed workbook law

- `README` already says: raw first, derived second.
- `Raw_Primitives_Catalog` is the workbook's primitive inventory.
- `Derived_Features_Catalog` is explicitly downstream of primitive capture.
- `Options_Chain_Raw_Spec` says preserve dense raw chain rows first and derive state later.
- `Volume_Baseline_Raw_Spec` says same-bucket historical baselines are required so participation logic is not a toy proxy.

### Binding pack constraint

Later gates in this pack must prefer the following order whenever a design choice exists:
1. capture or preserve the right raw fact;
2. define the lawful derived feature;
3. route that feature into playbook or posture logic;
4. only then decide whether a coefficient surface is needed.

The forbidden inversion is:
- using a dynamic coefficient to stand in for missing raw data;
- widening coefficient corridors because a raw-data design problem remains unresolved;
- or calling a derived state feature a coefficient merely because it affects trading behaviour.

## Step 1 stage-purity law frozen by Gate 158

Gate 158 also freezes the workbook's Step 1 stage-purity rule as pack law.

### Observed workbook law

`Temporal_Step1_Framework` explicitly states that Step 1 may reuse primitives later, but may not consume downstream derived outputs such as regime scores, options-pressure scores, Asia/breadth outputs, posture/risk vetoes, or playbook eligibility outputs.

### Binding pack constraint

For the remainder of this pack:
- Stage 1 temporal context may consume clock, session, event-proximity, and primitive intraday observables.
- Stage 1 may not consume later-stage synthetic verdicts and then masquerade that dependency as "context".
- Any later gate that proposes a new coefficient or threshold touching Step 1 must first prove the input obeys this stage-purity rule.

## Vocabulary sufficiency verdict

No new governed vocabulary is admitted in Gate 158.

### Vocabulary sufficiency matrix

| Descriptive need seen in planning | Existing canonical or repo-native term already good enough | Gate 158 verdict |
|---|---|---|
| runtime baseline vs live effective value | `baseline_coefficient`, `state_conditioned_modifier`, `effective_coefficient` | sufficient |
| downstream execution layer | `execution_expression` | sufficient |
| Stage 5 versus Stage 6 split | existing stage grammar plus later Gate 152 case law | sufficient |
| state-policy seam | existing state-policy / modifier language | sufficient |
| activation state | no canonical term required yet; descriptive phrase only until Gate 160 freezes the ledger | no admission |
| coefficient world status | descriptive phrase only until Gate 159 defines the inventory law | no admission |
| opportunity shaping / caution shaping | descriptive phrases only until Gate 161 freezes the boundary law | no admission |

Gate 158 therefore does **not** modify:
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `scripts/build_canonical_vocabulary.py`

## Constraints handed forward to later gates

1. Later gates must use existing canonical vocabulary first.
2. Descriptive bucket names in this receipt do not become governed vocabulary by repetition.
3. No later gate may promote workbook content into runtime truth by citation alone.
4. Gate 159 must define one live coefficient world without disturbing the raw-versus-derived order frozen here.
5. Gate 160 must treat `activation state` as a ledger attribute, not as retroactive vocabulary inflation.
6. Gate 161 must pursue richer upstream opportunity through better primitives, derived features, and routing before multiplying live knobs.

## Definition of done recorded by Gate 158

Gate 158 is complete only because:
- the repo now has one explicit target-architecture receipt for Workstream 1;
- the workbook's raw-first and Step 1 stage-purity laws are frozen as pack constraints;
- and the pack has an explicit no-new-vocabulary verdict rather than silent naming drift.
