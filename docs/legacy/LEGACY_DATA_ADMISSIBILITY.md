# Legacy data admissibility

This document classifies the remaining documents by whether they contain reusable numeric material and what that material is admissible for.

## Decision summary

### Admitted as fixture candidates
1. **`Options Data CSV Output.pdf` pages 1-7**
   - Contains manually structured rows for Apr 11 and Apr 17 expiries, plus historical Apr 1-4 rows and explicit timestamp reasoning.
   - Admissible use: small legacy options snapshot fixtures, parser tests, schema examples.
   - Provenance: manually reconstructed / conversation-structured.
   - Confidence: medium.
   - Recompute required: yes, before any production or research claim beyond fixture use.

2. **`Options Data CSV Output.pdf` pages 13-14**
   - OCR rescue pass for Apr 4 close screenshots with 0-day and 7-day rows.
   - Admissible use: OCR-noise regression fixtures, parser-stability tests, provenance examples.
   - Provenance: OCR cleaned.
   - Confidence: low.
   - Recompute required: yes.

3. **`of trading days below VWAP.pdf` pages 54-54**
   - Dated OHLC / change / volume table for Mar 17-28, 2025 appears as a compact market-state summary.
   - Admissible use: lightweight timeline fixture or eval scenario header.
   - Provenance: conversation-inferred summary table.
   - Confidence: medium-low.
   - Recompute required: yes.

4. **`of trading days below VWAP.pdf` page 351**
   - Clean portfolio arithmetic block: realised loss, unrealised loss, cash from sales, shares held, average cost.
   - Admissible use: deterministic eval/regression fixture for portfolio arithmetic and promotion logic.
   - Provenance: derived math claim from stated values.
   - Confidence: medium.
   - Recompute required: recommended but tractable.

5. **`of trading days below VWAP.pdf` pages 701-702**
   - Market-open ladder review with explicit hold/adjust actions, prices, shares, and notes.
   - Admissible use: regression/eval fixture for SLV-style ladder review and explanation outputs.
   - Provenance: manually reconstructed / conversation-inferred.
   - Confidence: medium.
   - Recompute required: yes.

## Not admitted as source datasets

### `Comprehensive Deep-Dive_ What's Really Happening Today in NVDA_ (1).pdf`
- Contains many numbers and dated narratives, but they are embedded inside strategy discussion and historical retellings rather than clean dataset blocks.
- Admissible as doctrine and feature inspiration only.
- Not admitted as fixture data in this pass.

### `NVDA GPT Framework Review.pdf`
- Meta-review, module archaeology, and failure commentary.
- No primary numeric dataset value.
- Not admitted as fixture data.

## Admissibility rules applied
- If the block is numeric but its provenance is screenshot/OCR/manual reconstruction, it may become a fixture candidate but never canonical truth.
- If the block is a clean arithmetic exercise tied to explicit stated inputs, it is admissible as an eval/regression fixture candidate.
- If the numbers are embedded in retrospective commentary without a clear data boundary, they stay out of the fixture manifest.
