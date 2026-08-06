# PMR-007 Deep V V2 distinct fresh rereview

Disposition: `PASS_WITH_NONBLOCKING_INTEGRATION_AND_AUTHORITY_NOTES`.

The rereview used a separate implementation from the primary checker:
restricted-growth enumeration of all set partitions and recursive topological
sorting of the product order. It also recomputed every coordinate directly from
the model owner and verified every frozen hash.

## Results

```text
frozen hash rows:
7

frozen hash mismatches:
0

evaluation episodes independently recomputed:
8

axis mismatches:
0

partitions of four pair states:
15

exact joint partitions:
1

blocks in the coarsest exact joint partition:
4

blocks in a coarsest profile-only partition:
2

blocks in a coarsest warrant-only partition:
2

blocks in the coarsest release partition:
2

partitions of eight three-axis states:
4,140

exact three-axis partitions:
1

blocks in the coarsest exact three-axis partition:
8

linear extensions of the product order:
2

axis-swap-invariant linear extensions:
0

world-axis flips at fixed profile/warrant pair:
4 / 4
```

The results independently confirm:

1. the product pair is the coarsest exact diagnostic for the two frozen axes;
2. one coordinate cannot recover the other;
3. the one-bit release quotient loses three-way failure-mode information;
4. mixed failures are incomparable before an extra priority is supplied;
5. world/target adequacy remains independent of both registered coordinates.

## Authority and scope notes

- The result is a product/factorization application with zero general novelty.
- The minimal warrant predicate is not the full Fable Core B calculus.
- The world-target parameter is independently supplied, not justified by the
  finite model.
- The product is diagnostic composition, not explanatory, causal, metaphysical,
  or proof-theoretic unification.
- Core A's false-closure vulnerability remains open.
- Same-session staged rereview is not external independence.

No blocking defect remains at the repaired scope.
