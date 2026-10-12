# Action length and moment tails for polynomial gradient laws

10 October 2026 UTC. Separate additive successor within ACTIVE T20. The parent proposed the ensemble gradient inequality and its moment-cometric consequence. This report verifies them and supplies an essential initial-time qualification. Frozen predecessors remain unchanged. Ordinary mathematics only; no formal-kernel, protected-integration, new-field-priority, infinite-dimensional smooth-manifold or programme-closure claim.

## 1. Exact result and scope

Let F:R^d→R be a coercive real polynomial. Start with any supplied Borel probability μ, and use the known characteristic law

    μ_t=(Φ_t)_#[exp(−∫_0^t F(Φ_s(x))ds)μ/Z_t],
    Φ'_t=−∇F(Φ_t),       Z_t=∫exp(−∫_0^t F(Φ_s(x))ds)dμ.

The frozen limit theorem identifies its limiting law μ_∞ and its least occupied limiting critical energy c*. In particular, for every t>0 all polynomial moments exist,

    F≥c*    μ_t-almost everywhere,
    E(t)=μ_t(F)↓c*,       h(t)=E(t)−c*≥0,
    −h'(t)=D(t):=μ_t(|∇F|²)+Var_(μ_t)(F).              (1)

There exist constants ε∈(0,1], C>0 and θ∈[1/2,1), depending on F and c*, such that

    D(t)≥C h(t)^(2θ)   whenever t>0 and h(t)≤ε/2.       (2)

For every sufficiently large t,

    ∫_t^∞ sqrt(D(s))ds
       ≤h(t)^(1−θ)/(sqrt(C)(1−θ)).                     (3)

Consequently the declared transport/reaction action representation has finite length on **[t_0,∞) for every t_0>0**, for every initial probability. Its length on [0,∞) is finite when μ(F)<∞. Without that integrability, the initial segment can have infinite length; §5 gives an exact counterexample even for F=x²/2.

For each polynomial p and each t_0>0 there is a finite, generally nonalgorithmic constant M_p such that

    |μ_t(p)−μ_∞(p)|
      ≤sqrt(M_p) h(t)^(1−θ)/(sqrt(C)(1−θ))              (4)

whenever t≥t_0 and h(t)≤ε/2. This is an energy-controlled error bound for each fixed polynomial observable. It is not a uniform reconstruction bound over all degrees, initial laws or data perturbations.

## 2. The uniform inequality on a thin energy strip

The level L={x:F(x)=c*} is nonempty and compact. At every y∈L the local analytic gradient inequality supplies κ_y>0, θ_y∈[0,1) and a neighborhood U_y with

    |∇F(x)|≥κ_y |F(x)−c*|^θ_y.

At a noncritical y, this also follows directly from a positive lower bound on |∇F| in a small neighborhood. Thus no isolated-critical-point assumption is involved. The classical general statement used here is Absil–Mahony–Andrews, Lemma 2.1, printed p.533. [Primary author-hosted paper](https://sites.uclouvain.be/absil/Publi/Convergence_SIOPT/13-60526.pdf).

Take a finite subcover U_1,…,U_N of L, restrict to |F−c*|≤1, and set

    θ=max{1/2,θ_1,…,θ_N}<1,       κ=min_i κ_i>0.

Increasing the exponent on [0,1] weakens the right-hand side, so the common inequality holds in their union. There exists ε∈(0,1] such that the entire strip {0≤F−c*≤ε} lies in that union. Otherwise points outside the union with F(x_n)↓c* would have a convergent subsequence in the compact sublevel {F≤c*+1}, landing on L outside its open cover. Therefore

    |∇F(x)|≥κ(F(x)−c*)^θ
       whenever 0≤F(x)−c*≤ε.                          (5)

This is a finite-cover deduction from a classical finite-dimensional analytic inequality, not an imported Łojasiewicz theorem on a space of measures.

Now fix t with h(t)≤ε/2 and put u(x)=F(x)−c*≥0 on the law's support. On {u≤ε}, (5) gives |∇F|²≥κ²u^(2θ). On {u≥ε},

    |F−E|=u−h≥u/2,
    (F−E)²≥u²/4≥ε^(2−2θ)u^(2θ)/4.

Consequently

    |∇F|²+(F−E)²≥C u^(2θ),
    C=min{κ², ε^(2−2θ)/4}>0.

Integrating and applying Jensen to the convex power 2θ≥1 yields (2). All integrals are finite because the positive-time law has all polynomial moments and 2θ≤2. The variance term controls particles away from the target energy strip, including higher-energy critical points where the gradient itself vanishes.

The inherited double-well extinction example makes that role necessary: for F=(x²−1)²/4 and ν=(1−a)δ_1+aδ_0 with 0<a<1, the gradient term is zero while h=a/4 can be arbitrarily small and Var_ν(F)=a(1−a)/16>0. A corresponding bound using only μ(|∇F|²) would fail.

The support condition F≥c* comes from occupied eventual basins of the supplied initial measure. Null lower-energy basins remain null under the strictly positive finite-time weighting. It is not inferred from a small mean gap alone.

## 3. Energy rates and action length

By the inherited convergence, choose T>0 with h(T)≤ε/2. If h(t)>0, (1)–(2) give

    −d(h^(1−θ))/dt
       =(1−θ)h^(−θ)D
       ≥sqrt(C)(1−θ)sqrt(D).

Integrating to infinity, using h→0, proves (3). If h reaches zero, its nonnegativity and monotonicity force it to remain zero. Equation (1) then gives zero gradient and zero variance almost everywhere under the later laws; the characteristic flow is stationary and its action speed is zero. Integrating up to that first zero gives the same bound. No division by zero is used.

For h(T)>0, the scalar comparison h'≤−Ch^(2θ) gives the explicit cases

    h(t)≤h(T)exp(−C(t−T))                     if θ=1/2,

    h(t)≤[h(T)^(1−2θ)+C(2θ−1)(t−T)]^(−1/(2θ−1))
                                             if θ>1/2. (6)

If h(T)=0, use h≡0 on [T,∞) instead; the negative power of h(T) in the second formula is not evaluated at zero.

Thus the tail length and the fixed-observable bound (4) decay exponentially in the first case, and at least as t^(−(1−θ)/(2θ−1)) in the second. The common exponent and constant depend on the selected energy level; the entry time T depends on the initial law. No effective procedure for computing those constants is asserted.

### Precisely which action is controlled

For t>0 define the displayed fields

    v_t=−∇F,       α_t=E(t)−F.

They satisfy ∂_tμ_t+div(μ_tv_t)=α_tμ_t and μ_t(α_t)=0. With unit coefficients, their quadratic transport/reaction action and its length are

    A[a,b]=∫_a^b μ_t(|v_t|²+|α_t|²)dt=h(a)−h(b),
    L[a,b]=∫_a^b sqrt(μ_t(|v_t|²+|α_t|²))dt
          =∫_a^b sqrt(D(t))dt.                         (7)

For each a>0, finite energy dissipation controls every finite initial portion by Cauchy–Schwarz; (3) controls its infinite tail. If μ(F)<∞, dominated convergence gives E(t)→μ(F) as t↓0, because F(Φ_t)≤F initially and the weight is bounded above on bounded time intervals. Hence ∫_0^T D=μ(F)−E(T)<∞, and

    L[0,T]≤sqrt(T[μ(F)−E(T)]).

Finite initial energy is sufficient, not asserted necessary, for total length from zero. For an arbitrary initial probability only the positive-time/tail conclusion is unconditional.

These statements concern this admissible velocity/reaction action. They do not assert a smooth manifold of all probabilities, equality with a global fixed-rank distance, a tangent-cone classification, or physical-space total variation convergence. On finite positive distinct atoms they recover the inherited metric speed; on general laws they provide the stated action control directly.

## 4. Moment tail bounds from the inherited cometric

For polynomials p,q define

    B_t(p,q)=μ_t(∇p·∇q)+μ_t(pq)−μ_t(p)μ_t(q).

The known-law hierarchy gives μ'_t(p)=−B_t(p,F), and B_t(F,F)=D(t). Cauchy–Schwarz for the pair (∇p,p−μ_t(p)) in L²(μ_t;R^d⊕R) therefore gives

    |μ'_t(p)|≤sqrt(B_t(p,p))sqrt(D(t)).                 (8)

The frozen arbitrary-law theorem's positive-time bounds imply

    M_p:=sup_(s≥t_0)[μ_s(|∇p|²)+μ_s(p²)]<∞,
    B_s(p,p)≤M_p.

Indeed each of the displayed functions is polynomial, and the terminal-energy exponential envelope is uniform for s≥t_0. Integrating (8) and using the already-established moment limit μ_∞(p) proves (4). Constants and additive polynomial gauges cause no problem; for a constant p the exact derivative and error are zero.

The cometric formula is inherited. Its use here requires no invertible infinite moment matrix and no invented infinite-dimensional Riemannian structure.

## 5. An infinite initial-length control

Let F(x)=x²/2, and choose the initial law by x=sqrt(2Y), where Y has density

    ρ(y)=1/[y(log y)²],       y≥e.

This is a probability, since its integral equals one. Its initial energy is infinite. The exact flow and weight are

    X_t=x exp(−t),
    s=(1−exp(−2t))/2,       K_t=sY,
    dν_s(Y)=exp(−sY)ρ(Y)dY / ∫exp(−sy)ρ(y)dy.

Under the physical law, F(X_t)=exp(−2t)Y and hence

    D(t)≥Var(F(X_t))=exp(−4t)Var_(ν_s)(Y),
    ds=exp(−2t)dt.                                     (9)

For 0<s≤1/(2e²), the event L={e≤Y≤e²} has ν_s probability at least exp(−1/2)/2, since the normalizer is at most one. The event H={1/s≤Y≤2/s} has probability at least

    exp(−2)log2/[log(2/s)]².

This follows by bounding exp(−sY) below by exp(−2), log Y above by log(2/s), and integrating dY/Y over H. On H×L the difference of the two independent Y values is at least 1/(2s). The identity Var(Y)=E[(Y−Y')²]/2, using both orientations, gives a constant c>0 with

    Var_(ν_s)(Y)≥c/[s²log²(2/s)].

Combining with (9),

    ∫_(0+) sqrt(D(t))dt
       ≥sqrt(c)∫_(0+) ds/[s log(2/s)]=∞.               (10)

Every positive-time law nevertheless has all moments and the finite tail length proved above. The divergence is an initial-time property of this chosen path. In particular, this infinite-energy initial law is not an all-moment initial hierarchy: any all-moment initial law has finite polynomial energy and is covered by the finite-length-from-zero result. The control does not claim an infinite distance between its endpoints under an action infimized over other paths.

## 6. Inheritance and evidence

The copied, hash-bound sources are listed in INPUT_BINDINGS.json. The frozen limit theorem and its independent review supply the actual characteristic law, endpoint selection, positive-time polynomial bounds, and h→0. The joint-atomic and spherical-interface predecessors own the metric/cometric and unit transport/reaction conventions. The Fisher-endpoint report concerns a specific all-moment lognormal reference and proves finite length for that different boundary path; it does not give an arbitrary-initial-law length theorem.

A bounded search of available top-level RESULT.md files for finite/action length, uniform analytic inequalities and the present ensemble dissipation bound found those antecedents, not (2)–(4). This is local deduplication, not field-priority research. The primary local analytic inequality is classical; the uniformization, low/high energy split, scalar integration and moment-cometric consequence are the explicit transported deduction here.

The short exact checker verifies derivative and normalization identities used in the proof and the initial-length control. These controls are supplementary; no numerical sampling campaign or universal theorem by enumeration is claimed. A successful run checks copied bindings and, optionally, unchanged originals. Independent review is separate. Frozen predecessors and T20 status are unchanged.
