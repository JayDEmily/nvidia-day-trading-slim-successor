# Audit Planning Input

This file is not the canonical gate pack. It is the planning consequence surface produced by the audit.

## Recommended downstream gate sequence

### Gate 46
Close the pre-implementation audit tranche and freeze its findings as the authoritative planning input.

### Gate 47
Playbook registry v2 planning and implementation:
- family
- setup variant
- execution expression
- horizon
- compatibility bridge from the current flat registry

### Gate 48
Carry-horizon handoff planning and implementation:
- explicit close-state -> carry-state contract
- Friday/weekend/event-carry taxonomy
- handoff rules from intraday runtime to carry runtime

### Gate 49
Compatibility-surface decision:
- retain `session_clock` only as an explicit compatibility wrapper, or
- retire it in favour of `temporal_state`-named outward surfaces

### Gate 50
Vocabulary governance rebase onto current main:
- rebase the vocabulary-consolidation workflow onto the current repo
- govern family/variant/expression/horizon labels
- block conflicting aliases and stale stage terms

## Explicit non-goals for the next implementation tranche

Do not, in the very next tranche:
- invent every possible trader playbook leaf;
- merge the stale vocabulary workspace blindly;
- rewrite DMP;
- mix weekend carry logic into ordinary intraday playbook selection.
