# Independent review: gradient discretization fidelity

10 October 2026 UTC. Ordinary independent mathematical review of the additive numerical-fidelity application. The author files are not edited by this reviewer. No integration, protected edit, formal-kernel certification, external novelty, inspected DAEE defect, or programme closure is asserted.

## Reviewed claims and proof assessment

The reviewed source is `gradient-discretization-fidelity-20261010/RESULT.md` and its executable `check_exact.py`; exact frozen bindings and replay results are recorded separately in `REVIEW_RECEIPT.json`. This report assesses the mathematics at the stated one-step/local-consistency scope, rather than importing a numerical guarantee from the continuous reverse-lift ancestors.

### 1. Raw Euler failure at a moving Dirac

The selection term cancels identically at a Dirac. Its Euler first and second moments are x+τb and xxᵀ+τ(xbᵀ+bxᵀ), so the covariance is exactly −τ²bbᵀ. For b≠0 and every τ>0 this has a negative quadratic-form direction. The displayed affine square is a direct certificate. This is an exact sign obstruction, not a rounding threshold, and no positive step size repairs raw Euler of these moments.

### 2. Universal finite-support extension

After repeated positions are merged, a separating linear form exists for every finite distinct support. The Lagrange factor e_j has the correct point values; its square eliminates both value and gradient at the other points. The correction in q gives q(x_j)=1 and ∇q(x_j)=−C b_j. Thus Λτ(q²)=w_j(A_j−|A_j|−1)<0 for the specified C. The degree bound deg(q²)≤4r−2 is correct, including r=1.

If all b_i vanish, nonnegative signed masses w_iA_i are sufficient, while Lagrange isolation proves necessity. Hence the moving-atom hypothesis is substantive. Covariance is sufficient for the Dirac obstruction but is not a universal finite-support detector: the independent two-atom quartic control below retains positive covariance while failing a degree-six square.

The report correctly distinguishes Euler of every retained hierarchy coordinate from Euler in a finite reconstruction chart followed by rebuilding higher moments. In particular the open rank-two three-moment chart is not ruled out by this theorem. It does not diagnose an actual implementation.

### 3. Law-valued rational repair and repeated atoms

The minimum shift gives d_i≥1 for every τ>0. Positive old weights therefore produce positive normalized new weights, so all polynomial square moments are nonnegative by a single actual law. This positivity assertion is independent of descent or injectivity. Equal input positions move together and receive equal factors; aggregation commutes with the step and preserves internal mass ratios if redundant labels are retained. This is dynamic consistency of a representation, not a new nondegenerate collision metric.

The rational step is not the exact fixed-position replicator flow; the exponential variant is that flow only after fixing the moved positions. Both variants have the stated invariance under adding a constant to F.

### 4. Descent and rank conditions

The upper Hessian bound on the actual step segment gives the Taylor estimate in §4. Checking only the starting point or a region that excludes part of the step would not suffice. The reweighting covariance identity and its rational sum-of-squares form have the correct sign and coefficient. Selection is strict exactly when the moved energies differ. Transport strictness requires a nonzero gradient with τL_i<2; the endpoint τL_i=2 only gives nonincrease.

For injectivity, the common convex-domain upper Hessian bound is enough: integrating along a chord makes T strongly monotone when τL<1. An absolute operator-norm bound is sufficient but unnecessary. The lower separation estimate follows by Cauchy–Schwarz. Positive weights and distinct points then retain full Hankel rank r. Under one common segment-containing region and τL<1, zero total energy loss forces every gradient to vanish and every occupied energy to agree. This proves the final source’s stationary-state/fixed-point equivalence, without identifying such points as minima.

Inverse recovery is correctly restricted to known fixed τ, F, the reweighting rule, and the declared injective domain. It is only an inverse on the actual range. Unrecorded varying steps cannot be discarded: the independent exact example x=1, τ=1/12 and x=21/20, τ=3200/27783 satisfies both quartic guards and produces the same output Dirac at 11/12. This does not refute the fixed-step claim.

### 5. First-order consistency and tied minima

For a fixed finite initial law and fixed polynomial test, the minimum is Lipschitz as a function of its finitely many values, even at ties. Therefore c(τ)=c(0)+O(τ), which is all the rational expansion needs. Its common c(0) contribution cancels after normalization. Combining the positional and mass expansions gives exactly the inherited joint-metric negative-gradient vector field and an O(τ²) coordinate local error.

Differentiability of the argmin or of the minimum across ties is not assumed. No uniform-in-degree estimate, unrestricted state-space error bound, global numerical convergence, gradient-flow distance contraction, or minimization guarantee follows from these local statements. The report does not claim them.

### 6. Guarded exact quartic implementation

The normalization is F=x⁴/4, not x⁴. Thus L=3M² and τ≤1/(6M²) imply τL≤1/2. The multiplier 1−τx² lies in [5/6,1], so positions and their whole segments stay in the certified interval. The derivative of T is at least 1/2 there. The zero-radius case is stationary and requires no division by M.

Inspection of the source confirms use of `fractions.Fraction` for accepted numeric inputs, explicit float/bool rejection, positive normalized weights, duplicate aggregation, exact guard comparison, and inclusion of τ, the potential/rule identifiers, and the certified interval in the returned step record. SymPy controls check algebra, rather than floating-point tolerances. This does not provide a formal kernel proof, complexity bound, robust floating-point implementation, or production-quality integrator certification.

## Independent exact controls

`check_independent.py` is separately written and imports no author code. It checks 91 exact identities, inequalities, and deliberately bounded examples. These include:

- Symbolic three-dimensional Dirac covariance.
- A quartic two-atom raw Euler record at τ=1/100 with covariance 3039/1600>0 but Λτ(q²)=−2/3 for a degree-six square.
- A separate two-dimensional three-node Hermite value-and-gradient construction.
- Zero-drift selection controls, including a positive small step and a negative large-step coefficient.
- Several rational laws at the quartic guard endpoint, the zero-radius case, repeated labels, exact square-moment identities, and four repeated guarded steps.
- Exact duplicate aggregation and preservation of internal mass ratios.
- Unguarded energy growth and collision, the quadratic τL=1 collision, and non-strict descent at τL=2.
- The wrong quartic normalization as a countercontrol, equal outputs under distinct unrecorded guarded step choices, and a stationary nonminimum with equal energies and zero gradients.
- Rational first-order offset cancellation, a genuinely switching minimum for F=x⁴−x³, and whole-step derivatives of moments through degree six.
- The pairwise covariance and rational-factor difference identities.

These controls supplement, rather than replace, the universal arguments above. Fresh replay passed 207 portable author controls and 210 controls with three additional live-original input-preservation checks. The 210-control replay JSON is byte-identical to the authoritative author-run JSON. Original/copy hash comparisons are recorded in the receipt.

## Literature and ancestry boundary

The three directly bound ancestor reports have their stated roles: continuous finite-atomic gradient geometry, the radial-quartic unrestricted-rank reverse lift, and the finite rank-two chart. No discrete preservation theorem is inherited merely from their continuous realizability statements.

I independently checked the cited primary-source passages. Vikas et al. discuss positivity of an effective velocity distribution in a spatial finite-volume construction; the context is distinct from this raw derivative-of-evaluation step. [AIAA 2010-1080, §§2.5–2.5.1](https://cfd.ku.edu/papers/AIAA-2010-1080.pdf).

The Chu et al. abstract states a model-specific fermion closure, limiter, CFL condition, and IMEX composition. The packet does not transfer that guarantee or claim an impossibility theorem for all SSP methods. [Primary abstract](https://arxiv.org/abs/1809.06949).

The recorded local search is a bounded deduplication check only. No exhaustive historical or novelty judgment is supplied here.

## Mathematical disposition

The claims are valid at the expressly stated full-hierarchy obstruction, finite-particle structural-preservation, and fixed-law first-order-consistency scope. No mathematical revision is required. This disposition binds only the precise frozen sources and successful replay recorded in `REVIEW_RECEIPT.json`; it carries no integration or closure authority.
