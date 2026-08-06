# PMR-007 Frontier Round 19 V1 — cold audit

```text
audit relation: SAME-MODEL PROCEDURALLY DISTINCT REVIEW
frozen owner: PMR-007_FRONTIER_ROUND19_V1_FROZEN_HASHES.sha256
disposition: REPAIR_REQUIRED
external independence: NO
```

## 1. Frozen-hash custody

All five V1 owner hashes were recomputed before review and matched the frozen
receipt.  The audit did not modify the frozen candidate.

## 2. Statement audit

The typed theorem statement is coherent at the declared finite deterministic
zero-error scope.  The boundary cases and the canonical-label/no-extra-cost
oracle assumptions are stated.  The claimed formula matches all primary finite
minimax instances.

## 3. Blocking findings

### R19-F01 — upper-bound algebra overstates boundary equalities

The V1 prose writes

```text
n + B(m-1,n,k) = B(m,n,k)
```

for the no-positive branch and gives an unconditional `m-1` slack for the
old-label branch.  Those identities fail when deleting a row or column makes
`k > min(m-1,n)` or `k > min(m-1,n-1)`, because the algorithm then terminates
immediately with constant false and the piecewise residual bound is zero.

Example:

```text
m=n=k=2
B(2,2,2)=3
no-positive branch cost = 2, not 3
```

The desired inequalities remain true, and the primary checker used the correct
piecewise base case.  The written induction must be repaired to split feasible
residual branches from immediate-false branches.

```text
severity: BLOCKING_PROOF_PRESENTATION
```

### R19-F02 — repeated queries are not explicitly label-consistent

The online lower reduction says to issue `alpha_j` on the `j`-th positive edge
"discovered", but it does not explicitly cache a label per edge.  A general
deterministic algorithm may redundantly query the same edge.  Returning a new
label on the second query would fail to define one fixed labelled input.

The repair must either normalize the algorithm to never repeat a query or,
preferably, cache each queried positive edge's first label and return it on all
repetitions.  The fresh-label counter advances only on a newly discovered
positive edge.

```text
severity: BLOCKING_ORACLE_CONSISTENCY
```

### R19-F03 — the primary countermodel check contains a tautological transcript comparison

The primary script records

```text
binary_same == binary_same
```

rather than independently constructing and comparing the two support-identical
binary transcripts.  The mathematical countermodel is correct, but the
executable receipt does not actually test the intended equality as written.
The repaired checker must construct both labelled worlds, project each to the
binary support transcript, and compare those two projections.

```text
severity: BLOCKING_EXECUTABLE_EVIDENCE
```

### R19-F04 — boundary cases are stated but not executable regressions

The primary checker tests only `1 <= t <= min(m,n)` and alphabet size `t`.
It does not separately verify the constant-true/constant-false boundary cases
or the `|Lambda|<t` branch.  Those cases are elementary, but they are part of
the theorem's advertised full convention and should be explicit regressions.

```text
severity: BLOCKING_ADVERTISED_SCOPE_CHECK
```

## 4. Nonblocking findings

### R19-N01 — Candidate 1 authority ceiling

The lower reduction is sound relative to the preserved Candidate 1 theorem,
but Candidate 1 still has open external mathematical and exhaustive prior-art
review.  Round 19 cannot outrank that inherited authority on the exact depth
formula.

### R19-N02 — no root-independence semantics

The packet correctly states that canonical labels do not themselves establish
independent acquisition, source truth, warrant, or recipient applicability.
This firewall must remain in the repaired packet and admission overlay.

### R19-N03 — prior-art search remains bounded

The located hidden-matching and bipartite-matching query papers are adjacent but
nonidentical.  Nonretrieval does not establish novelty.  External review remains
open.

### R19-N04 — no randomized or distributed transfer

The exact theorem is deterministic and centralized.  The result does not carry
over automatically to randomized, expected, parallel, multi-agent, or
communication complexity.

## 5. Proof attack summary

```text
old-label branch:
  survives after piecewise-bound repair;

online lifting:
  survives with per-edge label caching;

alphabet-size t:
  sufficient;

support-only access:
  explicit impossibility survives;

label aliases / merges:
  semantic controls survive;

Candidate 1 ancestry:
  exact reduction, not duplicate origin;

prior art:
  unresolved externally.
```

## 6. Required repair

1. Preserve V1 and this audit.
2. Create a V2 packet with piecewise branch inequalities.
3. Add cached-label semantics to the online oracle lift.
4. Repair the primary checker and add boundary regressions.
5. Freeze V2 and its new results.
6. Run a distinct fresh rereview using an independently written minimax and
   adversary implementation.
7. Admit only the V2 scope if the rereview passes.
