# Config Surfaces

These files preserve two different config roles. They are not interchangeable.

## Governed coefficient authority

- `coefficient_authority.v1.yaml`

This is the typed Gate 123 authority surface for the admitted tranche-one coefficient universe only. It freezes owner stage, units, baseline, min/max envelope, transform family, and allowed upstream drivers for the coefficient surfaces that later gates may wire into runtime.

This file is governed authority even though Gate 124 and Gate 126 have not yet wired every consumer to it. It is not a salvage placeholder.

## Legacy example and salvage surfaces

These files preserve useful structure salvaged from the master archive. They remain **example-only** and are not the governed runtime authority for coefficient surfaces.

Files:
- `runtime_settings.example.yaml`
- `evaluation_config.example.yaml`
- `coefficients_registry.example.yaml`
- `strategy_variants.example.yaml`

Use the example files as compatibility/reference inputs when promoting more of the archive into typed runtime configuration. Do not treat `coefficients_registry.example.yaml` as interchangeable with `coefficient_authority.v1.yaml`.
