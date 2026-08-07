# PMR-007 Deep Round I V1 cold audit

```text
audited candidate: PMR-007-OAS-1-CANDIDATE-V1
frozen hash receipt: PMR-007_DEEP_I_V1_FROZEN_HASHES.sha256
disposition: REPAIR_REQUIRED
```

## Independent recomputation

The fixed-point obstruction is valid: an equivariant selector must be fixed by every automorphism stabilizing the input order. A fixed-point-free action on the eligible fibre therefore blocks neutral unique selection. The primary partition checker is consistent with the proof at its declared full-symmetric-orbit scope.

## Blocking findings

### DI-F01 — empty-sort countermodel is semantically underspecified

`I-CM1` uses `X=∅`. Standard many-sorted first-order semantics often requires every sort to be nonempty. The nonentailment does not need an empty sort: use one or more concrete candidates with an empty applicability/actualization fibre. Until repaired, the model is framework-sensitive.

### DI-F02 — fixed-point sufficiency overstates what was proved

A unique globally fixed element is the sole automorphism-invariant *candidate inside one frozen structure*. V1 describes this as if it automatically generated a selector over an arbitrary class of structures. A class-level equivariant selector additionally needs a uniform isomorphism-invariant rule or a restricted domain in which the unique fixed candidate is functorially identified. The theorem should separate:

```text
within-structure necessity;
within-isomorphism-class eligibility;
and a uniform selector over a variable model class.
```

### DI-F03 — applicability and realization are conjoined too early

The candidate defines `C_o=Applies∧Actualizes`. That is sufficient for the selection theorem, but it obscures two independent bridge failures requested by the program:

```text
order -> applicability;
applicability -> concrete efficacy.
```

A model may have a nonempty applicability fibre and an empty actualization fibre. Add this deletion model and state separate fibres.

### DI-F04 — symmetry obstruction is not a metaphysical multiplicity theorem

The proof blocks a unique **neutral-structure-equivariant selection**. It does not prove that reality lacks one numerically unique realizer; a unique but neutrally indiscernible realizer may be posited through haecceity, source predication, or inaccessible structure. The candidate generally respects this distinction, but the title, positive condition, and terminal summary require an explicit epistemic/formal versus metaphysical firewall.

## Nonblocking notes

1. The theorem is a standard group-action/equivariance fact; general mathematical novelty is correctly zero.
2. The primary checker covers full symmetric actions on orbit partitions, not arbitrary subgroups. The proof covers arbitrary groups, so this is acceptable if a distinct rereview checks randomly generated finite subgroups.
3. Candidate G parity and Track-N nonmigration are correctly preserved.

## Required repair

```text
replace empty-sort witness;
separate applicability and efficacy fibres;
narrow the positive fixed-point statement;
state the neutral-selection/metaphysical-uniqueness firewall;
add arbitrary-subgroup fresh rereview;
freeze V2 and rereview.
```
