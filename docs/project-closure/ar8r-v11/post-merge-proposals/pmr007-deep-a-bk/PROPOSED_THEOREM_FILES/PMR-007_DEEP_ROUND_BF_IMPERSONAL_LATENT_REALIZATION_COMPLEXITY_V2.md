# PMR-007 Deep Round BF V2 — real nonnegative latent-product complexity and rival-width boundary

```text
identity: PMR-007-ILRC-1
round: DEEP_BF
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
```

## 1. Typed setting

Let `X,Y` be finite nonempty sets and let

\[
P\in\Delta(X\times Y)
\]

be one frozen **bivariate observational** probability law from one common
registered experiment.

A real latent-product realization of width `r` is

\[
P(x,y)=\sum_{h=1}^{r}\lambda_h a_h(x)b_h(y),
\]

where every `lambda_h > 0`, the weights sum to one, and
`a_h in Delta(X)`, `b_h in Delta(Y)`. Zero-weight terms are omitted. Let
`LRC_R(P)` be the least such width.

Let `rank_+^R(P)` be the minimum inner dimension in a factorization
`P=UV` over nonnegative real matrices. A rational quantity `rank_+^Q(P)`
is distinct and is not identified with it.

## 2. Exact scoped results

### ILRC-1A — normalized product-mixture equivalence

\[
\boxed{\operatorname{LRC}_{\mathbb R}(P)=
       \operatorname{rank}_{+}^{\mathbb R}(P)}.
\]

A latent product realization is already a sum of nonnegative rank-one
matrices. Conversely, for `P=UV=sum_h u_h v_h^T`, put
`s_h=sum_x u_h(x)` and `t_h=sum_y v_h(y)`. If `s_h t_h=0`, nonnegativity makes
the term zero, so delete it. Otherwise define

\[
\lambda_h=s_ht_h,\qquad a_h=u_h/s_h,\qquad b_h=v_h/t_h.
\]

Because `P` has total mass one, the remaining `lambda_h` sum to one. This
normalizes any real nonnegative factorization into a latent-product mixture
without increasing width.

### ILRC-1B — rank and saturation bounds

\[
\boxed{\operatorname{rank}(P)
       \le \operatorname{LRC}_{\mathbb R}(P)
       \le \min(|X|,|Y|)}.
\]

The upper bound is realized by taking `H=X` (or symmetrically `H=Y`) and using
row masses together with the conditional laws `P(Y|X=x)`; zero-mass rows are
omitted.

### ILRC-1C — common-channel monotonicity

Let `K_X(x'|x)` and `K_Y(y'|y)` be column-stochastic Markov kernels and

\[
P'=K_X P K_Y^{\mathsf T}.
\]

Then

\[
\boxed{\operatorname{LRC}_{\mathbb R}(P')
       \le \operatorname{LRC}_{\mathbb R}(P)}
\]

because each factor pushes forward to `(K_X a_h)(K_Y b_h)^T`. The inequality
can be strict. For comparative evidence, the channel must be common and
preregistered, or its selection mechanism must be modelled separately.

### ILRC-1D — width-restricted rival exclusion

For the formal rival class

\[
\mathcal R_{r_0}=\{P:\operatorname{LRC}_{\mathbb R}(P)\le r_0\},
\]

\[
\boxed{P\notin\mathcal R_{r_0}
       \iff \operatorname{rank}_{+}^{\mathbb R}(P)>r_0}.
\]

This is evidentially useful only when `r_0` has an independent empirical,
structural, implementation, intervention, or source warrant.

### ILRC-1E — unrestricted finite bivariate saturation

Every finite bivariate observational law has a formal latent-product
realization of width at most `min(|X|,|Y|)`. Therefore a bivariate joint law
alone cannot exclude an unrestricted finite impersonal latent-product model
class.

Here “impersonal” means only that the formal model includes no personal,
first-person, intentional, or Wisdom predicate. It does not establish physical
or metaphysical actuality.

### ILRC-1F — support-rectangle lower bound

Let `rcov(supp(P))` be the minimum number of combinatorial rectangles covering
the support. Each nonnegative rank-one term has rectangular support, so

\[
\boxed{\operatorname{rcov}(\operatorname{supp}P)
       \le \operatorname{rank}_{+}^{\mathbb R}(P)}.
\]

This is only a lower bound; it is exact for the diagonal witnesses used here.

## 3. Positive witnesses

```text
BF-POS1 PRODUCT:
  P = a b^T; LRC_R(P)=1.

BF-POS2 BINARY EQUALITY:
  diag(1/2,1/2) has ordinary rank, rectangle-cover number,
  and LRC_R all equal to 2.

BF-POS3 N-WAY EQUALITY:
  I_n/n has ordinary rank, rectangle-cover number,
  and LRC_R all equal to n.

BF-POS4 STRICT CHANNEL CONTRACTION:
  merging all X states sends I_n/n to a rank-one law.
```

## 4. Stronger-reading controls

```text
BF-CM1 UNRESTRICTED SATURATION:
  H=X realizes every finite bivariate law.

BF-CM2 WIDTH IS NOT SUBJECT COUNT:
  one n-state impersonal randomizer and one personal agent can each realize
  I_n/n; width counts mixture terms, not bearers.

BF-CM3 RANK ONE IS NOT CAUSAL UNITY:
  one product law is compatible with several causal and ontological stories.

BF-CM4 FACTORIZATION NONUNIQUENESS:
  P need not identify factors, latent meanings, or label orientation.

BF-CM5 CANDIDATE-SPECIFIC RECODING:
  different maps can create comparison artifacts; one common channel is needed.

BF-CM6 INTERVENTIONAL NONTRANSFER:
  observationally equal systems can disagree under interventions.

BF-CM7 TENSOR NONTRANSFER:
  one matrix flattening can lose multiway compatibility.

BF-CM8 REAL/RATIONAL SPLIT:
  a rational matrix can have different minimum nonnegative rank over R and Q.
```

## 5. Candidate-G and R5 effect

Deep BE showed that a joint interaction can distinguish candidates with equal
proper marginals. Deep BF identifies the next boundary:

```text
a bivariate interaction defeats a width-r0 impersonal latent rival
iff its real nonnegative rank exceeds r0;

without an independently warranted width or structural restriction,
every finite bivariate interaction remains formally impersonal-realizable.
```

Thus the strongest unrestricted R5 rival survives. Meniscus-relevant progress
requires a justified width bound, shared-latent interventional constraint,
modularity/causal restriction, source/world applicability restriction, or a
constitutive intentional bridge not recoverable from the same observational
law.

## 6. Authority and ancestry

```text
mathematical ancestry:
standard nonnegative-rank-one decomposition and probability normalization;
standard rank bounds; standard monotonicity under nonnegative multiplication

project relation:
typed Candidate-G/R5 application and burden relocation

general mathematical novelty:
0

historical identity:
NONE

external mathematical review:
OPEN

owner adoption:
PENDING
```

The rational checker supplies finite exact regression evidence only. It does
not compute generic real nonnegative rank. No Lean source, elaboration, or
kernel claim is made.

## 7. Nonclaims

Deep BF does not establish unique latent semantics, causal or interventional
identification, tensor rank, metaphysical actuality, bearer/subject/agent or
provenance-root count, personality, agency, fitting selection, Wisdom, one
common bearer, Necessary Being, Creatorhood, divine Speech, revelational
identification, integrated champion, meniscus, or closure.
