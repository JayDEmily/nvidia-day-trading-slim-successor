# 2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_SCOPE_NOTE_v1

Status: retained bounded-scope note for the capital-deployment authority foundation pack closed through Gate 191 on `main`
## Purpose

Carry the bounded truth split for the first capital-deployment authority slice and freeze the execution boundaries for the tranche.

## Verified evidence inputs

- clean repo baseline: `repo_options_trace_integrity_repair_pack_closed_gate186_main_fullgit_2026-04-03_docs03_04_07_updated.zip`
- repo routing state: no active pack currently routed at tranche start
- existing downstream/runtime surfaces already present in `DeskCognitionRuntimeResult`, the stage-local handoff seam, the parallel-risk lane packet, and the capital snapshot model

## First-slice truth split carried into this pack

### Explicitly included in execution scope
- new-opening capital authorisation only
- current capital read path using the repo-native capital snapshot/equivalent current-capital surface
- bounded deployment decision output: deploy a size or stand down
- vocabulary admission work for the new naming as a later implementation leaf

### Explicitly excluded from this tranche
- position-close recommendations
- lifecycle/held-position management
- recommendation-memory lookback logic
- broker sync, fills, or realised/unrealised P&L accounting
- full portfolio arbiter behaviour across all book exposures

## Non-goals that must remain non-goals in code review

- Do not let the service recalculate upstream cognition.
- Do not let the service become a disguised second posture/risk engine.
- Do not add a new JSON-ledger architecture if the existing repo-native capital snapshot path can carry the bounded proof slice.
- Do not treat brainstorm language about a future arbiter as implementation authority for this first slice.

## Bounded service statement

The service this pack plans is not a market predictor. It is a downstream capital authoriser that consumes the already-formed opening recommendation plus current available capital and emits a bounded deployment decision.

## Future-scope reminders preserved for later packs

- recommendation-history persistence may matter later, but is not part of this first slice
- close-position and lifecycle logic must be handled in a later distinct tranche
- cross-book portfolio arbitration belongs to a later stronger-capital-governance layer