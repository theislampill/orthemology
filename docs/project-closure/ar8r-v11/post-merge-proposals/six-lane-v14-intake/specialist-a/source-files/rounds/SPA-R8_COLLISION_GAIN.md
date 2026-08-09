# SPA-R8 — residual-collision gain for candidate-intervention selection

**Status:** specialist-local elementary partition-refinement / coverage-function
construction; no novelty or metaphysical target identification.

## Frozen object

For a finite declared model manifest, base profile `E`, target coordinate `Q`,
and eligible candidate factor `f`, let a target collision be an unordered pair
with equal `E` and unequal `Q`.

The collision gain of `f` is the number of current target-collision pairs that
`f` separates. For a set of factors, each pair is counted once.

## Result

```text
remaining collisions after adjoining factors
=
initial collisions - covered collision pairs.
```

The gain function is monotone and submodular because it is a finite set-coverage
function. A factor derived from `E` has zero gain, since it cannot split an
`E`-fibre. Full collision elimination identifies `Q` only on the frozen finite
manifest.

## Research-selection consequence

Among independently eligible target-blind candidates, rank the next operation
by *marginal residual-collision reduction*, not by raw cardinality, entropy,
complexity, or initial plausibility. Two weak factors can cover complementary
residuals. A high-cardinality profile-derived factor can have zero gain. A
factor equal to the target can have maximal gain and still be ineligible because
it leaks the disputed coordinate.

## Executable evidence

The checker exhausts 32,768 three-factor signatures over three objects,
including 262,144 gain/residual identities, monotonicity checks, and
submodularity checks, all with zero failures. Seven mutants are killed,
including raw-cardinality ranking, overlap double counting, profile-derived
gain, target-leak eligibility, and metaphysical overreading.

## Conclusion ceiling

```text
FINITE_DECLARED_MANIFEST_RIVAL_PARTITION_POWER
NO_EMPIRICAL_VALIDATION
NO_CAUSAL_IDENTIFICATION_WITHOUT_CAUSAL_GUARDS
NO_SOURCE_WORLD_OR_METAPHYSICAL_TRUTH
```
