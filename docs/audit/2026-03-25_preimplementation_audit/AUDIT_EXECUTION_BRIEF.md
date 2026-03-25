# Audit Execution Brief

## Objective

Audit the post-Gates 40-44 repo state before creating any new canonical planning gates.

## Binding audit order

1. Contract audit
2. Interchangeability audit
3. Playbook architecture audit
4. Carry / weekend / event-horizon audit
5. Planning synthesis input

## Pass criteria

The audit passes only if it produces:
- explicit evidence-backed findings;
- a clear split between `Known true`, `Gaps`, and `Planning consequences`;
- no silent mutation of active gate authority;
- no architecture claims without file evidence.

## Stopping rules

Stop the audit when:
- the five audit questions are answered with direct repo evidence;
- the findings are sufficient to write the next gate pack;
- the remaining uncertainty is vocabulary-level or implementation-level rather than architecture-level.
