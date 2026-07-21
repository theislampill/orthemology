# Sound descent: G0 / G1 / G2 model comparison

**Status:** DRAFT — application-level adjudication (Decision 0025). OPUS CANDIDATE
— REQUIRES FRESH FABLE REVIEW BEFORE MERGE. daee statements pinned to commit
`c86b3c6673147b8802fe222373a165a37d4d24a8`. No empirical or theological claim.

daee uses gradient/field vocabulary, but **its own formalism bounds it**: $\nabla$
is a "Route-ranking functional … **Not literal physical gradient**," and
$\nabla\cdot$ / $\nabla\times$ are "**not literal divergence/curl unless a rigorous
target space is later defined**" **[direct:
docs/algebraic-notation-and-noetic-formalism.md]**; the field-gradient audit
disclaims "literal mathematical performance" **[direct:
docs/audits/v0.4.1.0-field-gradient-loop-closure-coupling-implementation-audit.md]**.
Three readings must be distinguished.

## G0 — metaphor only

"Gradient," "field," "attractor," "descent" as analogy. Useful for describing
directed correction; **no** formal monotonicity or convergence follows.

## G1 — order-theoretic / route-ranked corrective descent (ADOPTED)

The strongest reading the current daee formalism supports. A vector or partially-
ordered burden state

```math
\mathbf{B}_t = \langle B^{\text{disclosure}}_t, B^{\text{evidence}}_t, B^{\text{warrant}}_t, B^{\text{dependency}}_t, B^{\text{route}}_t, B^{\text{closure}}_t \rangle
```

is ranked by a governing functional $\operatorname{GradRoute}_A(\mathbf{B}_t, r)$
over admissible routes. A step is **locally sound** only if it preserves hard
constraints, improves a declared ordering (or justified expected value),
preserves evidence and provenance, **hides no burden**, retains justified
uncertainty, and triggers a whole-state reread. "Descent" means an ordered,
governed improvement — not differentiation of a scalar loss.

### Why raw burden count is not a potential

Discovering three hidden burdens **grows** the ledger yet **improves** the
position (non-disclosure repaired). So

```math
|\mathbf{B}_{t+1}| > |\mathbf{B}_t| \ \text{does not imply deterioration}, \qquad |\mathbf{B}_{t+1}| < |\mathbf{B}_t| \ \text{does not imply progress}
```

Progress is **lexicographic**: truthful disclosure $\succ$ evidence integrity
$\succ$ dependency correctness $\succ$ hard constraints $\succ$ justified holds
$\succ$ legitimate reduction $\succ$ truthful closure. Otherwise the system could
simulate descent by deleting or concealing the very burdens it failed to address
(fixture N18).

## G2 — literal differentiable gradient flow (CONDITIONAL / FUTURE)

A literal claim requires a state space or manifold, a scalar potential or
precisely typed vector objective, a metric, differentiability, a gradient
operator, a step rule, convergence/stopping conditions, and treatment of local
minima, non-convexity, hysteresis, and path dependence. **daee does not supply
these**, so G2 remains conditional/future.

## Non-monotonicity and separate state spaces

Model newly-disclosed burdens, local minima, loops/curl, path dependence,
hysteresis, restarts/holds, metaortheme revision, and **no guaranteed
convergence**. Keep separate: actual noetic condition; inferred profile
$\hat p$; runtime/control state; the social/metaorthemic propagation field
$\Gamma^\mu$; released linguistic action; and actual uptake. A runtime can close
while the person is unchanged (fixture N19).

## Fiṭrah boundary [creed-internal]

Fiṭrah supplies a normative orientation / proper-function ground. It is **not**
one coordinate, one metaortheme, one algorithm, or one measured scalar target;
any "minimum-entropy attractor" language is provisional and creed-internal —
daee itself states the Shannon analogy does not prove noetic collapse **[direct]**.

## Verdict

Adopt **G1**. Preferred phrasing until G2's conditions are met: **governed,
route-ranked, descent-like restorative dynamics** — not literal mathematical
gradient descent.
