# Legacy Fixture Pack Spec

## Purpose
Preserve admitted legacy data as **test fixtures only**.

## Rules
- Fixtures are never canonical market truth.
- Every fixture must carry source document, page range, provenance, and confidence.
- Screenshot-derived or OCR-cleaned material may be used for tests and schema examples only.
- Conversation-inferred rows stay low-confidence unless later revalidated.

## Current admitted fixtures
1. `fixtures/legacy/options_snapshots/options_data_csv_output_admitted.csv`
2. `fixtures/legacy/fixtures_manifest.jsonl`

## Deferred source
`of trading days below VWAP.pdf` remains valuable, but its numeric content is too intertwined with retrospective commentary to admit more than a reserved placeholder in this pass.
