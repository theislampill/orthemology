# Correlated-target fixed-marginal correction: independent derivation

11 October 2026 UTC. Bounded mathematical review of the new correlated-target extension. This is not an audit-governor action and supplies no protected edit, integration, formal-kernel, external peer-review, or closure authority. The derivation below was completed separately from the author and root checker implementations. The problem statement and anticipated multiplier/ODE tests were supplied by the parent. The reviewer does not claim a blind discovery of those results.

## Verdict on the proposed mathematics

The proposed projection, Gaussian ODE, global existence argument, and convergence conclusion are correct under the inherited unit transport/centered-reaction tangent conventions. Full conditional y-score terms must be retained. A product-target formula applied using only conditional KL does not preserve the marginal for general correlated targets.

## 1. Declared target and first variation

Let Y be standard normal. Write the current centered Gaussian law as

    Z = bY + e,    e independent of Y,    e ~ N(0,s),    s>0,

and the target as Z* conditional on Y=y distributed as N(βy,τ), τ>0. Thus the joint covariances are [[1,b],[b,b²+s]] and [[1,β],[β,β²+τ]]. Set d=b−β. The fixed target marginal is standard normal, but the target need not be a product.

The log density ratio is

    q = ½ log(τ/s) + (e+dy)²/(2τ) − e²/(2s),
    E = KL(μ||π) = ½[(s+d²)/τ − 1 + log(τ/s)],
    h(y) = Eμ[q|Y=y] = ½[(s+d²y²)/τ − 1 + log(τ/s)].

Spatial differentiation with z held fixed is ∂y = ∂/∂y − b∂/∂e. Consequently

    Eμ[∂y q|Y=y] = −βdy/τ.

This is zero in the predecessor product-target problem but generally nonzero here. With Kμ f = −div(μ∇f)+μ(f−μf), integration in z therefore gives

    ν⁻¹ T_*Kμq = −ν⁻¹∂y(ν E[∂yq|Y]) + h−E
                = d(b−3β)(y²−1)/(2τ).

The standard-normal centered quadratic y²−1 has eigenvalue 3 for −ν⁻¹∂y(ν∂y)+I. Hence the centered horizontal potential is

    φ(y) = d(b−3β)(y²−1)/(6τ),
    Kνφ = T_*Kμq.

The inherited full tangent coisometry makes −Kμ(q−φ) the true ambient minimum-action constrained gradient. This is not a new proof of the inherited quotient theorem or merely a Gaussian moment projection.

## 2. Full density equality

Set Σ=[[1,b],[b,b²+s]], Σ*=[[1,β],[β,β²+τ]], and

    B = (Σ*)⁻¹ − Σ⁻¹ − [d(b−3β)/(3τ)] E11.

The corrected quadratic potential, modulo constants, is xᵀBx/2. Its fields are v=−Bx and α=−(xᵀBx−tr(BΣ))/2. Differentiation of the entire centered Gaussian density, not only covariance moments, gives

    Σ′ = −(BΣ+ΣB)−ΣBΣ.

An independent conditional-coordinate substitution also gives the pointwise polynomial identity

    −div(ρv)/ρ + α = (b′/s)ye + [s′/(2s²)](e²−s),

where

    b′ = [−(1+2s+b²/3)(b−β)+b(s−τ)]/τ,
    s′ = [2bs(b−β)−(s+2+2b²)(s−τ)]/τ.

The right side is exactly the parameter derivative of logρ. Its entire conditional expectation given Y is zero, so the entire prescribed marginal remains fixed. The mean stays zero. Gaussian tails justify polynomial pairings and integrations on each compact positive-covariance time interval.

The same vector field is exactly

    (b′,s′)ᵀ = −Mc ∇E,
    Mc = [[1+2s+b²/3, −2bs],
          [−2bs, 2s(s+2+2b²)]].

Here ∇E=((b−β)/τ, (s−τ)/(2τs)). Independent Gaussian integration verifies that the full corrected field action equals ∇EᵀMc∇E. The identification is supported by the full density equality and inherited minimum-field theorem, not by covariance matching alone.

Mc is positive definite for all b and s>0: its upper-left entry is positive and

    det Mc = 2s[2s²+5s+2+(7s+8)b²/3+2b⁴/3] > 0.

## 3. Global Gaussian existence and convergence

Fix any finite initial b0 and s0>0. Local existence and uniqueness hold for this smooth autonomous vector field on R×(0,∞). Its energy identity is

    E′ = −D,       D=∇EᵀMc∇E≥0.

The sublevel {E≤E(b0,s0)} is compact within R×(0,∞). Indeed, for u=s/τ,

    2E = (b−β)²/τ + g(u),       g(u)=u−1−log u≥0.

The function g tends to infinity as u decreases to zero or increases to infinity. Thus the sublevel bounds b, bounds s from above, and bounds s away from zero. A solution cannot leave this compact set because E is nonincreasing. The usual local ODE continuation theorem therefore gives a unique solution for every t≥0. The Gaussian family consequently supplies a global solution of the full constrained density equation in this ansatz.

For completeness, convergence needs an argument beyond monotonic energy. On the compact sublevel Mc has a positive minimum eigenvalue. The smooth nonnegative function D and vector field have bounded derivatives there, so D along the trajectory is uniformly continuous. Since ∫₀∞D(t)dt≤E(b0,s0)<∞, D(t)→0: otherwise infinitely many uniformly long disjoint intervals on which D has a fixed positive lower bound would force infinite integral. Therefore ∇E→0. Equivalently every subsequential limit is stationary, and positivity of Mc makes stationarity equivalent to

    b=β,       s=τ.

This is the unique critical point of E. Compactness now forces convergence of the entire trajectory to (β,τ). Thus Σ→Σ*, and the exact Gaussian KL tends to zero.

This proof is finite dimensional. It does not establish existence or uniqueness for arbitrary constrained PDE data, a convergence rate, a uniform entropy constant, or a shortest endpoint path.

## 4. Falsification controls and interpretive scope

If one reuses the product-target h-only multiplier

    φ_wrong = d²(y²−1)/(6τ),

the resulting negative-gradient density equation has

    d/dt Eμ[Y²] = 2β(b−β)/τ.

This is nonzero whenever β(b−β)≠0. For example b=1/2, β=1/3, s=3/4, τ=5/4 gives the exact leak 4/45. This control specifically detects dropping the target's conditional y-score.

At the initially independent state b=0,s=τ,

    b′=β(1+2τ)/τ,       s′=0.

Thus a nonzero target correlation is immediately created, and the global Gaussian solution converges to the stipulated correlated target. The full constrained geometry does not force independence. Independence in the predecessor was a consequence of its chosen product target. Neither result warrants the chosen marginal or joint target as true, supplies authority to intervene, or recovers information discarded by a coarse observation.

For β=0 and τ=1 the equations reduce exactly to the accepted predecessor:

    b′=−b(s+2+b²/3),       s′=(1−s)(s+2)+2b².

A numerically matched cross covariance is not itself conserved: at b=β one has b′=β(s−τ)/τ. The constraint fixes the entire y marginal and nothing more.

The new result extends that bounded construction; it does not invalidate it or create a new target-selection theorem.

## 5. Evidence limits

check_independent.py imports SymPy and standard Python modules only, and imports no author/root checker. Its 36 exact controls verify conditional scores, the multiplier, full density and covariance identities, parameter gradient agreement, action/dissipation, the SPD determinant decomposition, orthogonal horizontal action, stationary/product controls, and the nonzero wrong-multiplier witness. Both ordinary Python and optimized Python executions pass. Runtime exceptions, rather than Python assert statements, enforce these equalities.

The checks support the displayed algebra. They are not substitutes for the analytic compactness and convergence proof above, nor formal proofs of any infinite-dimensional theorem. The frozen-candidate review and complete hash binding are recorded in REVIEW.md and REVIEW_BINDINGS.json. Two deliberately corrupted checker copies are separately rejected under optimized Python, as recorded in NEGATIVE_CONTROLS.json.
