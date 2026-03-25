# 2026-03-24 Review Attribution Contracts

Status: Active Gate-23 supporting note  
Authority: subordinate to the Gate-23 leaf and gate map.

This note freezes the Gate-23 review-chain rule.

## 1. Frozen Gate-23 order

1. `profit_loss_ledger`
2. `module_trace_attribution`
3. `daily_summary`
4. `feedback_summary_writer`
5. `module_score_attributor`
6. `variant_trace_logger`
7. `variant_performance_tracker`
8. `confidence_divergence_logger`
9. `macro_alignment_checker`

## 2. Binding rules

- Every Gate-23 module must remain descriptive and packet-serialisable.
- `profit_loss_ledger` is a preview ledger only. It must not imply booked PnL, tax truth, or production reconciliation.
- Attribution, feedback, and variant-tracking surfaces must source their evidence from the deterministic packet chain and preview lifecycle state already present in the repo.
- `confidence_divergence_logger` and `macro_alignment_checker` remain evaluator-style outputs only. They must not quietly replace the existing posture gate.

## 3. Non-goals

Gate 23 must not:

- claim booked or audited financial results;
- relabel descriptive review-chain outputs as approved promotion evidence;
- widen into Gate-24 scope-definition work or new playbook invention;
- invent external analytics or broker ledgers that the repo does not own.
