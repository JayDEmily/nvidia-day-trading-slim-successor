# 2026-03-24 Playbook Registry Spec

Status: Gates 11-12 typed-registry surface

## Purpose

This registry makes the four live Gate-D playbooks and their execution-template shapes explicit checked-in artefacts.

It exists to do three things only:
1. define `PlaybookSpec` and `ExecutionTemplateSpec` as typed offline-loadable contracts;
2. keep playbook and execution-template ownership separate from `StackDefinition` and `CoefficientSet` ownership;
3. provide one checked-in registry format that Gate 12 and Gate 13 can promote without inventing a second stack family.

## Registry format

The checked-in registry format is YAML. That matches the repo's existing config surface and remains testable offline.

Top-level fields:
- `schema_version`
- `registry_version`
- `notes`
- `execution_templates`
- `playbooks`

## ExecutionTemplateSpec

`ExecutionTemplateSpec` holds playbook-execution shape, not stack configuration.

Required fields:
- `template_id`
- `entry_style`
- `watch_execution_style`
- `scaling_step_factors`
- `default_inventory_action`
- `default_fresh_capital_action`
- `thesis_invalidation_state`
- `invalidation_reasons`
- `exit_reasons`

Optional-but-typed fields keep current execution semantics explicit:
- `hedge_exit_reason`
- `respect_posture_biases`
- `posture_override_actions`
- `inventory_pressure_states`
- `inventory_pressure_exit_reason`

`scaling_step_factors` are deliberately **not** required to sum to 1.0. Some current live playbooks, especially `negative_gamma_flush`, use partial/probe deployment shapes that intentionally leave deployable capital unused.

## PlaybookSpec

`PlaybookSpec` holds live-playbook identity, priority, rule linkage, execution-template linkage, and decision-profile defaults.

Required fields:
- `playbook_id`
- `title`
- `rule_id`
- `execution_template_id`
- `priority`
- `eligible`
- `watch_only`
- `ineligible`

Each decision profile is typed as:
- `decision`
- `action_bias`
- `sizing_fraction`
- `hedge_overlay`

## Gate 12 backfill notes

The four live playbooks are backfilled one-for-one in this registry:
- `continuation_ladder`
- `compression_breakout`
- `pin_reversion`
- `negative_gamma_flush`

Their priority order remains:
1. `continuation_ladder`
2. `compression_breakout`
3. `pin_reversion`
4. `negative_gamma_flush`

No new playbooks are introduced in this registry.

## Ownership boundaries

The registry must not create a second stack/config family.

So this registry **must not** own:
- stack membership
- coefficient weights
- replay comparison weighting
- live integration credentials

Those remain under the existing stack, coefficient, and runtime settings surfaces.
