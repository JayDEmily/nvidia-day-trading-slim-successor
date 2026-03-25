# Next Promotion Tranche

## Objective
Choose the next implementation-worthy items after session clock and the current lightweight SLV / overnight evaluator contracts.

## Priority order
### 1. Strategic Ladder Validator deepening
Why:
- already a top-3 promotion candidate;
- archive salvage adds linked primitives (`slv_overlay_score.py`, `slv_validator.py`, `ladder_constructor.py`, `fill_bias_adjuster.py`);
- directly useful for pre-open ladder sanity and replay.

### 2. Macro shock / volatility supervisory expansion
Why:
- archive adds `macro_shock_responder.py`, `vvix_ladder_shaper.py`, and `conviction_tier_allocator.py`;
- these fit the current thesis that edge is more likely in vetoing/filtering than prediction.

### 3. Module attribution + confidence divergence evaluator slice
Why:
- archive evaluator modules provide a concrete path for post-run learning;
- good fit for paper-trading and replay review.

## Explicit deferrals
- wrapper scripts (`run_trading_bot.py`, `run_signal_scan.py`) stay deferred;
- broker adapter remains deferred;
- broad variant execution remains deferred until replay + config typing are stronger.

## Single next move
Implement **SLV deepening** first: shared strike-zone scoring primitive + ladder constructor + richer evaluation artefact.
