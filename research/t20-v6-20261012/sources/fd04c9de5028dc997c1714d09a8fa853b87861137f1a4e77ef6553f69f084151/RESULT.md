# Conditional entropy control through the fixed-marginal projection

11 October 2026 UTC. Additive ordinary mathematics for ACTIVE T20. No protected edit, integration, formal-kernel proof, general PDE well-posedness, empirical-noetic warrant, historical-priority claim, or programme closure is made. The parent proposed the conditional-coercivity transfer and supplied the two Gaussian scope controls and logistic-tilt control below. The investigator checked these, derived the decomposition and non-Gaussian polynomial control, and inspected the bounded predecessor/source set. Parent participation is not independent certification.

## 1. Result and ancestry boundary

Let Y=R^k, Z=R^m, and fix the entire observed marginal ν. The supplied target is

    π(dy,dz)=ν(dy)π_y(dz).

The current law μ=ν(dy)r_y(dz) has that same marginal. Use the inherited unit transport/centred-reaction full-law tangent metric, with orthogonal observation p(y,z)=y. Put

    q=log(dμ/dπ),       E=KL(μ||π)=∫ KL(r_y||π_y)dν(y).

At an admissible positive state, let φ(y) be the inherited full marginal-compensation potential, and let

    D=∫|∇(q−φ)|²dμ+Var_μ(q−φ).

Then the projected full-law gradient obeys the exact decomposition

    D = ∫ I_z(r_y||π_y)dν
        + ∫ Var_{r_y}(q(y,·))dν
        + ∫|∇_y q−∇φ|²dμ + Var_ν(h−φ),             (1)
    h(y)=∫q(y,z)r_y(dz).

In particular, the marginal constraint cannot remove either latent Fisher dissipation or the conditional reaction variance. If, for ν-almost every y and every conditional law in the declared domain,

    KL(r||π_y) ≤ (C/2) I_z(r||π_y),     0<C<∞,       (2)

with the same C, then

    D≥2E/C.                                        (3)

Any projected-flow solution for which the energy chain rule is justified consequently satisfies

    E(t)≤exp[−2(t−s)/C] E(s),                       (4)

at finite-energy times s≤t in its existence interval. A global admissible solution therefore converges to the supplied dependent target in KL. This is an all-law functional inequality and a conditional evolution implication, not another Gaussian parameter-flow construction.

The product-target version of (2)–(4) is already explicitly present in fixed-marginal-correction/RESULT.md §5, equation (16) and the following paragraph, although that report does not call the assumption a log-Sobolev inequality. The general conditional-score multiplier is already in correlated-target-marginal-correction/RESULT.md §3. Those are inherited, not new here. The bounded addition is their combined nonproduct, non-Gaussian conditional-coercivity transfer, its exact nonnegative remainder, and explicit controls separating whole-law decay from stronger unsupported claims. Classical log-Sobolev theory and unconstrained SHK entropy decay are credited in §7.

## 2. Geometry and a concrete weak interpretation

Retain the predecessor definitions

    H_μ=L²(μ;R^{k+m})⊕L²_0(μ),
    D_μ(v,α)=−div(μv)+μα,
    j_μf=(∇f,f−μf),       K_μf=D_μj_μf,
    B_μ(f,g)=∫∇f·∇g dμ+Cov_μ(f,g).

The tangent norm is the minimum H_μ norm over representations of the entire density tangent. The inherited cutoff/quotient result says potential fields attain that minimum. Thus the actual full-tangent constrained negative gradient is

    μdot=−K_μ(q−φ∘p),
    v=−∇(q−φ),       α=−[q−φ−μ(q−φ)],
    K_νφ=p_*K_μq.                                  (5)

This is a full-law orthogonal projection. It is not deletion of the observed velocity coordinate and not Gaussian variational restriction.

Here is a sufficient instantaneous regularity contract. Assume positive smooth densities ν and π_y, a positive density μ=νr, and that q and its weak spatial gradient are in L²(μ), up to an irrelevant constant. Require the admissible-potential/cutoff hypotheses of the copied full-marginal predecessor, so that the displayed gradients, dualities and lifted potentials belong to its minimum-field closure. For the pointwise score identity below, also require differentiation under the conditional integral and vanishing latent boundary terms. These are sufficient hypotheses, not a claim of minimal regularity.

Set m(y)=E_μ[∇_y q|Y=y]. Conditional Jensen gives m∈L²(ν) and h∈L²(ν). Let W_ν be the closure of C_c^∞ in the norm ∫(|ψ|²+|∇ψ|²)dν; positive smooth ν gives the usual closable weighted gradient. Smooth cutoffs place 1 in W_ν. Riesz representation for

    a(φ,ψ)=∫(∇φ·∇ψ+φψ)dν,
    L(ψ)=∫[m·∇ψ+(h−νh)ψ]dν                       (6)

gives a unique weak φ∈W_ν. Testing by 1 gives νφ=0. It follows that (6) is precisely the weak equation K_νφ=p_*K_μq. The +φ term supplies coercivity without a Poincaré or log-Sobolev assumption on ν. Its lift lies in the fine potential-field closure by the inherited cutoff argument.

Under the additional score differentiation assumptions,

    m(y)=−E_{r_y}[∇_y log π_y(Z)],
    −div_y(ν∇φ)+νφ=−div_y(νm)+ν(h−νh).              (7)

The flux term is generally nonzero. Omitting it reuses the product-target formula outside its hypotheses and need not preserve the marginal. Formula (6) can instead be used directly without separately asserting the pointwise target-score identity.

To justify that D really is entropy dissipation, use (6) with ψ=φ and the lifted duality:

    B_μ(q,φ∘p)=B_ν(φ,φ)=B_μ(φ∘p,φ∘p).

Consequently B_μ(q,q−φ)=B_μ(q−φ,q−φ)=D. The fields in (5) have squared norm D and are the inherited minimum representation of their entire tangent. An arbitrary admissible curve on the fixed-marginal slice need not have this dissipation; the gradient choice and entropy chain rule are essential.

## 3. Proof of conditional coercivity and the evolution statement

Since φ depends only on y, ∇_z(q−φ)=∇_zq. The orthogonal product spatial metric splits the gradient norm. The law of total variance gives

    Var_μ(q−φ)=∫Var_{r_y}(q)dν+Var_ν(h−φ).

These two identities prove (1). They do not require a product target. Integrating (2) and using the KL disintegration formula gives (3). Positivity of the additional three summands is all that is used. This is why the full compensation, even when it includes observed transport, cannot erase the latent coercivity.

A slightly more general sufficient assumption is the conditional combined inequality

    I_z(r||π_y)+Var_r log(dr/dπ_y) ≥ λ KL(r||π_y)   (8)

with uniform λ>0. Equation (1) transfers (8) to D≥λE. Thus (2) is a sufficient route, not a proved necessary condition; reaction could improve coercivity for particular targets or subclasses. No equivalence between conditional LSI and full projected coercivity is claimed.

For a time-dependent theorem, assume the curve solves (5) distributionally on an interval, has the fixed marginal ν, satisfies the preceding instantaneous domain conditions almost everywhere, and has locally integrable action D. In addition assume E(t) is locally absolutely continuous and the entropy chain rule holds:

    E′(t)=∫[∇q_t·v_t+q_t α_t]dμ_t=−D(t) a.e.     (9)

Then the derivative of exp(2t/C)E(t) is nonpositive almost everywhere, which proves (4). The same proof works with the explicitly assumed differential energy inequality E′≤−D. Merely writing the distributional continuity equation does not establish (9). A weak solution without a proved chain rule or a corresponding energy-dissipation inequality is not automatically covered.

For a singular entrance with E(0)=∞, apply (4) only from a positive time s at which E(s)<∞ and the contract holds. No finite initial entropy, original-time finite endpoint action, general non-Gaussian entrance, or general-law uniqueness is manufactured. The matrix-rank predecessor supplies such positive-time admissibility for its particular Gaussian construction; this theorem does not extend its entrance existence to arbitrary laws.

If a supplied target instead has observed marginal η≠ν, with ν≪η and finite KL(ν||η), write π=η(dy)π_y(dz) and π^ν=ν(dy)π_y(dz). The classical chain rule gives KL(μ||π)=KL(ν||η)+KL(μ||π^ν). Thus the decay estimate concerns the excess conditional entropy KL(μ||π^ν), and the slice optimum is π^ν. If the coarse log-ratio g=log(dν/dη) also lies in the admissible coarse potential domain (including its L² function/gradient and cutoff requirements), its full-KL gradient is removed exactly by the same horizontal projection; then the two projected flows agree. Without this extra domain condition, the chain-rule energy statement alone does not justify identifying those gradients. This extends the predecessor's explicit product-target caveat by the same inherited argument. For example, ν=N(1,1), η=N(0,1), π_y=N(0,1), and μ=π^ν give conditional E=D=0 but total KL(μ||π)=1/2.

## 4. Genuine non-Gaussian scope, with no coarse coercivity

Classical Bakry–Émery theory gives (2) with C=1/κ whenever

    π_y(dz)=Z_y^−1 exp[−V_y(z)]dz,
    ∇²_z V_y(z)≥κ I_m uniformly in y,z,

under its standard smooth Euclidean hypotheses. Convexity is required only in latent directions. The observed marginal may lack any spectral gap or LSI. Gaussian fibres with arbitrary means and covariance T_y≤C I_m are another example; for a constant covariance T, C=λ_max(T).

For an explicit dependent, non-Gaussian target, take ν to be the standard Cauchy law and

    π_y(dz)=Z^−1 exp[−u²/2−u⁴/4]dz,
    u=z−sin y.                                     (10)

Its latent Hessian is 1+3u²≥1, so the conditional theorem gives D≥2E. The whole target cannot satisfy an ordinary joint LSI: testing a proposed joint LSI with functions of y alone would imply a Cauchy LSI, hence a Poincaré inequality, which fails. One direct failure test is f_R(y)=R f(y/R) with smooth nonzero odd f supported in [−2,2]. Its Cauchy mean is zero; its Dirichlet integral is uniformly bounded, whereas its variance grows at least linearly in R on a fixed interval of nonzero rescaled argument. Thus no joint LSI is being covertly assumed.

The target in (10) is supplied. This example proves the functional inequality's class is genuinely broader than jointly log-concave or Gaussian laws. It does not claim that every non-Gaussian state generates a globally well-posed projected PDE. Admissible current states are nonempty; μ_y(dz)=Z^−1 exp[−(z−sin y−d)²/2−(z−sin y−d)⁴/4]dz with fixed d has the needed finite polynomial score moments and bounded observed derivatives.

For a stronger exact control of the multiplier, let ν=N(0,1), V(u)=u²/2+u⁴/4, ρ(u)=Z^−1e^−V(u), target π_y(z)=ρ(z−a y), and current r_y(z)=ρ(z−b y). Let δ=b−a, e=z−b y, c=E_ρ[e²], and A=1+3c. Then Y and e are independent under μ and

    q=V(e+δy)−V(e),
    h=Aδ²y²/2+δ⁴y⁴/4,
    m=−a(Aδy+δ³y³).

With H₂=y²−1, H₄=y⁴−6y²+3, the exact centred multiplier is

    φ=(R₂/3)H₂+(R₄/5)H₄,
    R₂=Aδ²/2+3δ⁴/2−a(Aδ+3δ³),
    R₄=δ⁴/4−aδ³.                                  (11)

The weighted coarse operator has eigenvalue n+1 on H_n, proving (11). Quartic integration by parts gives E[e⁴]=1−c and E[e⁶]=4c−1. These identities suffice for exact polynomial verification of (1), (6), the zero coarse drift, and (9)'s instantaneous duality. The test does not assert that this translated-quartic family is invariant under the PDE.

## 5. Two precise scope controls

### The all-law Gaussian-fibre constant cannot be upgraded from a centred subclass

For an independent product with latent current law N(M,s) and target N(0,T), T,s>0, the multiplier is zero. Direct Gaussian integration gives

    E=½[(s+M²)/T−1+log(T/s)],
    I=M²/T²+(s−T)²/(sT²),
    V_q=Var(q)=M²s/T²+(s−T)²/(2T²),
    D=I+V_q.                                       (12)

Fix T and let M→∞, s=1/M. Then D/E→2/T. Combined with (3), the all-admissible-state constant 2/T is sharp for this product Gaussian target, even with reaction. At T=1 this blocks exporting the predecessor's stronger D≥6E from its centred two-coordinate Gaussian family to arbitrary laws. No asymptotic-in-time rate sharpness for each trajectory is inferred from a sequence of instantaneous states. The sequence escapes finite entropy sublevels.

### Whole-law decay need not mean decay on every observed fibre

Use the inherited standard product Gaussian target and current r_y=N(by,s). Its full projected flow obeys

    b′=−b(s+2+b²/3),    s′=(1−s)(s+2)+2b²,
    h(y)=½[s−1−log s+b²y²].

At b=1,s=11/10,

    h′(y)=169/2200−103y²/30.                        (13)

This is positive on an interval of positive ν-measure around zero, while ∫h′dν<0. Thus (4) is an integrated conditional-entropy estimate. It does not assert a pointwise-in-y decay estimate for the full constrained flow. The stricter fibrewise field rule has a separate conditional energy identity; the full metric permits observed flux and reaction to cancel only after the marginal equation is assembled. Equation (13) exposes exactly that distinction.

The inherited constructive alternative is v_y=0, v_z=−∇_zq, α=−(q−h(y)). Under a justified fibrewise chain rule it gives h′(y)=−I_z(r_y||π_y)−Var_{r_y}(q)≤0. In this Gaussian example its equations give h′(y)=−b²y²(1+s)−(s−1)²(1/s+1/2). Its cost is the stricter field-representation control class already analysed in the predecessor; it is not asserted to minimize the ambient full-tangent action.

## 6. Optional bounded-entropy target-uniform obstruction

The preceding sharpness sequence already rules out a target-independent constant as T varies. A separate non-Gaussian state control shows this failure need not use unbounded entropy. Let π_T=N(0,T), σ(z)=(1+e^−z)^−1, and μ_T=2σ(z)π_T(dz). Symmetry normalizes μ_T, and q=log(2σ). The independent observed marginal again gives φ=0. With g_T=(2πT)^−1/2,

    I≤g_T,
    Var_{μ_T}(q)≤4ζ(3)g_T,
    log 2−(π²/3)g_T≤E≤log 2.                        (14)

For completeness, substitute u=σ(z), dz=du/[u(1−u)]. The needed integrals are

    ∫σ(1−σ)² dz=1/2,
    ∫σ(−logσ) dz=ζ(2),
    ∫σ(logσ)² dz=2ζ(3).

The Gaussian density is at most g_T. Apply that bound to the nonnegative integrands, and use Var(q)≤E_μ[(q−log2)²]. These steps prove (14), so D→0 while E→log2 as T→∞. All states are smooth, strictly positive and have finite score moments. Both transport and reaction are controlled. This does not refute a positive bound for any fixed T, construct a single fixed target with unbounded conditional variances, or prove conditional LSI necessary. No diffusion-only countermodel is substituted for the actual metric.

## 7. Sources, checks and exclusions

Classical ancestry and bounded reading:

- Gross, *Logarithmic Sobolev Inequalities*, American Journal of Mathematics 97 (1975), 1061–1083, https://www.jstor.org/stable/2373688 . Bibliographic identification checked against Cornell's author record; the JSTOR full text was not exposed by the web tool. No assertion of a full-text reread is made.
- Bakry and Émery, *Diffusions hypercontractives*, Séminaire de probabilités XIX (1985), 177–206, https://www.numdam.org/item/SPS_1985__19__177_0/ . Original primary PDF retrieved; Proposition 5 and Corollaries 1–2, printed pp. 198–199, were read, and p. 199 visually checked. Their Γ₂≥(λ/2)Γ criterion and entropy≤I/λ normalization give λ=2κ in the Euclidean curvature case. This is classical attribution, not a present discovery.
- Mielke and Zhu, *Hellinger–Kantorovich Gradient Flows: Global Exponential Decay of Entropy Functionals*, arXiv:2501.17049v1, §3.1 Theorem 3.2 and §4.2 Theorem 4.4 / Corollary 4.6, https://arxiv.org/html/2501.17049v1 . These give the 2κ curvature normalization and the unconstrained SHK inheritance of Wasserstein coercivity. Their unit transport/unit reaction operator matches ours. The fixed-entire-marginal conditional projection is derived above, not attributed to a theorem not located there.

INPUT_BINDINGS.json preserves the exact five inspected predecessor reports. SOURCE_READING.json records reading boundaries. verify.py performs exact polynomial controls of the genuinely non-Gaussian dependent example, full projected duality and decomposition, the Gaussian sharpness and per-fibre counterexamples, and independent high-precision scalar controls of the quartic moments and logistic integrals. Numerical checks are labelled numerical; they supplement the proofs and do not prove the universal LSI, PDE existence, chain rule, or arbitrary-law sharpness limit. Run python3 verify.py --output-dir private-locator:3eb3920439375ada6738; add --original-root .. to check the originals as well as snapshots.

This is an ordinary mathematical sufficient theorem within an inherited metric. It does not discover LSI or SHK, prove all-law flow existence/uniqueness, remove the chain-rule hypotheses, infer finite entropy at a singular start, make per-fibre claims from integrated decay, supply a general necessity theorem, authenticate the target or marginal, or close T20.
