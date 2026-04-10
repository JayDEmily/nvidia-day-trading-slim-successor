# 2026-04-06 Gate 210 Slim Active-Repo Cutover Entry Criteria

## Purpose

Define the exact boundary for the later slim active-repo creation and substantive test-audit work without starting that successor execution in Gate 210.

## Already complete upstream

- Gates 200-205 closed the target-repo admitted-evidence successor pack and froze the planning-to-coding handoff boundary.
- Gates 206-210 closed the workflow-hardening and active-repo reset foundation pack.
- The repo router, doctrine stack, template pack, planning/evidence taxonomy, operator-facing README guidance, and Makefile proof guidance now align with the hardened GitHub-native workflow.
- GitHub branch, commit, and merge history is the routine execution ledger, while `PLANS.md`, the canonical gate map, the active-or-closed leaves ledger, and the execution log remain the repo control surfaces.

## Entry criteria before any slim-repo cutover starts

The later slim active-repo successor work may start only when all of the following are true:

1. Gate 210 has been merged to `main` and the merge receipt is recorded.
2. Repo-root `PLANS.md` routes no active pack in this source repo.
3. The workflow-hardening pack is closed through Gate 210 in the canonical gate map, leaves ledger, and execution log.
4. The exact source commit to cut from has been frozen on `main`.
5. No additional runtime, schema, DB, API, or governance-pack changes are mixed into that cutover source commit.
6. The operator explicitly decides that the current repo remains the archive/evidence host and that the slim successor will become the new active execution repo.

If any one of those is false, the slim-repo successor work has not started yet.

## What must be frozen before the cutover

- The source repo must remain the intact evidence host for the closed planning packs, receipts, contradiction reports, scope notes, and other retained planning artefacts.
- The cutover source commit must be one exact merged `main` commit, not a moving work branch target.
- The live doctrine stack for the successor repo must already be frozen in this repo:
  - `docs/01_NORMATIVE.md`
  - `docs/02_OPERATING_MODEL.md`
  - `docs/03_DOMAIN_MODEL.md`
  - `docs/04_TECHNICAL_ARCHITECTURE.md`
  - `docs/05_GUARDRAILS.md`
  - `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
  - `docs/08_TESTING_AND_PROMOTION.md`
  - `AGENTS.md`
- No new active planning pack may be opened in this repo to sneak the cutover work in early.

## What the slim active-repo successor should contain

The later slim successor should contain only the surfaces needed for live ongoing execution and the next substantive audit pack, including:

- runtime code and supporting repo-native build surfaces required to run, test, and evolve the product;
- the frozen doctrine stack that still governs live work;
- the current operator-facing onboarding and Makefile guidance;
- the minimum planning/router surfaces needed to open the next active pack inside the slim repo;
- the tests, fixtures, and support artefacts that remain in scope for the successor repo's substantive audit and ongoing runtime work.

The slim successor should not inherit the full historical planning tree as active material.

## What stays behind as archive and evidence

The current repo remains the archive/evidence host for:

- closed planning packs under `docs/planning/`;
- closed execution logs, closeout receipts, contradiction reports, scope notes, salvage matrices, indexes, and cross-reference notes;
- historical patch, zip, and provenance artefacts already retained here;
- any planning material that is informative or evidentiary rather than required for ongoing active execution.

## What the first pack in the slim repo is expected to do

The first pack in the slim repo is expected to:

1. confirm the imported slim repo matches the frozen source-cut commit and doctrine stack;
2. inventory the retained runtime and operator surfaces that actually moved into the slim repo;
3. perform the substantive test-audit classification work that Gate 210 explicitly deferred;
4. decide, with evidence, which tests are kept, retired, rewritten, or moved without pretending those decisions were already made here;
5. open the next active pack inside the slim repo rather than reusing this repo's closed workflow-hardening pack.

## What must not be claimed as already executed

Do not claim any of the following as already done:

- the slim active-repo successor has been created;
- files have already been copied, deleted, or promoted into the successor repo;
- the substantive test-audit pack has already run;
- keep/retire/rewrite decisions for the test inventory have already been made;
- `07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER` substantive work has started;
- any downstream runtime, schema, packet, DB, or API changes were executed as part of Gate 210.

## Boundary summary

Gate 210 closes the current governance-hardening pack and defines the successor-cut criteria.
It does not create the slim repo, does not start the successor pack, and does not execute the substantive test audit.
