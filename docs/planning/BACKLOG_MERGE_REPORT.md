# Backlog Merge Report

## Inputs merged
- `backlog/legacy_module_backlog.jsonl`
- `backlog/legacy_feature_backlog.jsonl`
- top-3 promotion candidates (for context)
- archive salvage from `part5_module_registry_draft.yaml`
- archive config/value shape from `runtime_settings_starter.yaml`, `evaluation_config_starter.yaml`, `coefficients_registry_starter.yaml`, `strategy_variants_starter.yaml`

## Outputs
- `backlog/module_backlog_merged.jsonl`
- `backlog/feature_backlog_merged.jsonl`

## Module merge result
- existing current legacy candidates preserved: 8
- new archive module/evaluator candidates added: 55
- archive duplicates/linked items preserved with resolution tags: 3
- archive defer items preserved as wrapper/backlog placeholders: 3
- archive config-only entries excluded from runtime backlog and handled via config salvage: 2

## Feature merge result
- existing current legacy feature candidates preserved: 20
- archive-derived feature additions added: 12

## Most important new additive archive modules
- `Conviction Tier Allocator`
- `Vvix Ladder Shaper`
- `Fill Feedback Router`
- `Macro Shock Responder`
- `Ladder Continuity Tracker`
- `Tail Hedge Injector`
- `Model Confidence Scorer`
- evaluator modules around attribution, conflict detection, and confidence divergence

## Duplicate / linked resolutions
- `phase_detector.py` -> linked to existing session clock feature family
- `slv_overlay_score.py` and `slv_validator.py` -> linked to Strategic Ladder Validator instead of treated as fully separate top-level modules
- `runtime_settings.yaml` and `evaluation_config.yaml` -> migrated as config examples, not runtime modules

## Guardrail
This merged backlog is still a **planning surface**. Inclusion here does not imply implementation or validity.
