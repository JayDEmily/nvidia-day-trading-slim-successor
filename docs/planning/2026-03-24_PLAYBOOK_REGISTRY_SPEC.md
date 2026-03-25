# 2026-03-24 Playbook Registry Spec

Status: Gate 47 registry-v2 typed-registry surface

## Purpose

This registry now defines the live deterministic playbook hierarchy as checked-in typed artefacts.

It exists to do four things only:
1. define playbook families, setup variants, execution expressions, horizons, constraints, and risk overrides as typed offline-loadable contracts;
2. keep playbook hierarchy ownership separate from stack/coefficient ownership;
3. provide one checked-in registry format that runtime readers can consume without inventing ad hoc side dictionaries;
4. preserve a bounded compatibility bridge from the older flat playbook rows.

## Registry format

The checked-in registry format is YAML.

Top-level fields:
- `schema_version`
- `registry_version`
- `notes`
- `families`
- `setup_variants`
- `execution_templates`
- `playbooks`

## PlaybookFamilySpec

Required fields:
- `family_id`
- `title`
- `description`
- `horizon`
- `state_requirements`
- `phase_constraints`

## SetupVariantSpec

Required fields:
- `setup_variant_id`
- `family_id`
- `title`
- `description`
- `state_requirements`

Optional fields:
- `phase_constraints`
- `risk_overrides`

## ExecutionTemplateSpec

`ExecutionTemplateSpec` still holds execution shape, not stack configuration.

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

## PlaybookSpec

`PlaybookSpec` is now the leaf binding row that connects family, setup variant, and execution expression.

Required fields:
- `playbook_id`
- `title`
- `rule_id`
- `family_id`
- `setup_variant_id`
- `execution_expression_id`
- `horizon`
- `priority`
- `eligible`
- `watch_only`
- `ineligible`

Optional typed fields:
- `constraints`
- `risk_overrides`

Each decision profile remains typed as:
- `decision`
- `action_bias`
- `sizing_fraction`
- `hedge_overlay`

## Current live coverage

The live checked-in registry now covers seven playbooks across explicit family and setup-variant hierarchy, including the options-first additions introduced in the Gates 41–44 tranche.

## Ownership boundaries

This registry must not create a second stack/config family.

So this registry **must not** own:
- stack membership
- coefficient weights
- replay comparison weighting
- live integration credentials

Those remain under the existing stack, coefficient, and runtime settings surfaces.
