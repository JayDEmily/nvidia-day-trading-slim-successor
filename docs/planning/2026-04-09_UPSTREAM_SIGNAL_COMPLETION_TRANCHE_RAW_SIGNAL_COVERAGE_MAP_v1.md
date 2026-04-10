# 2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_RAW_SIGNAL_COVERAGE_MAP_v1

Status: closed support artefact retained as evidence for the upstream signal completion pack closed through Gate 252.

## Classification law

Exactly one runtime-state classification is allowed per family:
- already wired
- captured but weak
- schema-expected but unwired
- not raw-captured yet

Class law:
- **Class A** = not lawfully raw-captured in the current admitted repo path
- **Class B** = already capturable or already present elsewhere in repo/runtime fixtures but not yet fully promoted through the live prepared-runtime ingress path

## Authoritative coverage map

| family | runtime-state classification | class | tranche scope | notes |
|---|---|---|---|---|
| cross_asset_regime_core | captured but weak | Class B | in scope | promoted through `PreparedRuntimeRegimePacket` and conditional `MarketRegimeContextInput` wiring; currently complete in fixture/replay truth and optional in prepared-runtime carriage |
| breadth_score | schema-expected but unwired | Class A | deferred | canonical Step 2 field remains deferred until lawful raw-source admission exists; packet carriage stays optional only |
| concentration_score | schema-expected but unwired | Class A | deferred | same deferred rule as breadth_score |
| same_bucket_volume_baseline | captured but weak | Class B | in scope | `PreparedParticipationBaselinePacket` reconstructs bounded baseline from `relative_volume_ratio` where current admitted runtime truth permits it |
| same_bucket_spread_baseline | not raw-captured yet | Class A | deferred | no lawful spread-history substrate is admitted in the current runtime path |
| same_bucket_trade_count_baseline | not raw-captured yet | Class A | deferred | no lawful trade-count history substrate is admitted in the current runtime path |
| optional_top_of_book_bid_ask | not raw-captured yet | Class A | deferred optional | do not promote until cheap admitted capture exists in repo truth |
| dealer_flow_raw_drivers | not raw-captured yet | Class A | deferred | vanna/charm style raw drivers remain outside this tranche |

## Stop conditions frozen for this pack

1. Do not back-door breadth or concentration into live regime ingress from synthetic defaults.
2. Do not promote spread or trade-count baselines from inferred placeholders.
3. Do not widen optional top-of-book into scope without proving cheap lawful capture in current repo truth.
4. Do not redesign Steps 4-6 or CDA to consume new upstream packets directly.
5. Do not let `PreparedNormalisedFeatureSet` masquerade as the lawful live regime packet.
