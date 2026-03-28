# 2026-03-28 Financial Calendar Crosswalk Spec v1

Status: active supporting artefact for Gate 89 on `main` branch work only; not a closeout claim by itself
Authority: subordinate to `docs/01_NORMATIVE.md`, `docs/02_OPERATING_MODEL.md`, `docs/03_DOMAIN_MODEL.md`, and `docs/planning/2026-03-28_FINANCIAL_CALENDAR_INTERSTITIAL_GATES_v3.md`

## Purpose

This spec freezes the deterministic crosswalk for the supplied 2026 financial-calendar bundle before any checked-in import seam or runtime projection lands.

The crosswalk exists to prevent two failure modes:

1. rich scheduled-facts authority entering the repo and then collapsing into legacy compatibility hints too early;
2. raw bundle event names causing free-text taxonomy drift inside canonical event surfaces.

## Canonical code surfaces

The frozen code surfaces for Gate 89 are:

- `src/nvda_desk/schemas/financial_calendar.py`
- `src/nvda_desk/services/financial_calendar_reference.py`
- `src/nvda_desk/schemas/dmp_v2.py`
- `src/nvda_desk/schemas/events.py`
- `src/nvda_desk/schemas/session_clock.py`
- `src/nvda_desk/schemas/market.py`
- `src/nvda_desk/schemas/cognition.py`

## Crosswalk law

### Projection targets

The bundle may project only into these repo-native target surfaces:

- `desk_calendar_authority`
- `raw_event_ingestion`
- `event_store`
- `precursor_runtime_packet`
- `temporal_context`

No Gate 89 record may target `session_clock` as canonical truth.
No Gate 89 record may target `PreparedRuntimeSnapshot.next_event_at` as the primary event system.
No Gate 89 record may create a new free-text event class or subclass.

### Mapping rules by fact family

- U.S. market-structure closures and half-days map first to desk-calendar authority and may also remain visible as venue-session event truth.
- Listed-options expiry anchors map to canonical expiry event truth.
- Month-end markers map to bounded temporal context only unless later doctrine explicitly widens the taxonomy.
- U.S. macro and policy releases map only through existing macro / policy canonical classes.
- `earnings_release` splits by entity scope:
  - NVDA uses canonical company identity;
  - direct read-through mega-cap names use canonical peer-company identity.
- Asia holiday and connectivity facts remain precursor venue-state truth first and only map into canonical event surfaces where an existing venue-session class already exists.
- Holiday-trading exceptions such as `jpx_derivatives_holiday_open` must not invent a new canonical event subclass in Gate 89.

### Rich-field retention law

The import and projection path must preserve, at minimum:

- event id
- layer id
- event type
- title
- start/end date
- timezone
- jurisdiction
- venues
- entities
- impact level
- runtime tags
- evaluation tags
- source status
- source document
- notes
- repo artefact id/path
- import lineage key

## Repo-native DMP v2 lane

The financial-calendar reference bundle uses one repo-native DMP v2 lane with these frozen compatibility choices:

- `grammar_role = temporal_context`
- `behaviour_class = replay_artefact`
- `packet_schema_id = dmp.packet@2.0.0`
- `payload_contract_id = temporal_context.financial_calendar_reference_bundle@1.0.0`
- top-level compatibility surfaces must remain explicit for:
  - schema identifiers
  - lineage
  - execution context
  - summary
  - validation
- required block mix:
  - one `object_block` carrying `FinancialCalendarBundleMetadata`
  - one or more `artifact_ref_block`s carrying repo-controlled artefact references

The supplied external example packet remains evidence only. It must not be copied verbatim because its grammar-role and behaviour-class identifiers are incompatible with the repo helper layer.

## Deliberate exclusions

Gate 89 does not:

- land checked-in bundle artefacts under `data/reference/financial_calendar/`;
- create runtime policy behaviour;
- amend temporal derivation;
- amend carry/session routing;
- widen canonical event taxonomy.
