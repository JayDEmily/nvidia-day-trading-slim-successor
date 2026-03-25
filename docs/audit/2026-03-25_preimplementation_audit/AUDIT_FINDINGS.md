# Audit Findings

## Known true

### F1. The stage-contract spine is coherent and the DMP wrapper is not the blocker.

The normative runtime order remains fixed at temporal -> regime -> options/flow -> posture/risk -> eligibility -> execution -> review in `docs/01_NORMATIVE.md:41-53`. The runtime executes those exact seven typed stages in `_STAGE_SPECS` in `src/nvda_desk/services/cognition_runtime.py:103-145`. The DMP envelope still wraps the live payload class dynamically via `payload.__class__` and records `payload_model_name` and `payload_module_path` in `src/nvda_desk/schemas/dmp.py:171-187,276-310`.

Audit verdict: **pass**. The wrapper/protocol layer can carry richer stage payloads without needing a protocol rewrite.

### F2. Interchangeability is stage-bounded, not global.

The repo is architected around typed stage outputs such as `TemporalContextOutput`, `MarketRegimeContextOutput`, and `OptionsFlowContextOutput` in `src/nvda_desk/schemas/cognition.py`. Downstream imported-module contracts bind specifically to those stage outputs, for example `temporal: TemporalContextOutput` in `src/nvda_desk/schemas/imported_modules/context_scanners.py:120`, `market_context_synthesis.py:61`, `posture_enrichers.py:95`, `execution_planning.py:97`, `execution_lifecycle.py:135`, and `review_attribution.py:122`.

Audit verdict: **pass with boundary note**. Modules are interchangeable only within a grammar slot that preserves the same typed contract. They are not free-floating interchangeable parts across stages.

### F3. Weekend / overnight carry is already a separate branch in principle.

The carry schemas explicitly model `next_session_open_ts`, `weekend_window`, and `event_window_open` in `src/nvda_desk/schemas/overnight.py:94-123`. The replay service derives `weekend_window` and computes alternative paths (`flatten`, `hold_baseline`, `follow_recommendation`) in `src/nvda_desk/services/carry_replay.py:28-88`.

Audit verdict: **pass in principle**. Weekend logic already belongs to a carry-horizon branch, not the ordinary intraday playbook slot.

## Gaps

### G1. Legacy `session_clock` compatibility surfaces are still live and now create architecture-language drift.

The runtime Step-1 truth has moved to `temporal_state` in `src/nvda_desk/domain/temporal_state.py:60-151`, but several outward surfaces still expose `session_clock` semantics:
- `src/nvda_desk/schemas/market.py:20-24` still returns `session_clock: SessionClockFeaturePayload`;
- `src/nvda_desk/services/market_state.py:25-35` still serves `get_session_clock()`;
- `src/nvda_desk/api/app.py:236-243` still exposes `/market/session-clock`;
- `src/nvda_desk/services/replay.py:14-35` still groups replay by `SessionClockPhase` using `SessionClockClassifier`;
- `tests/test_session_clock.py:11-53` still treats the legacy classifier as the direct public truth.

Audit verdict: **gap**. The repo currently has a justified compatibility layer, but the compatibility decision is not yet codified as a deliberate long-term boundary versus an interim shim.

### G2. The playbook registry architecture is now stale, flat, and in direct conflict with current runtime reality.

The checked-in spec still says the registry exists to make the **four** live playbooks explicit and that “No new playbooks are introduced in this registry” in `docs/planning/2026-03-24_PLAYBOOK_REGISTRY_SPEC.md:7-12,69-83`. But the runtime now implements **seven** playbook rules in `src/nvda_desk/services/playbook_eligibility.py:37-47`, and the checked-in config carries seven entries in `config/playbook_registry.example.yaml:123-277`.

The registry also remains flat: it has `playbook_id`, `rule_id`, `execution_template_id`, priority, and three decision profiles, but no typed notion of family, setup variant, execution expression, or horizon in `docs/planning/2026-03-24_PLAYBOOK_REGISTRY_SPEC.md:14-67` and `config/playbook_registry.example.yaml:1-277`.

Audit verdict: **major gap**. The repo needs a registry-v2 planning tranche before more trader-real families/variants are added.

### G3. The carry branch exists, but there is no explicit typed handoff from close-state outputs to carry-horizon evaluation.

Intraday Step-1 emits `TemporalContextOutput` in `src/nvda_desk/schemas/cognition.py:126-146`, while carry modules consume separate overnight inputs in `src/nvda_desk/schemas/overnight.py:19-40,58-81,94-123`. There is no typed bridge contract that says exactly how a close-state packet, Friday close, event carry, or weekend horizon hand off from the intraday cognition chain into the carry branch.

Audit verdict: **major gap**. The branch separation is conceptually correct, but the handoff contract is not yet explicit.

### G4. The active planning stack has not yet been updated to reflect post-Gate-44 reality.

`PLANS.md` and the gate map still say Gate 45 is only a downstream placeholder in `PLANS.md:31-41` and `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md:52-68`. That is fine administratively, but it means the next tranche has no canonical gate pack yet for the audited work: playbook hierarchy, carry-handoff formalisation, compatibility-surface decision, or vocabulary governance.

Audit verdict: **expected gap**. This is precisely why this audit exists.

### G5. Non-blocking but real doc-hygiene drift is still present in the authoritative zip.

`docs/01_NORMATIVE.md:106-111` says dated implementation notes belong in `docs/status/` and historical artefacts belong in `docs/legacy/`. But the authoritative zip still carries dated historical files at the docs root, for example `docs/2026-03-18_NVIDIA_day_trading_build_plan_v1.md` and `docs/2026-03-18_NVIDIA_day_trading_technical_architecture_v1.md`.

Audit verdict: **non-blocking hygiene gap**. Not the main architecture blocker, but still drift.

## Planning consequences

1. The next canonical gate pack should treat DMP as stable and avoid rewriting the protocol surface.
2. The next gate pack should formalise **slot-bounded interchangeability** rather than vague module interchangeability.
3. The next gate pack should introduce a **playbook-registry v2** with at least `family`, `setup_variant`, `execution_expression`, and `horizon`.
4. The next gate pack should create a typed **intraday-close to carry-horizon handoff contract**.
5. The next gate pack should make an explicit decision about **legacy `session_clock` compatibility surfaces**: keep them as named compatibility wrappers or retire them in a bounded migration tranche.
6. Vocabulary governance should follow the audit, not precede it, because the audit has now identified the authoritative surfaces the vocabulary must govern.
