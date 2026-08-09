# SPA-R3 — representation-normalized resource comparison

**Status:** specialist-local standard construction; no novelty or class-wide
architecture exclusion.

## Problem

Raw cost is attached to a realization, not automatically to its observable
profile. State splitting, dead states, duplicated interfaces, or alternate
encodings can change memory or latency without changing the complete profile.
A resource intervention therefore needs a representation-invariant object.

## Scalar correction

For a finite registered realization set `R`, profile map `E`, and a scalar cost
`c` in common units, define

```text
c*(p) = min { c(r) : r ∈ R and E(r)=p }.
```

This is invariant under permutation and under changing the chosen
representative. It is only a minimum over the registered set.

## Vector correction

For vector costs, coordinatewise minima are insufficient. The two realizers
`(1,10)` and `(10,1)` have coordinatewise infimum `(1,1)`, but no realizer meets
budget `(1,1)`. Preserve the Pareto frontier—or, equivalently, the complete
budget-feasibility predicate—unless an independently warranted scalar
aggregator is frozen.

## Architecture exclusion guard

An architecture is excluded under a budget only relative to a complete declared
realization class with common coordinates, units, compiler, decoder, meter, and
budget. One observed high-cost implementation does not exclude a hidden
low-cost implementation.

## Executable evidence

The checker exhausts 216 three-realizer scalar registries, including 1,296
permutation checks, and 729 vector-cost multisets across 6,561 budget tests.
Pareto reduction preserves every feasibility answer. It also finds numerous
coordinatewise-infimum false positives.

Six mutants are killed: first representative, maximum instead of minimum,
coordinatewise chimera, incomplete-class exclusion, intrinsic scalar ordering
of Pareto-incomparable points, and architecture-specific units.

## Conclusion ceiling

```text
FINITE_REGISTERED_REALIZATION_FEASIBILITY
NO_LOWER_BOUND_OVER_UNREGISTERED_REALIZERS
NO_ARCHITECTURE_OR_METAPHYSICAL_TRUTH
```
