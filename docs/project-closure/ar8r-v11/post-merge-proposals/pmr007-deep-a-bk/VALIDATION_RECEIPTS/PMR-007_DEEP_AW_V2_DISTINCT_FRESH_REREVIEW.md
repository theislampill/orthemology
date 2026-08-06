# PMR-007 Deep AW V2 distinct fresh rereview

```text
identity: PMR-007-PRAD-1
candidate: PMR-007_DEEP_ROUND_AW_PROVENANCE_ROOT_ROBUST_DIAGNOSIS_V2.md
review relation: distinct same-session procedural rereview
external independence: NOT CLAIMED
disposition: PASS_WITH_NONBLOCKING_AUTHORITY_AND_DYNAMIC_SCOPE_NOTES
```

## 1. Frozen-hash custody

The rereview verified the six frozen V2 owners recorded by
`PMR-007_DEEP_AW_V2_FROZEN_HASHES.sha256` before evaluating the theorem.

```text
files checked: 6
hash mismatches: 0
```

## 2. Independent method

The primary checker enumerated binary root-level codebooks and compared the
candidate distance criteria against direct ambiguity semantics.  This rereview
used a separate ternary-alphabet construction and independently generated:

```text
unmarked substitution ambiguity sets;
marked-erasure projection classes;
selected-root pair-separation multiplicities;
and Hamming-distance thresholds.
```

It did not call the primary checker as an oracle.

## 3. Results

```text
exhaustive ternary codebooks: 19,683
substitution-characterization failures: 0
erasure-characterization failures: 0

random codebooks: 15,000
random substitution failures: 0
random erasure failures: 0

root-subset multicover cases: 45,000
subset criterion failures: 0
```

Mandatory controls also passed:

```text
distance two:
  corrects one marked erasure: true
  corrects one unmarked substitution: false

distance three:
  corrects one unmarked substitution: true

within-root multiplicity:
  many tests/copies from one actual root remain one alphabet symbol
  and one Hamming coordinate.
```

## 4. Scope and authority rereview

The exact finite theorem is supported at the declared scope:

```text
f unmarked adversarial root substitutions:
  exact diagnosis iff d_R >= 2f+1;

f marked root erasures:
  exact diagnosis iff d_R >= f+1;

minimum selected-root portfolio:
  pair-separation multicover with multiplicity 2f+1 or f+1.
```

The following remain outside the result:

```text
root authentication;
actual acquisition independence;
source truth;
tawatur warrant;
recipient authority or adoption;
common knowledge;
stochastic or adaptive querying;
dynamic membership or version drift;
mobile corruption;
collusion;
and stable noetic restoration.
```

The proof mechanism is standard Hamming-distance error/erasure correction plus
Test Cover/pair multicover.  General mathematical novelty remains zero.

## 5. Final disposition

```text
fresh rereview:
PASS_WITH_NONBLOCKING_AUTHORITY_AND_DYNAMIC_SCOPE_NOTES

blocking findings remaining:
0

repository integration:
NOT AUTHORIZED

external review:
OPEN

owner adoption:
PENDING
```
