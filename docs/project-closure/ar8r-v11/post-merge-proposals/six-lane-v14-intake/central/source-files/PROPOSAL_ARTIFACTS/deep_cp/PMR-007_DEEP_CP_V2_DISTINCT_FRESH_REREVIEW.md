# Deep CP V2 distinct fresh rereview

## Frozen object

The rereview consumed the V2 theorem, V2 registry, V2 repair log, primary
checker, and primary results under `PMR007_DEEP_CP_V2_FROZEN_HASHES.sha256`.
All five hashes matched.

## Independent method

The rereview did not enumerate the primary checker’s open-loop word list.
Instead it:

1. represented each neutral state as a seven-bit integer;
2. reconstructed each intervention as an independently parsed XOR mask;
3. constructed the declared Mealy transition/output system for both
   architectures;
4. computed the stable observational partition by iterative signature
   refinement over every action;
5. checked whether every paired `U(s), I(s)` remained in one experiment class;
6. ran 25,000 independently generated common-history adaptive-policy trials of
   horizons one through seven;
7. audited the common-contract and ineligible-operation metadata.

## Results

```text
frozen hash rows: 5
frozen hash mismatches: 0
states per architecture: 128
actions: 8
partition-refinement iterations: 2
stable declared experiment classes: 64
same-neutral-state U/I pairs equivalent: 128 / 128
architecture-equivalence failures: 0
target-varying pairs inside equal experiment classes: 128 / 128
adaptive-policy trials: 25,000
maximum sampled horizon: 7
adaptive-policy failures: 0
eligible-action registry and mask shape: PASS
common formal contract fields: PASS
physical operationalization not claimed: PASS
current ineligible operations blocked: 5 / 5
future operationalization not denied: PASS
```

The 64 stable classes reflect the declared output/transition quotient; every
class contains the U/I pair with the same neutral state. The hidden target
coordinates vary inside all 128 paired state comparisons.

## Scope and challenge findings

- The partition computation corroborates all-finite common-policy parity for
  the frozen deterministic kernel; the mathematical induction remains the
  proof owner.
- The finite regression does not establish completeness of the intervention
  universe.
- A self-model token remains a behavioral coordinate, not de-se ownership.
- A declared fittingness-status bit remains a carried input, not objective
  fittingness.
- An architecture-specific internal operation remains a changed experiment
  until a common type and semantics-preserving implementation are supplied.
- No physical, psychological, metaphysical, source-world, or prior-probability
  conclusion follows.

## Disposition

```text
PASS_WITH_NONBLOCKING_FORMAL_REGISTRY_AND_FUTURE_EXPERIMENT_NOTES
```
