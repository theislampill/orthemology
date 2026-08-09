# SPA-R7 — representation-fibre defect and joint correction

**Status:** existing T294/Deep BV fibre-factorization family under
representation vocabulary; no new theorem identity or novelty.

## Result

For finite objects `X`, representation `r : X → Z`, and exact target
`t : X → Y`, a common exact decoder exists exactly when `t` is constant on every
`r`-fibre.

Define the exact collision defect as the number of unordered pairs with equal
representation and unequal target. A joint representation `(r,q)` refines the
fibres of `r`, so its defect cannot increase. It repairs the target exactly when
the joint defect reaches zero.

## Representation firewalls

- Learned versus hand-authored is provenance metadata, not a formal information
  order. Identical maps have identical fibres regardless of tag.
- Higher raw cardinality or dimension does not imply target sufficiency.
- Equal label histograms do not imply equal partitions.
- Coordinate relabeling preserves the induced partition.
- Fibre sufficiency does not establish nonnegative rank, tensor-factor
  uniqueness, learned mechanism, ontology, or causal realization.

## Executable evidence

The checker exhausts 9,306 representation/target decoder cases and 271,364 joint
representation cases through five objects. Brute-force decoder existence agrees
with fibre constancy; joint defect never increases; and many joint corrections
remove a base residual. It also checks same-partition invariance.

Seven mutants are killed, including raw-cardinality sufficiency,
histogram/partition collapse, majority decoding, increasing joint defect,
learned-tag privilege, tensor-uniqueness transfer, and prefilled counters.

## Conclusion ceiling

Exact finite target sufficiency of induced partitions only.
