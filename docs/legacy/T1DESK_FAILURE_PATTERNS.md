# T1 Desk Legacy Failure Patterns

Source: `My tier 1 desk Lol not GS (1).pdf`

## Purpose

Capture the recurrent mistakes and fragility patterns in the legacy corpus so the current repo can turn them into guardrails, evals, and anti-regression doctrine.

## Failure patterns

### FP-001 - Screenshot dependence
**Pattern**  
Critical market observations are driven by screenshots and conversational reconstruction rather than canonical stored data.

**Why it is dangerous**  
- weak provenance,
- OCR/transcription drift,
- hard to replay deterministically,
- impossible to audit cleanly later.

**Guardrail now**  
No runtime or formal feature may rely on screenshot-only data.
Screenshots are research aids only.

**Source ranges**  
Pages 1-70, 330-345, 539-545

---

### FP-002 - Conversation reality mistaken for software reality
**Pattern**  
The source repeatedly uses language that sounds implementation-real:
- “done”,
- “wired”,
- “in the stack”,
- “logged and committed”.

**Why it is dangerous**  
It creates false confidence that architecture or code already exists when it may only exist in the conversation.

**Guardrail now**  
Only files, tests, migrations, routes, and machine-readable artefacts count as implementation evidence.

**Source ranges**  
Recurring throughout; especially pages 620-636 and late recap ranges 655-658

---

### FP-003 - Over-attribution from options structure
**Pattern**  
Options pressure, skew, and IV moves are sometimes read as stronger directional evidence than is justified.

**Why it is dangerous**  
Options can reflect hedging, dealer positioning, or vol demand rather than clean directional intent.

**Guardrail now**  
Options-derived reads must be treated as features and hypotheses, not conclusions.
Replay and attribution must test whether they improved decisions.

**Source ranges**  
Pages 1-6, 25-60, 330-345, 540-560

---

### FP-004 - Manually modelled Greeks without deterministic provenance
**Pattern**  
The document manually reconstructs Greek layers and support/resistance logic from screenshots and conversational estimates.

**Why it is dangerous**  
Even if directionally sensible, it is not robust enough for runtime use without deterministic recomputation.

**Guardrail now**  
Any manually modelled Greek or volatility statistic requires a reproducible formula and source inputs before reuse.

**Source ranges**  
Pages 330-345

---

### FP-005 - Layer mixing
**Pattern**  
Raw observations, vendor-derived values, derived features, human inference, and module logic sit in one blended conversational soup.

**Why it is dangerous**  
This makes it impossible to know what belongs in data storage, what belongs in derived features, and what belongs only in research narrative.

**Guardrail now**  
Every extracted item must map to one repo layer:
`raw_vendor`, `canonical_market`, `derived_features`, `research_artefacts`, `execution_records`.

**Source ranges**  
Recurring throughout the document

---

### FP-006 - Tool / connector failure leading to ad hoc manual fallback
**Pattern**  
When plugins or connectors fail, the conversation falls back to manual construction and narrative continuity.

**Why it is dangerous**  
Manual fallback can be useful for brainstorming but unsafe for authoritative outputs.

**Guardrail now**  
Connector failure should surface as:
- degraded confidence,
- blocked runtime promotion,
- explicit “manual-only” status for any affected artefact.

**Source ranges**  
Pages 217, 330

---

### FP-007 - Overfitting risk in a large module space
**Pattern**  
The source recognises 40+ modules, multiple coefficients, and a huge combinatorial search space.

**Why it is dangerous**  
Without disciplined evals, this becomes a perfect machine for curve-fitting noise.

**Guardrail now**  
Use walk-forward / expanding-window validation, module-family constraints, and attribution rules before promotion.

**Source ranges**  
Pages 156-159

---

### FP-008 - Qualitative source contamination
**Pattern**  
The source repeatedly notes the need to pass Bloomberg/news/qualitative market chatter through a “bullshit filter”.

**Why it is dangerous**  
Narrative sources can over-dominate the state read and contaminate deterministic logic with theatre.

**Guardrail now**  
Keep qualitative context in the research layer unless it is converted into a bounded, typed event label.

**Source ranges**  
Page 338 and macro commentary sections around 258-340

---

### FP-009 - Stale-data risk during peak volatility
**Pattern**  
The source explicitly notes stale options data during fast conditions.

**Why it is dangerous**  
Good logic on stale state is still bad execution.

**Guardrail now**  
Runtime paths need freshness checks and stale-data vetoes.

**Source ranges**  
Pages 335-345

---

### FP-010 - Hard-coded logic temptation
**Pattern**  
Late in the document, the conversation starts formatting structured outputs that look like a hard-coded rule engine.

**Why it is dangerous**  
It betrays the original goal of modelling a fluid desk-style hierarchy rather than a brittle static template.

**Guardrail now**  
Keep thresholds and weights configurable; freeze contracts, not numbers.

**Source ranges**  
Pages 630-636

## Highest-priority guardrails to lift into the repo

1. Screenshot-only data may inform research, not runtime.
2. Conversation claims do not count as build evidence.
3. Options-derived interpretation needs replay proof.
4. Any manual Greek/IV construct requires deterministic recomputation.
5. Module promotion requires walk-forward / replay discipline.
6. Runtime must veto stale data and degraded data feeds.
