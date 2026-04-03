# 2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_SCOPE_NOTE_v1

## Purpose

Carry the bounded truth split for the uploaded options findings report and freeze the execution boundaries for the repair tranche.

## Verified evidence inputs

- clean repo baseline: `repo_template_pack_governance_repair_main_fullgit_2026-04-03.zip`
- findings report: `nvda_options_trace_findings_report_2026-04-03.md`

## Findings truth split carried into this pack

### Confirmed bugs to repair in this tranche
- F1: IV unit contract inconsistency across runtime preparation, fixtures, and standalone options-context tests
- F4: dominant-strike and strike-cluster ranking become order-dependent when weighting truth is absent or zero

### Confirmed defect to repair in this tranche
- F2: persisted/API raw option-surface contract is weaker than the replay/runtime option-quote contract used by the loader

### Capability gap to address in this tranche
- F3: the packet cannot express surface-anchor divergence versus live spot; this is treated as a bounded feature addition, not as proof that current behaviour is already wrong

### Explicitly out of scope
- F5: workbook doctrine as raw-runtime replacement. Keep workbook surfaces as evidence input only.

## Non-negotiable tranche boundaries

- Do not treat the findings report as biblical authority. It is evidence input plus opinion; current repo truth still decides.
- Do not compress F1, F2, F3, and F4 into one vague code-fix gate.
- Do not introduce a second options engine or a shadow playbook selector while adding the surface-anchor divergence feature.
- Do not widen workbook doctrine into runtime truth.
- Do not blur raw-row API/persistence parity with reduced consumer-facing payloads; if both exist, name them honestly.

## Expected execution order

1. Gate 181 installs the pack and freezes the findings truth split.
2. Gate 182 fixes the IV unit contract.
3. Gate 183 aligns persisted/API raw option surfaces with runtime contract truth.
4. Gate 184 makes dominant-strike / cluster inference fail closed when weights are absent.
5. Gate 185 adds the bounded surface-anchor divergence feature end to end.
6. Gate 186 runs final proofs, closes the router surfaces honestly, and packages the repo.

## Unknown / not yet verified

- Gate 183 required a schema migration so raw option-surface persistence could lawfully carry `iv`, `delta`, and `gamma`.
- Gate 185 froze `surface_anchor_to_spot_pct` as the bounded schema-field name for the derived divergence feature. No canonical vocabulary-file amendment was required because no new stage/family/playbook taxonomy term was introduced.
- prepared real-data fixtures required regeneration so the lawful Gate 185 derived field could be carried in the checked-in prepared-runtime pack.
