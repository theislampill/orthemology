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

## Divergence/curl diagnostics require an explicit target field

Beyond the direct bound that $\nabla\cdot$ / $\nabla\times$ are "not literal
divergence/curl" **[direct]**, daee's own discipline constrains their *use*
**[crosswalk of `c86b3c66`; REBAKE §7.3 notation table, §7.5]**. $\nabla\cdot T$ and
$\nabla\times T$ are well-formed only over an **explicit multi-node target field**
$T$ carrying residual pressure, dependency, loop, or churn — never over a one-point
summary; this is why the framework rejects "proof-by-symbol" and scalarized closure.
An **acyclic** downstream dependency (a burden $B_2$ still live after landing $B_1$)
is **divergence** — a possibly non-neutral $\nabla\cdot B$ — while $\nabla\times$
stays **null** unless an actual loop, recoil, churn, or dependency rotation is
present. These remain typed control diagnostics, not physical operators, and assert
nothing about truth or interior states.

## G0 — metaphor only

"Gradient," "field," "attractor," "descent" as analogy. Useful for describing
directed correction; **no** formal monotonicity or convergence follows.

## G1 — order-theoretic / route-ranked corrective descent (PROPOSED-CANDIDATE)

The strongest reading the current daee formalism supports. A vector or partially-
ordered burden state

```math
\mathbf{B}_t = \langle B^{\text{disclosure}}_t, B^{\text{evidence}}_t, B^{\text{warrant}}_t, B^{\text{dependency}}_t, B^{\text{route}}_t, B^{\text{closure}}_t \rangle
```

is ranked by a governing functional $\operatorname{GradRoute}_A(\mathbf{B}_t, r)$
over admissible routes. A step is an **admissible / pathway-adequate governed
corrective transition** (R7D, Decision 0033 — *never* "strictly sound", which is
reserved for the factive claim-relative predicate of Decision 0011) only if it
preserves hard constraints, improves a declared ordering (or justified expected
value), preserves evidence and provenance, **hides no burden**, retains justified
uncertainty, and triggers a whole-state reread. "Descent" means an ordered,
governed improvement — not differentiation of a scalar loss.

### Why raw burden count is not a potential

Discovering three hidden burdens **grows** the ledger yet **improves** the
position (non-disclosure repaired). So

```math
|\mathbf{B}_{t+1}| > |\mathbf{B}_t| \ \text{does not imply deterioration}, \qquad |\mathbf{B}_{t+1}| < |\mathbf{B}_t| \ \text{does not imply progress}
```

Correction is therefore **feasibility-first**, not one universal total
lexicographic order (audit B14). **First**, a route violating any hard
constraint is *inadmissible* and filtered out — $\operatorname{Admissible}_A(S,r)$
— before any ranking; hard constraints are feasibility, not a rankable dimension.
**Second**, mandatory invariants are preserved (truthful disclosure, evidence and
provenance integrity, target and dependency correctness, retained uncertainty,
explicit holds, no fabricated closure). **Third**, admissible successors are
compared by a declared **partial order** $S' \succeq_A S$ — some routes remain
incomparable, licensing hold, escalation, parallel inquiry, or owner decision.
Otherwise the system could simulate descent by deleting or concealing the very
burdens it failed to address (fixture N18).

## Two timescales (audit B15)

**Fast** episode-level correction ($S_{e,t} \to S_{e,t+1}$: evidence, candidate
revision, token binding, route, burden landing, reread, hold/recurse/stop) is
distinct from **slow** meta-level adaptation ($\Gamma^\mu_t \to \Gamma^\mu_{t+1}$,
$\tilde\mu_t \to \tilde\mu_{t+1}$, $\mu_t \to \mu_{t+1}$, $A_t \to A_{t+1}$). A
pathway-adequate episode need not change the represented standard; a long-run
ecology may improve despite a failed episode; one runtime closure does not
establish interior restoration. `NOETIC-FIELD-DYNAMICS.yaml` `corrective_dynamics`.

## G2 — literal differentiable gradient flow (CONDITIONAL / FUTURE)

A literal claim requires a state space or manifold, a scalar potential or
precisely typed vector objective, a metric, differentiability, a gradient
operator, a step rule, convergence/stopping conditions, and treatment of local
minima, non-convexity, hysteresis, and path dependence. **daee does not supply
these**, so G2 remains conditional/future.

### Literal optimization exists elsewhere — and does not transfer

Literal optimization trajectories *do* occur in the OSM comparison: the RNNs are
trained by backpropagation-through-time and the CSCG is fit by Baum–Welch
expectation-maximization **[primary: 10.1038/s41586-024-08548-w]**. These are
literal descent/ascent over a defined objective in **model training** — a different
object from daee's runtime $\nabla$. The OSM result does **not** supply daee's
missing G2 conditions (no state space, metric, or differentiable gradient over the
runtime field), and daee's route-ranking imports **no** latent=ortheme or
clone=neuron identity. "Descent" and "trajectory" therefore carry two non-identical
senses across the corpus; neither transfers to the other.

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

**G1 is proposed-candidate** (R7D, Decision 0033; `NOETIC-FIELD-DYNAMICS.yaml`
`status: proposed-candidate`) — held pending fresh-Fable review and protected
merge, not adopted. Preferred phrasing until G2's conditions are met: **governed,
route-ranked, descent-like restorative dynamics** — not literal mathematical
gradient descent. A feasibility-admissible, order-improving, closed runtime
transition is an *admissible governed corrective transition*, not a strictly sound
one.
