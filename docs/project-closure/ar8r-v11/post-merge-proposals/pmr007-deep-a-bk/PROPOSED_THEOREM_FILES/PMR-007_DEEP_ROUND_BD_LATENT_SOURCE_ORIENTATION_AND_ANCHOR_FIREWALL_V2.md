# PMR-007 Deep Round BD V2 — latent source orientation and the source–world anchor firewall

```text
identity: PMR-007-LSRO-1
round: DEEP_BD
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_burden: whether unlabeled source agreement can orient a latent report model toward world-level truth
```

## 1. Typed finite model

Let `T in {0,1}` be a latent binary class with `0 < pi=P(T=1) < 1`.  Let
`X_1,...,X_m` be finite binary reports from declared source coordinates.  The
conditionally independent latent-source model is

\[
\theta=(\pi,Q_1,\ldots,Q_m),
\qquad
P_\theta(x)
=
\sum_{t\in\{0,1\}}P_\theta(T=t)
\prod_i Q_i(x_i\mid t),
\]

where each `Q_i` is a binary row-stochastic channel.

The model separates:

```text
LATENT     an unlabeled mixture component;
REPORT     a source's emitted symbol;
ROOT       authenticated acquisition lineage;
CHANNEL    report behavior conditional on the latent component;
SEM        the proposition asserted by a report symbol;
MAP        the latent/source-to-world interpretation;
ORIENT     independent evidence fixing which latent orientation is truth-linked;
VER        current domain, version, and membership applicability;
WORLD      actual-world/model-class adequacy;
WARRANT    subject-relative epistemic warrant.
```

`LATENT=1` is not definitionally `WORLD-TRUTH`.

## 2. LSRO-1A — label-swap invariance

Define

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

The two latent mixture terms are exchanged, so the equality is immediate.
Consequently every statistic that factors only through the complete observable
joint report law is invariant under this swap and cannot choose a latent
truth orientation.

This is a label-switching result.  It neither establishes nor denies any
additional parameter nonidentifiability.

## 3. LSRO-1B — symmetric reliability and posterior reversal

In the symmetric specialization

\[
Q_i(x\mid t)=
\begin{cases}
p_i,&x=t,\\1-p_i,&x\ne t,
\end{cases}
\]

the swap sends

\[
(\pi,p_1,\ldots,p_m)
\mapsto
(1-\pi,1-p_1,\ldots,1-p_m).
\]

For every report tuple in the common support,

\[
P_\theta(T=1\mid X=x)
+
P_{\theta^\sigma}(T^\sigma=1\mid X=x)
=1.
\]

Thus exact report agreement and exact recovery of the observational law do not
by themselves tell the analyst whether the inferred sources are positively
or negatively oriented toward world truth.

## 4. LSRO-1C — exact orientation-breaker requirement

Let `Obs(theta)` be the complete report distribution.  If

\[
Obs(\theta)=Obs(\theta^\sigma),
\]

then no deterministic selector `s(Obs(theta))` can return different
orientations for the two models.  Any successful orientation rule must use at
least one input that is not invariant under the swap.

Eligible inputs may include, at their own authority levels:

```text
independently truth-labeled calibration outcomes;
a verified intervention whose outcome is semantically oriented;
an independently defended asymmetric model-class restriction;
a source-relative premise that restricts Track-N models;
or an actual-world/source-reference bridge.
```

A preferred prior over arbitrary latent labels or a coding convention can
select a label but is not evidence of world truth unless independently
justified.

## 5. LSRO-1D — calibrated-root orientation theorem

Assume a separate component-identification result has reduced the admissible
parameter set to exactly the swap orbit `{theta,theta^sigma}`.  Let root `j`
have a current, authenticated orientation contract:

```text
ROOT_j:
  one actual acquisition/calibration root;

SEM_j:
  report symbol 1 is independently established to assert proposition P;

MAP_j:
  the calibration truth labels are linked to the same world predicate used by
  the target source model;

CAL_j:
  Q_j(1|WORLD-TRUE) > Q_j(1|WORLD-FALSE);

VER_j:
  the calibration applies to the current domain, version, and membership epoch;

INDEP_j:
  this directional evidence is not inferred solely from the unlabeled report
  law whose orientation is being selected.
```

Under those guards, exactly one member of `{theta,theta^sigma}` satisfies the
contract.  In the symmetric model, `CAL_j` is `p_j>1/2` after `SEM_j` and
`MAP_j` have fixed the meaning of equality between report and world label.

This theorem orients one already identified swap orbit.  It does not prove the
component model, source honesty, competence, source authority, actual-world
adequacy, or recipient warrant.

## 6. Countermodels and positive control

```text
BD-CM1 UNANIMOUS ANTI-RELIABILITY:
  pi=1/2 and three conditionally independent roots have p_i=1/4.
  Under the interpretation LATENT=1 as WORLD-TRUE, report tuple (1,1,1)
  gives posterior P(T=1|X)=1/28.  The p_i=3/4 swapped orientation has the
  identical observable distribution.

BD-CM2 COPIED-ROOT MAJORITY:
  with equal latent prior, one symmetric root of accuracy 3/4, and observed
  report 1, the root likelihood ratio is 3.  The visible tuple (1,1,1)
  formed by three deterministic exact copies still has likelihood ratio 3;
  treating the copies as independent incorrectly gives 27.

BD-CM3 COMMON-CAUSE AGREEMENT:
  multiple displayed reports are deterministic descendants of one hidden
  source event.  The conditional-product likelihood is invalid.

BD-CM4 STALE OR DOMAIN-SHIFTED ANCHOR:
  a source is positively calibrated at v1 and inverted or semantically shifted
  at v2.  The v1 orientation contract does not select the v2 model.

BD-CM5 SOURCE/WORLD MAP SWAP:
  the source-role graph admits two interpretation maps that exchange the
  truth/falsity realization.  Source compatibility does not choose a world.

BD-CM6 ADDITIONAL MIXTURE NONIDENTIFIABILITY:
  more than the swap pair may realize the same observable law.  CAL_j cannot
  establish full component recovery; it selects an orientation only after the
  swap-orbit premise is independently met.

BD-CM7 DISPLAYED-ROOT ALIAS:
  separately printed sources descend from one actual root.  Apparent witness
  number neither establishes conditional independence nor a calibration anchor.

BD-CM8 PRIOR OR CODING LABEL:
  an asymmetric prior over the names `latent-0` and `latent-1` chooses a code
  orientation without supplying source-world truth evidence.

BD-POS1 CURRENT TRUTH-LABELED CALIBRATION:
  an authenticated source is measured on independently truth-labeled current-
  domain cases and is strictly positively oriented.  Conditional on recovery
  up to swap, the contract selects one orientation.
```

## 7. Flywheel effects

### Candidate A / TAC / false multiplicity

Report count and agreement do not identify acquisition-root independence or
truth orientation.  Root authentication, conditional independence, component
identification, and orientation are four different burdens.

### Candidate B / restoration and daee

A self-consistent source ecology may stabilize an inverted latent orientation.
A restorative target therefore needs a source/world orientation contract in
addition to agreement, provenance, temporal persistence, and route closure.

### Candidate C / Track N

A source-relative premise may restrict the Track-N model class.  It does not
become a neutral source-world orientation theorem without an independently
eligible bridge.  Conversely, the neutral label-swap result does not erase a
source-internal premise; it locates the extra authority doing the orienting.

### Deep AR, AW, AX, AP, and BC

```text
Deep AR:
  deterministic copies preserve one root experiment rather than multiplying it;

Deep AW:
  robust root-level diagnosis does not orient class labels toward truth;

Deep AX:
  architecture-conditioned likelihoods presuppose a truth-oriented source model;

Deep AP:
  a singleton relative referent is still conditional on an admissible
  interpretation family and actual-world selection;

Deep BC:
  observationally equivalent experiments cannot be discriminated by a common
  downstream decision problem; calibration is a genuinely enlarged experiment.
```

## 8. Source and implementation firewall

Current main distinguishes machine source-dependence analysis from
creed-internal tawatur warrant.  Its false-tawatur fixtures forbid numeric or
prevalence-based warrant and distinguish copies/common source from supported
route independence.  Its qualitative tawatur example separately records
origin, path independence, non-collusion, transmitter honesty and competence,
content coherence, acquisition, defeaters, and subject-relative assessment.

Dawid–Skene supplies a classical latent observer-error model.  Latent-class
identifiability literature explicitly treats label swapping as observational
nonidentifiability and proves only guarded identifiability up to that swap in
selected model classes.  Neither body of work is the historical Taymiyyan
theory of tawatur.

The present result is a finite statistical/source-custody control.  It does not
reduce tawatur, fiṭrah, revelation, or source truth to majority voting or latent
class estimation.

## 9. Ancestry and novelty ceiling

```text
mathematical ancestry:
  finite mixture label switching and latent-class identifiability;

statistical model ancestry:
  Dawid-Skene observer-error estimation;

AR8R ancestry:
  Deep AR source-root conservation;
  Deep AW root-robust diagnosis;
  Deep AX source-likelihood gate;
  Deep AP source-world referent fibre;
  Deep BC experiment parity;

implementation correspondence:
  current-main false-tawatur and qualitative tawatur controls;

general mathematical novelty:
  0;

historical identity:
  NONE.
```

## 10. Conclusion ceiling

The strongest admitted candidate conclusion is:

> In the declared finite latent-source model, the complete unlabeled report law
> cannot orient the latent classes toward world truth.  Orientation requires a
> non-swap-invariant input.  A current authenticated truth-labeled calibration
> contract is sufficient to select one orientation only after the component
> model has independently been identified up to the swap.

It does not establish actual-world truth, source honesty, competence,
conditional independence, tawatur warrant, personal agency, revelation, or an
integrated metaphysical champion.
