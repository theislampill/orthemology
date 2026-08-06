# PMR-007 Deep Round AO V1 — representation-preserving predictive discrimination

```text
identity: PMR-007-RPDS-1
round: PMR-007-DEEP-AO
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_task: characterize when a representation preserves an architecture discriminator rather than relocating it
```

## 1. Finite binary experiment

Let `Ω` be a finite registered raw-evidence space and let candidate
architectures `A` and `R` induce frozen distributions `P` and `Q` on `Ω`.
Let a deterministic representation be `T:Ω→Y`, with pushforwards `P_T,Q_T`.
All zero-union-support points are removed from the comparison.

Define the extended likelihood ratio

```text
L(x)=P(x)/Q(x) when Q(x)>0;
L(x)=+infinity when P(x)>0 and Q(x)=0.
```

## 2. RPDS-1A — representation data processing

For total variation,

\[
TV(P_T,Q_T)\leq TV(P,Q).
\]

A deterministic recoding cannot create predictive discrimination absent from
the raw experiment. A bijective recoding preserves it.

## 3. RPDS-1B — exact Bayes-factor sufficiency

The following are equivalent:

```text
for every attained y and every x in T^{-1}(y), the raw likelihood ratio L(x)
is equal to the represented likelihood ratio P_T(y)/Q_T(y);

L is constant on every T-fibre;

the conditional distributions P(.|T=y) and Q(.|T=y) agree on every common-
support fibre.
```

Thus a representation preserves every pointwise Bayes factor exactly iff the
candidate likelihood ratio factors through that representation.

## 4. RPDS-1C — coarsest pairwise discriminator

The likelihood-ratio partition `x~x' iff L(x)=L(x')` is the coarsest
deterministic representation that preserves all pointwise Bayes factors for the
frozen pair `(P,Q)`. Every exact discriminator refines that partition.

This minimality is pair-relative. It is not a universal natural vocabulary,
semantic representation, or sufficient statistic for other candidate pairs.

## 5. Candidate-G and Bitter-Lesson consequence

Deep AN requires a predictive surplus for Candidate G P6. Deep AO adds:

```text
any claimed A-over-R predictive surplus must already exist in the frozen raw
experiment or in an independently warranted intervention experiment;

a hand-authored or learned representation may preserve or discard that surplus,
but a common deterministic representation cannot manufacture it;

exact preservation requires the A/R likelihood ratio to be constant on its
fibres.
```

Therefore architecture comparison should include raw/minimal, hand-authored,
and learned representations and test whether the result survives every
representation that is sufficient for the frozen comparison.

## 6. Positive and negative controls

### AO-POS1 — likelihood-ratio representation

`T=L` preserves every raw Bayes factor and is coarsest at the declared pairwise
scope.

### AO-CM1 — destructive coarsening

Two raw outcomes have opposite likelihood ratios but are mapped to one token.
The represented Bayes factor becomes their weighted average and exact evidence
is lost.

### AO-CM2 — equal raw experiment

If `P=Q`, then `P_T=Q_T` for every common deterministic representation. Any
reported represented discrimination must come from a changed measurement,
sampling, selection, scoring, or candidate contract.

### AO-CM3 — target leakage

A representation constructed with access to held-out outcomes can appear
perfectly discriminative while violating the preregistered measurement
contract. This is not evidence created by representation learning.

### AO-CM4 — PRH/OSM nontransfer

Kernel alignment, state separation, or trajectory fit may distinguish models
for their declared empirical tasks. It does not by itself supply a likelihood
ratio between a unified-personal metaphysics and a matched impersonal rival.

## 7. Theorem-family and novelty ceiling

The formal core is a standard finite statistical-sufficiency and data-
processing result. It is related to the recurring profile/fibre family, but the
target here is the architecture-pair likelihood ratio rather than a generic
truth predicate.

```text
general_mathematical_novelty: 0
historical_identity: NONE
repository_status: PROPOSAL_EVIDENCE_ONLY
external_review: OPEN
owner_adoption: PENDING
```

## 8. Nonclaims

No result establishes:

```text
a canonical raw evidence space;
a correct likelihood model;
a universal sufficient representation;
that learned or hand-authored representations are superior;
that PRH or OSM validates a metaphysical architecture;
proper function, mentality, personality, Wisdom, or Speech;
an integrated champion, meniscus, or natural closure.
```
