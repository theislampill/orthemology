# PMR-007 Frontier Round 14 V2 fresh rereview

```text
review relation: same-model procedurally distinct rereview over frozen V2 and cold-audit hashes
external human review: false
independent model-lineage review: false
disposition: PASS_WITH_NONBLOCKING_SCOPE_NOTES
```

## Frozen packet

The rereview reproduced the frozen candidate, primary checker, primary results,
and cold-audit hashes exactly. It did not import or call the primary checker.

## Independent method

The rereview used a second implementation with:

```text
set-valued outer and inner fixed-point approximants;
Tarjan strongly connected components for direct temporal semantics;
explicit enumeration of every memoryless strategy;
and extraction of the candidate's outer-rank strategy.
```

A strategy was accepted from a start exactly when all reachable states were
safe and no reachable directed cycle contained a non-target state.

## Exhaustive result

```text
Safe/Bad/Target-labelled games:           157,611
memoryless strategies checked:            804,585
formula/direct temporal mismatches:              0
rank-strategy extraction failures:               0
W_core subset failures:                          0
strict W_core subset W_coB cases:              300
```

The rereview exhausted every nonempty antichain-reduced action-menu game with
one, two, or three states. It also checked 6,000 deterministic random four- and
five-state games and 124,525 memoryless strategies with zero mismatch or rank
failure.

## Mandatory regression

`R14-F01` passed under the independent implementation:

```text
K      = {0}
W_core = {0,1}
W_coB  = {0,1,2}
```

Round 14 V1 therefore remains blocked. V2 does not erase or relabel the defect.

## Proof rereview

The two proof directions survive:

1. The outer least-fixed-point rank is nonincreasing at target states and
   strictly decreases after each bad state. Hence only finitely many bad visits
   are possible.
2. In a finite memoryless winning graph, a reachable bad-containing cycle
   would be an adversarial lasso violating co-Büchi. Absence of such cycles
   gives a finite bad-visit bound and the `R_k` post-fixed-point induction.

The fixed point is exact only relative to the declared game and predicates.

## Authority and nonclaims

The admitted scope does not establish:

```text
partial-observation or asynchronous sufficiency;
common-state construction;
randomized/probabilistic objectives;
dynamic-membership closure;
source truth;
target adequacy;
causal burden landing;
actual noetic restoration;
daee runtime implementation;
world or metaphysical truth;
external review;
or general mathematical novelty.
```

The standard co-Büchi mechanism receives zero general theorem novelty. The
post-merge contribution is the validated architecture repair and the typed
separation between one invariant-core certificate and branch-dependent eventual
persistence under locally eligible protocol fragments.

## Final disposition

```text
COB-1:
ADMITTED_POST_MERGE_SCOPED_RESULT

Round 14 V1:
BLOCKED_FORMAL_DEFECT
NOT_REPOSITORY_READY
PRESERVED_REJECTED_EVIDENCE

external review:
OPEN

owner adoption:
PENDING

repository proposal eligibility:
ELIGIBLE_FOR_SANITIZED_PROPOSAL
NOT AUTHORIZED FOR REPOSITORY INTEGRATION

integrated champion:
NONE

meniscus:
MENISCUS_NOT_REACHED

PMR-007 closure:
NOT ELIGIBLE
```
