# Exact passive updates of proper interaction-moment hierarchies

10 October 2026 UTC. Separate scratch research packet. Complete ordinary proofs and small exact rational controls; no protected-source edit, integration, formal-kernel claim, empirical or actual-warrant claim, or programme closure. The root supplied the proper-grade multiplier theorem, positive-likelihood normalized extension, moment-cone corollary, and finite-product interaction extension. The worker checked inheritance, proved the nonnegative support-rank sharpening, and assembled the proofs, boundaries, and controls. This is joint author verification, not independent review.

## 1. Result and scope first

On the full law simplex over m binary slots, retain every moment of degree at most k, where 1 <= k < m. A passive likelihood can update this same record exactly for every prior, including its branch probability, **if and only if it is constant**. The decoder need not have been assumed linear. The obstruction already concerns one observation, not a long experiment or an approximation limit.

For strictly positive likelihoods, even asking only for the retained posterior record gives the same conclusion, with arbitrary nonlinear decoders. With zero likelihoods permitted there is one precise escape: a likelihood supported at a single latent state has a constant revealing posterior on every possible branch. Its branch probability is not recoverable from the proper moments; on the full simplex its feasibility is not recoverable either. Thus the posterior-only and probability-plus-posterior contracts must stay distinct.

The same obstruction extends to arbitrary finite product alphabets, with order counting distinct interacting slots. The associated moment-image cone has only scalar linear maps in the positive interval between zero and the identity, and hence is indecomposable. At full order k=m it becomes a linear image of the full orthant, with one one-dimensional component per product atom (2^m in the binary case). This is a short exact algebraic/geometric consequence, not a physical quantum, cognition, epistemic, or efficiency result.

## 2. Inheritance checked before claiming an addition

The inspected inputs and their byte hashes are in INPUT_BINDINGS.json. These are targeted source reads, not whole-project priority certification.

- The inherited graded-interface manuscript, Theorem 4.2, already owns the elementary fibre factorization criterion. Theorem 5.1 and Corollary 5.2 already give opposite-parity proper-marginal collisions and their tensor contraction representation. Its tensor algebra separates semantic slots and expressly refuses automatic identification of workflow composition with tensor multiplication.
- H-ICS v5, the observation-congruence theorem, already relates fibre preservation, descended operations, and a kernel criterion for deterministic finite observations. Its hypotheses are not silently converted into a Bayesian theorem.
- H-Continuation Theorem 2 already owns the finite-instrument invariant observable space, arbitrary-decoder sufficiency for branch probabilities and terminal numerators, exact intertwining, and normalization only on positive branches. Its Theorem 3 computes the increasing Walsh hierarchy for specified pairwise state-changing actions. Those actions are different from the passive diagonal updates here.
- The tensor-moment continuation RESULT, especially §§3 and 7, already owns the symmetric-moment evolution under controlled exponential tilts and the first-grade all-directions affine-independence criterion. The present finite binary-slot cutoff is a different declared representation and a single-likelihood classification, not a new generic moment-closure method.
- The audit-continuation RESULT, §§3 and 5–6, already owns the moment-image cone, exact predictive intertwining, the distinction between posterior-only and probability-plus-posterior equivalence, and separate feasibility handling. Its paired tensor test concerns equality of future outputs between two laws. The result below instead asks whether a fixed one-law moment summary supports an exact same-summary update for every prior.

- The concurrent cone-transport RESULT, §§2–4 and 7.2, identifies the established proper-cone identity-interval/indecomposability theorem and the constrained-prior cone countercontrol. The exposed-column lift below is additional application-specific structure; the general cone theorem is not new here.

The inspected inherited passages do not state the proper interaction-space stabilizing algebra, the normalized support-rank dichotomy, or the resulting truncated/full cone transition. These are the bounded new-to-this-packet deductions. They specialize established Fourier analysis, linear factorization, and stabilizing-algebra machinery; no field-wide novelty is asserted.

## 3. Conventions and the inherited descent criterion

Let X be a finite set of n states. Laws p are nonnegative column vectors with u p=1, where u=(1,...,1). Let V be a real observable space containing 1. Choose a full-row-rank evaluation matrix M whose rows form a basis of V and whose first row is u. The retained record is z=M p; the first coordinate records mass.

A nonnegative likelihood L is a vector on X; D_L is its diagonal matrix. Write

    alpha_L(p) = u D_L p = L^T p,
    B_L(p) = D_L p / alpha_L(p), only when alpha_L(p)>0.

For one outcome of an actual passive channel, 0<=L<=1; all its outcome likelihoods sum pointwise to 1. Multiplying a nonzero likelihood by a positive constant changes alpha but not B. No target state is mutated by D_L.

**Proposition 1 (inherited mechanism, specialized).** The following are equivalent:

1. Some arbitrary function of M p determines M D_L p for every law p.
2. ker M is contained in ker(M D_L).
3. A linear T exists with M D_L=T M.
4. L V is contained in V under pointwise multiplication.

When these hold, branch probability and the retained normalized posterior are determined, with an explicit impossible-branch status when alpha=0. Conversely, branch probability together with the retained posterior on every possible branch determines M D_L p and implies all four conditions.

**Proof.** If d is in ker M, then u d=0. From any strictly positive p, both p and p+epsilon d are laws for sufficiently small nonzero epsilon. Condition 1 therefore gives M D_L d=0. Thus 1 implies 2. Under 2, define T(M v)=M D_L v for v in R^n; this is well-defined and linear, and gives 3. The rows of M D_L are the retained observables multiplied by L, so 3 and 4 are equivalent. Condition 3 supplies condition 1 directly.

The mass row reads alpha from M D_L p. Divide the whole vector by alpha on a positive branch. At alpha=0, nonnegativity implies D_L p=0. Conversely multiply the retained posterior by the supplied positive alpha, and return zero on impossible branches. This reconstructs every M D_L p. QED.

This proposition is recorded to make the contract exact. It is not offered as a new general descent theorem.

## 4. Proper Walsh grades have only constant likelihood multipliers

Now let X={-1,+1}^m, m>=2. For S subset of [m], put chi_S(x)=product_(i in S) x_i, including chi_empty=1. The characters form an orthonormal basis under uniform expectation, and chi_S chi_T=chi_(S symmetric-difference T). Let

    V_k = span{chi_S: |S|<=k},       1<=k<m,
    (M_k p)_S = E_p[chi_S],         |S|<=k.

This record is equivalent to all marginal laws on at most k slots: on a subset J, the mass at a sign vector a is

    2^(-|J|) sum_(S subset J) chi_S(a) E_p[chi_S].

The slots are labeled. Products here are products of functions; they are not workflow composition, and this notation does not identify distinct semantic roles.

**Theorem 2 (constant stabilizing algebra).** For every real function L on X,

    L V_k subset V_k  iff  L is constant.

Consequently the full probability-plus-retained-posterior contract of Proposition 1 permits no informative passive likelihood on this fixed proper hierarchy.

**Proof.** Constants plainly work. Conversely, 1 belongs to V_k, so L=L·1 belongs to V_k. Expand L=sum_(|S|<=k) a_S chi_S. Suppose a_S is nonzero for a nonempty S. Set s=|S|. Since 1<=s<=k<m, there are at least k-s+1 elements outside S. Choose T outside S with |T|=k-s+1. Then 1<=|T|<=k but |S union T|=k+1.

The coefficient of chi_(S union T) in L chi_T is exactly a_S. Indeed multiplication by chi_T sends a character index R to R symmetric-difference T, a bijection, so no other coefficient can cancel it. This gives a nonzero coefficient above degree k, contradicting L chi_T in V_k. Thus every nonconstant coefficient vanishes. QED.

This proof also handles k=0 for the unnormalized contract, but the normalized-only conclusions below need k>=1.

### Explicit interior witnesses, not only an existence argument

For any nonconstant L, a failure of the full contract can be exhibited with positive laws.

If a Walsh coefficient a_U of L is nonzero with |U|>k, take

    p_+(x)=2^(-m)(1+epsilon chi_U(x)),
    p_-(x)=2^(-m)(1-epsilon chi_U(x)),       0<epsilon<1.

They have the same retained moments but branch probabilities differing by 2 epsilon a_U.

Otherwise L belongs to V_k and has some nonzero a_S for nonempty S. Choose T as in the proof and U=S union T. The same p_+,p_- have equal retained moments and equal branch probabilities, because a_U=0. Their chi_T branch numerators differ by 2 epsilon a_S. If L>=0 is nonzero, their common branch probability is positive, so their retained posterior records differ. This provides the exact missing-interaction witness even when every next-branch probability has been retained.

For example, m=2,k=1, L(x)=(1+x_1/2)/2 and p_±(x)=(1±x_1x_2/2)/4 give the same initial two means and the same branch probability 1/2. Their posterior means are (1/2,1/4) and (1/2,-1/4). The latent correlation is required to update the other retained unary mean.

### Finite categorical slots: the same proper-interaction theorem

Let X=product_(i=1)^m X_i, with each finite |X_i|>=2. Give each X_i uniform probability, and write

    R^(X_i)=span{1_i} direct-sum H_i,
    H_i={f: uniform mean(f)=0}.

The evaluation map sending a pure tensor f_1 tensor ... tensor f_m to the function x -> product_i f_i(x_i) identifies the finite tensor product with R^X. It yields the orthogonal direct sum

    R^X = direct-sum_(S subset [m]) H_S,
    H_S=(tensor_(i in S) H_i) tensor (tensor_(i not in S) span{1_i}).

Define V_k as the sum of H_S with |S|<=k. This is exactly the span of functions depending on at most k slots, hence exactly the observable content of all marginals of order at most k. It is **interaction order across distinct slots**. It is not automatically polynomial total degree, a symmetric-power degree, or the free graded semantic tensor degree of the inherited manuscript.

**Theorem 2C.** For 1<=k<m, L V_k subset V_k implies L is constant; the converse also holds.

**Proof.** Since 1 belongs to V_k, decompose L=sum_(|U|<=k) L_U. If L is nonconstant, choose a nonzero component L_S of maximal degree d=|S|>=1. Choose T disjoint from S with |T|=k-d+1, and choose a nonzero product h_T of zero-mean functions on its slots. Such choices exist because k<m, d>=1, and each H_i is nonzero. Then h_T belongs to V_k and |S union T|=k+1.

Project L h_T onto H_(S union T). Outside T, multiplication by h_T changes no factor. Therefore a component L_U can contribute only if U outside T equals S. Such a U contains S; by maximality its degree is at most d, so U=S. The surviving projection is exactly L_S tensor h_T under the disjoint-slot evaluation identification. It is nonzero, since tensoring a nonzero vector with a nonzero vector over R is nonzero. Thus L h_T has a component of degree k+1, a contradiction. QED.

Overlapping categorical factors can multiply into constant and nonconstant parts. The proof does not assume a Walsh symmetric-difference rule there: it uses disjoint T and the maximal-degree component to exclude all competing contributions. Theorem 2 is the binary specialization with one-dimensional H_i.

## 5. Normalized-only descent, including all zero-likelihood exceptions

For this section an arbitrary finite M with mass row is allowed. Write c_i=M e_i for its columns. A posterior-only decoder means a function F on the retained records of priors with alpha_L(p)>0 such that

    M B_L(p) = F(M p).

No branch probability or feasibility output is silently included in this definition.

**Theorem 3 (support-rank dichotomy).** Let L>=0 be nonzero. Such a posterior-only decoder on the whole simplex exists if and only if at least one of the following holds:

(a) M D_L=T M for a linear T;

(b) all columns c_i with L_i>0 are equal.

The same equivalence holds if the required priors are only the full-support laws. Condition (b) is equivalent to rank(M restricted to supp L)=1, since the common mass coordinate is 1.

**Proof.** Either (a) or (b) supplies a decoder. Under (a), use the mass row of Tz as denominator. Under (b), every possible posterior is supported among columns with one common value c, so its retained record equals c.

For necessity, assume a decoder exists. Fix d in ker M, and put

    b=L^T d,       a=M D_L d,       q(p)=M B_L(p).

For every full-support p, its branch is positive. For sufficiently small nonzero epsilon, p+epsilon d is another full-support law with the same retained record. Cross-multiplying equality of its posterior record with q(p) gives

    a=b q(p).                                                  (1)

If some d has b nonzero, (1) forces q(p) to be one constant vector for every full-support p. For any i with L_i>0, let full-support p tend to e_i. The denominator tends to L_i>0 and q(p) tends to c_i. Thus all these columns coincide, giving (b).

If (b) fails, no d in ker M can have b nonzero. Equation (1) then gives a=0 for every d in ker M. Proposition 1 gives (a). This argument used only full-support priors, so establishes that version too. QED.

**Corollary 3.1.** If L>0 and rank M>1, posterior-only descent already implies linear unnormalized descent. Strict positivity puts every column in supp L, while rank M>1 prevents (b). No continuity, linearity, or differentiability of F is assumed.

**Corollary 3.2 (complete product-marginal classification).** For either the binary or finite-categorical V_k, with 1<=k<m and L>=0 nonzero, posterior-only descent through a basis evaluation matrix M_k holds exactly when L is a positive constant or supp L is a singleton.

**Proof.** The first-slot observables distinguish every pair of product atoms, so distinct columns of M_k are distinct. Thus Theorem 3(b) means singleton support, and Theorem 2 or 2C reduces case (a) to constants. QED.

The zero likelihood L=0 has no possible branches and no defined normalized update. Its posterior-only assertion is vacuous. It does satisfy unnormalized descent as the zero map. It is never an informative counterexample.

### What feasibility adds, and why the domain matters

Fix a singleton-supported likelihood L=lambda 1_{x0}, lambda>0. Its possible-branch posterior is always e_{x0}, but alpha=lambda p(x0) is not recoverable from proper moments. For the boundary-sensitive control let eta=chi_`[m](x0)` and use

    p_±(x)=2^(-m)(1±eta chi_[m](x)).

Both laws have all proper nonconstant moments zero. Yet p_+(x0)=2^(1-m)>0 and p_-(x0)=0. Their feasibility statuses differ. Thus on the full simplex, posterior record **plus feasibility** also allows only nonzero constant L (with L=0 as the always-impossible branch).

If the domain consists only of full-support priors, every nonzero nonnegative likelihood is always feasible. The feasibility guard then cannot remove singleton support. Its probability remains unrecoverable: replacing the preceding ±1 coefficient by ±1/2 gives two full-support laws with the same proper moments but different p(x0).

For categorical alphabets the same feasibility boundary is obtained by choosing two values per slot, including x0_i, and embedding the preceding binary parity pair on that two-value product subdomain. Equality of all proper marginals there remains equality on the whole categorical product. On a full-support categorical domain, put h_i(a)=1_{a=x0_i}-1/|X_i| and h(x)=product_i h_i(x_i). Then h has zero sum along every slot, h(x0) is nonzero, and p_±(x)=1/|X|±epsilon h(x) are positive laws for sufficiently small epsilon>0. They have identical proper marginals but different p(x0). Thus branch probabilities remain unrecoverable.

For a complete finite channel, posterior-only descent for every outcome therefore means that each nonzero likelihood row is constant or singleton-supported. Column normalization further makes the total singleton-supported probability at each state equal to 1 minus the sum of constant-row probabilities. This is an erasure-or-revelation form: constant rows leave the law unchanged; singleton rows reveal its state. Outcome probabilities still need not descend. This is only a corollary, not a new experiment-design claim.

## 6. The moment-image cone and the truncated/full transition

Let r=sum_(j=0)^k binomial(m,j) and

    K_k=M_k R_+^(2^m) = cone{c_x:x in X},      c_x=M_k e_x.

This is the admissible cone of unnormalized moment records, not a constrained prior family inside the original simplex. Its normalized base is Z_k=M_k Delta(X). K_k spans R^r because the Walsh rows are independent. It is pointed: its mass coordinate is nonnegative, and zero mass forces any representing nonnegative law vector to be zero. As a finitely generated cone it is closed.

A linear T is K_k-positive when T(K_k) is contained in K_k. Write 0<=T<=I when both T and I-T are K_k-positive. This is cone order, not entrywise order in the Walsh coordinates.

**Proposition 4 (every latent column is exposed).** For k>=1, each ray R_+ c_x is exposed and hence extreme in K_k.

**Proof.** The functional

    ell_x(z)=m z_empty - sum_i x_i z_{i}

is nonnegative on every generator c_y, since ell_x(c_y)=m-sum_i x_i y_i, twice the Hamming distance from x to y. It vanishes exactly when y=x. Consequently its zero face on K_k is exactly R_+ c_x. QED.

**Theorem 4 (scalar positive interval).** For 1<=k<m,

    {T linear : 0<=T<=I on K_k} = {c I:0<=c<=1}.

In particular K_k is indecomposable as a direct sum of two nonzero cones in complementary linear spans.

**Proof.** If 0<=T<=I, write c_x=T c_x+(I-T)c_x. Both summands lie in K_k; extremality forces T c_x=L_x c_x for a scalar L_x in [0,1]. Hence

    T M_k=M_k D_L.                                            (2)

Theorem 2 makes L constant, and because the columns span R^r, (2) gives T=cI. Conversely scalar maps with 0<=c<=1 plainly belong to the interval.

A nontrivial direct sum K_k=K_1 direct-sum K_2 would have a linear projection P onto the first summand with P and I-P both positive. Such a projection is neither zero nor identity. But a scalar idempotent is only zero or identity, a contradiction. QED.

Every finite positive linear instrument T_y on K_k with sum_y T_y=I therefore consists of scalar branches c_y I. Its normalized state is unchanged on each positive branch and its outcome probabilities are constants c_y. The identity-sum premise is essential.

At k=m the full Walsh matrix is invertible, with inverse 2^(-m) M_m^T. Therefore K_m is linearly isomorphic to R_+^(2^m), and all likelihoods descend by T=M_m D_L M_m^(-1). Every extreme ray is now a separate direct-sum component. This is the exact proper/full transition; it is not a continuity or complexity estimate.

For categorical products, the same cone proof uses ell_x(z)=sum_i (mass(z)-E_z[1_{X_i=x_i}]). It is nonnegative on all product-atom columns and zero only at x. Theorem 2C then gives the scalar interval and indecomposability for every proper k>=1. At k=m the full product evaluation basis is invertible and the cone is an orthant image, with product_i |X_i| ray components.

### Why an intrinsic positive map needs a faithful ambient lift

In general a positive identity-summing instrument on a cone does not automatically represent passive observation of a specified ambient hidden state. Here equation (2) is proved because **every given latent generator is extreme**, and is exactly the lift required by the original observation class.

For comparison, C={p in Delta_3:p_1=1/2} is a segment with endpoints v=(1/2,1/2,0) and w=(1/2,0,1/2). Its intrinsic cone has positive component projections onto v and w. But a diagonal D_L preserving that cone must satisfy L_1=L_2 on v and L_1=L_3 on w, hence L is constant. An intrinsic projection is therefore not an informative ambient passive branch. The cones and generating maps are different. This short countercontrol was communicated by the cone-transport worker and is derived here explicitly; it supplies no quantum conclusion.

## 7. Negative boundaries and positive countercontrols

**All priors versus structured priors.** For independent binary-slot priors the first moments determine the entire law. Under L=(1+a x_1)/2, |a|<1, independence is preserved and the means update as mu_1'=(mu_1+a)/(1+a mu_1), mu_i'=mu_i for i>1. This restricted family admits an informative exact unary filter. It is not the full simplex; silently imposing independence would erase the very correlations being tested.

**All low-grade observables versus a selected subalgebra.** On two slots, V=span(1,x_1) is closed under multiplication by every function of x_1. It supports informative observation about that selected slot. This is not V_1=span(1,x_1,x_2), and it does not promise the other retained unary posterior. A target-specific statistic can work while the all-proper-grade hierarchy cannot.

**Passive evidence versus state change.** Let an outcome have likelihood L and then independently reset the new state to fixed r. Its matrix is A=r L^T, so M A=(M r)L^T. If L belongs to V, the update descends and is generally informative about the old state. Complete reset instruments sum to r u, not I. They are not D_L updates of an unchanged target. A smaller or changing output contract is likewise a different question.

**One-step failure does not imply full-law recovery is the only repair.** The least invariant enlargement under a given channel is already supplied by inherited H-Continuation. A nonconstant L forces an enlargement beyond V_k, but it need not force all 2^m observables. For m=3,k=1 and L depending only on x_1, the closure is span(1,x_1,x_2,x_3,x_1x_2,x_1x_3), of dimension six, not eight. This preserves the declared channel and unary output, without claiming every future observation is available.

**Observation identity and permissions.** D_L denotes the declared conditional likelihood for the actual branch. A reread of an already known receipt is not automatically another fresh use of L. Extra observations, permission changes, source audits, target changes, and changed model versions need their own contract. The theorem supplies none of those premises.

**Exactness and interpretation.** No lower bound for approximate filtering, restricted reachable families, sampling, bits, finite precision, empirical memory, psychological architecture, truth, actual warrant, or noetic restoration is proved. A moment cone is a numerical representation domain. Its indecomposability is not an ontological finding.

## 8. Primary ancestry and bounded literature check

[O'Donnell, Analysis of Boolean Functions, §1.3, Theorem 1.5 and Fact 1.6](https://www.cs.cmu.edu/~odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf) supplies the standard orthonormal character basis and symmetric-difference product. The present coefficient argument is a short specialization of these identities.

[Randriambololona, On products and powers of linear codes under componentwise multiplication, Definition 2.6 and Proposition 2.11](https://arxiv.org/pdf/1312.0022) develops exactly the stabilizing algebra {a:a C subset C} and its connection to disjoint-support components. The opening conventions allow arbitrary fields for these sections, including R. This is direct ancestry for the algebra being computed, not evidence that the paper states this particular Bayesian or Walsh-cutoff application. Its decomposition of observable codes is not silently identified with the positive moment-image cone; §6 proves that additional bridge.

These targeted sources and the inherited reports were inspected. No exhaustive priority search was performed. The normalized support-rank lemma is proved here as elementary finite-dimensional quotient algebra; no historical first-discovery claim is made.

## 9. Verification and use

Run python3 verify.py in this directory. The script uses standard-library exact fractions, checks the displayed controls and small rank identities, verifies all bound local input hashes, and writes CONTROL_RESULTS.json. These finite controls supplement the written general proofs and do not replace them. MANIFEST.json binds this packet. External publications are linked and read-scope recorded, not bundled or remotely revalidated by the local replay.

Use the results only with their declared law domain, likelihood support, retained-output contract, and admissible operation class. Root and worker collaboration is author-stage work. Any independent review, packaging, integration, or broader research decision remains separate.
