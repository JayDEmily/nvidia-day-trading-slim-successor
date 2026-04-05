# 2026-04-05_TARGET_REPO_EVIDENCE_INVENTORY_BASELINE_v1

Status: Gate 201 planning authority; inventory baseline for the target-repo admitted-evidence successor pack.

## Purpose

Name the canonical evidence classes already present in the target repo, keep raw-versus-derived truth explicit, and record the exact anchor for each class before any later collection or admission work begins.

## Canonical evidence class matrix

| Evidence class | Status | Repo-native kind | Exact anchor | Governing admission / authority | Downstream use now | Mutation rule |
|---|---|---|---|---|---|---|
| Canonical raw runtime anchor | admitted canonical anchor | raw | `fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json` | `docs/planning/2026-03-30_GATE101_CANONICAL_RAW_BUNDLE_ADMISSION.md` | input to `RealDataLoaderService.prepare_runtime_dataset(...)` and `build_runtime_snapshot_sanity_report(...)` | immutable after admission; later evidence may supersede by new explicit admission only |
| Prepared runtime fixture pack | admitted checked-in derivative | derived from the raw runtime anchor | `fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json` | `docs/planning/2026-03-30_GATE101_CANONICAL_RAW_BUNDLE_ADMISSION.md`; `src/nvda_desk/services/real_data_loader.py` | runtime harnesses, prepared snapshot lineage, sanity-report regeneration | may be regenerated from the admitted raw bundle; regeneration must not silently rewrite the raw anchor |
| Bounded sibling trace scenario pack | admitted sibling / review input | sibling pack anchored to the prepared runtime path | `fixtures/trace_review/gate_132_bounded_trace_fixture_pack.json` | `docs/planning/2026-03-31_GATE132_BOUNDED_TRACE_SCENARIO_PACK.md` | bounded semantic review and scenario comparison | immutable once admitted; later packs must cite the anchor they branch from |
| Bounded trace report | admitted review output | derived review artefact | `fixtures/trace_review/gate_134_bounded_trace_report.json` | `docs/planning/2026-03-31_GATE134_BOUNDED_TRACE_REPORTING_CLOSEOUT.md` | plain-English report surface for the bounded sibling pack | may be regenerated from the admitted sibling pack and live runtime; must retain explicit pack linkage |
| Replay regression fixture pack | admitted replay evidence | replay pack | `fixtures/replay/gate_f_replay_regression_fixture_pack.json` | replay-facing tests plus successor-pack scope note | replay comparison, horizon discovery, review-packet comparison | immutable as admitted evidence; later replay packs must be separately admitted |
| Replay expected report | admitted replay review output | derived review/report artefact | `fixtures/replay/gate_f_expected_report.json` | replay comparison tests and checked-in replay evidence path | expected report baseline for replay comparison | may be regenerated only from the named replay pack and exact reviewed ruleset |
| Market-persisted reference state | repo-native persisted market evidence family | persisted reference tables | `instrument`, `bar_1m`, and `option_snapshot` tables in `src/nvda_desk/db/models.py` | `docs/status/2026-03-19_SLV_MARKET_DEEPENING_PASS6.md`; `src/nvda_desk/db/models.py`; `src/nvda_desk/services/slv_market.py` | market-backed SLV surface, option-surface retrieval, and later target-snapshot planning | rows are mutable through explicit seeding / migration / capture flows only; any later admission dossier must record the seeding source and environment |

## Exact anchor notes

### Raw bundle
- top-level blocks: `provenance`, `bars`, `option_chain_snapshots`, `events`
- current admitted counts: 4 bar rows, 3 option-chain snapshots, 2 event rows
- this is the only repo-native raw runtime anchor presently admitted for the successor pack.

### Prepared runtime fixture pack
- top-level blocks: `pack_id`, `bundle`, `prepared_dataset`, `sanity_report`
- the checked-in pack preserves the embedded raw bundle and the prepared derivative together, but Gate 101 froze the rule that only the raw bundle is admitted as the canonical raw anchor.

### Bounded trace review family
- `gate_132_bounded_trace_fixture_pack.json` carries the sibling scenarios.
- `gate_134_bounded_trace_report.json` carries the generated review/report output from that sibling pack.
- these are related but not the same evidence class.

### Replay family
- `gate_f_replay_regression_fixture_pack.json` is the admitted replay input pack.
- `gate_f_expected_report.json` is the report/expectation artefact derived against that replay pack.
- replay evidence is not a substitute for new raw-anchor admission.

### Market-persisted family
- `instrument` anchors symbol identity.
- `bar_1m` anchors persisted market bars.
- `option_snapshot` anchors persisted option-surface state used by the market-backed SLV path.
- later event/log/decision tables in `src/nvda_desk/db/models.py` are runtime records, not admitted evidence anchors for this pack.

## Class boundaries preserved

- raw and derived are not interchangeable;
- sibling packs and replay packs are review/evaluation evidence, not fresh raw anchors;
- persisted market tables are evidence-bearing storage surfaces only when their seeding/capture source is named explicitly;
- old standalone planning docs remain evidence-only and are not evidence classes in this inventory.

## Inventory result for Gate 201

The target repo currently has seven evidence classes that matter for successor planning:
1. one canonical raw runtime anchor;
2. one checked-in prepared derivative;
3. one sibling trace pack;
4. one bounded trace report;
5. one replay regression pack;
6. one replay expected report;
7. one market-persisted reference-state family.

That is the baseline Gate 202 onward must govern. It is enough to plan provenance, coverage review, redundancy rejection, and later collection without pretending the repo already has a broader real-anchor portfolio.
