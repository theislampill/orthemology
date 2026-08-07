# PMR-007 Deep BF — nonnegative-rank ancestry, factorization field, and scope note

## Primary sources pinned

### Cohen and Rothblum (1993)

```text
title:
Nonnegative Ranks, Decompositions, and Factorizations of Nonnegative Matrices

authors:
Joel E. Cohen; Uriel G. Rothblum

journal:
Linear Algebra and its Applications 190 (1993), 149–168

local evidence file:
Cohen_Rothblum_1993_Nonnegative_Ranks.pdf

SHA-256:
8151e9a43bedd714290f3bd3d51916c8854d3985d4fd3d588ccec783eb85195b

authority supplied:
foundational definition/equivalence of nonnegative rank,
nonnegative factorization, and nonnegative rank-one decomposition;
probability/stochastic normalization ancestry
```

### Chistikov, Kiefer, Marušić, Shirmohammadi, and Worrell (2017)

```text
title:
Nonnegative Matrix Factorization Requires Irrationality

journal:
SIAM Journal on Applied Algebra and Geometry 1(1), 285–307

arXiv:
1605.06848v2

local evidence file:
Chistikov_et_al_2017_NMF_Requires_Irrationality.pdf

SHA-256:
5c382caf391de7904cd1af16723481b6090ed261281c4bd7c5cb96b1becaed9a

authority supplied:
real/rational nonnegative-rank distinction;
negative answer to the Cohen–Rothblum rational-factorization question;
field-sensitive notation and computational-scope cautions
```

## Ancestry disposition

The equality between finite bivariate product-mixture width and matrix
nonnegative rank is not a new general theorem. It is the probability-normalized
form of the standard nonnegative rank-one decomposition definition.

```text
PMR-007-ILRC-1A:
APPLICATION / NORMALIZED REFORMULATION OF STANDARD NONNEGATIVE-RANK THEORY

PMR-007-ILRC-1B:
STANDARD RANK BOUNDS

PMR-007-ILRC-1C:
STANDARD MONOTONICITY UNDER NONNEGATIVE LEFT/RIGHT MULTIPLICATION,
TYPED AS COMMON MARKOV CHANNELS

PMR-007-ILRC-1D:
DEFINITIONAL EXCLUSION OF A WIDTH-BOUNDED RIVAL CLASS

PMR-007-ILRC-1E:
CANONICAL SATURATION CONTROL H=X OR H=Y

general mathematical novelty:
0
```

The project-specific value is a precise R5/Candidate-G burden relocation:
observed cross-lane interaction excludes an impersonal latent-product rival only
when the rival's width or structural restrictions are independently warranted.

## Field firewall

For a rational probability matrix `P`, define separately:

```text
rank_+^R(P):
minimum inner dimension over nonnegative real factors

rank_+^Q(P):
minimum inner dimension over nonnegative rational factors
```

The primary executable checker uses exact rational arithmetic. It validates
explicit rational constructions and finite regressions. It does not establish
that `rank_+^Q(P) = rank_+^R(P)` in general; the cited irrationality result
shows that such an equality can fail.

The canonical Deep BF theorem is therefore over nonnegative reals.

## Computational and evidential ceiling

The finite executable evidence does not solve generic nonnegative-rank
optimization. It checks explicit constructions and regressions only. It does
not provide a generic minimum-rank algorithm, unique latent semantics, causal
identification, interventional compatibility, tensor characterization,
metaphysical actuality, bearer/subject count, personality, agency, Wisdom, or
divine unity.
