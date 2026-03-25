# NVIDIA Day Trading Project v1
**Date:** 2026-03-18  
**Status:** Canonical working draft  
**Scope:** Whole-system operating model  
**Supersedes:** `NVIDIA_day_trading_project_architecture_brief.md`

## 1. Why this document exists

This document freezes the top-level operating model for the NVIDIA day trading project.

It does **not** freeze final parameter values. It freezes:
- the project purpose;
- the role split between human, GPT, database, and deterministic runtime;
- the promotion path from research to software;
- the two delivery modes:
  - API-first now;
  - ChatGPT/MCP later, when the account/surface supports it cleanly.

The project is a **single-operator, tier-one-desk-inspired research and playbook platform** focused on NVIDIA and its surrounding market state.

The desk discipline is the thing to copy. The headcount is not.

## 2. Project statement

Build a durable market-state warehouse and research workflow for NVDA day trading that:
- stores market data and account/execution state outside the chat thread;
- lets GPT reason over compact retrieved slices of that state;
- converts repeated insights into versioned deterministic modules;
- evaluates those modules via replay, backtest, and paper trading;
- promotes only approved modules into a non-LLM execution stack.

The model is a research partner and playbook compiler.
The model is **not** the execution engine.

## 3. The actual system you are building

There are really **three** systems, not one.

### 3.1 System A — Market-state memory
This is the durable memory of the desk.

It stores:
- raw vendor feeds;
- canonical market facts;
- derived features;
- event/calendar labels;
- account/risk state snapshots;
- order, fill, and ledger records;
- research artefacts.

### 3.2 System B — GPT research cockpit
This is the human + GPT operating surface.

It lets you:
- inspect current and historical market state;
- compare analogous sessions and regimes;
- discuss candidate strategies;
- design or revise modules;
- save hypotheses, notes, playbook entries, and structured artefacts.

### 3.3 System C — Deterministic runtime
This is the execution side.

It:
- loads approved modules only;
- calculates signals and vetoes;
- applies risk and broker constraints;
- runs paper or live logic;
- records all orders, fills, exceptions, and attribution.

GPT does not sit in this runtime loop.

## 4. The human / GPT boundary

### 4.1 What GPT is allowed to do
GPT may:
- read compact retrieved market and research state;
- read event/news context when useful;
- compare regimes, sessions, and setups;
- propose module designs;
- critique overfitting and bad reasoning;
- write structured artefacts;
- help explain post-trade behaviour;
- propose code scaffolds and test plans.

### 4.2 What GPT is not allowed to do
GPT must not:
- connect directly to the production database;
- issue arbitrary write queries;
- submit live orders;
- bypass the deterministic risk gateway;
- auto-promote a strategy into the execution stack.

### 4.3 Human responsibilities
You remain responsible for:
- choosing the research direction;
- approving module promotion;
- approving paper/live eligibility;
- setting risk policy values;
- deciding when a module is paused, retired, or revised.

## 5. Design principles

1. **SQL does the storage and retrieval work.**  
   Numeric work belongs in the database and deterministic code, not in chat context.

2. **The thread is not the database.**  
   Chat is for reasoning. The warehouse is for facts.

3. **Freeze contracts now, tune numbers later.**  
   Parameter values remain configurable; schemas and interfaces do not.

4. **Prefer vendor-agnostic canonical data.**  
   IBKR is an input boundary, not the shape of the whole system.

5. **Modules are formal objects, not vibes.**  
   Every module must conform to a machine-readable contract.

6. **Promotion must be gated.**  
   Research ideas only become runtime logic after deterministic checks.

7. **Execution is a separate safety domain.**  
   Research flexibility is acceptable. Execution ambiguity is not.

8. **Post-trade learning is mandatory.**  
   A module without attribution and review is an unfinished module.

## 6. Two delivery modes

### 6.1 Mode A — API-first now
You operate through your own backend and a thin client/chat UI.

Use this now because:
- it gives you full control;
- it does not depend on ChatGPT-side product readiness;
- it lets the backend and data model mature independently.

### 6.2 Mode B — ChatGPT + MCP later
When the ChatGPT surface you use supports the workflow cleanly, the same backend is exposed via MCP tools and optional widgets.

The backend remains the real product.
ChatGPT becomes an alternative client, not the source of truth.

## 7. Data layer taxonomy

Use five layers. This matters.

### 7.1 `raw_vendor`
Exactly what the broker/vendor provides, even if the vendor has already computed part of it.

Examples:
- IBKR watchlist ticks;
- historical bars;
- option computation bundles;
- broker account snapshots;
- order-status events.

### 7.2 `canonical_market`
Normalised market facts, independent of vendor quirks.

Examples:
- instrument master;
- one-minute bars;
- bid/ask snapshots;
- option contract master;
- session segmentation;
- event labels.

### 7.3 `derived_features`
Everything the platform computes for analysis.

Examples:
- VWAP and VWAP deviation;
- opening-range metrics;
- realised volatility windows;
- IV and skew summaries;
- gamma- or dealer-position proxies;
- cross-market precursor summaries;
- regime labels.

### 7.4 `research_artefacts`
What GPT and you produce together.

Examples:
- hypotheses;
- notes;
- playbooks;
- structured module specs;
- evaluation memos;
- code snippets.

### 7.5 `execution_records`
What the deterministic runtime produces.

Examples:
- signal emissions;
- veto decisions;
- risk blocks;
- orders, fills, cancels;
- capital allocation changes;
- daily P&L and attribution.

## 8. What the project is **not**

It is not:
- a giant general-purpose trading platform;
- an HFT engine;
- an autonomous LLM trader;
- a news-sentiment toy;
- a monolithic “predict the market” model;
- a prompt-heavy replacement for proper data engineering.

## 9. The desk model being emulated

The desk you are emulating behaves roughly like this:

- build a picture of market state before the U.S. open;
- incorporate overnight and precursor context;
- understand whether the day resembles a known regime;
- check which playbook modules are relevant;
- block bad states quickly;
- size only after risk and broker rules pass;
- execute deterministically;
- review not only signal quality, but execution quality and stack interaction.

That is the adult version of the project.

## 10. Module model

A module is a versioned desk behaviour.

Modules fall into four classes:
- **signal** — detects a setup;
- **veto** — blocks trading in bad states;
- **sizing** — determines exposure;
- **execution** — controls entry/exit tactics.

A module may be:
- intraday;
- overnight;
- weekend;
- event-driven.

A module is not “live” because it had a good chat. It is live only after passing promotion gates.

## 11. Promotion lifecycle

There are two meanings of lifecycle. Keep them separate.

### 11.1 Trade-horizon lifecycle
How long the position may be held:
- intraday;
- overnight;
- weekend;
- event carry.

### 11.2 Promotion lifecycle
How the idea matures:
1. research conversation;
2. formal spec;
3. deterministic implementation;
4. bug-gated;
5. replay/backtest evaluated;
6. paper-trade evaluated;
7. approved into the active playbook stack;
8. paused / revised / retired as needed.

## 12. Research workflow

### 12.1 Pre-market
The operator uses GPT to:
- retrieve overnight state;
- inspect precursor markets;
- inspect calendar and known event context;
- compare today against analogous historical sessions;
- review the currently approved playbook stack;
- identify whether new research is warranted.

### 12.2 Intraday
The operator may:
- inspect how current state differs from expectations;
- ask GPT to compare live conditions with earlier analogous sessions;
- design a new candidate module or revise thresholds conceptually;
- save research artefacts.

GPT can inform. GPT does not execute.

### 12.3 Post-market
The operator reviews:
- what fired and what was vetoed;
- whether execution degraded the edge;
- whether the module stack interacted well;
- what needs to be tuned, paused, promoted, or killed.

### 12.4 Weekend / deep research
This is where new modules are born:
- cluster historical sessions;
- analyse specific failure weeks or blip days;
- design candidate modules;
- codify and evaluate them.

## 13. Why options data matters in this project

The project does not rely on an LLM to tell you how to “feel” about the news.
The idea is that options and volatility state often act as a compressed market reaction function.

That said, event labels still matter.
You do not need sprawling NLP ingestion for v1, but you do want structured labels for things like:
- earnings;
- CPI / FOMC / NFP;
- major company events;
- exchange halts or market-wide shocks.

Use minimal structured event metadata, not a theatre production of market commentary.

## 14. Risk and broker reality

VIX and VVIX are useful market-risk inputs.
They are not a complete risk gateway.

The real system must also model:
- max trade risk;
- max daily loss;
- gross and net exposure constraints;
- broker buying-power and PDT constraints;
- settled-cash / account-state constraints where relevant;
- stale or corrupt data;
- duplicate order prevention;
- exchange-halt / reject-storm states;
- manual and automatic kill-switch conditions.

This project becomes realistic only when market-risk logic and broker/regulatory logic both exist.

## 15. The two-system bridge

The bridge from GPT research to deterministic execution is a **versioned artefact**, not a direct action.

In plain English:
- GPT and you discuss a strategy;
- the result becomes a structured module spec;
- code is generated or updated to satisfy that spec;
- the module is evaluated;
- only then may it enter paper trading or live eligibility.

There is no direct “GPT said buy” path.

## 16. Minimum viable v1

The first production slice is deliberately narrow.

### 16.1 Focus
- primary symbol: NVDA;
- one-minute bars as the main canonical resolution;
- bounded options strip around spot and near expiries;
- market context for a small set of benchmark and peer instruments;
- minimal structured event/calendar labels;
- deterministic paper-trade-capable runtime.

### 16.2 Explicitly defer
- full-market ingestion;
- full-depth order book everywhere;
- broad news/NLP pipelines;
- full multi-broker support;
- institutional OMS/EMS sprawl;
- full live-capital autonomy.

## 17. Recommended operator workflow

### Morning
1. Load desk briefing.
2. Inspect overnight state and precursor context.
3. Review event labels and known catalysts.
4. Review approved module stack for today.
5. Decide whether any module should be disabled, emphasised, or left unchanged.

### During market
1. Monitor deterministic system output.
2. Use GPT for explanation, comparison, and anomaly inspection.
3. Save notable observations and candidate module ideas.
4. Do not bypass risk controls because the chat felt persuasive.

### After market
1. Review fills, slippage, blocks, and missed opportunities.
2. Review module contribution and veto contribution.
3. Decide whether to tune, promote, pause, or retire modules.
4. Archive the day’s reasoning and execution artefacts.

## 18. Document hierarchy from here

This master document is the human-readable operating model.

It should be paired with:
- a **technical architecture document**;
- a **build plan / gated implementation plan**;
- the actual project scaffold and `pyproject.toml`.

## 19. Canonical decisions frozen by this pass

These decisions are now frozen unless new evidence forces a change:
- PostgreSQL is the system of record.
- Python 3.13 is the project runtime.
- GPT is upstream research/design, not downstream execution.
- The project has two client modes: API-first now, MCP/ChatGPT later.
- Data is layered as raw vendor → canonical market → derived features → research artefacts → execution records.
- Modules are typed objects and pass through promotion gates.
- The architecture must support replay, audit, and post-trade attribution.

## 20. Outstanding work that is intentionally **not** frozen yet

These remain configuration or later-design questions:
- exact instrument list and option strip bounds;
- exact threshold values;
- exact coefficient values;
- final event taxonomy;
- final evaluation score thresholds for promotion;
- live-capital operating policy.

That is fine.
Those are variables, not blockers.

## 21. Source inputs reviewed for this version

Reviewed in full for this pass:
- `NVIDIA_day_trading_project_architecture_brief.md`
- `gpt_action_sql_database.md`
- `gpt_action_sql_database.ipynb`
- `data-retrieval.md`
- `structured-outputs.md`
- `latest-model.md`
- the full conversation in this thread through 2026-03-18

## 22. Bottom line

You were not heading in the wrong direction.

The concept is now mature enough.
The next job is not “more idea”.
The next job is freezing contracts, building the scaffold, and getting the research-to-runtime promotion path into software.
