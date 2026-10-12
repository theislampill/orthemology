# Nonautonomous reverse lift under a common coercive SOS energy

10 October 2026 UTC. Additive ordinary mathematical research within ACTIVE T20. The parent proposed the common-energy moving-test route and the moving quadratic discriminator. This author proof tests and completes that route, with an exact clock refinement. It is not independent review, protected integration, formal-kernel verification, field-priority claim, empirical/noetic identification, or programme closure. Every earlier packet remains unchanged.

## 1. Exact finite-horizon theorem

Fix finite dimension d≥1 and a finite prescribed horizon T>0. Let H be a fixed coercive real polynomial that is SOS and satisfies H(x)≥1 pointwise. Let b_t:R^d→R^d and V_t:R^d→R be polynomial families on [0,T]. Each family must lie in a common finite polynomial basis with continuous coefficient functions on that closed interval. No time derivatives of those coefficients are assumed.

Suppose there are constants C,D≥0 and κ>0 such that for every t∈[0,T] the polynomials

    Q_t=CH−b_t·∇H,
    P_t=V_t+D−κH                                    (S)

are SOS. Their SOS decompositions need not be chosen continuously. Define K_t=V_t+D. In particular K_t is SOS and pointwise K_t≥κH≥κ, while b_t·∇H≤CH.

Let L_t be real linear functionals on the whole polynomial algebra P=R[x_1,…,x_d], with coordinatewise C¹ dependence on [0,T] (one-sided at its endpoints). Require all polynomial equations and all square tests:

    L_t(1)=1,                  L_t(q²)≥0,
    L'_t(p)=L_t(b_t·∇p)−L_t(V_t p)+L_t(V_t)L_t(p).    (H)

There is no initial law, rank, compact-support or moment-growth assumption. The pointwise statement H≥1 is not used to apply an abstract square-positive functional to H−1: only the explicit SOS certificates are used before representation.

**Theorem.** The nonautonomous ODE X'=b_t(X) has a unique forward flow Φ_(t,s) for 0≤s≤t≤T. There is exactly one probability μ with all absolute polynomial moments finite such that the whole supplied path is

    E_(t,s)(x)=exp(−∫_s^t K_r(Φ_(r,s)(x))dr),
    Z_t=∫E_(t,0)dμ,
    L_t(p)=∫p(Φ_(t,0)(x))E_(t,0)(x)dμ(x)/Z_t.        (1)

The same normalized formula uses V instead of K, because the constant factor e^(−Dt) cancels. Every positive-time full moment record is determinate. Writing ν_t=(Φ_(t,0))_*(E_(t,0)μ), the endpoint energy bound is

    ∫exp(r_C(t)H(y))dν_t(y)≤1,
    r_C(t)=κ(1−e^(−Ct))/C   if C>0,
    r_0(t)=κt.                                      (2)

Conversely, every all-moment initial probability gives an admitted C¹ path on the prescribed horizon. Paths with a fixed valid initial full moment functional are in bijection with its complete representing-law fibre. Distinct initial laws give different full records at every positive time. Finite initial full Hankel rank r forces the unique r-atomic characteristic evolution with constant rank r, without a promised future rank bound.

The statement also applies to paths supplied on a half-open interval by restricting to compact windows; when the prescribed coefficient family continues and the certificates hold on each larger finite window, the selected law gives unique continuation along that family. No continuation beyond an unspecified future schedule, globally uniform constants, arbitrary adaptive history policy or convergence theorem is asserted.

## 2. Ancestry: what was already solved

The changing-objective note `tensor-objective-switching-20261010/RESULT.md` already glues finite pure-killing switches and identifies a genuine failure of the autonomous even-time-derivative proof for moving objectives. That failure is a proof-route obstruction, not a nonrealizability example.

`time-varying-square-positivity-20261010/RESULT.md` already repairs continuously changing **pure killing** under uniform SOS domination of |x|². It explicitly covers moving coercive quadratics, so pure-killing moving quadratics and first-derivative inequalities are inherited results, not new credit here.

The accepted `general-coercive-energy-drift-20261010` proves the autonomous polynomial-drift theorem using inherited compact-fibre representation and the new compact-energy residual/PDE bridge. Its scalar-energy localization, bounded weighted spatial-cutoff uniqueness, tight initial recovery and fibre classification are the principal ingredients reused here.

The actual extension is a genuine nonautonomous transport/reaction hierarchy with one fixed coercive polynomial controlling both drift growth and killing. The moving test e^(−Ct)H supplies the missing estimate; the common-H localized PDE proof and two-time characteristics then require no time derivatives of the coefficients. This covers a changing-objective gradient instance, but a moving quadratic alone is not the whole claimed increment.

The static existence/determinacy bridge is inherited from `coercive-energy-moment-bridge-20261010/RESULT.md`, ultimately the compact-fibre Lemma F and compact-sublevel determinacy lemma in the earlier coercive and tensor-realizability packets. The polynomial sublevel envelope used in the converse is inherited from the nonconvex-limit packet and already requalified in the autonomous general-drift proof. Input bindings identify all inspected versions; this is a local ancestry check, not a broad priority survey.

## 3. Abstract moving-energy moments and the correct clock

Define, before any measure,

    a(t)=exp(−∫_0^t L_r(K_r)dr),       A_t=a(t)L_t.

The fixed finite coefficient bases and coordinate continuity make L_r(K_r) continuous. Thus a is C¹, positive, and a(0)=1. Constant shifts cancel in (H), so

    A'_t(p)=A_t(b_t·∇p−K_t p)                        (3)

for each fixed polynomial p. Since K_t=κH+P_t is SOS, a'≤0 and a≤1.

Set

    B_n(t)=e^(−Cnt)A_t(H^n),          n≥0.

These are C¹ because H is fixed and the scalar coefficient is smooth. The moving-test derivative, for n≥1, gives the exact identity

    B'_n=−n e^(−Cnt)A_t(H^(n−1)Q_t)
                        −e^(−Cnt)A_t(K_tH^n).

The products H^(n−1)Q_t and H^nP_t are SOS. Therefore, including n=0 by the mass equation,

    B'_n≤−κe^(Ct)B_(n+1)≤0.                         (4)

Every B_n is nonnegative. No derivative of b_t,V_t,Q_t or an SOS decomposition is taken. No positivity on an arbitrary nonnegative polynomial is assumed.

Use the increasing clock

    θ(t)=κ∫_0^t e^(Cr)dr.

Writing B_n as functions of θ gives dB_n/dθ≤−B_(n+1). The inherited nested-simplex integration from B_0(0)=1 gives

    B_n(t)≤n!θ(t)^(−n),
    A_t(H^n)≤n!r_C(t)^(−n),              t>0,        (5)

where r_C(t)=e^(−Ct)θ(t) is exactly (2). For C=0 the clock is κt. The weaker bound obtained by replacing κe^(Ct) by κ is valid, but (5) retains the correct sharper time dependence. Every step uses only first derivatives and finitely repeated integrations.

## 4. Static representation, determinacy, and time-dependent residual localization

At each positive t, (5) and abstract Cauchy–Schwarz give, for every polynomial q,

    A_t(q²H^(2n))
      ≤sqrt(A_t(q⁴))(2n)![2/r_C(t)]^(2n).

The common width r_C(t)/2 and compact fibres of H meet the inherited Lemma F. Thus A_t has a finite positive representative ν_t, of mass a(t); exponential-energy summation gives

    ∫e^(σH)dν_t≤1/[1−σ/r_C(t)],       0≤σ<r_C(t).     (6)

The inherited compact-sublevel lemma proves joint determinacy. No coordinate Carleman or exponential |x| bound is needed. Tightness and uniform higher polynomial moments, obtained from coordinate continuity on each interior time interval, then show ν_t and ρ_t=ν_t/a(t) are weakly continuous.

On J=[η,B] with η>0, choose ε=r_C(η)/4. Since r_C increases,

    sup_(t∈J)∫|p|e^(εH)dν_t
             ≤sqrt(2 sup_(t∈J)A_t(p²))<∞             (7)

for every fixed polynomial p. The same estimate is uniform for polynomial families in a common finite basis with bounded coefficients, by summing the estimates for the basis. This explicitly covers b_t·∇p, K_t p and p b_t·∇H. The fixed common H, rather than differentiability of the changing coefficients, is essential here.

For 0<u<v≤T define the order-one residual

    D_(u,v)(φ)=ν_v(φ)−ν_u(φ)
                    −∫_u^vν_r(b_r·∇φ−K_rφ)dr.       (8)

After representation, the common-energy localization argument from the autonomous packet applies with the following precise time-dependent coefficients. Taylor polynomials in e^(izH) and (7) first give D_(u,v)(p e^(izH))=0 for small real z. The product identity is

    (b_r·∇−K_r)[pP(H)]
       =(b_r·∇p−K_rp)P(H)+p(b_r·∇H)P'(H).           (9)

Holomorphic continuation in the scalar z strip |Im z|<ε/2 gives the identity at all real frequencies. Coefficient time continuity and the uniform finite-basis bounds justify all integrated terms; no ∂_r b_r or ∂_rK_r occurs.

The scalar signed coefficients are now

    α_p=H_*(pν_v−pν_u)
             −∫_u^v H_*((b_r·∇p−K_rp)ν_r)dr,
    β_p=−∫_u^v H_*(p(b_r·∇H)ν_r)dr.

They are finite with exponential energy tails by (7). Their combined scalar Fourier relation implies, by ordinary Fourier inversion,

    D_(u,v)(pχ(H))=α_p(χ)+β_p(χ')=0                 (10)

for every polynomial p and scalar χ∈C_c∞. One does not assert α_p=β_p=0 separately.

Because H is coercive, χ(H)D_(u,v) is a compactly supported order-one distribution. It kills every polynomial by (10). Coordinate exponential Taylor polynomials converge with their first derivatives on its compact support, so it kills every Fourier exponential and hence every compact smooth test. Choosing χ equal to one around H(supp φ) yields

    ν_v(φ)−ν_u(φ)=∫_u^vν_r(b_r·∇φ−K_rφ)dr           (11)

for every compact smooth φ. This is the actual nonautonomous weak PDE, derived after representation. Weak continuity, compact supports and continuous time coefficients make its right integrand continuous. The time-dependent compact-test rule follows by the usual difference quotient. These are precisely the autonomous localization steps with their time-dependent bounds checked, not an assumption that polynomial equations automatically determine a measure PDE.

## 5. Genuine two-time characteristics and noncompact uniqueness

Along a local ordinary trajectory,

    dH(X_r)/dr=b_r·∇H(X_r)≤CH(X_r).

Gronwall gives H(Φ_(t,s)(x))≤e^(C(t−s))H(x). On the finite horizon this confines the trajectory to one compact H-sublevel. The continuous-in-time polynomial vector field is uniformly locally Lipschitz in x and bounded on that compact set. Ordinary ODE continuation therefore gives Φ_(t,s) for every s≤t≤T.

Each Φ_(t,s) is smooth in x and injective, with nonzero spatial Jacobian determinant. Local backward uniqueness along existing trajectories supplies injectivity, without assuming globally defined backward characteristics. It is a diffeomorphism onto its open image.

The two-time cocycles are

    Φ_(t,s)=Φ_(t,r)∘Φ_(r,s),
    E_(t,s)=E_(r,s)(E_(t,r)∘Φ_(r,s)).                (12)

Because K_r≥0, 0<E_(t,s)≤1. For terminal f∈C_c∞ set

    U(r,x)=E_(t,r)(x)f(Φ_(t,r)(x)).

It is C¹ in r and smooth in x on compact sets, and

    ∂_rU+b_r·∇U−K_rU=0,       |U|≤||f||∞.           (13)

The start-time derivative in (13) follows by differentiating the two-time cocycle at a short initial step. Continuous b_r,K_r and smooth spatial dependence suffice: Φ_(r+h,r)(x)=x+h b_r(x)+o(h) and E_(r+h,r)(x)=1−hK_r(x)+o(h), uniformly on compact sets. Local inverse maps supply the equivalent backward difference quotient. No time derivative of b_r or K_r is required.

Apply the compact-test rule to χ_N(x)U(r,x), with a fixed standard spatial cutoff dilated by N. Exact cancellation leaves ν_r(U b_r·∇χ_N). Common polynomial degrees and bounded coefficients give |b_r(x)|≤K(1+|x|^m) uniformly. Uniformly bounded higher moments on [s,t] then make the cutoff error vanish just as in the autonomous proof. Hence

    ν_t=(Φ_(t,s))_*[E_(t,s)ν_s],        0<s<t≤T.       (14)

No compact inverse-flow support or global derivative bound for U is needed. Lower-bounded killing supplies the bounded test; polynomial drift and uniform high moments remove the spatial boundary term.

## 6. Initial recovery, endpoint estimate, converse and fibres

Coordinate continuity near zero gives tightness and uniform polynomial integrability of ρ_s. Choose one weak limit μ along s_j↓0. All polynomial moments pass to the limit, so μ represents L_0 and has every absolute polynomial moment. Since a(s_j)→1, ν_(s_j) has the same limit.

For fixed t>0, E_(t,s_j)f∘Φ_(t,s_j) is uniformly bounded and converges locally uniformly to E_(t,0)f∘Φ_(t,0), by continuous dependence of nonautonomous solutions and weights on the initial time. Tightness permits passage through (14), giving ν_t=(Φ_(t,0))_*(E_(t,0)μ), and its mass is a(t)=Z_t.

At a fixed positive t, inverse pushforward on the open spatial image and division by the strictly positive weight recover the initial finite measure. For normalized laws this recovers proportional initial probabilities, which their total masses identify. Positive-time determinacy therefore proves unique selected-law recovery and the full initial-law-fibre classification, including separation at every positive time. Finite initial rank gives the inherited finite GNS law; distinct atom positions and positive weights preserve full rank.

For the endpoint bound, along an initial trajectory the earlier Gronwall estimate implies

    H(Φ_(r,0)(x))≥e^(−C(t−r))H(Φ_(t,0)(x)),  r≤t.

Thus ∫_0^t K_r(Φ_(r,0)(x))dr≥r_C(t)H(Φ_(t,0)(x)), proving (2). This stronger endpoint exponential estimate is used only after characteristics are identified, not obtained by summing (6) at its endpoint.

For the converse, the inherited semialgebraic sublevel envelope of a coercive polynomial gives constants M,N with 1+|y|²≤M(1+H(y))^N. Combined with H(Φ_(t,0)(x))≤e^(CT)H(x), it gives a polynomial bound in the initial |x| for all forward positions on [0,T]. The common finite coefficient bases similarly bound every generator polynomial b_t·∇p−K_tp. Since E≤1, every all-moment μ permits dominated differentiation, continuously through t=0. This yields ν'_t(p)=ν_t(b_t·∇p−K_tp) and Z'_t=−ν_t(K_t); normalization gives exactly (H). This proves the complete converse under merely continuous time coefficients.

The future coefficient schedule is part of the data. If it extends with these local-window assumptions, this same μ gives the unique corresponding extension; a choice of unspecified future coefficients is not forced by the past hierarchy.

## 7. Moving quadratic transport: certificates and exact solution

In one dimension, on [0,T], take

    V_t(x)=(x−t)²,       b_t(x)=−2(x−t),       H=1+x²,
    C=T²,               κ=1/2,                D=T²+1/2.

The certificates are exact:

    CH−b_tH'=4(x−t/2)²+T²x²+(T²−t²),
    V_t+D−κH=(x−2t)²/2+(T²−t²).                    (15)

The final scalar coefficients are nonnegative on the stated horizon, so each right side is SOS. This is a finite-horizon certificate; the displayed C,D are not claimed independent of T.

For τ=t−s≥0 and A=z−s+1/2,

    Φ_(t,s)(z)=t−1/2+A e^(−2τ),
    I_(t,s)(z)=∫_s^t V_r(Φ_(r,s)(z))dr
             =τ/4+A²(1−e^(−4τ))/4−A(1−e^(−2τ))/2,
    E_(t,s)(z)=exp(−Dτ−I_(t,s)(z)).                 (16)

Differentiation verifies the ODE, initial datum and nonnegative integrated killing. Every finite-time spatial map is affine with positive slope e^(−2τ), so its image is all R. This example has actual time-dependent transport, which the earlier pure-killing Theorem V does not by itself supply.

For μ=(δ_(−1)+δ_0)/2 at s=0, the ratio of the two unnormalized surviving weights is

    exp(−[1−e^(−2t)]/2).

It is nonconstant, and both atom positions move under (16). This distinguishes the model from the earlier fixed-position pure-killing ratio exp(−t−t²). Neither model is being substituted for the other.

### The even-time-derivative route still is not the argument

For differentiable coefficients only, the original unshifted mass a_V of a transported law satisfies

    a_V''=ν_t^V(V_t²−b_t·∇V_t−∂_tV_t).

In the moving quadratic this integrand is r⁴+4r²+2r, r=x−t, not simply V_t². For initial μ=δ_(−1/4), at the interior time t=(log 2)/2 on horizon T=1, formula (16) gives r=−3/8 and

    r⁴+4r²+2r=−687/4096<0.

Thus the original unshifted positive mass has a strictly negative second derivative there. This is an exact proof-route control, not a counterexample to representation. The particular added D in (15) changes that derivative, and no negative-second-derivative claim is made for that shifted mass. More fundamentally the theorem assumes only continuous coefficients, so second time derivatives need not exist at all. Its proof uses the first-derivative moving-energy inequalities instead.

## 8. Controlled-geometry scope and limits

The theorem treats an externally prescribed coefficient schedule. An adaptive or history-dependent rule is covered only after a valid state/control model and its resulting coefficient path, regularity and certificates are supplied; no arbitrary hidden-memory policy is silently included.

When b_t=−∇V_t, the forced finite-atomic equations are the instantaneous negative gradient of E_t=Σ_jw_jV_t(x_j) in the inherited Fisher-weight/Euclidean-position metric. With a specified positive-definite factored mobility, the analogous positional metric is M_t^(-1). If ∂_tV_t exists, the total energy derivative also has the external-work term Σ_jw_j∂_tV_t(x_j); it is not generally nonpositive. No time-varying convexity, convergence or cognitive-identifiability conclusion follows from the reverse lift.

Pointwise coercivity of each V_t alone does not establish the common certificates (S). No finite square-test truncation, diffusion theorem, stable reconstruction algorithm, field-priority finding, empirical/noetic interpretation, protected integration or programme closure is asserted. Finite exact controls supplement the ordinary universal proof and preserve the distinction between inherited pure-killing results and the new time-dependent transport extension.
