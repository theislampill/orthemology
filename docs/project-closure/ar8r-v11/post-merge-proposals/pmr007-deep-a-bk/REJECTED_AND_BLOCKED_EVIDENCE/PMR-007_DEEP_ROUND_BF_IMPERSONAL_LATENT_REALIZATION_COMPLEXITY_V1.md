# PMR-007 Deep Round BF V1 — impersonal latent realization complexity

```text
identity: PMR-007-ILRC-1
round: DEEP_BF
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_burden: whether a nontrivial cross-lane joint law excludes an impersonal latent-field realization
```

## 1. Candidate setting

Let `X` and `Y` be finite nonempty registered evidence domains and let

\[
P\in\Delta(X\times Y)
\]

be one architecture-conditioned joint probability matrix from a frozen common experiment.
A latent product realization of width `r` is

\[
P(x,y)=\sum_{h=1}^r \lambda_h a_h(x)b_h(y),
\]

where `lambda` is a probability vector and each `a_h`, `b_h` is a probability distribution.  The latent coordinate is treated as a formally impersonal common field unless a separate subject or agency predicate is independently supplied.

Define `LRC(P)` to be the minimum such `r`, and define `rank_+(P)` as the minimum inner dimension of a factorization `P=UV` with `U,V` entrywise nonnegative.

## 2. Candidate theorem

```text
ILRC-1A:
LRC(P) = rank_+(P).

ILRC-1B:
rank(P) <= LRC(P) <= min(|X|,|Y|).

ILRC-1C:
A common deterministic or stochastic coarse-graining of X and Y cannot
increase LRC.

ILRC-1D:
A rival class restricted to latent width at most r0 is excluded by a frozen
joint law P whenever rank_+(P) > r0.

ILRC-1E:
Without an independently warranted width, modularity, intervention, or
source constraint on the impersonal rival, every finite joint law admits an
impersonal latent product realization.
```

## 3. Proof sketch

A latent product realization directly gives a nonnegative rank-one decomposition. Conversely, normalize each nonzero rank-one term in a nonnegative factorization into a mixing weight and two probability vectors. Ordinary rank is a lower bound, and choosing `H=X` or `H=Y` gives the upper bound. Common stochastic maps push any factorization forward without increasing its inner dimension.

## 4. Central constructions

```text
BF-POS1 PRODUCT:
  Independent X,Y have LRC=1.

BF-POS2 BINARY EQUALITY:
  diag(1/2,1/2) has ordinary and nonnegative rank 2.

BF-POS3 THREE-WAY EQUALITY:
  I_3/3 has LRC=3 and defeats every width-2 latent rival.

BF-CM1 SATURATED IMPERSONAL FIELD:
  H=X with deterministic X output and conditional Y output realizes every P.

BF-CM2 COPY COUNT:
  repeated descendants of one latent source increase report availability but
  do not by themselves create additional independent latent causes.

BF-CM3 NONUNIQUE FACTORIZATION:
  one P may admit multiple latent decompositions and label permutations.

BF-CM4 COARSE REPRESENTATION:
  a common representation can lower latent complexity and erase an otherwise
  eligible interaction.

BF-CM5 PERSONALITY OVERREAD:
  one latent variable or one low-width mixture is not one subject, one bearer,
  intentional uptake, personality, Wisdom, or divine unity.
```

## 5. Proposed central consequence

Deep BE showed that joint interaction can discriminate candidates with equal marginals.  Deep BF asks the next load-bearing question: does that interaction force a personal unifier?  The candidate answer is no unless the matched impersonal model class is independently restricted.  Nonnegative rank supplies the exact two-lane latent-width invariant and an eligible positive discriminator against *restricted* rivals.

## 6. Initial scope ceiling

The candidate is finite and observational.  It does not yet distinguish real from rational factorizations, prove uniqueness of latent semantics, extend to arbitrary multiway tensors or intervention families, identify causal structure, or establish metaphysical possibility or actuality.  These issues are assigned to cold audit.
