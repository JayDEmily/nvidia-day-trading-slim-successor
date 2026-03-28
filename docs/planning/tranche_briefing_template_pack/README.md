# Tranche Briefing Template Pack

## Purpose

This folder is the repo-local reference pack for writing future tranche briefs.

The usual pattern is:
- a **planning thread** reads the repo and writes the brief;
- a **coding thread** executes that brief gate by gate.

Use this pack when creating a new tranche.
Do not improvise a new planning structure unless the repo doctrine has explicitly changed.

## What this pack contains

- `2026-03-29_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v2.md`
- `2026-03-29_GENERIC_GATE_TEMPLATE_v2.md`
- `2026-03-29_GENERIC_LEAVES_TEMPLATE_v2.json`
- `2026-03-29_WORKED_EXAMPLE_FINANCIAL_CALENDAR_SKELETON_v2.md`
- `HOW_TO_USE_THESE_DOCUMENTS.md`

## How to use it

1. Read `HOW_TO_USE_THESE_DOCUMENTS.md` first.
2. Read the repo's normative stack, active control surfaces, vocabulary authority, and packet/contract authority.
3. Populate the generic gate template and leaves template with repo-specific truth.
4. Write only one active gate master and one active leaves ledger for the tranche.
5. Ensure the leaves are granular enough that a coding thread can execute them without filling in blanks.

## Non-negotiable briefing rules

- Do **not** fill blanks with guesses.
- Do **not** invent new naming without checking the vocabulary authority first.
- Do **not** plan packet or interface work without reading the packet/contract authority first.
- Do **not** plan workflow changes in the abstract; trace the live workflow surfaces first.
- Do **not** let a rich upstream source be collapsed back into legacy thin compatibility surfaces unless that collapse is an explicit, bounded runtime derivation.
- Do **not** treat a gate as done without green tests, synchronized control-surface updates, and a fresh full-history zip from the exact green repo state.

## Why this exists

This pack exists to reduce drift between:
- the repo's intent;
- the planning brief;
- the leaves ledger;
- the code that eventually gets written.

Git history preserves older brief packs, so the active repo tree should prefer the latest usable template rather than a clutter pile of superseded planning notes.
