# 2026-03-24 Posture Enricher Contracts

Status: Active Gate-20 supporting note  
Authority: subordinate to the Gate-20 leaf and gate map.

This note freezes the Gate-20 advisory enricher rule.

## 1. Frozen Gate-20 order

1. `fill_bias_adjuster`
2. `archetype_tagger`
3. `compression_regime_detector`
4. `obv_vi_flow_confirmation`
5. `tail_hedge_injector`
6. `volatility_sentiment_index`

## 2. Binding rules

- Every Gate-20 enricher must cite upstream Gate-19 contracts or current posture/eligibility surfaces explicitly.
- Gate-20 enrichers remain advisory-only. They must not place orders, mutate inventory, or imply broker integration.
- Missing raw inputs, especially volume-tape requirements, must stay fenced rather than hidden behind fake readiness.
- Gate 20 finishes the current non-execution contract tranche and must stop before Gate 21 execution-chain work.

## 3. Non-goals

Gate 20 must not:

- widen into broker adapters or order simulation;
- relabel advisory enrichers as approved runtime logic;
- add new playbooks;
- smuggle order-routing semantics into contract notes or field names.
