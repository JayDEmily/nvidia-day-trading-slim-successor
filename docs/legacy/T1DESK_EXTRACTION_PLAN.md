# T1 Desk Legacy Extraction Plan

Date: 2026-03-18  
Source corpus: `My tier 1 desk Lol not GS (1).pdf` (669 pages)

## Purpose

This plan exists to stop the legacy T1 desk corpus being used as one giant conversational blob.

The source file contains three different kinds of value mixed together:
1. screenshot-derived market observations and options tables,
2. candidate features and module ideas,
3. self-criticism, meta-process notes, and guardrail-worthy failure patterns.

The extraction path below separates those layers so the current NVIDIA day-trading repo can absorb the useful parts without importing year-old conversational sludge wholesale.

## Source-handling rule

Treat the PDF as a **legacy evidence corpus**, not as implementation truth.

Each extracted item must carry:
- source document,
- page range,
- extraction confidence,
- whether numeric recomputation is required,
- whether it maps to `raw_vendor`, `canonical_market`, `derived_features`, `research_artefacts`, or `execution_records`.

## Extraction method

### Step 1 - Freeze the source corpus
Read the PDF as a single canonical source and avoid ad hoc re-reading.
Create a page-indexed extraction basis and topic map.

### Step 2 - Separate claims by type
Classify extracted material into:
- raw data claims,
- derived maths claims,
- market-interpretation claims,
- module/playbook claims,
- post-mortem/guardrail claims.

### Step 3 - Recompute formulas, not prose
Do not try to “verify” every sentence.
Recompute only the maths that would influence architecture or runtime logic:
- ladder metrics,
- IV/HV relationships,
- VWAP-relative logic,
- coefficient formulas,
- any score that later becomes a runtime input.

### Step 4 - Extract candidate modules as formal objects
Anything that behaves like a repeatable desk action becomes a structured module candidate with:
- name,
- module class,
- thesis,
- required inputs,
- outputs,
- regime/session dependencies,
- failure modes,
- evaluation notes,
- source pages.

### Step 5 - Extract candidate features separately
Do not force every useful idea into a module.
Session clock features, volatility overlays, options-structure summaries, and cross-market precursors should become feature backlog entries first.

### Step 6 - Extract failure patterns explicitly
Preserve the source document’s own criticism:
- over-attribution,
- retrospective bias,
- screenshot dependence,
- stale data risks,
- plugin/tool failure fallback risks,
- “conversation reality” being mistaken for software reality.

### Step 7 - Map all surviving items into the current repo architecture
Each item must answer:
- which repo layer does it belong to?
- is it a feature, module, doctrine note, or guardrail?
- is it research-only, or a candidate for deterministic runtime?

### Step 8 - Produce machine-readable backlogs
Write:
- `backlog/legacy_module_backlog.jsonl`
- `backlog/legacy_feature_backlog.jsonl`

### Step 9 - Produce human-readable synthesis docs
Write:
- `docs/legacy/T1DESK_VALUE_CAPTURE.md`
- `docs/legacy/T1DESK_FAILURE_PATTERNS.md`
- `docs/legacy/T1DESK_PAGE_MAP.md`

## Pass / fail criteria

The extraction pass is complete when:
1. the source has a page-linked topic map,
2. modules and features have been split into separate JSONL backlogs,
3. failure patterns have been captured as first-class guardrails,
4. each extracted item has provenance and confidence,
5. the repo changelog records the extraction artefacts.

## What this plan does **not** do

- It does not declare any legacy strategy “correct”.
- It does not promote any legacy item directly into the runtime.
- It does not treat screenshot-derived values as canonical data without recomputation.
- It does not assume the old conversation’s “done / wired / committed” language corresponds to real software.

## Immediate outputs from this pass

1. `docs/legacy/T1DESK_PAGE_MAP.md`
2. `docs/legacy/T1DESK_VALUE_CAPTURE.md`
3. `docs/legacy/T1DESK_FAILURE_PATTERNS.md`
4. `backlog/legacy_module_backlog.jsonl`
5. `backlog/legacy_feature_backlog.jsonl`
