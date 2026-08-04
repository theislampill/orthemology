# PMR-007 Frontier Round 20 V2 — distinct fresh rereview

```text
candidate: PMR-007-PRRC-1
rereview relation: distinct implementation over frozen V2 hashes
external independence: NOT ESTABLISHED
result: PASS_WITH_NONBLOCKING_SCOPE_AND_AUTHORITY_NOTES
```

## 1. Frozen custody

Every file listed in `PMR-007_FRONTIER_ROUND20_V2_FROZEN_HASHES.sha256`
matched its frozen digest.  The rereview did not amend the theorem while testing
it.

## 2. Independent semantic method

The primary checker constructed path-root families and compared the candidate
criterion to direct `f`-robustness.  The fresh rereview instead:

1. generated finite **action systems** with path sets and required-root sets;
2. computed the minimum corruption size that directly leaves some path without
   a surviving blocker;
3. computed each path's transversal number using a separate recursive
   backtracking solver;
4. compared the two minima;
5. separately tested duplication, portfolio enlargement, action deletion, root
   aliasing, redundant support, action incompatibility, and dynamic rerouting.

## 3. Results

```text
exhaustive action systems checked:
13,985

random action systems checked:
120,000

frozen-hash failures:
0

static theorem mismatches:
0

monotonicity failures:
0
```

The required scope-separation controls all fired:

```text
redundant alternative support:
  differs from conjunctive required-root semantics;

incompatible repairs:
  pathwise certificate true while joint execution false;

root-label aliasing:
  displayed failure budget 2, actual failure budget 1;

dynamic rerouting:
  fixed registered certificate true while dynamic restoration false.
```

## 4. Proof and necessity/sufficiency audit

The equivalence is exact at the declared static semantics because the minimum
corruption that disables all blockers of one path is definitionally the
minimum transversal of that path's required-root hypergraph.  The minimum over
paths gives the first path that can be exposed.

The theorem does not require pairwise root disjointness.  It correctly detects
more general bottlenecks through the transversal number.  It also handles:

```text
no blockers:
  tau=0, immediate failure;

root-independent blocker:
  empty hyperedge, tau=infinity;

copied blockers:
  no increase in the invariant;

partially overlapping required-root sets:
  exact finite hitting-set value.
```

## 5. Surviving scope notes

These are nonblocking because V2 states them as exclusions rather than hidden
assumptions:

- static corruption does not cover adaptive one-shot or history-dependent
  adversaries;
- fixed complete paths do not cover repair-created or hidden paths;
- pathwise availability does not cover incompatible or resource-conflicting
  actions;
- actual-root identity is an input contract, not a consequence;
- root resilience is one coordinate of restoration, not target truth, causal
  landing, custody, reread, or human/fiṭrī restoration;
- the theorem is not a tawātur-warrant result.

## 6. Theorem family and novelty disposition

```text
mathematical family:
finite hypergraph transversal / hitting-set characterization

AR8R relation:
compositional corollary/application of T351/T352 path structure

post-merge relation:
uses Round 19 canonical-root interface and Round 15 implementation boundary

general mathematical novelty:
0

historical identity:
NONE

eligible contribution:
scoped provenance-resilience certificate and false-multiplicity control
```

## 7. Admission recommendation

Admit exactly `PMR-007-PRRC-1` at the finite, static, fixed-path,
conjunctive-required-root, pathwise-certificate scope.  Retain external review,
owner adoption, implementation binding, root-authentication, dynamic-game, and
causal-restoration burdens as open.
