# Deep CN V1 — authority-indexed anchor covers

## Candidate

```text
identity: PMR-007-AIAC-1
status: POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
```

Let `M` be a finite model class, `Q` a target coordinate, `C` a set of authority contexts, and `A_c` the anchors eligible in context `c`. Define `kappa_Q(c)` as the minimum number of eligible anchors whose joint values separate every pair of models with different `Q` values, and infinity if no such family exists.

The candidate claims:

```text
Q is identifiable in context c iff kappa_Q(c) is finite;

if A_c is included in A_d then kappa_Q(d) <= kappa_Q(c);

and an anchor eligible only in context d may not be used in c without an explicit authority transport.
```

Applications are proposed to:

```text
U/I/P architecture discrimination;
same-bytes/different-version recipient applicability;
and Track-N source-role versus world-personality classification.
```
