# AR8R Candidate 1 exact dossier — current post-merge custody

## Canonical statement

Let `M` be an unknown arbitrary partial matching in the complete bipartite graph `K_{m,n}`. An adaptive deterministic algorithm may query individual edges for membership in `M` and must decide whether `|M| ≥ t`, where `1 ≤ t ≤ min(m,n)`.

The preserved exact deterministic decision-tree depth is

\[
D_{m,n,t}=mn-\binom{t}{2}.
\]

```text
status: ESTABLISHED_BUT_EXTERNAL_REVIEW_OPEN
historical identity: Candidate 1 / C1
conflation with PRR-T1 or M11–M13: PROHIBITED
```

## Upper-bound architecture

A recursive row scan queries one residual row. If a positive edge is found, its endpoints are committed and deleted; the residual threshold decreases by one. If no positive edge is found, that row is removed. The charging schedule leaves exactly `binom(t,2)` queries unneeded in the worst case.

## Lower-bound architecture

Maintain:

```text
P: committed positive matching
G: residual bipartite graph on unused endpoints
r = t - |P|: residual demand
invariant: ν(G) ≥ r
```

For a queried residual edge `e`:

```text
answer 0 if ν(G-e) ≥ r;
otherwise answer 1, commit e, delete its endpoints, and decrement r.
```

At a forced-positive stage, `ν(G-e) ≤ r-1`. By Kőnig's theorem, `G-e` has a vertex cover of size at most `r-1`. The complement rectangle, together with the forced positive edge, supplies a disjoint query charge. Summed over the positive stages and the final residual rectangle, the charge is:

\[
\sum_{p=0}^{t-2}(m+n-t-p)+(m-t+1)(n-t+1)
=mn-\frac{t(t-1)}2.
\]

The adversary keeps both a positive and a negative completion alive until the terminal stage.

## Exact evidence located

| Evidence | Status | Scope |
|---|---|---|
| `CHAMPION_CHALLENGER_ROUND_1.md` | located | statement, proof architecture, 26-case check |
| `CANDIDATE1_PROOF_AUDIT_B_LOWER.md` | located | cold lower-bound reconstruction, consistency and charging proof |
| `R_EXECUTABLE_MODELS/w1_adversary_audit.py` | referenced by audit | executable path not mounted in current local runtime |
| 26 rectangular instances through order five | preserved in audit result | finite evidence only |
| owner four-case independent check | assertion located, raw output not located | `OWNER_ASSERTED_RECEIPT_NOT_YET_EXACTLY_LOCATED` |

## Proof-authority status

```text
human proof: preserved and independently reconstructed at historical scope
finite executable check: preserved for 26 instances
current rerun: NOT PERFORMED — executable bytes not mounted
Lean source: exact Candidate 1 Lean module not located in current local corpus
Lean parse/elaboration/kernel: NOT ESTABLISHED
external mathematical review: OPEN
exhaustive prior-art review: OPEN
```

## Theorem-family relation

Candidate 1 is a finite zero-error query-complexity result. Its method interacts with reachability, profile, provenance, and collective-access lanes, but it is not identical to:

```text
PRR-T1 provenance/nonindependence
M11 invariant-confluence
M12 six-guard normalization
M13 fixed-warrant quotient factorization
AR-T4 finite discrimination
T366 profile factorization
```

Current relation to those families remains `UNRESOLVED` or `APPLICATION_ONLY` unless exact statements are compared.

## Prior-art obligations

The review packet must compare the exact neutral theorem against:

- decision trees for monotone properties on matching/chessboard complexes;
- evasiveness and matching-cardinality threshold results;
- promised query complexity for partial matchings;
- rectangular and threshold-parametric variants;
- randomized/expected refinements already present in later AR8R records.

No meniscus, dissertation, or general-new-theory credit is assigned before that review.

## Next bounded operation

Prepare one external-review packet containing the exact statement, full upper and lower proofs, checker source/results, scope restrictions, and a search protocol. External transmission remains owner-gated.
