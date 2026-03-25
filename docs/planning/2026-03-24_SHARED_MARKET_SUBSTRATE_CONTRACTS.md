# 2026-03-24 Shared Market-Data Substrate Contracts

Status: Active Gate-18 contract note  
Authority: Subordinate to the gate map and leaf ledger.

## Purpose

This note freezes the proxy-versus-fence rule for Gate 18 shared substrate imports.

## Rule

A Gate-18 shared substrate contract may do one of two things only:
1. proxy an already-existing deterministic runtime field honestly; or
2. remain explicitly fenced where the repo still lacks the raw feed or tick series.

## Proxy band

Proxy surfaces are allowed for:
- `spot_data_capture`
- `peer_equity_capture`
- `options_data_capture`
- `options_metadata_capture`
- `macro_data_capture`

These contracts preserve meaning and packet lineage without pretending the repo owns raw-feed ingestion.

## Fence band

Fence-only surfaces remain mandatory for:
- `vwap_accumulator`
- `vwap_roc`

Those two require raw trade-tick state that the current deterministic runtime still does not have.

## Non-goals

Gate 18 must not:
- build live feed handlers;
- invent broker adapters;
- widen into execution-chain logic; or
- mark any substrate import as approved runtime.
