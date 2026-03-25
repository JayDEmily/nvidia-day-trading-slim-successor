# 2026-03-24 DMP V2 Normative Specification

Status: design draft only; not yet implemented  
Authority: subordinate to `docs/01_NORMATIVE.md`; non-governing design artefact for the next DMP redesign pass  
Design target: replace DMP v1 as the long-term canonical internal message contract after explicit promotion and implementation

## 1. Purpose

Desk Module Protocol (DMP) v2 is the **canonical internal message contract** for module-to-module handoff.

DMP v2 exists to solve a different problem from DMP v1.

- DMP v1 wraps a bounded set of current runtime and replay payloads in a narrow typed envelope.
- DMP v2 must support a broader future module universe in which modules may emit compact decision objects, scalar metrics, time-series outputs, rich tabular datasets, replay artefacts, review artefacts, and external artefact references without collapsing into untyped JSON blobs.

The design target is therefore:

> a fixed, versioned envelope carrying one or more typed payload blocks, with explicit lineage, contract metadata, execution context, and first-class support for large artefact references.

## 2. Design drivers

This specification is driven by three realities already present in the repo and official reference guidance.

### 2.1 Future module shapes are heterogeneous

The preserved module universe already includes modules whose output shapes vary materially:

- `options_data_capture` -> `options_chain`
- `options_metadata_capture` -> `options_metadata`
- `gamma_pressure` consumes `options_chain`, `options_metadata`, `spot_prices`
- `iv_vs_rv_analysis` consumes `options_chain`, `rv_metrics`
- `ladder_constructor` consumes `options_metadata`, `spot_prices`
- `module_trace_attribution` emits attribution logs
- `variant_trace_logger` emits variant-level trace surfaces

These are recorded in `docs/planning/2026-03-23_GATE_B_SOURCE_REGISTRY.jsonl`.

### 2.2 DMP v1 is intentionally narrower

DMP v1 currently uses:

- a fixed top-level envelope,
- a closed grammar-role enum,
- a closed payload union,
- sparse lineage metadata,
- no first-class table contract,
- no first-class artefact-reference block,
- no declared extension lane.

That is acceptable for Gates 8-10 and insufficient for the later canonical-universe programme.

### 2.3 Official guidance favours strict contracts, stable metadata, and externalisation of large payloads

This design aligns with:

- OpenAI Structured Outputs and tool/function interfaces, which use explicit JSON-schema-governed structures and call correlation rather than loose payloads.
- AWS EventBridge event design, which uses a stable top-level event envelope with explicit metadata such as version, id, source, type, and detail.
- AWS large-payload guidance, which uses a claim-check pattern so large payloads can be stored externally and referenced from the message.

DMP v2 uses those ideas as design precedent, not as a claim that this repo is literally implementing EventBridge or the OpenAI Responses API.

## 3. Core principles

DMP v2 is binding to the following principles.

1. **Fixed outside, variable inside.**
   The envelope is stable and versioned. The data blocks are typed and declared.
2. **Schema-governed, not blob-governed.**
   Every block must name its contract/schema.
3. **Lineage is first-class.**
   Provenance, ancestry, correlation, and artefact references must be explicit.
4. **Desk execution context stays top-level.**
   `stack_id`, `coefficient_set_id`, and later live-runtime context remain first-class.
5. **Large datasets are not forced inline.**
   The protocol must support externalised artefacts via typed references.
6. **Future extension is explicit.**
   Reserved extension surfaces exist, but uncontrolled arbitrary keys do not.
7. **No second config family.**
   DMP v2 must not accidentally create a separate ad hoc registry or configuration universe.

## 4. DMP v2 packet model

A DMP v2 packet is a single canonical message with the following top-level surfaces.

```json
{
  "protocol_version": "dmp.v2",
  "packet_id": "string",
  "trace_id": "string",
  "run_id": "string",
  "scenario_id": "string|null",
  "producer": {},
  "contract": {},
  "lineage": {},
  "execution_context": {},
  "blocks": [],
  "summary": {},
  "validation": {},
  "extensions": {}
}
```

### 4.1 Required top-level fields

| Field | Required | Meaning |
|---|---:|---|
| `protocol_version` | yes | Literal protocol identifier, initially `dmp.v2` |
| `packet_id` | yes | Globally unique packet identity within the repo runtime |
| `trace_id` | yes | Correlation id spanning a logical runtime/replay/review flow |
| `run_id` | yes | Identity of the concrete run, snapshot, replay, or evaluation instance |
| `scenario_id` | no | Optional scenario/snapshot label |
| `producer` | yes | Who emitted the packet |
| `contract` | yes | What contract the packet and blocks conform to |
| `lineage` | yes | What this packet depends on and descends from |
| `execution_context` | yes | Desk/runtime context that remains first-class |
| `blocks` | yes | One or more typed data blocks |
| `summary` | yes | Human-legible summary surface |
| `validation` | yes | Contract/schema validation result surface |
| `extensions` | yes | Reserved structured extension map |

## 5. Producer surface

The producer surface identifies the emitting module or stage.

```json
{
  "module_id": "string",
  "module_version": "string",
  "module_instance_id": "string",
  "grammar_role": "string",
  "stage_name": "string|null",
  "behaviour_class": "string",
  "emitted_at": "RFC3339 timestamp"
}
```

### 5.1 Producer invariants

- `module_id` must be stable across runs for the same logical producer.
- `module_version` must change when the emitting contract or logic changes materially.
- `module_instance_id` distinguishes concrete instances/configurations of a producer.
- `grammar_role` remains the desk-cognition role, but v2 does not require a closed enum baked into the transport layer.
- `stage_name` is optional so non-runtime-stage modules are still supported.
- `behaviour_class` names the general family, for example `stage_output`, `module_output`, `review_packet`, `replay_artefact`, `registry_artifact`.

## 6. Contract surface

The contract surface tells consumers what they may assume.

```json
{
  "packet_schema_id": "string",
  "payload_contract_id": "string",
  "compatibility_version": "string",
  "required_blocks": ["string"],
  "optional_blocks": ["string"]
}
```

### 6.1 Contract invariants

- `packet_schema_id` identifies the top-level DMP packet schema.
- `payload_contract_id` identifies the semantic meaning of the emitted packet.
- `compatibility_version` changes only when downstream expectations must change.
- `required_blocks` and `optional_blocks` must list block **kinds**, not arbitrary names.

The contract surface is the primary swappability mechanism. A consumer should not need to scrape arbitrary payload internals merely to discover what kind of message arrived.

## 7. Lineage surface

The lineage surface carries ancestry, dependency, and artefact provenance.

```json
{
  "parent_packet_ids": ["string"],
  "dependency_packet_ids": ["string"],
  "source_artifact_ids": ["string"],
  "input_fingerprint": "string|null",
  "review_trace_id": "string|null",
  "replay_trace_id": "string|null",
  "decision_trace_id": "string|null"
}
```

### 7.1 Lineage invariants

- `parent_packet_ids` are direct packet ancestors in the same logical chain.
- `dependency_packet_ids` are packet dependencies that influenced the current packet.
- `source_artifact_ids` identify externally stored artefacts referenced by the packet.
- `input_fingerprint` is a stable digest of the effective input set when deterministic comparison matters.
- `review_trace_id`, `replay_trace_id`, and `decision_trace_id` support later review/replay attribution without overloading `trace_id` itself.

## 8. Execution context surface

The execution-context surface keeps desk/runtime-specific controls at top level.

```json
{
  "stack_id": "string|null",
  "coefficient_set_id": "string|null",
  "playbook_id": "string|null",
  "registry_version": "string|null",
  "environment_tag": "string|null"
}
```

### 8.1 Execution-context invariants

- `stack_id` and `coefficient_set_id` remain first-class because replay and comparison work must cite them directly.
- `playbook_id` becomes relevant once registry-backed playbooks are live.
- `registry_version` identifies the relevant checked-in registry surface when applicable.
- `environment_tag` distinguishes research/simulation/live-like contexts without rewriting packet structure.

## 9. Block model

DMP v2 replaces the single v1 `payload` field with a **typed block array**.

Each block must declare:

```json
{
  "block_type": "string",
  "block_id": "string",
  "schema_id": "string",
  "data": {}
}
```

### 9.1 Allowed block families in v2 design

| Block family | Purpose |
|---|---|
| `object_block` | compact structured object |
| `metrics_block` | scalar metrics, flags, scores |
| `table_block` | tabular data with columns and row semantics |
| `timeseries_block` | ordered time-indexed sequences |
| `artifact_ref_block` | reference to externally stored artefact |
| `summary_block` | bounded human-readable summary surface |

Packets may carry one or more blocks. The packet contract declares which block kinds are required or optional.

### 9.2 Object block

Use when the output is a compact typed object.

Required `data` properties:

- object fields defined by `schema_id`

Examples:

- one decision payload
- one registry artifact descriptor
- one ladder span object

### 9.3 Metrics block

Use when the output is primarily scalar or categorical.

Required `data` properties:

- `metrics`: object of explicitly named values

Examples:

- `signal_score`
- `allow_trade`
- `zone_gamma`
- confidence bands or veto flags

### 9.4 Table block

Use when the output is tabular.

Required properties:

```json
{
  "table_schema_id": "string",
  "columns": [{"name": "string", "dtype": "string", "unit": "string|null"}],
  "primary_key": ["string"],
  "partition_keys": ["string"],
  "row_count": 0,
  "inline_rows": [],
  "artifact_ref": null
}
```

#### Table-block rules

- `table_schema_id` is mandatory.
- `columns` must be explicit.
- `primary_key` and `partition_keys` must be declared when known.
- small tables may use `inline_rows`.
- large tables must prefer an artefact reference.
- a table block must not silently mix inline rows and an artefact reference without a declared reason.

This is the critical surface for rich options-chain and options-metadata outputs.

### 9.5 Timeseries block

Use when order and index semantics matter.

Required properties:

- `index_kind`
- `index_name`
- `columns`
- either `points` or `artifact_ref`

Examples:

- realised volatility curves
- intraday price feature sequences
- replay score trajectories

### 9.6 Artefact-reference block

Use when the data is too large, too binary, or too persistent for inline transfer.

Required properties:

```json
{
  "artifact_id": "string",
  "artifact_kind": "string",
  "media_type": "string",
  "schema_id": "string",
  "uri": "string|null",
  "checksum": "string|null",
  "byte_count": 0
}
```

This is the claim-check lane for:

- options surfaces
- snapshots
- parquet/csv/json artefacts
- large replay outputs

### 9.7 Summary block

Use for bounded human-readable context only.

Required properties:

- `trader_summary`
- optional `operator_notes`

The summary block never replaces structured data. It exists so review surfaces can stay legible.

## 10. Summary surface

The top-level `summary` surface is mandatory even when there is also a `summary_block`.

```json
{
  "trader_summary": "string",
  "operator_summary": "string|null"
}
```

This keeps a consistent, bounded top-level explanation lane for review and UI surfaces.

## 11. Validation surface

The validation surface records schema and contract checks.

```json
{
  "schema_valid": true,
  "validation_errors": [],
  "contract_warnings": []
}
```

Packets with invalid schemas should not be silently accepted into runtime interchange.

## 12. Extensions surface

The `extensions` surface is the only reserved future-extension lane.

Rules:

- top-level unknown fields remain forbidden;
- future additions must land either in a version bump or under `extensions` with documented keys;
- `extensions` is not a dumping ground for untyped payload substitution.

## 13. Inline-versus-reference rule

DMP v2 must apply the following rule:

- compact objects, compact metrics, and small tables may be inline;
- rich tables, bulk snapshots, and large replay/report artefacts should prefer an artefact-reference block or a table/timeseries block with an attached `artifact_ref`.

This is mandatory for options-chain and other rich tabular surfaces.

## 14. Versioning rules

- `protocol_version` changes when the top-level DMP packet contract changes.
- `packet_schema_id` changes when the packet schema changes.
- `payload_contract_id` changes when the semantic meaning of the message changes.
- `compatibility_version` changes only when downstream consumers must adjust their assumptions.

## 15. Compatibility goals

DMP v2 is intended to support three concurrent shapes cleanly:

1. compact runtime-stage outputs,
2. review/replay lineage packets,
3. rich data packets such as options surfaces or external artefact references.

If a proposed packet shape does not fit one of those classes without distorting the protocol, the design is not ready.

## 16. Non-goals

DMP v2 does **not**:

- define an external vendor or broker protocol;
- replace MCP or any external transport protocol;
- guarantee frontend API shape;
- define storage implementation for every artefact reference;
- solve live deployment orchestration;
- permit arbitrary blob-style payloads without declared schemas.

## 17. Design stop rules

Stop the design if any of the following occurs:

1. packet structure starts duplicating the entire data lake inline;
2. the protocol stops being schema-governed and falls back to arbitrary dictionaries;
3. lineage becomes optional to the point of being decorative only;
4. the transport layer hardcodes today's seven-stage runtime so tightly that future modules cannot fit;
5. the extension lane becomes an excuse to bypass versioned contracts.
