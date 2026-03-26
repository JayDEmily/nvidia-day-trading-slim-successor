# 2026-03-24 DMP V2 Acceptance Checklist

Status: historical planning artefact; retained after Gates 56–58 for audit context


Status: design draft only; not yet implemented

Use this checklist before any DMP v2 implementation is treated as acceptable.

## 1. Design acceptance

### 1.1 Core design

- [ ] The document explicitly defines DMP v2 as the canonical internal message contract.
- [ ] The protocol is described as **fixed envelope + typed blocks**, not as a generic JSON blob.
- [ ] The protocol includes a reserved `extensions` surface rather than uncontrolled top-level extras.
- [ ] The design keeps `stack_id` and `coefficient_set_id` first-class.
- [ ] The design explicitly distinguishes packet lineage from external artefact provenance.

### 1.2 Contract clarity

- [ ] There is an explicit `contract` surface.
- [ ] Packet schema id and payload contract id are both defined.
- [ ] Required and optional block kinds are declared.
- [ ] The protocol does not require payload archaeology to discover message meaning.

### 1.3 Rich data support

- [ ] The design has a first-class `table_block`.
- [ ] The design has a first-class `timeseries_block`.
- [ ] The design has a first-class `artifact_ref_block`.
- [ ] The design explicitly supports large options tables without forcing them inline.
- [ ] The inline-versus-reference rule is written down, not assumed.

### 1.4 Provenance depth

- [ ] Parent packet ids are supported.
- [ ] Dependency packet ids are supported.
- [ ] Source artefact ids are supported.
- [ ] Input fingerprint is supported.
- [ ] Review, replay, and decision trace ids are supported.

## 2. Example acceptance

- [ ] There is at least one compact packet example.
- [ ] There is at least one rich options-surface example.
- [ ] There is at least one review/replay lineage example.
- [ ] At least one example demonstrates inline rows.
- [ ] At least one example demonstrates an external artefact reference.

## 3. Migration acceptance

- [ ] The v1 -> v2 field mapping is explicit.
- [ ] Breaking changes are named explicitly.
- [ ] Stability goals are named explicitly.
- [ ] A phased migration path exists.
- [ ] The migration note forbids deleting v1 in the same pass that first introduces v2.

## 4. Implementation acceptance

The following must be true before a DMP v2 code pass is marked complete.

### 4.1 Schema layer

- [ ] DMP v2 schemas exist in code beside v1 rather than silently replacing v1.
- [ ] Unknown top-level fields are rejected.
- [ ] Required top-level surfaces validate correctly.
- [ ] Block-level schema ids validate correctly.
- [ ] Validation and summary surfaces exist and serialise cleanly.

### 4.2 Block layer

- [ ] `object_block` is implemented and tested.
- [ ] `metrics_block` is implemented and tested.
- [ ] `table_block` is implemented and tested.
- [ ] `timeseries_block` is implemented and tested.
- [ ] `artifact_ref_block` is implemented and tested.
- [ ] `summary_block` is implemented and tested.

### 4.3 Rich-data tests

- [ ] A small inline table case passes.
- [ ] A large-table-as-artefact-reference case passes.
- [ ] An options-surface-like contract case passes.
- [ ] A replay/report artefact-reference case passes.

### 4.4 Lineage tests

- [ ] Parent lineage is preserved.
- [ ] Dependency lineage is preserved.
- [ ] Review trace id is preserved.
- [ ] Replay trace id is preserved.
- [ ] Decision trace id is preserved.
- [ ] Input fingerprint is stable under deterministic replay.

### 4.5 Regression tests

- [ ] Current Gate 8-10 behaviours still pass.
- [ ] Review/replay serialisation remains deterministic.
- [ ] Runtime packet order remains truthful where runtime stages are involved.
- [ ] Current playbook behaviour does not drift just because packet shape changed.

## 5. Rejection criteria

Reject a proposed DMP v2 implementation if any of the following is true.

- [ ] The implementation falls back to untyped `dict[str, Any]` payload blobs.
- [ ] The implementation treats the options-table case as an afterthought.
- [ ] The implementation removes first-class stack/coefficient identity.
- [ ] The implementation hides lineage in free-form text.
- [ ] The implementation forces all artefacts inline.
- [ ] The implementation silently replaces v1 without dual-path evidence.

## 6. Promotion rule

Do not promote DMP v2 to active runtime truth until:

- [ ] the design artefacts are approved,
- [ ] the code artefacts pass the schema and regression tests,
- [ ] the migration evidence exists,
- [ ] and an explicit planning decision says v2 is now the active DMP path.