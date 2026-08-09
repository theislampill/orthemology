# Deep CT V1 cold audit

```text
candidate: PMR-007-PCDF-1 V1
review relation: same-model-lineage cold audit over frozen V1
primary-check disposition: FAIL_COUNTEREXAMPLE_FOUND
overall disposition: REPAIR_REQUIRED
```

## Blocking findings

### CT-F01 — nonimplementation can itself become an observed discriminator

V1 said that a proper implementation domain prevents target identification even
when nonimplementation is recorded as `⊥`. This is false. If availability is
`0,0,0,1` and the target is `0,0,0,1`, the availability/`⊥` pattern identifies
the target exactly. The primary checker produced eight explicit witnesses.

### CT-F02 — domain restriction and totalized observation were conflated

An experiment defined only on `D_a` yields evidence only over that restricted
class. Totalizing it with an availability bit creates a different experiment on
all of `M`. The two cases require separate statements.

### CT-F03 — a separating availability bit may be target leakage

The V1 counterexample is evidentially useless when availability was defined as
the desired target or an architecture label. Mathematical separation is not an
independent capability certificate.

### CT-F04 — independently observed capability is a new anchor

When nonimplementation is certified by a target-blind common test, that
certificate is additional evidence. It must pass the same profile-fibre,
typing, semantics, version, authorization, resource, and implementation gates;
it is not a free consequence of partiality.

### CT-F05 — common-postprocessing boundary was unstated

If both availability and realized outcome are functions of the current profile
`E`, bottom-totalization is itself a common postprocessing of `E` and cannot
split an existing target conflict. This exact residual should be proved.

### CT-F06 — empirical missingness and causal overlap were not separated

Architecture-dependent nonimplementation can resemble missing-not-at-random
selection or lack of intervention positivity. Neither statistical analogy
licenses interpreting absence as a substantive target value without a frozen
observation and semantics contract.

## Required repair

Replace V1 with a three-way domain/capability fork:

1. **restricted-domain evidence** identifies only the restricted target;
2. **independently certified totalization** is a new experiment and succeeds
   exactly by the ordinary fibre criterion;
3. **target-defined totalization** is circular even when it separates.

Prove the common-postprocessing barrier, preserve the V1 counterexample, and
state the current U/I/P application without treating a target-laden personal
operation as a neutral common intervention.
