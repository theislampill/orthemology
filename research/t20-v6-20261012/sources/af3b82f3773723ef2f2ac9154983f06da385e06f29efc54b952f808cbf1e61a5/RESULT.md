# Damped atom escape: transport finite-rank boundary test

## Finding and scope

The proposed example is valid. Smooth polynomial transport and killing can admit a global positive measure-valued solution with every moment finite and C∞ on all real times, uniformly bounded Hankel rank, and an actual rank loss from two to one at a finite time. Ordinary measure tightness and uniform integrability of every fixed moment do not rule this out. Nonexplosion of atom trajectories, or appropriate control of their locations and survival weights, is a materially stronger requirement.

This is a boundary test for extending a killing-only finite-rank theorem, not a counterexample to that theorem. It also falsifies a literal standalone reading of the constant-rank assertion under only the displayed hypotheses of arXiv:2211.04416v3 Theorem 4.2, when evolution includes distributional measure solutions with the stated smooth moments. It does not challenge the bounded smooth hypotheses of Lemma 4.1. The damped-escape example alone does not refute uniqueness; the separately identified time-reversed corollary below does exhibit nonuniqueness in an unrestricted distributional/moment solution class. The source itself explains why unbounded transport can explode: its Example 4.5 supplies the very characteristic used here. The added reaction hides that escape from moment smoothness and finiteness.

## Exact construction

For t<1 set

x(t) = 1/(1−t),
c(t) = exp((1−(1−t)^(−3))/3),
μ_t = δ_0 + c(t)δ_{x(t)}.

For t≥1 set μ_t=δ_0. In particular μ_0=δ_0+δ_1. These are finite positive Borel measures for every real t. On t<1,

x′=x², c′=−x⁴c, c=exp((1−x³)/3)>0.

Choose g(x)=x² and h(x)=−x⁴−2x. In the source's non-divergence convention,

∂_t μ = −g ∂_x μ + h μ = −∂_x(x²μ) − x⁴μ.

The distinction is essential: the dual reaction is h+g′=−x⁴, not h alone. The coefficients are polynomial and smooth, but not globally bounded.

## Distributional PDE, including the escape time

For any spatial test function φ∈C_c∞(R) and t<1,

d/dt ⟨φ,μ_t⟩ = c[x²φ′(x)−x⁴φ(x)]
                 = ⟨x²φ′−x⁴φ,μ_t⟩.

The stationary atom contributes zero because both x² and x⁴ vanish at zero. For a compact spatial support, the moving atom eventually leaves it as t approaches 1 from below. Consequently its test pairing is identically zero in a left neighborhood of 1; this glues smoothly to the zero moving component after 1. No distribution supported at t=1 appears. Equivalently, for every ψ∈C_c∞(R_t×R_x),

∫_R ⟨∂_tψ + x²∂_xψ − x⁴ψ, μ_t⟩ dt = 0.

All integrals exist: compact time intervals have uniformly bounded mass, and the test function's spatial support is compact. This proves the PDE on all real times, not merely before explosion. The path is weakly continuous through t=1, and even converges to δ_0 in total variation there since c(t)→0. No claim of total-variation differentiability of moving Dirac measures away from t=1 is made.

## All moments and their smooth gluing

For every integer n≥0,

m_n(t)=1_{n=0}+c(t)x(t)^n   (t<1),
m_n(t)=1_{n=0}             (t≥1).

Every derivative of c x^n on t<1 is c P(x) for a polynomial P: differentiation sends P to x²P′−x⁴P. Since exp(−x³/3) times any polynomial tends to zero as x→+∞, every such derivative tends to zero at t=1. Extension by zero is C∞ and flat there. Thus all m_n are finite C∞ functions on R. They are not analytic across t=1.

The exact hierarchy on all real times is

m_n′ = n m_{n+1} − m_{n+4}, n≥0.

For n=0 the first term is zero. At t=1 and later both sides vanish. Polynomial test functions are legitimate here by the explicit moment formulas; the claim is stronger than just the compactly supported distributional identity.

## Hankel rank

For t<1, the moment matrix is the sum of the two rank-one forms from atoms 0 and x(t). Its leading 2×2 determinant is

m_0m_2−m_1² = c x² > 0.

Hence the infinite Hankel rank is exactly two. The polynomial z(z−x(t)) vanishes on both atoms, giving the matching rank upper bound. For t≥1 the sequence is (1,0,0,…) and the Hankel rank is one. In particular the rank is uniformly bounded by two, even on any neighborhood spanning the escape time. All finite principal Hankel truncations of order at least one have the same 2→1 rank loss.

## Normalized probability variant

Let ν_t=μ_t/m_0(t) and q_n=∫z^n dν_t. For t<1,

ν_t = [δ_0+cδ_x]/(1+c), q_0=1,
q_n = c x^n/(1+c) for n≥1.

For t≥1, ν_t=δ_0. The denominator is at least one and is C∞, so all normalized moments are C∞. Direct differentiation gives, on all real times,

q_n′ = n q_{n+1} − q_{n+4} + q_4 q_n.

In divergence form the normalized equation is

∂_tν = −∂_x(x²ν) − (x⁴−q_4(t))ν.

In the source's non-divergence convention its reaction coefficient is −x⁴−2x+q_4(t). This is a nonlinear transport/selection evolution because q_4 depends on the evolving law; it is not the same linear equation as for μ. Its Hankel determinant is c x²/(1+c)²>0 before 1, and its rank again drops from two to one.

## Tightness does not detect the lost atom

Indeed x ranges over (0,∞) as t ranges over (−∞,1), and c=exp((1−x³)/3). For each n≥0,

sup_t ∫_{|z|>R}|z|^n dμ_t(z)
  ≤ exp(1/3) sup_{y>R} y^n exp(−y³/3) → 0 as R→∞.

Thus the entire real-time family is uniformly tight (n=0) and has uniformly integrable moments of every fixed order. The same is true for ν because its denominator is ≥1. Nevertheless the union of atom locations near t=1 is unbounded, and the positive moving weight tends to zero. Do not describe ordinary tightness as a sufficient repair. Uniform boundedness of the actual support near an interior time, together with appropriate coefficient regularity and characteristic uniqueness, is a different condition.

## Strong tail bounds and snapshot determinacy

For every fixed a>0, the positive exponential moment is uniformly bounded over all real times, because

∫ exp(a|z|) dμ_t = 1 + exp(1/3) exp(−x³/3+a x)  (t<1),

and the exponent has a finite maximum on x>0. More strongly, for every 0<b<1/3,

∫ exp(b|z|³) dμ_t = 1 + exp(1/3) exp(−(1/3−b)x³) ≤ 1+exp(1/3).

Both expectations tend to 1 as t↑1 and agree with 1 afterward. The normalized expectations have the same continuity and uniform boundedness, by division by 1+c. These bounds do not imply nonexplosion of individual atom locations. Every snapshot remains a determinate, genuine finite-atomic law; there is no failure of moment determinacy or law validity here.

## Concrete noninjectivity statement

For the fixed linear polynomial PDE above, every initial measure δ_0+aδ_1, a>0, has the exhibited evolution δ_0+a c(t)δ_{x(t)} before 1 and δ_0 afterward. Distinct initial measures therefore have the same later measure and moment sequence under this explicit propagation.

For normalized probability laws, initial data wδ_0+(1−w)δ_1, 0<w<1, evolve under the same nonlinear normalized rule to

[wδ_0+(1−w)c(t)δ_{x(t)}]/[w+(1−w)c(t)]

before 1 and to δ_0 afterward. Each has smooth finite moments and rank ≤2. These distinct earlier numerical laws cannot be recovered from the later law alone. For the *unnormalized* linear equation, starting instead at wδ_0+(1−w)δ_1 ends at wδ_0, not δ_0; normalization must not be silently omitted.

This is noninjectivity of the specified propagation, not two different forward solutions with the same initial data. No uniqueness refutation is established or needed by this forward construction. It is a mathematical information-loss claim only, with no interpretation as physical or noetic bearer identity.

## Separate time-reversed corollary: inflow from infinity

The damped-escape example by itself only proves noninjectivity. Reversing its mechanism gives a distinct and explicit nonuniqueness test under *different* polynomial coefficients. Set μ̃_t=δ_0 for t≤0, and for t>0 let

x̃(t)=1/t, c̃(t)=exp(−1/(3t³)),
μ̃_t=δ_0+c̃(t)δ_{x̃(t)}.

Then x̃′=−x̃² and c̃′=x̃⁴c̃. Choose g̃(z)=−z² and h̃(z)=z⁴+2z, so h̃+g̃′=z⁴. Exactly the same compact-test gluing argument shows

∂_tμ̃ = −∂_z(−z²μ̃)+z⁴μ̃

on all real times, including 0. Its moment hierarchy is

m̃_n′ = −n m̃_{n+1}+m̃_{n+4}.

Every moving moment c̃ x̃^n is C∞ and flat at t=0. The stationary path μ̂_t=δ_0 is another solution of the same PDE with the same initial measure μ̃_0=δ_0, the same initial moments, and the same full initial time jet of every moment. Yet μ̃_t has rank two at every t>0, whereas μ̂_t has rank one always. Initial-law determinacy is not in question: δ_0 is uniquely represented by its moment sequence. The extra atom enters from spatial infinity, which the unrestricted compact-test and smooth-moment conditions permit.

Normalization gives ν̃_t=μ̃_t/(1+c̃(t)), and its hierarchy is

q̃_n′ = −n q̃_{n+1}+q̃_{n+4}−q̃_4q̃_n.

Both ν̃ and the stationary δ_0 path solve this same nonlinear normalized hierarchy and normalized PDE, with the same initial probability law and initial moment jets. Fixed positive exponential moments and subcritical cubic-exponential moments are uniformly bounded and continuous across 0, by the same exp(−x³/3) bounds.

Thus the reverse-time variant genuinely disproves forward uniqueness in the broad distributional/positive smooth-moment class for these unbounded coefficients, unless an additional no-inflow/nonexplosion or solution-selection condition is imposed. It does not assert nonuniqueness of an already selected characteristic semigroup, does not apply to bounded-smooth Lemma 4.1, and does not apply to a pure-killing hierarchy. This is a separate result from the original damped-escape example's information-loss statement.

## Relationship to killing-only arguments

The transport contribution n m_{n+1} (or n q_{n+1}) is genuinely present. The example therefore does not satisfy a pure-killing hierarchy. Under pure killing, atoms stay at fixed finite positions and finite locally integrable rates cannot annihilate a positive atom in finite time. Here the integrated killing along the escaping characteristic diverges as t↑1, even though the coefficient is smooth at every finite spatial point. Smoothness of all moment coordinates and a locally uniform finite rank bound do not prevent this transport-specific mechanism.

## Source reading and attribution boundaries

Inherited before this task: the source-comparison record already noted the displayed continuity/uniqueness mismatch in Theorem 4.2 and the stronger hypotheses of Lemma 4.1. This task did not discover that caveat anew.

New checks in this task: continuously read the supplied text of printed pp.21–23, and rendered/read PDF images of all three pages. Page 21 explicitly places Lemma 4.1 in the bounded-smooth setting and supplies the h+div g weight. Page 22 displays only continuity for g,h in Theorem 4.2 and invokes trajectory uniqueness in its proof. Page 23 explicitly discusses extending beyond bounded smooth coefficients and Example 4.5 uses x′=x², x(0)=1, x(t)=(1−t)^(−1), explaining finite-time escape and the need for boundedness. Credit the escape mechanism to that example. The new discriminator tested here is the damping c(t), which keeps *all* moments C∞ and finite through the same escape while rank drops.

Primary source: Curto–di Dio–Korda–Magron, arXiv:2211.04416v3, https://arxiv.org/pdf/2211.04416v3, printed pp.21–23. Source PDF read from the existing source-comparison directory; SHA-256 a01ce0c1b9d2f5cbdf6f55c655d03ddeb70179b29549f7fba5bc0f43f729be78. No new broad literature search, author contact, whole-paper audit, or protected artifact update was performed.

The proof above is a direct independent verification of the root-proposed explicit construction. It does not import Theorem 4.2 as a theorem. It does not establish novelty in the literature.

## Reproducible controls

`check_exact.py` uses SymPy exact arithmetic/algebra to verify x′, c′, the source dual reaction, the general symbolic moving-moment identity, moment hierarchies for n=0,…,12, rank minors, and the derivative polynomial recursion. All checks passed; see `EXACT_CHECKS.json`. These finite checks supplement, rather than replace, the all-n induction and distributional proof above. PDF page images are in `source-checks/`.
