# Unrestricted-rank reverse lift for SOS-dissipative polynomial gradients

10 October 2026 UTC. Additive ordinary mathematical research within ACTIVE T20. The parent proposed both the dissipative-gradient class and its additive-constant strengthening and participated in proof development. The radial quartic packet and every other bound predecessor remain unchanged. This is an author deliverable, not an independent review, protected integration, formal-kernel verification, priority claim, empirical/noetic identification, or programme closure.

## 1. The theorem and its exact hypotheses

Fix a finite dimension d≥1, P=R[x_1,…,x_d], R(x)=|x|², an autonomous polynomial F∈P, and constants

    κ>0,    λ≥0,    D≥0,    C≥0.

Assume the following two polynomials are sums of squares of real polynomials:

    V=F+C,
    Q=x·∇F−κR²+λR+D.                                  (S)

A zero polynomial is allowed as an SOS. The second certificate is a radial dissipativity condition in the declared Euclidean coordinates. It is not a convexity assumption. The additive D term is important; setting D=0 would force ∇F(0)=0.

Let 0<T≤∞ and let L_t:P→R be real linear functionals for 0≤t<T. Assume every polynomial coordinate is C¹, including a continuous right derivative at zero, and for all p,q∈P and all supplied times,

    L_t(1)=1,                 L_t(q²)≥0,
    L'_t(p)=−L_t(∇F·∇p)−L_t(Fp)+L_t(F)L_t(p).           (H)

There is no initial-law assumption, rank assumption, initial moment-growth assumption, or finite truncation of the square tests.

**Theorem.** The polynomial ODE X'=−∇F(X) has a unique global forward flow Φ_t. There is exactly one Borel probability μ on R^d, with all absolute polynomial moments finite, such that the entire supplied path is

    E_t(x)=exp(−∫_0^t V(Φ_s(x))ds),     Z_t=∫E_t dμ,
    L_t(p)=∫p(Φ_t(x))E_t(x)dμ(x)/Z_t.                   (1)

At zero, Φ_0=id, E_0=1 and Z_0=1. The same normalized formula results if V is replaced by F: writing E_t^V and E_t^F for the respective weights, E_t^V=e^(−Ct)E_t^F, and this constant factor cancels between numerator and denominator.

Every positive-time full moment record is determinate. Put

    Δ=sqrt(λ²+4κD),
    Y(t)=(λ+Δ coth(Δt))/(2κ)           if Δ>0,
    Y(t)=1/(2κt)                      if Δ=0.           (2)

Its representing probability is carried by the open forward image O_t=Φ_t(R^d), and

    O_t ⊂ {x:R(x)<Y(t)}.

Consequently its topological support lies in the closed ball R≤Y(t), and the bounding sphere has zero mass. The topological support can nevertheless meet that sphere as a limit set. The image need not be the whole open ball, and the flow is not asserted to be onto R^d.

Conversely, every probability with all absolute polynomial moments generates a normalized full-square-positive C¹ path (H) for all t≥0. Therefore the admitted paths with any fixed valid initial full moment functional are in bijection with that functional's representing-law fibre. Distinct initial laws in one fibre give different full records at every positive time. A supplied nontrivial finite-horizon path has a unique extension to every future time for this fixed F.

If the initial full Hankel rank is finite r, the entire path is the unique r-atomic characteristic evolution, with constant full rank r. No bound on future rank needs to be promised. The inherited finite-atomic metric then makes it a genuine negative-gradient trajectory. For arbitrary infinite laws the theorem proves the measure dynamics and energy dissipation, not an infinite-dimensional smooth Riemannian-manifold construction.

## 2. What is inherited and what changes

The inspected inputs are bound in INPUT_BINDINGS.json, and no old file is edited.

1. radial-quartic-gradient-reverse-lift-20261010/RESULT.md and its independent review already establish the complete reverse-existence chain for F=R²/4. The order of proof here is inherited: force positive-time representation, extend polynomial tests to a compact-test PDE, identify actual characteristics, and only then recover the initial law. Their compact Fourier-test and tight initial-limit arguments are reused with the necessary estimates written out below.
2. diffusive-coercive-realizability-20261010/RESULT.md, §§3–4, already proves the square-only radial log-convexity and interpolation argument. We use precisely that argument, without importing its diffusion theorem or its strict-interior-positivity claim. Our scalar root equation has coefficients independent of moment index n, giving compact rather than merely Gaussian-tailed positive-time measures. Zeros are genuinely possible here.
3. complete-flow-finite-rank-20261010/RESULT.md, §9, already gives a forward-complete/lower-killing reverse lift under a locally uniform finite full-path rank bound. joint-atomic-gradient-lift-20261010/RESULT.md already identifies its finite-atomic gradient metric. Those results do not remove the path-rank hypothesis for the present general class.
4. polynomial-transport-continuation-20261010/RESULT.md already gives an unrestricted-rank reverse lift for bounded-degree polynomial-automorphism characteristic paths. The present positive-time flow has a bounded image and is injective, so it cannot be a polynomial automorphism of R^d; no inverse-flow substitution into an abstract polynomial functional is used.

The incremental theorem is the passage from the one radial quartic to the certificate class (S), allowing nonconvex, nonradial and shifted polynomial potentials, with an n-independent Riccati bound before representation. The D=0 clock estimate in §5 records the original narrower route; it is not the only basis for the stronger theorem.

A bounded search of available top-level RESULT.md files for radial estimates, dissipative polynomial gradients and unrestricted-rank gradient lifts found these antecedents but no earlier instance of this certificate theorem. This is local deduplication, not an exhaustive literature or priority survey.

The only specialized imported existence result is the classical Nussbaum–Carleman theorem: full square positivity plus all marginal Carleman conditions yields a unique multivariate representing measure. The inspected primary statement is Putinar–Schmüdgen, *Multivariate Determinateness*, Theorem 25 and the immediately following Nussbaum attribution, printed p.24, https://arxiv.org/pdf/0810.0840v1 . The inherited PDF and page extraction are hash-bound, and the corresponding current primary-web statement was checked. For dimension one use Hamburger existence and Carleman uniqueness. Standard local ODE theory, polynomial approximation, Fourier inversion and tight weak compactness are used with their needed bounds below.

## 3. The radial differential inequality before representation

Set

    a(t)=exp(−∫_0^t [L_s(F)+C]ds),
    A_t(p)=a(t)L_t(p),          a_n(t)=A_t(R^n), n≥0.

Coordinate continuity makes the integral finite on every compact time interval, so a>0 and a(0)=1. Unnormalization gives

    A'_t(p)=A_t(Gp),      Gp=−∇F·∇p−Vp.                (3)

Each R^n is SOS by the multinomial expansion. Products of SOS polynomials are SOS: (Σf_i²)(Σg_j²)=Σ_(i,j)(f_ig_j)². Thus a_n≥0 and A_t(VR^n)≥0. Also

    a_0'=−A_t(V)≤0,          0<a_0=a≤1.

For n≥1, ∇R^n=2nR^(n−1)x and the exact certificate identity give

    a_n'=2nD a_(n−1)+2λn a_n−2κn a_(n+1)
                       −2n A_t(R^(n−1)Q)−A_t(VR^n).

Both final terms are nonnegative before their minus signs, since both tested polynomials are SOS. Hence

    a_n'≤2nD a_(n−1)+2λn a_n−2κn a_(n+1).             (4)

No non-SOS nonnegative polynomial has been tested in an unrepresented functional.

At a fixed time, polynomial Cauchy–Schwarz proves

    a_n²≤a_(n−1)a_(n+1),                n≥1.           (5)

For odd n=2k+1 use the pair R^k,R^(k+1). For even n=2k use the direct-sum pairs x_iR^(k−1),x_iR^k, summed over i. This is the inherited radial interpolation argument; it needs no representing measure.

To cover zero moments, temporarily add ε ev_z with |z|=1 to the static functional. Its radial moments a_n+ε are positive and log-convex. Comparing the index n−1 with the chord between 0 and n, and n with the chord between 0 and n+1, then letting ε↓0, yields

    a_(n−1)≤a_0^(1/n)a_n^((n−1)/n),
    a_(n+1)≥a_n^((n+1)/n)/a_0^(1/n).                  (6)

For n=1 the first formula means the equality a_0=a_0 directly, including at a_1=0. The static ε perturbation is not claimed to solve any differential equation. Since a_0≤1, (4) and (6) imply, wherever a_n>0,

    u_n=a_n^(1/n),
    u_n'≤f(u_n),       f(u)=2D+2λu−2κu².               (7)

The coefficients in (7) do not depend on n. This is the crucial difference from the inherited diffusion inequality.

## 4. Zero-safe Riccati comparison and compact moment growth

Each u_n is continuous and nonnegative, and is C¹ on its positive set. It need not be C¹ at a zero. We do not assert strict positivity of positive radial moments.

For r>0 let y(t;r) solve y'=f(y), y(0)=r. This solution stays strictly positive at every finite time, is forward global, and is bounded on each finite window. Fix r>u_n(0). Then u_n(t)≤y(t;r). To justify comparison, any interval on which u_n>y lies within the positive set of u_n. On a finite such interval f is Lipschitz on the bounded ranges of u_n and y. At its left endpoint u_n−y≤0; the differential inequality (u_n−y)'≤K(u_n−y) on the positive component and Gronwall exclude that component. Equivalently one may use a strict supersolution followed by a limit. A zero of u_n cannot jump past the strictly positive comparator. This never differentiates u_n at a zero.

For Δ>0 set

    α=(λ+Δ)/(2κ),       β=(λ−Δ)/(2κ),       q=e^(−2Δt).

Here α>0 and β≤0. The exact finite-initial solution is

    y(t;r)=[α(r−β)−β(r−α)q]/[(r−β)−(r−α)q].           (8)

For r≥0 and t≥0 its denominator is (r−β)(1−q)+(α−β)q>0. Thus formula (8) works even for r=β=0, when the solution is zero; no division by an initial positive radius is needed. Its limit as r→∞ is Y(t) in (2). For t>0 it is strictly below Y(t), since

    Y(t)−y(t;r)=(α−β)² q /
        [(1−q)((r−β)−(r−α)q)] >0.                    (9)

When Δ=0, necessarily λ=D=0, and

    y(t;r)=r/(1+2κrt),          Y(t)=1/(2κt).

Apply comparison for arbitrary r>u_n(0), then either pass r↓u_n(0), or just use y(t;r)<Y(t). We obtain for all n≥1 and t>0,

    0≤a_n(t)≤Y(t)^n.                                  (10)

The bound is independent of all initial high moments. No finite initial moment is replaced by an actually infinite value. It follows from finite scalar comparisons and their explicit envelope. The closed inequality in (10) is all that is used for representation.

The function Y is positive, decreasing and finite for t>0; it solves Y'=f(Y). In the D=0, λ>0 case it reduces to

    Y(t)=λ/[κ(1−e^(−2λt))].

## 5. The original D=0 clock estimate, as a refinement

When D=0, one can avoid interpolation and recover the parent-proposed route directly from (4). Define

    c_n(t)=e^(−2λnt)a_n(t),
    u(t)=∫_0^t e^(2λs)ds.

The transformed functions satisfy dc_n/du≤−2κn c_(n+1), so every c_n is nonincreasing. Iterating the integrated inequalities from index 1 to n−1 over a time simplex yields

    c_1(0)≥[2κu(t)]^(n−1)c_n(t).

The product (2κ)^(n−1)(n−1)! cancels the simplex factorial exactly. Thus, with M=L_0(R),

    a_n(t)≤M e^(2λt)Y(t)^(n−1),          n≥1.          (11)

For λ=0 take u=t and Y=1/(2κt). This is sometimes sharper than (10) when M is small. If M=0, every positive radial moment vanishes throughout positive time, consistently with the forced stationary origin. Indeed when D=0, Q is nonnegative with Q(0)=0, so ∇Q(0)=0; its linear part is ∇F(0)·x, proving ∇F(0)=0. For D>0 this origin-criticality argument and the monotone-clock argument are unavailable, which is why §4 explicitly handles zeros without importing the diffusion positivity claim.

## 6. Positive-time representing measures and the actual PDE

Fix t>0. The polynomial R^n−x_i^(2n) is SOS, so

    0≤L_t(x_i^(2n))≤a(t)^(−1)Y(t)^n.

For nonzero moments, their inverse 2n-th roots are at least a(t)^(1/(2n))/sqrt(Y(t)), which tends to the positive value 1/sqrt(Y(t)). Every marginal Carleman series diverges; a zero moment is interpreted as an infinite term. Nussbaum–Carleman now supplies a unique representing probability ρ_t for L_t. Put ν_t=a(t)ρ_t. This is the unique finite positive measure representing A_t, and it has mass at most one.

For r>Y(t), Markov's inequality and (10) give

    ν_t({R≥r})≤a_n(t)/r^n≤[Y(t)/r]^n→0.

Hence ν_t is supported in the closed ball R≤Y(t). On every interior time interval J=[s,t], s>0, all ν_r have a common compact support K={R≤Y(s)}. Polynomial coordinate continuity and uniform polynomial approximation on K imply weak continuity of r↦ν_r: first approximate a continuous test on K uniformly by a polynomial, and use the common mass bound to control the error.

We spell out the inherited polynomial-to-PDE step, since merely naming a transport equation before this point would assume the existence being proved. For ξ∈R^d take P_N(x)=Σ_(j=0)^N(iξ·x)^j/j!. On K these polynomials and their first derivatives converge uniformly to e^(iξ·x) and its first derivatives; ∂_iP_N=iξ_iP_(N−1). As b=−∇F and V are bounded on K, GP_N converges uniformly there to (ib·ξ−V)e^(iξ·x). Passing the integrated polynomial identity

    ν_v(P_N)−ν_u(P_N)=∫_u^v ν_r(GP_N)dr

to the limit is justified by the common mass bound. For φ∈C_c∞, its Fourier transform has ∫(1+|ξ|)|φ̂(ξ)|dξ<∞, and the generator bound on K is a constant times 1+|ξ|. Fourier inversion and Fubini therefore imply

    ν_v(φ)−ν_u(φ)=∫_u^v ν_r(b·∇φ−Vφ)dr.              (12)

The integrand is continuous by the proved weak continuity. This is the actual weak equation ∂_tν=−div(bν)−Vν on positive times.

For a family ψ_r smooth in space and C¹ in time with common compact support, whose needed derivatives vary uniformly continuously, splitting the difference quotient into change of test and change of measure gives

    dν_r(ψ_r)/dr=ν_r(∂_rψ_r+b·∇ψ_r−Vψ_r).             (13)

Bounded masses and uniform time differentiation handle the first part; weak continuity and (12), with ψ_r frozen at the differentiation time, handle the other part. No nonpolynomial test is fed into the abstract A_t.

## 7. Forward characteristics, their image and backward tests

Pointwise nonnegativity of Q implies, along every local characteristic,

    dR(Φ_t(x))/dt≤2D+2λR(Φ_t(x))−2κR(Φ_t(x))².        (14)

Scalar comparison with (8) gives R(Φ_t(x))≤y(t;R(x))<Y(t) for t>0. Dropping the negative term also yields the useful initial-coordinate bound

    R(Φ_t(x))≤e^(2λt)R(x)+2D∫_0^t e^(2λs)ds.          (15)

For λ=0 the integral is t. This prevents finite-time escape: on each finite time segment the trajectory stays in a bounded ball, where the polynomial vector field is bounded and locally Lipschitz. A hypothetical finite terminal time has a finite endpoint limit and local ODE existence continues it. Thus Φ_t exists for every t≥0 and finite x.

When D=0, the sharper scalar comparison is explicitly

    R(Φ_t(x))≤e^(2λt)R(x)/
        [1+(κ/λ)(e^(2λt)−1)R(x)]                     (λ>0),
    R(Φ_t(x))≤R(x)/[1+2κtR(x)]                       (λ=0).

In particular |Φ_t(x)|≤e^(λt)|x| in that branch. For D>0 the additive term in (15) must be retained.

Smooth local ODE theory makes (t,x)↦Φ_t(x) smooth on all finite forward time-space neighborhoods. A finite-time map is injective: if two trajectories meet, local uniqueness for the reversed equation, along those existing compact trajectory segments, forces the two histories to agree all the way back to zero. This uses local backward uniqueness along existing paths, not global backward completeness.

The derivative J_t=D_xΦ_t solves J'_t=Db(Φ_t)J_t, J_0=I, so

    det J_t=exp(∫_0^t div b(Φ_s(x))ds)>0.

The inverse function theorem makes Φ_t a local diffeomorphism. Together with injectivity, its local inverses agree, giving a smooth inverse on the open image O_t. Hence it is a homeomorphism R^d→O_t. There is no surjectivity assertion beyond that image. By (14), O_t lies strictly inside the radius bound in the theorem.

Since V≥0, the weight E_t in (1) satisfies 0<E_t≤1. Smooth dependence on compact sets gives smooth E_t; the flow and integral obey the semigroup and multiplicative identities

    Φ_(u+v)=Φ_u∘Φ_v,
    E_(u+v)=E_v(E_u∘Φ_v).                              (16)

For fixed 0<s<t and terminal f∈C_c∞, let U(r,x)=E_(t−r)(x)f(Φ_(t−r)(x)). Differentiating (16) at a short initial step gives

    ∂_rU+b·∇U−VU=0.

Choose a fixed compact smooth cutoff χ equal to one on a neighborhood of the common ball K supporting all ν_r for s≤r≤t. The function χU satisfies the time-dependent test hypotheses in (13). On K, χ=1 and ∇χ=0, so the integrand vanishes. Consequently

    ν_t(f)=ν_s(E_(t−s)f∘Φ_(t−s)),
    ν_t=(Φ_(t−s))_*[E_(t−s)ν_s],       0<s<t<T.         (17)

This proves the exact measure evolution using only compact tests already justified from the hierarchy. It does not appeal to an unspecified unbounded-coefficient transport uniqueness theorem.

## 8. Recover the initial law and exclude hidden inflow

By coordinate continuity near zero, for every fixed k the moments L_s(R^k) are bounded on a short compact time interval. The second-moment bound makes the represented probabilities ρ_s tight as s↓0. Choose one sequence s_j↓0 with ρ_(s_j) converging weakly to a probability μ. Since a(s_j)→1, ν_(s_j) has the same weak limit.

Lower semicontinuity of R^k gives finite radial moments for μ. Every polynomial p of degree m is uniformly integrable along the sequence: choose 2k>m and N≥1; outside |x|≤N,

    |p(x)|≤C_p(1+|x|^m)≤2C_p N^(m−2k)|x|^(2k).

The uniform R^k moment bound makes these tails uniformly small. Compact cutoff approximation, weak convergence and this tail bound yield

    ∫p dμ=lim_j L_(s_j)(p)=L_0(p).                     (18)

Thus μ has all absolute polynomial moments and represents the initial functional. This is existence, not a premature assertion of initial determinacy.

Fix t>0 and f∈C_c∞. For large j, s_j<t. The kernels

    g_j(x)=E_(t−s_j)(x)f(Φ_(t−s_j)(x))

are uniformly bounded by ||f||∞ and converge locally uniformly to the bounded continuous g(x)=E_t(x)f(Φ_t(x)). For a fixed compact cutoff, weak convergence and local uniform convergence pass the integrals to the limit. Tightness and the uniform bound make the complementary tail uniformly small. Passing (17) along this single sequence gives

    ν_t=(Φ_t)_*(E_t μ).                                (19)

The same μ works for each fixed t; no t-dependent subsequence is chosen. Taking masses gives a(t)=Z_t, proving (1). Equation (18) supplies t=0.

The output in (19) is carried by O_t, so its bounding sphere has zero mass. To prove uniqueness of μ, inverse-pushforward on O_t by its continuous inverse gives E_tμ. Division by the strictly positive Borel function E_t then recovers μ. The reciprocal need not be bounded; equality of known positive measures can be integrated against it, and finiteness is guaranteed for actual inputs. Thus two possible initial weak limits or initial representing laws producing the supplied path must coincide.

The normalized map is injective on probabilities as well: equality of normalized outputs gives E_tμ/Z_μ=E_tμ'/Z_μ' after inverse pushforward, hence μ/Z_μ=μ'/Z_μ' after division by E_t. Their probability masses force Z_μ=Z_μ' and μ=μ'. This is an inverse on the actual output range. An arbitrary law in the closed bounding ball need not lie in that range or have a finite all-moment inverse-weighted pullback.

## 9. Converse, classification and gradient consequences

Let μ be any probability with all absolute polynomial moments. The bound (15) implies |Φ_t(x)|≤C_H(1+|x|) on every finite window 0≤t≤H. Also 0<E_t≤1, so all integrals in (1) are finite and Z_t is strictly positive. For any fixed polynomial p, each of p, b·∇p and Vp is a polynomial of a fixed finite degree. Their compositions with Φ_t are therefore bounded uniformly on that window by C(1+|x|^m) for a sufficiently large fixed m, which is μ-integrable. Differentiation of p(Φ_t)E_t is dominated by such a bound. Dominated differentiation gives, including continuous right derivatives at zero,

    dν_t(p)/dt=ν_t(b·∇p−Vp),       Z'_t=−ν_t(V).

Normalizing cancels the C terms and gives exactly (H), with normalization and all square tests automatic. This constructs the path globally.

Reverse existence plus the converse gives the law/path correspondence and the initial-moment-fibre classification in §1. Positive-time compact determinacy and normalized-map injectivity show that distinct laws in the same initial fibre have distinct full positive-time records. A supplied nontrivial path therefore fixes its initial law and its unique future extension. Bare initial moments alone have that uniqueness exactly when their fibre is a singleton.

For finite full initial Hankel rank, the inherited finite GNS theorem gives its unique finite atomic law. Positive E_t preserves positive masses, and injective Φ_t preserves distinct positions, hence full rank stays constant. With the inherited metric

    G((u,v),(u,v))=Σ_j u_j²/w_j+Σ_j w_j|v_j|²,
    Σ_j u_j=0,

the forced equations x'_j=−∇F(x_j), w'_j=−w_j(F(x_j)−Σ_lw_lF(x_l)) are the negative gradient of Σ_jw_jF(x_j). The radial certificate also implies coercivity if needed to match the predecessor's hypothesis: for |θ|=1 and r≥1, integrate

    dF(rθ)/dr≥κr³−λr−D/r

to get a uniform quartic lower bound minus quadratic and logarithmic terms, using the minimum of F on the unit sphere.

For every represented path, and also directly by full square positivity in (H),

    dL_t(F)/dt=−L_t(|∇F|²)−[L_t(F²)−L_t(F)²]≤0.       (20)

The variance term is L_t((F−L_t(F))²). This energy decrease does not imply convergence to a global minimizer for nonconvex F, and is not substituted for the reverse-existence proof.

## 10. Main discriminating example: a nonconvex multiwell

Take

    F(x)=(R(x)−1)²/4,
    b(x)=(1−R(x))x,
    κ=λ=1,      D=C=0.

Here F is itself a square, x·∇F=R²−R and Q=0. The Hessian at the origin is −I, so F is nonconvex. In dimension one it has two global minima ±1; in higher dimensions the global minimizers form the unit sphere. The theorem applies with no rank promise or initial representing law.

For r=R(x), t≥0 and H_t=1+(e^(2t)−1)r, the exact flow, radius and integrated original killing are

    Φ_t(x)=e^t x/sqrt(H_t),
    r_t=e^(2t)r/H_t,
    K_t(x)=∫_0^t F(Φ_s(x))ds
          =t/4−log(H_t)/8−(r_t−r)/8.                  (21)

Indeed r'_t=2r_t−2r_t², (log H_t)'=2r_t, and differentiating K gives (r_t−1)²/4 with K_0=0. Thus K_t≥0 despite the mixed signs in its closed form, and E_t=e^(−K_t)≤1.

For t>0 the image is exactly

    O_t={y:R(y)<1/(1−e^(−2t))},

with inverse

    Φ_t^(-1)(y)=e^(−t)y/sqrt(1−(1−e^(−2t))R(y)).       (22)

It is a bounded-image nonpolynomial flow, outside the polynomial-automorphism theorem. It is not a monomial quartic flow: the added negative quadratic changes both the dynamics and its stationary set. The present SOS certificate theorem, not a mistaken assertion that all coercive gradients were already covered, supplies its unrestricted-rank reverse lift.

The formulas pass through r=0 and r=1 without division by either: at the origin Φ_t=0 and K_t=t/4; on the unit sphere Φ_t=x and K_t=0. Hence δ_0 is a stationary normalized path, although the origin is a strict local maximum of F, and every law carried by the unit sphere is stationary. In dimension one every mixture of δ_(-1) and δ_1 is stationary. These are exact controls against importing the radial predecessor's universal collapse to δ_0 or a global-minimization conclusion. The general bound tends to R≤1, which is consistent with these stationary examples.

## 11. Additive-D and nonradial scope controls

A concise shifted control shows why the D term and zero-safe argument matter. In one dimension take

    F=(x−1)^4/4,    κ=1/4,    λ=1,    D=1/4,    C=0.

Then the exact certificate is

    xF'−κx^4+λx²+D
       =(3/4)(x²−2x)²+(x−1/2)².                       (23)

Here F'(0)=−1, so no D=0 certificate in these coordinates can hold. The actual translated radial flow is

    Φ_t(x)=1+(x−1)/sqrt(1+2t(x−1)²).

Its δ_0 path leaves zero immediately. Its initial positive radial moments all vanish, yet its positive-time radial moments are positive, so the diffusion predecessor's strict-positivity reasoning and the narrower M=0 conclusion must not be copied into the D>0 case. The translated quartic dynamics is an inherited coordinate corollary; (23) is a certificate and zero-branch control, not a separate claim of mathematical novelty.

The class is not restricted to radial potentials. For example in dimension two,

    F(x_1,x_2)=((x_1²+x_2²−1)²)/4+x_1²/2

has the same κ=λ=1, D=C=0 and Q=x_1². Both certificates are explicit SOS, while the two minima are (0,±1). This single check witnesses nonradial scope; no closed-form flow or additional example campaign is required for the general proof.

## 12. Exact evidence and nonclaims

check_exact.py verifies all old-input hashes; both radial Cauchy–Schwarz decompositions; the exact generator/certificate identity; marginal SOS differences in selected dimensions; the Riccati envelope, finite-initial solution and strict gap; the λ=D=0 and D=0 clock limits; the simplex coefficient; multiwell flow/radius/killing/cocycle/inverse and backward-generator identities; normalized quotient cancellation including C; shifted/nonradial SOS controls; and stationary/non-minimization scope controls. Its executed checks and source preservation are recorded in EXACT_CHECKS.json and check_exact.log. The frozen manifest binds the author files for separate review.

These are finite symbolic and exact-algebra controls supplementing the universal written argument. They do not establish infinite-dimensional measure existence by enumeration or verify the theorem in a formal proof kernel. Full square positivity and the exact C¹ all-polynomial hierarchy remain strong supplied-path hypotheses. Mere pointwise dissipativity without an SOS certificate, bare coercivity, a finite selection of positive moment matrices, finite data, or energy decrease alone are not asserted sufficient by this theorem. There is no global backward completeness, surjectivity onto arbitrary later laws, stable numerical inversion, empirical/noetic identity, independent-review verdict, protected change, integration or closure claim.
