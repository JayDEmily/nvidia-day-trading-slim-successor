# 2026-04-02_GATE159_COEFFICIENT_WORLD_STATUS_AND_INVENTORY_LAW

Status: complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`

## Purpose

Collapse Workstream 2 into one repo-native coefficient-world statement.

Gate 159 does not claim that the repo had no split already. The split already existed in doctrine, config layout, runtime loaders, and workbook intent. Gate 159 makes that split explicit enough that future-you can answer what is live, what is reference, what is provenance, and what is deferred without spelunking three different document families.

## Scope boundary

Gate 159 is planning-only.

It may:
- classify the repo's coefficient sources into live, reference, provenance, and deferred classes;
- define the coefficient-status inventory that later coding must populate or maintain;
- freeze migration law for workbook and salvage surfaces.

It may not:
- promote workbook or salvage sheets into runtime authority;
- widen the admitted live surface set;
- or collapse owner-stage truth and activation-state truth into this gate before Gate 160.

No new governed vocabulary is admitted in Gate 159.

## One live coefficient world, stated plainly

The repo's **one live coefficient world** is not a spreadsheet and not the salvage registry.

It is the governed authority chain consisting of:
1. `config/README.md` as the routing statement;
2. `config/coefficient_authority.v1.yaml` as the admitted runtime authority for the currently governed subset;
3. `src/nvda_desk/config_models.py` as the typed authority contract;
4. runtime readers such as `src/nvda_desk/services/state_conditioned_modifier.py` and `src/nvda_desk/domain/temporal_state.py` for the admitted subset.

Everything else may still matter, but it matters as reference, provenance, or deferred candidate material unless and until a later gate explicitly promotes it.

## Coefficient-world classification law

### The four status classes frozen by Gate 159

| Status class | Meaning | May drive runtime today? | Typical sources | Example repo surfaces |
|---|---|---|---|---|
| `live_runtime_authority` | admitted authority surface with explicit runtime status | yes | governed YAML + typed models + runtime readers | `config/coefficient_authority.v1.yaml`; admitted temporal thresholds read by `temporal_state.py`; admitted mutable surfaces read by `state_conditioned_modifier.py` |
| `reference_registry` | non-authoritative registry or example config that remains useful for research, naming, or migration context | no | example/salvage config, example registries | `config/coefficients_registry.example.yaml` |
| `provenance_workbook` | workbook evidence, handoff structure, starter bands, or migration ledger material | no | workbook sheets | `Runtime_Surface_Drivers`, `Coeff_Universe_Index`, `Temporal_Bounds_Draft`, `Temporal_Step1_Framework`, `Bounds_Method`, `Signal_Coeff_Handoff` |
| `deferred_candidate` | identified candidate surface or threshold that has not yet been admitted into governed runtime authority | no | workbook candidate universe, salvage/config candidates, future module coefficients | legacy example-config rows not admitted into `coefficient_authority.v1.yaml`; workbook temporal draft bands beyond the already governed subset |

### Classification rules

1. A surface is **live** only if the governed runtime chain admits it.
2. A surface is **not live** merely because it appears in the workbook with bounds.
3. A surface is **not live** merely because it appears in `coefficients_registry.example.yaml`.
4. Workbook and salvage sources may inform migration and prioritisation, but not runtime truth by default.
5. Gate 160 will add owner-stage and activation-state truth on top of this classification, not instead of it.

## Source-by-source verdict table

| Source or surface | Gate 159 class | Why |
|---|---|---|
| `config/coefficient_authority.v1.yaml` | `live_runtime_authority` | repo already routes it as governed runtime authority for the admitted subset |
| `src/nvda_desk/config_models.py` | part of the `live_runtime_authority` chain | typed validator and contract for governed authority |
| `src/nvda_desk/services/state_conditioned_modifier.py` authority load path | part of the `live_runtime_authority` chain | consumes admitted runtime mutable surfaces from governed authority |
| `src/nvda_desk/domain/temporal_state.py` authority load path | part of the `live_runtime_authority` chain | consumes admitted bounded temporal subset from governed authority |
| `config/coefficients_registry.example.yaml` | `reference_registry` | broader salvage/reference universe, explicitly not interchangeable with governed runtime authority |
| workbook `Runtime_Surface_Drivers` | `provenance_workbook` | best current migration summary of admitted runtime surfaces, bounds, drivers, and current source of truth, but not runtime authority |
| workbook `Coeff_Universe_Index` | `provenance_workbook` plus `deferred_candidate` rows | strongest candidate-universe ledger, but still workbook evidence until promoted |
| workbook `Temporal_Bounds_Draft` | `provenance_workbook` | starter research bands, not final truth |
| workbook `Temporal_Step1_Framework` | `provenance_workbook` | baseline/source temporal surface with stage-purity context, not runtime authority on its own |
| workbook `Bounds_Method` | `provenance_workbook` | method sheet that informs research order and transform families |
| workbook `Signal_Coeff_Handoff` | `provenance_workbook` | navigation and implementation-handoff sheet, not the authority chain itself |

## Coefficient-status inventory law

Gate 159 freezes one repo-native inventory schema that later coding or documentation may materialise as YAML, JSON, or another explicit artefact.

### Required inventory fields

Every coefficient or threshold tracked by the pack must be representable with at least these fields:

- `inventory_id`
- `surface_or_threshold_id`
- `status_class` with one of the four classes frozen above
- `authority_source`
- `provenance_sources`
- `declared_owner_stage` or `owner_layer`
- `transform_family` if applicable
- `current_value_or_baseline`
- `min_floor`
- `max_cap`
- `notes`
- `promotion_rule` or `defer_rule`
- `activation_state` placeholder, pending Gate 160

### Why Gate 159 freezes this schema now

The workbook already does much of this informally in `Runtime_Surface_Drivers` and `Coeff_Universe_Index`. Gate 159 freezes the minimum repo-native law so later coding has one target inventory shape instead of inventing another ad hoc sheet or note.

## Migration law for workbook and salvage surfaces

Workbook and salvage material may influence the repo only through explicit promotion.

### Allowed promotion sequence

1. identify the candidate in workbook or salvage material;
2. classify it under the Gate 159 status law;
3. check owner stage and downstream consequence;
4. decide whether it remains deferred, becomes reference-only, or is promoted into governed authority;
5. if promoted, update the governed authority chain and the relevant runtime/tests explicitly.

### Forbidden shortcuts

- do not read workbook tabs directly from runtime and call that promotion;
- do not copy a workbook band into runtime just because it looks plausible;
- do not treat the salvage registry as a shadow authority file;
- do not confuse "present in ontology" with "live in runtime";
- do not skip the owner-stage and activation-state pass that Gate 160 still owes.

## What Gate 159 hands forward

1. Gate 160 inherits a clean coefficient-world classification and can focus on owner-stage plus activation-state truth.
2. Gate 161 inherits the rule that richer upstream opportunity should come from inputs, features, and routing before new coefficient promotion.
3. Gate 162 inherits a defined inventory target rather than a fuzzy request for "one source of truth".

## Definition of done recorded by Gate 159

Gate 159 is complete only because:
- the repo now has one explicit statement of what counts as the live coefficient world;
- the workbook and salvage surfaces are preserved as useful but non-authoritative classes;
- and a minimum coefficient-status inventory law now exists for later execution work.
