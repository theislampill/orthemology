# PMR-007 Deep BB V1 cold audit

```text
disposition: REPAIR_REQUIRED
candidate: PMR-007-JCIQ-1 V1
primary executable result: PASS
review relation: same-program cold audit over frozen bytes
external independence: NOT CLAIMED
```

## Blocking findings

### BB-F01 — raw product deficit is not an integration measure by itself

The primary checker found 4,374 systems in which the two interfaces were exact
duplicates, had more than one quotient state, and nevertheless had positive
`D_raw`.  This is mathematically correct: diagonal support is a proper subset
of a product.  It also shows that `D_raw` cannot be called explanatory
integration without an independently warranted product-null comparison and
nonduplicate typing.

### BB-F02 — support restriction is not derivation

A proper joint image may result from a definitional relation, sampling
restriction, omitted latent coordinate, unreachable state, target encoding, or
version contract.  V2 must separate:

```text
raw nonproduct support;
dynamic invariance;
causal/derivational explanation;
metaphysical unity.
```

### BB-F03 — completeness guards are load bearing

The theorem is exact only for the complete declared finite state system and all
permitted actions.  A sample of observed joint profiles may have a positive
deficit even when the full admissible state space is a product.

### BB-F04 — cardinal deficit is not comparable across arbitrary registries

Duplicating, splitting, or coarsening an interface changes the product size.
`D_raw` and its normalized ratio may be reported only inside one fixed typed
registry; they are not architecture scores across arbitrary coordinate
choices.

### BB-F05 — dynamic subdirectness does not identify causal direction

Action invariance shows closure of the joint image under declared transitions.
It does not say which coordinate grounds another, whether the coupling is
causal, or whether one bearer owns the interaction.

### BB-F06 — pairwise tests are incomplete for higher arity

The parity control correctly shows that all pairwise projections can be full
while the complete joint image is proper.  V2 must preserve this as a warning
against pairwise-only unification audits.

### BB-F07 — personal/impersonal parity remains

Every formal object in the theorem can be realized by a rigid impersonal law or
coupled plural system.  Candidate G gains a nonproduct constraint, not a
personal-ground discriminator.

## Nonblocking notes

The common-refinement and subdirect-product results are standard universal
algebra / automata consequences.  General mathematical novelty is zero.
