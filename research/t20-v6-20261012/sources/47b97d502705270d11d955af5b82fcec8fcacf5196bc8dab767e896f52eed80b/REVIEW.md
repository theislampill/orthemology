# Independent review of leafwise Fisher geometry

10 October 2026 UTC. Review of the frozen mathematical packet in `leafwise-noetic-geometry-20261010`. The root and derivation worker are joint authors. This reviewer did not edit their result or control script and reconstructed the proofs and finite controls independently. This is an ordinary mathematical review, not formal-kernel certification, empirical validation, field-wide novelty certification, protected-source integration, or programme closure.

## Verdict and binding

No blocking mathematical error was found in the frozen result. The one-objective whole-positive-fibre criterion, global block-mass objective classification, complete proper interaction corollary, global exponential-leaf mean coordinates, exact induced Fisher dynamics, invariant-class reconstruction, and positive-likelihood preservation criterion are correct under their stated hypotheses.

The reviewed result has SHA256 `6d5c3c38f6e89c8f74f3b5d58cabcace7b9cae0eb2d6f8bf3a2f6ef4f4aef724`. The reviewed author script has SHA256 `65f195f5573411844423cc67bbafe471cec8edaadd5781563ccbf9d199ca3249`. The author's manifest has SHA256 `1ed0d611e6f9e85a594573328e4ec4234cb65ec400404295f8a17857e1a7d115`. Every listed author-manifest entry and every local inherited-input binding was checked against current bytes.

The separate `independent_controls.py` passed 37 exact control groups in Python 3.12.14 and SymPy 1.14.0. A copy of the frozen author script, run in `author-replay` without modifying its original directory, passed all 43 author control groups. These executions support the calculations below; the finite tests are not substitutes for the general proofs.

## One objective at one positive fibre

Let M have independent rows forming V, with first row 1. Its mass-one image has affine dimension dim(V)−1. An intrinsic objective differential therefore has ambient representatives differing precisely by a multiple of the mass covector. If f=Mᵀg, replacing that representative adds a constant to f. Both membership in A(V) and the Fisher field are unaffected.

At Mp=z the negative fine Fisher gradient is

    X(p)=−diag(p)f+(g·z)p.

The sign and normalization follow directly by pairing its negative with every sum-zero tangent in the metric Σ h_x k_x/p_x. For p and q in the same positive fibre,

    M X(p)−M X(q)=−M diag(f)(p−q).

Every h in ker M is a mass-zero direction. From any fixed positive p, both p+εh and p−εh remain positive for sufficiently small ε. Thus constancy on the entire positive fibre is equivalent to M diag(f) annihilating ker M. Row/kernel duality makes that equivalent to every row of M diag(f) lying in row(M), namely fV⊆V. The reverse implication follows from the same identity. This proves the exact iff without assuming a linear or continuous decoder.

Full row rank also ensures that f constant is equivalent to the intrinsic differential being zero. The argument does not incorrectly demand that a chosen mass-coordinate derivative vanish. At an isolated critical moment the field is exactly zero, even if J is nonconstant elsewhere; this is compatible with the global conclusion.

The interior-fibre premise is justified. A strictly positive combination of the statistic evaluation points cannot lie on a proper supporting face: equality of the support functional at a positive weighted average would force equality at every point. Conversely, let b be a strictly positive barycentre and z an interior point. For sufficiently small ε>0, y=z+ε(z−b) remains in the polytope, and z=(y+εb)/(1+ε) has a strictly positive representing law. Hence the positive image is exactly the relative interior.

## Global classification and its algebraic blocks

A(V) is a unital subalgebra of real functions on a finite set. To reconstruct the partition proof, declare two states equivalent when all its functions agree there. A generic linear combination of a basis separates the distinct equivalence classes, since the finitely many forbidden equalities are proper hyperplanes. Lagrange polynomials in that separating element produce all block indicators. Therefore A(V) is exactly the blockconstant algebra; this conclusion needs no positivity assumption on its functions.

Each block indicator lies in V, so its mass w_j is a linear function of the retained moment. If f(z) is blockconstant, dJ_z(Mh)=f(z)·h=0 whenever all block-mass changes vanish. The intersection of the convex interior moment domain with any fixed-w affine slice is convex. Integrating along a segment within it proves that J is constant on the entire slice, not merely locally constant. Choosing a fixed strictly positive conditional law in each block gives a linear global section w↦p(w). Consequently Φ(w)=J(Mp(w)) has the same C² regularity and J=Φ∘w. Conversely, the differential of any such factorization has blockconstant fitness, so the local criterion applies at every moment.

There is no topological factorization gap and no assumption that every block slice admits arbitrary ambient directions outside its domain. Convexity supplies precisely the connecting segments used. The descended field is smooth: for a blockconstant fitness, multiplication by f preserves V, and its coefficients depend smoothly on w through dΦ.

For the five-state mixed example, the four-state two-bit block has only scalar stabilizing fitnesses, while the separate atom permits an independent value. Thus A=span{1_B,1_e}. For J=w the retained unnormalized block moments satisfy

    w′=−w(1−w),  u′=−u(1−w),  v′=−v(1−w).

At w=1/2, zero conditional unary means, and conditional correlations ±1/2, J=u instead gives v′=∓1/4. Both the block classification and this distinction were reconstructed exactly.

These are observable-space stabilizer blocks, not intrinsic components of the positive moment cone. A concrete countercontrol uses V=span{1,x} on x=−1,0,1. Its stabilizer is scalar, since x² is not affine on those three points. Yet its cone is generated by the independent rays (1,−1) and (1,1), and decomposes into their sum. The middle column is their average. The independent script checks the nontrivial positive complementary cone projections explicitly. No unrestricted diagonal-lift theorem can identify these two partitions.

## Complete proper finite-product interactions

The categorical proof survives the fact that products of contrasts on the same slot can have several grades. Choose a nonzero component f_S of highest support degree d≥1. Since d≤k<m, a disjoint T of size k−d+1 exists. A nonzero pure contrast h_T belongs to V_k. Project f h_T to H_(S∪T). Outside T, multiplication cannot introduce or remove a contrast; a contributing component f_U must have U\T=S. Therefore U contains S. Maximality of d forces U=S, so the surviving component is exactly the nonzero tensor f_S⊗h_T of degree k+1. This is a contradiction.

Thus A(V_k)=span{1}. Combining it with the local theorem gives dJ_z=0 as the exact criterion at every interior z. Requiring it throughout the connected interior makes J constant and the field zero. The proof neither requires that every pair in a fibre distinguish a nonzero differential nor asserts that one selected trajectory cannot admit a smaller description. At full order, V=R^X and all objectives descend; with only the mass statistic the intrinsic objective domain is a point.

## Global mean parametrization and dual metric

For basis {1,φ_1,…,φ_d}, all finite references r_x>0, and

    A_r(θ)=log Σ_x r_x exp(θ·φ(x)),

finite differentiation gives ∇A_r=E_θφ and Hess A_r=Cov_θ(φ). The covariance is strictly positive definite: a zero variance would make a nonzero combination a·φ constant on the full support, contradicting basis independence. Integrating this positive Hessian along a line proves strict monotonicity of the gradient and hence injectivity.

For surjectivity, fix z in the interior of P=conv{φ(x)} and choose δ>0 such that its δ-ball is in P. The support function then gives max_x θ·(φ(x)−z)≥δ||θ||. As r_min>0,

    A_r(θ)−θ·z ≥ log(r_min)+δ||θ||.

This is a genuine coercive bound in every parameter direction, not merely strict convexity. A minimizer exists; positive Hessian makes it unique; its first-order condition gives ∇A_r(θ)=z. Invertibility of the Hessian gives local smooth inverses, which uniqueness patches to a global smooth inverse. The d=0 case is the trivial one-point map. No compactness of parameter space or unproved general exponential-family theorem is needed.

The Legendre expression ψ_r(z)=θ_r(z)·z−A_r(θ_r(z)) differentiates to ∇ψ_r=θ_r and Hess ψ_r=C_r(z)⁻¹. Substitution in the relative-entropy expression gives exactly

    Σ p_x log(p_x/r_x)=D_KL(p||p_(r,θ_r(z)))+ψ_r(z).

Consequently the leaf member is the unique constrained relative-entropy minimizer, including comparison laws with zeros. This variational characterization does not identify an arbitrary actual law with the selected leaf member.

## Geometry, leaf invariance, and maximal flow intervals

The embedding derivative sends a to p(a·(φ−z)). Pulling back the full Fisher metric gives aᵀCb. Since dz=C dθ, the mean-coordinate metric is C⁻¹. The leaf tangent is Fisher-orthogonal to ker M: pairing it with h in ker M gives Σ(a·(φ−z))h=0. Their dimensions exhaust the fine tangent space. Therefore the unique least-energy lift of u is p(φ−z)ᵀC⁻¹u, with energy uᵀC⁻¹u. The author's added horizontal-lift interpretation is correct.

For any C² J, the leaf parameter gradient is C⁻¹(C∇J)=∇J. Its negative flow is θ′=−∇J(z), z′=−C∇J(z), and p′=−p ∇J(z)·(φ−z). The latter is exactly the full fine gradient, so restricting to a leaf preserves the vector and time parameter. The energy derivative is −∇JᵀC∇J and vanishes precisely at critical points. A critical point is stationary by local uniqueness.

The log-density derivative belongs to V, so [log p] in R^X/V is conserved. Two positive laws have the same class exactly when their log ratio is constant plus a combination of φ; normalization converts this into an exponential tilt. Each class defines one leaf, and the global mean theorem gives exactly one point of that leaf at every interior moment. Every quotient class has a real representative w, giving a positive reference exp(w). Thus (moment,class) is bijective onto int(P)×(R^X/V). Choosing a linear complement and applying the parameter-dependent inverse theorem gives smooth reconstruction. Dimensions add to n−1; this retains the complete positive law.

Changing r within its leaf to r exp(b+a·φ) gives the new parameter label θ_new=θ_old−a and changes ψ by −b−a·z. Covariance and the mean metric therefore remain unchanged. Changing the class can change covariance at the same mean.

All flow equivalences are on their maximal positive interior interval. Bounded ∇J gives bounded parameter velocity, hence no finite-time parameter escape; compact parameter neighborhoods then support the ordinary extension argument. Arbitrary C² objectives do not have this bound. The independent control J(u,v)=−atanh(u) on the uniform two-bit product leaf gives u′=1, v′=0, so from zero means it reaches the boundary at time 1. This confirms that the author's all-time qualification is substantive. Zero likelihoods similarly leave the positive domain and are excluded rather than silently assigned an interior metric.

## Exact finite likelihood criterion and two-bit reconstruction

For positive L,

    log posterior−log prior=log L−log E_p L.

The constant term lies in V. Hence even one positive prior and its posterior belong to the same leaf exactly when log L∈V. If log L=b+a·φ, the new parameter is θ+a and the branch normalizer is exp(b+A_r(θ+a)−A_r(θ)). Otherwise the leaf changes to E_(rL); the update remains calculable given the old leaf and moment, but closure in that same leaf fails. This is different from the whole-simplex multiplier requirement LV⊆V. Merely L∈V is not enough.

For r_ρ=(1+ρxy)/4 and ρ=±1/2, both unary means are zero and C=[[1,ρ],[ρ,1]]. The objective J=z_1 gives velocities (−1,−ρ), so the discrepancy changes direction. The exact linear-objective orbit has means (−tanh t,−ρ tanh t); the independent script checks its value at t=log 2 entirely rationally. At arbitrary means (u,v), the fibre parameter c has interval −1+|u+v|<c<1−|u−v| and covariance off-diagonal c−uv. Comparing c with c′ gives −(c−c′)(b,a) for covector (a,b). Thus the two-bit obstruction holds at every interior mean, not only at the origin.

The reference odds ratios are 9 and 1/9. Starting from ρ=1/2, the tilt (1+x/3)(1+y/4) gives exact means (11/25,2/5), raw interaction 14/25, and unchanged odds ratio 9. Fixed log interaction therefore does not mean fixed raw interaction or independence. The additive positive L=1+(x+y)/4 belongs to the unary observable space but produces odds ratio 3/4 from the uniform law; its mixed log coefficient is log(3/4)/4. Rescaling by 2/3 makes a valid event likelihood and changes neither posterior nor this failure.

## Inheritance checked against actual passages

The reviewer inspected the following local results directly, rather than relying solely on the author's summary:

- `tensor-moment-continuation-20261009/RESULT.md`, §§2–5 and 7–9: the evolving Fisher replicator equation, covariance mobility, exponential controls, finite sufficient moment closure, and rich-control continuation theorem are already present. Its fixed-objective caveat is explicit. The leaf packet's individual-objective classification specializes a different observable-space question and does not replace that caveat with an invalid rich-control converse.
- `noetic-gradient-transport-20261009/RESULT.md`, §§2–5: μ is fixed auxiliary geometric data, and its weighted-quadratic tangent metric is constant. Its induced quotient field depends only on the coarse state. The particular-objective support-graph condition asks agreement with a separately prescribed canonical channel metric. None of these results is contradicted by fibre dependence of the evolving-Fisher covariance. Its least-energy tangent quotient proof is correctly related to the leafwise horizontal lift.
- `state-dependent-gradient-obstruction-20261009/RESULT.md`, §§2–4: this already gives a one-linear-objective same-fibre counterexample and deterministic-channel controls. It does not give the present exact criterion for every individual objective on each complete proper hierarchy.
- `tensor-likelihood-closure-20261010/RESULT.md`, §§3–4 and the start of §5: the general multiplier mechanism and the categorical constant-stabilizer proof are genuine inputs. The new packet properly attributes them, retains posterior/probability/domain distinctions, and does not identify passive diagonal updating with arbitrary state-changing instruments.

The author-hosted [Wainwright and Jordan text](https://people.eecs.berkeley.edu/~jordan/sail/readings/wainwright-jordan-fnt.pdf) was independently checked at Proposition 2, Proposition 3, Theorem 1, and Proposition 18. Those numbered loci in this version support the claimed classical covariance, mean-map, and duality ancestry. The proof review above is self-contained in the finite setting; no general-measure theorem, source-byte pin, full-paper review, or comprehensive literature search is asserted.

## Scope assessment and remaining limits

The result appropriately distinguishes a conditional model restriction from universal compression. Choosing a reference class is additional model data; recording arbitrary classes alongside the moments recovers all positive fine-state information. A maximum-entropy or product representative is not inferred from a moment record alone.

The report also keeps separate objective descent, evidence receipt, exact posterior sufficiency, and actual warranted learning. It specifies no physical or cognitive realization of the law or metric, no justified objective or reference-selection procedure, no source authentication, no actual truth criterion, no intervention permission, and no sampling or computational efficiency guarantee. It does not claim Newtonian mechanics or finite empirical samples instantiate these equations. Its exponential leaves are generally nonconvex as subsets of law space, so convex restricted-prior cone results cannot be transferred without their own premises.

No additional mathematical revision is required for the bounded frozen claims reviewed here. Any future change to the hypotheses, positive domain, objective class, reference selection, likelihood support, or claimed application needs a corresponding new check. This review supplies no merge, release, closure, or lifecycle authority.
