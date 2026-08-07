# PMR-007 Deep BE V2 distinct fresh rereview

```text
candidate: PMR-007-CJID-1 V2
frozen packet: PMR-007_DEEP_BE_V2_FROZEN_HASHES.sha256
review relation: distinct implementation, same-model procedural rereview
external independence: NOT CLAIMED
result: PASS_WITH_NONBLOCKING_EVIDENCE_AND_ANTI_UNIFICATION_NOTES
```

## Custody

```text
frozen hash rows checked: 6
hash mismatches: 0
```

## Failed rereview implementations preserved

Two earlier fresh-rereview harnesses exceeded the 120-second execution window:

```text
pmr007_deep_be_distinct_walsh_rereview_v2.py
pmr007_deep_be_distinct_modular_walsh_rereview_v3.py
pmr007_deep_be_distinct_bitset_walsh_rereview_v4.py
```

They are preserved with the optimization log.  No PASS was inferred from those
runs.

## Successful independent mechanism

The V5 rereview used bitset Gaussian elimination over `GF(2)` to certify the
rank of the one-coordinate-deletion marginal constraints.  Since the explicit
rational parity vector lies in the kernel, a modular rank of `2^k-1` proves the
rational nullspace is exactly one-dimensional.

```text
arities checked: k=2 through k=9
all ranks: 2^k - 1
rank failures: 0
rational parity-null failures: 0
```

The rereview then generated exact integer-count parity perturbations at arities
two through nine and independently checked all one-coordinate-deletion
marginals, the total-variation/parity-moment identity, and parity loss under a
proper projection.

```text
higher-arity integer trials: 1,000
higher-arity failures: 0
parity-erasing projection failures: 0
```

A separately generated equal-marginal two-binary portfolio checked the exact
coupling formula:

```text
two-binary trials: 5,000
strict coupling cases: 3,413
formula failures: 0
```

## Scope and significance rereview

The theorem supplies a real cross-lane discriminator structure, not a personal
or explanatory-unification theorem.  It changes Candidate G's burden from
`put the desired coordinates in one bearer` to `derive a preregistered joint
restriction that the matched rival cannot reproduce`.

The strongest impersonal rival survives whenever it can match the same joint
law, or whenever the joint object is manufactured by unit mismatch,
source/version drift, post-selection, or candidate-dependent representation.

The OSM and PRH materials are used only as method comparators.  Neither supplies
personal-versus-impersonal likelihoods or a metaphysical world bridge.

## Nonblocking notes

1. General mathematical novelty remains zero; the finite result belongs to
   standard contingency-table and Walsh-interaction theory.
2. Held-out predictive or interventional evidence is still absent for the
   personal/impersonal architecture pair.
3. Causal, derivational, intentional, and explanatory interpretations of a
   coupling require further premises.
4. External statistical and scientific review remains open.

## Disposition

```text
PASS_WITH_NONBLOCKING_EVIDENCE_AND_ANTI_UNIFICATION_NOTES
```
