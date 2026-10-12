# The sharp rank boundary for square-positive quadratic damping

10 October 2026 UTC. Additive ordinary mathematical research. This packet proves a project-relative discriminator, not a field-priority claim. The parent proposed the rank question and the strengthened Gaussian-mixture obstruction. The investigator checked and assembled the proofs. These contributions are author-side work, not independent review. No protected source, integration target, or closure status is changed.

## 1. Exact statement and distinct quantifiers

Fix a finite dimension d≥1, an integer 0≤r≤d, and 0<T≤∞. Set

    h(x)=x₁²+⋯+xᵣ²,       k=d−r.

The empty sum is zero. An admissible path is a family of real linear functionals L_t on R[x₁,…,x_d], 0≤t<T, satisfying:

- L_t(1)=1;
- L_t(q²)≥0 for every real polynomial q and every t;
- every monomial coordinate is C¹, including continuity and a continuous right derivative at zero;
- for every polynomial p,

    L_t'(p)=−L_t(hp)+L_t(h)L_t(p).                         (H)

There is no degree cutoff, finite support assumption, initial-law assumption, growth premise on uncontrolled moments, or uniform-in-degree differentiability hypothesis. Let P∞(R^d) denote probabilities having every absolute polynomial moment. A whole-path lift is one fixed μ∈P∞ such that

    L_t(p)=∫p e^(−th)dμ / ∫e^(−th)dμ,   p∈R[x], 0≤t<T.   (L)

**Theorem R (automatic existence).** For each fixed pair (d,r), the following universal assertion holds if and only if k≤1: every admissible path, on every positive-length interval, has a whole-path lift. When k≤1, initial representability follows too, and each such path has a unique global continuation as an admissible moment-coordinate path. When k≥2, there is a global admissible path with no representing law at any time. It can be chosen strictly square-positive at every finite time. It can additionally be chosen nonstationary if r≥1; when r=0, (H) forces every path to be stationary.

**Theorem I (universal law identification).** Every admissible path has a unique whole-path lift, with determinate full moment records at every positive time, if and only if k=0. More discriminatingly, even after restricting to paths known to have lifts, the assertion that every such path has a unique lift holds if and only if k=0. For every k≥1 there are distinct full-support probabilities whose tilted laws have the same full moment record for all t≥0. These are genuine probability paths, entirely separate from the nonmoment obstruction in Theorem R.

Thus k=1 is the exact gap: every full-square-positive hierarchy is realizable, but law identification is not automatic. This is a universal classification; it does not say that any particular partially damped path lacks a unique law. Nor does a failure of law identification imply failure of uniqueness of continuation of its moment coordinates.

## 2. Dynamical bounds in precisely the controlled directions

This section specializes the inherited unnormalization and joint-square argument from tensor-realizability-extension-20261010/RESULT.md, Sections 2–3 and 6. Write

    a(t)=exp(−∫₀ᵗ L_v(h)dv),       A_t(p)=a(t)L_t(p).

Since h is a sum of squares, L_t(h)≥0 and 0<a(t)≤1. Product differentiation gives A_t'(p)=−A_t(hp). Induction over polynomials gives C∞ regularity and

    A_t^(n)(p)=(−1)^n A_t(hⁿp).                           (2)

For every q and n≥0, q²hⁿ is a finite sum of squares, including the empty-sum case. Hence A_t(q²hⁿ)≥0. Backward Taylor expansion from t to t−b, 0<b<t, has nonnegative terms and nonnegative integral remainder:

    Σ_{n=0}^N bⁿ A_t(q²hⁿ)/n! ≤ A_{t−b}(q²).

Selecting a term and letting b increase to t yields

    0≤A_t(q²hⁿ)≤n! A₀(q²)/tⁿ,       t>0.                (3)

For each i≤r, the multinomial expansion expresses hⁿ−x_i^(2n) as a sum of monomial squares with nonnegative coefficients. Taking q=1 in (3), and using A₀(1)=1, gives

    0≤L_t(x_i^(2n))≤n!/[a(t)tⁿ].                         (4)

When this even moment is nonzero, n!≤nⁿ implies

    L_t(x_i^(2n))^(−1/(2n))
       ≥a(t)^(1/(2n)) sqrt(t/n)
       ≥sqrt(a(t)t)/sqrt(n).

A zero even moment contributes +∞ in the Carleman convention. Therefore every controlled marginal satisfies Carleman's divergent-series condition at every t>0. No analogous estimate has been obtained for a hidden coordinate.

**The precise classical existence input.** For a full positive-semidefinite d-sequence, Carleman conditions in d−1 marginals already imply representing-measure existence; imposing the condition in all d also gives determinacy. This is Putinar–Schmüdgen, Theorem 25, printed p.24, [arXiv:0810.0840v1](https://arxiv.org/pdf/0810.0840v1). It starts from positivity, not an already supplied multivariate measure. Thus if d≥2 and r≥d−1, (4) provides a probability representative at every positive time. If r=d, these representatives are unique.

The dimension-one edge is handled directly by the classical Hamburger theorem: square positivity of a functional on R[x] already supplies a representing measure. For d=1,r=1, (4) and scalar Carleman give determinacy. For d=1,r=0, h=0 makes L_t=L₀, and any Hamburger representative of L₀ is a whole-path lift. Its uniqueness is not guaranteed. This avoids relying on an unstated d=1 interpretation of Theorem 25.

## 3. One positive-time representative recovers the entire path

For completeness, the inherited one-time-representative strengthening of Theorem E is made explicit. This is not a new exhaustion theorem being credited again.

By (2)–(3), on a neighborhood of any s>0 with t≥s/2,

    |A_t^(n)(q²)|≤n! (2/s)ⁿ A₀(q²).

Taylor remainders tend to zero for sufficiently small increments, so A_t(q²) is real analytic on (0,T). Polarization p=((p+1)²−(p−1)²)/4 gives analyticity of A_t(p) for every p.

Choose one s∈(0,T), one probability representative ρ_s, and set λ_s=a(s)ρ_s. For 0<b<s the nonnegative exponential series and the backward Taylor inequality give

    ∫q²e^(bh)dλ_s
       =Σ_{n≥0} bⁿA_s(q²hⁿ)/n! ≤ A_{s−b}(q²).           (5)

For u>0 set G_q(u)=∫q²e^((s−u)h)dλ_s. This is finite: use (5) when 0<u<s, and polynomial integrability when u≥s. Around any u>0 there is a strictly positive exponential margin below s, or a strictly negative exponent margin when u>s. This dominates the Taylor series and all derivative factors. Thus G_q is real analytic, and at u=s its derivatives equal (−1)^nA_s(q²hⁿ). Analytic identity on (0,T) yields

    A_u(q²)=∫q²e^((s−u)h)dλ_s.

Let u decrease to zero. Monotone convergence and boundary continuity yield

    ∫q²e^(sh)dλ_s=A₀(q²).

Consequently μ=e^(sh)λ_s is a probability, since A₀(1)=1, and it has every polynomial moment absolutely finite, since |p|≤(1+p²)/2. Polarization supplies all signed and mixed moments. This is exactly (L) for every time, including zero. There was no need to select representatives measurably across times, and no hidden-coordinate tail estimate was needed.

Conversely, any μ∈P∞ gives a global path (L): h≥0 makes e^(−th) bounded by one; |p|hⁿ is polynomially integrable; dominated convergence gives the hierarchy and all required boundary derivatives. Its normalizer never vanishes at a finite time.

For k≤1, Section 2 supplies the one positive-time representative. This proves the existence direction of Theorem R and the global extension's existence.

## 4. The exact identification and continuation distinctions

The following facts are inherited from Theorem E and its noncoercive equivalence relation, with their roles kept separate.

For μ,ν∈P∞ write μ∼_hν when

    h_*(pμ)=h_*(pν) for every polynomial p,                (6)

as finite signed measures on [0,∞). Equivalently all transforms ∫p e^(−th)dμ and ∫p e^(−th)dν agree for t≥0. To see the relevant direction, equality of a normalized path determines its normalizer uniquely by a'=−L_t(h)a, a(0)=1. Hence the unnormalized transforms agree on its positive-time interval. They are analytic for t>0, so agreement extends to all positive times. Uniqueness of the signed Laplace transform then gives (6). The converse is immediate.

For an initial moment record c with representing-law fibre F_c, the lifted moment paths are therefore indexed exactly by F_c/∼_h. When k≤1 these are all admissible paths. In particular all lifts of a finite path give the same global moment coordinates. Any admissible extension in this rank range again has a lift by Theorem R, so the global extension is unique in the full admissible class. For arbitrary k, the same uniqueness holds within the class of lifted paths. No blanket existence or continuation assertion for all nonmoment paths at k≥2 is needed.

There is an even more direct law-identification test for a particular lifted path. At any s>0, every representative ρ of its full record L_s de-tilts by

    μ=a(s)e^(sh)ρ

to a lift of the whole path, by Section 3; every lift yields a representative by tilting. These maps are inverse. Therefore a path has one lift exactly when its full moment record is determinate at one, equivalently every, positive time.

When k=0, Section 2 guarantees positive-time determinacy, proving the positive direction of Theorem I. At zero time, determinacy still need not hold: different initial laws with the same initial moments can produce different hierarchy paths. That is a different question from how many laws lift one already specified path.

For a unique-law partially damped control, take L_t(p)=p(0). Any representative has ∫x_i²=0 for every i and must be δ₀. Thus partial damping does not make every path ambiguous. When r=0, all coordinate paths are constant, so each valid initial record has exactly one coordinate path even when its law fibre is indeterminate.

## 5. Distinct full-support laws with the same entire record whenever k≥1

Use the inherited lognormal Stieltjes pair

    f(y)=exp(−(log y)²/2)/(y sqrt(2π)),   y>0,
    ν_±(dy)=f(y)[1±(1/2)sin(2πlog y)]dy.

The laws are distinct. For every integer n≥0, Gaussian square completion gives

    ∫yⁿsin(2πlog y)f(y)dy
       =exp(n²/2−2π²)sin(2πn)=0.

They therefore have identical moments exp(n²/2). This pair and its cancellation are inherited, not a new indeterminate-family construction.

Let γ_m be standard Gaussian law on R^m, with γ₀ the one-point empty product, and put η_±=(ν_±+γ₁)/2. These are distinct laws with identical moments and an everywhere-positive density on R. For any k≥1 set

    μ_±=γ_r⊗η_±⊗γ_{k−1}.

They have full support on R^d and all absolute polynomial moments. Damping acts only on γ_r. Its survival mass is Z_r(t)=(1+2t)^(−r/2), and its normalized tilted coordinates remain independent centered Gaussians of variance (1+2t)^(−1). All hidden laws are unchanged. Factorization therefore gives identical full mixed moments for μ_+ and μ_- at every t≥0, while their vector laws remain distinct because the η marginal differs.

These are strictly square-positive records: the tilted joint densities are positive everywhere. For r≥1, the controlled second moment 1/(1+2t) makes the common path nonstationary. For r=0 it is necessarily stationary. This proves the negative direction of Theorem I, including the nullity-one case where Theorem R guarantees every admissible path is realizable.

## 6. At least two hidden directions admit forever nonmoment paths

### 6.1 The direct stationary obstruction

The retained classical input is a normalized square-positive nonmoment functional Λ on R[u,v]. Its existence is already used in moment-evolution-source-comparison-20261010/RESULT.md, Section 3, sourced to Schmüdgen's Proposition 13.5. For k≥2 define the polynomial substitution

    E(p)(u,v)=p(0,…,0,u,v,0,…,0),

where u,v occupy two hidden coordinates. Define B(p)=Λ(E(p)). Then B(1)=1, B(q²)=Λ(E(q)²)≥0, and B(hp)=0 for every p. Thus L_t=B is a global stationary admissible path. If B had a representing probability, its projection onto these two hidden coordinates would represent Λ, a contradiction. This proves necessity in Theorem R without any initial representation premise.

The substitution E is an algebra homomorphism. It is not itself an underlying probability construction for Λ, and no representing measure is presupposed by the word “hidden.”

### 6.2 A strictly square-positive obstruction for all finite times

The parent's strengthened control removes the degeneracy of square positivity. In the same classical source one can take Λ(1)=1 and

    F(u,v)=1+u⁴v²+u²v⁴−u²v²,       Λ(F)=−1.

The nonnegative witness is checked independently by AM–GM: u⁴v²+u²v⁴+1≥3u²v², hence F≥0. Only the source's full-square-positive Λ is imported; no finite control is claimed to construct or certify that infinite functional. [Schmüdgen, The Moment Problem, Proposition 13.5, pp.318–319](https://www.imath.kiev.ua/~golub/ref2/The-Moment-Problem.pdf).

Let γ_d be standard full-support product Gaussian, and define the genuine, unnormalized Gaussian-killed functional

    G_t(p)=∫p(x)e^(−th(x))dγ_d(x).

It satisfies G_t'=-G_t(h·). Independence and Gaussian moments give

    G_t(1)=Z_r(t)=(1+2t)^(−r/2),
    G_t(F)=6Z_r(t).

Choose the explicit mixture

    A_t=(13/14)B+(1/14)G_t,
    a(t)=A_t(1)=(13+Z_r(t))/14,
    L_t=A_t/a(t).                                         (7)

Both summands solve the unnormalized hierarchy, so (7) solves (H). It is normalized and C∞ at the boundary and thereafter. Its normalizer is at least 13/14. For every nonzero polynomial q and finite t, G_t(q²)>0: the integrand is nonzero on an open set and the weighted Gaussian density is positive everywhere. Thus L_t(q²)>0.

Nevertheless,

    A_t(F)=−13/14+(3/7)Z_r(t)≤−1/2<0

for every t≥0. Since F is globally nonnegative, no L_t has any positive representing measure. This is an all-time obstruction for one fixed path, not a family with successively longer finite horizons.

For r≥1, h−L_t(h) is a nonzero polynomial and strict square positivity gives

    dL_t(h)/dt=−L_t((h−L_t(h))²)<0.

Hence the path is nonstationary. Explicitly, with s=1+2t and Z=s^(−r/2),

    L_t(h)=rZ/[s(13+Z)]>0.

For r=0, h=0 and the whole path is constant, as required by (H).

For a normalized classical Λ without a specified witness value, the same argument works with any F≥0 having B(F)=−δ<0. Put M=∫F dγ_d and ε=δ/[2(δ+M)]. Then A_t=(1−ε)B+εG_t gives A_t(F)≤−δ/2. Thus the sharp boundary does not depend on reconstructing the source's explicit formula for Λ.

## 7. Invertible coordinates and general lower-bounded quadratics

Let h(x)=xᵀQx+bᵀx+c, with Q symmetric positive semidefinite of rank r. It is lower bounded exactly when b belongs to the range of Q: otherwise its restriction along some null vector has nonzero linear slope and is unbounded below. Under the lower-bound condition choose x₀ solving Qx₀=−b/2. Then

    h(x)=(x−x₀)ᵀQ(x−x₀)+c₀.

Orthogonal diagonalization and positive rescaling in the r positive-eigenvalue directions give an invertible affine map Φ with

    h(x)=Φ₁(x)²+⋯+Φᵣ(x)²+c₀.

The remaining d−r coordinates complete the invertible map. Set K_t(q)=L_t(q∘Φ). This preserves normalization, all square tests, finite polynomial-coordinate regularity, and the hierarchy with potential Σ_{i≤r}z_i², since constants cancel. Conversely the affine inverse transports every path back. Both directions preserve P∞, full moment records, representability, determinacy, and the number of whole-path lifts.

Therefore both sharp thresholds depend only on the nullity of Q, for every lower-bounded affine quadratic. Homogeneous positive-semidefinite quadratic forms are the immediate special case b=0. A positive-semidefinite leading matrix alone does not cover an uncontrolled nonzero linear term. No unbounded-below extension is claimed.

More generally this particular classification transports through a supplied polynomial automorphism Φ and its polynomial inverse whenever h=Σ_{i≤r}Φ_i²+C. That is a direct reparameterization of the same hierarchy, not a claim covering all noncoercive polynomials or characterizing their fibres by a quadratic rank.

## 8. Dependency scope, limitations, and executed evidence

The project-relative addition is the sharp nullity≤1 existence versus nullity=0 identification split, including the strict forever-nonmoment discriminator. The backward Taylor bounds, analyticity, single-time de-tilting, exact equivalence relation, and lognormal pair were already established in the bound tensor-realizability packet. They are retained ingredients. The classical d−1 marginal existence theorem supplies the missing threshold step. Hamburger existence supplies the one-dimensional zero-damping edge. The square-positive nonmoment functional is inherited classical input, not newly constructed here. The Gaussian mixture is the parent's strengthening, checked in this packet.

Three evidence scopes remain distinct: the inherited classical full-functional R² counterexample; the newly checked exact mixture built from it; and the explicit genuine full-support lognormal/Gaussian probability pair. The full-functional counterexample is not the neighbouring R³ degree-four truncated functional checked in Lean. That finite truncation and its specified higher-degree continuation cannot supply this premise; the latter fails full PSD. No kernel-checked realization or new formal-kernel claim is made here.

The result concerns one declared finite-dimensional numerical vector and its full commutative polynomial moments. It supplies no finite-degree certification, effective reconstruction algorithm, law-selection rule, noncommutative tensor interpretation, empirical identification claim, or metaphysical conclusion. It does not generalize to an arbitrary generator merely because that generator preserves square positivity. No theorem is inferred from a finite numerical sample.

check_controls.py supplies exact symbolic controls for the SOS expansions, Gaussian killing hierarchy, stationary substitution, mixture normalization and negative witness, strict-decrease formula, lognormal cancellation, affine substitutions, and source-input integrity. The ordinary proofs establish the universal conclusions; the finite controls do not replace Hamburger, Theorem 25, or the imported infinite-dimensional Λ. The author run passed 1,232 exact checks. Run information and results are recorded in CONTROL_RESULTS.json and check_controls.log. Separate independent review, when available, is not part of the author proof.
