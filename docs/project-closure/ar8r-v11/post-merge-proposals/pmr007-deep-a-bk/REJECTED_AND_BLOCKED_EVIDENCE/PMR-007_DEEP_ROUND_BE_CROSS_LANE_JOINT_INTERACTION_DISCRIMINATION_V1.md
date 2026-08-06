# PMR-007 Deep Round BE V1 — cross-lane joint interaction discrimination and the unification-evidence gate

```text
identity: PMR-007-CJID-1
round: DEEP_BE
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_burden: whether integrated cross-domain evidence can break architecture parity when every lane viewed separately is nondiscriminating
```

## 1. Frozen comparison surface

Let `A` be the unified-personal architecture and `R` the strongest matched
impersonal/powers rival.  Let

\[
X=(X_1,\ldots,X_k)\in\Omega_1\times\cdots\times\Omega_k
\]

be one jointly sampled, provenance-bound, version-bound registered experiment.
Coordinates may represent, for example:

```text
source report;
semantic truth score;
intervention response;
normative correction outcome;
representation trajectory;
recipient uptake;
or temporal restoration status.
```

Let `P_A` and `P_R` be the architecture-conditioned joint laws on the same
frozen sample space.  A lane-specific analysis sees a marginal or proper-subset
projection; an integrated analysis sees a declared joint event or statistic.

## 2. CJID-1A — marginal parity does not imply joint parity

If every one-coordinate marginal agrees,

\[
(P_A)_{X_i}=(P_R)_{X_i}\qquad(i=1,\ldots,k),
\]

the joint distributions may still differ.  Therefore separate lane parity does
not establish architecture parity on the joint experiment.

Conversely, if `P_A=P_R` jointly, no event, statistic, common representation,
or finite expected-utility decision problem built from that same experiment can
discriminate the architectures.

## 3. CJID-1B — exact two-binary coupling invariant

Let `X,Y in {0,1}` and suppose `P_A` and `P_R` have the same `X` and `Y`
marginals.  Put

\[
\delta=P_A(X=1,Y=1)-P_R(X=1,Y=1).
\]

The common marginals force the signed cell difference to be

\[
\begin{array}{c|cc}
&Y=0&Y=1\\\hline
X=0&\delta&-\delta\\
X=1&-\delta&\delta
\end{array}
\]

and hence

\[
TV(P_A,P_R)=2|\delta|
=2\,|\operatorname{Cov}_{P_A}(X,Y)-\operatorname{Cov}_{P_R}(X,Y)|.
\]

Thus, in the two-binary equal-marginal case, all architecture discrimination is
exactly coupling discrimination.

## 4. CJID-1C — top-order parity characterization

Let `X_1,...,X_k` be binary.  Suppose `P_A` and `P_R` have equal marginals on
every proper subset of coordinates.  Then their signed difference has the form

\[
P_A(x)-P_R(x)=c(-1)^{x_1+\cdots+x_k}
\]

for one scalar `c`.  Equivalently, the only possible discriminator is the
full `k`-way parity interaction.  Moreover,

\[
TV(P_A,P_R)
=
\frac12\left|
\mathbb E_{P_A}[(-1)^{\sum_iX_i}]
-
\mathbb E_{P_R}[(-1)^{\sum_iX_i}]
\right|.
\]

### Proof sketch

A signed measure with zero marginal on every proper coordinate subset lies in
the one-dimensional tensor product of the zero-sum subspaces of all binary
coordinates.  That tensor product is spanned by the parity sign function.
Summing absolute values and pairing with parity gives the total-variation
formula.

## 5. CJID-1D — separable tests cannot see the missing interaction

If every proper-subset marginal agrees, then every statistic expressible as a
sum of functions each depending on a proper subset has equal expectation under
`P_A` and `P_R`.  Any discriminator must evaluate a genuinely full-joint
interaction or use a changed experiment.

This gives Candidate G an exact evidential gate:

```text
mere availability of modal, semantic, causal, normative, representational,
and source coordinates is not integration evidence;

a preregistered cross-domain interaction predicted differently by A and R is
eligible discrimination evidence;

if the strongest rival is allowed to match the same joint law, parity remains.
```

## 6. Positive and negative constructions

```text
BE-POS1 EVEN/ODD PARITY:
  P_A is uniform on even-parity binary strings;
  P_R is uniform on odd-parity strings.
  Every proper marginal is uniform and identical, while supports are disjoint
  and TV=1.

BE-POS2 TWO-LANE COUPLING:
  equal Bernoulli marginals with different P(1,1) values yield exact positive
  joint discrimination quantified by 2|delta|.

BE-CM1 PRODUCT-OF-MARGINALS BLINDNESS:
  analyzing each lane separately records complete parity despite a maximally
  different joint law.

BE-CM2 POST-HOC INTERACTION:
  an analyst searches many couplings after seeing outcomes and reports only a
  favorable one.  This does not supply preregistered architecture evidence.

BE-CM3 UNIT/PROVENANCE MISMATCH:
  source, intervention, and restoration records from different subjects,
  versions, or worlds are joined as if jointly sampled.  The apparent coupling
  is not one admissible experiment.

BE-CM4 COMMON REPRESENTATION LOSS:
  a channel that discards the parity coordinate sends the two joint laws to the
  same representation.  Representation alignment cannot recover the lost
  discriminator.

BE-CM5 IMPERSONAL COUPLING REALIZER:
  an impersonal field or powers architecture realizes the same nonproduct joint
  law as the personal architecture.  Joint constraint alone does not establish
  one subject, intentionality, or Wisdom.

BE-CM6 SOURCE-COMPATIBLE JOINT PARITY:
  source-relative predicates and neutral interventions have identical joint
  laws under A and R.  Source compatibility plus multiple lanes supplies no
  discriminator.

BE-CM7 SELECTED-SUBSET OVERREAD:
  equality of one-coordinate marginals does not mean all lower-order
  interactions agree.  The top-order theorem requires equality on every proper
  subset.
```

## 7. Empirical and representation interface

The hippocampal OSM study reports not merely an endpoint representation but a
learning trajectory: among the tested models, CSCG reproduced both the final
orthogonalized state structure and the observed progression.  This illustrates
how a temporal/joint signature may discriminate models that share selected
endpoint properties.  It does not identify the true biological algorithm, a
proper function, a personal subject, or a metaphysical ground.

PRH-style kernel alignment is likewise a representation-level coordinate.  A
common representation cannot create a joint architecture difference that is
absent in the underlying experiment, and it may erase a higher-order
interaction.

## 8. Cross-lane effects

### Candidate G / epistemic unification

Candidate G receives an exact positive evidence target: derive and predict a
cross-domain interaction under a frozen experiment, rather than count
coordinates or place them in one bearer.  The result does not say that every
interaction is explanatory unification.

### Candidate A / source and collective evidence

Independent roots and communication channels may have equal individual
marginals while their joint provenance/warrant pattern differs.  Joint sampling
and root custody are required before using the dependence.

### Candidate B / restoration

Endpoint correctness and source agreement may be marginally identical across
architectures while learning/restoration trajectories differ.  A temporal
interaction is eligible only under one model-bound, causally interpretable
experiment.

### Candidate C / transcendental ascent

Multiple neutral lanes do not accumulate into a personal-ground conclusion by
conjunction.  A genuine cross-lane prediction can discriminate a rival, but an
impersonal architecture may realize the same coupling.

## 9. Ancestry and novelty ceiling

```text
mathematical ancestry:
finite probability, total variation, contingency tables, log-linear/ANOVA
interaction decomposition;

Deep AN/BC:
predictive surplus and common-experiment parity;

Deep AO:
common-channel data processing;

Candidate G:
derivational-unification and carrier-boxing burden;

general mathematical novelty:
0;

historical identity:
NONE.
```

## 10. Nonclaims

- Joint dependence is not causation, derivation, intention, or explanation.
- A nonproduct support does not establish one bearer or one subject.
- The theorem does not canonically select an experiment or interaction.
- Equal marginals in observed data do not establish exact population equality.
- The OSM and PRH studies do not test personal versus impersonal metaphysics.
- Proposal admission would not authorize repository adoption.
