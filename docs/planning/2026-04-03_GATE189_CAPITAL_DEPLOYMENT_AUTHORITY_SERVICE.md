# 2026-04-03_GATE189_CAPITAL_DEPLOYMENT_AUTHORITY_SERVICE

## Purpose

Implement the standalone `CapitalDeploymentAuthorityService` against the existing runtime result surfaces plus the repo-native current-capital snapshot path.

## Completed work

- added `src/nvda_desk/services/capital_deployment_authority.py`
- implemented deterministic deploy-versus-stand-down logic without recalculating upstream cognition
- preserved the repo-native capital read path as source evidence through `ExecutionRecordsService.latest_capital_state()` returning `CapitalStateSnapshotPayload`
- proved controlled `$1,000` capital bootstrap coverage using `CapitalStateSnapshotPayload` directly in the bounded sandbox proof slice rather than inventing a second ledger architecture

## Key scope holds

- service reads current buying power from the repo-native capital snapshot path
- service sizes from already-computed execution/posture surfaces plus bounded terminal-risk carriage
- service does not write a new ledger, close positions, or remember prior recommendations

## Evidence

- `src/nvda_desk/services/execution_records.py`
- `src/nvda_desk/services/capital_deployment_authority.py`
- `tests/test_gate189_capital_deployment_authority_service.py`
