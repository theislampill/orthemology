# SPA-R10 — minimum eligible residual-collision cover

**Status:** specialist-local application of standard finite set-cover and
coverage-function machinery; no new theorem identity, novelty, architecture
implementation, repository adoption, or metaphysical conclusion.

## Frozen object

Let `C` be the finite set of cross-target pairs that still collide under the
current complete profile. Every independently certified eligible factor `f`
has a coverage set `C_f ⊆ C`: the collisions that factor separates.
Eligibility and target blindness are determined before optimization.

## Criterion and bounded impossibility

A factor set `S` identifies the frozen target partition exactly when

```text
union { C_f : f in S } = C.
```

Therefore minimum-factor selection is an exact finite set-cover problem. If the
union of *all* eligible factors leaves some collision, then no composition from
that declared factor family identifies the target on the frozen manifest. This
is a bounded no-cover result—not metaphysical impossibility and not a claim
about unregistered interventions.

## Deletion criterion

For a factor `f` inside a covering set `S`, deleting `f` destroys coverage iff
`f` has a private collision witness not covered by `S \ {f}`. Positive
individual gain does not make a factor indispensable; another factor may cover
every collision it covers.

## Pairwise versus class-wide distinction

In the three-rival fixture, each of two weak factors separates some architecture
pairs while leaving others. Their union removes every frozen collision; neither
one alone provides three-way identification. A target-equal factor removes all
collisions but is rejected before optimization because it leaks the disputed
coordinate.

## Executable evidence

The checker exhausts 74,954 finite set systems with collision universes and
factor families of sizes one through four. An independent dynamic program and
brute-force subset search agree on every minimum cover. The all-factor-union
criterion agrees with no-cover status, and factor deletion agrees with the
private-witness criterion in every tested covering set.

Seven mutants are killed, including greedy optimality, positive-gain
indispensability, pairwise-to-class-wide collapse, target-leak admission,
deletions without witnesses, metaphysical overreading, and prefilled counts.
A six-element countermodel shows deterministic maximum-gain greedy selection
can use three factors where the optimum uses two.

## Residual-guided successor

The exact next empirical operation is not “choose the most plausible factor.”
It is:

1. certify neutrality and implementation maps;
2. compute its marginal coverage of the current residual collision set;
3. reject profile-derived zero-gain and target-leaking candidates;
4. update the exact minimum-cover/no-cover calculation.

## Conclusion ceiling

```text
FINITE_FROZEN_MANIFEST_MINIMUM_ELIGIBLE_FACTOR_COVER
OR_DECLARED_FACTOR_FAMILY_NO_COVER
NO_EMPIRICAL_ARCHITECTURE_IMPLEMENTATION
NO_METAPHYSICAL_IMPOSSIBILITY
```
