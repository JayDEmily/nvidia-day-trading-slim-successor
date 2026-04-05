# 2026-04-05_TARGET_REPO_EVIDENCE_PROVENANCE_AND_IMMUTABILITY_RULES_v1

Status: Gate 201 planning authority; provenance, derivation, and immutability rules for later evidence-governance work.

## Purpose

Define the fields and rules that future evidence-governance and admission work must record so raw anchors, derived artefacts, sibling packs, replay packs, packet artefacts, and market-persisted surfaces cannot drift into one another silently.

## Mandatory provenance fields

Every future evidence dossier, inventory row, or admission note must capture all of the following:

- `evidence_id`: stable identifier for the surface being discussed;
- `evidence_class`: raw, derived, sibling, replay, review-report, packet, or market-persisted reference state;
- `exact_anchor`: checked-in file path, table name, or packet contract identifier;
- `authority_surface`: the gate/doc/test that admitted or governs the surface;
- `producer_path`: repo-native service, seed path, or review flow that creates the surface;
- `lineage_from`: exact upstream raw or packet anchor when the surface is derived;
- `downstream_consumers`: tests, services, or reports that read the surface now;
- `immutability_class`: immutable-admitted-anchor, immutable-admitted-pack, re-derivable-artefact, or persisted-reference-state;
- `supersession_policy`: what kind of later artefact could replace authority for this surface;
- `compatibility_state`: canonical, evidence-only, compatibility-only, or retired-from-authority.

## Immutability classes

### 1. Immutable admitted anchors
Use this for raw anchors and any later real-anchor admissions.

Rules:
- content does not mutate in place after admission;
- later stronger evidence must enter as a new anchor with its own admission surface;
- the prior anchor may be retired from authority but must remain referenceable.

Current repo examples:
- `fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json`

### 2. Immutable admitted packs
Use this for admitted sibling/replay packs whose content is treated as a reviewed baseline.

Rules:
- the pack content remains fixed once admitted;
- later versions require a new pack id and new admission or closeout surface;
- reports derived from the pack must cite the exact pack id.

Current repo examples:
- `fixtures/trace_review/gate_132_bounded_trace_fixture_pack.json`
- `fixtures/replay/gate_f_replay_regression_fixture_pack.json`

### 3. Re-derivable artefacts
Use this for checked-in artefacts that can be rebuilt from a named upstream anchor or pack.

Rules:
- the derivation path must be named;
- regeneration may update the artefact, but it may not silently rewrite the admitted upstream anchor;
- any regeneration must cite the exact upstream source and producing code path.

Current repo examples:
- `fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json`
- `fixtures/trace_review/gate_134_bounded_trace_report.json`
- `fixtures/replay/gate_f_expected_report.json`

### 4. Persisted reference state
Use this for repo-native tables that hold market-backed or execution-adjacent state used by services.

Rules:
- the seeding or capture origin must be named explicitly;
- migrations, seeders, or capture adapters may mutate the rows, but the provenance trail must identify the source document or fixture bundle;
- persisted reference state does not become a raw anchor automatically.

Current repo examples:
- `instrument`
- `bar_1m`
- `option_snapshot`

## Provenance-to-lineage law

- derived surfaces must cite their upstream anchor or pack by exact file/table/packet identifier;
- packet artefacts must also cite the governing packet contract surface;
- review reports must name both the reviewed evidence pack and the producing comparison/report path;
- evidence-only historical docs may be cited as context but may not become the sole authority field for a repo-native evidence surface.

## Supersession law

- supersession may change authority, not history;
- a new stronger anchor may supersede an older anchor, but the older anchor remains referenceable by exact identifier;
- a regenerated derivative may supersede an older derivative only when the upstream anchor and producing path are named;
- persisted reference-state updates must cite the migration, seed, or capture surface that changed them.

## What later work must not do

- invent provenance fields detached from repo-native evidence classes;
- treat prepared/runtime/replay/report surfaces as if they were raw anchors;
- rewrite historical evidence in place without an explicit supersession note;
- copy standalone machine-readable examples into repo authority without mapping them to repo-native packet law first.
