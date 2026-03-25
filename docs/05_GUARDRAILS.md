# 05_GUARDRAILS

## Non-negotiable system rules

1. **No LLM live execution.**
2. **Deterministic runtime only.**
3. **Risk gateway mandatory.**
4. **Ledger mandatory.**
5. **No silent schema drift.**
6. **No hidden state.**
7. **No vendor lock-in in the domain model.**
8. **No direct route-handler business logic.**
9. **Replayability first.**
10. **Promotion is conservative.**
11. **Docstrings are mandatory on every new or refactored Python file.**
12. **Every runtime decision that affects capital or playbook eligibility must be explainable.**
13. **No allocation path bypasses posture and risk permission.**
14. **No module import discards preserved evidence without an explicit changelog entry.**

## Required runtime guardrails

At minimum, the runtime supports configurable checks for:
- stale data;
- market halts;
- reject storms;
- manual kill switch;
- broker disconnect;
- max position and exposure;
- max daily loss;
- insufficient buying power and PDT-style constraints;
- inventory-aware deployable-capital limits;
- no-overnight enforcement;
- review-packet completeness.

## Documentation guardrails

- stable docs live under `docs/`;
- active execution plans live under `docs/planning/`;
- dated notes live under `docs/status/` or `docs/legacy/`;
- README points to the authoritative set;
- `CHANGELOG.jsonl` is append-only.
