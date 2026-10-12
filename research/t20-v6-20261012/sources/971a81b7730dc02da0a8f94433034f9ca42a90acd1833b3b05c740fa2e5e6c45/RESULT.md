# Unrestricted-rank reverse lift from a coercive SOS energy

10 October 2026 UTC. Additive ordinary mathematical research within ACTIVE T20. The parent proposed the energy-power route, the squared-energy coercivity certificate, and the curved-valley discriminator, and participated in the proof development. The compact-gradient investigator also proposed the noncompact cutoff and Fourier continuation repairs. This is an author proof, not independent review, protected integration, formal-kernel verification, field-priority claim, empirical/noetic identification, or programme closure. All hash-bound predecessor files remain unchanged.

## 1. The theorem and its exact scope

Fix d≥1, P=R[x_1,…,x_d], R(x)=|x|², a real polynomial F, a constant C∈R and c>0. Assume both polynomials

    H=F+C,                 Q=H²−cR                         (S)

are sums of squares of real polynomials. A zero summand is permitted. In particular H≥0 and H≥sqrt(c)|x| pointwise, so F is coercive. There is no radial dissipativity hypothesis.

Let 0<T≤∞ and L_t:P→R be real linear functionals for 0≤t<T. Assume coordinatewise C¹ dependence, including continuous right derivatives at zero, and for every p,q∈P at every supplied time,

    L_t(1)=1,               L_t(q²)≥0,
    L'_t(p)=−L_t(∇F·∇p)−L_t(Fp)+L_t(F)L_t(p).          (H)

There is no initial representing-law, rank, compact-support, or moment-growth assumption. All polynomial equations and all square tests, not a finite truncation, are required.

**Theorem.** The polynomial ODE X'=−∇F(X) has a global forward flow Φ_t. There is exactly one Borel probability μ on R^d with all absolute polynomial moments finite such that the entire supplied path is

    E_t(x)=exp(−∫_0^t H(Φ_s(x))ds),       Z_t=∫E_t dμ,
    L_t(p)=∫p(Φ_t(x))E_t(x)dμ(x)/Z_t,     0≤t<T.       (1)

At zero Φ_0=id, E_0=1 and Z_0=1. Replacing H by F multiplies E_t and Z_t by e^(Ct), so the normalized formula is unchanged.

Every positive-time full moment record is determinate. If ν_t=(Φ_t)_*(E_t μ), then after identification the endpoint energy bound is

    ∫exp(tH(y))dν_t(y)≤1,
    ∫exp(t sqrt(c)|y|)dν_t(y)≤1,             t>0.       (2)

The normalized law has the corresponding bounds divided by Z_t>0. It is carried by the open image O_t=Φ_t(R^d), and Φ_t is a diffeomorphism onto that image. Neither bounded image nor global backward completeness is asserted.

Conversely every probability with all absolute polynomial moments generates such a path globally for t≥0. For any fixed valid initial full moment functional, its admitted paths are in bijection with its entire representing-law fibre. Distinct initial laws in that fibre give different full moment records at every positive time. A supplied path on any nontrivial horizon has a unique global continuation under this fixed F.

In particular, finite initial full Hankel rank r forces the unique r-atomic gradient/selection evolution with constant full rank r, without a future rank hypothesis. The theorem establishes measure dynamics for arbitrary initial laws, and uses the inherited genuine finite-atomic gradient metric when the initial law is finite; it does not claim an infinite-dimensional smooth Riemannian manifold.

## 2. Ancestry and the actual increment

INPUT_BINDINGS.json binds the directly inspected predecessors and the inherited primary-source record. The bounded local scan is retained in DEDUP_SCAN.json.

- The radial-quartic and SOS-dissipative-gradient reverse-lift packets already remove rank for their respective compactifying gradient classes. The latter requires F+C SOS and x·∇F−κR²+λR+D SOS with κ>0, λ,D≥0. Its positive-time measures have common compact supports on interior time windows. The present energy certificate permits curved valleys that fail that radial condition.
- The diffusion packet already separates abstract moment growth, representation, actual PDE identification, and tight initial recovery. Its Gaussian tails justify Fourier Taylor passage at every frequency; our initial bound gives only exponential |x| tails, requiring an additional analytic-continuation step.
- The polynomial-transport packet covers supplied bounded-degree polynomial automorphism flows under a different pulled-back killing certificate. A general gradient flow here need not be polynomial or onto, so that theorem is not a direct substitute.
- The complete-flow finite-rank packet already proves characteristic lifting with forward completeness and lower-bounded killing under a locally uniform full-path rank bound. The joint-atomic-gradient packet supplies the finite-atomic metric. Those results are inherited, not new here.
- The coercive-square-positivity packet handles all coercive polynomial **pure killing** by a different scalar/fibre argument. Its central even-time-derivative identity does not persist after nonlinear gradient transport and is not silently reused.
- The transport escape/inflow countercontrols remain applicable outside the present hypotheses. Tightness and smooth moments alone are not being declared sufficient for arbitrary transport.

The new bridge is energy-power monotonicity before representation, followed by noncompact polynomial-to-PDE passage and a bounded weighted characteristic test with a vanishing spatial-cutoff error. The sequence of proof matters: nonpolynomial tests are used only after actual positive measures have been obtained.

The specialized existence input is the classical Nussbaum–Carleman theorem, as stated in Putinar–Schmüdgen, *Multivariate Determinateness*, Theorem 25 and its following Nussbaum attribution, printed p.24, https://arxiv.org/pdf/0810.0840v1 . It starts from a positive-semidefinite multisequence; all coordinate Carleman conditions give existence and determinacy. The pinned source and p.24 extraction were inspected and hash-bound, and the primary-web theorem statement was checked. In d=1 use Hamburger existence and Carleman uniqueness. No general unbounded-coefficient transport uniqueness theorem is imported.

## 3. Energy powers come down from arbitrary initial moments

Everything in this section is algebra on the abstract functionals. Define

    a(t)=exp(−∫_0^t L_s(H)ds),
    A_t(p)=a(t)L_t(p),       b_n(t)=A_t(H^n), n≥0.

Coordinate continuity makes a well-defined and strictly positive on every finite supplied interval, with a(0)=1. Since ∇H=∇F, unnormalization gives

    A'_t(p)=A_t(Gp),       Gp=−∇H·∇p−Hp.              (3)

Products and powers of SOS polynomials are SOS: (Σf_i²)(Σg_j²)=Σ_(i,j)(f_i g_j)². Therefore H^n and H^(n−1)|∇H|² are SOS for their indicated nonnegative powers. In particular b_n≥0, and the exact energy recurrence is

    b_0'=−b_1,
    b_n'=−n A_t(H^(n−1)|∇H|²)−b_(n+1)≤−b_(n+1),
                                                   n≥1. (4)

Thus every b_n is nonincreasing and 0<b_0=a≤1. Neither pointwise nonnegativity alone nor positivity on arbitrary nonnegative polynomials is used.

For 0≤s<t<T, integrate (4), discard only nonnegative endpoint terms, and repeat from indices 0 through n−1. This gives

    b_0(s)≥∫_(s≤u_1≤…≤u_n≤t) b_n(u_n)du_1…du_n
           ≥(t−s)^n b_n(t)/n!.

The last inequality uses the already proved monotonicity of b_n. Set s=0 and b_0(0)=1:

    0≤b_n(t)≤n! t^(−n),        n≥0, t>0.              (5)

For n=0 this is a≤1. Only first derivatives and finite repeated integrations are needed. Zero moments cause no root differentiation or division.

## 4. SOS comparison forces positive-time vector measures

For n≥1 the exact factorization

    H^(2n)−(cR)^n
      =Q Σ_(j=0)^(n−1) H^(2(n−1−j))(cR)^j             (6)

is SOS. Every term in its right factor is SOS, and Q is SOS. Hence, still before any measure,

    0≤A_t(R^n)≤c^(−n)b_(2n)(t)
                    ≤c^(−n)(2n)!t^(−2n).             (7)

Also R^n−x_i^(2n) is SOS by the multinomial expansion. Thus

    0≤L_t(x_i^(2n))≤a(t)^(−1)c^(−n)(2n)!t^(−2n).

Since (2n)!≤(2n)^(2n), each nonzero Carleman term is at least

    [L_t(x_i^(2n))]^(−1/(2n))
                 ≥a(t)^(1/(2n))sqrt(c)t/(2n).

The factor a(t)^(1/(2n)) tends to one. Every coordinate Carleman series therefore diverges; zero even moments use the standard infinite-term convention. Nussbaum–Carleman gives a unique representing probability ρ_t for L_t at every t>0. Put ν_t=a(t)ρ_t, the unique finite positive measure representing A_t. Only now do we use measure tests.

Because H≥0, (5) and monotone convergence show for 0≤σ<t,

    ∫exp(σH)dν_t = Σ_(n≥0) σ^n b_n(t)/n!
                  ≤1/(1−σ/t).                        (8)

In particular, on an interior compact time interval J=[η,B] with η>0, set δ=sqrt(c)η/2. Since H≥sqrt(c)|x|,

    sup_(r∈J) ∫exp(δ|x|)dν_r≤2.                      (9)

Every fixed polynomial absolute moment is therefore uniformly bounded on J. At this stage (8) is asserted only for σ<t. The stronger endpoint estimate (2) will follow from the identified dynamics, not by summing a divergent endpoint bound.

### Weak continuity is derived, not assumed

On J, a has a positive minimum. Equation (7) gives uniform radial moments for the probabilities ρ_r. If r_j→r∈J, these probabilities are tight, so each subsequence has a weakly convergent further subsequence. Uniform higher radial moments make every polynomial uniformly integrable along such a subsequence. Its limit represents L_r by coordinate continuity and has all polynomial moments. Positive-time determinacy identifies that limit with ρ_r. Thus the whole sequence converges to ρ_r. This proves weak continuity of ρ and of ν on J. It also establishes the measurability needed for time integrals; no unexplained selection of representatives is made.

## 5. The polynomial hierarchy yields the noncompact weak PDE

Fix 0<u<v<T and an interior compact interval J containing [u,v], with δ as in (9). All equations below are extended complex-linearly where needed.

### 5.1 Fourier tests first near zero

For ξ∈R^d with |ξ|<δ/2 define

    P_N(x)=Σ_(j=0)^N (iξ·x)^j/j!.

Then P_N→e^(iξ·x) and ∇P_N→iξ e^(iξ·x) pointwise, while

    |P_N|≤e^(|ξ||x|),
    |∇P_N|≤|ξ|e^(|ξ||x|).

Since b=−∇H and H are polynomials, (|b||ξ|+H)e^(|ξ||x|) is bounded by a constant times e^(δ|x|). The strict frequency inequality leaves room to absorb every fixed polynomial factor. Equation (9) and dominated convergence, first under each ν_r and then in time, pass the integrated polynomial identity to

    ν_v(e^(iξ·x))−ν_u(e^(iξ·x))
       =∫_u^v ν_r((ib·ξ−H)e^(iξ·x))dr.               (10)

Measurability of the unbounded continuous integrands follows by bounded continuous cutoffs and weak continuity; the same bounds justify the limits. Unlike the Gaussian-tail argument in the diffusion predecessor, this Taylor argument has only a guaranteed small-frequency range.

### 5.2 Analytic continuation supplies every real frequency

Fix any nonzero ξ_0∈R^d. For a complex scalar z define the residual

    D(z)=ν_v(e^(izξ_0·x))−ν_u(e^(izξ_0·x))
            −∫_u^v ν_r((iz b·ξ_0−H)e^(izξ_0·x))dr.

It is holomorphic in the connected strip

    |Im z|<δ/(2|ξ_0|).

Indeed on each compact subset of that strip, differentiating any finite number of times in z introduces only fixed polynomial factors in x, while the exponential absolute value has rate strictly below δ/2. Those factors are dominated by a constant times e^(δ|x|), uniformly in r∈J; (9) justifies differentiation under space and time integrals. Thus the holomorphic claim is at the level of actual finite measures with a proved uniform exponential bound.

By (10), D(z)=0 for real z in a neighborhood of zero. The one-variable holomorphic identity theorem gives D≡0 throughout the strip, in particular D(1)=0. Since ξ_0 was arbitrary and ξ=0 is already the polynomial mass equation, (10) holds for all ξ∈R^d. We never claim that the original Taylor polynomials converge integrably at arbitrary frequencies.

### 5.3 Compact tests and their time-dependent rule

For φ∈C_c∞(R^d), its Fourier transform satisfies

    ∫(1+|ξ|)|φ̂(ξ)|dξ<∞.

The uniform polynomial moments in (9) bound ν_r(|b|+H) on [u,v], so Fourier inversion and Fubini applied to (10) give

    ν_v(φ)−ν_u(φ)=∫_u^v ν_r(b·∇φ−Hφ)dr.            (11)

The integrand is continuous because b·∇φ−Hφ is bounded continuous with compact support and ν is weakly continuous. Thus each such pairing is C¹ and ν solves the actual weak equation

    ∂_tν=−div(bν)−Hν                                  (12)

on positive times.

If ψ_r is smooth in x and C¹ in r with common compact support and the needed derivatives continuous uniformly there, splitting a difference quotient into the change of test and the change of measure gives

    dν_r(ψ_r)/dr=ν_r(∂_rψ_r+b·∇ψ_r−Hψ_r).            (13)

Uniform time differentiation and bounded masses handle the changed-test term; weak continuity and (11) handle the frozen-test term. This rule is proved after (11), rather than fed into an unrepresented polynomial functional.

## 6. Forward completeness and the correct weighted characteristic test

Along every local solution of X'=−∇H(X),

    dH(X(t))/dt=−|∇H(X(t))|²≤0.

The certificate implies

    |X(t)|≤H(X(t))/sqrt(c)≤H(X(0))/sqrt(c).             (14)

Thus each forward trajectory stays in a compact energy sublevel. A smooth polynomial vector field is bounded and locally Lipschitz there. If a finite terminal time existed, the trajectory would have a finite endpoint and local ODE existence would extend it. Hence Φ_t is defined for every t≥0 and every finite starting point.

Smooth ODE dependence is available on every compact forward time-space neighborhood. Local backward uniqueness along two existing finite trajectories proves injectivity of Φ_t: trajectories meeting at t must have identical histories back to zero. This does not assume global backward completeness. Its derivative J_t solves J'_t=Db(Φ_t)J_t with J_0=I, so

    det J_t=exp(∫_0^t div b(Φ_s(x))ds)>0.

The inverse function theorem and injectivity make Φ_t a smooth diffeomorphism onto its open image O_t. It need not be onto R^d.

The weight in (1) is smooth on compact time-space sets, satisfies 0<E_t≤1, and obeys

    Φ_(r+s)=Φ_r∘Φ_s,
    E_(r+s)(x)=E_s(x)E_r(Φ_s(x)).                     (15)

Fix 0<s<t<T and f∈C_c∞. The globally defined forward-flow backward test is

    U(r,x)=E_(t−r)(x)f(Φ_(t−r)(x)),       s≤r≤t.

It is smooth on compact sets, |U|≤||f||∞, and differentiating (15) at a short initial step gives

    ∂_rU+b·∇U−HU=0.                                  (16)

The support of U need not be compact; the inverse flow may fail to exist for arbitrary points over a full backward interval. Neither is a problem because U uses only the complete forward flow.

Choose χ∈C_c∞ with 0≤χ≤1, χ=1 for |x|≤1 and χ=0 for |x|≥2, and let χ_N(x)=χ(x/N). Apply (13) to ψ_r=χ_N U. Exact cancellation in (16) leaves only

    dν_r(χ_N U)/dr=ν_r(U b·∇χ_N).                    (17)

No global bound on ∇U or its higher derivatives is required: for each N the test is compactly supported, and these derivatives cancel before the limit. Let m≥0 and K satisfy |b(x)|≤K(1+|x|^m). On N≤|x|≤2N, |∇χ_N|≤K_χ/N. If q is an even integer greater than m+1, then the uniform q-th radial moment on [s,t] gives

    sup_(r∈[s,t]) |ν_r(U b·∇χ_N)|
           ≤K' ||f||∞ N^(m−q−1)
                         sup_(r∈[s,t])ν_r(|x|^q)
              →0.                                    (18)

Here N≥1 absorbs the constant in 1+|x|^m. One can equally use the stronger exponential tail bound, but fixed sufficiently high moments already suffice.

Integrate (17), send N→∞ using (18), and use bounded convergence at s and t. Since U(t,x)=f(x),

    ν_t(f)=ν_s(E_(t−s) f∘Φ_(t−s)).

Compact smooth tests determine finite measures. Therefore

    ν_t=(Φ_(t−s))_*[E_(t−s)ν_s],       0<s<t<T.         (19)

This is the actual weighted characteristic uniqueness statement in the admitted moment/tail class. It excludes an additional interior inflow. The lower killing bound H≥0 is used through |U|≤||f||∞; polynomial transport growth and uniformly bounded high moments remove the spatial boundary error. Compact inverse-flow supports or unproved global derivative estimates are not premises.

## 7. Tight initial recovery and uniqueness of the selected law

Coordinate continuity near zero bounds L_r(R^k) uniformly for every fixed k on a short interval. The represented probabilities ρ_r, r>0, are consequently tight as r↓0. Choose one sequence s_j↓0 with ρ_(s_j) converging weakly to a probability μ. Since a(s_j)→1, ν_(s_j) has the same weak limit.

Lower semicontinuity gives every radial moment of μ finite. For a polynomial p of degree m, choose 2k>m. Outside |x|≤N, N≥1,

    |p(x)|≤C_p(1+|x|^m)≤2C_p N^(m−2k)|x|^(2k).

The uniform higher moments make p uniformly integrable along the sequence. Compact cutoffs, weak convergence and coordinate continuity imply

    ∫p dμ=lim_j L_(s_j)(p)=L_0(p).                    (20)

Thus the initial functional is represented. This is not an assertion that it is determinate.

Fix t>0 and f∈C_c∞. The functions

    g_j(x)=E_(t−s_j)(x)f(Φ_(t−s_j)(x))

are bounded by ||f||∞ and converge locally uniformly to the bounded continuous g(x)=E_t(x)f(Φ_t(x)). Tightness of ν_(s_j) handles the complement of a fixed compact set; local uniform convergence and weak convergence handle that compact set. Passing (19) along this one fixed sequence yields

    ν_t=(Φ_t)_*(E_t μ),       0<t<T.                  (21)

The same μ works for each fixed t; no time-dependent sequence is chosen. Taking total masses gives a(t)=Z_t, and (20) supplies time zero. Formula (1) is proved.

For a fixed t>0, Φ_t has a continuous inverse on O_t and E_t(x)>0 at every finite x. Thus the transformation μ↦(Φ_t)_*(E_t μ) is injective on finite input measures: inverse-pushforward recovers E_t μ, and division by the strictly positive Borel weight recovers μ. The reciprocal need not be bounded; equality of two known measures can be integrated against it, and finiteness holds for actual inputs.

The normalized map is injective on probabilities as well. Equality of normalized outputs gives E_t μ/Z_μ=E_t μ'/Z_μ' after inverse-pushforward, hence μ/Z_μ=μ'/Z_μ'. Total masses force the proportionality constant to be one. Therefore every possible tight boundary limit is the same selected μ, and no independent boundary law enters from infinity. The image concentration ν_t(O_t)=a(t) follows directly from (21), without any assertion that O_t is bounded or has a prescribed boundary.

Finally H decreases on each characteristic, so

    ∫_0^t H(Φ_s(x))ds≥tH(Φ_t(x)).

Multiplying this inequality into the weight and integrating against μ yields

    ∫exp(tH(y))dν_t(y)
      =∫exp(tH(Φ_t(x))−∫_0^tH(Φ_s(x))ds)dμ(x)≤1.

This proves the endpoint bound (2), only after (21) has been established.

## 8. Converse, fibre classification, and finite initial rank

Let μ have all absolute polynomial moments. Formula (14) bounds every forward position by the polynomial H(x)/sqrt(c) in its initial position, and 0<E_t≤1. For every polynomial p, both p(Φ_t(x)) and (Gp)(Φ_t(x)) are therefore bounded in absolute value by a fixed polynomial in |x|, uniformly on any finite forward time window, indeed uniformly in t≥0 if its coefficients are enlarged once. That polynomial is μ-integrable.

Pointwise differentiation gives

    d[p(Φ_t(x))E_t(x)]/dt=(Gp)(Φ_t(x))E_t(x).

Dominated differentiation and continuity give C¹ moment coordinates through t=0, with the right derivative there, and

    ν'_t(p)=ν_t(Gp),           Z'_t=−ν_t(H).

The mass Z_t is strictly positive because E_t is pointwise strictly positive. Normalization produces exactly (H), with full square positivity automatic from the positive probability law. This constructs the global converse from every all-moment initial law, without an initial tail bound.

Reverse lifting and this converse give the claimed bijection. For a fixed initial moment functional, all its representing probabilities have all absolute polynomial moments and give admitted paths. If two such laws differed but their positive-time full records agreed, positive-time determinacy would identify the output laws; normalized-map injectivity would then identify the inputs, a contradiction. Thus different members of an indeterminate initial fibre yield different records at every positive time, while a determinate initial record gives a unique path. A given nontrivial path already selects one μ, so its continuation is unique even when L_0 alone is indeterminate.

If the initial full Hankel rank is finite r, the inherited finite GNS theorem gives its unique r-atomic law. Formula (1) transports its distinct atoms by injective Φ_t and gives strictly positive normalized weights. Thus the full rank stays r. This is a conclusion from finite **initial** rank, not the earlier finite-full-path-rank assumption or a fixed truncated-rank surrogate.

For every represented path,

    dL_t(F)/dt=−L_t(|∇F|²)−[L_t(F²)−L_t(F)²]≤0.

For finite laws the inherited metric Σ_j u_j²/w_j+Σ_j w_j|v_j|² on Σ_j u_j=0 makes these same weight and position equations the genuine negative gradient of Σ_jw_jF(x_j). That metric theorem is credited to its predecessor. No global-minimizer convergence or infinite-dimensional smooth metric is inferred merely from energy decrease.

## 9. Curved-valley discriminator

In d=2 put

    u=x−y²,        F(x,y)=u²+y²,        H=F+1,
    R=x²+y²,       c=1.

H=1²+u²+y² is SOS, and the exact identity is

    H²−R=1+u⁴+u²+2y²(u−1/2)²+y²/2.                  (22)

Each displayed term is a polynomial square with a nonnegative coefficient, so (S) holds. In particular H≥sqrt(R), giving coercivity even along its curved valley.

The radial derivative is

    x∂_xF+y∂_yF=2u²−2uy²+2y².                       (23)

Along u=2, equivalently x=y²+2, it equals 8−2y² and is unbounded below. More precisely, for every κ>0 and any finite λ,D, the candidate old radial certificate along this curve is

    8−2y²−κ[(y²+2)²+y²]²+λ[(y²+2)²+y²]+D.

Its leading coefficient in y is −κ at degree eight. It is negative for sufficiently large |y| and therefore cannot be SOS. This falsifies the prior quartic-radial-dissipativity hypothesis even when its λR and D allowances are present.

The weaker linear energy domination also fails: for any c'>0 and any finite additive constant C', along x=y²,

    F+C'−c'R=y²+C'−c'(y⁴+y²)→−∞.

Thus no shifted F−c'R SOS comparison is available. This example requires the squared-energy comparison rather than the Gaussian-tail H−cR route. No closed-form flow is needed or asserted; its complete forward gradient flow follows from the proved energy sublevel argument.

The pointwise radial derivative may be negative because Euclidean radius can increase while F decreases. There is no contradiction with gradient energy dissipation. Nor does this packet reclassify this one example as all coercive polynomial gradients: the explicit certificates remain hypotheses.

## 10. Boundary controls and evidence limits

The present theorem does not imply compact positive-time support. For example, F=R and H=R+1 satisfy H SOS and H²−R=R²+R+1 SOS. Their flow is Φ_t(x)=e^(−2t)x, a diffeomorphism onto all R^d. Starting from a full-support Gaussian, the positive weight E_t leaves full support at every finite time. This example is an inherited affine case used only to refute an unjustified compactification claim.

The curved-valley certificate excludes the prior dissipative theorem's hypotheses, but no claim is made that the entire new class contains every member of that prior certificate class. Bare coercivity, arbitrary pointwise nonnegativity without SOS, or finite square-test data are not proved sufficient here. The pure-killing theorem for all coercive polynomials is a different result and is not generalized wholesale by this argument.

A useful Fourier boundary control is the probability density e^(−|x|)/2 on the line. Its even moments are (2n)! and its characteristic function is 1/(1+ξ²). Its Taylor series at zero is Σ_n(−ξ²)^n, which fails already at ξ=2. Thus a mere exponential |x| tail cannot justify global-frequency polynomial Taylor passage; §5.2 repairs a real gap rather than adding a redundant step.

The proof supplies no stable numerical reconstruction, finite-grade certificate, finite observation guarantee, formal proof-kernel check, philosophical/noetic identity, or empirical conclusion. The exact symbolic controls verify finite instances of the identities and key discriminator algebra; they do not establish the universal measure-existence or analytic-continuation theorem by enumeration. Their executed result, input preservation, and frozen author digests are recorded beside this file.

## 11. Same-proof corollary: energy-controlled polynomial drift

The proof is not specific to the Euclidean gradient once its energy derivative has the required SOS sign. Here is the exact additional result, rather than an implicit broadening of (H).

Let H∈P and b:R^d→R^d be polynomial, and assume for some c>0 that

    H is SOS,      H²−cR is SOS,      S=−b·∇H is SOS.  (D)

Suppose normalized full-square-positive coordinatewise C¹ functionals satisfy

    L'_t(p)=L_t(b·∇p)−L_t(Hp)+L_t(H)L_t(p)            (HD)

on a nontrivial [0,T), with the same endpoint regularity. Then every conclusion of §1 concerning existence, unique initial-law selection, positive-time determinacy, characteristic representation, exponential energy/norm bounds, global converse, fixed-initial-law fibres, unique continuation, open-image injectivity and finite-initial-rank preservation holds for the forward flow X'=b(X) and the killing H. No gradient, variational or convergence conclusion is included for arbitrary b.

The proof changes are exhaustively specified:

1. Unnormalization is unchanged, with Gp=b·∇p−Hp. The exact recurrence is

       b_n'=−n A_t(H^(n−1)S)−b_(n+1),    n≥1,
       b_0'=−b_1.

   Every subtracted polynomial is SOS by (D). Thus §§3–5, including the factorial bound, representation, weak continuity, analytic continuation and weak PDE, remain valid verbatim with this polynomial b.
2. Along the ordinary characteristic, H'=b·∇H=−S≤0. Therefore (14) and compact-sublevel forward completeness hold exactly as before. The proof of injectivity uses local ODE uniqueness, not a gradient property.
3. The weight still lies in (0,1], the cocycle and backward equation still hold, and the cutoff proof (17)–(19) uses only polynomiality of b and uniform moments. Hence §7 recovers and uniquely identifies the initial law. H monotonicity again proves the endpoint bound (2).
4. Polynomiality of b and the forward position bound (14) dominate Gp in initial coordinates, proving the global converse and fibre/rank conclusions of §8. The energy identity becomes

       L'_t(H)=−L_t(S)−[L_t(H²)−L_t(H)²]≤0.

These observations prove the corollary; they do not merely conjecture an analogous result. They also explain why an SOS certificate for S is needed before representation: pointwise b·∇H≤0 alone cannot be inserted into a general square-positive abstract functional.

### A nongradient, nonconvergent control

Take d=2, H=1+x²+y², b=(−y,x), c=1. Then H²−R=1+R+R² is SOS and S=0. Starting from a nonzero Dirac law, the normalized path rotates periodically on its circle; the killing has constant value along that trajectory and cancels under normalization. The corollary applies, but no convergence to a point or negative-gradient interpretation follows. Thus energy-controlled drift is a strictly broader dynamical description than a gradient flow.

## 12. Factored polynomial mobility and a genuine finite-atomic metric

Let F be polynomial, H=F+C, and retain the two certificates (S). Let B(x) be a real polynomial matrix and

    M(x)=B(x)^T B(x),       b(x)=−M(x)∇F(x).

Then

    −b·∇H=∇F^T M∇F=|B∇F|²

is explicitly SOS. The corollary in §11 therefore supplies the complete unrestricted-rank reverse lift for this state-dependent polynomial mobility, even if M is degenerate. Mere pointwise positive semidefiniteness of a polynomial matrix is not asserted to give a polynomial factorization B^T B; the factorization is a stated hypothesis.

If additionally M(x) is positive definite for every x, g_x(v,w)=v^T M(x)^(-1)w is a smooth genuine Riemannian metric on R^d. No uniform ellipticity is required. On the manifold of distinct positive r-atomic laws, modulo permutations, use

    G((u,v),(ũ,ṽ))=Σ_j u_jũ_j/w_j
                       +Σ_j w_j v_j^T M(x_j)^(-1)ṽ_j,
    Σ_j u_j=Σ_j ũ_j=0.                                (24)

This is positive definite and smooth. For E=Σ_j w_jF(x_j), direct pairing with any tangent gives

    grad_G E=((w_j(F(x_j)−E))_j,(M(x_j)∇F(x_j))_j).

Thus the forced atomic equations supplied by the reverse lift are exactly the negative gradient of E for this metric. Their dissipation is

    −E'=Σ_j w_j∇F(x_j)^T M(x_j)∇F(x_j)+Var_w(F).

For polynomial moment observables ℓ_p=Σ_jw_jp(x_j), direct pairing likewise gives the moment cometric

    G(grad_G ℓ_p,grad_G ℓ_q)
       =L(∇p^T M∇q)+L(pq)−L(p)L(q).                 (25)

Indeed grad_G ℓ_p has weight block w_j(p(x_j)−ℓ_p) and position block M(x_j)∇p(x_j). The cancellation of M^(-1)M establishes (25) without differentiating M. This extends the inherited Euclidean finite-atomic metric calculation; it does not claim that every positive M is a Hessian metric, nor that a degenerate M has an inverse or gives a genuine Riemannian metric.

### One exact one-dimensional mobility/Hessian control

Take

    F(x)=x²/2,       H=1+x²/2,       M(x)=1+x²,
    b(x)=−x(1+x²),       S=x²+x⁴.

Here M=1²+x², H is SOS, and H²−x²=1+x⁴/4 is SOS. With initial point z, define

    D_t(z)=1+z²(1−e^(−2t)),
    Φ_t(z)=z e^(−t)/sqrt(D_t(z)),
    ∫_0^t F(Φ_s(z))ds=(1/4)log D_t(z),
    E_t^H(z)=e^(−t)D_t(z)^(−1/4).                    (26)

D_t≥1 for t≥0. Direct differentiation verifies the ODE and killing integral, including z=0 and t=0. For t>0 the spatial image is exactly

    |x|<1/sqrt(e^(2t)−1).

This differs from the Euclidean quadratic gradient's onto linear contraction, although both are covered reverse lifts under their stated mobilities.

The position metric is g=dx²/(1+x²). Its geodesic coordinate is q=asinh x, because dq/dx=1/sqrt(1+x²). It also has the strictly convex Hessian potential

    ψ(x)=x arctan x−(1/2)log(1+x²),
    ψ'(x)=arctan x,        ψ''(x)=1/(1+x²)>0.          (27)

Therefore the Bregman divergence D_ψ(y,x)=ψ(y)−ψ(x)−ψ'(x)(y−x) is a legitimate strictly-convex-potential Bregman divergence, and the position metric is its Hessian. This is a particular explicit realization, not a statement that arbitrary polynomial mobility has a Hessian inverse.

The dual affine coordinate η=ψ'(x)=arctan x, with η∈(−π/2,π/2), is different from the geodesic coordinate asinh x. Its gradient trajectory satisfies

    η'=−tan η,       (sin η)'=−sin η,
    sin η(t)=e^(−t)sin η(0).

Solving this identity for x reproduces Φ_t in (26). These formulas are exact ordinary differential identities and connect the state-dependent metric to its characteristic dynamics; no discrete Bregman update, empirical interpretation, or noetic identification is inferred.

## 13. A bounded next question, not part of the theorem

For F=(x−y^m)²+y² with integer m>2, the valley x=y^m prevents every certificate (F+C)²−cR≥0 with finite C and c>0: the leading negative term −cy^(2m) dominates the fourth-degree energy square there. The present theorem therefore does not cover it in these coordinates.

The static polynomial automorphism (x,y)↦(u=x−y^m,y) makes F=u²+y². The already proved energy-power recurrence suggests a possible separate route: first prove Carleman existence in those energy-controlled polynomial coordinates, then pull back by the polynomial inverse. The transformed drift is still polynomial. This is not the earlier polynomial-characteristic theorem, because this static coordinate map is not the gradient-flow characteristic map. A separate transformed-generator/PDE proof and full coordinate-algebra check would be needed before claiming this additional class. No such extension is asserted by this packet.
