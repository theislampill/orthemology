# PMR-007 Deep Round BD V1 — latent source reliability orientation and truth-anchor necessity

```text
identity: PMR-007-LSRO-1
round: DEEP_BD
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_burden: whether source agreement and inferred reliability orient a latent class toward truth without an external anchor
```

## 1. Typed finite model

Let `T in {0,1}` be a latent binary state and let `X_1,...,X_m` be binary
reports from declared source roots.  A conditionally independent latent-source
model is

\[
\theta=(\pi,Q_1,\ldots,Q_m),
\qquad
\pi=P(T=1),
\]

where `Q_i(x|t)` is a row-stochastic binary reporting channel and

\[
P_\theta(x_1,\ldots,x_m)
=
\sum_{t\in\{0,1\}}P_\theta(T=t)
\prod_{i=1}^m Q_i(x_i\mid t).
\]

The symbols `0` and `1` in the latent coordinate are not yet identified with
world-level falsity and truth.  The following coordinates remain separate:

```text
latent class;
report symbol;
authenticated acquisition root;
source reliability channel;
truth orientation;
source-to-world interpretation;
actual-world selection;
recipient warrant;
and creed-internal tawatur assessment.
```

## 2. LSRO-1A — latent-orientation nonidentifiability

Define the latent-label swap

\[
\pi^\sigma=1-\pi,
\qquad
Q_i^\sigma(x\mid t)=Q_i(x\mid 1-t).
\]

Then

\[
P_{\theta^\sigma}(x)=P_\theta(x)
\quad\text{for every report tuple }x.
\]

### Proof

The two summands in the latent mixture are merely exchanged:

\[
\begin{aligned}
P_{\theta^\sigma}(x)
&=(1-\pi)\prod_iQ_i(x_i\mid 1)
  +\pi\prod_iQ_i(x_i\mid 0)\\
&=P_\theta(x).
\end{aligned}
\]

Therefore no observation-only rule, even with exact knowledge of the complete
joint report distribution, can distinguish the two latent orientations.

This is the standard latent-class label-switching boundary.  It does not claim
that the model is otherwise identifiable up to only this swap.

## 3. LSRO-1B — symmetric-reliability specialization

Suppose each root has one symmetric accuracy coordinate `p_i`:

\[
Q_i(x\mid t)=
\begin{cases}
p_i,&x=t,\\
1-p_i,&x\neq t.
\end{cases}
\]

The swapped model has

\[
\pi^\sigma=1-\pi,
\qquad
p_i^\sigma=1-p_i.
\]

Thus an observationally inferred parameter vector with all `p_i>1/2` and the
vector with all `p_i<1/2` describe the same report law after reversing the
latent truth orientation.  Agreement alone does not determine whether the
sources are jointly truth-tracking or jointly inverted.

## 4. LSRO-1C — exact orientation-anchor condition

Assume separately that an identification theorem or evidence packet has
already narrowed the admissible parameter set to one swap orbit

\[
\{\theta,\theta^\sigma\}.
\]

Let root `j` have an independently warranted directional anchor

\[
Q_j(1\mid 1)>Q_j(1\mid 0).
\]

The inequality reverses under the latent swap.  Therefore exactly one member of
the two-element orbit satisfies the anchor.  In the symmetric specialization,
this is the guard `p_j>1/2`.

The result is conditional on all of the following:

```text
the component model has already been identified up to the latent swap;
the anchored root is authenticated;
the directional reliability evidence is independent of the unlabeled report law;
the anchor applies to the current version, domain, and membership epoch;
and the report symbols and world-level truth labels are linked by an independently warranted map.
```

An anchor does not follow from numerical agreement, source popularity,
conditional independence, or the model fit itself.

## 5. LSRO-1D — posterior complement

For every report tuple in the common support,

\[
P_\theta(T=1\mid X=x)
+
P_{\theta^\sigma}(T^\sigma=1\mid X=x)
=1.
\]

The same observable report can therefore receive opposite latent-truth
orientations in observationally identical models.

## 6. Countermodels and positive control

```text
BD-CM1 UNANIMOUS ANTI-RELIABILITY:
  pi=1/2 and three independent roots have p_i=1/4.
  unanimous report 1 strongly supports latent state 0, not 1.
  The p_i=3/4 swapped model has the same observable report distribution.

BD-CM2 COPIED-ROOT MAJORITY:
  one root observation is copied into many carriers.
  apparent unanimity does not create new independent likelihood factors
  or break the latent-orientation symmetry.

BD-CM3 COMMON-CAUSE AGREEMENT:
  several reports descend from one hidden acquisition cause.
  the conditional-product model is false even though reports agree.

BD-CM4 STALE DIRECTIONAL ANCHOR:
  a root is positively oriented in version v1 and inverted or domain-shifted
  in version v2.  Reusing the v1 anchor does not orient the v2 model.

BD-CM5 SOURCE/WORLD MAP SWAP:
  one source-role bundle admits two source-to-world maps that exchange the
  truth and falsity interpretation.  Source-role compatibility alone does not
  choose the actual-world map.

BD-CM6 ADDITIONAL MIXTURE NONIDENTIFIABILITY:
  the observation law may have parameter collisions beyond label swapping.
  a directional anchor selects one orientation only after an independent
  component-identification result establishes the relevant swap orbit.

BD-CM7 DISPLAYED-ROOT ALIAS:
  distinct displayed sources can be copies of one actual root.  Label count
  does not establish conditional independence or source quality.

BD-POS1 INDEPENDENT CALIBRATION ANCHOR:
  an authenticated root is tested on independently truth-labeled calibration
  items at the current version and is strictly better than chance.  Conditional
  on component identification up to swap, this selects one orientation.
```

## 7. Cross-lane consequences

### Candidate A / TAC / false multiplicity

Source count, carrier count, and report agreement do not identify independent
roots or truth orientation.  Root authentication and a truth-oriented anchor
are distinct obligations.

### Candidate B / restoration

A restorative system cannot infer that its source majority is truth-directed
from agreement alone.  A false but coherent source ecology can stabilize one
inverted latent orientation.  Source version and domain custody remain part of
restorative eligibility.

### Candidate C / Track N

A source architecture can constrain the admissible model class at a
school-internal level.  It does not become a neutral world-orientation theorem
unless the source-to-world and directional-reliability anchors are
independently warranted.

### Deep AR, AW, AX, and AP

```text
Deep AR:
  copied presentations do not create independent likelihood factors;

Deep AW:
  robust diagnosis assumes authenticated root coordinates but does not orient
  the latent labels toward truth;

Deep AX:
  an exact source likelihood ratio presupposes architecture-conditioned,
  truth-oriented source models;

Deep AP:
  a singleton relative source referent remains conditional on the admissible
  interpretation family and does not by itself identify the actual world.
```

## 8. Source and implementation boundary

The current daee `FALSE-TAWATUR-FIXTURES.yaml` explicitly distinguishes
source-independence from tawatur warrant and treats common source or copying as
dependence.  `TAWATUR-WARRANT.example.yaml` separately records creed-internal
qualitative conditions such as source origin, path independence, non-collusion,
transmitter quality, content coherence, subject acquisition, and defeaters.

The present latent-class result is not a reconstruction of the historical
Taymiyyan theory of tawatur.  It supplies one finite statistical firewall:
unlabeled agreement cannot orient a latent source class toward world-level
truth without an additional anchor.

## 9. Ancestry and novelty ceiling

```text
Dawid-Skene observer-error latent class model:
  model-family and estimation ancestry;

latent-class label switching and generic identifiability theory:
  direct mathematical ancestry;

Deep AR / AX:
  root conservation and joint likelihood accounting;

current daee false-tawatur controls:
  implementation and governance correspondence;

general mathematical novelty:
  0;

historical identity:
  NONE.
```

## 10. Nonclaims

- The theorem does not establish that an impersonal or inverted world is actual.
- It does not establish that source reliability is impossible to learn with
  calibration, constraints, interventions, or trusted labels.
- It does not establish generic identifiability of a latent class model.
- Conditional independence is a declared model guard, not a consequence of
  distinct carriers.
- A calibrated source does not automatically establish honesty, competence,
  authority, applicability, tawatur, or recipient warrant.
- A Track-N premise does not become a neutral theorem premise by appearing in a
  formal source model.
- Proposal-level admission would not authorize repository adoption.
