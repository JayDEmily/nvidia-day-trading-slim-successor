# Tranche Briefing Template Pack

## Purpose

This folder is the repo-local reference pack for writing future tranche briefs.

The usual pattern is:
- a **planning thread** reads the repo and writes the brief;
- a **coding thread** executes that brief gate by gate on repo-local Git branches.

Use this pack when creating a new tranche.
Do not improvise a new planning structure unless the repo doctrine has explicitly changed.
Use the latest closed pack as evidence input only; do not clone its structure forward when the durable template pack already defines the planning grammar.

## What this pack contains

- `2026-03-29_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v2.md`
- `2026-03-29_GENERIC_GATE_TEMPLATE_v2.md`
- `2026-03-29_GENERIC_LEAVES_TEMPLATE_v2.json`
- `2026-03-29_WORKED_EXAMPLE_FINANCIAL_CALENDAR_SKELETON_v2.md`
- `2026-03-30_GENERIC_EXECUTION_LOG_TEMPLATE_v1.md`
- `2026-03-30_GENERIC_DOCUMENT_TOUCH_CHECKLIST_TEMPLATE_v1.md`
- `HOW_TO_USE_THESE_DOCUMENTS.md`

## How to use it

1. Read `HOW_TO_USE_THESE_DOCUMENTS.md` first.
2. Read the repo's normative stack, the permanent process-law doc, active control surfaces, vocabulary authority, and packet/contract authority.
3. Populate the generic gate template, leaves template, execution-log template, and document-touch checklist with repo-specific truth.
4. Write only one active gate master, one active leaves ledger, and one active execution log for the tranche.
5. Choose variable gate and leaf counts that preserve granularity for the actual tranche; do not force a fixed number copied from another pack.
6. Ensure the leaves are granular enough that a coding thread can execute them without filling in blanks.

## Non-negotiable briefing rules

- Do **not** fill blanks with guesses.
- Do **not** invent new naming without checking the vocabulary authority first.
- Do **not** plan packet or interface work without reading the packet/contract authority first.
- Do **not** plan workflow changes in the abstract; trace the live workflow surfaces first.
- Do **not** let a rich upstream source be collapsed back into legacy thin compatibility surfaces unless that collapse is an explicit, bounded runtime derivation.
- Do **not** skip the document-touch checklist.
- Do **not** ignore material control-surface contradictions; emit a contradiction report before continuing.
- Do **not** let `completed_leaf_ids` and `remaining_leaf_ids` overlap.
- Do **not** treat a multi-gate user request as permission to skip per-gate closeout.
- Do **not** treat a gate as done without green tests, synchronized control-surface updates, and GitHub branch/commit receipts recorded in the execution log.
- Do **not** treat routine zip packaging as the default execution ledger; create a full-history zip only when the operator explicitly requests backup, offline handoff, or sandbox transfer packaging.

## Why this exists

This pack exists to reduce drift between:
- the repo's intent;
- the planning brief;
- the leaves ledger;
- the code that eventually gets written.

Git history preserves older brief packs, so the active repo tree should prefer the latest usable template rather than a clutter pile of superseded planning notes. GitHub branch, commit, and merge history is the default routine execution ledger for ordinary gate work.


## Execution-thread reminder

When a planning pack becomes active, the coding thread must reread the vocabulary authority and the packet/data contract authority named in that pack before implementing the approved gate.

## Research-thread reminder

When the operator is brainstorming or researching a new tranche, the planning thread should pursue candidate edge and asymmetry first, then label implementation readiness only if the operator asks for current-state, promotion, or live-operability judgment.
