# SPA-R9 — common decoder on the tagged architecture union

**Status:** specialist-local specialization of the existing finite
fibre-factorization family; no new theorem identity, novelty, repository
adoption, architecture implementation, or metaphysical conclusion.

## Frozen object

For each declared architecture index `a`, let `X_a` be its finite local domain,
`e_a : X_a -> Y` its common-profile observation, and `q_a : X_a -> Q` the
frozen target. The decoder signature is exactly `d : Y -> Q`; it may not read
`a`, a private role, or the disputed target coordinate.

## Criterion

A single decoder satisfying

```text
d(e_a(x)) = q_a(x)
```

for every architecture and local point exists exactly when

```text
e_a(x) = e_b(x')  =>  q_a(x) = q_b(x')
```

for all architecture indices and points. This is ordinary fibre constancy on
the tagged disjoint union of all `X_a`. The decoder maps each observed profile
to its unique consistent target value and takes an arbitrary default at
unobserved profiles.

## Critical separation

Architecture-specific decoders are insufficient. One architecture may require
`d(0)=0` while another requires `d(0)=1`; each local problem is soluble, but no
common target-blind decoder exists. Permitting `d(a,y)` would hide the target
inside an architecture-relative signature and violate the common-interface
contract.

## Executable evidence

The checker exhausts all 4,096 triples of two-point binary
observation/target maps. Direct enumeration of all common decoders agrees with
cross-architecture fibre constancy in every case. It preserves the result under
all architecture-order permutations and produces many cases with local
architecture decoders but no common decoder.

Seven mutants are killed, including local-to-common collapse, histogram
sufficiency, architecture-tag leakage, within-architecture-only constancy,
order dependence, prefilled counts, and metaphysical overreading.

## Anti-false-multiplicity disposition

No new Lean theorem is allocated. The proposition is the existing finite
T294/Deep-BV fibre theorem after replacing the domain by a tagged disjoint
union. A duplicate formal theorem would add vocabulary, not mathematical
content.

## Conclusion ceiling

```text
FINITE_COMMON_TARGET_DECODER_ON_FROZEN_TAGGED_DOMAIN
NO_ACTUAL_ARCHITECTURE_IMPLEMENTATION
NO_SOURCE_WORLD_TRANSFER
NO_METAPHYSICAL_IDENTIFICATION
```
