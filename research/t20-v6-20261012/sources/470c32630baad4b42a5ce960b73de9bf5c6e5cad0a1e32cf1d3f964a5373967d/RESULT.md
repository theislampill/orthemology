# A fibrewise exact-law correction using classical W–FR splitting

11 October 2026 UTC. Additive ordinary mathematics within ACTIVE T20. This is an author-side construction, with the parent supplying the proposed split, regularization/moment argument and matrix fixture. The investigator supplied the proof details and controls. It is not independent review, protected integration, formal-kernel certification, empirical warrant, or programme closure.

## 1. Result, and an important attribution boundary

The full fixed-marginal gradient can lower integrated conditional entropy while worsening individual fibres. Its inherited stricter control rule, with observed velocity zero and conditionally centred reaction, avoids that defect when a suitable continuous solution exists. Here is a globally defined **discrete law-valued** alternative that does not assume existence of that nonlinear PDE.

Fix a Borel probability ν on Y=R^k, a Borel function g:Y→R^m, and a symmetric positive-definite m×m matrix T. The supplied target is

    π(dy,dz)=ν(dy)π_y(dz),          π_y=N(g(y),T).

Let μ₀=ν(dy)r₀,y(dz) be any probability kernel satisfying

    M₀=∫(z−g(y))ᵀT⁻¹(z−g(y)) dμ₀(y,z)<∞.             (1)

The conditional laws may be singular, discrete, or non-Gaussian. Neither ν nor g needs a density, smoothness, a spectral gap or a finite ordinary second moment. All conditional statements are ν-almost everywhere.

For each fixed step h>0 set

    A=e^(−hT⁻¹),       Q=T(I−A²)>0,       a=e^(−h).

Apply these two exact substeps separately at every observed y:

    D_h: Z↦g(y)+A(Z−g(y))+ξ,              ξ~N(0,Q),
    R_h: f↦f^a/Z_y(a),                    Z_y(a)=∫f^a dπ_y,
    f=d(D_h r_y)/dπ_y,                    Φ_h=R_h D_h.        (2)

Then μₙ=ν(dy)rₙ,y(dz), rₙ₊₁,y=Φ_h rₙ,y, is well defined for every n≥0. Every substep preserves the **entire** observed marginal ν. The first step has finite integrated conditional KL; thereafter every fibre's KL is nonincreasing, and indeed

    Hₙ₊₁(y)≤exp[−2h/λ_max(T)] Hₙ(y),
    Eₙ₊₁≤exp[−2h/λ_max(T)] Eₙ,                    n≥1,       (3)
    Hₙ(y)=KL(rₙ,y||π_y),          Eₙ=∫Hₙ dν.

Thus μₙ→π in KL and total variation as n→∞. If E₀<∞, (3) also holds from n=0. The displayed rate only records the standard OU/LSI bound; no rate optimization is attempted.

**The basic scheme and its Gaussian update are already in the literature.** Crucinio and Pathiraja, *An operator splitting analysis of Wasserstein–Fisher–Rao gradient flows*, [arXiv:2511.18060v3](https://arxiv.org/html/2511.18060v3), §2 equation (2.5) and display (W-FR), and §3 equations (3.3)–(3.4), explicitly study exact probability-normalized W→FR splitting, its normalized power reaction, and Gaussian mean/covariance formulas. The present use is a fibrewise application to the fixed-entire-marginal problem, with the measurable-kernel, finite-relative-moment and singular-input guarantees proved below. It is not a new splitting method. Their inspected v3 analysis assumes regular initial densities; we do not import a general PDE existence result from it. Source versions and exact reading boundaries are recorded separately.

Local ancestry is equally explicit. The copied fixed-marginal-correction report §5 already owns the stricter field class and its per-fibre gradient identity; its §7 supplies an exact scalar Gaussian continuous comparator. The copied conditional-entropy report §5 owns the per-fibre-worsening counterexample and recalls that comparator. The copied gradient-discretization-fidelity report owns the distinction between genuine law updates and coordinate/raw-moment Euler, and supplies a different finite-atomic split for expected potential energy. It does not supply the entropy-dependent density power in (2). The Gaussian-source and matrix-rank reports own their stated Gaussian SHK and continuous entrance results. These mechanisms are inherited, not rediscovered here.

## 2. The diffusion step is an actual conditional law, including at singular inputs

Since A is a function of T, A commutes with T and Q=T−ATA is positive definite. The kernel in (2) is the exact Ornstein–Uhlenbeck semigroup with invariant law π_y. Its output has the jointly Borel, strictly positive, finite Lebesgue density

    d_y(z)=∫ϕ_Q(z−g(y)−A(x−g(y))) r_y(dx).               (4)

It is bounded by the maximum of ϕ_Q and is smooth in z. Integrating (4) in z gives one for every y on which r_y is a probability kernel. Defining any versions on a ν-null exceptional set does not affect the joint law. There is no motion, reweighting, or approximation of the observed coordinate.

Convexity of relative entropy under mixtures, applied to the Gaussian transition kernels, gives the finite bound

    KL(D_h r_y||π_y)
      ≤ c_h + ½∫(x−g(y))ᵀ A T⁻¹ A (x−g(y)) r_y(dx),
    c_h=½[−tr(A²)−log det(I−A²)].                         (5)

Indeed the KL of N(g+A(x−g),Q) relative to N(g,T) is exactly the right integrand plus c_h, by the Gaussian KL formula. Convexity follows also by retaining the input x as a latent variable and applying KL data processing to its removal. Hence

    E(D_h μ)≤c_h+½||A||² M(μ)<∞.                         (6)

This proves finite entropy at the smoothed law without assigning any finite KL, score, Fisher action, or ordinary density to a singular input. The second relative moment after D_h is finite directly:

    M(D_h μ)≤||A||² M(μ)+tr(T⁻¹Q).

OU entropy contraction is classical. For smooth positive densities the entropy identity H'=-I and Gaussian LSI H≤λ_max(T)I/2 yield

    KL(D_h r||π_y)≤e^(−2h/λ_max(T)) KL(r||π_y).           (7)

It extends to every finite-entropy input by entropy-preserving density approximation, semigroup continuity, and lower semicontinuity of KL. Finite KL relative to a Gaussian supplies the relative second moment by (11) below. Alternatively, entropy monotonicity without a rate follows directly from data processing because D_hπ_y=π_y. The bound has no dependence on g(y), so it integrates in ν.

## 3. The centred reaction: normalization, support, and entropy

The following elementary lemma applies to any probability π and density f≥0 with ∫f dπ=1. For 0<a<1, Hölder gives

    0<Z(a)=∫f^a dπ≤(∫f dπ)^a(∫1 dπ)^(1−a)=1.           (8)

Thus R_a has density f^a/Z(a). Powers and parameter integrals are Borel, proving measurability of the reaction kernel in y. Applied after (4), the output remains strictly positive. No lower bound uniform in y on Z_y is assumed or needed.

For ψ(a)=log Z(a), differentiation is justified on every compact subinterval of (0,1): for any fixed derivative order j, x^a|log x|^j is bounded by a constant times 1+x uniformly on that subinterval. With 0^a log^j0 interpreted as zero, this covers zeros of f. Consequently

    H(R_a)=aψ'(a)−ψ(a),
    dH(R_a)/da=aψ''(a)=a Var_(R_a)(log f)≥0.             (9)

If H(f)<∞, dominated convergence separately on f≥1 and f<1 gives Z(a)→1 and ∫f^a log f→∫f log f as a↑1. Hence H(R_a)≤H(f). If H(f)=∞ the inequality in extended reals is automatic; H(R_a) itself is finite for every interior a. No variance differentiability at a=1 is asserted from finite KL alone.

Using a=e^(−t), direct differentiation for t>0 gives

    ∂_t R_t = −R_t[log(dR_t/dπ)−KL(R_t||π)].             (10)

The powers and normalizers also give R_sR_t=R_(s+t). Thus (2) is an exact centred-reaction subflow, not an explicit Euler reaction step. For a finite-entropy initial density its trace at t=0 follows by dominated convergence; no endpoint action statement is needed.

Pure reaction preserves the density's support for every finite t. For example, f=1_B/π(B), 0<π(B)<1, is fixed by every R_t although its KL is positive. It cannot turn a singular probability into an absolutely continuous law merely by writing a density power. The OU-first ordering supplies full support and a valid density before reaction. For a strictly positive density, equality in the finite-time reaction entropy comparison forces f=1 π-almost everywhere. None of these facts identifies a supplied target with empirical truth.

## 4. Iteration, and why small conditional normalizers cause no gap

It is insufficient to estimate the reaction's second moment by a numerator divided by Z_y and then assume 1/Z_y is ν-integrable. Instead use the entropy variational inequality. With u=z−g(y) and any 0<θ<1/2, the Gaussian exponential moment is

    ∫exp(θuᵀT⁻¹u)dπ_y=(1−2θ)^(−m/2).

Apply the variational inequality first to bounded truncations of θuᵀT⁻¹u and then monotone convergence. It proves

    ∫uᵀT⁻¹u dr_y
      ≤ [KL(r_y||π_y)−(m/2)log(1−2θ)]/θ,
    M(μ)≤4E(μ)+2m log2                         at θ=1/4. (11)

Equations (6), (9), and (11) close induction: D_h turns a finite-relative-moment input into finite integrated entropy, R_h does not increase that entropy, and finite entropy supplies a finite relative moment for the next step. Every finite iteration is therefore defined on entire probability laws. In fact M(μₙ)≤4E₁+2m log2 for all n≥1.

Combining (7) and (9) proves (3) pointwise and after integration. The first finite value satisfies the explicit upper bound E₁≤c_h+||A||²M₀/2. The chain rule for disintegrations gives Eₙ=KL(μₙ||π). Hence Pinsker's inequality, in the convention TV(P,Q)=sup_B|P(B)−Q(B)|, gives TV(μₙ,π)≤sqrt(Eₙ/2)→0. This convergence is that of the discrete correction as the number of fixed steps increases; it is not a convergence theorem to a continuous PDE as h↓0.

If the supplied full target instead is η(dy)π_y(dz) with η≠ν, the algorithm still preserves ν and reaches ν(dy)π_y(dz). Whenever the usual absolute-continuity/finite-KL conditions hold, the original full KL retains the residual KL(ν||η). The full target is reached only if its observed marginal already matches ν. The target conditionals and g are supplied inputs; their correctness is not learned from this procedure.

## 5. A bounded singular-endpoint check

The discrete map is compatible with the original singular law in the weak topology as its single step shrinks. For any finite-entropy density f and its reaction R_a, Jensen under f dπ gives

    −(1−a)H(f)≤log Z(a)≤0,
    KL(f dπ||R_a)=(1−a)H(f)+log Z(a)≤(1−a)H(f).         (12)

Apply this on every fibre to D_h μ₀ and integrate. By (6),

    KL(D_h μ₀||Φ_h μ₀)
       ≤(1−e^(−h))[c_h+½||A||²M₀]→0.                   (13)

Here c_h=(m/2)log(1/h)+O(1) as h↓0, so the prefactor makes the bound tend to zero. The two stages are therefore close in total variation. Meanwhile the direct OU coupling, with Y unchanged, satisfies

    E|Z_h−Z|²
      ≤||A−I||²∫|Z−g(Y)|²dμ₀+tr Q→0.

Thus D_h μ₀ converges weakly to μ₀ on R^(k+m), and (13) proves Φ_h μ₀⇒μ₀. This does not imply total-variation convergence to a singular input: an initially conditionally singular law and the smoothed law can remain mutually singular. Nor does it give a finite initial KL, a continuous entrance solution, an original-time finite gradient action, or an all-law PDE uniqueness result.

## 6. What is implementable by finite Gaussian parameters

Suppose the conditional input is N(m(y),S(y)), with S(y) symmetric positive semidefinite. Write δ=m−g. The OU output is exactly Gaussian:

    δ_D=Aδ,             S_D=A S A+Q>0.

Multiplying its density and π_y to the indicated powers and completing the square gives the exact Gaussian reaction:

    P=a S_D⁻¹+(1−a)T⁻¹,
    S_+=P⁻¹,            δ_+=P⁻¹ a S_D⁻¹ δ_D,
    m_+=g+δ_+.                                             (14)

The order of these matrices matters. No commutation of S and T is assumed. These are formulas for the **whole conditional density**, justified by its Gaussian kernel and quadratic exponent, not a moment closure. Both output covariances are positive definite for every h>0, including S=0 or partial rank loss. In particular one must not invert a singular S before the diffusion stage.

The standalone implementation gaussian_step.py evaluates (14) using symmetric eigendecomposition and linear solves. In ordinary floating-point execution it approximates these exact-real parameters; it is not exact finite-bit Gaussian sampling or a numerical error certificate. It checks real/finite parameters, symmetry, definiteness and positive step. Its strict numerical symmetry and eigenvalue checks may reject mathematically valid inputs after rounding, and numerical ill-conditioning can make it raise. Exact rational fixtures in verify.py avoid matrix-exponential rounding by taking T=diag(1,2), h=log4, whence A=diag(1/4,1/2), a=1/4 and Q=diag(15/16,3/2), with a genuinely noncommuting S.

For constant S and a fixed supplied finite feature vector ψ(y), the family m(y)=g(y)+Bψ(y) stays in that same finite-parameter form: B_+=P⁻¹a S_D⁻¹AB. Thus one finite matrix update specifies every conditional in this family, for arbitrary fixed ν, g and ψ satisfying (1). Their evaluation/representation remains an input obligation. Arbitrary measurable functions m(y),S(y), or an arbitrary conditional density kernel need not possess a finite representation.

For a finite Gaussian mixture the OU stage remains a finite mixture, but applying a fractional power to its **total density** is not the same as applying (14) to each component. For example a symmetric mixture of N(±1,3/4), after a=1/2 reaction toward N(0,1), has density proportional to

    exp(−7z²/12) sqrt(cosh(4z/3)).

Componentwise reaction would instead give a density proportional to exp(−7z²/12)cosh(2z/3). These cannot differ by a constant since cosh(2x)=2cosh²x−1. No general closed finite-mixture representation, arbitrary-law finite numerical algorithm, or recovery of an arbitrary law from finitely many moments is claimed. The law-level construction and the finite Gaussian implementation are distinct conclusions.

## 7. First-order fidelity to the inherited stricter control

Fix a fibre and write r=fπ_y. On an explicit sufficient positive regularity core, take f=1+u with u∈C_c^∞, ∫u dπ_y=0, and 0<c≤f≤C. The OU semigroup acting on ratios has generator

    Lf=Δ_z f−[T⁻¹(z−g(y))]·∇_z f.

This core has a justified L¹(π_y) generator derivative. Moreover the OU output stays between c and C. Taylor expansion of the bounded logarithm/power map and its normalizer therefore gives

    (Φ_h r−r)/h → π_y Lf−r(log f−H(r)) in L¹,
      = Δ_z r+div_z(rT⁻¹(z−g(y)))−r(q−H(r)),
    q=log(r/π_y).                                           (15)

For an integrated statement impose an integrable domination of these fibrewise remainders/generator terms, or restrict to a uniformly controlled parameter family. Without it, a fibrewise derivative is not automatically an integrated derivative. Singular initial laws are not in this positive-density differentiability assertion.

Equation (15) is exactly the inherited restricted-control equation

    v_y=0,       v_z=−∇_zq,       α=−[q−H(r_y)].             (16)

Where the full smooth joint metric is defined, these fields are the negative gradient in the stricter field-representation class F. They need not minimize the ambient full-law action for their density tangent. In particular (15) is not consistency with the full orthogonally projected fixed-marginal gradient, which may use nonzero observed flux compensated by reaction. The finite-step descent established here does not require invoking that metric for an irregular ν or g.

For Gaussian positive S, differentiating the exact map (14) independently gives

    δ' = −T⁻¹δ−S T⁻¹δ,
    S' = 2I−T⁻¹S−S T⁻¹+S−S T⁻¹S.                       (17)

Substitution in the derivative of the complete Gaussian density verifies (15) exactly. Noncommuting matrix controls and a nonzero mean are included in the checker. Using both subflows for their parameter time h is standard Lie splitting for one algorithmic step h: the derivative is the sum in (15). No claim is made that Φ_h is the exact combined flow, that iterated splitting converges to a unique continuous PDE for arbitrary laws, or that a Trotter theorem applies without its additional hypotheses.

## 8. Evidence and stopping boundary

verify.py supplies exact symbolic/rational controls of Gaussian density identities, noncommuting updates, singular and partial-rank input cases, reaction composition, support obstruction, mixture countercontrol, target invariance, and first-order generators. Labelled numerical tests check the finite implementation, separate-stage entropy descent, finite-entropy bounds, and dependent conditional means. They supplement the universal proofs above rather than replace them. Input snapshots and optional original checks prevent silent predecessor edits.

The bounded local scan is recorded in DEDUP_SCAN.json. Primary-source reading and attribution are in literature/. The direct exact-splitting source rules out presenting (2) or (14) as newly discovered algorithms. This packet contributes an explicit, qualified application that resolves the specified per-fibre worsening at the discrete law level, together with a declared finite Gaussian implementation and singular-input validity proof. It does not claim field novelty, continuous all-law well-posedness, universal efficient computation, full-metric projection optimality, or T20 closure.

This is target-driven law correction, not automatic evidential assimilation or the production of independent grounds. It protects the declared observed marginal and decreases conditional KL relative to the supplied targets. It does not automatically preserve further latent provenance, identity, or other invariants not specified in the construction, and does not authenticate the target or observed marginal.
