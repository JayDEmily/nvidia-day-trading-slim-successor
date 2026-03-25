# Config and Variants Crosswalk

## Source files salvaged
- `runtime_settings_starter.yaml`
- `evaluation_config_starter.yaml`
- `coefficients_registry_starter.yaml`
- `strategy_variants_starter.yaml`

## Current repo target
The repo **now has typed config surfaces** for the salvaged examples.
The archive salvage still lands as example YAML under `config/`, but selected parts are wired into sandbox-safe services and routes:
- runtime settings surface
- evaluation settings surface
- coefficient-group lookup surface
- strategy-variant lookup surface
- coefficient and variant use in batch experiments / allocation

This is still **not** a live external runtime-config system. It is a typed, offline-safe surface that keeps provenance explicit.

## Preserved value
### Runtime settings
Useful value preserved:
- explicit separation of runtime safety toggles, entry gating, execution expectations, and environment controls.
- typed route and loader surface for review and experiments.

### Evaluation config
Useful value preserved:
- separation of runtime from evaluator review;
- explicit evaluator inputs/outputs;
- human-reviewed post-run evaluation discipline.

### Coefficients registry
Useful value preserved:
- each coefficient has value, test range, and notes;
- promotes empirical pruning rather than hidden magic numbers;
- selected coefficient groups can now influence sandbox-safe experiment and allocation flows.

### Strategy variants
Useful value preserved:
- named variant profiles (`baseline`, `conservative`, `aggressive`, `macro_defensive`, `gamma_heavy`, etc.);
- weights/coefficient overrides separated from the module registry itself;
- variant selection can now flow into batch ranking and allocator surfaces.

## What was not imported as-is
- no archive config file is treated as validated trading truth;
- no archive coefficient is treated as market-verified truth;
- no strategy variant is treated as a live strategy;
- no live external config reload loop exists in the sandbox.

## Repo additions from this crosswalk
- `config/runtime_settings.example.yaml`
- `config/evaluation_config.example.yaml`
- `config/coefficients_registry.example.yaml`
- `config/strategy_variants.example.yaml`
- `config/README.md`
- `src/nvda_desk/config_models.py`
- `src/nvda_desk/services/config_surface.py`
- `/config/*` routes in the API surface

## Recommended discipline from here
1. keep config files as typed example inputs unless replay/eval evidence promotes them;
2. allow coefficient groups and variants to steer experiments/allocation before they steer real execution;
3. continue treating config as a provenance-carrying input surface, not an oracle.
