# PMR-007 Deep BF — distinct-rereview harness repair log

```text
candidate theorem version: V2
candidate theorem bytes changed by this repair: false
finding class: REVIEW_HARNESS_DEFECT
```

The first distinct-rereview run timed out because the identity-support witness
called a generic dynamic-programming rectangle-cover routine over all
`2^(n^2)` masks for `n` through six. That was an unnecessary exponential
implementation choice, not a mathematical counterexample.

The harness was repaired before any admission decision:

```text
- exhaustive generic rectangle-cover DP retained for every 3x3 support;
- diagonal n×n supports handled by the direct independent observation that
  every contained nonempty rectangle has one cell;
- reconstruction and channel checks unchanged in mathematical target;
- the repaired implementation was rerun from the beginning;
- only the repaired PASS is used for rereview disposition.
```

The exact pre-repair script bytes were not separately frozen before the timeout.
This custody limitation is recorded rather than concealed. It does not alter
the frozen V2 theorem/model hashes.
