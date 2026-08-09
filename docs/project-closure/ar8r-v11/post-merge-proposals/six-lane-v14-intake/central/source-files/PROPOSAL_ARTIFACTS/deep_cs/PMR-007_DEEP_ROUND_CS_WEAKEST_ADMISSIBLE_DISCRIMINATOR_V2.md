# Deep CS V2 — minimal-commitment admissible discrimination under a recurrent residual

## 1. Identity and authority

```text
identity: PMR-007-WADF-1
round: DEEP_CS
version: V2
status before fresh rereview: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
general mathematical novelty: 0
owner adoption: PENDING
external review: OPEN
```

## 2. Typed finite setting

Let `M` be a finite declared model class, `E:M→Obs` the frozen current evidence
profile, and `Q:M→Target` the unresolved target coordinate. Let `C` be a finite
family of **independently eligible** candidate refinements `r:M→Y_r`.
Eligibility is external to the partition theorem and may include:

```text
target blindness;
common typing and semantics;
version identity;
authorization;
resource feasibility;
source/world custody;
and architecture-independent implementation rules.
```

Two candidates are equivalent at this surface when `(E,r)` induces the same
partition of `M`.

Call `r` weaker than `s` when the partition induced by `(E,r)` is coarser than
the one induced by `(E,s)`. Call `r` discriminating when `Q` is constant on
every `(E,r)` fibre.

## 3. WADF-1A — exact admissible discriminator characterization

The eligible discriminator set is

```text
D = {r in C : ker(E,r) subseteq ker(Q)}.
```

Equivalently, every target-conflict pair inside an `E` fibre must be split by
`r`. This is the standard finite fibre criterion, not new general mathematics.

If `D` is nonempty, its finite partition order has at least one minimal element.
It may have several incomparable minimal elements. There is no canonical unique
"weakest" discriminator without a further independently justified order, cost,
probability model, or selection rule.

## 4. WADF-1B — unrestricted coarsest sufficient refinement and target leakage

If every map is allowed, the coarsest target-sufficient refinement of `E` is the
joint partition

```text
Pi_* = Pi_E meet Pi_Q,
```

whose cells are intersections of `E`-fibres with `Q`-fibres. Every sufficient
refinement of `E` refines `Pi_*`.

But the obvious realization `r=Q` reads the target. Thus the unrestricted
mathematical floor is not automatically an eligible experiment or anchor.
This is the exact point at which target-blindness and independent evidence enter.

## 5. WADF-1C — common-postprocessing barrier

If `r=g∘E`, then `(E,r)` has exactly the same fibres as `E`. Therefore, whenever
`E` already contains a `Q` conflict, no deterministic common postprocessing,
quotient, score, normalization, relabeling, or representation computed only
from `E` can resolve it.

This specializes Deep CO. A genuinely successful candidate must enlarge the
experiment, add an independently warranted non-`E` anchor, or restrict the
model class by evidence not determined by `E`.

## 6. Current U/I/P application

For the frozen architecture surface:

```text
neutral E: {U,I,P};
common bearer: {U,I}|{P};
intentional uptake: {U}|{I,P}.
```

The common-bearer coordinate does not split the surviving `U/I` conflict.
Intentional uptake does split it formally, but is presently a target coordinate,
not an independently operationalized common measurement. The Track-N package
can split it only conditionally on its source/world guards.

Hence:

```text
current eligible neutral discriminator set for U/I:
EMPTY_AT_CURRENT_REGISTRY.
```

This is registry-relative, not a theorem that no future common experiment can
exist.

## 7. Bennett source comparison

Bennett defines weakness as extension cardinality in a finite implementable
language and proves its generalization optimality only under his task formalism
and a uniform distribution over tasks. The present partition order is an
independently proved finite commitment order. No theorem transfer from Bennett
is claimed.

The retained research heuristic is narrower:

> among independently eligible candidates that actually discriminate a live
> burden, prefer partition-minimal commitments unless a separately warranted
> cost or information model selects otherwise.

Two adversarial controls are mandatory:

```text
pure weakness failure:
  the constant map is maximally coarse and useless for U/I;

pure discrimination failure:
  the target oracle is maximally direct and evidentially ineligible.
```

The toy binary-arithmetic experiments in Bennett were not locally reproduced;
the referenced technical appendix and code package were not supplied here.

## 8. Balanced-EF1 correction comparison

The balanced-EF1/fPO paper supplies a concrete proof-search case in which an
order-statistic correction repairs a specific unequal-cardinality residual,
restores common-shift invariance, and gives the remaining term the needed sign.
Its failed-rounding example also shows that a valid relaxed/fractional witness
need not survive arbitrary discrete implementation.

Current classification:

```text
order-statistic correction -> AR8R residual search:
PROOF_SEARCH_HEURISTIC_ONLY;

failed rounding -> source/formal/implementation/world projection:
COUNTERMODEL_PATTERN_ONLY.
```

No typed reduction from the fair-division objects to the U/I architecture
surface has been proved. The paper does not establish that every recurrent
residual has a correction, that a correction is scalar, or that it selects a
metaphysical architecture.

## 9. Combined residual-guided policy result

The combined policy survives only in guarded form:

```text
H0 identify a recurrent residual and freeze its conflict pairs;
H1 derive structural conditions any eligible repair must satisfy;
H2 test which rival classes admit such a repair;
H3 test representation and vocabulary sensitivity;
H4 construct a concrete object only after H0-H3 earn it.
```

At the present U/I residual, Deep CO and this round give a clean H1 failure for
the entire family of common postprocessings of `E`. Deep CP gives no current
eligible common intervention. Deep CR gives only a conditional source route.
The correct next strengthening is therefore not another score over `E`, but a
new independently typed experiment/anchor proposal or a source/world
adjudication.

## 10. Theorem-family and nonclaims

```text
mathematical core:
  finite partition/fibre order and attained quotient;
novelty:
  0;
relation to Deep CL/CN:
  shared conflict-cover mechanism, here converted into a candidate-selection
  and anti-target-leakage gate;
relation to Bennett:
  heuristic only;
relation to balanced EF1:
  heuristic and countermodel pattern only.
```

No claim is made that minimal commitment maximizes truth under nonuniform tasks,
that expected information gain is canonical, that description length is
irrelevant in every setting, that the current candidate family is complete, or
that a personal, impersonal, plural, proper-function, Wisdom, Speech, or
Necessary-Being conclusion follows.
