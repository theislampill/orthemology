# Independent review: fixed audit transport of Fisher–Rao path length

11 October 2026 UTC. Verdict: **the explicit counterexample and uniform two-sided metric repair are valid**. The final root report incorporates the regularity clarification and direct metric proof supplied during review. Its amended section was read and checked before binding this review; the rectifiability conclusion needs no differentiability.

## Reviewed bindings

- `audit-fisher-length-transport-20261011/RESULT.md`: SHA-256 `00c38a528d3d8030627eb4dd8e11aa44bb6abfa122efd2da26ece4e8e93a8a58`.
- Earlier reviewed infinite-length root report: `infinite-initial-fisher-length-20261011/RESULT.md`, SHA-256 `e8743a543021cd86d205c7b757c038f2acaeb80e0ecc117f1ebf1cef6d6493ec`.
- Earlier independent proof review: `initial-fisher-length-independent-review-20261011/REVIEW.md`, SHA-256 `35efa98e6673b44566fb1c6a26dffc4c6a699ec7a59356f60bac70414cb3a6fb`.

This review concerns countable-state probability laws, the fixed exponential tilt, fixed Bayes reweighting, and Fisher–Rao metric convention g_q(h,h)=sum h_n²/q_n. No corpus survey, full re-review of endpoint discretization, source-warrant assertion, or protected-source edit was performed.

## 1. Exact normalized audit and unchanged support

The original p has p_0=1/2 and p_n=1/[2n(n+1)], n≥1. Its fixed loss is V_0=0 and V_n=exp(n²). Let L_0=1 and L_n=(n+1)/n³. Then 0<L_n≤2: for n≥1, L_n=n⁻²+n⁻³≤2, with equality at n=1. Its infimum is zero, despite every individual value being positive.

For n≥1, p_nL_n=1/(2n⁴); hence

    Z_L(p)=(1+ζ(4))/2,
    p'_0=1/(1+ζ(4)),
    p'_n=1/[(1+ζ(4))n⁴].

These masses sum to one. All states retain positive mass. The audit is defined for every probability on this countable state space, since L is everywhere positive and bounded. The exponential tilt is also defined for every t≥0, since all losses are finite and nonnegative. The product normalizer sum p_nL_n exp(−tV_n) is finite and strictly positive. Cancelling normalizers proves B_L(S_t p)=S_t(B_L p) exactly, including at zero. No moment assumption or support deletion enters this commutation proof.

## 2. Finite audited length versus infinite original length

The previous harmonic lower-bound proof establishes infinite length for the original exponential orbit in every (0,ε]. For the audited law let r_n(t)=sqrt(p'_n)exp(−tV_n/2) and x(t)=r(t)/||r(t)||_2. On positive delayed intervals these are smooth Hilbert-space curves. Since V_0=0,

    ||r(t)||_2≥sqrt(p'_0),
    x'(t)=(I−x(t)⊗x(t))r'(t)/||r(t)||_2,
    ||x'(t)||_2≤sum_{n≥1}|r'_n(t)|/sqrt(p'_0).

The Fisher–Rao speed is 2||x'(t)||_2. Tonelli and the scalar integral give

    L_FR≤[2/sqrt(p'_0)]sum_{n≥1}sqrt(p'_n)[1−exp(−TV_n/2)]
        =2sum_{n≥1}n⁻²[1−exp(−T exp(n²)/2)]
        ≤2ζ(2)<∞.

Endpoint continuity extends this to [0,T]. Equivalently, r has an integrable Hilbert derivative and is absolutely continuous down to zero; normalization is Lipschitz on this path's region ||r||≥sqrt(p'_0). Thus this is an actual finite metric arc-length bound, not merely a formal derivative integral. The bound is even uniform over finite T, though that strengthening is not needed.

The audited initial mean remains infinite because exp(n²)/n⁴ does not tend to zero. The finite-length conclusion therefore does not secretly invoke the finite-mean sufficient repair.

Both original and audited endpoints have finite intrinsic Fisher–Rao distance from their respective initial laws. The contrast concerns the lengths of these particular commuting orbits. It neither establishes infinite endpoint separation nor rules out other finite-length paths.

## 3. Inverse likelihood: unbounded function, checked image domain

The reciprocal likelihood K=1/L has K_0=1 and K_n=n³/(n+1), which is unbounded. The inverse audit B_K is defined precisely on probabilities ν satisfying

    0<E_νK<∞.

Strict positivity makes the lower inequality automatic; finiteness is a real condition. If ν=B_L μ for any probability μ, then

    E_νK=1/E_μL<∞,
    B_Kν=μ.

Conversely, any ν with finite E_νK lies in the image, by μ=B_Kν. Thus there is an exact inverse on the appropriate image, without a global bounded-condition metric estimate.

Along this particular original orbit μ_t=S_t p, one even has E_{μ_t}L≥μ_t({0})≥1/2 and E_{μ_t}L≤2; consequently the inverse expectation on ν_t=B_Lμ_t lies in [1/2,2]. These finite normalization bounds do not bound the pointwise reciprocal likelihood and do not restore lower tangent comparison.

The image is not the entire probability simplex: take ν_0=1/2 and ν_n=1/[2ζ(2)n²] for n≥1. Then sum_{n≥1}ν_nK_n is a positive constant times sum n/(n+1), which diverges. The inverse audit is undefined there. No such domain failure occurs for the displayed commuting paths.

## 4. Correct tangent map and variance constants

Fix a common domain on which 0<ell≤L≤u<∞. With ν=B_L μ and Z=E_μL,

    ell≤Z≤u,
    ell/u≤dν/dμ=L/Z≤u/ell.

For a Fisher-regular tangent inside a fixed support face, write dμ'=v dμ with E_μv=0 and E_μv²<∞. Bounded likelihood makes all required first moments finite. Differentiating normalized reweighting gives

    dν'=(v−E_νv)dν.

The audited tangent norm squared is Var_ν(v). Using Var_ρ(v)=inf_c E_ρ[(v−c)²], the pointwise density bounds imply

    (ell/u)Var_μ(v)≤Var_ν(v)≤(u/ell)Var_μ(v).

Taking the infimum preserves the lower bound as well as the upper one; centering in the two different laws causes no coefficient error. Square roots give the stated speed constants. The formula uses Fisher-regular score tangents; it should not be read as a claim that every total-variation derivative has a square-integrable score or that boundary support-creation tangents are captured by this score expression.

For locally Fisher–Rao absolutely continuous paths, and in particular all positive-time portions of the exponential orbits here, integration gives the length comparison. The final root report uses this regularity qualification explicitly. Its unrestricted metric rectifiability conclusion is justified independently next.

## 5. Global metric proof: rectifiability for arbitrary continuous curves

In square-root coordinates on the nonnegative unit sphere, reweighting is

    F(x)=A x/||A x||_2,  A=diag(sqrt(L_n)).

The bounds sqrt(ell)||z||_2≤||Az||_2≤sqrt(u)||z||_2 hold for all z. Differentiating this Hilbert-sphere map yields

    ||DF_x h||_2≤sqrt(u/ell)||h||_2.

Its inverse is the corresponding normalized map for A⁻¹ and has the same Lipschitz constant bound. A shortest nonnegative great-circle arc between two probability square roots remains in the domain. Integrating the derivative estimate along this smooth arc, then applying the inverse estimate, proves the global intrinsic-distance comparison

    sqrt(ell/u)d_FR(μ_1,μ_2)
       ≤d_FR(B_Lμ_1,B_Lμ_2)
       ≤sqrt(u/ell)d_FR(μ_1,μ_2).

For countable laws with zeros this Hilbert argument also handles boundary points, without assigning score tangents at zero masses. For general dominated measures the same multiplication-operator proof applies on L².

Taking suprema of sums of distances over partitions gives identical constants for metric arc lengths of any continuous curve. Thus rectifiability preservation does not require a possibly ambiguous appeal to integrating derivatives of an arbitrary differentiable curve. Uniform lower and upper likelihood bounds genuinely give the claimed metric repair.

## 6. Scope and verdict

The counterexample uses an infinite state space essentially for a fixed everywhere-positive likelihood whose infimum is zero. On a finite support, fixed positive likelihood values have a positive minimum, so the two-sided repair applies automatically. On infinite support these bounds are sufficient, not necessary for every individual path.

The bounded strictly positive audit can therefore map a nonrectifiable prescribed exponential orbit to a rectifiable commuting orbit, while preserving support and admitting an inverse on that image. Exact operator commutation is weaker than control of metric costs. This is a correct scoped ordinary mathematical result. No finite numerical tests were used or claimed to establish either infinite or finite length, and no global novelty, epistemic reliability, or psychological consequence is inferred.
