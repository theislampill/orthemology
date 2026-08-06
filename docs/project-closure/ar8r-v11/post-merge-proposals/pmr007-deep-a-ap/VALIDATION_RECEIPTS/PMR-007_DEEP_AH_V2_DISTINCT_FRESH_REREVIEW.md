# PMR-007 Deep Round AH V2 — distinct fresh rereview

```text
candidate: PMR-007-SDIG-1 V2
review relation: distinct source-anchor, incidence-graph, full-partition, and bearer-assignment implementation in the same Pro program
external independence: false
disposition: PASS_WITH_NONBLOCKING_SOURCE_AUTHORITY_AND_REPRESENTATION_SCOPE_NOTES
```

The rereview began from the frozen V2 hashes and did not use the primary
bipartition checker as its oracle.  It independently:

1. verified the exact Asfahani translation hash and 17 source-line anchors;
2. rebuilt the selected graph as a support-incidence structure;
3. enumerated every set partition of the ten selected nodes;
4. tested 20,000 coordinate relabelings;
5. exercised 50,000 bearer assignments; and
6. reran the source-coordinate and qiyas guard-deletion controls.

The first rereview attempt failed because two literal source-anchor probes were
misindexed or case-mismatched.  That failed checker/result is preserved.  A
custody-only repair corrected those probes without changing any frozen
candidate byte, source byte, proof claim, model, primary check, audit, or V2
hash.

```text
frozen hash rows:                         7
frozen hash mismatches:                   0
source anchors checked:                  17
source anchor failures after repair:      0
selected incidence components:            1
set partitions checked:             115,975
nontrivial uncrossed partitions:           0
coordinate relabelings:               20,000
relabeling failures:                       0
bearer assignments:                   50,000
plural assignments exercised:         49,995
source-coordinate deletion witnesses:      6
qiyas single-guard deletion witnesses:     4
```

The selected source graph is therefore connected and predicate-level
nonflatness is stable under relabeling.  Connectedness still does not derive the
textual co-reference binder: plural bearer assignments realize the same local
support topology in the declared semantics.

The result remains representation-relative and source-conditional.  It neither
verifies Arabic primary text nor turns a translated source proposition into a
neutral or world-directed common-bearer theorem.
