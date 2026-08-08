# PMR-007 Deep BL–BV semantic custody reissue

**Status:** `MATERIALIZED_PUBLIC_PROPOSAL_NOT_ADOPTED`

**Custody:** `SEMANTIC_REISSUE_OR_REGENERATED_CUSTODY_COPY`
**Original Deep BL–BV response-linked bytes recovered:** `2 / 28`

This directory preserves the public-safe portion of the verified custody reissue
archive `AR8R_PMR007_DEEP_BL_BV_CUSTODY_REISSUE_V1.zip` (SHA-256
`6ed381f16d2bbd46dd31a987bdc2b9552aa2ae083874dde650e75ff0794f27d3`).
The 22 files under `source-files/` are copied byte-for-byte from the archive's
sanitized semantic-delta tree. That exact copy relationship does **not** make
the regenerated files original Deep BL–BV bytes.

Only these two response-linked files survived as original bytes:

- `EXTERNAL_PDF_CUSTODY_AND_METHOD_NOTE.md`;
- `EXTERNAL_PDF_CUSTODY_SANITIZED.json`.

The other 26 response-linked artifacts remain unavailable in their original
byte form. Their reissued counterparts preserve only the bounded dispositions
visible in the authenticated owner-facing response. In particular:

- Deep BL–BU are summary-level semantic custody records with no recovered
  individual theorem identities or original proof/checker packets;
- `PMR-007-CIID-1` is retained as a reported post-merge scoped proposal with no
  historical identity, no general novelty credit, open external review, and
  pending owner adoption;
- the reported Deep BV experiment counts are transcriptions, not an executable
  reproduction; and
- this repository import does not select a champion, reach a meniscus, establish
  natural closure, or modify the exact Deep A–BK snapshot.

Validate this surface with:

```text
python tests/test_pmr007_deep_bv_semantic_reissue.py
python scripts/validate_pmr007_deep_bv_semantic_reissue.py
```
