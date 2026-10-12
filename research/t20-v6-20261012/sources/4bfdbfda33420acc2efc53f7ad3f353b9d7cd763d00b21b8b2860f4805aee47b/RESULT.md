# Singular Gaussian entrance with a fixed entire marginal

11 October 2026 UTC. Additive ordinary mathematics within ACTIVE T20. The parent proposed the singular extension and its asymptotic/action distinction; this investigation verifies that proposal and supplies endpoint continuity, Gaussian-class uniqueness and approximation details. No protected or predecessor edits, independent-review claim, formal-kernel certification, empirical warrant, field-priority claim or programme closure.

## 1. Result and exact scope

Fix β∈R, τ>0 and target π=N(0,Γ), where

    Γ=[[1,β],[β,β²+τ]].

Let Y,G be independent standard Gaussians. For b∈R and s≥0 define μ(b,s) as the law of (Y,bY+√s G). Its entire y-marginal is N(0,1), including at s=0. Starting at any b₀∈R,s₀=0, the polynomial system inherited from the correlated-target packet,

    b′=[b(s−τ)−(b−β)(1+2s+b²/3)]/τ,
    s′=[2bs(b−β)−(s+2+2b²)(s−τ)]/τ,                 (1)

has a unique global forward solution, with s(t)>0 for every t>0. The resulting law solves the actual projected full-density KL gradient equation for t>0, converges narrowly (indeed in W₂) to its singular initial law at zero, and converges to π at infinity with KL tending to zero. It retains the whole y-marginal at all times.

Put a=2(1+b₀²). As t↓0,

    s(t)=a t+O(t²),     b(t)=b₀+O(t),
    E(t)=−½log t+C₀+O(t),
    C₀=½[(b₀−β)²/τ−1+log(τ/a)],
    D(t)=1/(2t)+O(1),                                 (2)

where E=KL(μt||π) and D is the minimum instantaneous full transport–centred-reaction action of its density tangent. Hence

    ∫₀^ε D(t)dt=∞,
    L(0,ε):=∫₀^ε √D(t)dt=√(2ε)+O(ε^(3/2)).            (3)

This L is the length of the specified curve in the induced tangent metric; it is not asserted to be the shortest endpoint distance.

The original-time fields satisfy an L¹ spacetime endpoint continuity equation, but not the finite-L²-action endpoint contract. The time change t=u² gives finite action including the singular endpoint, with instantaneous action tending to 2. Equivalently, t=εr² on r∈[0,1] gives a whole-marginal-preserving endpoint competitor of action

    Aε=2ε+O(ε²).                                      (4)

Time change preserves the geometric curve and its marginal; it changes its speed, so the changed curve is not the original unit-speed-in-time KL gradient equation. Neither E(0) nor the original-time action is made finite. No ordinary initial Riemannian tangent or finite initial KL gradient is assigned. The singular initial Gaussian has all finite moments and is moment-determinate; its infinite KL comes from singularity relative to π, not heavy tails. This entrance is distinct from polynomial heavy-tail recovery.

## 2. Inheritance, bounded deduplication and primary credit

The copied, hash-bound inputs in INPUT_BINDINGS.json were inspected. The correlated-target RESULT and its independent REVIEW own (1), the positive-time full-density identification, constrained mobility, dissipation identity and positive-initial-state global theorem. The fixed-marginal endpoint report owns singular feasibility and endpoint attainment on compact products; it expressly does not claim noncompact attainment or a KL entrance theorem. The Gaussian geometry report already places the zero-variance boundary at finite intrinsic distance. The Gaussian entropy-transfer report starts with positive covariance and distinguishes entropy-driven positive covariance from the zero-entropy terminal singular limit. The Fisher endpoint report treats a different one-sided statistical boundary, not a rank-deficient Gaussian initial law. No inspected predecessor states this fixed-marginal singular-initialisation contract.

The Gaussian SHK operator, Gaussian covariance dynamics and entropy smoothing mechanism are classical ancestry, not claimed discoveries. Liero, Mielke, Tse and Zhu, *Evolution of Gaussians in the Hellinger–Kantorovich–Boltzmann gradient flow*, https://arxiv.org/html/2504.20400v1, §§2.1–2.2 and §3.4, supplies the unconstrained Gaussian system. Its displayed Gaussian parameter domain is positive definite; the inspected statements do not expressly supply the fixed-entire-marginal singular initial condition here. Extending a smooth covariance ODE to a semidefinite initial covariance is a classical elementary ODE mechanism. This report's bounded addition is its application to the inherited constrained equation and the exact endpoint-action qualifications. This is not an exhaustive literature search or a novelty claim for Gaussian entrance itself. Finite endpoint feasibility alone is already supplied by the inherited pure-reaction conditional sphere or mixture construction: that feasibility mechanism does not need compactness, although the preceding attainment theorem does. The present addition is this specified constrained KL-gradient entrance and its boundary asymptotic/action realization, not the first finite-distance connection of these laws.

## 3. ODE entrance, global continuation and convergence

For fixed τ>0, the right side of (1) is polynomial in (b,s), hence locally Lipschitz on all of R², including s=0. Local existence and uniqueness therefore apply at (b₀,0). Direct evaluation gives

    s′(0)=2(1+b₀²)=a>0,
    b′(0)=−b₀−(b₀−β)(1+b₀²/3)/τ.                    (5)

Smoothness gives the Taylor statements in (2), and s(t)>0 on some (0,δ]. From any t*=δ/2 the solution is the inherited positive-state solution by ODE uniqueness. That solution is global, remains in a compact subset of R×(0,∞) after t*, and converges to (β,τ). The proof of the inherited assertion is short: E=½[(s+(b−β)²)/τ−1+log(τ/s)] has compact sublevels inside s>0, E′=−D≤0, and D vanishes only at (β,τ). Compact-sublevel ODE continuation is global; uniform continuity and integrability of D imply D→0 and convergence to that unique point. No finite initial energy at t=0 is used.

For completeness, uniqueness includes entrance curves which solve the displayed ODE only for t>0 and have parameter trace (b₀,0): continuity of the polynomial vector field makes it bounded near that trace, so integration from h>0 and h↓0 gives the usual initial-value integral equation. Standard ODE uniqueness then applies. No backward probability continuation through the boundary follows: s(t)=at+O(t²)<0 for small negative t.

The positive-time density and fields are exactly those already verified in the correlated-target report. Set Σ=[[1,b],[b,b²+s]], γ=(b−β)(b−3β)/τ and

    C=Γ⁻¹−Σ⁻¹−(γ/3)diag(1,0),
    v=−Cx,     α=−½[xᵀCx−tr(CΣ)].                    (6)

They satisfy ∂tμ+div(μv)=μα, ∫αdμ=0 and the constrained KL gradient projection for t>0. No logarithmic score or inverse covariance is assigned at t=0.

## 4. Trace and uniqueness within the Gaussian class

Couple all laws by the same (Y,G). Then

    E|(Y,b(t)Y+√s(t)G)−(Y,b₀Y)|²
      =(b(t)−b₀)²+s(t)→0.                            (7)

This proves W₂ and narrow convergence, not total-variation convergence. Indeed μ0 is carried by the line z=b₀y whereas every μt, t>0, has a full Lebesgue density; their laws are mutually singular. The fixed entire marginal passes by the explicit construction, with no moment-identification inference.

One can also check uniqueness among Gaussian entrances without silently imposing a zero z-mean. Write a general Gaussian with the fixed y-law as (Y,c+bY+√s G). For the same centred target, direct Gaussian projection gives the same covariance equations (1) and

    c′=−c(1+s+b²/2)/τ.                               (8)

To see this, at the mean m=(0,c), the score gradient is Γ⁻¹m=c(−β,1)/τ. The additional linear part of the marginal multiplier is k y, k=c(b−2β)/(2τ). The projected score gradient at m is c(−b/2,1)/τ. Multiplication by −(I+Σ) gives zero y-mean derivative and precisely (8). The quadratic part is unchanged, so covariance still obeys (1). These are identities of full Gaussian tangents, since quadratic/linear potential fields produce exactly Gaussian density tangents.

A narrow Gaussian trace equal to μ(b₀,0) forces convergence of its means and covariance entries to the stated values. For this finite-dimensional Gaussian family, this follows from convergence of the Gaussian characteristic functions (or the standard Gaussian weak-convergence criterion), not from a general inference of moment convergence from narrow convergence. Thus c→0,b→b₀,s→0. The polynomial system (1),(8) has that unique initial-value solution, and c≡0. This proves uniqueness among Gaussian projected-flow entrances that are nondegenerate and classical for t>0 with the declared narrow trace. It does not prove uniqueness among arbitrary weak full-law PDE solutions, nor assert all such solutions remain Gaussian.

## 5. Dissipation asymptotics and the unavoidable infinite original-time action

The inherited positive-time full tangent minimum is

    D=tr(CΣC)+½tr(CΣCΣ)=∇EᵀMc∇E,
    Mc=[[1+2s+b²/3,−2bs],
        [−2bs,2s(s+2+2b²)]].                         (9)

Since Eb=(b−β)/τ and Es=(s−τ)/(2sτ), direct expansion shows

    D=(1+b²)/s+R(b,s),                               (10)

where R is polynomial in b,s for fixed β,τ. More explicitly,

    R=(1+2s+b²/3)(b−β)²/τ²
      −2b(b−β)(s−τ)/τ²
      +[s²+(2+2b²−2τ)s+τ²−4τ(1+b²)]/(2τ²).

Thus (5) yields D=1/(2t)+O(1). Substitution into E gives its stated constant C₀. The O(t) remainder in E can also be differentiated because the ODE is smooth and s/t extends smoothly and positively at zero; nevertheless (10) proves D's expansion directly.

The initial KL is +∞: μ0 is not absolutely continuous with respect to the nondegenerate target π. For any 0<h<T, the valid energy identity is

    E(h)−E(T)=∫h^T D(t)dt.

Letting h↓0 makes both the initial energy and accumulated dissipation diverge; it is not a finite-energy balance at t=0. At every positive time (6) minimizes among all representations of the entire density tangent. Therefore any alternative fields representing this same original-time curve have instantaneous squared norm at least D almost everywhere. None can turn it into a finite-action original-time curve.

By (2), √D=(2t)^(-1/2)(1+O(t)). Integrating proves (3). The leading coefficient is independent of β,τ and b₀: the normal-direction variance entrance and its reciprocal dissipation cancel exactly. This is a boundary asymptotic, not a convergence-rate programme or a shortest-path claim.

## 6. Endpoint continuity equation and finite-action time change

For any finite T, ∫₀^T √D dt is finite: the singular part is integrable by (3), and D is continuous away from zero. By probability Cauchy–Schwarz,

    ∫₀^T∫(|v|+|α|)dμt dt≤√2∫₀^T √D dt<∞.            (11)

Hence m=v dt μt and σ=α dt μt are finite spacetime measures. Take a compactly supported C¹ spacetime test ψ. The ordinary continuity equation on [h,T] reads

    ∫h^T∫(∂tψ+∇ψ·v+ψα)dμt dt
      =∫ψ(T)dμT−∫ψ(h)dμh.

Narrow convergence, bounded test coefficients, and (11) permit h↓0. This establishes the endpoint distributional identity with μ0 and no extra impulsive source at time zero. The fields are defined only dt μt-almost everywhere, so arbitrary values on the zero-time slice do not change the identity. They are L¹ over spacetime; their squared norm has infinite integral. Thus this identity alone does not meet the predecessor's finite-action admissibility definition.

Now put t=u², μ̃u=μu², ṽu=2u vu² and α̃u=2u αu² for u>0. Their action density is

    D̃(u)=4u²D(u²)=2+O(u²).                           (12)

They are L² on every finite u interval, preserve probabilities and the entire marginal, and their positive-time continuity equation follows by the chain rule. Passing to the narrow trace by the finite-action estimate proves the endpoint continuity equation as above. The action from u=0 to u=√ε is 2√ε+O(ε^(3/2)); the interval length matters when comparing endpoint actions.

For a unit-time endpoint competitor use t=εr², r∈[0,1], and multiply the old fields by 2εr. Then

    Dε(r)=4ε²r²D(εr²)=2ε+O(ε²r²),
    ∫₀¹Dε(r)dr=2ε+O(ε²),                            (13)

uniformly for small ε. Its square-root action provides an upper bound for any endpoint infimum defined by the same whole-marginal action on R². This is an explicit feasible path, not a proof of noncompact attainment, equality with an unrestricted SHK distance, geodesic minimality, or metric completeness. The compact-product endpoint theorem is neither imported beyond its hypotheses nor needed here.

## 7. Positive-state approximation and limits

If bₙ→b₀ and sₙ>0 tends to zero, the inherited positive-state solutions converge uniformly in parameters on each fixed finite [0,T] to this entrance. A direct ODE continuous-dependence argument applies in a compact tube around the smooth polynomial entrance path on [0,T]; stop an approximate trajectory on leaving the tube, use the vector field's finite Lipschitz bound and Gronwall before the stopping time, and small initial displacement prevents exit. Their global existence is already known. Coupling as in (7) then gives uniform W₂ convergence, since |√sₙ(t)−√s(t)|²≤|sₙ(t)−s(t)|.

On [h,T], h>0, energies and dissipations converge uniformly as well because s is bounded away from zero. No energy convergence at zero is claimed: E(bₙ,sₙ) diverges, and the original-time total actions on [0,T] diverge accordingly. The time-changed singular path, rather than an unjustified uniform original-time energy bound, is what supplies finite endpoint action.

## 8. Verification and ceiling

verify.py independently recomputes the boundary derivatives, pole decomposition, energy constant, full covariance tangent, constrained mean projection, finite-action time-change coefficients, and input bindings by exact symbolic identities. These controls supplement the ordinary ODE, integrability and trace arguments; no finite enumeration proves their general analytic conclusions. No sampling, optimization campaign, general nonlinear PDE well-posedness, arbitrary singular law theorem, target identification, empirical noetic warrant, protected integration or T20 closure is supplied.
