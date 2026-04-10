# 2026-04-10_WORKFLOW_LAW_AND_TEMPLATE_PACK_REFRESH_CONTRADICTION_REPORT_v1

Status: closed contradiction note retained as evidence for Gate 254. No active pack currently routed.

## Contradiction

The available workflow docs refresh bundle contains an older `repo_updates/AGENTS.md` that would overwrite the later Gate 253 `AGENTS.md` if applied verbatim.

Observed hashes:
- Gate 253 / current repo-root `AGENTS.md`: `2ea30b3ee36ba778d71262dafd4c5b14ce684099c860474891ae3e2754a514a3`
- workflow-bundle `repo_updates/AGENTS.md`: `505e49bc7e6eb5f03912e8a4d843a5ea671fcb669e1e50cafdce3aca922b0011`

Material behavioural conflict:
- the later Gate 253 `AGENTS.md` restores `docs/08_TESTING_AND_PROMOTION.md` into the live read stack and names it as governing testing/promotion doctrine;
- the workflow-bundle `AGENTS.md` drops that restored read-stack item and would therefore regress the later checkpoint-integrity/testing-doctrine authority if applied verbatim.

## Resolution used in Gate 254

- preserve repo-root `AGENTS.md` from Gate 253 unchanged;
- merge the workflow-bundle continuity additions into `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md` instead;
- refresh the tranche briefing template pack to the 2026-04-06 template generation;
- carry the external sidecar note outside the repo as handoff context only.

This is therefore a truthful partial adoption of the workflow docs refresh bundle, not a silent full verbatim replacement.

## Supporting hash note for `docs/06`

- current Gate 254 merged `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`: `024fea2202311045803e7d772f2304feb9bbae40763e30dd15c87c604c8e3505`
- raw workflow-bundle `repo_updates/docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`: `0513bedee68ae1b4d26645bfdefc2e3e18a60630ce1010ad508742bd8a7cd538`

The `docs/06` file is intentionally a merged later state rather than a verbatim workflow-bundle replacement because it preserves the later `docs/08_TESTING_AND_PROMOTION.md` checkpoint-integrity authority while importing the continuity model.
