# Determinate initial moments still do not enforce realizable dynamics

10 October 2026 UTC. Additive ordinary research, separate from both frozen earlier packets. No field-novelty, canonical-integration, protected-edit, or formal-kernel claim.

## 1. Results

**Negative theorem.** Even a Hamburger-determinate initial Stieltjes moment sequence, together with strict coordinate positivity and a coordinatewise C∞ hierarchy solution, does not imply realizability at any positive time. Counterexamples exist on every prescribed finite horizon.

**Positive boundary.** If the initial Stieltjes moments c additionally satisfy the Stieltjes Carleman condition

    Σ_(n≥1) c_n^(−1/(2n)) = ∞,                         (C)

then coordinate nonnegativity and the hierarchy do force the unique normalized tilt of the initial law. Thus general determinacy and this sufficient growth condition must not be conflated.

The negative result uses two explicitly attributed classical facts about extremal moment measures. The positive result uses classical Carleman determinacy and an elementary mixed-Poisson reduction. Neither modifies the existing classification.

## 2. Classical facts used in the negative construction

Let μ be standard lognormal LN(0,1), with moments b_r=exp(r²/2). This Stieltjes moment sequence is indeterminate: for example, the probability proportional to Σ_(k∈Z)exp(−k²/2)δ_(exp k) has the same moments by an integer index shift and is different from μ.

For any Stieltjes-indeterminate sequence there is a **Krein representing measure** η_K which is N-extremal for its Hamburger moment problem, is supported on [0,∞), and has an atom at zero. The measure is discrete, with no finite accumulation point in its support. Hence “zero belongs to the support” here really does mean positive atomic mass, not only an accumulation point. Applied to b, put

    w = η_K({0}).

Then 0<w<1. Positivity follows from the zero atom, and w<1 follows from the nonzero first moment b_1.

The **full-atom deletion theorem** says that removing all the mass at one support point of an indeterminate N-extremal measure yields a Hamburger-determinate positive measure. Accordingly

    ρ = (η_K−wδ_0)/(1−w)                              (1)

is a Hamburger-determinate probability supported on (0,∞), with finite moments of every order. Positive scalar normalization preserves determinacy. Its moments are

    c_0=1,     c_r=exp(r²/2)/(1−w) for r≥1.            (2)

It is essential that the entire Krein atom is removed. The earlier elementary lattice representative is not asserted to be N-extremal, and subtracting only a small portion of an atom does not justify determinacy.

### Precisely inspected sources

1. Z. J. Jabłoński, I. B. Jung, and J. Stochel, *A non-hyponormal operator generating Stieltjes moment sequences*, arXiv:1110.0249v1, §2.1, pp. 5–6, especially equation (2.1.6) and the paragraph after it. These passages identify the Krein measure as N-extremal, locate its support in [0,∞), and give 0∈supp(μ_K). The preceding discussion states that N-extremal supports have no finite accumulation point. Published in Journal of Functional Analysis 262 (2012), 3946–3980, DOI 10.1016/j.jfa.2012.02.006. Inspected primary text: https://arxiv.org/pdf/1110.0249 .
2. Christian Berg and J. P. R. Christensen, *Density questions in the classical theory of moments*, Annales de l'Institut Fourier 31(3) (1981), 99–114. Theorem 7, printed p. 111, and its proof continuing on p. 112, establish full-atom deletion determinacy. The subsequent paragraph explicitly restates this consequence. Inspected original article: https://www.numdam.org/article/AIF_1981__31_3_99_0.pdf .

These classical inputs carry the determinacy claim. Section 8 below additionally derives an explicit convergent product for w; no numerical reconstruction of the full support of η_K is needed.

## 3. A strictly positive hierarchy with this determinate initial sequence

Set

    B_r(t)=∫x^r exp(−tx)dμ(x).

Define, for t≥0,

    a_0(t)=[B_0(t)−w]/(1−w),
    a_r(t)=B_r(t)/(1−w), r≥1.                         (3)

Every coordinate is C∞ up to zero in the one-sided sense, by dominated convergence and the finite moments of μ. For every r≥0,

    a_r' = −a_(r+1).

In particular the r=0 identity is correct because the subtracted zero-atom term is a constant, whose derivatives vanish. At zero a_0(0)=1 and a_r(0)=c_r.

For an explicit positive interval take

    T_0=(1−w)/(2 exp(1/2))>0.

Since exp(−tx)≥1−tx,

    B_0(t)−w ≥ 1−w−t exp(1/2) > (1−w)/2

for 0≤t<T_0. Hence a_0(t)>1/2 there. Every a_r(t), r≥1, is strictly positive because μ is carried by positive x.

Define m_r=a_r/a_0 on [0,T_0). Then all m_r are strictly positive and C∞, m_0=1, m_r(0)=c_r, and the quotient rule gives

    m_r' = −m_(r+1)+m_1m_r.                           (4)

These conclusions hold for the full infinite hierarchy; no finite-grade inference or numerical sampling is used.

## 4. No positive-time moment sequence is realizable

Fix s∈(0,T_0). Suppose a probability σ_s represented every m_r(s). The positive finite measures

    κ_s=(B_0(s)−w)σ_s+wδ_0,
    λ_s(dx)=exp(−sx)μ(dx)

then have identical moments. At r=0 they both have mass B_0(s). At every r≥1 the δ_0 term vanishes, and

    ∫x^r dκ_s=(B_0(s)−w)m_r(s)=B_r(s)=∫x^r dλ_s.

But λ_s has a positive exponential moment, for example

    ∫exp((s/2)x)dλ_s≤1.

Such a positive finite measure is determined by all its moments: monotone convergence transfers exponential integrability to any competing positive representative, equal moments identify their convergent Laplace Taylor series, analyticity propagates equality, and Laplace uniqueness identifies the measures.

Consequently κ_s=λ_s. This contradicts κ_s({0})≥w>0 and λ_s({0})=0. Thus no positive-time sequence in (4) is Stieltjes-realizable.

The scalar function in (3) is the Laplace transform of the signed measure (μ−wδ_0)/(1−w), and its initial derivative sequence is nevertheless Hamburger determinate. The unique positive initial representative is (1), not this signed measure.

This also proves nonuniqueness of the merely coordinate-positive hierarchy at a determinate initial point: the genuine tilt of ρ is another strictly positive C∞ solution with the same initial coordinates; the path (3) is not that tilt.

## 5. Finite horizons and the endpoint

B_0 is continuous and strictly decreasing from 1 to 0, since μ((0,∞))=1. Therefore there is a unique finite t_*>0 such that B_0(t_*)=w. The construction is strictly positive throughout [0,t_*), and a_0(t) tends to zero as t increases to t_*. A probability Laplace transform cannot vanish at a finite nonnegative time. This gives another obstruction to representing the entire scalar path; §4 gives the stronger pointwise moment obstruction.

For any prescribed finite H>0 choose λ>0 with λH<T_0 and replace x by λx in μ and η_K. The zero mass w is unchanged, positive scaling preserves Hamburger determinacy of (1), and

    a_0(t)=[B_0(λt)−w]/(1−w),
    a_r(t)=λ^r B_r(λt)/(1−w), r≥1

gives the same counterexample on [0,H). There is no assertion of coordinate positivity for all nonnegative times.

## 6. A sufficient condition: Stieltjes Carleman growth

Assume now a_r≥0, a_0(0)=1, a_r'=−a_(r+1), and c_r=a_r(0) is a valid Stieltjes sequence satisfying (C). These assumptions arise from the hierarchy's usual unnormalization. We show that a_0 must be the initial law's Laplace transform.

The degenerate case c_1=0 is immediate: the initial law is δ_0, and 0≤a_1(t)≤a_1(0)=0 gives a_0=1. Otherwise all c_n>0.

### 6.1 Convert a local completely monotone function into a count law

The backward Taylor inequalities give a_n(s)≤n!/s^n for every interior s>0. They also give real analyticity on the positive-time interval, as in the existing classification. Fix 0<s<T and put

    p_j=a_j(s)s^j/j!≥0.

The power series with these coefficients converges for |z|<1. By Taylor expansion near s and analytic continuation,

    a_0(s(1−z))=Σ_(j≥0)p_j z^j, 0≤z<1.

As z increases to one, monotone convergence and continuity at zero yield Σp_j=1. Thus p is the law of a nonnegative integer-valued N. Differentiating the power series and taking z↑1 gives, again by monotone convergence and boundary continuity,

    E[(N)_r]=s^r c_r, r≥0,                           (5)

where (N)_r=N(N−1)…(N−r+1).

If X has the initial law, a mixed-Poisson variable Y conditional on X, with Poisson mean sX, has the same factorial moments. Therefore N and Y have the same raw moments

    d_n=Σ_(k=0)^n S(n,k)s^k c_k,                      (6)

where S(n,k) are Stirling numbers of the second kind.

### 6.2 Transfer the Stieltjes Carleman condition

The elementary partition count bound

    S(n,k)≤binom(n,k)n^(n−k)

follows by choosing one distinguished representative in each block and assigning every remaining element to a block, an overcount. Since c_k≤c_n^(k/n) for 0≤k≤n by monotonicity of probability L^p norms, (6) implies

    d_n≤[s c_n^(1/n)+n]^n.

Let b_n=c_n^(−1/(2n)). This is a positive nonincreasing sequence. Consequently

    d_n^(−1/(2n))
      ≥ [s c_n^(1/n)+n]^(-1/2)
      ≥ (1/√2) min{b_n/√s,n^(−1/2)}.                (7)

If Σb_n diverges, so does Σmin{b_n/√s,n^(−1/2)}. One proof uses Cauchy condensation: the condensed terms are the minimum of a divergent-sum sequence 2^k b_(2^k)/√s and the cap 2^(k/2). If infinitely many terms are capped, their sum diverges because the cap tends to infinity; otherwise the minimum eventually equals the first sequence. Thus (7) establishes

    Σ_(n≥1)d_n^(−1/(2n))=∞.

The classical Stieltjes Carleman theorem now makes the count moment sequence determinate among positive measures on [0,∞). Hence N and Y have the same law.

Their probability generating functions agree, so for 0<t≤s,

    a_0(t)=E[(1−t/s)^N]=E[exp(−tX)].

Both sides are real analytic for t>0. Identity therefore propagates over (0,T), with equality at zero by continuity. Differentiation gives every a_r, and normalization yields the unique realizable hierarchy solution.

### 6.3 Attribution and limits of the positive theorem

Kuba and Panholzer's *On moment sequences and mixed Poisson distributions*, arXiv:1403.2712, Lemma 1, pp. 8–10 in the inspected author preprint, proves transfer of the **Hamburger** Carleman criterion between mixing and mixed-Poisson moments. The count/factorial-moment estimate and monotone-series comparison are established techniques; the argument above spells out the Stieltjes variant and its application to this hierarchy. Inspected source: https://www.dmg.tuwien.ac.at/kuba/preprintMomseq.pdf . The paper's Proposition 2 assumes an mgf near zero and is not imported under mere determinacy.

The only moment representation/determinacy theorem imported in §6 is the classical Stieltjes Carleman criterion. Its form is distinct from the stronger derivative-class criterion Σc_n^(−1/n)=∞. For example c_n=(2n)! satisfies (C), whereas Σc_n^(−1/n) converges. No exponential moment is required by §6.

The counterexample in §§2–5 has c_n=exp(n²/2)/(1−w) for n≥1, so its Stieltjes Carleman series converges. This is fully consistent with its determinacy and with the positive sufficient theorem.

## 7. Scope

The negative construction settles the general determinate-initial-data strengthening. It does not alter the prior theorem that coordinate positivity plus realizability at one positive time force a tilt path. The counterexample lacks that premise at every positive time.

Classical Krein theory and full-atom deletion own the non-elementary moment-theoretic inputs. The project-relative addition is their use in the hierarchy separation, together with the explicit local positivity and positive-time atom contradiction. No comprehensive literature survey or universal originality claim is made.

All arguments are ordinary proofs. No formal-kernel verification, numerical approximation of an extremal measure, universal reconstruction algorithm, protected integration, or empirical certification is claimed. The two predecessor RESULT.md files remain unchanged.


## 8. Explicit zero-atom mass and effective initial coordinates

This refinement was derived independently in participating root work; it is not an independent review of the proof above. Put q=exp(−1), so b_n=q^(−n²/2). Then

    w=∏_(j≥1)(1−q^j).                                (8)

Here is a complete derivation from the same N-extremality input. Write H_N=(b_(i+j))_(i,j=0)^N. The least value of ∫p² dη_K among real polynomials of degree at most N with p(0)=1 is the Schur complement

    w_N=det(H_N)/det((b_(i+j))_(i,j=1)^N).

Equivalently w_N=1/Σ_(j=0)^N P_j(0)² for the orthonormal polynomials P_j. Because η_K is N-extremal, these polynomials form a complete orthonormal basis of L²(η_K). Evaluation at its atom zero extends to the bounded coordinate functional f↦f(0), whose squared norm is 1/w. Parseval therefore gives Σ_(j≥0)P_j(0)²=1/w, so w_N↓w. The same atom/kernel identity is stated in the proof of Berg–Christensen Theorem 3, printed p. 106: the atom mass times the diagonal reproducing kernel equals one.

The determinant ratio is explicit. Factor

    b_(i+j)=q^(−i²/2)q^(−j²/2)(q^(−i))^j.

The row and column factors in the numerator and denominator cancel (the missing index zero contributes one). Writing x_i=q^(−i), the numerator has Vandermonde determinant on x_0=1,x_1,…,x_N; the denominator has the Vandermonde on x_1,…,x_N multiplied by ∏_(i=1)^N x_i, because its column exponents start at one. Their ratio is

    w_N=∏_(i=1)^N (x_i−1)/x_i=∏_(i=1)^N(1−q^i).

This proves (8). The elementary product inequality ∏(1−u_j)≥1−Σu_j for 0≤u_j≤1 yields the explicit tail estimate

    0≤w_N−w≤q^(N+1)/(1−q).

Thus w and every initial coordinate c_r in (2) are uniformly computable real numbers. This does not turn the spurious coordinate-positive hierarchy into a realizable path. It is consistent with effective recovery of the unique positive initial law and its genuine tilt: those statements concern the realizable solution class. No claim of a new general effective moment-reconstruction algorithm is made here.
