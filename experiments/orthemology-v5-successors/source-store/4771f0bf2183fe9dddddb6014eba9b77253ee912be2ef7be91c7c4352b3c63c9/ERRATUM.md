# Erratum: paragraph-indexing explanation

Date: 2026-10-07 UTC

The earlier explanation that an empty DOCX paragraph caused the veracity proposal's citation discrepancy was mistaken. Direct inspection finds no empty body paragraphs in the T17 report, T17 source guide, or T19 report. The sealed paragraph IDs are zero-based, beginning at P00000. The active references were corrected against those exact IDs; this erratum does not substitute an unverified causal account of the original mismatch.

The affected explanation occurs once in the sealed CHANGE_RECORD.md and once in the approved PROPOSED_DESIGN.md. The sealed originals, proposal history, Lean sources, proof receipts, and independent review identities have not been rewritten. The two corrected public-facing projections replace only those explanatory sentences; their exact original and derived hashes and unified diffs are in ERRATUM_MANIFEST.json. A curator should use the projections for those two documents and retain this erratum alongside the preserved v1 record.

All 47 bound paragraphs still match direct zero-based DOCX extraction. The scientific source identities and all 95 files covered by the original v1 seal are unchanged. No Lean compilation, model run, proof replay, theorem change, or philosophical reappraisal was performed for this documentation-only correction. The existing independent review PASS remains attached to its original immutable inputs and receipt.
