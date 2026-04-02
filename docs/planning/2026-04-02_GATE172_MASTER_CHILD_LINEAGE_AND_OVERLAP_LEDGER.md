# 2026-04-02_GATE172_MASTER_CHILD_LINEAGE_AND_OVERLAP_LEDGER

## Purpose

Freeze the exact git ancestry, overlap surfaces, child-only import surfaces, and manual merge law before any runtime coding claims are made.

## Shared base and unique commit ranges

- shared base: `4640f70`
- master unique commits: `b73c306`, `0e3a300`, `fc4ea50`, `fad9a68`, `a6790b4`, `5d5590e`, `5634036`, `3ce4bf8`
- child unique commits: `ad32306`, `ff8f32c`, `1bec0e2`, `ce3f373`, `ef165c8`

## Verified repo-state finding

The child repo contains **no verified `src/` runtime delta** from the shared base. It is a planning-law, reference-data, vocabulary, and workbook-governance branch.

## Overlap ledger

### Shared router/control surfaces requiring manual rewrite

- `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `CHANGELOG.jsonl`

### Child-only surfaces to import into master

- frozen-law updates in `docs/01_NORMATIVE.md`, `docs/02_OPERATING_MODEL.md`, and `config/README.md`
- governed workbook/reference-data updates under `docs/reference/` and `data/reference/signal_workbooks/`
- generator/vocabulary updates in `scripts/build_canonical_vocabulary.py` and the generated vocabulary JSON
- active-lineage workbook-path rewires in the 2026-03-31 signal-coefficient authority planning files
- the full child planning pack and planning-guard tests

## Manual merge law

1. Master remains canonical.
2. child wins on parallel-risk planning law, workbook-governance law, and canonical workbook path rewiring.
3. Master wins on already closed coefficient / policy / temporal / observability planning law.
4. Router/control surfaces are rewritten manually rather than cherry-picked.
5. No `src/` runtime import may be claimed from child because no verified `src/` child delta exists.
6. Gate 173 must finish before Gate 174 or Gate 175 may claim lawful runtime implementation.

## Resulting execution order

1. import child planning/reference-data/vocabulary into master
2. reconcile workbook promotion/demotion and rebuild vocabulary surfaces
3. code the lane input contract and lawful-read boundary in master
4. code temporal/calendar/event/multi-clock runtime surfaces in master
