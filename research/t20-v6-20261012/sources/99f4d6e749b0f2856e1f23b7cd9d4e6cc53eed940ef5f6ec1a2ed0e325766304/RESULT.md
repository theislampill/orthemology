# Attained finite-endpoint action with an entire fixed marginal

11 October 2026 UTC. Additive ordinary mathematics within ACTIVE T20. The frozen fixed-marginal-correction packet and all accepted inputs remain unchanged. No protected edit, integration, formal-kernel certification, field-priority claim, empirical interpretation or programme closure is made. The parent proposed the compact direct-method argument, conditional square-root competitor, refining-constraint consequence and atomic comparison. The investigator supplies the detailed measure, measurability, compactness, metric and approximation proofs and exact controls. These are participating mathematical contributions, not independent review.

## 1. Result and domain

Let X=Y×Z be a product of flat tori with the product Riemannian metric, T(y,z)=y, and let ν be any Borel probability on Y. It may be singular or atomic. Define

    Sν={μ∈P(X):T#μ=ν}.

Use the unit actual-rate action

    A(μ,v,α)=∫₀¹∫X (|v|²+α²)dμt dt,
    ∂tμ+div(μv)=μα.                                    (1)

Paths must remain probabilities with the entire marginal ν at every time; all spatial velocity components are allowed. No positive-density, fixed-support or fixed-rank assumption is imposed.

**Theorem.** For every μ0,μ1∈Sν:

1. There exists an admissible finite-action path. A jointly measurable reaction-only conditional square-root construction has exact action

       4∫Y θ(y)²dν(y)≤π²,                             (2)

   where θ(y)∈[0,π/2] is the conditional Hellinger angle.
2. The infimum of (1) is attained, including for singular endpoints.
3. Its square root dν is a finite metric on Sν, with

       dS(μ0,μ1)≤dν(μ0,μ1)≤2(∫θ²dν)^(1/2)≤π,        (3)

   where dS is defined by the same action with only the mass-one constraint. Every action-minimizing path is a constant-speed dν-geodesic.
4. If finite, nested continuous marginal-test catalogues have uniformly dense linear span in C(Y), while mass one is imposed explicitly, their endpoint minimum actions increase to the full fixed-marginal minimum. Subsequential limits of their minimizers are full fixed-marginal minimizers.

These are finite-endpoint variational statements. They do not establish a nonlinear KL flow, a minimizing-movement/JKO limit, numerical-grid convergence, an algorithmic rate, uniqueness of a minimizer, or its smoothness. The reaction-only competitor supplies feasibility; it is not asserted to minimize the full transport–reaction action.

## 2. Classical and inherited scope

The directly inspected primary source is Nishino, Bauer, Needham and Charon, *A Benamou–Brenier proximal splitting method for constrained unbalanced optimal transport*, [arXiv:2512.09250v1](https://arxiv.org/html/2512.09250v1), Definitions 1–2 and 6–7, Theorem 9, Remark 10 and Appendix C.1. Its theorem concerns finitely many continuous affine path constraints and assumes a finite-cost feasible competitor. Appendix C.1 proves attainment by Fenchel–Rockafellar duality. Its infinitesimal cost has a factor 1/2: at δ=1 it is exactly half of (1) for identical triples. We prove the whole-marginal, infinitely constrained statement directly rather than silently substituting an infinite constraint family into that theorem. Feasibility here is proved constructively.

The immediate ancestor, Bauer, Charon, Needham and Nishino, *Path constrained unbalanced optimal transport*, [arXiv:2402.15860v3](https://arxiv.org/html/2402.15860v3), already proves finite-constraint attainment (Theorem 3.4), constant energy and metric structure (Lemma 3.8, Theorem 3.9), and attainment on parallelizable manifolds (Theorem 5.5). Its Remark 4.24 also identifies weighted-Sobolev projection of constraint potentials. Thus neither the constrained-metric concept, time-rescaling mechanism, nor manifold formulation is claimed new. The present proof keeps the infinitely many marginal tests and singular feasibility explicit.

The action and square-root sphere are classical. The copied and hash-bound inherited inputs retain ownership:

- spherical-atomic-source-interface-20261010/SOURCE_INTERFACE.md already gives the unit/unit dynamic action, square-root normalization, and the singular rank-changing two-Dirac reaction path of action π². Our conditional construction applies that sphere geometry measurably fibre by fibre; it does not rediscover the two-atom path.
- full-law-coarse-graining-20261011/RESULT.md proves the full-tangent coisometric quotient and contraction, and separates local tangent facts from endpoint distances.
- fixed-marginal-correction-20261011/RESULT.md gives the actual smooth/weak constrained KL gradient and its globally convergent Gaussian construction. It deliberately does not prove general endpoint attainment or general nonlinear PDE existence.
- fisher-endpoint-geometry-20261010/RESULT.md uses square-root Fisher geometry for its one-sided statistical endpoint and explicitly avoids ambient endpoint-minimality claims.
- face-stratified-noetic-geometry-20261010/RESULT.md concerns finite exponential leaves and support faces; it makes no general support-changing geodesic claim.

DEDUP_SCAN.json records a bounded local report scan and these targeted comparisons. Absence from inspected passages is not field-wide priority evidence. The contribution here is the explicitly justified fixed-entire-marginal endpoint contract, including singular feasibility and convergence of refining finite constraints.

## 3. Admissible curves and the measure action

Put Q=[0,1]×X. An admissible curve is μ∈C([0,1];P(X)) for the narrow topology, with μ(0)=μ0, μ(1)=μ1 and T#μt=ν for all t. Let η=dt μt be its spacetime measure. Let v:Q→R^dim(X) and α:Q→R be Borel fields in L²(η), and put m=vη and σ=αη. The flat torus identifies tangent vectors globally and has no boundary flux condition to leave implicit. The continuity equation means that every ψ∈C¹(Q) satisfies

    ∫Q ∂tψ dη+∫Q ∇xψ·dm+∫Q ψ dσ
      =∫X ψ(1,x)dμ1−∫X ψ(0,x)dμ0.                   (4)

Taking ψ(t,x)=χ(t) and using μt(X)=1 gives ∫α(t,x)dμt(x)=0 for a.e. t. Thus (1) uses exactly the globally centred reaction convention of the inherited spherical action. Fixed marginal does not require vy=0 or E[α|Y]=0 separately: transport and reaction may cancel after pushforward.

For weak-* limits it is useful to define the action for arbitrary η≥0 and vector measure w=(m,σ) on Q by

    J(η,w)=∫Q |dw/dη|²dη       if w≪η and dw/dη∈L²(η),
           +∞                  otherwise.             (5)

Equivalently, against any common positive dominating measure λ, the integrand is |dw/dλ|²/(dη/dλ), with 0/0=0 when both numerators vanish, and +∞ when dη/dλ=0 but dw/dλ≠0. This perspective convention permits zero densities; it does not permit finite-action momentum or source singular relative to spacetime mass.

### Exact dual formula and lower semicontinuity

One has

    J(η,w)=sup_F {2∫Q F·dw−∫Q |F|²dη},               (6)

where F ranges over continuous R^(dim(X)+1)-valued functions on Q. For finite J, the inequality “≤” follows by completing a square, and continuous functions are dense in L²(η), yielding equality. Conversely, if the supremum M is finite, scaling any continuous F by a real scalar gives

    |∫F·dw|≤√M ||F||L²(η).

The induced functional therefore extends to L²(η). Hilbert-space representation gives w=aη with a∈L²(η), because the equality against continuous functions identifies finite Radon measures. The supremum is ||a||². This proves (6), including the infinite-cost cases, rather than assuming absolute continuity survives weak limits.

For each fixed continuous F the expression in braces is weak-* continuous in (η,w). Its supremum is lower semicontinuous. This is the convex quadratic-perspective mechanism needed below.

## 4. Singular feasibility: a measurable conditional sphere path

Disintegrate μi(dy,dz)=ν(dy)ri(y,dz), i=0,1. Compact metric spaces are standard Borel, so probability kernels ri exist. Set

    λy=r0(y,·)+r1(y,·),       λ=μ0+μ1=ν(dy)λy(dz).     (7)

Here λy has mass 2; it is not a probability kernel. Disintegration against 2ν would instead require λy/2 and a corresponding rescaling. We use (7) throughout.

Choose Borel Radon–Nikodym functions fi=dμi/dλ with 0≤fi≤1 and f0+f1=1 λ-a.e. They also satisfy ri(y,dz)=fi(y,z)λy(dz) for ν-a.e. y. To obtain a single full-measure set of y for this statement, first test the global Radon–Nikodym identity on products of a Borel set in Y with one set from a countable generating algebra in Z; then use uniqueness and a monotone-class argument. Thus all conditional integral identities can be required simultaneously on one ν-full Borel set. Values on its complement may be set to any fixed common probability kernel without changing μi.

Put ui=√fi. In L²(λy), both ui have norm 1. Define

    a(y)=∫Z u0u1 dλy∈[0,1],
    θ(y)=arccos a(y)∈[0,π/2].                          (8)

Kernel integration of a jointly Borel bounded function is Borel, so a and θ are measurable. Define coefficient functions

    A(t,θ)=sin((1−t)θ)/sin θ,
    B(t,θ)=sin(tθ)/sin θ                               (θ>0),
    A(t,0)=1−t,       B(t,0)=t,

and the square-root path

    u(t,y,z)=A(t,θ(y))u0(y,z)+B(t,θ(y))u1(y,z),
    rt(y,dz)=u(t,y,z)²λy(dz),
    μt(dy,dz)=ν(dy)rt(y,dz).                           (9)

The coefficients and their t-derivatives extend continuously to θ=0. At θ=0, ||u0−u1||²=2−2a=0, so (9) is constant in that fibre. For θ>0, the standard sphere identities, verified by expanding using ⟨u0,u1⟩=cos θ, are

    ||u(t)||²L²(λy)=1,
    ||∂tu(t)||²L²(λy)=θ(y)²,
    ⟨u(t),∂tu(t)⟩L²(λy)=0.                            (10)

They also hold at θ=0. All coefficients in u are nonnegative. They are strictly positive for 0<t<1, so u(t)>0 λy-a.e. at every interior time, using f0+f1=1. Neither absolute continuity of ri relative to volume nor any relation between their supports is required.

All quantities in (9) are jointly Borel. Moreover 0≤A,B≤1 and |∂tA|,|∂tB|≤π/2 on the coefficient rectangle. As λ is finite, these bounds give dominated continuity of u² in L¹(λ), hence even total-variation continuity of μt. They also justify differentiating under the integral, with source measure

    m=0,
    σ=2u∂tu dt λ.

Define the actual reaction field by

    α=2∂tu/u where u>0,       α=0 where u=0.            (11)

Then σ=αη. The numerator 2u∂tu is zero wherever u=0. The reaction field may grow without bound near t=0 or 1; its weighted square is integrable. The zero-density convention is not an assignment of an infinite field to a zero mass. At interior times u>0 λ-a.e., so

    ∫Q α²dη=4∫₀¹∫Y ||∂tu||²L²(λy)dν dt
             =4∫Y θ(y)²dν≤π².                        (12)

The two endpoint time slices have dt-measure zero; pointwise equality with 4|∂tu|² on those slices is unnecessary. Differentiating u² and integrating by parts in time proves (4), including the exact endpoints. Equation (10) gives both rt(y,Z)=1 and ∫α drt(y)=0. Thus this particular competitor uses a conditionally centred reaction and preserves the entire marginal for every t.

When the endpoint conditionals coincide, θ=0 and no action is spent there. When they are mutually singular, a=0, θ=π/2, and the fibre path is the inherited cos²/sin² mixture. This proves feasibility for every pair in Sν, including singular laws.

### A simpler universal feasibility control

The parent also supplied an alternative which avoids disintegration when only a finite-action bound is needed. Set a(t)=cos(πt/2), b(t)=sin(πt/2) and

    μt=a(t)²μ0+b(t)²μ1,       m=0,       σ=∂tμ.

This convex mixture preserves every affine probability constraint shared by the endpoints, in particular the whole marginal. With λ=μ0+μ1 and fi=dμi/dλ, its density is q=a²f0+b²f1. Weighted Cauchy–Schwarz gives

    (∂tq)²/q ≤ 4[(a′)²f0+(b′)²f1],

with the same zero-density convention. After integrating in space the right side is 4[(a′)²+(b′)²]=π², so total action is at most π². The identity behind the inequality is the nonnegative remainder 4f0f1(ab′−ba′)² after multiplication by q. Interior times have q>0 λ-a.e.; endpoint zeros cause no spacetime-action difficulty. This provides an independent simple feasibility route for singular endpoints. The conditional sphere construction supplies the more informative bound (2), which spends no action on unchanged fibres. No additional general theory of arbitrary convex constraint sets is claimed here.

## 5. Attainment by direct compactness

Choose a minimizing sequence (μn,vn,αn), with actions An bounded by some finite C; (12) supplies such a bound. Let ηn=dt μnt, wn=(vn,αn)ηn.

For f∈C¹(X), the continuity equation and narrow continuity imply that t↦∫f dμnt is absolutely continuous. Indeed its distributional derivative is the L¹ function ∫(∇f·vn+fαn)dμnt; its continuous representative is already the given curve. For 0≤s≤t≤1, Cauchy–Schwarz gives

    |∫f d(μnt−μns)|
      ≤√(∫sᵗ∫(|vn|²+αn²)dμnu du)
         √(∫sᵗ∫(|∇f|²+f²)dμnu du)
      ≤√C Cf √(t−s),
    Cf=max_X √(|∇f|²+f²).                              (13)

A countable dense smooth test family, with summable weights normalized by 1+Cf, defines a metric for the narrow topology of P(X). Equation (13) gives uniform equicontinuity in that metric. Since X is compact, P(X) is compact; Arzelà–Ascoli yields a subsequence and μ∈C([0,1];P(X)) such that μnt→μt uniformly in the narrow topology. Endpoints pass to the limit. Since T is continuous, T#μt=ν for every t.

Uniform narrow convergence implies ηn⇀*η=dt μt: first test finite sums of products of continuous time and spatial functions, then use their uniform density in C(Q). Also

    ||wn||TV=∫Q √(|vn|²+αn²)dηn≤√An≤√C,              (14)

because ηn(Q)=1. Sequential weak-* compactness of bounded Radon measures on compact metric Q gives, after another subsequence, wn⇀*w=(m,σ). For each ψ∈C¹(Q), all coefficients in (4) are continuous, so the distributional continuity equation and endpoint terms pass to the limit.

By (6),

    J(η,w)≤liminf An<∞.                                (15)

Consequently w=(v,α)η for Borel L²(η) fields. This simultaneously excludes nonzero singular momentum/source in the limiting triple and restores the required actual-rate representation. The limit is admissible and has no more than the infimum action; therefore it attains that infimum. Mass-one testing gives mean-zero α at a.e. time as before.

The proof uses the whole marginal as a closed condition directly. It never replaces that condition with one fixed finite-dimensional moment vector. Compactness of X, exact total spacetime mass 1 and the finite-action competitor are the explicit hypotheses doing the work. No corresponding noncompact theorem is inferred without additional tightness and moment control.

## 6. A finite metric and attained constant-speed geodesics

Let dν² be the minimum established above.

- It is nonnegative and at most (12); the constant curve gives dν(μ,μ)=0.
- Reversing time and negating v and α gives symmetry.
- From (13) over [0,1], every competitor satisfies

      |∫f d(μ1−μ0)|≤Cf √A.

  Infimizing shows that dν=0 forces equality of all smooth-test integrals. Smooth functions are uniformly dense in C(X), so the endpoints are equal. Thus definiteness does not depend on importing a topology theorem for an ambient named distance.
- Suppose a=dν(μ0,μ1)>0 and b=dν(μ1,μ2)>0. Run a minimizing first path in time τ=a/(a+b), scaling its velocities and reaction by 1/τ, and run the second in time 1−τ. Its action is

      a²/τ+b²/(1−τ)=(a+b)².                            (16)

  The continuity equation, endpoints and whole marginal persist under this affine time change and concatenation. Hence dν(μ0,μ2)≤a+b. Cases a=0 or b=0 reduce to equal endpoints.

Every fixed-marginal path is an admissible mass-one ambient path, so dS≤dν by inclusion of competitor sets. Here dS means exactly the inherited unit/unit dynamic definition, not an unverified angular/static normalization.

### Subarcs and speed

Let a full minimizer have action d², where d=dν(μ0,μ1), and write E[s,t] for its action on [s,t]. Rescaling its restriction to unit time gives

    dν(μs,μt)²≤(t−s)E[s,t].                            (17)

Equality must hold: if it were strict, take the already established minimizer between μs and μt, compress it to [s,t], and replace that subarc. The strictly smaller action contradicts minimality of the original full curve. No differentiable time reparametrization theorem is needed for this replacement; affine rescaling suffices.

For a partition 0=t0<...<tN=1, equality in (17), the triangle inequality, and Cauchy–Schwarz imply

    d≤Σi√((ti−t(i−1))E[t(i−1),ti])≤√(Σi E_i)=d.

For d>0, the equality condition in Cauchy–Schwarz gives E_i=d²(ti−t(i−1)). Choose partitions containing any s<t to conclude

    E[s,t]=d²(t−s),
    dν(μs,μt)=d|t−s|.                                  (18)

The zero-distance case is constant. Thus every minimizing path is a constant-speed metric geodesic and its action density is d² a.e. This is a finite-endpoint statement about the attained variational problem, not a claim that the KL gradient equation follows geodesics or that a particular reaction-only competitor is globally minimizing.

## 7. Refining finite marginal tests converge to the exact constraint

Choose f1,f2,...∈C(Y) whose linear span is uniformly dense in C(Y), for example a countable real trigonometric-polynomial family. For each n define an endpoint problem with the same μ0,μ1 and action, with the **explicit mass-one constraint** and only

    ∫X fj(Tx)dμt(x)=∫Y fj dν,
              j=1,...,n,     for every t.               (19)

Let its minimum action be an and let the whole-marginal minimum be a∞=dν². The mass-one condition is retained even if the constant function appears later in the catalogue; it is what gives the uniform compactness estimate.

Each finite problem has a feasible competitor (9). Its constraints are closed under uniform narrow convergence, so the same direct proof gives a minimizer. The classes are nested, hence

    0≤a1≤a2≤...≤a∞≤π².

Let a=lim an and take corresponding minimizers. Their uniformly bounded actions supply exactly the compactness used in §5. For any fixed j, every sufficiently late member satisfies the j-th constraint. Uniform narrow convergence passes it to the limiting curve at every time. Density of the linear span then forces T#μt=ν for every t. Lower semicontinuity gives a∞≤A(limit)≤a≤a∞, proving

    lim_n an=a∞,       A(limit)=a∞.                     (20)

The same argument applies to any convergent subsequence of the minimizing triples in these compactness topologies. It gives subsequential limiting minimizers, not uniqueness or convergence of the entire sequence to one selected path.

A finite catalogue generally enforces only the supplied moments; it does not automatically preserve the entire marginal. Special finite catalogues can determine particular laws, but no such identification is assumed here. Equation (20) is an infinite-refinement continuum variational result. It gives no finite stopping certificate, numerical mesh-consistency theorem, computable error rate, or claim that a solver returns an exact whole marginal after finitely many tests.

## 8. Exact singular comparison and boundary controls

Place two distinct y labels yA,yB in the torus and take ν=(1/3)δyA+(2/3)δyB. Choose distinct z0,z1 for the first fibre and any fixed z* for the second. Let

    μ0=(1/3)δ(yA,z0)+(2/3)δ(yB,z*),
    μ1=(1/3)δ(yA,z1)+(2/3)δ(yB,z*).

The conditional construction is

    μt=(1/3)cos²(πt/2)δ(yA,z0)
        +(1/3)sin²(πt/2)δ(yA,z1)
        +(2/3)δ(yB,z*).                                 (21)

It has the entire correct marginal at every time and constant unit-action density π²/3. The two changing reaction rates are −π tan(πt/2) and π cot(πt/2) at interior times. They diverge at opposite endpoints while the weighted squared action is finite. The common conditional fibre has θ=0 and consumes no action.

A different, global probability square-root great circle between these same endpoint measures has global affinity 2/3. At its midpoint the unchanged second-row mass is

    (2/3) × 2/(1+2/3)=4/5,

rather than 2/3; the first-row mass is 1/5. Therefore a mass-one Fisher-type sphere interpolation need not preserve the entire marginal. This exact comparison was supplied by the parent and checked here. It is not evidence that the full constrained transport–reaction optimum equals π²/3, nor that the global square-root curve minimizes the full ambient transport–reaction action. Spatial transport may lower either endpoint action.

The examples also expose the boundary qualifications: endpoint KL between mutually singular conditionals may be infinite, yet their constrained endpoint action is finite; support/rank changes are allowed; no logarithm, positive-density assumption, smooth disintegration in y, or bounded pointwise reaction is used. Conversely, excluding support change or requiring bounded reaction would change the admissible class and invalidate this universal feasibility argument.

## 9. Verification and claim ceiling

verify.py uses exact symbolic controls for the sphere norm and speed, conditional centering, zero-angle limit, singular two-atom action, the finite atomic marginal example and its global-square-root failure, affine time-rescaling and triangle algebra, together with copied-input and frozen-predecessor bindings. It supplements the ordinary disintegration, Hilbert duality, weak-* compactness and density arguments; those are not proved by finite enumeration. Run `python3 verify.py --output-dir private-locator:71c3ac0c0a1e3f35edfd`, optionally adding `--original-root ..` from this directory.

This contract supplies a realized minimum-action path between any two compatible endpoint laws on the declared compact product domain. The marginal is supplied data, not independently warranted reality. It does not authenticate endpoints, select a true target, determine an empirical noetic state, authorize intervention, make a finite observation catalogue complete, or close T20. The older smooth constrained KL packet and the present singular finite-endpoint packet remain distinct, compatible results with different hypotheses and conclusions.
