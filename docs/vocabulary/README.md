# Vocabulary Governance

This folder governs canonical repo language after the architecture is pinned.

## What this is for

- keep one term meaning one thing;
- keep aliases explicit rather than accidental;
- stop stale `session_clock`-era labels or duplicate playbook labels from drifting back in;
- preserve the difference between raw primitives, derived features, stage labels, family labels, setup variants, execution expressions, and workflow-routing concepts such as Step 0 calendar/horizon and carry handoff.

## What this is not for

- not a blind merge target for stale harvested vocabulary payloads;
- not a runtime redesign surface;
- not a free-form glossary detached from typed contracts.

## Authoritative artefacts

- workflow: `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- canonical vocabulary file: `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- Gate 55 alignment note: `docs/planning/2026-03-26_GATE55_VOCABULARY_GOVERNANCE_ALIGNMENT.md`
- schema: `src/nvda_desk/schemas/vocabulary.py`
- generator: `scripts/build_canonical_vocabulary.py`
