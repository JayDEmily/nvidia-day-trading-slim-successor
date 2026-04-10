# Tranche Briefing Template Pack

## Purpose

This folder is the repo-local reference pack for writing future tranche briefs.

The normal pattern is:
- a **planning thread** reads the repo and writes the brief;
- a **coding thread** executes that brief gate by gate on repo-local Git branches.

A second lawful pattern also exists:
- a **controlled continuity execution pack** may authorise a coding thread to carry several gates in sequence without operator relay between each gate, but only when the pack explicitly states the gate sequence, pack-install proof, merge rule, stop conditions, and final router state.

Use this pack when creating a new tranche.
Do not improvise a new planning structure unless the repo doctrine has explicitly changed.
Use the latest closed pack as evidence input only; do not clone its structure forward when the durable template pack already defines the planning grammar.

## What this pack contains

- `2026-04-06_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v3.md`
- `2026-04-06_GENERIC_GATE_TEMPLATE_v3.md`
- `2026-04-06_GENERIC_LEAVES_TEMPLATE_v3.json`
- `2026-04-06_GENERIC_EXECUTION_LOG_TEMPLATE_v2.md`
- `2026-04-06_GENERIC_DOCUMENT_TOUCH_CHECKLIST_TEMPLATE_v2.md`
- `2026-04-06_WORKED_EXAMPLE_CONTROLLED_CONTINUITY_EXECUTION_PACK_SKELETON_v1.md`
- `HOW_TO_USE_THESE_DOCUMENTS.md`

## How to use it

1. Read `HOW_TO_USE_THESE_DOCUMENTS.md` first.
2. Read the repo's normative stack, the permanent process-law doc, active control surfaces, vocabulary authority, and packet/contract authority.
3. Populate the generic gate template, leaves template, execution-log template, and document-touch checklist with repo-specific truth.
4. Write only one active gate master, one active leaves ledger, and one active execution log for the tranche.
5. Choose variable gate and leaf counts that preserve granularity for the actual tranche; do not force a fixed number copied from another pack.
6. Ensure the leaves are closed-world enough that a coding thread can execute them without filling in blanks.
7. Decide explicitly whether the pack is default stop-after-gate or controlled continuity.

## Non-negotiable briefing rules

- Do **not** fill blanks with guesses.
- Do **not** invent new naming without checking the vocabulary authority first.
- Do **not** plan packet or interface work without reading the packet/contract authority first.
- Do **not** plan workflow changes in the abstract; trace the live workflow first.
- Do **not** author a controlled continuity pack unless the gate sequence, merge rule, stop conditions, and final router state are explicit.
- Do **not** leave the execution thread to infer decision-row ownership, allowed fallout repair, or proof widening.
