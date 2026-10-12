# All moments can fail to determine an exponential-tilt continuation

9 October 2026 UTC. Additive ordinary mathematical result. This packet tests an explicitly enlarged, noncompact numerical model. It makes no protected edit, integration, T20 closure, T21, formal-kernel, empirical, noetic-realization, or metaphysical-uniqueness claim. Classical moment theory is credited below; no field-wide novelty claim is made.

## 1. Outcome and exact transfer boundary

The finite-support tensor result survives unchanged. For fixed known support of N distinct channel columns, moments through degree N−1 determine the aggregate law and its controlled tilt trajectory. Infinite support alone does not defeat that conclusion's full-moment analogue: on a fixed compact subset of a finite-dimensional real vector space, **all tensor moments determine the law**, and hence every admitted normalized exponential tilt.

The boundary appears when the trait itself is unbounded. On [0,∞), there are two different, strictly positive densities with all nonnegative integer moments equal for which the same constant nonnegative control produces different future means. More strongly:

- All coordinates of the initial infinite moment record agree.
- Every finite-order right time derivative of every moment coordinate agrees at time zero.
- The mean-response functions disagree somewhere in every open interval of positive time, including arbitrarily close to zero.
- Both moment trajectories satisfy the same exact infinite hierarchy, with the same initial sequence.

Thus **closure under the infinitesimal moment equations is weaker than a continuation-complete representation**. It supplies neither uniqueness of the coordinatewise smooth hierarchy solution nor a descended finite-update map. The full initial probability law still gives one unambiguous, explicitly specified tilt continuation.

This is a scoped application of classical lognormal moment indeterminacy and Laplace-transform uniqueness to the preceding tensor-continuation interface. The general future-congruence requirement is already inherited. The finding is a negative transfer test for replacing actual-update preservation by generator/derivative closure.

## 2. State, controls, output, and Fisher interpretation

### 2.1 New model class

Let P∞ be the Borel probability measures μ on [0,∞) for which

\[
m_r(\mu)=\int x^r\,\mu(dx)<\infty\quad(r=0,1,2,\ldots),\qquad m_0=1.
\]

The variable x is a nonnegative, generally unbounded numerical trait. It is **not a column of a finite stochastic channel**, not a probability, and not a source token or evidence item. The output is the scalar trait mean q=m₁. Its codomain is [0,∞), rather than a probability simplex. The retained record is

\[
R(\mu)=(m_0,m_1,m_2,\ldots)\in\prod_{r\ge0}\operatorname{Sym}^r(\mathbb R).
\]

In this one-dimensional trait space the tensor components are precisely scalar moments. This is a graded **product**, or equivalently an expectation functional on the polynomial algebra, not an element of the algebraic direct sum T(ℝ). For the example below every grade is nonzero. Nothing identifies this infinite record with an actual finite episode representation in the inherited graded manuscript.

Controls g(t) are nonnegative, piecewise constant, with finitely many switches and finite values on each bounded time interval. Put u(t)=∫₀ᵗg(s)ds, so u(t)≥0 and finite. Define

\[
L_\mu(u)=\int e^{-ux}\,\mu(dx),\qquad
T_u\mu(dx)=\frac{e^{-ux}}{L_\mu(u)}\mu(dx),\qquad u\ge0. \tag{1}
\]

Because 0<e^(−ux)≤1 for finite x and u≥0, 0<Lμ(u)≤1. Normalization never divides by zero. All moments of Tᵤμ are finite, since ∫xʳe^(−ux)dμ≤mᵣ(μ). Its Radon–Nikodym density relative to μ is strictly positive, so it has the same null sets at every finite u. Direct cancellation proves T₀=id and TᵥTᵤ=Tᵤ₊ᵥ for u,v≥0. This is an everywhere-defined semigroup on P∞, not an asserted two-sided group.

### 2.2 Legitimate derivatives and the hierarchy

Write Aᵣ(u)=∫xʳe^(−ux)dμ. For each fixed r,k, dominated convergence, using xʳ⁺ᵏ as a dominating function for the corresponding parameter derivatives on u≥0, gives

\[
A_r^{(k)}(u)=(-1)^k A_{r+k}(u),\qquad
A_r^{(k)}(0+)=(-1)^k m_{r+k}(\mu). \tag{2}
\]

Difference quotients at zero can be dominated by xʳ⁺ᵏ⁺¹ when establishing the next derivative. All required moments exist. Consequently each Aᵣ and Aᵣ/L is C∞ on the closed half-line in the right-derivative sense, and ordinary C∞ in its interior. Positivity and continuity give a positive lower bound for L on each bounded u interval; there is no normalization singularity there.

At nonswitching times, with Mᵣ(t)=mᵣ(Tᵤ₍ₜ₎μ), quotient differentiation yields

\[
\boxed{\dot M_r=-g(t)M_{r+1}+g(t)M_1M_r,\qquad r\ge0.} \tag{3}
\]

The equations also hold almost everywhere and in integrated form across switches. In particular

\[
\dot q=-g(t)\operatorname{Var}_{T_u\mu}(x),\qquad
q_\mu(u)=-\frac{L'_\mu(u)}{L_\mu(u)}. \tag{4}
\]

All orders of the initial time jet below refer to the constant control g=1. Piecewise-constant controls generally do not have high-order time derivatives at their switches.

### 2.3 Precise extent of the Fisher connection

At a law μ with finite second moment, take zero-mean square-integrable scores a,b∈L²₀(μ), representing tangent signed measures aμ,bμ, and define the Fisher pairing hμ(aμ,bμ)=∫ab dμ. For the linear expectation objective J(μ)=∫x dμ, the differential on such scores is DJμ[aμ]=∫xa dμ. Cauchy–Schwarz and m₂<∞ make it finite, and

\[
h_\mu((x-m_1)\mu,a\mu)=\int xa\,d\mu.
\]

Thus x−m₁ is its Fisher Riesz gradient score. Equation (1) has negative-gradient velocity −g(x−q)Tᵤμ and Fisher squared speed g²Var(x). This is a checked tangent pairing and an explicit realizable one-sided trajectory. It is not a claim that all positive densities form an open Hilbert manifold, that arbitrary L² scores admit a two-sided positive affine perturbation, or that an unspecified infinite-dimensional Hessian theorem automatically applies.

For a direct uniqueness qualification, consider positive densities pₜ relative to the full initial μ, starting at p₀=1, whose logarithms are locally absolutely continuous for μ-almost every x and solve ∂ₜlog pₜ(x)=−g(t)(x−q(t)), where q(t)=∫xpₜdμ and gq is locally integrable. Integration gives pₜ(x)=exp(−u(t)x+∫₀ᵗgq). Normalization forces the scalar prefactor to be 1/Lμ(u(t)), hence (1). The explicit tilt satisfies these conditions. No uniqueness for a broader, unspecified class of weak measure equations is imported.

## 3. Positive compact-support theorem

**Theorem 1.** Let K⊂ℝᵐ be a fixed compact set, and μ,ν be Borel probability measures carried by K. If

\[
\int z^{\otimes r}\,d\mu=\int z^{\otimes r}\,d\nu\quad\text{for all }r\ge0,
\]

then μ=ν. Therefore their outputs and entire laws agree after every normalized tilt e^(−u·z), u∈ℝᵐ, including all endpoints and histories of finite piecewise-constant real controls.

**Proof.** Equality of the tensor components gives equal integrals of every coordinate monomial and hence every polynomial. Restricted coordinate polynomials form a real algebra containing constants and separating the points of K. Stone–Weierstrass makes them uniformly dense in C(K). Finite total masses allow passage to the uniform limit, so μ and ν have equal integrals of all continuous functions. Uniqueness of finite Borel measures on the compact metric space K gives μ=ν. All tilt factors are positive and bounded above and below on K for fixed finite u, so their normalized updates are well-defined. □

For this specific continuation one can also see the role of compactness directly. If ||z||≤B on K, the exponential series is uniformly absolutely convergent and

\[
Z_\mu(u)=\sum_{r=0}^{\infty}\frac{(-1)^r}{r!}
\langle u^{\otimes r},M_r(\mu)\rangle.
\]

The corresponding vector numerator ∫z e^(−u·z)dμ has the analogous uniformly convergent moment expansion. Bounds by e^(||u||B), with an additional B for the numerator, justify integration term by term. These are genuine convergent series, not merely formal jets.

**Application to the inherited channel type.** For any measurable channel-column map κ:Ω→Δₘ with finite output dimension m and a fine probability law P, the aggregate law κ_*P lies in the compact closed simplex. All symmetric tensor moments of κ determine that aggregate law and its linear-objective tilt continuation. The number of fine states or distinct columns may be infinite. This retains aggregate-law sufficiency only; labels, within-fibre structure, and other interventions can still require additional records, exactly as in the finite theorem.

Full-moment sufficiency on an infinite compact support is not a claim of a finite cutoff. Already on the binary-simplex line, for each cutoff d, choose d+2 distinct columns. The inherited finite Vandermonde countermodel supplies positive laws agreeing through degree d but with distinct tilt continuations. Nor is the theorem a claim of effective recovery, numerical stability, or a finite storage/measurement procedure. Unlike the finite-support separating-direction theorem, it does not assert that one generic scalar projection determines an arbitrary multivariate compact law.

## 4. Exact noncompact countermodel

### 4.1 The correctly parameterized Stieltjes family

Let

\[
f(x)=\frac{1}{x\sqrt{2\pi}}\exp\!\left(-\frac{(\log x)^2}{2}\right),\qquad x>0,
\]

and for −1<ε<1 set

\[
f_\varepsilon(x)=f(x)\bigl[1+\varepsilon\sin(2\pi\log x)\bigr]. \tag{5}
\]

Use the concrete pair ε=+1/2 and ε=−1/2. Both are everywhere strictly positive on (0,∞), between f/2 and 3f/2, and define different laws. In particular, sin(2πlog x)>0 on (1,e^(1/2)), so the plus law assigns that interval strictly greater probability.

To prove normalization and moment matching at once, put Y=log X under f, so Y is standard normal. For every nonnegative integer n,

\[
\begin{aligned}
\int_0^\infty x^n f(x)\sin(2\pi\log x)\,dx
 &=\mathbb E[e^{nY}\sin(2\pi Y)]\\
 &=e^{n^2/2}\mathbb E[\sin(2\pi(Z+n))]\\
 &=e^{n^2/2-2\pi^2}\sin(2\pi n)=0, \tag{6}
\end{aligned}
\]

where Z is standard normal. The second equality is the real Gaussian square-completion identity e^(ny)φ(y)=e^(n²/2)φ(y−n). The last equality uses symmetry to cancel the sine expectation and the Gaussian characteristic-function identity E cos(2πZ)=e^(−2π²). All integrals are absolutely finite because |sin|≤1 and the normal has every exponential moment. Consequently

\[
\boxed{m_n(\mu_+)=m_n(\mu_-)=e^{n^2/2}\quad(n=0,1,2,\ldots).} \tag{7}
\]

The n=0 identity proves both densities have total mass one. This is the classical lognormal Stieltjes class, not a newly found moment-indeterminate distribution.

The parameter choice matters. For log X∼N(a,σ²), the uniform construction uses sin(2π(log x−a)/σ²); the corresponding mixed expectation is exp(na+n²σ²/2−2π²/σ²)sin(2πn). Leaving sin(2πlog x) unchanged for arbitrary a,σ does not generally give the same cancellation.

### 4.2 Why the controls are one-sided

For c>0,

\[
\int e^{cx}f(x)\,dx
=\frac1{\sqrt{2\pi}}\int_{\mathbb R}
       \exp(ce^y-y^2/2)\,dy=\infty.
\]

Indeed ceʸ−y²/2 tends to +∞ as y→∞, so the integrand is eventually at least a positive constant. The lower bound f±≥f/2 proves the same divergence for the two chosen laws. A negative cumulative tilt u=−c therefore cannot be normalized from these initial laws. The all-real-control promise of the finite/compact theorem is not transferred. Nonnegative controls, including the single constant g=1 used here, suffice to prove failure. Signed controls whose cumulative u stays nonnegative can also be handled with suitable endpoint differentiability, but they are not needed or claimed as a two-sided semigroup on P∞.

### 4.3 Laplace uniqueness and future separation

The following classical fact is given with a short proof to make the existence claim exact: finite Borel measures on [0,∞) are determined by their Laplace transforms. Push a measure forward by s=e^(−x) into (0,1] and regard it as a measure on [0,1] with zero mass at 0. Its n-th moment is L(n). If two normalized measures have equal Laplace transforms on t>0, continuity as t↓0 gives equal total masses; their transformed measures then have all polynomial moments equal. Uniform polynomial approximation on [0,1] and finite-measure uniqueness make the transformed measures equal. The map x↦e^(−x) is a Borel bijection onto (0,1], with Borel inverse −log s, hence the original measures are equal.

Because μ+≠μ−, their Laplace functions cannot agree for every t>0. This alone does not yet show that their normalized means differ at a particular preselected time. Suppose, instead, their means agreed for every t>0. Equation (4) would give

\[
(\log L_+-\log L_-)'=0.
\]

The ratio L+/L− would be constant. Both transforms tend to 1 at zero by dominated convergence, so the ratio would be 1, contradicting Laplace uniqueness. Thus a future mean differs.

There is also a stronger interval statement. For any finite measure on [0,∞), L(z)=∫e^(−zx)dμ is holomorphic for Re z>0: on each smaller half-plane, xᵏe^(−ax) is bounded for every fixed derivative order k, justifying differentiation. In particular L is real analytic for t>0. If the two means agreed on any nonempty open subinterval of (0,∞), their transforms would be proportional there; the identity theorem would make that proportionality hold on the whole right half-plane. Continuity at zero fixes the proportionality constant to 1, again a contradiction.

**Theorem 2.** For the exact pair (5) with ε=±1/2 under g=1, q+(t) and q−(t) disagree somewhere in every nonempty open subinterval of (0,∞). In particular they have different right-hand continuation germs at 0.

This does **not** claim q+(t)≠q−(t) at every individual t>0. It does not select a numerical time or separation magnitude. No numerical quadrature is used as the existence proof.

## 5. Equal jets and nonunique smooth hierarchy continuations

For the constant control g=1, equations (2) and (7) give

\[
L_+^{(k)}(0+)=L_-^{(k)}(0+)=(-1)^ke^{k^2/2}.
\]

Since Lq=−L′ and L(0)=1, differentiating n times from the right gives

\[
q^{(n)}(0+)=-L^{(n+1)}(0+)
 -\sum_{k=1}^{n}\binom nk L^{(k)}(0+)q^{(n-k)}(0+). \tag{8}
\]

Induction proves q+^(n)(0+)=q−^(n)(0+) for every n. The same quotient argument with Aᵣ/L proves equality of every finite right derivative of every Mᵣ. Equivalently, iterating (3) expresses a k-th initial derivative of grade r as a polynomial in finitely many initial moments, no higher than grade r+k.

For illustration only, their common first three mean-jet entries are

\[
q(0)=e^{1/2},\quad
q'(0)=e-e^2,\quad
q''(0)=e^{9/2}-3e^{5/2}+2e^{3/2}.
\]

Taylor's theorem on a right neighborhood therefore makes q+(t)−q−(t)=o(tᴺ) for every fixed integer N≥0, although Theorem 2 forbids its vanishing on any right interval. Smooth right jets do not determine a smooth right germ.

There is no analytic paradox. The formal Taylor series of L at zero has coefficients (−1)ⁿe^(n²/2)/n!, whose absolute term ratio at any nonzero t is |t|e^(n+1/2)/(n+1)→∞. Its convergence radius is zero. Integrating the exponential's power series term by term is invalid at this heavy-tailed boundary, even though each differentiated moment is finite. The functions are analytic at every strictly positive time, but not at the boundary zero.

The two curves (Mᵣ⁺(t))ᵣ and (Mᵣ⁻(t))ᵣ are different coordinatewise C∞ solutions of the exact same system

\[
\dot M_r=-M_{r+1}+M_1M_r
\]

on the admissible moment image R(P∞), from precisely the same initial point. This establishes nonuniqueness **in that coordinatewise-smooth solution class**. No Banach-space ODE uniqueness theorem with a verified Lipschitz/growth norm has been invoked or refuted.

At the derivative level the projected rule Fᵣ(Rμ)=−mᵣ₊₁+m₁mᵣ really is well-defined on moment fibres. At finite time, however, Rμ+=Rμ− and Theorem 2 implies R(Tₜμ+)≠R(Tₜμ−) for some t in every interval. Hence no family of deterministic maps \bar Tₜ on R(P∞) can satisfy \bar Tₜ∘R=R∘Tₜ for all t≥0 and all μ. This is the exact failure of continuation descent; it is not a failure of the full-law semigroup (1).

## 6. Two precise repairs

### 6.1 Tail hypotheses: a finite positive exponential moment suffices

Suppose μ is a probability on [0,∞) and ∫e^(ax)dμ<∞ for some a>0. If another probability ν has the same nonnegative integer moments, monotone convergence of the nonnegative series for e^(bx), 0≤b≤a, gives

\[
\int e^{bx}\,d\nu=\sum_{n\ge0}\frac{b^n m_n}{n!}
=\int e^{bx}\,d\mu<\infty.
\]

For |t|<a, absolute domination by e^(|t|x) now justifies the common moment series for both Laplace transforms. They agree on a positive interval, and analyticity plus Laplace uniqueness gives μ=ν. This proves determinacy in the present half-line class, with no Carleman theorem required. Their admitted continuations therefore agree. The tail hypothesis is sufficient, not necessary, and no rule for deciding it from arbitrary data is claimed.

There is a useful positive-time check: for every u>0, E_{Tᵤμ}[e^(uX/2)]=Lμ(u/2)/Lμ(u)<∞. Thus every positive-time tilted law in this model is moment-determinate, even if its initial law is not. Also Tᵤ is injective on its image: multiplying its law by e^(ux) and renormalizing recovers μ, with integral 1/Lμ(u)<∞. Hence the two countermodel laws remain distinct and their **full moment sequences differ at every t>0**, although their scalar means need not differ at every individual time. This is compatible with the two smooth hierarchy solutions sharing all right jets at zero.

### 6.2 A continuation-adapted observable record

Retaining the actual Laplace profile s↦Lμ(s), s≥0, is sufficient for every μ∈P∞. Besides determining μ, it has the exact closed finite-update rule

\[
L_{T_u\mu}(s)=\frac{L_\mu(s+u)}{L_\mu(u)},\qquad s,u\ge0. \tag{9}
\]

The mean is −L′(0+) when finite, and after a tilt is −L′(u)/L(u). Formula (9) follows immediately from the two integrals and their positive normalization. This record preserves the actual update family rather than only its formal derivatives at zero.

Even the countable family Lμ(n), n=0,1,2,…, determines μ set-theoretically, by the compactification proof above. These are all moments of the bounded coordinate s=e^(−x). Equivalently, they are contained in the full tensor moments of the simplex map κ(x)=(e^(−x),1−e^(−x)). Those bounded-coordinate tensors distinguish the countermodel; the raw x-polynomial tensors do not. The finite-control update from the countable sample record can be defined through its unique measure, but no effective algorithm, stable interpolation, or finite-coordinate rule follows from that fact. The full profile has the transparent shift formula (9). In the bounded coordinate, the initial output is E[−log s], an unbounded observable as s approaches 0; mere moment determinacy supplies no finite-precision modulus for its recovery.

This makes the dependence on the declared observable algebra explicit. “All moments” always means moments of named coordinates. It is not synonymous with “all information,” and changing coordinates changes which observables the record carries.

## 7. Inherited ownership, classical ancestry, and non-claims

### Inherited obligations already owned

1. **Graded formalisation, §§3 and 11.** The pinned H-formalisation manuscript declares the algebraic direct sum and finite support per actual representation. Its Theorem 11.2 already requires the actual retained update, output, and relevant inquiry landscape to be constant on representation fibres. Those obligations are not discovered here. This packet uses the criterion to show failure for R and Tₜ and does not assert any undeclared inquiry landscape preservation.
2. **H-continuation, finite reference model and Theorem 2.** The retained manuscript explicitly fixes finite X and finite action–observation instruments, closes required observables under the actual operators Kₐ,ₒ, and proves exact predictive updates. It does not replace finite updates by generator derivatives. Its finite stabilization and coordinate-dimension results are not imported into the noncompact law class here. Even before this packet, its true requirement would reject an update whose relevant output varies within a retained fibre.
3. **H-ICS v5, information criterion and observation congruence.** The basic fibre-factorization criterion is set-theoretic and expressly carries no computability guarantee. Its operational state-identification theorem has finite state/repertoire hypotheses. The present noncompact example is a direct new application of the criterion, not an extension of its finite theorem by assertion.
4. **Available inherited measure/computability branch.** The pinned DEFECT_COMPUTABILITY.md concerns the point-concentration defect of explicitly indexed total synchronous Cantor observers, with exact cylinder probabilities and an arithmetical hierarchy. The local P02 U05 measure core treats positive singleton mass, conull-event intersections, pushforwards, countable mixtures, and weak versus total-variation limits; P02 CV-C treats the declared effective observer numbering. Their continuous proof sections were read. They already distinguish measure existence, effective presentation, and decision complexity. They neither state the lognormal moment/tilt countermodel in the read sources nor license identifying arbitrary moment records with law-determining cylinder probabilities. Both laws here are atomless, so their shared point-concentration defect is 1; that defect is not a moment-determinacy invariant. This is a scoped source comparison, not a repository-wide absence or priority claim.

### Classical mathematics already owned

The density family (5) is classical. Jordan Stoyanov's 2004 paper, *Stieltjes classes for moment-indeterminate probability distributions*, §§2–3 and 5, explicitly states the standard-lognormal sine family and distinguishes the classical bounded-support and exponential-moment positive cases. It credits Stieltjes's 1894 construction and Heyde's 1963 general lognormal treatment. The inspected author-uploaded full text supports that attribution; Heyde's publisher abstract/metadata were inspected, not its complete proof. The derivation (6) here checks the precise parameterization directly.

Laplace uniqueness for finite measures is classical; Zenghu Li's *Continuous-state branching processes with immigration*, §1, Theorem 1.1, provides an explicitly inspected monotone-class proof on [0,∞). The compactification proof here is another elementary verification, not a novelty claim. Compact-support determination uses the standard Stone–Weierstrass and finite-measure uniqueness theorems. Replicator/normalized-exponential geometry is already classical and credited in the preceding finite packet.

The scoped contribution is the **verified application and transfer boundary**: the completed finite tensor-continuation calculation extends positively to compact aggregate laws when the full moment record is allowed, but a noncompact trait enlargement admits equal all-order tensors and equal all initial jets without future output agreement. Actual-update congruence survives as the correct inherited criterion; generator closure alone does not replace it. No absolute memory lower bound, field priority, sampling-complexity result, physical realization, cognitive identification, metaphysical conclusion, or permission to discard source/provenance distinctions follows.

## 8. Verification and source ledger

`verify.py` performs exact symbolic controls on the general integer cancellation, corrected lognormal parameterization, normalized hierarchy, low-order jet recurrence, and finite-update profile composition. These finite controls supplement the ordinary universal proofs above. They do not numerically certify an existential separating time, prove all moments by testing finitely many, or provide a formal-kernel proof.

`SOURCE_LEDGER.json` records exact local hashes, source URLs, inspected scopes, and the limits of each source claim. `RESEARCH_EVENTS.jsonl` records prospective work events; there is no idle-time or reconstructed earlier research-time credit. Protected sources and earlier result bytes are unchanged.

### Verified source links

- [Inherited H-formalisation at the declared repository pin](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-formalisation/orthing_formalisation_v1.md).
- [Inherited H-continuation at the same pin](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-continuation/continuation_complete_orthing.md).
- [H-ICS v5 at the same pin](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-ics-v5/information-composition-and-self-revision-v5.tex).
- [Pinned inherited point-concentration computability result](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/experiments/orthemology-v5/mathematics/DEFECT_COMPUTABILITY.md).
- [Stoyanov (2004), publisher record](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/stieltjes-classes-for-momentindeterminate-probability-distributions/3D6EA0EEC47B46B3DDA05BA0DC709F83), [inspected author-uploaded full text](https://www.researchgate.net/publication/305974332_Stieltjes_classes_for_moment-indeterminate_probability_distributions). The publisher displays DOI 10.1239/jap/1082552205; the author-uploaded record also lists 10.1017/S0021900200112355.
- [Heyde (1963), publisher abstract and metadata](https://academic.oup.com/jrsssb/article/25/2/392/7035281).
- [Li (2019), §1, Theorem 1.1](https://arxiv.org/pdf/1901.03521).
