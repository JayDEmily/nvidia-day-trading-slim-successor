# 2026-04-02_GATE175_TEMPORAL_CALENDAR_MULTI_CLOCK_IMPLEMENTATION

## Purpose

Implement the temporal/calendar/event/multi-clock runtime surface for the co-resident lane and align it with the governed temporal-status ledger already frozen in master.

## Runtime surface built here

The lane now preserves one typed `ParallelRiskTemporalSurface` with:

- session phase and behavioural phase
- desk window and clock envelope
- minutes-since-open / minutes-to-close
- closure classes and bridge rules
- next-session-open hint
- event minutes remaining, event-window state, overlap class, risk-timing class, and carry sensitivity
- event timing profile and active event family
- expiry-days remaining and expiry-cycle state
- governance statuses for session clock, behavioural phase, calendar source, event source, and expiry source
- lineage keys from the live event snapshot when present

## Governance alignment frozen here

- session clock remains a fixed structural heuristic surface
- behavioural phase remains a governed live threshold surface
- desk calendar authority remains an invariant direct-read surface when present
- live event snapshot remains the direct event-identity/evidence source when present
- `next_event_at` and `next_expiry` remain compatibility timestamp sources when direct richer packets are absent

## What remains for later gates

- market/options dependency and dislocation logic
- candidate-specific fragility classification
- anti-duplication and review emission
