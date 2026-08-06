# PMR-007 Round 19 — bounded prior-art and theorem-family note

```text
candidate: PMR-007-PRQT-1
search class: bounded, nonexhaustive
historical theorem-origin authority: V5
external review: OPEN
```

## Exact internal ancestor

The controlling internal ancestor is the preserved Candidate 1 theorem:

```text
unknown arbitrary partial matching in K_mn;
binary edge-membership queries;
decide |M| >= t;
exact deterministic depth mn - binom(t,2).
```

Round 19 changes the oracle and target:

```text
present replies expose canonical labels;
labels may repeat;
target is number of distinct labels.
```

The upper proof adds an old-label branch.  The lower proof is an online oracle
lifting from Candidate 1.  The family relation is therefore:

```text
TIGHT_ORACLE_ENRICHED_EXTENSION_AND_REDUCTION
```

not `INDEPENDENT_RESULT`, not an exact historical recovery, and not a second
origin for the Candidate 1 formula.

## Nearby external objects inspected

### Hidden matching learning via edge queries

N. S. Mande, S. Sanyal, and V. Zamaraev, *Complexity of learning
matchings and half graphs via edge queries*, arXiv:2507.03151 (2025).

The paper studies full reconstruction of hidden perfect matchings and gives a
tight deterministic `n(n-1)/2` bound, a quadratic randomized order, and a
`Theta(n^(3/2))` quantum order.  Its input class, output requirement, and
threshold are different from Round 19:

```text
paper:
  full learning of a perfect matching;

Round 19:
  yes/no distinct-root threshold for an arbitrary partial matching with
  repeated labels.
```

### Bipartite matching communication and richer query models

J. Blikstad, J. van den Brand, Y. Efron, S. Mukhopadhyay, and
D. Nanongkai, *Nearly Optimal Communication and Query Complexity of
Bipartite Matching*, arXiv:2208.02526 (2022).

That work studies maximum-cardinality bipartite matching in two-party
communication and AND/OR/XOR/quantum query models.  It does not supply the
Round 19 labelled-partial-matching threshold theorem.

### Rainbow and edge-coloured matching literature

The bounded search found extensive work on rainbow subgraphs and rainbow
matchings in explicitly given edge-coloured graphs.  These results ask for the
existence, size, or complexity of a rainbow matching in an exposed graph.  They
do not, on the inspected evidence, determine the deterministic edge-query
depth of deciding a distinct-colour threshold in a hidden arbitrary partial
matching.

## Searches performed

The bounded search used combinations of:

```text
hidden colored matching edge query complexity distinct colors threshold;
rainbow matching query complexity hidden matching colors;
query complexity colored matching partial matching;
matching property decision tree threshold.
```

No exact `PRQT-1` statement was located.  Search-engine nonretrieval is not a
proof of novelty.

## Prior-art disposition

```text
exact external ancestor located:
NO

nearby matching-query work:
YES

nearby rainbow/edge-coloured work:
YES

exhaustive prior-art search:
NO

general mathematical novelty:
NOT ESTABLISHED

external mathematical review:
OPEN
```

## Scope firewall

No result from the external literature is imported as proof authority for
`PRQT-1`.  Conversely, `PRQT-1` is not represented as solving full matching
learning, maximum matching, randomized or quantum query complexity, rainbow
matching existence, or evidential-independence certification.
