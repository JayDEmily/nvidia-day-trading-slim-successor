# Remaining-doc failure patterns

## Scope
Only the four remaining PDFs covered by `REMAINING_DOCS_EXTRACTION_PLAN.md`.

## Recurrent failure patterns that survive extraction

### 1. Equal-spacing ladder fantasy
Repeated warning: ladder spacing and capital allocation were often discussed as if they could be mechanically equal. The surviving doctrine says ladder placement must come from IV/VWAP/strike pressure, not neat spacing.

### 2. IV without HV or macro confirmation
Several passages reinforce that IV alone is a weak guide. If IV is elevated but HV, VIX, yields, sector ETFs, or macro stress do not confirm, confidence should be downgraded.

### 3. Treating OCR as market truth
The options-data PDF explicitly says the OCR rescue is noisy. OCR-cleaned rows can be fixture candidates, never canonical truth.

### 4. Narrative conviction outrunning fill reality
Pages 701-702 in the VWAP thread show why explicit ladder review matters: good-sounding trades still need fill-likelihood, support, and realistic TP adjustment.

### 5. Overly optimistic take-profit placement
The remaining docs repeatedly show TPs being set too far away from intraday reality. A bounded TP hit-rate check belongs in evals and review packets.

### 6. Macro as story rather than veto
The strongest surviving logic uses macro as a go/no-go or confidence modifier, not as an excuse to add infinite narrative context.

### 7. “All wired” implementation claims without evidence
The deep-dive tail contains classic conversation-reality drift. Claims of complete implementation remain docs-only unless independently verified in repo code.

### 8. Missing module attribution
Framework-review passages reinforce that when a decision goes wrong, the system must say whether the failure came from signal, veto, sizing, execution or macro overlay.

### 9. Poor separation between planning artefacts and executable truth
The remaining PDFs mix doctrine, screenshots, advice, and implementation claims. Promotion status must remain explicit.

### 10. Capital-release ambiguity
The VWAP thread shows cash-release reasoning is fragile when open orders, reserved capital, and realized/unrealized loss are not clearly separated.

## Guardrail mapping
- `derived_features`: macro confirmation, precursor composites, gap behaviour, session weighting
- `risk`: downgrade or block when IV is unconfirmed or event/macro risk is hot
- `execution_records`: explicit fill likelihood, TP adjustment, capital reservation, module attribution
- `docs_only`: OCR caveats, implementation-claim skepticism, doctrine notes
