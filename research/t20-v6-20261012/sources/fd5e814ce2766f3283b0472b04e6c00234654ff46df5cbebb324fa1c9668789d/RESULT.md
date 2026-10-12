# Exact limits of polynomial gradient transport and selection

10 October 2026 UTC. Additive ordinary mathematical research within ACTIVE T20. The parent identified the unresolved question and proposed the analytic-gradient route. This report supplies the proof and its finite-atomic transport. It does not claim field priority, independent review, formal-kernel verification, protected integration, actual noetic identification, or programme closure. T20 remains open.

## 1. Result and inheritance

For every coercive real polynomial F and every finite positive initial atomic probability, **each gradient particle converges to one critical point, every particle has finite integrated excess energy, and every labelled mass has an exact limit**. After merging coincident winning endpoints, the entire law converges, rather than merely having classified subsequential limits.

Write X'_j=−∇F(X_j), X_j(0)=z_j, and let a_j>0, Σa_j=1. Set

    q_j = lim_(t→∞) X_j(t),       c_j = F(q_j),
    I_j = ∫_0^∞ [F(X_j(t))−c_j]dt,
    α_j = a_j exp(−I_j),          c* = min_j c_j,
    S = {j:c_j=c*},               A* = Σ_(j∈S) α_j.

All I_j are finite and nonnegative, so every α_j and A* is strictly positive. The solution of

    w'_j = −w_j(F(X_j)−E),        E=Σ_j w_jF(X_j),
    w_j(0)=a_j

satisfies

    lim_(t→∞) w_j(t) = α_j/A*   if j∈S,
                         0      if j∉S.                 (1)

For each losing label there is the stronger exact asymptotic

    lim_(t→∞) exp((c_j−c*)t)w_j(t) = α_j/A*.             (2)

If Q={q_j:j∈S} is the set of distinct winning endpoints, then

    μ_t = Σ_j w_j(t)δ_(X_j(t)) → μ_∞ = Σ_(q∈Q) b_qδ_q,
    b_q = (Σ_(j∈S:q_j=q) α_j)/A* > 0.                   (3)

The convergence is weak, in every polynomial moment, and in every Wasserstein distance W_p with 1≤p<∞. It is generally **not** convergence in total variation on physical space. The limiting rank is exactly |Q|.

The classical input is the analytic Łojasiewicz gradient inequality and its finite-length argument. The finite-atomic exponential normalization is inherited. The addition here is their combination into (1)–(3), with explicit tail estimates, exact losing prefactors, and the compatible hierarchy/boundary scope. None of these classical ingredients is presented as a new general convergence theorem in optimization.

Section 5 proves the parent's further proposed extension: for **any supplied Borel probability**, the known characteristic law has an explicit whole-law limit selected by its least positive-mass critical-energy basin. No initial moment assumption is needed for weak convergence, for positive-time finiteness of all moments, or for asymptotic convergence of every polynomial moment and every finite W_p. This stronger forward statement does not solve reverse existence for arbitrary abstract hierarchies.

### Local deduplication

`LOCAL_DEDUP.json` records a bounded search of 154 top-level RESULT.md files. The six inspected reports in `INPUT_BINDINGS.json` are copied and hash-bound; no predecessor is edited.

- `joint-atomic-gradient-lift-20261010/RESULT.md`, §7, proves compactness, critical subsequential limits and elimination of higher limiting energies; it explicitly leaves general particle convergence and same-energy weight convergence unasserted. Its strongly convex case already has positive limiting labelled masses.
- `joint-atomic-geometry-independent-review-20261010/REVIEW.md`, §6, confirms precisely that scope.
- `complete-flow-finite-rank-20261010/RESULT.md`, §9, owns the finite-atomic reverse lift under locally bounded full path rank, forward completeness and finite-time injectivity.
- `radial-quartic-gradient-reverse-lift-20261010/RESULT.md`, §9, already gives whole-law convergence and an explicit reweighted initial-law limit for its particular radial quartic, even for infinite initial laws. This report does not rebrand that specialization as new.
- `dissipative-polynomial-gradient-reverse-lift-20261010/RESULT.md`, §§1–2, removes the path-rank promise under its additional SOS certificates. That is a different reverse-existence improvement, compatible with the present long-time theorem when the initial rank is finite.
- `gradient-discretization-fidelity-20261010/RESULT.md` has conditional one-step preservation and consistency, without a global numerical-convergence theorem. The present exact continuous-flow theorem is not a convergence theorem for its iterates.

The local search is not a literature-priority survey.

## 2. Precise particle theorem

Let F:R^d→R be a coercive real polynomial, with d≥1, and let finitely many z_j∈R^d be given. Distinctness is not needed for particle or weight convergence; it is needed to identify labelled states modulo permutations with an exact-r atomic stratum. Coincident initial positions can first be merged.

For each j there is a unique solution X_j:[0,∞)→R^d. It stays in the compact sublevel {F≤F(z_j)}. There is one q_j such that

    X_j(t)→q_j,       ∇F(q_j)=0,       F(X_j(t))↓c_j=F(q_j).

The trajectory has finite Euclidean length, and I_j above is finite. No isolated-critical-point, Morse, convexity, nondegenerate-Hessian or local-minimum assumption is required. In particular, a positive-dimensional critical set causes no difficulty: a single trajectory still selects one point.

For a nonstationary particle put h(t)=F(X(t))−c>0. There are T≥0, κ>0 and θ∈[1/2,1) such that for all t≥T,

    ||∇F(X(t))|| ≥ κ h(t)^θ.                            (4)

For every such t,

    ∫_t^∞ ||X'(s)||ds ≤ h(t)^(1−θ)/(κ(1−θ)),            (5)
    ||X(t)−q|| ≤ h(t)^(1−θ)/(κ(1−θ)),
    R(t):=∫_t^∞ h(s)ds ≤ h(t)^(2−2θ)/(κ²(2−2θ)).        (6)

If θ=1/2,

    h(t) ≤ h(T) exp(−κ²(t−T)).                          (7)

If 1/2<θ<1,

    h(t) ≤ [h(T)^(1−2θ)+κ²(2θ−1)(t−T)]^(−1/(2θ−1)).   (8)

The exponent 1/(2θ−1) is strictly greater than one. Thus the energy gap is integrable in every case. Formula (6) proves this directly, without first integrating a big-O estimate. It gives R(t)=O(t^(−(2−2θ)/(2θ−1))) in the algebraic case and an exponential bound in the θ=1/2 case. The constants, exponents and entry times can depend on the particle; no uniform algorithm to compute them is supplied.

### Proof of compactness and a critical cluster point

The polynomial vector field is locally Lipschitz. Along a solution,

    dF(X(t))/dt = −||∇F(X(t))||².                       (9)

Coercivity gives compact sublevels and a finite lower bound for F. No finite-time escape is possible, so local existence extends globally. The energy decreases to some finite c, and ∫_0^∞||∇F(X)||²dt=F(z)−c<∞.

On the compact sublevel, the gradient and Hessian are bounded. Therefore the time derivative of ||∇F(X)||², namely −2∇F(X)^T Hess F(X)∇F(X), is bounded. A nonnegative integrable uniformly continuous function tends to zero: otherwise uniformly wide positive-height spikes contradict its finite integral. Consequently ∇F(X(t))→0. Any cluster point q has ∇F(q)=0 and F(q)=c.

### The classical analytic inequality and trapping argument

Near q, real analyticity supplies constants κ>0 and θ_0∈[0,1) with

    ||∇F(x)|| ≥ κ |F(x)−F(q)|^θ_0.

This is the classical Łojasiewicz gradient inequality. See Absil–Mahony–Andrews, Lemma 2.1 and §2, printed pp.533–535, [author-hosted paper](https://sites.uclouvain.be/absil/Publi/Convergence_SIOPT/13-60526.pdf). Shrink the neighborhood so |F−c|≤1 and take θ=max{θ_0,1/2}; increasing the exponent on [0,1] weakens the right-hand side and preserves the inequality. This explains the convention θ∈[1/2,1) used here without claiming an optimal exponent.

If h vanishes at some finite time, (9) and its limiting value force h≡0 thereafter and X is stationary there. Uniqueness of the locally Lipschitz autonomous ODE then forces the earlier trajectory to have been stationary too. Thus a genuinely nonstationary trajectory has h>0 at every finite time.

On any interval for which X stays in the inequality neighborhood,

    −d(h^(1−θ))/dt
      = (1−θ)h^(−θ)||∇F(X)||²
      ≥ κ(1−θ)||∇F(X)||
      = κ(1−θ)||X'||.                                  (10)

Choose a ball B_r(q) contained in that neighborhood. Since q is a cluster point and h→0, choose T with ||X(T)−q||<r/2 and h(T)^(1−θ)/(κ(1−θ))<r/2. A first exit from B_r(q) would require travel at least r/2, while integrating (10) up to that exit gives length less than r/2. Hence there is no exit.

Integrating (10) on [t,u] and then taking u→∞ gives (5). The tail length tends to zero, so X is Cauchy and converges. Its cluster point was q, which identifies the limit. This proof uses F−c≥0 **along this trajectory**, not in a full neighborhood of q; a saddle endpoint is allowed.

### Integrated excess energy and the exponent cases

From (4) and (9),

    h' ≤ −κ²h^(2θ).

Solving this scalar differential inequality yields (7) or (8). More directly,

    −d(h^(2−2θ))/dt
      = (2−2θ)h^(1−2θ)||∇F(X)||²
      ≥ κ²(2−2θ)h.                                    (11)

Integration proves (6). The integral on [0,T] is finite by continuity; adding it proves I<∞. Stationary particles have h≡0 and I=0. A convention writing the inequality as ||∇F||≥κh^(1−σ) uses σ=1−θ∈(0,1/2]; the exponents must not be interchanged. An exponent equal to one would give only a borderline O(1/t) comparison and would not establish integrability by this argument; analyticity supplies the strict θ<1 needed here.

The same proof applies to a real-analytic F on an open domain if the forward trajectories remain in a compact subset of that domain. Coercivity is a sufficient compactness mechanism, not an indispensable feature of the convergence argument. Mere C∞ smoothness with bounded trajectories does not supply the analytic conclusion; the cited paper's §2 gives a smooth bounded nonconvergent gradient trajectory.

## 3. Exact normalization and the limiting weights

Let f_j(t)=F(X_j(t)) and K_j(t)=∫_0^t f_j(s)ds. Direct differentiation, or the inherited finite-atomic formula, gives

    Z(t)=Σ_j a_jexp(−K_j(t)),
    w_j(t)=a_jexp(−K_j(t))/Z(t)>0.                       (12)

Let R_j(t)=∫_t^∞(f_j(s)−c_j)ds. The particle theorem gives R_j(t)↓0 and

    K_j(t)=c_jt+I_j−R_j(t).

Consequently the following identity, not merely an asymptotic approximation, holds at every finite t:

    D(t)=exp(c*t)Z(t)
        =Σ_l α_l exp(R_l(t)) exp(−(c_l−c*)t),
    w_j(t)=α_j exp(R_j(t)) exp(−(c_j−c*)t)/D(t).         (13)

Because there are only finitely many particles, D(t)→A*. Formula (1) follows for winners and (2) follows for losers. In particular, different critical endpoints with the same minimal energy both survive with strictly positive masses. A particle cannot lose all its mass merely because it approaches that shared energy more slowly: its total excess is still finite. Among winners,

    lim w_i(t)/w_j(t) = (a_i/a_j)exp(−I_i+I_j).          (14)

There is no assumption that I_i=I_j or that masses return to their initial ratios.

For an explicit error estimate, write

    B(t)=Σ_(j∈S) α_j(exp(R_j(t))−1)
         +Σ_(j∉S) α_jexp(R_j(t))exp(−(c_j−c*)t).

Then B(t)≥0, D(t)=A*+B(t), and for i∈S,

    |w_i(t)−α_i/A*|
      ≤ α_i(exp(R_i(t))−1)/A* + α_iB(t)/(A*)².           (15)

If there are losers, let δ=min_(j∉S)(c_j−c*)>0. For large t, B(t)=O(Σ_(j∈S)R_j(t)+exp(−δt)); the losing R_j are bounded and need not be included in the first term. Thus the winner convergence inherits the integrated-gap rates in (6). If there are no losers, omit the exponential term. No uniform positive δ over varying initial data is asserted.

### An exact integrated ensemble gap

Differentiating (12) gives −(log Z)'=E. Since Z(0)=1,

    ∫_0^t(E(s)−c*)ds = −log D(t).

Here E(t)≥c*, D(t) decreases from 1 to A*, and

    ∫_0^∞(E(t)−c*)dt = −log A* < ∞.                    (16)

This identity also confirms A*≤1, already clear from α_j≤a_j. The remaining ensemble tail is log(D(t)/A*). The normalization is essential: c* is subtracted before integration; ∫F(X_j) itself need not be finite when c_j≠0.

## 4. The limiting law and the atomic geometry

All positions lie in one compact set K, the finite union of initial sublevels. For a continuous function φ on K, the finite sum in (12) tends to the sum of its limits. Dropping zero limiting weights and merging equal q_j proves (3). Every polynomial is continuous and bounded on K, giving convergence of every polynomial moment. On one common compact set, weak convergence implies W_p convergence for each finite p; alternatively, couple the convergent labelled masses and positions and bound the unmatched mass by the diameter of K.

The limit is a positive law with exactly |Q| atoms. All its atoms are critical points of F with the common value c*, so it is stationary for the inherited gradient field in its own true-rank stratum. The limiting law need not be a local minimum of that objective.

At every finite time, distinct initial positions remain distinct by ODE uniqueness, and all weights remain positive by (12). Thus the full atomic rank stays r at finite times. A limit may have fewer atoms because losing weights vanish, winning endpoints coincide, or both. These are limiting mechanisms, not finite-time births or deaths.

The whole lifted trajectory also has finite length for the inherited metric

    G((u,v),(u,v))=Σ_j u_j²/w_j+Σ_jw_j||v_j||².

Indeed its transport length is bounded by Σ_j∫||X'_j||<∞. For the reaction block set y_j=2√w_j, so |y'_j|=√w_j|f_j−E|. For a winner, |f_j−E|≤(f_j−c*)+(E−c*), whose integral is finite by the particle theorem and (16). For a loser, √w_j decays exponentially by (2), while f_j and E stay bounded. Hence Σ_j∫|y'_j|<∞, and the total G length is finite. This gives a Cauchy curve in the metric completion of its stratum; it does not install a smooth metric across all ranks, identify that completion globally, or prove equality with an ambient transport/reaction distance.

### Transport back to the hierarchy

If an abstract normalized full-square-positive hierarchy satisfies the inherited forward-complete/lower-killing reverse-lift hypotheses, including locally uniform bounded **full path rank**, its forced representation is (12). Therefore (1)–(16) apply to its unique admitted finite-atomic trajectory and to its exact moment coordinates. An initial finite-rank condition alone is not silently substituted for that path hypothesis for arbitrary coercive F.

For the separately proved SOS-dissipative class, the stronger reverse lift in the inspected report supplies the representation from finite initial rank without a future rank promise. The present theorem then applies after that representation has been obtained. Section 5 also applies to any infinite representing law actually supplied by that reverse theorem. It does not enlarge that certificate class or establish unrestricted reverse existence for abstract hierarchies at general coercive F.

In the programme's terminology, this is an additional consequence of the already defined mathematical transport into atomic/noetic coordinates. Analytic convergence does not itself authenticate sources, select a true objective, identify a real cognitive or metaphysical bearer, prove actual correction efficacy, or grant a closure decision.

## 5. Extension to an arbitrary supplied initial probability

This section concerns the **forward characteristic law of a specified Borel probability μ on R^d**. It assumes neither finite rank nor any moment of μ. The polynomial F remains coercive. Let Φ_t(x) be its forward gradient flow and define

    K_t(x)=∫_0^t F(Φ_s(x))ds,
    Z_t=∫ exp(−K_t(x))dμ(x),
    μ_t=(Φ_t)_# [exp(−K_t)μ/Z_t].                       (17)

Since m=min F is finite, 0<exp(−K_t(x))≤exp(−mt), so 0<Z_t<∞ for each finite t. Thus (17) always defines a probability. No assertion that every formal hierarchy is represented by (17) is used or obtained.

### Finitely many critical energy levels and measurable limits

The set C=F({∇F=0}) of critical values is finite. One short proof is: {∇F=0} and its image under the polynomial F are semialgebraic by Tarski–Seidenberg; Sard's theorem makes that image Lebesgue-null; a semialgebraic subset of R is a finite union of points and intervals, so no intervals can occur. Equivalently, the critical set has finitely many semialgebraic path components and F is constant along each piecewise C¹ path in it. Coercivity guarantees a global minimizer, so C is nonempty. The semialgebraic facts are recorded in Kurdyka, §1; the needed scalar Sard statement is in Sard's original article, p.883. [Kurdyka primary paper](https://aif.centre-mersenne.org/item/10.5802/aif.1638.pdf), [Sard primary paper](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/sard.pdf).

By §2, for every x there exist

    q(x)=lim_(t→∞)Φ_t(x),        c(x)=F(q(x))∈C,
    I(x)=∫_0^∞[F(Φ_s(x))−c(x)]ds <∞.

The map q is Borel as the pointwise limit of the continuous maps Φ_n. Hence c is Borel; the finite-time integrals and their increasing excess limits make I Borel as well. No semialgebraicity of the flow or basin map is assumed. Define the Borel basins B_c={x:c(x)=c} and

    c*=min{c∈C:μ(B_c)>0},       B*=B_(c*),
    A*=∫_(B*) exp(−I(x))dμ(x)>0.                        (18)

Finiteness of C guarantees that this least positive-mass level is attained. Its basin has positive μ mass and exp(−I)>0 everywhere, proving A*>0 without assuming ∫I dμ<∞ or a uniform bound on I. Lower-level basins, if present, have μ mass zero and are discarded in all almost-everywhere inequalities below.

### Exact law selection by dominated convergence

Put I_t(x)=∫_0^t[F(Φ_s(x))−c(x)]ds and

    g_t(x)=exp(c*t−K_t(x))
          =exp(−(c(x)−c*)t−I_t(x)),
    g_∞(x)=1_(B*)(x)exp(−I(x)),
    D_t=∫g_t dμ=exp(c*t)Z_t.

On the complement of the null lower-level basins,

    0≤g_t≤1,        g_t→g_∞,        D_t↓A*>0.           (19)

The decreasing assertion follows also from F(Φ_t(x))≥c(x)≥c*. Dominated convergence gives both D_t→A* and L¹(μ) convergence of g_t. Consequently the probability on **initial coordinates**

    ν_t=g_tμ/D_t

converges in total variation to ν_∞=g_∞μ/A*. For any bounded continuous φ on R^d,

    ∫φ dμ_t = [∫φ(Φ_t(x))g_t(x)dμ(x)]/D_t
       → [∫_(B*) φ(q(x))exp(−I(x))dμ(x)]/A*.

Thus the full physical law has the explicit limit

    μ_∞ = q_# [1_(B*)exp(−I)μ/A*].                     (20)

It is carried by the compact critical level {y:∇F(y)=0,F(y)=c*}; it may be nonatomic. Formula (3) is exactly (20) for a finite initial law, including endpoint aggregation. Physical-space total variation convergence still need not hold.

For any losing critical level c with μ(B_c)>0,

    lim_(t→∞) exp((c−c*)t)ν_t(B_c)
       = [∫_(B_c)exp(−I)dμ]/A* >0.                     (21)

This is a statement about labels by eventual basin, not an assertion that spatial basins are inferred from finitely many observations. If losing positive-mass levels exist, their finite minimum gap δ>0 gives ν_t(R^d\B*)≤exp(−δt)/A*. No universal rate for the remaining within-basin reweighting or positional convergence is claimed.

### A polynomial sublevel envelope

We give the growth argument explicitly rather than assume a quadratic lower bound on an arbitrary coercive polynomial. Set

    M(s)=max{1+|y|²:F(y)≤m+s},       s≥0.

The maximum is finite and attained, and M is nondecreasing. Its graph is described by a first-order polynomial formula: an attaining y exists and every z in the sublevel satisfies 1+|z|²≤M(s). Tarski–Seidenberg therefore makes this graph semialgebraic.

Take a quantifier-free description of the graph involving finitely many nonzero polynomials in (s,u). At every graph point at least one of those polynomials must vanish: if none did, every sign in the description would be locally constant and the graph would contain an open neighborhood, impossible for the graph of a function. Their nonzero product P(s,u) therefore vanishes at u=M(s).

Write P(s,u)=a_d(s)u^d+⋯+a_0(s). It must have d≥1, since a nonzero polynomial in s alone cannot vanish for all s≥0. For sufficiently large s the nonzero polynomial a_d(s) never vanishes. Cauchy's elementary root bound gives

    M(s)≤1+max_(i<d)|a_i(s)/a_d(s)|≤C(1+s)^N

there, for a finite integer N and C>0. On the remaining bounded s interval, monotonicity bounds M, so increasing C gives this inequality for all s≥0. No exponent is claimed optimal or algorithmically computed. In particular, for any polynomial p there are constants C_p,N_p such that

    |p(y)|≤C_p(1+F(y)−m)^N_p       for every y.          (22)

This proof uses only quantifier elimination and an elementary polynomial root bound; it does not invoke an unsupported coercivity rate.

### Positive-time moment regularization and convergence without initial moments

For μ-almost every initial x, put u_t(x)=F(Φ_t(x))−c*≥0. Energy is decreasing, so

    g_t(x)=exp(−∫_0^t u_s(x)ds)≤exp(−t u_t(x)).         (23)

Combining (22), with the harmless constant shift c*−m, and (23), gives for every fixed t_0>0 and all t≥t_0,

    |p(Φ_t(x))|g_t(x)
       ≤C'_p(1+u_t(x))^N_p exp(−t_0u_t(x))
       ≤C'_p sup_(u≥0)(1+u)^N_p exp(−t_0u)<∞.          (24)

The final constant is independent of x and t≥t_0, so it is μ-integrable for **every** initial probability. Thus μ_t has every absolute polynomial moment at each t>0. Dominated convergence in the numerator of (17), together with (19), proves

    ∫p dμ_t → ∫p dμ_∞                                (25)

for every polynomial p, without an initial-moment hypothesis. The same argument applies to |y|^p for every finite real p≥1 by increasing the integer power in (22). Weak convergence together with convergence of these p-th absolute moments gives W_p(μ_t,μ_∞)→0. This concerns t>0; it does not assert a finite W_p distance to an initial law having infinite p-th moment, or finite polynomial coordinates at t=0.

For completeness the W_p implication also follows by an explicit coupling. Couple the common part of ν_t and ν_∞ at the same starting x and transport it to (Φ_t(x),q(x)). Its cost tends to zero by dominated convergence. Couple the remaining equal masses arbitrarily; their cost is bounded by 2^(p−1) times their p-th moment sums, which tend to zero by weighted L¹ convergence. On B*, g_∞≤g_t, while off B* g_∞=0; hence both initial-coordinate densities are bounded by g_t/A*, and (24) supplies the needed domination. The relevant q(x) on B* lie in one compact critical level.

The ensemble energy E(t)=∫F dμ_t is finite for t>0. Differentiating D_t on any interval bounded away from zero is justified by u_tg_t≤u_texp(−t u_t), which is uniformly bounded there. It gives D'_t=−(E(t)−c*)D_t. Also D_t→1 as t↓0 by dominated convergence. Therefore the improper identity survives unchanged:

    ∫_0^∞(E(t)−c*)dt=−log A*<∞.                       (26)

E(0) itself may be infinite. The integral in (26) does not require it to be finite.

The abstract hierarchy can inherit (20)–(26) only after its representing law and characteristic formula are justified by a separate reverse theorem. Positive-time moment regularization of (17) is not by itself such a reverse theorem.

Conversely, for this **known** forward law, differentiating (17) gives, for every polynomial p and every t>0,

    dμ_t(p)/dt=−μ_t(∇F·∇p)−μ_t(Fp)+μ_t(F)μ_t(p).

This is justified on a neighborhood of any positive time by applying (24) to the polynomial ∇F·∇p+Fp, along with the denominator derivative. The coordinates are C¹ there. If μ initially has all absolute polynomial moments, the bound 1+|Φ_t(x)|²≤C(1+F(x)−m)^N from the sublevel argument provides an integrable polynomial-in-x envelope on intervals including zero; exp(−K_t)≤exp(−mt) provides the weight bound. Dominated differentiation then extends the coordinates and their right derivatives to t=0. These are forward existence assertions from supplied measures, not reverse-existence or initial-moment determinacy assertions.

## 6. Exact controls and countercontrols

These examples check the formulas and delimit the theorem. They are ordinary mathematical examples; the accompanying executed symbolic controls are not substituted for the universal proofs.

### Flat minima still have integrable excess energy

For F_m(x)=x^(2m)/(2m), m≥2, the exact solution is

    X(t)=z/[1+(2m−2)z^(2m−2)t]^(1/(2m−2)),
    I=z²/(4m),           R(t)=X(t)²/(4m).

For z=0 these expressions mean the stationary zero solution. The identity −d(X²/(4m))/dt=F_m(X) proves the integrated-gap formula. The gradient inequality is an equality with θ=(2m−1)/(2m) and κ=(2m)^θ. Thus h(t) has decay exponent m/(m−1)>1, while the exponent approaches the borderline one as m grows. There is no uniform exponential rate over coercive polynomials. For m=1, X=ze^(−t), I=z²/4 and R=X²/4 give the θ=1/2 control. The quadratic and quartic special cases are inherited controls; the general expression here illustrates the exponent convention.

### Equal endpoint energies need not preserve initial mass ratios

For the coercive double well F(x)=(x²−1)²/4,

    X(t)=z/[z²+(1−z²)exp(−2t)]^(1/2),       z≠0,
    q=sign(z),      c=0,
    I(z)=(z²−1−log(z²))/8.

The denominator is positive for t≥0. Since log u≤u−1, I(z)≥0, with equality only at |z|=1. A primitive calculation gives

    J'(x)=(x−1/x)/4,
    J'(x)[x(1−x²)]=−F(x),
    J(x)=(x²−1−log(x²))/8.

Hence R(t)=J(X(t)). With z_1=−1, z_2=2 and a_1=a_2=1/2, both energies tend to zero at different endpoints, but I_1=0 and I_2=(3−log4)/8>0. The limiting weight at −1 is 1/(1+exp(−I_2))>1/2. Endpoint energy equality retains both labels without erasing transient energy costs. If z_1=−b and z_2=b, the equal histories do preserve the initial ratio while the endpoints remain distinct.

### The selected energy can be a nonglobal local minimum

Let

    F(x)=x⁴/4−x³/3−x²,
    F'(x)=x(x−2)(x+1).

This coercive polynomial has strict local minima at −1 and 2, with

    F(−1)=−5/12,        F(2)=−8/3,        F(0)=0,
    F''(−1)=3,          F''(2)=6.

Every initial z<0 converges to −1: on (−∞,−1) the velocity −F' is positive, and on (−1,0) it is negative; uniqueness prevents crossing the equilibrium. Thus any finite family initially in (−∞,0), including nonstationary labels, has c*=−5/12>min F=−8/3. The weight dynamics selects the least limiting energy **among the supplied trajectories**, not a globally best basin absent from the initial support.

### Even a nonstationary trajectory can converge to a saddle

Let F(x,y)=(x²−1)²/4+y²/2 and start at (0,z), z≠0. Then

    X(t)=(0,ze^(−t)),      q=(0,0),      c=1/4,
    I=z²/4,               Hess F(q)=diag(−1,1).

The energy strictly decreases, but the endpoint is a saddle. Starting two atoms at (0,1) and (0,−1) gives distinct finite-time positions, identical energies and fixed positive weights; both positions converge to that same saddle. Their limiting law is δ_(0,0). Thus neither particle convergence nor limiting stationarity implies local minimization.

### Mass extinction and collision are different rank losses

For the double well, start three atoms at −1, 1 and 0 with positive masses a_−,a_+,a_0. The positions are stationary, their energies are 0,0,1/4, and

    w_0(t)=a_0exp(−t/4)/(a_−+a_++a_0exp(−t/4)),
    w_±(t)=a_±/(a_−+a_++a_0exp(−t/4)).

The limiting rank is two, solely through mass extinction. By contrast the preceding saddle example has no losing masses and loses rank solely through collision. Aggregation of equal endpoints is necessary in (3).

### The physical law can lose information without total variation convergence

For F=x²/2 and z≠0, δ_(ze^(−t)) converges weakly and in every moment to δ_0, but its total variation distance from δ_0 is one for every finite t, under the convention d_TV(μ,ν)=sup_A|μ(A)−ν(A)|. All such initial Dirac laws have the same limit. Finite-time injectivity on the actual forward image is compatible with a many-to-one limiting map. Convergence of weights on a finite **label space** does give total variation convergence there; pushing those labels to moving spatial positions is a different assertion.

### Selection can be discontinuous when a lower basin first receives mass

In the unequal-well polynomial above take a=−1 and b=2, with Δ=F(a)−F(b)=9/4>0. The initial law μ_0=δ_a is stationary and has limit δ_a. For every 0<ε<1,

    μ_ε=(1−ε)δ_a+εδ_b

has limiting law δ_b. At finite time its weight at b is

    v_ε(t)=ε/[ε+(1−ε)exp(−Δt)].

For 0<ε<1/2 the half-mass crossover is exactly t=log((1−ε)/ε)/Δ. At every fixed finite t, v_ε(t)→0 as ε↓0, whereas lim_(t→∞)v_ε(t)=1 for every ε>0. Hence the infinite-time selection map is discontinuous at δ_a, and the two orders of limits disagree. This is a missing-lower-basin and infinite-horizon sensitivity control, not a failure of the finite-time flow theorem or a claim of global minimization from arbitrary initial support.

### An arbitrary-law limit need not be finite atomic

For F(x,y)=(x²+y²−1)²/4, every point on the unit circle is critical with energy zero. Normalized arclength on that circle is a stationary nonatomic probability, so (20) can have infinite support even though there are only finitely many critical **values**. Finitely many levels do not mean finitely many endpoints.

## 7. Sources and evidence boundaries

Łojasiewicz, *Sur la géométrie semi- et sous-analytique*, Annales de l'Institut Fourier 43(5), 1575–1595 (1993), p.1592, discusses the analytic gradient inequality and a local trajectory theorem with a nonnegative analytic function. The retrieved inequality-line OCR is imperfect, so the operative general inequality statement in this report is the unambiguous Lemma 2.1 in the next source. In particular, a nonnegative-neighborhood hypothesis is not imposed at saddle endpoints. [Primary article](https://doi.org/10.5802/aif.1384), [journal PDF](https://aif.centre-mersenne.org/item/10.5802/aif.1384.pdf).

Absil, Mahony and Andrews, *Convergence of the Iterates of Descent Methods for Analytic Cost Functions*, SIAM J. Optim. 16(2), 531–547 (2005), Lemma 2.1 and Theorem 2.2, give the local inequality and continuous finite-length trapping argument. This report specializes the exact Euclidean gradient flow and derives (11) and the normalization consequences directly. Their author's page reports an erratum to the **discrete** Proposition 3.3; that proposition is not used. Their §2 smooth counterexample is only a scope warning, not an executed control in this packet. [Author-hosted paper](https://sites.uclouvain.be/absil/Publi/Convergence_SIOPT/13-60526.pdf), [author record and erratum](https://sites.uclouvain.be/absil/2005.901).

Kurdyka, *On gradients of functions definable in o-minimal structures*, Annales de l'Institut Fourier 48(3), 769–783 (1998), §1, pp.771–772, records the projection, one-dimensional finiteness, quantifier and image properties used in §5, including the semialgebraic example via Tarski–Seidenberg. Its Proposition 2 concerns bounded domains and is **not** used to assert a global asymptotic-critical-value theorem. [Primary journal PDF](https://aif.centre-mersenne.org/item/10.5802/aif.1638.pdf).

Sard, *The measure of the critical values of differentiable maps*, Bull. Amer. Math. Soc. 48 (1942), 883–890, p.883, gives the needed nullity of scalar critical values at sufficient differentiability. A polynomial has the required differentiability in every finite dimension. The deduction from nullity plus semialgebraicity to finiteness is made explicitly above. [Primary article scan](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/sard.pdf).

`check_exact.py` checks the energy-tail derivative identity, scalar comparison solutions, exact monomial/double-well/quadratic controls, the unequal-well and saddle countercontrols, and exponential normalization/merging algebra. Reports list only controls actually executed. Copied input hashes are checked on every run; an optional original-root check verifies the inspected predecessors remain unchanged. No numerical simulation, inferred numerical rate, automatic basin solver, computed Łojasiewicz exponent for arbitrary F, or formal proof checker is claimed. The universal theorem rests on the written argument and the identified classical analytic inequality.

The unresolved qualification in the ancestor's §7 is therefore strengthened for finite atomic coercive-polynomial flows, and extended to the forward law of every supplied probability. The ancestor remains frozen and correct as a deliberately weaker statement. This additive result has no authority to close T20.
