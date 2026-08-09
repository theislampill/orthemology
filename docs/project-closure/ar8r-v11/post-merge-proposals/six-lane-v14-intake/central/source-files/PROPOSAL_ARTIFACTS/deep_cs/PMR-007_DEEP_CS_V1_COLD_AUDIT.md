# Deep CS V1 cold audit

```text
disposition: REPAIR_REQUIRED
candidate: PMR-007-WADF-1 V1
review relation: same-model-lineage cold audit over frozen V1
```

## Blocking findings

### CS-F01 — unique weakest discriminator is false

The exhaustive partition check found 210 four-model `(E,Q)` cases with more
than one incomparable minimal sufficient refinement. A finite admissible family
has minimal elements when nonempty, but uniqueness requires a separate order or
cost premise.

### CS-F02 — Bennett's theorem was imported outside its domain

Bennett's result is conditional on a finite implementable language, his task
formalism, extension-cardinality weakness, and a uniform task distribution.
Candidate evidence refinements over an architecture model class are not those
objects. The partition theorem must stand on its own; Bennett can at most
motivate a guarded research heuristic.

### CS-F03 — weakness alone can be vacuous

The constant map is maximally coarse but leaves every current architecture
collision unresolved. The policy must require sufficient discrimination in
addition to minimal commitment.

### CS-F04 — discrimination alone can be target leakage

`r=Q` always separates the target, but it reads the desired answer. Eligibility,
target blindness, version, authority, and implementation semantics must be
independently checked.

### CS-F05 — residuals do not generally have one correction term

The balanced-EF1 order-statistic correction succeeds because a specific
algebraic residual, shift invariance, and sign inequality are proved. It does
not establish a theorem that every recurrent AR8R residual has a unique scalar
or even any admissible correction.

### CS-F06 — information gain and cost are not canonical

Expected information gain requires a probability model; cost requires a unit
and accounting rule. Neither follows from partition order.

### CS-F07 — map and partition equivalence need quotient typing

Candidate maps that induce the same joint partition are equivalent at the
current discrimination surface. Minimality should be stated over induced
partitions/equivalence classes rather than raw labels.

## Required repair

- prove only the finite admissible-refinement characterization;
- permit multiple incomparable minimal candidates or no candidate;
- separate independent partition mathematics from Bennett's conditional result;
- classify the balanced-EF1 transfer as a proof-search heuristic/countermodel
  pattern only;
- retain target leakage, vacuous weakness, representation sensitivity, and
  nonunique-minimum controls;
- give the current U/I residual disposition without inventing a discriminator.
