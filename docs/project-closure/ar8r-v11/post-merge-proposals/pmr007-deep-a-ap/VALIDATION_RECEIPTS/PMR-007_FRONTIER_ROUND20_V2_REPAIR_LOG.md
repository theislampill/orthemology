# PMR-007 Frontier Round 20 — V2 repair log

```text
source candidate: Round 20 V1
cold audit: REPAIR_REQUIRED
repaired candidate: Round 20 V2
mathematical statement changed: NO
historical bytes changed: NOT APPLICABLE — new post-merge research
```

## Closed findings

### R20-F01 — closed

The V2 ancestry note contains only repository-relative/stable labels and exact
hashes. No local absolute path is retained in the sanitized-eligible owner.

### R20-F02 — closed

The V2 checker searches compatible action subsets and verifies that the
incompatible-repair instance has pathwise support but no compatible path cover.

### R20-F03 — closed

Dynamic rerouting now updates the active path set after execution and returns
`p1` as an unblocked created path. The partial-registry check independently
compares the registered path family against the operative family containing the
omitted path.

### R20-F04 — closed

The V2 checker enumerates every action commitment and every allowed corruption.
It verifies the separation between static `forall C exists a` robustness and
post-commitment `exists a forall C` robustness.

## Scope preserved

The theorem remains the exact finite static fixed-path support characterization
under authenticated conjunctive root dependencies. No adaptive, dynamic,
compatibility, source-truth, causal, or world-level claim was added.
