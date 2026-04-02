# 2026-04-02_GATE161_OPPORTUNITY_VS_CAUTION_SHAPING_LAW

Status: complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`

## Purpose

Make Workstream 4 executable without pretending the repo already has a finished upstream opportunity branch.

Gate 161 freezes three truths together:
1. what the current live modifier plane actually does today;
2. where richer upstream opportunity architecture should come from first;
3. how to separate opportunity shaping from caution shaping without multiplying live knobs or swallowing the separate independent risk-lane thread.

## Scope boundary

Gate 161 is planning-only.

It may:
- describe the current live modifier plane exactly as implemented;
- freeze the workbook-derived upstream path through primitives, derived features, and playbook routing;
- define bounded-surface and non-duplication law for later coding.

It may not:
- claim the independent risk lane already exists inside this pack;
- widen the admitted live mutable surface set;
- or use "opportunity shaping" as a backdoor to skip raw-versus-derived or stage-purity law.

No new governed vocabulary is admitted in Gate 161.

## Current live reality: the modifier plane is caution-heavy

Gate 161 freezes the current live dynamic plane honestly.

### What the current live state-policy layer actively deforms

Current policy applications materially deform:
- `target_fresh_deployable_pct`
- `entry_gate_score_floor`
- `max_risk_per_trade`
- `hedge_required`
- stand-down / degradation / kill-switch consequences that compress posture and execution behaviour

This means the live modifier plane today is primarily:
- capital compression,
- entry tightening,
- risk-cap tightening,
- hedge forcing,
- and stand-down / veto pressure.

### What is admitted but not yet dynamically rich

The following admitted surfaces remain governed but baseline-only today:
- `zone_score_threshold`
- `distance_to_vwap_soft_limit_pct`
- `risk_vix_caution_threshold`
- `risk_vix_hot_threshold`

### Honest verdict

The current live modifier plane is **not** yet a true upstream opportunity branch.

It is mainly a posture / execution caution-and-envelope layer with explicit later-risk-sensitive consequences.

Gate 161 freezes that as current truth so later coding does not design against aspiration instead of evidence.

## Upstream opportunity path frozen by Gate 161

The workbook already shows a richer upstream path that should come **before** coefficient proliferation.

### Opportunity should come first from better raw inputs

Relevant workbook evidence surfaces already named by this pack:
- `Raw_Primitives_Catalog`
- `Options_Chain_Raw_Spec`
- `Volume_Baseline_Raw_Spec`

These sheets push the repo toward denser primitive capture rather than toy proxies.

### Opportunity should then come from better derived features

Relevant workbook evidence surfaces:
- `Derived_Features_Catalog`
- `Temporal_Step1_Framework`

This freezes that derived state should be lawful downstream of primitives and must still obey Stage 1 purity.

### Opportunity should then come from playbook-family routing

Relevant workbook evidence surfaces:
- `Playbook_Module_Audit`
- `Gate_41_44_Summary`
- `Test_Use_Cases`

These already point toward richer options-first playbook families and better routing through admissibility / family logic before adding fresh runtime coefficient surfaces.

## Opportunity-versus-caution separation law

Gate 161 freezes the following planning law for later coding:

1. **Opportunity shaping belongs upstream.**
   It should grow first through richer primitives, better derived features, and better playbook-family routing.

2. **Caution shaping belongs in bounded runtime envelope control.**
   It may tighten entry, compress capital, require hedges, reduce size, or trigger stand-down / veto pressure.

3. **Missing upstream design work must not be replaced by coefficient inflation.**
   No later gate may solve weak raw capture, weak feature definition, or weak playbook routing by casually adding a new live coefficient surface.

4. **Stage purity still applies.**
   Stage 1 and other earlier stages may not consume later-stage verdicts and call that opportunity architecture.

5. **Owner-stage truth still applies.**
   A surface cannot become the "opportunity branch" merely because it influences outcomes; it must have a truthful stage owner and direct consumer path.

## Bounded-surface discipline frozen by Gate 161

The admitted live mutable surface set remains intentionally narrow for this pack.

Gate 161 therefore freezes:
- no widening of the admitted live mutable surface set during this planning tranche;
- no claim that the workbook candidate universe is runtime-ready merely because the bounds exist;
- no assumption that every interesting opportunity concept needs a new coefficient surface.

The preferred sequence remains:
1. preserve or add the right raw primitive;
2. define the right derived feature;
3. route it lawfully through playbook-family and stage grammar;
4. only then ask whether a bounded coefficient surface is genuinely required.

## Non-duplication law against the independent risk lane

Gate 161 is also where the pack freezes the anti-duplication rule.

1. This pack may describe current caution-heavy behaviour and reserve space for the future independent risk lane.
2. This pack may not claim to implement that lane.
3. Later coding in this pack must not quietly duplicate future independent risk responsibilities inside posture, execution, or modifier code just because the separate thread exists elsewhere.
4. If later code introduces an additional caution surface or override path, it must prove that it is not merely duplicating a future risk-lane responsibility.

## What Gate 161 says **is** allowed now

Later coding inside this pack may:
- tighten owner-stage truth for existing surfaces;
- materialise the coefficient-status inventory from Gate 159;
- clarify which admitted surfaces are baseline-only versus dynamic;
- improve documentation and contract law for the existing caution-heavy runtime plane;
- reserve clean integration seams for the separate risk-lane thread.

## What Gate 161 says is **not** allowed now

Later coding inside this pack may not:
- multiply live coefficient knobs to compensate for missing options/raw-data work;
- relabel a downstream caution surface as upstream opportunity merely because it changes outcomes;
- claim the pack has solved serial conservatism by prose alone;
- or merge this pack with the independent risk-lane thread.

## What Gate 161 hands forward

1. Gate 162 inherits an execution-ready distinction between upstream opportunity architecture and downstream caution shaping.
2. Later coding now has an explicit anti-knob-inflation rule.
3. The pack now preserves the workbook gold that upstream richness should come first from inputs, derived features, and playbook routing.

## Definition of done recorded by Gate 161

Gate 161 is complete only because:
- the repo now has one explicit statement that the current live modifier plane is caution-heavy rather than a finished upstream opportunity branch;
- the workbook-derived upstream path through primitives, features, and playbook routing is frozen as the preferred first move;
- and the pack now has bounded-surface plus non-duplication law against silent coefficient proliferation and silent risk-lane duplication.
