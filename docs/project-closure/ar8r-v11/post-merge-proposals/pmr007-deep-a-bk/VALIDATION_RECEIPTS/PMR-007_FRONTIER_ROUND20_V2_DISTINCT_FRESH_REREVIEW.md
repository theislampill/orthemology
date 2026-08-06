# PMR-007 Frontier Round 20 V2 — distinct fresh rereview

```text
review relation: SAME-MODEL PROCEDURALLY DISTINCT
candidate frozen by: PMR-007_FRONTIER_ROUND20_V2_FROZEN_HASHES.sha256
result: PASS_WITH_NONBLOCKING_SCOPE_AND_ANCESTRY_NOTES
external independence: NO
```

## 1. Frozen custody

```text
frozen files checked: 7
hash mismatches: 0
```

The rereview used the V2 frozen packet and did not modify it.

## 2. Independent semantics

The primary checker computes hypergraph transversals from explicit root sets and
then compares `kappa > f` to direct corruption enumeration. The rereview used a
separate bitmask implementation and compared two independently computed
quantities:

```text
pathwise minimum transversal size;
least corruption-mask size that uncovers at least one path.
```

Results:

```text
single-path hypergraph families:     32,906
single-path failures:                     0
all two-path systems on three roots: 16,384
two-path failures:                        0
random multi-path systems:           50,000
random failures:                          0
root-contraction cases:           1,662,078
root-contraction failures:                0
```

## 3. Strongest-reading controls

The rereview reconstructed the controls from the model rather than trusting the
primary result labels.

```text
incompatible-repair compatible cover: ABSENT
rerouting-created p1:                 SURVIVES
every post-commitment action:         DEFEATABLE WITH ONE ROOT
omitted path blocker:                 ABSENT
displayed x/y actual-root image:      ONE ROOT
positive construction margin:        3
```

Therefore the exact equivalence survives while every stronger execution,
dynamic, adaptive, unauthenticated, or incomplete-registry reading fails.

## 4. Quantifier and semantics audit

```text
static theorem:
forall corruption C with |C| <= f,
forall registered path p,
exists surviving blocker a.

post-commitment rival:
exists committed a,
forall allowed corruption C,
a survives.
```

The latter does not follow from the former. Nor does pathwise support imply one
jointly executable compatible action set. The theorem's conjunctive-integrity
semantics is explicit: corruption of any required root disables an action.

## 5. Ancestry and novelty

The mathematical mechanism is the standard transversal-number characterization
of the least hitting set. Minimizing it across registered paths is a direct
product/minimum construction. The domain-specific value is its typed use as a
false-multiplicity and model-relative restoration-resilience interface.

```text
general mathematical novelty: ZERO
historical identity: NONE
T351/T352 relation: STRICT_SPECIALIZATION_AND_COMPOSITIONAL_COROLLARY
T353 relation: GOVERNOR/OUTPUT NONRESTORATION CONTROL REMAINS
Round 19 relation: AUTHENTICATED-ROOT ACCESS INTERFACE ONLY
```

## 6. Final disposition

```text
proof at declared finite static fixed-path scope: PASS
primary executable evidence: PASS
V1 blocking findings: CLOSED
fresh rereview: PASS_WITH_NONBLOCKING_SCOPE_AND_ANCESTRY_NOTES
external review: OPEN
owner adoption: PENDING
historical identity: NONE
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
natural closure: NOT_REACHED
```
