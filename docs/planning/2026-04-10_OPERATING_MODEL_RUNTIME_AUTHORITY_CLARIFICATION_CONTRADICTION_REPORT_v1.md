# 2026-04-10_OPERATING_MODEL_RUNTIME_AUTHORITY_CLARIFICATION_CONTRADICTION_REPORT_v1

Status: closed contradiction report retained as evidence for Gate 257.

## Contradiction addressed

`docs/02_OPERATING_MODEL.md` still left a bounded runtime-authority ambiguity around Independent Parallel Risk Lane.

Observed truth before Gate 257:
- the file already described the lane as co-resident in planning placement terms;
- the file did not yet state explicitly that the lane is not an eighth serial stage;
- the file did not yet state explicitly that the lane is not an independent final arbiter over the seven-step grammar;
- the file did not yet state explicitly that `final_risk_join` is compatibility-only and does not outrank preserved downstream seam surfaces;
- the file did not yet state explicitly that after Expression and Execution forms the candidate, Capital Deployment Authority Service is the only downstream fresh-capital authority.

## Resolution

- add the missing explicit authority-boundary wording inside the existing Independent Parallel Risk Lane section of `docs/02_OPERATING_MODEL.md`;
- leave runtime code, schemas, services, `docs/03_DOMAIN_MODEL.md`, and `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` untouched;
- prove the clarification with targeted grep/assert doctrine checks only.

## Result

The operating-model doctrine now says explicitly that Independent Parallel Risk Lane is co-resident and descriptive, not an eighth serial stage or independent final arbiter, that `final_risk_join` remains compatibility-only, and that Capital Deployment Authority Service remains the sole downstream fresh-capital authority after Expression and Execution.
