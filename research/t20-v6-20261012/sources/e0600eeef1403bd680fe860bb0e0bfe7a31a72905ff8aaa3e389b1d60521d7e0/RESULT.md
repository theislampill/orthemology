# Complete-flow repair of the transport finite-rank lift

10 October 2026 UTC. Additive ordinary mathematical proof and exact controls within ACTIVE T20. No protected input change, baseline rebuild, integration, independent review, formal-kernel verification, literature-priority claim, or T20 closure is claimed.

## 1. Result and ancestry boundary

**The proposed complete-flow repair is valid.** A normalized, coordinatewise C1, full-square-positive polynomial hierarchy with locally uniformly finite full Hankel rank and complete unique two-sided polynomial characteristics is forced to be the finite-atomic characteristic evolution. Every atom survives with positive weight, full rank is constant, the admitted abstract path is unique from its initial functional, and fixed-control finite-law transitions are invertible. A second sufficient criterion, proved in §9, replaces two-sided completeness by forward completeness plus a global lower bound on killing on each finite time interval; it covers autonomous coercive polynomial gradient/selection dynamics and gives injectivity with an inverse on the forward image.

The directly inspected predecessor `continuous-signed-finite-rank-20261010/RESULT.md` proves the killing-only bounded-rank reverse lift, using static finite GNS, local atomic charts, Hermite tests, and maximal-rank endpoint continuation. The present proof reuses those ingredients, with moving characteristics in place of fixed atoms. `transport-rank-boundary-20261010/RESULT.md` supplies the necessary warning: polynomial smoothness, all smooth finite moments, a uniform rank bound, tightness, and strong moment tails do not rule out damped finite-time atom escape or reverse-time inflow. The new hypothesis here is actual two-sided characteristic completeness.

An ancestry search of existing RESULT.md files for complete flow, nonexplosion, and Lyapunov arguments found no existing exact version of this reverse-lift theorem. The source-comparison predecessor already has an affine-transport extension under its different SOS-domination hypotheses; that is not duplicated as a new result here. Its description of Curto–di Dio–Korda–Magron v3, Theorem 4.2, concerns transport of finite atomic measures and records the characteristic-uniqueness caveat; no version of that theorem is imported to establish the present abstract-path assertion. This is a bounded local ancestry check, not an exhaustive literature search. Input digests are retained separately.

## 2. Precise statement

Let I be a nondegenerate real time interval, with endpoint derivatives interpreted one-sided when appropriate. Let P=R[x_1,...,x_d]. For each t in I let L_t:P→R be linear, with

    L_t(1)=1,   L_t(q²)≥0 for every q∈P.

Assume every scalar coordinate t↦L_t(p) is C1 and satisfies

    L'_t(p)=L_t(b_t·∇p)−L_t(k_t p)+L_t(k_t)L_t(p).             (H)

The vector field b_t and killing k_t have polynomial spatial components, continuous time-dependent coefficients, and a common finite degree bound on each compact time interval. In particular their evaluations and spatial derivatives are jointly continuous and uniformly locally bounded on compact time-space sets.

Assume:

(R) For each compact interval K⊂I there is an integer R_K<∞ such that the full polynomial Hankel rank of L_t is at most R_K for every t∈K. The full rank is the supremum of ranks of all finite polynomial Gram matrices, equivalently the rank of (L_t(x^{α+β})) indexed by all monomials.

(C) For every s∈I and z∈R^d the initial-value problem X'=b_t(X), X(s)=z has a unique solution defined through every t∈I. Write it Φ_{t,s}(z). Thus the flow exists both forward and backward on each supplied finite interval, through every spatial point. No claim about times outside I is needed.

Then, for any reference time s∈I, there are exactly r=rank H(L_s) distinct points z_1,...,z_r and positive weights a_j summing to one such that, for every t∈I and p∈P,

    X_j(t)=Φ_{t,s}(z_j),
    K_j(t,s)=∫_s^t k_u(X_j(u)) du,
    W_j(t)=a_j exp(−K_j(t,s)) / Σ_l a_l exp(−K_l(t,s)),
    L_t(p)=Σ_j W_j(t)p(X_j(t)).                              (F)

Oriented integrals apply when t<s. Each integral is finite on every compact time interval, each W_j(t) is strictly positive, and the X_j(t) remain distinct. Every snapshot has exactly one positive representing probability law, with exactly r atoms. Full Hankel rank is r for every t.

Conversely, any finite atomic probability at s produces (F), which satisfies every hypothesis, including (R) with bound r. Therefore among the admitted abstract paths there is exactly one path with the given initial functional. The theorem does **not** deduce the path promise (R) from initial finite rank alone, and does not assert uniqueness in classes where (R) is absent. Neither a rank bound on one fixed truncation nor merely pointwise finite rank is substituted for (R).

## 3. Static representation and local charts

For completeness, the finite GNS argument is recalled briefly. For a square-positive functional L, polynomial Cauchy–Schwarz gives that N={p:L(p²)=0} annihilates every product: L(pq)=0 for p∈N. It also makes N an ideal, since L((pr)²)=L(p·pr²)=0. The quotient P/N has the inner product L(pq), dimension equal to the full Hankel rank, and commuting symmetric coordinate multiplication operators. At finite rank r they simultaneously diagonalize. The vector [1] is cyclic; hence each joint eigenspace has dimension one and a nonzero [1] component. Their distinct joint eigenvalues give exactly r real points with strictly positive weights. Normalization makes this a probability measure.

Uniqueness requires no global moment-determinacy criterion. The nonnegative polynomial ∏_j ||x−z_j||² has zero integral for any representing measure, forcing its support into the displayed finite set. Interpolation then determines all weights.

Fix a compact interval K⊂I and let r be its largest attained rank, which exists by (R) and normalization. The set U={t∈K:rank H(L_t)=r} is relatively open: at each such t a positive r×r Gram determinant stays positive nearby, while the maximal bound prohibits higher rank.

On a neighborhood of any t*∈U choose a linear form ℓ separating its r atoms. The matrix B_t=(L_t(ℓ^{a+b}))_{0≤a,b<r} is positive definite nearby. Solve the degree-r monic annihilator P_t through L_t(ℓ^a P_t(ℓ))=0, a<r. Its coefficients are C1 because B_t is invertible. At every nearby time it vanishes on all r distinct projected atoms, by the Vandermonde system. Its simple roots therefore have C1 local labels λ_j(t). Recover positive C1 weights w_j(t) from L_t(ℓ^a), and recover each C1 spatial coordinate ξ_{ji}(t) from

    L_t(x_i ℓ^a)=Σ_j w_j(t)ξ_{ji}(t)λ_j(t)^a,  0≤a<r.

This derives C1 atom charts from finitely many supplied moment coordinates. It does not assume differentiability of a chosen measure path.

## 4. Hermite tests identify the transport and weights

Fix a time t in such a chart. Define the polynomial

    e_j(x)=∏_{l≠j}(ℓ(x)−λ_l(t))/(λ_j(t)−λ_l(t)),
    p_{ji}(x)=(x_i−ξ_{ji}(t)) e_j(x)².

Hold all coefficients of this test polynomial fixed when differentiating at t. It vanishes at every current atom; its gradient is the i-th coordinate unit vector at atom j and zero at the other atoms. Applying (H) and differentiating the finite sum gives

    w_j(t) ξ'_{ji}(t)=w_j(t)b_{t,i}(ξ_j(t)).

The reaction terms vanish because p_{ji} vanishes at every atom. Since w_j>0, ξ'_j=b_t(ξ_j).

For an arbitrary fixed polynomial p, differentiating its local atomic representation and cancelling these transport contributions in (H) gives

    Σ_j [w'_j+w_j(k_t(ξ_j)−Σ_l w_l k_t(ξ_l))]p(ξ_j)=0.

Interpolation isolates each coefficient. Thus

    w'_j=−w_j(k_t(ξ_j)−Σ_l w_l k_t(ξ_l)).                  (W)

On any connected component J of U, choose s∈J and label its atoms. Local uniqueness for the transport ODE identifies each local chart with the complete curves Φ_{t,s}(ξ_j(s)); labels can be continued through J. Uniqueness prevents two curves from meeting: a meeting at t would give two solutions through the same point, and backward uniqueness returns the same point at s. The weight equation has the explicit solution in (F), with these curves. One may justify continuation of the formula by the usual open-and-relatively-closed argument inside J, using the local chart at any putative interior stopping time. All coefficients of the finite weight system are continuous.

This is not an illicit polynomial pullback by a nonlinear flow. For a nonlinear polynomial vector field, p∘Φ_{t,s} need not be polynomial. The proof uses only polynomial tests in local atomic charts and actual finite-dimensional characteristics.

## 5. A maximal-rank component cannot terminate

Let τ∈K be an endpoint in the relative closure of a nonempty component J. Fix s∈J. Completeness gives each X_j(t)=Φ_{t,s}(ξ_j(s)) at τ and across its compact time segment. Each continuous curve has bounded image there. Uniqueness makes the r endpoints X_j(τ) pairwise distinct. Their union over this finite time segment is compact; joint continuity of k makes all rates k_t(X_j(t)) bounded. Hence the oriented integrals K_j(τ,s) are finite, and formula (F) has r strictly positive limiting weights at τ.

For every fixed p, coordinate continuity of L_t identifies L_τ(p) with this r-atom endpoint formula. The static argument gives rank r at τ. Choose a linear form separating the endpoint atoms; its r×r moment Gram determinant is strictly positive at τ and remains so nearby. The global maximal bound r places that whole relative neighborhood in U. It intersects J, so τ belongs to J and is not a boundary separating rank strata.

Consequently every such component is relatively closed as well as relatively open in connected K, and must equal K. This proves constant rank and formula (F) throughout K. Apply this to a compact interval containing any selected s and t to obtain the assertion on I. The proof excludes escape, collision, and finite-time loss of weight, and also excludes atom birth through a rank-stratum boundary.

The corresponding statements in the killing-only predecessor concerned fixed supports and unchanged polynomial null ideals. Here supports move. Full rank remains constant, but equality of polynomial null ideals at different times is generally false (already for a translating point). No fixed-truncation rank invariance is asserted for nonlinear flow.

## 6. A checkable sufficient condition for completeness

A useful sufficient replacement for (C) is a nonnegative coercive C1 function V:R^d→[0,∞) with compact sublevel sets, such that for every compact time interval K⊂I there is C_K<∞ with

    |∇V(x)·b_t(x)| ≤ C_K(1+V(x))  for all t∈K, x∈R^d.   (L)

Along any maximal local solution, in either time orientation, Gronwall gives

    1+V(X(t)) ≤ (1+V(X(s))) exp(C_K|t−s|).

Thus no solution can leave one compact sublevel set in a finite subinterval of K. On this compact set b is bounded and locally Lipschitz in x uniformly in time (polynomial coefficients with the stated time regularity). Bounded velocity gives an endpoint limit; local existence from that limit extends the solution. This rules out either finite endpoint of a maximal solution lying in I. Local uniqueness yields (C) and the identities

    Φ_{u,t}∘Φ_{t,s}=Φ_{u,s},    Φ_{s,t}=Φ_{t,s}^{−1}.

The absolute value in (L) supplies both time directions. A one-sided forward growth estimate alone is not silently treated as a two-sided completeness criterion. No spatial growth restriction on k is needed: finitely many complete trajectories over a compact time segment give finite continuous killing integrals even for signed, high-degree k.

Affine controls b_t(x)=A_t x+c_t with continuous coefficients satisfy (L) using V=||x||². Indeed

    |2x·(A_t x+c_t)| ≤ (2||A_t||+||c_t||)||x||²+||c_t||.

Compact time intervals bound the displayed coefficients. This recovers finite-law uniqueness/invertibility for affine controls without the SOS restrictions needed by other infinite-rank reverse-representation arguments.

## 7. Non-affine complete control and the excluded escape

A genuinely non-affine polynomial example in R² is

    b(x,y)=(x²+y²)(−y,x).

For V=x²+y², ∇V·b=0. All radii are conserved and the explicit complete flow is rotation through angle (x²+y²)(t−s). Its inverse rotates by the negative angle. It is not in general an affine or polynomial map of the starting point. Completeness therefore yields a genuine extension beyond affine polynomial-preserving pullbacks.

Take s=0, initial atoms (0,0), (1,0), (0,2), and weights (1/6,1/3,1/2), with signed time-dependent polynomial killing

    k_t(x,y)=t(x²+y²)+x.

The trajectories are (0,0), (cos t,sin t), and (−2 sin 4t,2 cos 4t). The killing integrals from zero are respectively

    K_0=0,
    K_1=t²/2+sin t,
    K_2=2t²+(cos 4t−1)/2.

Formula (F) is therefore an explicit all-real-time, three-atom positive hierarchy with constant full rank three. Distinct conserved radii make noncollision immediate. The signed killing is allowed without an SOS or nonnegativity promise.

By contrast b(x)=x² has X(t)=1/(1−t) from X(0)=1. It fails (C) on any supplied interval containing t=1. Therefore the damped-escape example with k=x⁴ is excluded at exactly the missing hypothesis, although its rank bound, positivity and moment smoothness hold. Similarly b=−x² is not complete backward through every positive point on an interval containing 0, excluding the predecessor's smooth inflow-from-infinity example. The repair does not contradict either example. Nonexplosion only along the initially represented support would not suffice: the reverse-inflow example starts at δ_0, whose known characteristic is stationary, yet another atom can enter from infinity. The proof must continue atoms discovered at an arbitrary maximal-rank time back to the reference time as well as forward. Also, b=x² is not complete through every spatial point on any nondegenerate finite interval, even one strictly before the displayed atom’s explosion. Its particular two-atom characteristic formula is valid before explosion, but that restricted formula does not meet the theorem’s global-through-every-point completeness hypothesis.

## 8. Invertibility and source-convention bookkeeping

For fixed b,k define, on finite atomic probabilities,

    T_{t,s}(μ)= (Φ_{t,s})_*[E_{t,s} μ] / ∫ E_{t,s} dμ,
    E_{t,s}(z)=exp(−∫_s^t k_u(Φ_{u,s}(z))du).

Every factor is positive finite at every finite atom. The complete flow is bijective. If ν=T_{t,s}(μ), recover μ by pulling each atom y back to z=Φ_{s,t}(y), multiplying its weight by 1/E_{t,s}(z), and normalizing. Equivalently T_{s,t} is the inverse because

    E_{s,t}(Φ_{t,s}(z)) E_{t,s}(z)=1.

The cocycle identity for E follows by splitting the integral. Consequently T_{u,t}T_{t,s}=T_{u,s}. The transitions are bijections of the class of all finite atomic probabilities and preserve the exact number of atoms. The unnormalized map has the same inverse formula without the normalization. These are fixed-control assertions; no injectivity conclusion for unspecified feedback/control choices is smuggled in. Abstract inverse formulas do not provide a numerical stability or effective reconstruction certificate.

The dual unnormalized measure equation associated with (H) is

    ∂_t μ=−div(b_t μ)−k_t μ.

If one instead writes the source's non-divergence distributional form

    ∂_t μ=−b_t·∇μ+h_t μ,

then multiplication/distributional differentiation gives h_t=−k_t−div b_t. The atom rate is h_t+div b_t=−k_t, not h_t alone. For normalized laws the source-convention coefficient becomes h_t=−k_t−div b_t+L_t(k_t). The radial rotation has div b=0; the x² escape has div b=2x. These conventions are not interchangeable.

## 9. Second repair: forward completeness and a lower bound on killing

A different sufficient condition is useful for genuine gradient descent. On a supplied interval [0,T), retain the polynomial regularity, normalization, coordinatewise C1, positivity, hierarchy, and local rank promise (R). Replace (C) by:

(C+) Every initial-value problem through every (s,z), s∈[0,T), has a unique characteristic through every later t<T.

(K−) For each H<T there is C_H≥0 with k_t(x)≥−C_H for every 0≤t≤H and x∈R^d.

Then every admitted abstract path is exactly the positive finite atomic forward evolution of its initial law. Its full rank is constant, and it is unique from that initial functional. Formula (F) holds with s=0, t≥0; it also holds for each forward transition between supplied times. Existence for any finite initial law follows directly from the forward complete characteristics and finite rates on their compact trajectory segments. This criterion does not assume or establish backward completeness through arbitrary later spatial points.

**Proof of the changed endpoint step.** All static GNS, chart, velocity and local weight arguments above apply unchanged. Since the coefficients of k have a common finite degree on [0,H], t↦L_t(k_t) is continuous. Unnormalize by

    ρ(t)=exp(−∫_0^t L_u(k_u)du),    A_t=ρ(t)L_t.

Then ρ is positive C1 and bounded above and away from zero on [0,H]; every A-coordinate is continuous, and

    A'_t(p)=A_t(b_t·∇p)−A_t(k_t p).

On a maximal-rank component J write its local atomic masses as c_j(t)=ρ(t)w_j(t). They obey c'_j=−k_t(X_j)c_j. Fix s∈J. For t∈J with t≤s, (K−) gives

    c_j(t)=c_j(s)exp(∫_t^s k_u(X_j(u))du)
          ≥c_j(s)exp(−C_H H)>0.                           (B)

Meanwhile M=sup_{0≤t≤H} A_t(||x||²)<∞ by coordinate continuity. Positivity yields

    c_j(t)||X_j(t)||² ≤ A_t(||x||²) ≤ M.

Thus each atom is uniformly bounded as the left endpoint τ of J is approached. This uses moment continuity only after establishing the nonvanishing mass bound (B); ordinary tightness alone did not suffice in the escape test. On the resulting compact spatial set, b and k are bounded. Bounded velocity gives a limit X_j(τ); local ODE theory extends the curve through it. The bounded killing rate gives a finite limiting integral and a positive limiting mass. Two endpoint atoms cannot coincide: uniqueness forward from their shared hypothetical endpoint would identify them at s. The endpoint functional consequently has exactly r distinct positive atoms. The positive Gram determinant argument extends J through its left endpoint.

At the right endpoint use (C+): each atom present at s extends there along a bounded-on-that-segment continuous characteristic; killing is finite on those curves, and uniqueness prevents collisions. This supplies exactly the right-endpoint reasoning of §5. Hence J is all [0,H], and arbitrary H proves the second theorem. In particular lower-bounded killing prevents a new positive atom from entering the abstract finite-rank path from infinity. The counterexample with reverse-time inflow has k=−x⁴ and fails (K−).

The other direction remains essential: the original damped escape has k=x⁴≥0 and hence satisfies (K−), but b=x² fails (C+). Thus the lower killing bound alone does not prevent forward escape.

**Autonomous coercive gradient example.** If F:R^d→R is a coercive polynomial, take b=−∇F and k=F. F is bounded below, supplying (K−). Along any characteristic,

    dF(X(t))/dt=−||∇F(X(t))||²≤0.

The forward trajectory stays in the compact sublevel {F≤F(X(s))}; local polynomial ODE existence and uniqueness then extend it through every finite future time, supplying (C+). The second theorem applies to this gradient/selection hierarchy under (R), with any finite initial law. This assertion is for autonomous F: pointwise coercivity of an arbitrary time-dependent F_t is not silently made into a common-sublevel bound.

For example F(x)=x⁴/4 gives b=−x³, k=x⁴/4 and, with h=t−s≥0,

    Φ_{s+h,s}(a)=a/sqrt(1+2a²h),
    ∫_s^{s+h} k(X(u))du = (a²/8)(1−1/(1+2a²h)).

It is forward complete, while every nonzero trajectory explodes in the backward direction at h=−1/(2a²). Thus this is genuinely beyond criterion (C). Positive atomic weights follow the finite exponential formula and never vanish at a finite forward time.

**Injectivity, but not global surjectivity.** Unique forward trajectories cannot merge on their common finite segment, so Φ_{t,s} is injective; it may not be onto. Positive finite reweighting therefore makes the finite-law transition injective. Its inverse is defined on its actual forward image by recovering the unique preimage positions and undoing the weights as in §8. It need not define a map on every later finite law. In the explicit −x³ example at duration h>0, the spatial image is the proper interval (−1/sqrt(2h),1/sqrt(2h)); on that interval the inverse is y/sqrt(1−2hy²). A Dirac mass outside the image has no earlier finite-law preimage. Consequently the all-finite-law bijection in §8 belongs to the two-sided-complete theorem, not this second criterion.

This creates a conditional interface to gradient mathematics without identifying a numerical law with an actual noetic realization. The rank promise remains a hypothesis on an abstract path, including in this example.

## 10. Verification, limits, and next use

`check_exact.py` verifies local Hermite values/gradients, conserved radius and divergence, the explicit non-affine trajectories and their killing integrals, unnormalized polynomial generator identities and normalized quotient algebra, a time-dependent affine example, finite-weight inverse algebra, the forward-complete coercive quartic gradient example and its image inverse, and the escape/source-convention discriminator. These exact finite controls supplement the general proof rather than establish it by enumeration. `EXACT_CHECKS.json` gives the executed check count and input-preservation result.

This is conditional representation and continuation mathematics. It identifies a supplied abstract hierarchy with a numerical finite law under explicit rank and completeness promises. It does not authenticate tokens, identify an actual noetic or metaphysical bearer, certify target truth or epistemic warrant, settle the unrestricted infinite-rank hierarchy problem, or show that bare initial finite rank enforces (R). It supplies neither an independent review nor a closure decision.
