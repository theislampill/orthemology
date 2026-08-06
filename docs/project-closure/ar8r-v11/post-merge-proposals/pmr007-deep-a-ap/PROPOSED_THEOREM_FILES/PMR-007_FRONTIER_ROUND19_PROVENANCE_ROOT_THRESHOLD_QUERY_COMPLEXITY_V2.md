# PMR-007 Frontier Round 19 V2 — provenance-root threshold query complexity

```text
round: PMR-007-FRONTIER-ROUND19
candidate identity: PMR-007-PRQT-1
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
current disposition: REPAIRED_FROZEN_PENDING_FRESH_REREVIEW
repository mutation: NONE
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```

## 1. Central Candidate-A burden

Candidate 1 exactly determines the deterministic edge-query cost of deciding
whether an unknown partial matching contains at least `t` edges.  A provenance-
bearing agentic setting is harder in one respect and richer in another:
positive edges may repeat a common acquisition root, while a query may expose a
canonical root label rather than only membership.

Round 19 asks the exact finite zero-error question:

> How many edge queries are necessary and sufficient to decide whether an
> unknown labelled partial matching contains at least `t` distinct canonical
> provenance roots?

This is not a theorem about whether the labels are truthful, whether different
labels are evidentially independent, or whether a recipient may adopt the
reported claim.  Those are separate source, custody, and warrant contracts.

## 2. Typed oracle model

Let `L=[m]`, `R=[n]`, and let `E=L x R`.  An input is:

```text
M subseteq E:
  an arbitrary partial matching;

Lambda:
  a finite root-label alphabet;

lambda : M -> Lambda:
  a canonical label attached to every present edge;
  repetition is allowed.
```

The root count is

```text
roots(M,lambda) = |lambda(M)|.
```

A query to edge `e` returns

```text
BOTTOM       if e notin M;
lambda(e)    if e in M.
```

The query cost counts only edge-oracle calls.  The returned label is assumed to
be canonical, authenticated, and available at no additional query cost.  The
algorithm is deterministic, adaptive, and zero-error.  It must decide

```text
ROOTS_t(M,lambda) = 1  iff  roots(M,lambda) >= t.
```

Write `D_root(m,n,t;Lambda)` for the minimum worst-case depth.

## 3. Exact theorem PRQT-1

### Theorem

For positive `m,n`, a root alphabet with `|Lambda| >= t`, and

```text
1 <= t <= min(m,n),
```

one has

\[
D_{\mathrm{root}}(m,n,t;\Lambda)
=
mn-\binom{t}{2}.
\]

The full boundary convention is:

```text
t <= 0:
  the answer is identically true and the depth is 0;

t > min(m,n):
  a partial matching cannot contain t present edges, hence cannot contain
  t distinct root labels; the answer is identically false and the depth is 0;

|Lambda| < t:
  the answer is identically false and the depth is 0.
```

### Interpretation

Root-label repetition does not increase the worst-case deterministic edge-query
cost above Candidate 1 when positive replies expose exact canonical labels.  It
also does not decrease the cost: an adversarial binary matching instance can be
lifted online to a labelled instance that reveals fresh labels exactly when
needed.

## 4. Upper bound

For all integer residual parameters define the piecewise budget

\[
B(m,n,k)=
\begin{cases}
0, & k\le 0\text{ or }k>\min(m,n),\\
mn-\binom{k}{2}, & 1\le k\le\min(m,n).
\end{cases}
\]

Maintain the set `S` of already observed root labels.  Let `k` be the number of
additional distinct labels required:

```text
k = t - |S|.
```

The algorithm scans one residual row, querying at most `n` edges.

### Branch 1 — no positive edge in the row

Remove the row.  The residual state is `(m-1,n,k)`.  If
`k <= min(m-1,n)`, then

\[
n+B(m-1,n,k)=B(m,n,k).
\]

If instead deletion makes `k > min(m-1,n)`, the residual answer is
immediately false and costs zero.  The branch costs only `n`, and

\[
B(m,n,k)-n
=n(m-1)-\binom{k}{2}\ge 0,
\]

because `m,n >= k`.

### Branch 2 — a positive edge with a new label

Remove its row and column and decrement the remaining root demand.  The branch
cost is at most

\[
n+B(m-1,n-1,k-1).
\]

The slack against `B(m,n,k)` is

\[
B(m,n,k)-\left[n+B(m-1,n-1,k-1)\right]=m-k\ge 0.
\]

### Branch 3 — a positive edge with an already seen label

Remove its row and column but keep `k` unchanged.  If
`k <= min(m-1,n-1)`, the branch cost is at most

\[
n+B(m-1,n-1,k),
\]

with slack

\[
B(m,n,k)-\left[n+B(m-1,n-1,k)\right]=m-1\ge 0.
\]

If deletion makes the residual demand impossible, the algorithm returns false
immediately after the row scan.  Its cost is `n <= B(m,n,k)` by the same
inequality above.  Thus the branch bound remains valid without pretending the
closed-form formula applies outside its feasible residual domain.

The base cases are:

```text
k = 0:
  return true;

k > min(m,n):
  return false.
```

Induction proves the upper bound.  The old-label branch is essential: a
cardinality-threshold proof that decrements on every positive edge would be
unsound in the provenance-root problem.

## 5. Lower bound by online oracle lifting

Use the exact Candidate 1 problem as the source problem:

```text
unknown arbitrary partial matching M subseteq K_{m,n};
binary edge-membership queries;
decide |M| >= t.
```

Candidate 1 has preserved exact deterministic depth

\[
D_{m,n,t}=mn-\binom{t}{2}.
\]

Assume, toward a contradiction, that a deterministic root-threshold algorithm
`A` uses fewer queries.  Construct a binary membership algorithm `B` for
Candidate 1.

Fix `t` distinct labels

```text
alpha_1, ..., alpha_t in Lambda.
```

`B` keeps a cache from queried positive edges to their assigned labels.
Whenever `A` asks edge `e`, `B` proceeds as follows:

```text
if e is already in the positive-edge cache:
  return its cached label without advancing the fresh-label counter;

otherwise ask the binary oracle about e;

if the binary answer is 0:
  return BOTTOM to A;

if the binary answer is 1:
  if this is the j-th newly discovered positive edge and j <= t,
     cache and return alpha_j;
  otherwise cache and return alpha_t.
```

Hence repeated queries are label-consistent and the transcript is generated by
one fixed partial label map on all queried edges.

This online transcript is consistent with at least one complete label map on
the hidden matching:

```text
- every queried positive edge keeps its returned label;
- if |M| >= t but fewer than t positives were queried before A stops,
  assign the still-unused alpha labels to enough unqueried positive edges;
- label any remaining positives arbitrarily;
- if |M| < t, every label map has fewer than t distinct labels because
  there are fewer than t positive edges.
```

Therefore the completed labelled input satisfies

```text
roots(M,lambda) >= t  iff  |M| >= t.
```

Because `A` must be correct for every labelled input consistent with its
transcript, `B` decides Candidate 1 with the same query depth.  This contradicts
the exact Candidate 1 lower bound.  Hence

\[
D_{\mathrm{root}}(m,n,t;\Lambda)
\ge mn-\binom{t}{2}.
\]

Combined with the upper bound, this proves `PRQT-1`. ∎

## 6. Direct adversary interpretation

The reduction can also be read directly through the preserved Candidate 1
residual-matching adversary.  At its `p`-th forced positive stage, issue a fresh
root label `alpha_p`.  While `p<t`:

```text
negative completion:
  keep only the committed positive matching;

positive completion:
  use the residual matching invariant to add t-p unqueried edges and assign
  the remaining fresh labels.
```

Thus the root-bearing transcript preserves both a `<t`-root completion and a
`>=t`-root completion for exactly the same charged query depth.  This is an
interpretive inheritance of Candidate 1's lower-bound mechanism, not an
independent historical proof object.

## 7. Countermodels and authority firewalls

### R19-CM-MEMBERSHIP-ONLY

Let the support be two disjoint positive edges.  One labelled input assigns the
same root to both; another assigns different roots.  Every binary membership
answer is identical, while the `t=2` root-threshold verdict differs.

Therefore binary support access alone cannot decide root multiplicity, even
after all `mn` edge queries.

### R19-CM-SYMBOL-ALIAS

Two distinct printed labels may be aliases for one actual acquisition root.
Counting strings then overstates root multiplicity.

### R19-CM-SYMBOL-MERGE

One printed label may conflate two actual acquisition roots.  Counting strings
then understates root multiplicity.

### R19-CM-ROOT-NONINDEPENDENCE

Even authenticated distinct source roots need not be evidentially independent:
they may share a common upstream witness, dataset, training run, source packet,
or causal ancestor.  `PRQT-1` decides canonical-label multiplicity only.

### R19-CM-VERIFICATION-COST

If label authenticity or root equivalence requires additional queries, the
formula does not include those costs.  A richer cost model is a distinct
problem.

### R19-CM-RECIPIENT-CONTRACT

A root threshold does not establish target applicability, current version,
authority, capability, invalidator closure, adoption, execution, or writeback.
AR3-style recipient obligations remain separate.

## 8. Exact ancestry and family relation

### Candidate 1

```text
relation:
TIGHT_ORACLE_ENRICHED_EXTENSION_AND_REDUCTION

transferred:
finite partial-matching domain;
edge-query cost model;
row-scan architecture;
exact residual-matching lower bound;
threshold algebra mn - binom(t,2).

not transferred:
historical identity;
external review;
prior-art closure;
randomized or expected bounds;
provenance semantics;
evidential independence;
recipient warrant.
```

`PRQT-1` is stronger in input expressivity because root labels may repeat, but
its tight lower bound is inherited by an oracle-lifting reduction to Candidate
1.  It receives no duplicate Candidate 1 origin credit.

### AR2 / AR3

```text
relation:
FORMAL QUERY-COMPLEXITY INTERFACE TO PROVENANCE-BEARING TRANSPORT
```

AR2/AR3 supplies the reason-certificate, source, target, authority, version,
capability, permission, resource, and invalidator distinctions needed before a
label can function as a warrant-bearing provenance root.  `PRQT-1` does not
prove those guards.  It quantifies edge access only after canonical root labels
are independently defined.

### PRR-T1 and TAC/SAC

Exact historical statements are not assigned here.  The result supplies a
candidate lower/upper-bound interface for provenance multiplicity and copied-
availability studies, but no PRR-T1, SAC-T4, CC-T4, `orthemologous`, or
`paralemologous` identity is inferred.

## 9. Prior-art boundary

The bounded search located nearby but nonidentical objects:

```text
- deterministic, randomized, and quantum edge-query complexity for fully
  learning hidden perfect matchings;

- query and communication models for bipartite matching problems;

- explicit-graph rainbow matching and edge-coloured extremal problems;

- general decision-tree and graph-property query complexity.
```

The closest inspected hidden-matching paper learns an entire perfect matching,
not a threshold on distinct labels of an arbitrary partial matching.  The
rainbow-matching literature generally receives an explicit edge-coloured graph
and asks for a rainbow substructure, rather than learning a hidden labelled
partial matching through edge queries.

No exact prior theorem for `PRQT-1` was located in the bounded search.  This is
not an exhaustive literature review.  The external mathematical and prior-art
review burden remains open.

## 10. Novelty ceiling

```text
general mathematical novelty:
NOT ESTABLISHED

current value:
scoped exact extension of Candidate 1;
provenance-bearing query-complexity interface;
load-bearing Candidate-A result;
reusable authenticated-root oracle boundary.

historical theorem identity:
NONE
```

The formula itself retains Candidate 1's proof architecture.  The substantive
new content is the exact treatment of repeated canonical roots, the old-label
upper branch, the online oracle-lifting lower reduction, and the explicit
separation between root-label count and evidential independence.

## 11. Candidate A/B/C effects

### Candidate A

The result supplies an exact information-access cost for one authenticated
provenance-multiplicity predicate.  It sharpens the difference between:

```text
support availability;
root-label multiplicity;
independent acquisition;
recipient warrant;
and common knowledge of provenance.
```

### Candidate B

A restorative runtime that requires at least `t` distinct canonical roots
cannot infer that condition from support-only observations.  Its action/query
budget must include the root-bearing oracle contract or additional provenance
verification.

### Candidate C

Multiple argument presentations or source routes do not become independent
metaphysical support merely by being numerous.  The theorem supplies no
world-directed bridge and no source-truth conclusion.

## 12. Formalization opportunity

A Lean-ready development can separate:

```text
LabeledPartialMatching;
RootThreshold;
rowScanUpper;
onlineLabelLift;
Candidate1LowerTransfer;
rootThresholdDepth.
```

The lower reduction should be formalized as an oracle simulation rather than
by importing label semantics into the historical Candidate 1 theorem.

## 13. Current admission gates

```text
primary executable check:
PASS_AT_DECLARED_FINITE_SCOPE

cold audit:
V1_REPAIR_REQUIRED

blocking repair:
R19-F01 through R19-F04 CLOSED_IN_V2

fresh rereview:
PENDING

external review:
OPEN

owner adoption:
PENDING

repository proposal:
NOT YET CLASSIFIED
```
