# 2026-03-23 Canonical Desk Rebuild Execution Plan

Status: Historical completed rebuild plan
Version: v1.2
Authority: Subordinate to `docs/01_NORMATIVE.md`; retained as completed rebuild evidence and no longer active under `PLANS.md`.

## Execution status

- Gates 0 through 6 are complete on `main`.
- The sequential leaf cycle was executed on work branches and merged to `main` one leaf at a time.
- Future work will begin from this canonical completion baseline without reviving shortcut completion claims.

## 0. Purpose

This plan will drive the canonical rebuild of the NVDA desk system.

This plan will turn the preserved module universe, the completed Phase A corpus-bounded recovery work, and the incoming real-data corpus into one deterministic rebuild programme.

This plan will govern:
- normative alignment;
- desk cognition grammar formalisation;
- module and feature import from every recovered source form;
- architecture mapping;
- contract-first reintroduction;
- real-data ingestion preparation;
- replay, calibration, and comparison scaffolding.

This plan will not be treated as aspiration. This plan will be treated as executable doctrine.

## 1. Binding doctrine

1. The system will be rebuilt from the point of view of a human operating a tier-1 desk.
2. Runtime decision-making will not depend on LLMs.
3. The Makefile will remain the single operational front door for normal developer workflows.
4. Normative documents will control architecture, contracts, and authority hierarchy.
5. No code path will bypass posture and risk permission.
6. No valuable recovered idea will be discarded during import planning.
7. Recovered ideas will not all be promoted into live runtime code immediately.
8. Every module, classifier, feature family, overlay, and review artefact will be placed into the Desk Cognition Grammar before broad implementation.
9. Every new or refactored Python module will contain clear docstrings that state purpose, required inputs, produced outputs, and deterministic behaviour.
10. Package and folder organisation will remain explicit, stable, and reviewable.
11. Legacy code will be translated into the current architecture. Legacy code will not be copied blindly.
12. Gatsby, UI, Markdown, YAML, JSON, backlog, and archive artefacts will be treated as recoverable source material. They will not be treated as runtime code until they are translated into contracts and implementations.
13. Another thread is aggregating real market and options data. That corpus will be treated as an incoming upstream dependency. This plan will prepare the system to ingest it and use it deterministically when it lands.
14. Phase A is complete for the currently attached recoverable corpus and will remain corpus-bounded until new source material arrives.
15. Every implementation decision will be judged through the human desk lens: what does the trader need to know, what decision becomes eligible, what risk becomes unacceptable, and what action becomes valid.

## 2. Desk Cognition Grammar

The system will reason in this fixed order:

1. Temporal Context
   - session date
   - time of day
   - session phase
   - expiry proximity
   - event proximity
   - what changed in the recent path
2. Market Regime Context
   - beta state
   - sector and semis leadership
   - breadth and concentration
   - volatility regime
   - rates and FX pressure
   - cross-asset stress
3. Options and Flow Context
   - term structure
   - implied versus realised state
   - skew state
   - gamma and dealer state
   - strike concentration and pin risk
   - flow imbalance and squeeze conditions
4. Posture and Risk Permission
   - allowed
   - derisk
   - block
   - no-overnight
   - deployable capital cap
   - inventory-aware constraints
5. Playbook Eligibility
   - which playbooks are eligible now
   - which playbooks are invalid now
   - which playbooks are watch-only
6. Expression and Execution
   - entry shape
   - laddering
   - sizing
   - scaling
   - hedge requirements
   - exit rules
7. Review and Explanation
   - why the system acted
   - why the system did not act
   - which modules governed the decision
   - which conflicts and vetoes were active

No module will be implemented outside this grammar.

## 3. Source forms that will be imported

The import programme will cover every recovered source form:
- Python modules
- partial Python modules
- Gatsby or UI artefacts
- YAML specifications
- JSON and JSONL registries
- backlog rows
- Markdown design fragments
- dated handover notes
- archive extracts
- synthetic harness artefacts that still carry decision value

Each recovered item will become one of the following:
- implemented runtime module
- implemented feature family
- implemented classifier
- implemented risk or posture gate
- implemented execution component
- review or explanation component
- preserved concept-contract pending dependency completion
- preserved evidence-only artefact

No recovered item will be silently dropped.

## 4. Gate structure

### Gate 0 — Normative alignment

This gate will reconcile the authority docs before broad build work.

This gate will:
- audit `docs/01_NORMATIVE.md`, `docs/02_OPERATING_MODEL.md`, `docs/03_DOMAIN_MODEL.md`, `docs/04_TECHNICAL_ARCHITECTURE.md`, `docs/05_GUARDRAILS.md`, `docs/08_TESTING_AND_PROMOTION.md`, `README.md`, `AGENTS.md`, and `PLANS.md`;
- remove conflicts, stale language, and ambiguity;
- align terminology around module, feature, classifier, overlay, gate, playbook, and review artefact;
- define mandatory docstring requirements;
- define canonical package and folder rules;
- define contract placement and naming rules;
- reset downstream gate status to blocked until sequential execution resumes from `main`.

Gate 0 pass criteria:
- all audited docs agree on authority, terminology, and execution order;
- downstream gate status is truthfully reset in `PLANS.md`, the execution plan, the leaf ledger, and the execution log;
- absolute execution wording is preserved across all audited docs.

No implementation leaf beyond Gate 0 will begin before Gate 0 passes and is merged to `main`.

### Gate 1 — Canonical universe import

This gate will turn the preservation pack and corpus-bounded Phase A surface into one canonical import registry.

This gate will:
- merge module, feature, and desk-cognition records into one importable universe;
- preserve provenance;
- assign canonical identifiers;
- assign maturity state;
- assign source-form type;
- assign required upstream inputs and intended downstream outputs.

Gate 1 pass criteria:
- the registry covers the full corpus-bounded universe with no-loss evidence;
- the registry is the only canonical import surface for downstream gates;
- no runtime completion claim is made for concept-contract or evidence-only items.

### Gate 2 — Grammar and architecture mapping

This gate will map every canonical item into:
- the Desk Cognition Grammar;
- the current technical architecture;
- the eventual runtime target.

This gate will define what is raw input, derived state, classifier, posture gate, playbook qualifier, execution component, or review component.

Gate 2 pass criteria:
- every canonical item has one grammar role and one architecture role;
- no orphan canonical item remains;
- evidence-only items terminate outside active runtime completion counts.

### Gate 3 — Contract-first runtime scaffold

This gate will add or revise the runtime scaffold so that imported items can be reintroduced cleanly.

This gate will:
- define common module interfaces;
- define contract schemas;
- define registries and loaders;
- define trace and explanation packets;
- define import surfaces for real-data datasets;
- enforce docstring standards in code review and tests.

Gate 3 pass criteria:
- runtime contracts and loaders are deterministic and traceable;
- every touched public module has docstrings;
- the full repo suite passes in the repo venv.

### Gate 4 — Desk-order import tranches

Recovered items will be implemented or refactored in this order:
1. temporal context
2. market regime context
3. options and flow context
4. posture and risk permission
5. playbook eligibility
6. expression and execution
7. review and explanation

No lower-order tranche will leapfrog a higher-order tranche.

Gate 4 pass criteria:
- each tranche increases the implemented-runtime depth for its grammar role;
- each tranche adds targeted tests that cover positive and negative paths;
- tranche completion will not be claimed on scaffold existence alone.

### Gate 5 — Real-data integration scaffold

This gate will prepare the system to ingest the real-data corpus being assembled in another thread.

This gate will:
- define dataset schemas;
- define import commands;
- define storage and provenance expectations;
- define replay-ready canonical formats for bars, options chains, events, and auxiliary state.

Gate 5 pass criteria:
- the runtime consumes a typed real-data bundle rather than validating one in isolation;
- provenance survives ingestion;
- options-chain state enters the Desk Cognition Grammar through typed contracts.

### Gate 6 — Replay, calibration, and comparison harness

This gate will prepare the system for deterministic evaluation and coefficient tuning.

This gate will:
- run replay on real and synthetic data under what-was-known-then rules;
- support coefficient and sub-coefficient tuning;
- support stack and playbook comparison without brute-force combinatorial sludge;
- measure calibration, stability, veto quality, deployable capital discipline, and explanation quality.

Gate 6 pass criteria:
- replay uses module weights and sub-coefficients in runtime evaluation rather than leaving them dormant;
- comparison operates on explicit stack definitions;
- walk-forward discipline and holdout discipline are encoded in the harness.

## 5. Workstreams

### Workstream A — Normative and organisational alignment

This workstream will:
- reconcile doctrine;
- update root and planning docs;
- lock naming and folder rules;
- lock docstring rules;
- define contract locations.

### Workstream B — Canonical import registry

This workstream will:
- ingest `nvda_module_preservation_pack_20260322.zip` outputs;
- ingest the corpus-bounded Phase A canonical universe;
- merge modules, features, and desk-cognition fragments;
- produce one canonical import registry and one canonical grammar mapping.

### Workstream C — Runtime scaffold and contracts

This workstream will:
- create or revise common module interfaces;
- create registries and loaders;
- add deterministic explanation packets;
- add test harness support for imported components.

### Workstream D — Module and feature reintroduction

This workstream will:
- translate legacy or conceptual artefacts into the runtime;
- refactor surviving code where useful;
- leave preserved concept-contracts in place where runtime implementation is blocked by missing dependencies.

### Workstream E — Real-data ingestion preparation

This workstream will:
- formalise ingestion schemas and loaders for the incoming real-data corpus;
- ensure options data becomes first-class and does not remain a secondary overlay;
- support replay and calibration when the real corpus lands.

### Workstream F — Replay and calibration discipline

This workstream will:
- support repeated deterministic runs;
- support coefficient and sub-coefficient tuning;
- support playbook comparison at the stack-definition level;
- reject brittle stacks even when in-sample metrics look attractive.
