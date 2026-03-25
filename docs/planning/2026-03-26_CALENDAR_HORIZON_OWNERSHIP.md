# 2026-03-26 Calendar/Horizon Ownership

Status: complete on `main`
Version: v1.0
Gate: Gate 51
Purpose: pin explicit ownership for Step 0 calendar/horizon classification so intraday and carry evaluation cannot drift between temporal and carry code paths.
Authority boundary: subordinate to `docs/01_NORMATIVE.md`, `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_IMPLEMENTATION_MAP.md`, and `docs/planning/2026-03-26_COGNITIVE_WORKFLOW_BOUNDARY_RULES.md`.

## Step 0 decision

Step 0 is an **explicit runtime routing concern**.

It is not a hidden eighth analytical stage and it does not replace the seven-stage cognition spine. Instead, it owns the question:

> Which evaluation horizon is being entered before the normal stage traversal begins?

## Owner

The owner of Step 0 is the **runtime orchestration / routing layer**.

That owner is responsible for selecting between:
- normal intraday seven-stage traversal; and
- carry-horizon evaluation (`overnight`, `weekend`, `event_carry`) when the route is appropriate.

## Inputs Step 0 may use

Step 0 may consume only routing-relevant facts such as:
- timestamp / market-hours facts;
- session-calendar facts;
- event schedule facts;
- expiry-calendar facts;
- explicit held-position / inventory presence;
- explicit request to evaluate carry rather than intraday deployment.

## Inputs Step 0 must not use

Step 0 must not consume:
- temporal-stage behavioural verdicts as if they already existed;
- downstream regime/options/posture verdicts;
- family/setup/expression decisions;
- review/attribution outcomes.

## Route outcomes

Step 0 may yield one of these route classes:
- `intraday_session_route`
- `overnight_carry_route`
- `weekend_carry_route`
- `event_carry_route`
- `out_of_scope_closed_route` (for states where no normal intraday traversal should begin)

These route classes are routing outcomes, not playbooks.

## Selection semantics

### Intraday route
Chosen when the system is evaluating live/session intraday deployment.
The seven-stage cognition order remains binding.

### Overnight / weekend / event-carry routes
Chosen when the system is evaluating whether an existing or contemplated position may be held beyond the current session horizon.
These routes enter the carry branch with explicit handoff expectations rather than running ordinary intraday family selection as if the problem were the same.

### Out-of-scope closed route
Chosen when the system is outside ordinary evaluation conditions and no valid intraday or carry decision is being requested.
This prevents hidden fallback behaviour.

## Why Step 0 is not an eighth stage

The seven-stage analytical spine remains:
`temporal -> regime -> options/flow -> posture/risk -> playbook eligibility -> execution -> review`

Step 0 sits **before** that analytical chain as a routing decision about horizon and traversal. It exists so the repo can be explicit about when the intraday chain runs and when the carry branch runs.

## Consequences for later gates

- Gate 52 may assume candidate family generation only happens on the intraday route unless a future gate explicitly proves otherwise.
- Gate 53 must define the typed handoff from intraday close-state to carry routes and must preserve the route classes above or justify a replacement.
- Gate 54 must not confuse Step 0 routing with DMP transport concerns.
