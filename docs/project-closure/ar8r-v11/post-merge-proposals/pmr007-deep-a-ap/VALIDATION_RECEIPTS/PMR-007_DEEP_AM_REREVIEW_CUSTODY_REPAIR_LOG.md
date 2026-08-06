# PMR-007 Deep Round AM — rereview custody repair

```text
failed rereview owner:
pmr007_deep_am_networkx_semantic_rigidity_rereview_v1.py

failed result:
source_anchor_checks failed 2 / 13

mathematical/model result:
PASS

candidate scope changed:
false
```

The first distinct rereview correctly preserved a `FAIL` because two literal
source-anchor checks were brittle:

1. the OSM abstract uses `hidden state inference`, while the later model section
   uses `latent state inference`;
2. the PRH PDF layout split one sentence across columns/lines, so an exact
   contiguous-string search failed.

The repair changes only source-anchor normalization:

- use the exact OSM abstract phrase and separately check the later latent-state
  passage;
- normalize PDF whitespace before phrase matching.

The failed V1 script and result remain preserved.  No theorem, model,
countermodel, or authority scope is changed.

A second attempt still failed because two-column PDF extraction interleaved the
sentence with an adjacent column.  V3 therefore checks the two independent
fragments actually present in the extracted text rather than requiring a
contiguous cross-column sentence.  V2 remains preserved as failed custody
evidence.
