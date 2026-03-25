# Remaining documents extraction plan

## Objective
Extract the four remaining legacy PDFs into admissible data fixtures, feature/module backlog additions, and failure-pattern guardrails without promoting unverified legacy material into executable repo surfaces.

## In scope
- `Options Data CSV Output.pdf`
- `of trading days below VWAP.pdf`
- `Comprehensive Deep-Dive_ What's Really Happening Today in NVDA_ (1).pdf`
- `NVDA GPT Framework Review.pdf`

## Out of scope
- runtime/API/DB changes
- IBKR/OpenAI/MCP work
- promotion into deterministic execution code
- treating screenshot/OCR-derived values as canonical market truth

## Classification contract
Every extracted item must carry:
- `source_document`
- `source_pages`
- `item_type`
- `provenance`
- `confidence`
- `repo_layer`
- `recompute_required`
- `promotion_status`

### Allowed values
`item_type`
- `raw_data_claim`
- `derived_math_claim`
- `feature_candidate`
- `module_candidate`
- `failure_pattern`
- `doctrine_note`

`provenance`
- `screenshot_derived`
- `ocr_cleaned`
- `manually_reconstructed`
- `conversation_inferred`
- `meta_review`

`repo_layer`
- `raw_vendor`
- `canonical_market`
- `derived_features`
- `research_artefacts`
- `execution_records`
- `docs_only`

`promotion_status`
- `fixture_candidate`
- `backlog_only`
- `needs_recompute`
- `discard`

## Execution phases
1. Freeze source inventory and page map.
2. Extract data-bearing blocks from `Options Data CSV Output.pdf` and `of trading days below VWAP.pdf`.
3. Extract strategy/module/feature value from `Comprehensive Deep-Dive...pdf` and `NVDA GPT Framework Review.pdf`.
4. Extract recurring failure patterns and map them to repo guardrail layers.
5. Recommend one next implementation-facing move.

## Hard rules
1. Numeric prose without a visible table/screenshot/OCR/manual reconstruction trail is not data.
2. OCR-cleaned or manually reconstructed rows may become fixture candidates, never canonical truth.
3. Strong ideas with weak provenance become backlog items, not code.
4. Off-topic identity/career drift is `docs_only` or discard.
5. Nothing extracted here is auto-promoted into runtime surfaces.

## Deliverables created in this pass
- `docs/legacy/REMAINING_DOCS_EXTRACTION_PLAN.md`
- `docs/legacy/REMAINING_DOCS_PAGE_MAP.md`
- `docs/legacy/LEGACY_DATA_ADMISSIBILITY.md`
- `backlog/legacy_data_fixtures_manifest.jsonl`
- `docs/legacy/LEGACY_STRATEGY_AND_FEATURE_CAPTURE.md`
- `backlog/legacy_feature_backlog_additions.jsonl`
- `backlog/legacy_module_backlog_additions.jsonl`
- `docs/legacy/LEGACY_FAILURE_PATTERNS_REMAINING_DOCS.md`
- `docs/planning/2026-03-18_REMAINING_DOCS_PROMOTION_RECOMMENDATION.md`
