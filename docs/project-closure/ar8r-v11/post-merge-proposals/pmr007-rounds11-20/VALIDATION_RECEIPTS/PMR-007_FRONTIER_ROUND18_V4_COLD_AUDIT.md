# PMR-007 Frontier Round 18 V4 cold audit

```text
audit epoch: ROUND18-EPOCH-B4
audit input: frozen V4 hashes
result: PASS_WITH_NONBLOCKING_AUTHORITY_NOTES
```

## Load-bearing checks

| Check | Result |
|---|---|
| Complete certificate object is distinct from surface action | PASS |
| Exact-state encoder assumption is explicit in `ORTC-EXACT` | PASS |
| General encoder-information partition is separately typed | PASS |
| Decoder access to original observation is explicit | PASS |
| Fixed-length and worst-case prefix-free claims are separated from expected length | PASS |
| Pointwise zero-error randomization uses finite-state seed fixing only | PASS |
| Bounded-error and interactive protocols are excluded | PASS |
| Robust relation selection is stated by ambiguity-set intersections | PASS |
| Exact label recovery is only a stronger special case | PASS |
| `R18-RELATION-BEATS-LABEL` refutes the V3 necessity claim | PASS |
| Partial/stale completion uses intersection, not union | PASS |
| Temporal statement is model-bound and only sufficient | PASS |
| History and future-hidden-branch limitation is preserved | PASS |
| Source, warrant, authorization, and provenance truth are not inferred | PASS |
| Set Cover and zero-error functional-compression ancestry is recorded | PASS |
| Historical identity and general novelty are not assigned | PASS |
| Primary executable result is parse-valid and PASS | PASS |

## Nonblocking authority notes

1. `ORTC-INFO` is an exact finite characterization, not an efficient algorithm
   or a new graph-entropy theorem.
2. The NP-completeness result assumes an explicit admissibility matrix/support
   representation.  Succinct or oracle representations may have different
   complexity.
3. The zero-error seed-fixing result does not constrain bounded-error,
   privacy-preserving, cryptographic, or interactive protocols.
4. The temporal rank architecture does not characterize all
   partial-observation co-Büchi winning strategies.
5. The source and prior-art assessment remains bounded rather than exhaustive;
   external review remains open.

## Disposition

```text
blocking findings: 0
repair required after V4 freeze: false
fresh rereview required: true
admission before fresh rereview: WITHHELD
```
