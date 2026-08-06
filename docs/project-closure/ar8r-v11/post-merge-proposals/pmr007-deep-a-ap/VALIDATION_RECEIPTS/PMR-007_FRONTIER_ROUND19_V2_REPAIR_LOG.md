# PMR-007 Frontier Round 19 — V2 repair log

```text
source candidate: Round 19 V1
cold audit: REPAIR_REQUIRED
repaired candidate: Round 19 V2
historical bytes changed: NOT APPLICABLE — new post-merge research
```

## Closed findings

### R19-F01 — closed

The upper proof now defines `B(m,n,k)` piecewise and separates feasible
residual recurrences from immediate-false branches.  Equality is asserted only
where the residual demand remains feasible; otherwise the direct inequality
`n <= B(m,n,k)` is proved.

### R19-F02 — closed

The lower oracle simulation now caches one label per queried positive edge and
returns it on repeated queries.  The fresh-label counter advances only on a
newly discovered positive edge.

### R19-F03 — closed

The V2 checker independently constructs the same-label and distinct-label
worlds, projects each to a binary support transcript, and compares the two
projections.

### R19-F04 — closed

The V2 checker registers constant-true, rank-impossible, and alphabet-too-small
boundary cases across all `1 <= m,n <= 7`.

## Scope unchanged

The repair changes no theorem conclusion.  It narrows the proof text to its
correct piecewise residual domain and strengthens oracle/executable custody.
The deterministic canonical-label/no-extra-cost scope and all nonclaims remain
unchanged.
