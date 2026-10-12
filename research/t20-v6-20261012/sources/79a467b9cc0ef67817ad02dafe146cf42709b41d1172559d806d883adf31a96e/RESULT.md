# Reverse lift for coercive SOS energy-controlled polynomial drift

10 October 2026 UTC. Additive ordinary mathematical research within ACTIVE T20. The earlier squared-energy packet remains frozen and unchanged. The parent proposed the compact-energy localization argument developed here and participated in proof development. The static moment bridge and polynomial sublevel envelope are inherited from separately identified local results. This is an author theorem, not independent review, protected integration, formal-kernel verification, field-priority claim, empirical/noetic identification, or programme closure.

## 1. The broader theorem

Fix finite d≥1 and P=R[x_1,…,x_d]. Let H∈P be coercive and SOS, and b:R^d→R^d polynomial. Assume the polynomial

    S=−b·∇H

is SOS. There is no certificate comparing H or H² to |x|², no coordinate Carleman assumption, and no polynomial-coordinate or characteristic-map assumption.

Suppose L_t:P→R is normalized, full-square-positive and coordinatewise C¹ on a nontrivial interval 0≤t<T, including continuous right derivatives at zero, with

    L'_t(p)=L_t(b·∇p)−L_t(Hp)+L_t(H)L_t(p)            (H)

for every polynomial p. Full-square-positive means L_t(q²)≥0 for every polynomial q. No initial representing law, rank, compact-support or tail bound is assumed.

**Theorem.** The ODE X'=b(X) has a complete forward flow Φ_t. There exists exactly one probability μ with all absolute polynomial moments finite such that the entire supplied path is

    E_t(x)=exp(−∫_0^t H(Φ_s(x))ds),       Z_t=∫E_t dμ,
    L_t(p)=∫p(Φ_t(x))E_t(x)dμ(x)/Z_t.                  (1)

Every positive-time full moment record is determinate. The unnormalized measure ν_t=(Φ_t)_*(E_t μ) satisfies

    ∫exp(tH(y))dν_t(y)≤1,                 t>0.        (2)

Every all-moment initial probability conversely gives a global admitted path. For each fixed valid initial full moment functional, its admitted paths are in bijection with its full representing-law fibre. Different initial laws give different full moment records at every positive time. A supplied nontrivial finite-horizon path has a unique global continuation for these fixed H,b.

Finite initial full Hankel rank r forces the unique r-atomic characteristic evolution with constant rank r, without a full-path rank bound. The finite-time spatial map is a diffeomorphism onto an open image; normalized reweighting followed by this map is injective on initial probabilities. No onto claim or globally complete backward flow is made.

For a coercive polynomial F with H=F+C SOS, b=−∇F satisfies S=|∇F|² SOS, so the theorem covers that Euclidean gradient/selection hierarchy. It also covers b=−B^T B∇F for any polynomial matrix B, with S=|B∇F|². When M=B^T B is pointwise positive definite, the finite-atomic position metric M^(-1), Fisher weight block, and cometric

    L(∇p^T M∇q)+L(pq)−L(p)L(q)

are exactly those proved in the frozen squared-energy packet; that metric calculation did not depend on its radial certificate. Degenerate mobility is not called Riemannian, a pointwise PSD matrix is not silently factorized, and arbitrary energy-controlled b is not called gradient or convergent.

## 2. Inherited ingredients and the actual remaining bridge

The frozen `energy-controlled-gradient-reverse-lift-20261010` already proves the full statement under the stronger SOS certificate H²−c|x|², including the polynomial energy recurrence, noncompact cutoff characteristic uniqueness, initial-law recovery and fibre classification. Its exponential |x| proof of the compact-test PDE cannot be reused under bare coercivity.

The static note `coercive-energy-moment-bridge-20261010/RESULT.md` recognizes that Lemma F of `coercive-square-positivity-20261010/RESULT.md`, §3, already applies to the unweighted energy factorial bound by Cauchy–Schwarz. It supplies positive-time existence. The static compact-sublevel determinacy lemma in `tensor-realizability-extension-20261010/RESULT.md`, §4, supplies uniqueness. Those results and their prior independent reviews are inherited; they are not newly proved representation theorems here.

The polynomial sublevel envelope in `nonconvex-atomic-limit-classification-20261010/RESULT.md`, subsection “A polynomial sublevel envelope”, supplies a rigorous quantitative converse bound for arbitrary coercive polynomials. Its graph/root-bound proof is restated in §7 with its assumptions exposed.

The genuine additional step is §4: polynomial equations imply a compact-test PDE by first localizing in the scalar coercive energy. This avoids coordinate exponential tails, measurable selection of fibre measures, global derivative approximation and an assumed nonlinear transport PDE. Sections 5–8 explicitly requalify the previously proved characteristic, boundary, converse and classification arguments in the broader class.

This is bounded local ancestry, not an exhaustive literature or priority survey. Input bindings and source notes specify the inspected versions. In particular the classical compact algebraic-set moment theorem, Hamburger/Haviland and scalar determinacy ingredients belong to the inherited static argument.

## 3. Positive-time measures before nonpolynomial tests

Set

    a(t)=exp(−∫_0^t L_r(H)dr),       A_t=a(t)L_t,
    Gp=b·∇p−Hp,                    b_n(t)=A_t(H^n).

These are defined at the abstract polynomial level. Then A'_t(p)=A_t(Gp), b_0=a>0 and

    b_0'=−b_1,
    b_n'=−n A_t(H^(n−1)S)−b_(n+1)≤−b_(n+1), n≥1.

H^n and H^(n−1)S are SOS, so every b_n is nonnegative and nonincreasing, and a≤1. The inherited nested-simplex argument from b_0(0)=1 gives

    b_n(t)≤n!t^(−n),               n≥0,t>0.           (3)

No radial comparison is involved in this argument.

For every polynomial q, square-functional Cauchy–Schwarz gives

    0≤A_t(q²H^(2n))
       ≤sqrt(A_t(q⁴)A_t(H^(4n)))
       ≤sqrt(A_t(q⁴))sqrt((4n)!)t^(−2n)
       ≤sqrt(A_t(q⁴))(2n)!(2/t)^(2n).                 (4)

The final inequality is binomial(4n,2n)≤2^(4n). The same positive width t/2 works for every q; only the front constant depends on q. Coercivity makes every level set {H=r} compact. Thus the inherited Lemma F gives a finite positive measure ν_t representing A_t. Its mass is a(t), and ρ_t=ν_t/a(t) represents L_t.

Because H≥0, monotone convergence and (3) imply

    ∫e^(σH)dν_t≤1/(1−σ/t),             0≤σ<t.        (5)

The inherited compact-sublevel determinacy lemma makes ν_t and ρ_t unique. In brief, two full-moment representatives have identical exponentially integrable scalar signed measures H_*(pν−pν') for every polynomial p; their restrictions to compact energy sublevels consequently have identical polynomial integrals and are equal by polynomial uniform approximation. Exhaustion identifies the whole measures. This is joint determinacy without coordinate Carleman or exponential |x| tails.

### Continuity and uniform polynomial-weighted energy tails

On an interior compact interval J=[η,B], a has a positive minimum. Every fixed A_t(R^k), R=|x|², is uniformly bounded by coordinate continuity of the original hierarchy. After representation these moments give tightness and uniform polynomial integrability for ρ_t. The same subsequence argument as in the frozen theorem proves weak continuity: every limit along t_j→t has the prescribed full moments and hence equals the determinate ρ_t. Thus ν is also weakly continuous.

Set ε=η/4. Equation (5) at σ=2ε gives a uniform bound of two. For every polynomial P, actual-measure Cauchy–Schwarz yields

    sup_(r∈J) ∫|P|e^(εH)dν_r
       ≤sqrt(2 sup_(r∈J) A_r(P²))<∞.                (6)

The rate ε is independent of P. This is the key tail estimate used below. It is exponential in H, not necessarily in |x|. All nonpolynomial tests in the rest of the proof are applied to these already established measures.

## 4. Compact-energy localization proves the missing weak PDE

Fix 0<u<v<T in J, extending polynomial functionals and measure pairings complex-linearly when needed. Define the residual functional on compact smooth tests by

    D(φ)=ν_v(φ)−ν_u(φ)−∫_u^v ν_r(b·∇φ−Hφ)dr.       (7)

This is an order-at-most-one distribution. Explicitly its zero-order coefficient is the finite signed measure ν_v−ν_u+∫_u^v Hν_r dr, and its first-derivative coefficients are −∫_u^v b_iν_r dr. They are finite because all polynomial moments are uniformly bounded. Weak continuity and uniform moments make the needed test integrals measurable. Equivalently the integrated signed measures can be defined by bounded functionals on C_0 and the Riesz theorem. We do not yet know D=0.

### 4.1 Polynomial times scalar energy exponentials

For a fixed polynomial p, let P_N(h)=Σ_(j=0)^N(izh)^j/j!. If z is real and |z|<ε/2, then

    |P_N(H)|≤e^(|z|H),       |P'_N(H)|≤|z|e^(|z|H).

The product-generator identity is

    G[pP_N(H)]=(b·∇p−Hp)P_N(H)
                         +p(b·∇H)P'_N(H).           (8)

All its coefficient factors are polynomials. Equation (6) therefore justifies dominated passage from the integrated hierarchy for the polynomial pP_N(H) to

    D(p e^(izH))=0,                    |z|<ε/2.      (9)

Here D on this noncompact function means its explicit integral formula (7), whose three terms are absolutely integrable by (6).

For each fixed p the same formula defines a holomorphic function

    z ↦ D(p e^(izH))

on the connected strip |Im z|<ε/2. On every compact subset of the strip, z differentiation produces only additional polynomial factors H^k and bounded z coefficients, while the exponential absolute value has rate strictly below ε/2. Equation (6), with room between that rate and ε, justifies differentiating the spatial and time integrals. The one-variable identity theorem applied to (9) now gives

    D(p e^(iξH))=0,              every real ξ.        (10)

The continuation is only in the scalar energy variable. No Fourier analyticity in the original coordinate x is claimed.

### 4.2 Scalar Fourier inversion produces smooth energy cutoffs

For each p define finite signed scalar measures

    α_p=H_*(pν_v−pν_u)
             −∫_u^v H_*((b·∇p−Hp)ν_r)dr,
    β_p=−∫_u^v H_*(p(b·∇H)ν_r)dr.                   (11)

These expressions are rigorous signed-measure integrals: their total variations are bounded by the corresponding integrals of absolute polynomial coefficients, which are uniformly finite. One may first define them on C_0(R) and invoke the signed Riesz representation theorem. The weakly continuous measure kernel and polynomial uniform integrability give the requisite measurability; bounded Borel functions then follow by the monotone-class extension. Moreover (6) shows both signed measures have an exponential absolute moment in their scalar argument, since H≥0.

For a smooth scalar χ with compact support, direct use of the product rule gives

    D(pχ(H))=α_p(χ)+β_p(χ').                          (12)

The Fourier expression in (10) is exactly

    α_p(e^(iξh))+iξ β_p(e^(iξh))=0.                  (13)

Because α_p,β_p are finite and ∫(1+|ξ|)|χ̂(ξ)|dξ<∞, ordinary one-dimensional Fourier inversion and Fubini applied to (13) imply

    D(pχ(H))=0                                       (14)

for every polynomial p and every χ∈C_c∞(R). This step converts the scalar exponential identity into compact **energy** localization, not into a conclusion about a selected family of fibre measures.

### 4.3 A compactly supported distribution that kills all polynomials is zero

Fix χ∈C_c∞(R), and form T=χ(H)D, meaning T(φ)=D(χ(H)φ). Coercivity of H makes

    K=H^(-1)(supp χ)

compact. Thus T is an order-at-most-one compactly supported distribution, with an explicit integral representation using χ(H), χ'(H), b, H and the finite measure coefficients of D. Equation (14) says T(p)=0 for every polynomial p; evaluation on noncompact p is well defined because T has compact support.

For any ξ∈R^d, multivariate-coordinate exponential Taylor polynomials

    Q_N(x)=Σ_(j=0)^N(iξ·x)^j/j!

converge to e^(iξ·x), together with their first derivatives, uniformly on K. Multiplication by χ(H) and its fixed smooth derivative preserves this uniform convergence on the common compact support. The explicit order-one bound for T therefore yields

    T(e^(iξ·x))=lim_N T(Q_N)=0.

For φ∈C_c∞(R^d), Fourier inversion is valid under T: its exponential test bound is at most a fixed constant times 1+|ξ|, and φ̂ is rapidly decreasing. Hence T(φ)=0. This proves T=0 by elementary compact Fourier approximation, with no unproved global C¹ approximation claim.

Finally, given any φ∈C_c∞, choose scalar χ∈C_c∞ equal to one on a neighborhood of the compact set H(supp φ). Then χ(H)φ=φ, including their derivatives, so

    D(φ)=T(φ)=0.

We have proved the missing compact-test equation

    ν_v(φ)−ν_u(φ)=∫_u^v ν_r(b·∇φ−Hφ)dr             (15)

for every compact smooth φ and every 0<u<v<T. The integrand is continuous by weak continuity and compact support. Consequently ν solves the actual weak PDE

    ∂_tν=−div(bν)−Hν

on positive times. This concludes the genuinely new bridge; static determinacy alone was not substituted for it.

## 5. Characteristics: what must be requalified in the broader class

Along each local characteristic, H'=−S≤0. Coercivity makes its fixed energy sublevel compact, so polynomial ODE local existence and uniqueness extend the trajectory through every finite forward time. This argument needs only compact sublevels, not a radial growth rate.

Smooth local ODE dependence, local backward uniqueness along existing trajectories and the nonzero variational determinant show Φ_t is a diffeomorphism onto its open image, exactly as in the frozen proof. No global backward flow is assumed.

The weight E_t lies in (0,1] and satisfies the usual cocycle. For fixed 0<s<t and f∈C_c∞ define

    U(r,x)=E_(t−r)(x)f(Φ_(t−r)(x)).

It is smooth on compact sets, bounded by ||f||∞, and solves

    ∂_rU+b·∇U−HU=0.

The time-dependent compact-test rule follows from (15) by the same difference-quotient argument as before. With χ_N(x)=χ(x/N), a spatial cutoff, this gives exactly

    dν_r(χ_N U)/dr=ν_r(U b·∇χ_N).

If |b(x)|≤K(1+|x|^m), choose an even q>m+1. Uniform boundedness of ν_r(|x|^q) on [s,t] follows from polynomial coordinate continuity; no exponential coordinate tail is needed. The cutoff error is at most a constant times

    ||f||∞ N^(m−q−1) sup_(r∈[s,t])ν_r(|x|^q)→0.

Thus the frozen cutoff proof requalifies completely and yields

    ν_t=(Φ_(t−s))_*[E_(t−s)ν_s],       0<s<t<T.        (16)

The cancellation is performed before removing the cutoff, so no global derivative-U estimate or compact inverse-flow support is introduced. This establishes the weighted measure-level evolution and excludes an additional interior inflow within the admitted class.

## 6. Initial recovery and selected-law uniqueness

Near zero all original radial moment coordinates L_r(R^k) are uniformly bounded for each fixed k. Thus ρ_r is tight as r↓0. Choose one weakly convergent subsequence ρ_(s_j)→μ with s_j↓0. The limiting probability has all polynomial moments, and uniform higher radial moments identify

    ∫p dμ=L_0(p)

for every polynomial p. Since a(s_j)→1, ν_(s_j) has the same weak limit. This is initial representability, not initial determinacy.

For fixed t>0 and compact smooth f, E_(t−s_j)f∘Φ_(t−s_j) is uniformly bounded and converges locally uniformly to E_t f∘Φ_t. Tightness and (16) therefore give

    ν_t=(Φ_t)_*(E_t μ)

using the same subsequence for every fixed t. Taking masses identifies a(t)=Z_t and proves (1).

The inverse spatial map on the open image and strict positivity of E_t recover μ from any one positive-time unnormalized output. For normalized outputs they recover proportional input probabilities, whose total masses force equality. Therefore the selected initial law is unique, all candidate boundary limits agree, and no extra boundary inflow survives the tight initial recovery. Neither reciprocal weights nor inverse flow are assumed bounded on their images; equality is applied to actual positive measures in the established range.

Since H decreases along every trajectory,

    ∫_0^tH(Φ_s(x))ds≥tH(Φ_t(x)),

which proves (2) after characteristic identification. This endpoint exponential energy estimate is not obtained by evaluating the geometric-series bound (5) at its divergent endpoint.

## 7. Polynomial sublevel growth supplies the full converse

For clarity, mere smooth properness would not by itself give the polynomial initial-coordinate domination needed here. Polynomiality of the coercive energy supplies it through the following inherited graph/root-bound argument.

Let h_*=min H≥0 and define

    M(s)=max{1+|y|²:H(y)≤h_*+s},       s≥0.

The maximum is attained and finite, and M is nondecreasing. Its graph has a first-order polynomial description asserting an attaining point and the upper bound for every point of the sublevel. Tarski–Seidenberg makes the graph semialgebraic.

Take a quantifier-free graph description involving finitely many nonzero polynomials. At each graph point at least one must vanish; otherwise all signs would be locally constant and the graph would contain an open neighborhood, which the graph of a function cannot. The product P(s,u) of these nonzero polynomials is nonzero and satisfies P(s,M(s))=0. Its u-degree is positive, since a nonzero polynomial in s alone cannot vanish for every s≥0.

Write P(s,u)=a_d(s)u^d+…+a_0(s). Beyond the finitely many real roots of its nonzero leading coefficient, Cauchy's elementary polynomial root bound gives

    M(s)≤1+max_(i<d)|a_i(s)/a_d(s)|≤K(1+s)^N

for some finite integer N and K>0. Ratios of fixed univariate polynomials have at most polynomial growth at infinity. Monotonicity handles the remaining compact s interval after enlarging K. Thus

    1+|y|²≤K(1+H(y))^N                       for all y. (17)

No optimal exponent or computed coercivity modulus is claimed. This is the separately derived inherited envelope; the semialgebraic projection/quantifier facts are recorded in Kurdyka, *On gradients of functions definable in o-minimal structures*, §1, pp.771–772, primary journal PDF https://aif.centre-mersenne.org/item/10.5802/aif.1638.pdf . The elementary root-bound deduction is written above.

Along the energy-decreasing flow, (17) gives

    1+|Φ_t(x)|²≤K(1+H(x))^N.

The right side is bounded by a polynomial in |x|. For each polynomial p and Gp=b·∇p−Hp, both p(Φ_t(x)) and Gp(Φ_t(x)) are therefore bounded by a fixed polynomial in |x|, uniformly in finite time windows, indeed uniformly for t≥0 after choosing that polynomial. Since E_t≤1, an all-moment initial μ supplies an integrable dominating function.

Differentiation under μ yields ν'_t(p)=ν_t(Gp), continuously through zero with the right derivative. The strictly positive mass satisfies Z'_t=−ν_t(H). Normalization gives (H), and positive-law square tests are automatic. This proves the full global converse under bare coercivity, not a converse conditional on an unproved radial growth rate.

## 8. Classification and a genuinely beyond-H² control

The reverse direction and global converse identify admitted paths with all-moment initial laws. Restricting to an initial moment functional gives its full representing-law fibre. Joint positive-time determinacy, proved before the PDE, and normalized finite-time injectivity show different laws in one initial fibre give different full records at every positive time. A supplied path selects one law and therefore extends uniquely even when its initial moment functional is indeterminate. Finite initial full rank gives a unique finite-atomic law, whose positive weights and injectively moved atoms preserve full rank at every finite time.

For an explicit case outside the frozen squared-energy theorem, set

    u=x−y³,      F=u²+y²,      H=1+F,
    b=−∇F,      S=|∇F|²=4u²+(−6y²u+2y)².            (18)

H and S are explicit SOS. H is coercive: bounded H bounds y and u, hence x=u+y³. More quantitatively,

    x²+y²≤2u²+2y⁶+y²≤3H+2H³.

For any c>0 and any finite C, along x=y³ the prospective old squared-energy comparison is

    (F+C)²−c(x²+y²)=(y²+C)²−c(y⁶+y²),

whose degree-six leading coefficient is −c. It is eventually negative and cannot be SOS. Thus no additive shift rescues the frozen H² hypothesis in these coordinates. The theorem proved here does apply through compact-energy localization, without treating the static automorphism (x,y)↦(u,y) as the gradient characteristic map.

No larger example campaign is needed: (18) witnesses the exact removed hypothesis. The proof still requires H SOS and S SOS. It does not yet cover every coercive polynomial energy without an SOS shift, arbitrary merely pointwise energy-decreasing drift, finite square-test data, or arbitrary diffusion. There is no universal convergence claim for nongradient b; the inherited rotation control already disproves one.

## 9. Evidence and limits

The finite exact controls in this packet target the new product-generator/localization identities, the scalar α/β sign, the compact-distribution product rule, the inherited envelope root-bound mechanism in representative algebraic cases, and the m=3 exclusion. Integrity checks verify the frozen narrow packet and all declared inputs. Replaying an inherited identity is a regression check, not a newly discovered theorem or independent verification of its analytic proof.

The universal argument is ordinary written mathematics. Finite symbolic controls do not formalize the representation theorem, prove holomorphic continuation by enumeration, or reconstruct a general measure. No independent-review verdict, protected integration, programme closure, field priority, empirical/noetic identity or stable finite-data algorithm is asserted by this author packet.
