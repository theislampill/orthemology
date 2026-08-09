# Deep CS V1 — weakest admissible discriminator for a recurrent residual

## Candidate identity

```text
identity: PMR-007-WADF-1
round: DEEP_CS
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
owner adoption: PENDING
external review: OPEN
general mathematical novelty: 0
```

Let `M` be a finite model class, `E:M→Obs` the current evidence profile, and
`Q:M→Target` the unresolved architecture coordinate. A candidate refinement
`r:M→Y_r` is weaker than `s:M→Y_s` when `(E,s)` determines `(E,r)`, equivalently
when every `(E,s)` fibre lies inside an `(E,r)` fibre.

A refinement is discriminating when `Q` is constant on every `(E,r)` fibre.
V1 proposes choosing the unique weakest discriminating refinement. It further
proposes this as a direct AR8R import of Bennett's weakness-maximization theorem
and treats the balanced-EF1 order-statistic correction as evidence that repeated
residuals generally admit one invariant-restoring correction.

The current U/I residual has no such certified neutral refinement. Intentional
uptake and the Track-N source package separate it only as target/source-relative
coordinates.
