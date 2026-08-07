# PMR-007 Frontier Round 18 V4 distinct fresh rereview

```text
rereview epoch: ROUND18-EPOCH-D4
frozen candidate: V4
cold-audit relation: post-audit, no repair-author overlap asserted as external independence
result: PASS_WITH_NONBLOCKING_SCOPE_NOTES
```

## Independent mechanisms used

The rereview did not import the primary checker.  It used:

1. bitmask dynamic programming for complete-object cover size versus a separate
   recursive enumeration of statewise outputs;
2. decoder-first enumeration for general encoder-information protocols;
3. independent ambiguity-set construction and decoder feasibility for noisy
   relation selection;
4. direct SCC semantics for the rank-certified temporal claim;
5. randomized projection/completion stress tests; and
6. frozen-hash verification before all semantic checks.

## Results

```text
frozen hash failures:                         0
exact-state relations checked:        1,161,388
exact-state mismatches:                       0
general encoder-information cases:        1,600
general encoder-information mismatches:       0
random relation-channel cases:            30,000
relation-channel mismatches:                   0
projection cases:                          20,000
projection failures:                           0
robust-completion cases:                   20,000
robust-completion failures:                   0
finite temporal structures checked:        74,088
rank-guard eligible structures:             2,655
direct temporal failures:                       0
```

For the strict relation-selection witness, every two-bit received word had a
three-state ambiguity set and a singleton common admissible object:

```text
00 -> k3
01 -> k2
10 -> k1
11 -> k0
```

Thus the V3 exact-label necessity claim is genuinely false, while the repaired
ambiguity-intersection theorem passes.

## Scope notes

- The rereview is procedurally distinct but not external human review or
  independent model-lineage confirmation.
- The theorem is finite, deterministic, one-shot, pointwise zero-error, and
  model-bound except where a different model is explicitly named.
- The bounded prior-art note is sufficient to cap novelty at zero, not to claim
  an exhaustive literature review.
- Bounded-error, interactive, private, cryptographic, asynchronous, and dynamic
  membership problems remain open.

## Disposition

```text
admitted identity: PMR-007-ORTC-V4
status: ADMITTED_POST_MERGE_SCOPED_RESULT
general mathematical novelty: 0
historical identity: NONE
external review: OPEN
owner adoption: PENDING
repository proposal: EXTERNAL_REVIEW_AND_OWNER_ADOPTION_REQUIRED
```
