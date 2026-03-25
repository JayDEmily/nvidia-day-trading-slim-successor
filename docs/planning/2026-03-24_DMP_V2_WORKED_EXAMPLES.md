# 2026-03-24 DMP V2 Worked Examples

Status: design draft only; not yet implemented

## 1. Purpose

This document gives specimen DMP v2 packets so the protocol can be read like a human artefact rather than a theorem.

The examples are intentionally mixed:

1. compact object/metrics packet,
2. rich options-surface packet,
3. mixed packet with inline summary plus external artefact reference,
4. replay/review lineage packet.

These are **examples**, not yet binding schemas.

---

## 2. Example A — compact temporal-context packet

Use case: a compact stage output with a small object block and a metrics block.

```json
{
  "protocol_version": "dmp.v2",
  "packet_id": "dmp::temporal_context::2026-03-24T15:20:00Z::core_full_stack::base_v1",
  "trace_id": "trace::2026-03-24::live_snapshot_001",
  "run_id": "run::2026-03-24::snapshot_001",
  "scenario_id": "live_snapshot",
  "producer": {
    "module_id": "temporal_context",
    "module_version": "2.0.0",
    "module_instance_id": "temporal_context::default",
    "grammar_role": "temporal_context",
    "stage_name": "temporal",
    "behaviour_class": "stage_output",
    "emitted_at": "2026-03-24T15:20:00Z"
  },
  "contract": {
    "packet_schema_id": "dmp.packet@2.0.0",
    "payload_contract_id": "temporal_context.output@1.0.0",
    "compatibility_version": "1",
    "required_blocks": ["object_block", "metrics_block"],
    "optional_blocks": ["summary_block"]
  },
  "lineage": {
    "parent_packet_ids": [],
    "dependency_packet_ids": [],
    "source_artifact_ids": [],
    "input_fingerprint": "sha256:temporal-input-001",
    "review_trace_id": null,
    "replay_trace_id": null,
    "decision_trace_id": null
  },
  "execution_context": {
    "stack_id": "core_full_stack",
    "coefficient_set_id": "base_v1",
    "playbook_id": null,
    "registry_version": null,
    "environment_tag": "research"
  },
  "blocks": [
    {
      "block_type": "object_block",
      "block_id": "temporal_window",
      "schema_id": "temporal_context.window@1.0.0",
      "data": {
        "session_phase": "opening_drive",
        "minutes_since_open": 17,
        "minutes_to_close": 373
      }
    },
    {
      "block_type": "metrics_block",
      "block_id": "temporal_flags",
      "schema_id": "temporal_context.flags@1.0.0",
      "data": {
        "metrics": {
          "is_opening_window": true,
          "is_midday": false,
          "volatility_bias": 0.62
        }
      }
    }
  ],
  "summary": {
    "trader_summary": "Still in opening-drive behaviour regime; time-of-day weighting remains elevated.",
    "operator_summary": null
  },
  "validation": {
    "schema_valid": true,
    "validation_errors": [],
    "contract_warnings": []
  },
  "extensions": {}
}
```

---

## 3. Example B — gamma-pressure packet with rich options surface

Use case: a module that emits a compact metrics block but also needs a large options table.

```json
{
  "protocol_version": "dmp.v2",
  "packet_id": "dmp::gamma_pressure::2026-03-24T15:20:00Z::core_full_stack::base_v1",
  "trace_id": "trace::2026-03-24::live_snapshot_001",
  "run_id": "run::2026-03-24::snapshot_001",
  "scenario_id": "live_snapshot",
  "producer": {
    "module_id": "gamma_pressure",
    "module_version": "2.0.0",
    "module_instance_id": "gamma_pressure::default",
    "grammar_role": "options_flow_context",
    "stage_name": "options_flow",
    "behaviour_class": "module_output",
    "emitted_at": "2026-03-24T15:20:00Z"
  },
  "contract": {
    "packet_schema_id": "dmp.packet@2.0.0",
    "payload_contract_id": "gamma_pressure.output@1.0.0",
    "compatibility_version": "1",
    "required_blocks": ["metrics_block", "table_block"],
    "optional_blocks": ["summary_block", "artifact_ref_block"]
  },
  "lineage": {
    "parent_packet_ids": [
      "dmp::options_data_capture::2026-03-24T15:19:58Z::core_full_stack::base_v1",
      "dmp::options_metadata_capture::2026-03-24T15:19:58Z::core_full_stack::base_v1"
    ],
    "dependency_packet_ids": [
      "dmp::spot_data_capture::2026-03-24T15:19:58Z::core_full_stack::base_v1"
    ],
    "source_artifact_ids": [
      "artifact::options_chain_surface::2026-03-24T15:19:58Z"
    ],
    "input_fingerprint": "sha256:gamma-input-001",
    "review_trace_id": null,
    "replay_trace_id": null,
    "decision_trace_id": null
  },
  "execution_context": {
    "stack_id": "core_full_stack",
    "coefficient_set_id": "base_v1",
    "playbook_id": null,
    "registry_version": null,
    "environment_tag": "research"
  },
  "blocks": [
    {
      "block_type": "metrics_block",
      "block_id": "gamma_metrics",
      "schema_id": "gamma_pressure.metrics@1.0.0",
      "data": {
        "metrics": {
          "signal_score": 0.84,
          "zone_gamma": "negative",
          "tag": "flush_risk"
        }
      }
    },
    {
      "block_type": "table_block",
      "block_id": "options_surface",
      "schema_id": "options.chain.surface@1.0.0",
      "data": {
        "table_schema_id": "options.chain.surface@1.0.0",
        "columns": [
          {"name": "expiry", "dtype": "date", "unit": null},
          {"name": "strike", "dtype": "float", "unit": "usd"},
          {"name": "call_gamma", "dtype": "float", "unit": null},
          {"name": "put_gamma", "dtype": "float", "unit": null}
        ],
        "primary_key": ["expiry", "strike"],
        "partition_keys": ["snapshot_ts"],
        "row_count": 0,
        "inline_rows": [],
        "artifact_ref": {
          "artifact_id": "artifact::options_chain_surface::2026-03-24T15:19:58Z",
          "artifact_kind": "options_surface",
          "media_type": "application/parquet",
          "schema_id": "options.chain.surface@1.0.0",
          "uri": "artifact://options_chain_surface/2026-03-24T15:19:58Z",
          "checksum": "sha256:options-surface-001",
          "byte_count": 285104
        }
      }
    }
  ],
  "summary": {
    "trader_summary": "Negative gamma cluster building near spot; flush risk elevated.",
    "operator_summary": "Large options surface externalised via artefact reference."
  },
  "validation": {
    "schema_valid": true,
    "validation_errors": [],
    "contract_warnings": []
  },
  "extensions": {}
}
```

---

## 4. Example C — ladder-constructor packet with mixed compact outputs

Use case: a module that emits one structured object and a small inline table.

```json
{
  "protocol_version": "dmp.v2",
  "packet_id": "dmp::ladder_constructor::2026-03-24T15:21:00Z::core_full_stack::base_v1",
  "trace_id": "trace::2026-03-24::live_snapshot_001",
  "run_id": "run::2026-03-24::snapshot_001",
  "scenario_id": "live_snapshot",
  "producer": {
    "module_id": "ladder_constructor",
    "module_version": "2.0.0",
    "module_instance_id": "ladder_constructor::default",
    "grammar_role": "expression_execution",
    "stage_name": null,
    "behaviour_class": "module_output",
    "emitted_at": "2026-03-24T15:21:00Z"
  },
  "contract": {
    "packet_schema_id": "dmp.packet@2.0.0",
    "payload_contract_id": "ladder_constructor.output@1.0.0",
    "compatibility_version": "1",
    "required_blocks": ["object_block", "table_block"],
    "optional_blocks": ["summary_block"]
  },
  "lineage": {
    "parent_packet_ids": [
      "dmp::options_metadata_capture::2026-03-24T15:20:54Z::core_full_stack::base_v1"
    ],
    "dependency_packet_ids": [
      "dmp::spot_data_capture::2026-03-24T15:20:54Z::core_full_stack::base_v1"
    ],
    "source_artifact_ids": [],
    "input_fingerprint": "sha256:ladder-input-001",
    "review_trace_id": null,
    "replay_trace_id": null,
    "decision_trace_id": null
  },
  "execution_context": {
    "stack_id": "core_full_stack",
    "coefficient_set_id": "base_v1",
    "playbook_id": "continuation_ladder",
    "registry_version": "registry.v1",
    "environment_tag": "research"
  },
  "blocks": [
    {
      "block_type": "object_block",
      "block_id": "ladder_summary",
      "schema_id": "ladder_constructor.summary@1.0.0",
      "data": {
        "expiry": "2026-03-27",
        "ladder_span": 5,
        "anchor_spot": 972.35
      }
    },
    {
      "block_type": "table_block",
      "block_id": "ladder_rows",
      "schema_id": "ladder_constructor.rows@1.0.0",
      "data": {
        "table_schema_id": "ladder_constructor.rows@1.0.0",
        "columns": [
          {"name": "leg_index", "dtype": "integer", "unit": null},
          {"name": "strike", "dtype": "float", "unit": "usd"},
          {"name": "direction", "dtype": "string", "unit": null}
        ],
        "primary_key": ["leg_index"],
        "partition_keys": [],
        "row_count": 3,
        "inline_rows": [
          {"leg_index": 1, "strike": 970.0, "direction": "buy"},
          {"leg_index": 2, "strike": 975.0, "direction": "sell"},
          {"leg_index": 3, "strike": 980.0, "direction": "sell"}
        ],
        "artifact_ref": null
      }
    }
  ],
  "summary": {
    "trader_summary": "Short ladder built around spot with bounded inline legs.",
    "operator_summary": null
  },
  "validation": {
    "schema_valid": true,
    "validation_errors": [],
    "contract_warnings": []
  },
  "extensions": {}
}
```

---

## 5. Example D — review/replay attribution packet

Use case: a packet that exists mainly to explain and trace a decision rather than to move a market-data surface.

```json
{
  "protocol_version": "dmp.v2",
  "packet_id": "dmp::review_trace::2026-03-24T15:25:00Z::core_full_stack::base_v1",
  "trace_id": "trace::2026-03-24::live_snapshot_001",
  "run_id": "replay::2026-03-24::config_a_vs_b",
  "scenario_id": "config_compare",
  "producer": {
    "module_id": "review_trace_attribution",
    "module_version": "2.0.0",
    "module_instance_id": "review_trace_attribution::default",
    "grammar_role": "review_explanation",
    "stage_name": "review",
    "behaviour_class": "review_packet",
    "emitted_at": "2026-03-24T15:25:00Z"
  },
  "contract": {
    "packet_schema_id": "dmp.packet@2.0.0",
    "payload_contract_id": "review_trace.output@1.0.0",
    "compatibility_version": "1",
    "required_blocks": ["object_block", "summary_block"],
    "optional_blocks": ["artifact_ref_block"]
  },
  "lineage": {
    "parent_packet_ids": [
      "dmp::execution_expression::2026-03-24T15:24:55Z::core_full_stack::base_v1"
    ],
    "dependency_packet_ids": [
      "dmp::temporal_context::2026-03-24T15:24:53Z::core_full_stack::base_v1",
      "dmp::market_regime_context::2026-03-24T15:24:53Z::core_full_stack::base_v1",
      "dmp::options_flow_context::2026-03-24T15:24:54Z::core_full_stack::base_v1",
      "dmp::posture_risk_permission::2026-03-24T15:24:54Z::core_full_stack::base_v1",
      "dmp::playbook_eligibility::2026-03-24T15:24:55Z::core_full_stack::base_v1"
    ],
    "source_artifact_ids": [
      "artifact::replay_compare::2026-03-24T15:25:00Z"
    ],
    "input_fingerprint": "sha256:review-trace-001",
    "review_trace_id": "review::2026-03-24::001",
    "replay_trace_id": "replay::2026-03-24::config_a_vs_b",
    "decision_trace_id": "decision::2026-03-24::001"
  },
  "execution_context": {
    "stack_id": "core_full_stack",
    "coefficient_set_id": "base_v1",
    "playbook_id": "continuation_ladder",
    "registry_version": "registry.v1",
    "environment_tag": "research"
  },
  "blocks": [
    {
      "block_type": "object_block",
      "block_id": "review_attribution",
      "schema_id": "review_trace.output@1.0.0",
      "data": {
        "decision": "allow",
        "review_packet_id": "review::2026-03-24::001",
        "decision_packet_id": "dmp::execution_expression::2026-03-24T15:24:55Z::core_full_stack::base_v1",
        "stage_packet_ids": {
          "temporal": "dmp::temporal_context::2026-03-24T15:24:53Z::core_full_stack::base_v1",
          "regime": "dmp::market_regime_context::2026-03-24T15:24:53Z::core_full_stack::base_v1",
          "options_flow": "dmp::options_flow_context::2026-03-24T15:24:54Z::core_full_stack::base_v1",
          "posture": "dmp::posture_risk_permission::2026-03-24T15:24:54Z::core_full_stack::base_v1",
          "eligibility": "dmp::playbook_eligibility::2026-03-24T15:24:55Z::core_full_stack::base_v1",
          "execution": "dmp::execution_expression::2026-03-24T15:24:55Z::core_full_stack::base_v1"
        }
      }
    },
    {
      "block_type": "summary_block",
      "block_id": "review_summary",
      "schema_id": "review_trace.summary@1.0.0",
      "data": {
        "trader_summary": "Decision allowed after temporal tailwind and options-flow support aligned; posture remained permissive.",
        "operator_notes": "Replay artefact available for full comparison drill-down."
      }
    }
  ],
  "summary": {
    "trader_summary": "Review trace packet preserves full packet ancestry for replay and operator explanation.",
    "operator_summary": "Designed for review/replay observability, not new trade logic."
  },
  "validation": {
    "schema_valid": true,
    "validation_errors": [],
    "contract_warnings": []
  },
  "extensions": {}
}
```
