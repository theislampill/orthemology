# PMR-007 Frontier Round 19 V2 — distinct fresh rereview

```text
review relation: SAME-MODEL PROCEDURALLY DISTINCT
candidate frozen by: PMR-007_FRONTIER_ROUND19_V2_FROZEN_HASHES.sha256
result: PASS_WITH_NONBLOCKING_AUTHORITY_AND_NOVELTY_NOTES
external independence: NO
```

## 1. Custody

```text
frozen files checked: 7
hash mismatches: 0
```

The rereview used only the frozen V2 packet, model, primary checker/results,
V1 audit, V2 repair log, and prior-art note.

## 2. Independent exact minimax

The rereview reimplemented the decision problem using a depth-feasibility
solver rather than the primary checker's value recursion.  It generated every
labelled partial matching and searched for the least decision-tree depth.

| `(m,n,t)` | Labelled worlds | Exact depth | Formula |
|---|---:|---:|---:|
| `(1,1,1)` | 2 | 1 | 1 |
| `(2,2,1)` | 7 | 4 | 4 |
| `(2,2,2)` | 17 | 3 | 3 |
| `(2,3,2)` | 37 | 5 | 5 |
| `(3,2,2)` | 37 | 5 | 5 |
| `(3,3,2)` | 139 | 8 | 8 |
| `(3,3,3)` | 352 | 6 | 6 |

```text
minimax mismatches: 0
```

## 3. Piecewise upper-bound rereview

The V2 piecewise budget and all three row-scan branches were independently
evaluated for every

```text
1 <= m,n <= 100
1 <= k <= min(m,n).
```

```text
branch cases: 338,350
branch-bound failures: 0
```

The repair correctly avoids applying the closed formula to an impossible
residual demand.

## 4. Online lower-reduction rereview

A separate randomized harness generated partial matchings, query sequences with
repeated edges, cached positive labels, and post-transcript full label
completions.

```text
trials: 50,000
transcript-consistency failures: 0
threshold-equivalence failures: 0
```

The essential proof point survives: for every binary matching and the actual
transcript produced by the simulation, there exists one fixed complete label
map consistent with the transcript such that

```text
root_count >= t  iff  matching_cardinality >= t.
```

Repeated queries receive the cached label and do not create false roots.

## 5. Strongest-reading attacks

### More informative labels lower the worst case

Rejected.  The algorithm may exploit repeated labels on some inputs, but the
online lift supplies a worst-case family in which newly discovered positives
receive fresh labels.  Any faster root-threshold algorithm would yield a faster
Candidate 1 algorithm.

### Alphabet size must scale with `mn`

Rejected.  The lower lift uses only `t` fixed labels; labels beyond the first
`t` are unnecessary for the threshold reduction.

### Binary membership is sufficient

Rejected by the support-identical two-edge collision.  The rereview separately
constructed both binary projections and obtained identical transcripts with
opposite `t=2` root verdicts.

### Root-label count establishes evidential independence

Rejected.  Canonical distinctness is only the theorem's target predicate.
Independence, common ancestry, source truth, authority, and recipient warrant
are outside the oracle model.

### Randomized, distributed, or common-knowledge bounds follow

Rejected.  No such transfer is proved.

## 6. Ancestry and novelty disposition

```text
Candidate 1 relation:
TIGHT_ORACLE_ENRICHED_EXTENSION_AND_REDUCTION

AR2/AR3 relation:
FORMAL QUERY-COMPLEXITY INTERFACE ONLY

PRR-T1 / TAC / SAC identity:
NOT ASSIGNED

exact external prior theorem:
NOT LOCATED IN BOUNDED SEARCH

exhaustive prior-art review:
NOT PERFORMED

general mathematical novelty:
NOT ESTABLISHED
```

The result is theorem-strength and changes a central Candidate-A burden, but its
formula and lower mechanism inherit Candidate 1.  It is not eligible for
meniscus credit without external mathematical and prior-art review.

## 7. Final rereview disposition

```text
proof at declared finite deterministic scope: PASS
primary executable evidence: PASS
blocking V1 findings: CLOSED
fresh rereview: PASS_WITH_NONBLOCKING_AUTHORITY_AND_NOVELTY_NOTES
external review: OPEN
owner adoption: PENDING
historical identity: NONE
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
natural closure: NOT_REACHED
```
