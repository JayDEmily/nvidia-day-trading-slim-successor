# 2026-03-24 DMP V2 Implementation Receipt

Status: historical implementation receipt from the mixed-mode pre-promotion phase


Status: implemented on `main` as draft/migration surface; not the canonical live runtime transport  
Scope: DMP v2 schema layer, runtime packetisation adapter path, review/replay lineage adoption, and regression proof against the existing Gate 8-10 surfaces.

## What was implemented

- Added `src/nvda_desk/schemas/dmp_v2.py` with:
  - fixed v2 packet envelope,
  - producer / contract / lineage / execution-context surfaces,
  - typed block families (`object_block`, `metrics_block`, `table_block`, `timeseries_block`, `artifact_ref_block`, `summary_block`),
  - v1-to-v2 upgrade helper.
- Kept `src/nvda_desk/schemas/dmp.py` intact as the bounded v1 surface.
- Extended the runtime to emit `stage_packets_v2` while keeping the v1 packet path available.
- Updated review/replay lineage surfaces to record `protocol_version="dmp.v2"`.
- Added DMP v2 protocol and migration tests, plus runtime/review/replay regression checks proving the v2 packet ids stay aligned with the deterministic stage order.

## Non-goals preserved

- No frontend transport changes.
- No broker/live vendor protocol redesign.
- No playbook registry work.
- No silent deletion of DMP v1.

## Validation target

The implementation is acceptable only if:

- targeted DMP v1/v2 and runtime-lineage tests pass,
- the full pytest suite passes,
- `make check` passes,
- the changelog remains parseable,
- and the generated zip excludes `.venv` plus cache artefacts while keeping `.git` history.