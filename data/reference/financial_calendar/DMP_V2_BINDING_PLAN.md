# DMP v2 Binding Plan for the Financial Calendar Bundle

Status: proposal artifact for pre-testing architecture work  
Authority: subordinate to `docs/01_NORMATIVE.md` and the canonical DMP v2 spec  
Scope: how the financial calendar bundle should sit inside the repo before historical testing begins

## 1. Intent

The calendar bundle is **reference truth**, not a live alpha module.

It should be stored as layered raw artefacts, then projected into narrow runtime state labels such as:

- `us_cash_closed`
- `us_cash_half_day`
- `monthly_opex`
- `macro_risk_window`
- `fomc_window`
- `cpi_release`
- `employment_release`
- `nvda_earnings`
- `direct_readthrough_earnings`
- `jpx_cash_closed`
- `jpx_derivatives_open`
- `stock_connect_closed`

The runtime should consume those derived labels in deterministic posture logic, not re-interpret the web at runtime.

## 2. Suggested repo placement

Recommended on-repo destination:

`data/reference/financial_calendar/`

Suggested contents:

- `financial_calendar_master_2026.json`
- `layers/*.json`
- `source_manifest.json`
- `DMP_V2_BINDING_PLAN.md`
- `dmp_v2_financial_calendar_bundle_example.json`

## 3. Suggested import path

### 3.1 Raw import
Import the JSON bundle into a reference store or checked-in data artefact path.

### 3.2 Canonical projection
Normalize raw facts into:
- session calendar rows where a venue is closed or half-day
- market event rows for macro, expiry, earnings, and precursor-state events

### 3.3 Runtime projection
At runtime, produce only the bounded labels needed by:
- `EventsService`
- `TemporalContextService`
- carry / event-window routing
- later state-conditioned modifier policy

## 4. DMP v2 shape

The bundle should travel as:
- one compact `object_block` carrying bundle metadata and coverage summary
- one or more `artifact_ref_block`s referencing the master JSON and layer JSON artefacts

The packet should not inline the entire calendar as one giant object block.

## 5. Review and audit expectations

Every imported event should retain:
- source document identity
- confirmed vs estimated status
- venue / jurisdiction ownership
- runtime tags and evaluation tags

This lets review packets explain **why** a given day was treated as:
- event-imminent
- expiry-elevated
- half-day
- precursor-thin
- direct-readthrough risk

## 6. Deliberate exclusions

This bundle does **not**:
- fetch data live from the internet
- attempt to encode unscheduled headlines
- attempt to predict market reaction
- include every earnings date in the world
- override options-surface or market-structure evidence

It is a scheduled-facts scaffold only.
