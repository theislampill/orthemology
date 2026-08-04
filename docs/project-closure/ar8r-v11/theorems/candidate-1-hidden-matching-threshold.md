# Candidate 1 — exact hidden-matching threshold complexity

Status: exact recovered historical theorem packet; non-adopted research theorem; not peer reviewed.

## Typed setting

Let `1 <= t <= min(m,n)`. An unknown arbitrary partial matching `M` in the complete bipartite graph `K_{m,n}` is accessed by adaptive deterministic edge-membership queries. A query asks whether one declared edge belongs to `M`. The decision problem is whether `|M| >= t`.

## Exact statement

The exact worst-case deterministic decision-tree depth is

```text
D(m,n,t) = mn - binom(t,2).
```

## Row-scan upper bound

Scan one row until either a positive edge appears or the row is exhausted.

- On a positive answer, delete its row and column and decrement the residual demand.
- On an exhausted row, delete only that row.

The resulting rectangular recurrence, including endpoint cases, closes at `mn - binom(t,2)`.

## Adversary lower bound

Maintain a committed matching together with a residual graph of still-possible positive edges whose matching number is at least the residual demand.

Answer zero unless deleting the queried edge would destroy every residual matching of the required size. In that essential-edge case, answer one and commit the edge. At each positive stage, a minimum vertex cover supplied by König's theorem charges at least `a+b-r-1` earlier zero answers plus the positive answer. Deleting both endpoints makes the charged sets disjoint. The final residual rectangle contributes all its remaining edges. Summing the charges gives `mn - binom(t,2)`.

The consistency obligations are:

- every zero remains compatible with the final committed matching;
- every committed positive is essential to every required residual matching at that stage;
- deleting its endpoints leaves the decremented demand feasible;
- no charged edge is reused after an endpoint is removed; and
- all rectangular cases, endpoints, adaptivity, and termination remain inside the typed setting.

## Additional bounded result

The deterministic nonadaptive depth is `mn`; adaptivity therefore saves exactly `binom(t,2)` queries in this model.

A scoped randomized lower bound of order `(m-t+1)(n-t+1)` survives the historical audit, but exact randomized complexity remains open.

## Executable evidence and count reconciliation

An exact V8 result file with SHA-256
`267cc7c06efd844408f3aca9833c3ea56dbe416a0898d065bcaf65f330fc2bfd`
records 29 parameter triples, covering rectangles with at most 12 edges. For
every listed case, exact minimax depth and row-scan worst-case depth both equal
the displayed formula.

The later exact PMR-001 dossier separately describes a historical 26-instance
check and does not expose the executable bytes in that packet. The 26- and
29-instance records are preserved as distinct evidence surfaces; V11 does not
claim they are the same checker run or merge their custody. The public 29 count
comes only from the exact V8 result file. Both counts are bounded finite evidence,
not proof substitutes.

## Audit and prior-art boundary

Two candidate-specific cold reconstructions reported the proof globally consistent. The prior-art disposition was `STRENGTHENED_RECTANGULAR_THRESHOLD_VARIANT` with moderate confidence. Nearby work concerned complete reconstruction, broader set-query models, unrestricted matching properties, or general evasiveness. Failure to locate the same formula in the same promise/query model is not an originality finding.

External mathematical review: open.

Exhaustive prior-art review: open.

Owner adoption: pending.

This theorem is not a meniscus result and does not establish any broader orthemological, empirical, metaphysical, or implementation claim.

## Post-merge provenance-root extension

The sanitized PMR-007 Round 19 proposal contains `PMR-007-PRQT-1`, an
oracle-enriched threshold problem in which positive edge queries return
canonical root labels. Its exact depth has the same displayed formula under its
additional label and authentication assumptions. The proposal classifies it as
a tight extension/reduction with zero second historical origin, open external
mathematical and prior-art review, and pending owner adoption. It is not merged
into Candidate 1's historical payload.
