# PMR-007 Deep Round AR — provenance-root evidence conservation under retransmission V2

```text
campaign: AR8R_POST_MERGE_MENISCUS_PROGRAM_V1
wave: PMR-007
round: Deep AR
canonical post-merge identity: PMR-007-PREC-1
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
repository authority inspected: 4c3dc103e8c753690fa5de560ab82157392ced4c
```

## 1. Central question

When do multiple messages, copies, synchronizations, translations, or agents supply multiple pieces of evidence rather than multiple presentations of one acquisition root?

The answer requires an authenticated provenance-root model. Printed labels, carriers, message count, and storage count are not roots by themselves.

## 2. Typed finite setting

Let `H={A,R}` be the compared hypotheses. Let `r` range over a finite set of **authenticated acquisition roots**. Root `r` produces an observation `X_r` with distributions

\[
P_A^r,\quad P_R^r.
\]

A retransmitted message bundle `Y` is generated from a root observation by one common candidate-independent Markov channel `K`:

\[
H\to X_r\to Y.
\]

An exact faithful copy is a channel sufficient for the root likelihood ratio; a lossy paraphrase need not be sufficient. A candidate-dependent transmitter defines a different experiment and is excluded from the conservation theorem.

## 3. PREC-1A — retransmission data processing

For every common channel `K`,

\[
TV(K_*P_A^r,K_*P_R^r)\le TV(P_A^r,P_R^r).
\]

Thus copying, forwarding, synchronization, paraphrase, or format conversion cannot create architecture discrimination absent from the authenticated root experiment.

## 4. PREC-1B — faithful copies preserve rather than exponentiate likelihood

Suppose a message bundle is a faithful deterministic encoding `Y=c(X_r)` that is sufficient for the pointwise likelihood ratio. Then for every received bundle `y` in the common support,

\[
\frac{P_A(Y=y)}{P_R(Y=y)}
=
\frac{P_A^r(X_r=x)}{P_R^r(X_r=x)}
\]

for the corresponding root observation `x`.

If the same root observation is copied `n` times, the joint copy tuple is a deterministic function of that one observation. Its likelihood ratio is the root ratio, not its `n`th power. Treating the copies as conditionally independent double-counts one root.

## 5. PREC-1C — independent roots multiply evidence

Let authenticated roots `r_1,...,r_m` be conditionally independent given `H`. Then

\[
P_h(x_1,\ldots,x_m)=\prod_{j=1}^m P_h^{r_j}(x_j)
\]

and, wherever the denominator is positive,

\[
\Lambda(x_1,\ldots,x_m)
=
\prod_{j=1}^m \Lambda_{r_j}(x_j).
\]

For finite positive ratios,

\[
\log\Lambda=\sum_j\log\Lambda_{r_j}.
\]

This motivates the scoped invariant:

```text
provenance-adjusted log evidence
=
sum of log likelihood ratios over authenticated conditionally independent roots,
not over messages, carriers, copies, or labels.
```

The independence factorization is a premise, not a consequence of distinct names or paths.

## 6. PREC-1D — root contraction and alias invariance

If several message nodes contract to one authenticated root, evidential accounting is invariant under the contraction. Splitting one root into aliases does not change the root experiment. Conversely, conflating distinct roots under one printed label can undercount evidence.

Therefore both root aliasing and root merging are errors unless an independently supported root-equivalence relation is supplied.

## 7. Countermodels

### AR-CM-COPY-COUNT

One binary root observation has likelihood ratio `L`. A bundle containing `n` exact copies has likelihood ratio `L`; naive independent-copy multiplication yields `L^n` and overcounts whenever `L` is finite and not `0`, `1`, or `∞`.

### AR-CM-ROOT-ALIAS

Two printed source identifiers point to one acquisition event. Apparent source multiplicity is one actual root.

### AR-CM-ROOT-MERGE

One displayed source identifier combines two conditionally independent acquisition events. Label count undercounts root multiplicity.

### AR-CM-CANDIDATE-CHANNEL

The transmitter encodes different messages depending directly on whether `A` or `R` is true. The channel can create discrimination, but it is not a common retransmission channel and therefore defines a changed experiment.

### AR-CM-DEPENDENT-ROOTS

Two apparent roots are deterministic functions of one hidden cause. Product likelihood is invalid without the conditional-independence factorization.

### AR-CM-WARRANT-NONTRANSFER

Several authenticated roots may still fail truth, competence, source eligibility, recipient authority, version, applicability, invalidator closure, mutual knowledge, or common knowledge. Machine provenance is not the whole warrant relation.

## 8. Candidate and flywheel effects

### Candidate A

Pooled message count does not measure independent evidence. Distributed diagnosis must account over authenticated roots and the recipient's local contract.

### Candidate B

Synchronized restorative records sharing one root do not multiply causal support for restoration. Route selection and burden landing must preserve root custody.

### Candidate C

Multiple source presentations or translations do not create independent support for a metaphysical architecture when they share one source root. Source multiplicity must remain separate from world truth.

### Deep AQ

`GATE E` is supplied by independent experiments or roots, not by repeated copies of one likelihood ratio.

### TAC/SAC and false tawātur

Multiple carriers, episodes, or copies do not raise evidential independence rank merely by being numerically multiple.

## 9. Tawātur and source boundary

Current daee source-copying controls distinguish machine source-dependence analysis from creed-internal tawātur warrant. The present theorem concerns finite probabilistic evidence under authenticated roots. It does not establish the historical, testimonial, competence, truth, impossibility-of-collusion, or school-internal conditions of tawātur.

## 10. Ancestry and novelty

```text
Deep AO:
common-channel data processing.

Round 19:
canonical-root access and root-multiplicity query interface.

AR2/AR3 and agentic communication:
provenance-preserving transport and recipient re-orthing.

TAC/SAC / false tawatur:
common-source and copied-availability controls.

AR8R-T227:
root authentication/factorization boundary.

general mathematical novelty:
0.

historical identity:
NONE.
```

The contribution is a cross-lane evidence-accounting invariant and explicit anti-false-multiplicity interface.

## 11. Nonclaims

- Root identity is not inferred from labels.
- Conditional independence is not inferred from distinct carriers or routes.
- Evidence is not truth, warrant, source authority, common knowledge, or adoption.
- The theorem does not authenticate any source or experiment.
- The theorem does not establish equal or unequal metaphysical priors.
- Proposal-level admission does not authorize repository adoption.
