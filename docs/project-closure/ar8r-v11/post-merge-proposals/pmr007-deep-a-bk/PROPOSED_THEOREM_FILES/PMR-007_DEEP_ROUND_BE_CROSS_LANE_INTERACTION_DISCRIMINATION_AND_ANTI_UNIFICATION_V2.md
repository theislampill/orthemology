# PMR-007 Deep Round BE V2 — cross-lane interaction discrimination and the anti-unification firewall

```text
identity: PMR-007-CJID-1
round: DEEP_BE
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_burden: what joint evidence can break architecture parity without being misclassified as explanatory or personal unity
```

## 1. Typed common experiment

Let `A` be the unified-personal architecture and `R` the strongest matched
impersonal/powers rival.  Let

\[
X=(X_1,\ldots,X_k)\in\Omega_1\times\cdots\times\Omega_k
\]

be one finite common experiment with architecture-conditioned laws `P_A` and
`P_R`.

The joint object is eligible only under a declared custody contract:

```text
UNIT:
  every coordinate belongs to the same declared subject, episode, world, or
  matched unit;

VER:
  source, model, membership, and semantic versions are aligned;

INT:
  observational and interventional regimes are not silently mixed;

ROOT:
  source and acquisition lineage are retained;

MAP:
  coordinate meanings and world references are common across A and R;

PRED:
  the architecture-conditioned joint prediction was frozen before the held-out
  outcome or is tested on a genuinely new experiment;

REP:
  any representation is one common channel applied to both candidates.
```

Without this contract, an apparent cross-lane coupling may be an artifact of
record joining, semantic drift, target selection, or candidate-dependent
processing.

## 2. CJID-1A — single-lane parity does not imply joint parity

If each coordinate marginal agrees,

\[
(P_A)_{X_i}=(P_R)_{X_i}\qquad(i=1,\ldots,k),
\]

the joint distributions may still differ.  A joint event can therefore
discriminate architectures even when every coordinate viewed separately is
nondiscriminating.

This conclusion does **not** imply that all lower-order interactions are equal.

If `P_A=P_R` on the complete common experiment, then every event, statistic,
common representation, and finite common-prior expected-utility decision built
from that same experiment has equal distribution or value under the two
architectures.  Breaking parity then requires a genuinely enlarged experiment,
an independently defended prior/model restriction, or source/world evidence at
its own authority level.

## 3. CJID-1B — exact two-binary coupling invariant

Let `X,Y in {0,1}` with their ordinary 0/1 coding.  Suppose `P_A` and `P_R`
have identical `X` and `Y` marginals.  Put

\[
\delta=P_A(1,1)-P_R(1,1).
\]

The equal marginals force the signed difference table

\[
\begin{array}{c|cc}
&Y=0&Y=1\\\hline
X=0&\delta&-\delta\\
X=1&-\delta&\delta.
\end{array}
\]

Consequently,

\[
TV(P_A,P_R)=2|\delta|
=2|\operatorname{Cov}_{P_A}(X,Y)-\operatorname{Cov}_{P_R}(X,Y)|.
\]

This covariance identity is not asserted for nonbinary variables, unequal
marginals, different codings, or observational samples with estimation error.

## 4. CJID-1C — top-order interaction characterization

Now let all `X_i` be binary and assume the stronger guard:

\[
(P_A)_{X_S}=(P_R)_{X_S}
\quad\text{for every proper subset }S\subsetneq\{1,\ldots,k\}.
\]

Let `Delta=P_A-P_R`.  For one binary coordinate the signed zero-sum subspace is
spanned by `(1,-1)`.  Vanishing of every proper marginal places `Delta` in the
tensor product of these zero-sum subspaces:

\[
\bigotimes_{i=1}^k\operatorname{span}\{(1,-1)\}.
\]

Hence there is one scalar `c` such that

\[
\Delta(x)=c(-1)^{x_1+\cdots+x_k}.
\]

Pairing with the parity character and summing absolute values gives

\[
TV(P_A,P_R)
=
\frac12\left|
\mathbb E_{P_A}[(-1)^{\sum_iX_i}]
-
\mathbb E_{P_R}[(-1)^{\sum_iX_i}]
\right|.
\]

Thus, under equality of every proper marginal, the only remaining difference is
the full `k`-way Walsh interaction.

## 5. CJID-1D — proper-subset tests are blind

Under the guard of Section 4, every statistic of the form

\[
f(X)=\sum_j f_j(X_{S_j}),
\qquad S_j\subsetneq\{1,\ldots,k\},
\]

has equal expectation under `P_A` and `P_R`.  Any eligible discriminator must
use a full-joint interaction or a changed experiment.

This is an exact target for Candidate G's open predictive-surplus burden:

```text
eligible progress:
  A and R make different frozen joint predictions under one common experiment;

not progress:
  more coordinates are stored in one object;
  a post-hoc coupling is selected;
  source-intended labels are imported into the neutral model;
  or the rival is permitted to match the same joint law.
```

## 6. Positive constructions and adversarial controls

```text
BE-POS1 EVEN/ODD PARITY:
  P_A is uniform on even-parity strings and P_R on odd-parity strings.
  Every proper marginal is uniform, supports are disjoint, and TV=1.

BE-POS2 TWO-LANE COUPLING:
  equal binary marginals with different P(1,1) values yield exact positive
  discrimination measured by 2|delta|.

BE-CM1 PRODUCT-OF-MARGINALS BLINDNESS:
  every separate lane is identical while the full joint law differs.

BE-CM2 POST-SELECTION:
  the interaction is chosen after the data are inspected.  This does not meet
  the frozen-prediction or held-out-experiment guard.

BE-CM3 UNIT/PROVENANCE MISMATCH:
  coordinates from different subjects, episodes, roots, versions, or worlds
  are joined.  The resulting array is not one common experiment.

BE-CM4 REPRESENTATION LOSS:
  a common channel discards parity, producing identical represented laws.

BE-CM5 IMPERSONAL COUPLING REALIZER:
  an impersonal field or distributed powers system realizes the same joint
  coupling.  Dependence does not establish one subject, intention, or Wisdom.

BE-CM6 SOURCE-COMPATIBLE JOINT PARITY:
  all source and neutral joint predictions remain equal under A and R.

BE-CM7 LOWER-ORDER OVERREAD:
  equality of one-coordinate marginals is mistaken for equality of all proper
  marginals; a pairwise interaction already distinguishes the candidates.

BE-CM8 COMMON-CAUSE NONDERIVATION:
  a common external cause produces cross-lane correlation without internal
  derivational unity of the registered coordinates.
```

## 7. OSM and PRH method comparison

The supplied hippocampal OSM study reports a progression from initially similar
activity to task-state-specific orthogonalized representations.  Among the
models it tested, CSCG reproduced both the selected final organization and the
reported learning trajectory, whereas selected alternative models could match
parts of the endpoint without the trajectory.  This is an empirical example of
a joint/temporal signature adding model discrimination beyond one endpoint.
It does not establish the uniquely true biological algorithm, proper function,
subjecthood, or metaphysical personality.

The PRH paper studies kernel-level representation alignment and its association
with scale and performance while retaining sensor, modality, metric, and
information-loss limitations.  Such alignment is not a personal-versus-
impersonal architecture likelihood.  A common representation may preserve or
erase a registered joint interaction; it cannot create one absent from the raw
common experiment.

## 8. Flywheel effects

### Candidate G / epistemic and explanatory unification

The round supplies a non-carrier-boxing evidence criterion: a candidate must
predict a joint restriction or interaction that the matched rival does not.
Even then, predictive discrimination is not automatically causal,
derivational, intentional, or personal unity.

### Candidate A / source and collective evidence

Source reports, acknowledgments, and provenance records require one matched
unit and root graph before their dependence is evidential.  Separate route
marginals can conceal a joint collusion or independence pattern.

### Candidate B / restoration

Endpoint success can be identical while the intervention/restoration trajectory
or burden/source interaction differs.  The joint temporal discriminator remains
model-bound and requires causal and version custody.

### Candidate C / transcendental ascent

Conjoining nondiscriminating formal, source, and metaphysical coordinates does
not defeat R5.  A cross-domain prediction can pressure a rival only when its
bridge and experiment are independently eligible.  An impersonal rival that
matches the joint law remains live.

### Deep AN, AO, BC, and BD

```text
Deep AN:
  joint interaction supplies a candidate nonunit likelihood ratio only when
  frozen before the held-out outcome;

Deep AO:
  a common representation contracts or preserves, but does not manufacture,
  the joint discriminator;

Deep BC:
  equal complete experiments imply universal decision parity;

Deep BD:
  source orientation itself requires a non-swap-invariant anchor before source
  coordinates can participate in a truth-oriented joint prediction.
```

## 9. Ancestry and novelty ceiling

```text
mathematical ancestry:
  finite contingency tables;
  total variation;
  Walsh/Fourier analysis on the Boolean cube;
  log-linear and ANOVA interaction decomposition;

AR8R relation:
  Candidate G predictive-surplus and real-unification burden;
  Deep AN/BC architecture discrimination;
  Deep AO representation sufficiency;

general mathematical novelty:
  0;

historical identity:
  NONE.
```

## 10. Conclusion ceiling

The admitted candidate conclusion is limited to:

> Marginal parity does not establish joint architecture parity.  Under equality
> of every proper binary marginal, the sole remaining distinction is the full
> parity interaction, and proper-subset tests are blind to it.  Such a frozen
> joint prediction can discriminate architectures, but does not by itself
> establish explanatory unity, one bearer, personality, or Wisdom.

No source truth, actual-world selection, personal-ground conclusion, or
repository adoption follows.
