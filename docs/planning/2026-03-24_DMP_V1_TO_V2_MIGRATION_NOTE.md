# 2026-03-24 DMP V1 to V2 Migration Note

Status: design draft only; not yet implemented

## 1. Purpose

This note explains why DMP v2 exists, what changes relative to v1, and how migration should happen without breaking the current runtime or replay spine.

## 2. Why DMP v1 is not enough for the long-term target

DMP v1 is correct for Gates 8-10. It was intentionally designed to be narrow.

That narrowness now becomes the reason v2 is needed.

### 2.1 What v1 does well

- fixed top-level typed envelope
- explicit `stack_id` and `coefficient_set_id`
- deterministic packet ids
- seven-stage runtime packetisation
- review/replay lineage for the current runtime and replay surfaces

### 2.2 What v1 cannot do cleanly

- it uses a **closed** payload union;
- it uses a **closed** grammar-role enum;
- it has no first-class table contract;
- it has no first-class artefact-reference block;
- it has limited lineage depth;
- it has no declared compatibility surface for future module consumers;
- it has no reserved structured extension lane apart from versioned schema evolution.

That makes v1 a good runtime wrapper and a poor long-term module bus.

## 3. Migration goals

The migration to v2 must preserve five things:

1. current Gates 8-10 behaviour remains truthful during migration;
2. packet lineage already attached to review/replay is preserved;
3. `stack_id` and `coefficient_set_id` remain first-class;
4. future table-heavy modules can be introduced without blob payloads;
5. downstream consumers can reason from declared contracts rather than payload archaeology.

## 4. Mapping summary

| V1 surface | V2 destination | Migration note |
|---|---|---|
| `protocol_version` | `protocol_version` | version changes from `dmp.v1` to `dmp.v2` |
| `packet_identity.packet_id` | `packet_id` | flattened at top level |
| `packet_identity.emitted_at` | `producer.emitted_at` | moves under producer surface |
| `grammar_role` | `producer.grammar_role` | moves under producer surface; no longer transport-level closed enum |
| `behaviour_class` | `producer.behaviour_class` | moves under producer surface |
| `schema_identifiers.*` | `contract.*` + per-block `schema_id` | split into packet contract and block contracts |
| `stack_id` | `execution_context.stack_id` | still first-class |
| `coefficient_set_id` | `execution_context.coefficient_set_id` | still first-class |
| `dependencies` | `lineage.dependency_packet_ids` or contract metadata | split by meaning |
| `trace_references.parent_packet_id` | `lineage.parent_packet_ids` | pluralised lineage model |
| `trace_references.upstream_packet_ids` | `lineage.dependency_packet_ids` / `parent_packet_ids` | normalised by semantic intent |
| `trace_references.review_trace_id` | `lineage.review_trace_id` | preserved |
| `trace_references.replay_trace_id` | `lineage.replay_trace_id` | preserved |
| `trader_summary` | `summary.trader_summary` and/or `summary_block` | top-level summary becomes explicit |
| `payload` | `blocks[]` | biggest structural change |

## 5. Breaking changes

The following are deliberate breaking changes:

1. the single `payload` field is replaced by `blocks[]`;
2. packet identity is flattened and producer metadata is separated from payload metadata;
3. contract metadata becomes explicit instead of being partly inferred from payload model names;
4. large datasets are expected to use table or artefact-reference blocks rather than opaque inline payloads;
5. consumers that previously assumed one Pydantic payload model per packet must adapt to block-aware reading.

## 6. What should remain stable

The following should remain stable across migration:

- packet-level traceability
- deterministic packet ids
- stack/coefficient top-level visibility
- replay/review attribution intent
- binding desk-runtime order where runtime stages remain involved

## 7. Recommended migration sequence

### Phase 0 — freeze design only

- approve the v2 spec,
- approve worked examples,
- approve acceptance checklist,
- confirm no silent gate rewrite is required.

### Phase 1 — implement v2 schemas beside v1

- add `dmp_v2.py` or equivalent beside the current v1 schema surface,
- do **not** delete or mutate v1 in the same pass,
- create v2 validation tests first.

### Phase 2 — add adapters from current runtime outputs into v2 blocks

- map current stage outputs into v2 block sets,
- preserve v1 packet emission until parity is proven,
- dual-write if necessary during migration.

### Phase 3 — add table and artefact-reference support

- implement `table_block`, `timeseries_block`, and `artifact_ref_block`,
- test against options-chain-like examples,
- prove small inline tables and large artefact references both work.

### Phase 4 — migrate review/replay lineage surfaces

- move review/replay lineage readers to v2,
- prove current deterministic comparison behaviour remains stable.

### Phase 5 — retire v1 only after explicit parity sign-off

- mark v1 as superseded only after packet-shape parity and lineage parity are both evidenced,
- keep a bounded adapter path until all v1 consumers are removed or upgraded.

## 8. Migration constraints

The migration must not:

- widen into frontend transport redesign,
- widen into broker/live-vendor protocol redesign,
- silently invent new playbook semantics,
- collapse into a free-form `dict[str, Any]` design,
- force all large datasets inline,
- erase the distinction between packet ancestry and external artefact provenance.

## 9. Minimum migration evidence

V1 -> V2 migration is not believable until the following are shown:

- one compact runtime-stage packet in v2,
- one rich options-surface packet in v2,
- one review/replay lineage packet in v2,
- explicit field mapping from v1 to v2,
- test evidence that current lineage, stack identity, and coefficient identity survive the migration.

## 10. Deletion rule

DMP v1 must not be deleted in the same pass that first introduces DMP v2.

The repo has already been burned once by reality getting ahead of artefacts. We do not need a sequel.
