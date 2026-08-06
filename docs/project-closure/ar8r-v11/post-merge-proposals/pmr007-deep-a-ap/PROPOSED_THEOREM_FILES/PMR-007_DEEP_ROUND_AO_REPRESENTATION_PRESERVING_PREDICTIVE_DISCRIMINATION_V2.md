# PMR-007 Deep Round AO V2 — representation-preserving predictive discrimination

```text
identity: PMR-007-RPDS-1
round: PMR-007-DEEP-AO
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_task: characterize when a representation preserves an architecture discriminator rather than relocating it
```

## 1. Frozen experiment and support

Let `Ω` be finite and let architectures `A,R` induce frozen distributions
`P,Q`. Define the union support

\[
S=\{x\in\Omega:P(x)+Q(x)>0\}.
\]

A deterministic representation is `T:S→Y`. Its pushforwards are `P_T,Q_T`.
Define the extended likelihood ratio on `S` by

\[
L(x)=P(x)/Q(x)\quad(Q(x)>0),
\]

and `L(x)=+∞` when `P(x)>0,Q(x)=0`.

Impossible points outside `S` have no likelihood-ratio or minimality role.

## 2. RPDS-1A — common-channel data processing

For every deterministic `T`,

\[
TV(P_T,Q_T)\leq TV(P,Q).
\]

More generally, for every common finite Markov kernel `K`,

\[
TV(PK,QK)\leq TV(P,Q).
\]

A common recoding or randomized channel cannot create predictive separation
absent from the frozen experiment. A new sensor, intervention, or query may add
information only by defining an enlarged experiment, not by recoding the old
one.

## 3. RPDS-1B — exact pointwise Bayes-factor sufficiency

The following are equivalent on `S`:

```text
for every x, the represented extended likelihood ratio at T(x) equals L(x);

L is constant on every T-fibre;

on every fibre with positive P_T and Q_T, the conditional distributions
P(.|T=y) and Q(.|T=y) agree; fibres with Q_T=0 carry the separate +infinity
case.
```

Thus a deterministic representation preserves every pointwise Bayes factor
exactly iff the frozen architecture likelihood ratio factors through it.

This is stronger than equality in the total-variation data-processing bound.

## 4. RPDS-1C — coarsest support-relative exact discriminator

The partition of `S` by equal extended likelihood ratio is the coarsest
deterministic representation preserving all pointwise Bayes factors for the
frozen pair `(P,Q)`. Every exact representation restricted to `S` refines it.
Behaviour on `Ω\S` is arbitrary.

The result is pair-relative. It supplies neither a natural vocabulary nor a
sufficient statistic for other candidate pairs.

## 5. Candidate-G and Bitter-Lesson consequence

Deep AN requires predictive surplus for Candidate G P6. Deep AO establishes the
representation contract:

```text
a claimed A-over-R predictive surplus must exist in the frozen raw or
independently enlarged experiment;

a common hand-authored, learned, or randomized representation can preserve or
destroy that surplus but cannot manufacture it;

full pointwise preservation requires likelihood-ratio constancy on fibres;

representation selection and held-out evaluation must be separated.
```

Architecture comparison should therefore include raw/minimal, hand-authored,
and learned representations under matched information, compute, train/held-out
splits, and one common scoring contract.

## 6. Positive constructions and controls

### AO-POS1 — likelihood-ratio representation

`T=L` preserves all pointwise Bayes factors and is coarsest on `S`.

### AO-CM1 — destructive coarsening

Outcomes with opposite likelihood ratios are merged. Total variation strictly
decreases and exact Bayes factors are lost.

### AO-CM2 — equal raw experiment

If `P=Q`, every common deterministic or stochastic channel preserves equality.
Any represented discrimination must come from changed measurement, selection,
sampling, scoring, or candidate definitions.

### AO-CM3 — target leakage

A representation constructed using held-out outcomes can appear perfectly
predictive but violates the frozen experiment contract.

### AO-CM4 — new evidence versus recoding

An intervention reveals a variable absent from `Ω` and separates the
architectures. This is legitimate only as a new experiment with its own
likelihoods and custody, not as evidence that a representation of the old data
created information.

### AO-CM5 — PRH/OSM nontransfer

Kernel alignment, state separation, trajectory fit, and latent-state inference
may discriminate empirical models at their declared task scope. They do not by
themselves specify `P_A/P_R` for personal versus impersonal metaphysical
architectures.

## 7. Theorem-family and novelty

The formal results are standard finite statistical sufficiency and data
processing. They are a guarded likelihood-ratio specialization of the recurring
fibre/factorization family.

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
a correct or complete raw experiment;
a canonical likelihood, representation, or scoring rule;
that learned or hand-authored representations are superior;
that PRH or OSM validates a metaphysical architecture;
proper function, mentality, personality, Wisdom, Speech, or source truth;
an integrated champion, meniscus, or natural closure.
```
