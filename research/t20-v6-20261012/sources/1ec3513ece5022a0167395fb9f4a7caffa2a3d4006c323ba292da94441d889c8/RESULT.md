# Universal Bayes preservation of probability classes: the topology boundary

10 October 2026 UTC. Focused ordinary mathematical transport check. Scratch-only evidence; no integration, protected edit, release, audit closure, T20 closure, formal-kernel certificate, psychological identification, or theological conclusion. No field novelty is claimed.

## 1. Result and meaningful increment

The finite simplex theorem does transport, but its exact analogue depends on the topology:

1. On an arbitrary measurable space, a nonempty total-variation-closed convex class of countably additive probabilities is preserved by every bounded measurable likelihood bounded away from zero if and only if it is a total-variation-closed face of the probability simplex. Equivalently, it is downward closed under absolute continuity.
2. On a Polish space with its Borel sigma-algebra, a nonempty weakly closed convex class is preserved by all those likelihoods if and only if it consists of all probability measures carried by one nonempty closed set.
3. The first class need not be a point-support restriction: all laws absolutely continuous with respect to Lebesgue probability on [0,1] give a proper TV-closed Bayes-stable face containing a full-topological-support law but no Dirac law.

This is a classification of feasible *probability classes*, conditional on that being the declared mathematical model. It does not turn an action constraint into a zero-probability event. The source's distinctions between measure existence, computable presentation, singleton mass, actual evidence operations, and relevant outputs remain intact.

A second precise transport boundary: finite positive likelihoods are invertible within their admitted class. Infinite-space bounded strictly positive likelihoods need not have bounded inverses and need not map even the full probability simplex onto itself. Bounded-above-and-away-from-zero likelihoods do form an invertible class.

## 2. Definitions and exact quantifiers

Let (X, Sigma) be any measurable space and P(X,Sigma) its countably additive probability measures. No topology on X, measurable-singleton assumption, completion, regular conditional probability, or effective presentation is required in Sections 2–4.

For measurable L:X -> [0,infinity] and p in P, define

    Z_L(p) = integral L dp,
    B_L(p)(A) = integral_A L dp / Z_L(p),

only if 0 < Z_L(p) < infinity. All claims involving such a likelihood refer only to its defined updates. A null or infinite normalizer has no posterior under this definition.

Let G be the measurable functions L for which there are constants 0 < m_L <= M_L < infinity satisfying m_L <= L(x) <= M_L for every x. The constants may depend on L; there is no common fixed likelihood-ratio budget. Let H be all bounded, everywhere strictly positive measurable likelihoods. Then G is a subset of H. Both have defined updates at every p.

Use

    d_TV(p,q) = sup_{A in Sigma} |p(A)-q(A)|.

For p and q dominated by a common measure this is half the L1 distance of their densities. A set C is a face of P if it is convex and, whenever p=tq+(1-t)r belongs to C with q,r in P and 0<t<1, both q and r belong to C.

“Preserved” means B_L(C) is a subset of C, not a priori equality. Universal preservation quantifies over every p in C and every likelihood in the named class. It says nothing about what likelihoods a particular fixed evidence mechanism can actually supply or what observations are authorized.

## 3. The total-variation theorem

**Theorem 1.** Let C be a nonempty convex TV-closed subset of P. The following are equivalent:

(a) B_L(p) belongs to C for every p in C and every L in G.
(b) C is a face of P.
(c) For every p in C and q in P, q << p implies q in C.
(d) Every defined update by every nonnegative measurable p-integrable likelihood preserves C.

Consequently the same classification results if G in (a) is replaced by H, or by all bounded nonnegative measurable likelihoods with positive normalizer.

### Proof of (a) implies (b)

Suppose p=tq+(1-t)r belongs to C with 0<t<1. Then q << p and its Radon–Nikodym derivative f=dq/dp satisfies 0<=f<=1/t p-almost everywhere. The Radon–Nikodym theorem applies because both measures are finite. Choose a bounded measurable version taking values in [0,1/t] everywhere: replace f on its measurable exceptional null set as necessary. This needs no completion of Sigma.

For epsilon>0 set L_epsilon=f+epsilon. This lies in G and

    B_(L_epsilon)(p) = (q + epsilon p)/(1+epsilon).

Its TV distance from q is exactly

    epsilon/(1+epsilon) d_TV(p,q) <= epsilon/(1+epsilon).

Thus q belongs to C by TV closure. The identical argument with dr/dp<=1/(1-t) gives r in C. Convexity was assumed, so C is a face. This proves the full face condition, not merely the midpoint case.

### Proof of (b) implies (c)

Fix p in C and q << p, with density f=dq/dp and integral f dp=1. For integers n>=1 put

    f_n = min(f,n),  a_n = integral f_n dp,
    q_n = (f_n/a_n) p.

Every a_n is positive and a_n increases to 1. Each q_n has bounded density relative to p. Choose t_n=a_n/(2n), which lies in (0,1). Then

    p = t_n q_n + (1-t_n) r_n,
    r_n = (p-t_n q_n)/(1-t_n)

is a convex decomposition into probabilities, since t_n f_n/a_n<=1/2. The face property gives q_n in C. Moreover,

    integral |f_n/a_n-f| dp
      <= integral |f_n/a_n-f_n| dp + integral (f-f_n) dp
      = 2(1-a_n) -> 0.

Hence d_TV(q_n,q)<=1-a_n ->0, and TV closure gives q in C.

### Remaining implications and reverse check

Every defined B_L(p) is absolutely continuous with respect to p, so (c) implies (d). Clearly (d) implies (a). For an independent direct check of the bounded-likelihood reverse direction, if L<=M and Z=Z_L(p)>0, then q=B_L(p) satisfies q<= (M/Z)p. Taking t=Z/(2M) realizes p=tq+(1-t)r with r a probability; any face containing p therefore contains q. No closure is needed for this bounded reverse direction. QED.

The role of closure is real. On a two-point space, the probabilities assigning positive mass to both points form a convex positive-likelihood-stable class that is not a face. Convexity is also real: the two Dirac laws form a closed stable set that is not convex. These are already finite obstructions, not additional discoveries here.

### Principal closed face generated by a prior

For a fixed p, let D(p)={q:q<<p}. This is TV closed: if q_n<<p and q_n tends to q in TV, then for every p-null measurable A,

    q(A) <= d_TV(q,q_n) ->0.

It is convex, and the null-set test on a strict mixture proves it is a face. Theorem 1 shows that D(p) is the smallest TV-closed face containing p and the smallest TV-closed convex universally preserved class containing p.

More exactly, the G-orbit of p consists of q with density dq/dp bounded above and bounded away from zero, up to p-null modifications. Its TV closure is D(p). To see density explicitly, take q<<p and use the strictly positive bounded densities proportional to min(dq/dp,n)+1/n. The L1 estimate above and normalization give convergence to q.

The individual G-orbit can be smaller than the whole mutual-absolute-continuity class. The finite statement “same support implies one positive update reaches the other law” silently uses the boundedness of ratios on a finite nonzero support. That boundedness is absent in general.

## 4. TV faces are not generally point-support restrictions

Take X=[0,1], Sigma its Borel sets, and mu Lebesgue probability. Put C=D(mu).

- C is nonempty, convex and TV closed, as just proved.
- C is a face and is preserved by every defined likelihood update from any p in C, because B_L(p)<<p<<mu.
- mu has full topological support [0,1].
- Every singleton has mu-mass zero, so no delta_x belongs to C.

Therefore C is not P(F)={q:q(F)=1} for any nonempty Borel F: such a class contains delta_x for every x in F. In particular it is not described by one closed topological carrier. It is a null-set/absolute-continuity restriction, not merely a restriction of the available points.

It is not weakly closed. The law with density n 1_[0,1/n] relative to mu belongs to C and tends weakly to delta_0: for any bounded continuous h,

    |integral h dq_n-h(0)|
      <= sup_{0<=x<=1/n}|h(x)-h(0)| ->0.

Its TV distance from delta_0 is exactly one, witnessed by {0}. The weak concentration construction and the distinction between singleton mass and topological support are inherited facts; their application here is to an exact stable-class classification.

## 5. Weak closure on a Polish space

Let X now be Polish, Sigma=B(X), and let weak convergence mean convergence of integrals against every bounded continuous real function on X. Closure is taken in P(X), not in a larger space containing subprobabilities or mass at infinity.

For a nonempty closed F subset of X, write

    P(F) = {p in P(X):p(F)=1}.

This means carried by F; it does not mean that every member has topological support exactly F or positive mass at each point of F.

**Theorem 2.** A nonempty weakly closed convex C subset of P(X) is preserved by every L in G if and only if C=P(F) for a unique nonempty closed F subset of X. The same equivalence holds with G replaced by H, or by all defined nonnegative integrable likelihoods.

### Proof: stable C determines a closed set of allowed Dirac laws

Weakly closed sets are TV closed, because TV convergence implies convergence against all bounded continuous functions. Theorem 1 therefore makes C a face and downward closed under absolute continuity.

Set

    F={x in X:delta_x belongs to C}.

The Dirac map x -> delta_x is continuous for the weak topology: evaluating it at any bounded continuous h gives h(x). Thus F is closed.

For any p in C, define its topological support as the set of x for which every open neighborhood has positive p-mass. The complement is open. A countable base writes that complement as a countable union of p-null basic open sets. Consequently the support is measurable, closed, and has p-mass one. In particular it is nonempty. This is where countability of the topology matters; no such support assertion is being made on an arbitrary measurable space.

Fix x in supp(p) and a compatible metric d. Every B(x,1/n) has positive p-mass. Define the ordinary positive-event restriction

    r_n(A)=p(A intersect B(x,1/n))/p(B(x,1/n)).

Then r_n<<p, so r_n is in C. No conditioning on a null singleton or disintegration is being used. For every bounded continuous h,

    |integral h dr_n-h(x)|
      <= sup_{y in B(x,1/n)}|h(y)-h(x)| ->0

by continuity at x. Hence r_n tends weakly to delta_x, and delta_x belongs to C. Thus supp(p) is contained in F and p(F)=1. We have proved C subset P(F), and F is nonempty.

### Proof: all laws on F belong to C

Every delta_x with x in F belongs to C by definition, so all finite mixtures of those Dirac laws belong to C by convexity. Here is a complete density argument without assuming X or P(X) compact.

Choose a countable dense sequence (x_j) in F. For each n, disjointify the relative-open cover F intersect B(x_j,1/n) into Borel cells A_(n,j), and set s_n(x)=x_j on A_(n,j). This is a Borel measurable map on F with d(s_n(x),x)<1/n.

For any nu in P(F), the pushforward nu_n=(s_n)_*nu is countably supported on the x_j. Its finite truncations

    nu_(n,k)=sum_(j<=k) nu(A_(n,j)) delta_(x_j)
              + (sum_(j>k) nu(A_(n,j))) delta_(x_1)

belong to C. Their TV distance from nu_n is at most the tail mass, which tends to zero. Weak closure therefore gives nu_n in C. Finally h(s_n(x)) tends to h(x) pointwise for every bounded continuous h, and bounded convergence yields nu_n => nu. Weak closure gives nu in C. This proves P(F) subset C.

### Converse, closedness, and uniqueness

P(F) is convex and a face by evaluating a strict mixture on X\F. It is preserved by every defined likelihood update because those updates are absolutely continuous with respect to the prior. It is weakly closed: phi(x)=min(1,d(x,F)) is bounded continuous, nonnegative, and zero exactly on F, and

    P(F)={p:integral phi dp=0}.

Finally delta_x belongs to P(F) exactly when x belongs to F, so F is uniquely determined. QED.

No Krein–Milman compactness argument is used; P(X) need not be compact. The proof actually requires only a separable metric Borel space, but the declared theorem retains the requested Polish hypotheses. No extra generalization is needed for the present transport.

**Corollary.** The smallest weakly closed convex universally preserved class containing one prior p is P(supp(p)). Thus a full-topological-support prior forces the entire P(X) under weak closure, whereas its TV-closed generated class is only D(p). This is the exact boundary between topological carrier constraints and absolute-continuity constraints.

## 6. Which finite properties transport, and which do not

### Invertibility requires the likelihood class to be closed under reciprocals

For L,M in G, multiplication and reciprocals stay in G and

    B_L B_M = B_(LM),  B_1=id,  (B_L)^(-1)=B_(1/L).

Therefore universal G-preservation implies B_L(C)=C for every L in G. With all defined integrable likelihoods the composition formula remains valid where its normalizers are finite and nonzero; it does not establish a globally defined group.

For a concrete failure with H, let X=(0,1] and L(x)=x. This L is bounded and strictly positive but not bounded away from zero. Let u be uniform probability. If B_L(p)=u for a probability p, then x p(dx)=Z u(dx) with Z>0. Since x>0 everywhere, measure integration gives

    1=integral 1 dp=Z integral_(0,1] (1/x) du=infinity,

a contradiction. Thus B_L(P(X)) is a proper subset of P(X), although the whole simplex is of course preserved. The inverse update exists on the image, but not at u. This counterexample does not affect either theorem: G already suffices for their forward direction, and absolute continuity gives the stronger invariance conclusions.

### Exact scope of the stable-class result

- The universal likelihood quantifier is essential. A restricted declared likelihood family can preserve other convex constraints; the concurrent finite result supplies exact examples and its separate affine test. Theorems 1–2 do not classify such restricted families.
- Neither theorem transports the finite row-rank or component-graph algorithm, finite storage, computable law reconstruction, finite-sample identification, or the finite-dimensional optimization claims.
- The classification is about preserving actual probability laws in a declared class. A coarser record still needs the inherited update/output congruence condition to support a descended update.
- Restricting the ambient state space, for example to laws with prescribed finite moments, changes the ambient face question. Theorem 1 uses the full countably additive P(X,Sigma). A face relative to a smaller ambient convex class is not silently a face of P.
- In the moment packet, allowed half-line exponential tilts are one-sided and preserve all polynomial moments' finiteness. Their restricted action is not the universal likelihood action used here. The equal-moment/different-continuation countermodel and its positive compact-law theorem remain unchanged.
- This supplies no normative authority, source validation, cognition theorem, psychological mechanism, or metaphysical uniqueness claim.

## 7. Targeted inheritance and ancestry

### Inherited work inspected

The exact inspected local files and hashes are in INPUT_BINDINGS.json. The comparison is targeted, not an assertion of repository-wide absence or priority.

1. The source-measure preservation archive's READ_FIRST and SOURCE_DEPENDENCIES identify the earlier packet's scope and inherited inputs. Its measure result treats full moment records, compact determinacy, the noncompact lognormal countermodel, and actual finite-time continuation. These concern sufficiency of representations for particular tilts, not classification of all convex feasible law classes under universal likelihoods.
2. P02 U05_MEASURE_CORE, Sections M2-01 through M2-05, already separates singleton support, nonatomicity, arbitrary versus countable mixtures, topological support, and weak versus TV limits. In particular it already has the shrinking-uniform weak limit, full-measure support using a countable base, finite discrete approximations, and TV-closedness of singleton-free/countably supported classes. Those facts are retained and reused, not rediscovered.
3. P03 U05_MEASURE_SEMANTICS Sections 1–6 retain the actual-measure/abstract-predicate and formalisation boundaries. This result does not supply their missing kernel proofs or erase those warnings.
4. The concurrent finite RESULT.md, Section 2, classifies universal-positive stable closed convex finite classes as coordinate faces. The present contribution is its exact measure transport and topology/reciprocal boundary. It is separate from that packet's affine likelihood classification and projection calculations.

### Primary mathematical ancestry, with bounded source claims

- Stephan Weis, *A note on faces of convex sets*, arXiv:2404.00832v2 (3 August 2024), Section 9: Theorem 9.1 identifies the face generated by a probability through bounded density domination; Corollary 9.2 states that D(mu) is a face; Corollary 9.3 describes the bounded two-sided density class. Section 11, Lemma 11.5 identifies norm-closed faces of the countable simplex with coordinate subsets. These directly antecede the present Bayes formulation. [Author text](https://arxiv.org/html/2404.00832v2#S9).
- Weis's Section 4 attributes the general generated-face formula to E. M. Alfsen, *Compact Convex Sets and Boundary Integrals* (1971), p.121. The present inspection was of Weis's proof and attribution, not that page of Alfsen's book. [Inspected attribution](https://arxiv.org/html/2404.00832v2#S4).
- The published article is *Journal of Convex Analysis* 32 (2025), No.3, 901–919; publication metadata were checked on the [journal page](https://journalofconvexanalysis.com/articles/jca32046/). No assertion that this is the earliest occurrence of every measure fact is made.
- Onno van Gaans, *Probability measures on metric spaces*, author-hosted notes: Sections 2–4 give metric-space probability regularity, Polish tightness, weak convergence, and finite-discrete density. The notes themselves identify Parthasarathy and Billingsley as antecedents. [Author-hosted text](https://pub.math.leidenuniv.nl/~gaansowvan/jancol1.pdf). Our weak theorem is supplied with an elementary proof above; it is not presented as an exact named theorem located in these notes or as novel Choquet theory.

The proofs here independently check the normalization, Radon–Nikodym versions, TV approximation, support measurability, conditioning denominators, and finite-mixture limit needed for this precise interface. Classical probability/convexity machinery and inherited limits own the underlying facts. The meaningful increment is a bounded, explicit transport application; no new measure-theory campaign follows.

## 8. Verification status

These are ordinary universal proofs, not numerical experiments or a kernel-checked certificate. No finite numerical census is offered as evidence of the infinite-space classification. INPUT_BINDINGS.json records read-only inputs; SOURCE_LEDGER.json records inspected external statements and limitations; VERIFICATION.md checks proof obligations; MANIFEST.json binds the completed scratch deliverables. No imported source or concurrent finite-author file was edited.
