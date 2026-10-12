# Full-law coarse-graining: exact gradient transport and a conditional-KL obstruction

11 October 2026 UTC. Additive scratch-only mathematics within ACTIVE T20. Ordinary proofs and exact symbolic controls. No protected edits, integration, formal-kernel claim, field-priority claim, empirical interpretation, or programme closure. The parent supplied the coarse-graining question and the conditional-KL/correlated-Gaussian control; this investigator supplied the coisometry criterion, quotient-norm proof, hidden spatial-mobility test, and finite-time formula. The parent and sibling's algebraic checks are participating inputs, not independent review.

## 1. Result and precise credit

For the declared unit transport/centred-reaction action on probability laws, a smooth deterministic 1-Lipschitz observation T contracts action. That is classical background. The useful transport contract is sharper:

1. A pulled-back coarse objective with first variation φ has exactly the canonical coarse gradient after pushforward if and only if its coarse spatial gradient lies in the unit-eigenvalue space of Aμ(y)=Eμ[DT DTᵀ | T=y]. For all smooth test objectives this is equivalent to DT DTᵀ=I μ-almost everywhere. Thus orthogonal projections genuinely preserve these full-law gradients, their minimal action norms, and their time-dependent flows under uniqueness hypotheses, with no independence assumption on the hidden coordinates.
2. Under a coisometric differential, every coarse tangent has an equal-minimum-norm fine lift. This is an infimum over full distributional tangents, not an equality inferred from Jensen alone. For a general given tangent, an exact norm-loss formula includes the nonminimality of its pushed field representation as well as spatial contraction and conditional variances.
3. A fixed orthogonal projection can fail completely for an objective which is not pulled back. With a product target πY⊗πZ, projecting the full KL flow gives the coarse KL flow plus the additional reaction −ν(h−νh), where h(y)=KL(μ(dz|y)||πZ). Its instantaneous vanishing is exactly constancy of h. A full product initial law supplies an invariant affirmative case.
4. In the two-dimensional Gaussian control with covariance [[1,c],[c,1]], 0<|c|<1, and standard Gaussian target, the observed marginal starts exactly at its target but has variance derivative −c². It leaves that target at every finite positive time while the standalone coarse flow remains stationary, and returns asymptotically. The exact finite-time variance is given in §7.

The new-to-the-inspected-passages content is this bounded full-law transport contract, its energy-sensitive conditional-KL obstruction, and the accompanying exact controls. It is not a discovery of HK contraction, spherical HK, Riemannian submersions, Gaussian HK geometry, entropy gradient flows, or Gaussian invariance. Nine inherited reports were inspected and copied; a bounded scan of 173 top-level RESULT.md files is recorded in DEDUP_SCAN.json. This is not an exhaustive project or literature priority search.

## 2. Tangents, admissibility, and the classical part

Let μ be a Borel probability on R^d. Put

    Hμ = L²(μ;R^d) ⊕ L²_0(μ),
    Dμ(v,α) = −div(μv)+μα,
    ||σ||²_μ = min{ ∫(|v|²+α²)dμ : Dμ(v,α)=σ }.       (1)

The last expression is defined for σ in the range of Dμ. Distributional equality is initially tested against compactly supported smooth functions. For a bounded smooth f with bounded gradient, choose cutoffs χ_R equal to one on the radius-R ball and satisfying |∇χ_R|≤C/R. Then χ_R f→f and ∇(χ_R f)→∇f in L²(μ): the main terms converge by dominated convergence, and the boundary-gradient term has norm at most C||f||∞/R. Consequently every zero-tangent field annihilates f as well as the compact tests. Bounded C¹ functions with bounded gradient follow by smooth approximation on compact sets. Thus every σ in range Dμ has a unique extension to this larger test class, independent of its representing fields. This argument applies to f=φ∘T even when T is nonproper, such as an orthogonal projection. No pushforward of a wholly arbitrary distribution is claimed. Equivalently one may define Dμ from the outset using all these bounded C¹ tests. The kernel of Dμ is closed in Hμ because every test pairing is continuous. Every nonempty affine fibre is therefore closed, and Hilbert projection gives its unique minimum-norm representative. No manifold structure on all probabilities is presumed.

For a test potential f, write

    jμ f=(∇f,f−μf),
    Kμ f=Dμ jμ f,
    Bμ(f,g)=∫∇f·∇g dμ+Covμ(f,g).                    (2)

The identity ⟨jμf,h⟩=⟨f,Dμh⟩ makes jμf orthogonal to ker Dμ, so it is the genuine minimum-norm representative of Kμf. In particular ||Kμf||²_μ=Bμ(f,f). More general unbounded potentials are allowed whenever compact cutoffs converge in the relevant L² function-and-gradient norms and the tangent pairing passes to the limit. All polynomial potentials used with Gaussian laws below have this property.

For a differentiable law functional E with first variation f, its negative gradient in this declared weak tangent geometry is −Kμf. The probability constraint makes additive constants in f irrelevant. A weak solution is

    ∂tμ = div(μ∇f)−μ(f−μf).                         (3)

When its energy chain rule is justified, E′=−Bμ(f,f). These definitions and the centred Onsager formula are classical. Kondratyev–Vorotnikov, Remark 1.1 and Definition 3.15, use the same unit/unit convention; their displayed dynamic metric is on a torus and their PDE existence results have additional assumptions. We do not import those PDE theorems to arbitrary Euclidean measures. [Primary source](https://arxiv.org/html/1809.03430v2).

Let T:R^d→R^k be smooth and 1-Lipschitz, and ν=T#μ. Conditional expectations below exist on these standard Borel spaces. For h=(v,α)∈Hμ, define

    Cμh=(v̄,ᾱ),
    v̄(y)=Eμ[DT(x)v(x)|T(x)=y],
    ᾱ(y)=Eμ[α(x)|T(x)=y].                          (4)

Then νᾱ=0 and the chain rule gives Dν Cμh=T_*Dμh. Here T_*σ is defined by testing σ against φ∘T; it is well defined independently of the representative by the bounded-test extension. The same calculation applied in space-time pushes any finite-action continuity/reaction path forward.

An exact conditional-variance expansion gives

    ||h||²_Hμ−||Cμh||²_Hν
      =∫(|v|²−|DTv|²)dμ
       +∫|DTv−v̄(Tx)|²dμ
       +∫|α−ᾱ(Tx)|²dμ.                            (5)

All three terms are nonnegative. Equality holds precisely when all vanish. Integration in time proves action contraction and hence contraction of any distance defined by infimizing this same dynamic action over admissible paths. This contraction is background, not new credit: Liero–Mielke–Savaré, Lemma 8.22, already proves 1-Lipschitz pushforward contraction for HK on separable metric spaces. [Primary source](https://link.springer.com/article/10.1007/s00222-017-0759-8). The spherical angular normalization of Laschos–Mielke is also classical; it must not be silently identified with a different scale. [Primary source](https://arxiv.org/html/1712.01888v2).

### Minimum tangent norms require an extra step

Let h* be the fine minimum representative of σ, and k* the coarse minimum representative of T_*σ. Since Cμh* and k* represent the same coarse tangent, Hilbert orthogonality gives the exact identity

    ||σ||²_μ−||T_*σ||²_ν
      = spatial loss + velocity variance + reaction variance
         +||Cμh*−k*||²_Hν,                          (6)

where the first three terms are (5) evaluated at h*. Thus action equality for a displayed representation cannot simply be declared equality of minimum tangent norms. Equation (6) identifies the extra issue exactly. Nor does equality of either kind, for an arbitrary tangent, prove commutation for a stipulated objective.

The extra term can really be positive even for an orthogonal projection. Take μ=N(0,[[1,c],[c,1]]) and the positive fine gradient potential f(y,z)=z²/2. Its fine minimum fields are v=(0,z), α=(z²−1)/2. The pushed fields are v̄=0, ᾱ=c²(y²−1)/2, with action c⁴/2. This is the full tangent of N(0,1) with variance velocity V=c². Its true minimizing fields are w=c²y/3, β=c²(y²−1)/6, with squared norm c⁴/6, as follows by direct density differentiation and Gaussian orthogonality (also the inherited Gaussian metric). Their difference has cost c⁴/3. Thus the representation and minimum losses differ by exactly that amount. The reviewing investigator supplied this illustrative control during review; its contribution is credited separately and is not independent confirmation of itself.

## 3. Exact pulled-back-gradient criterion

Let E(μ)=Ē(T#μ). At ν=T#μ suppose Ē has an admissible first variation φ. The fine first variation is φ∘T, by the functional chain rule. Define

    M(x)=DT(x)DT(x)ᵀ,
    Aμ(y)=Eμ[M(x)|T(x)=y],      0≤Aμ≤I.              (7)

The pushed negative gradient has representative

    v̄=−Aμ∇φ,       ᾱ=−(φ−νφ).                    (8)

Its tangent differs from the canonical coarse negative gradient by

    div(ν(Aμ−I)∇φ).                                (9)

**Theorem 1.** For φ∈C_c^∞(R^k), or any potential for which the same test by φ is justified, (9) vanishes as a distribution if and only if

    (I−Aμ)∇φ=0  ν-a.e.,                            (10)

and this is equivalent to

    (I−M(x))∇φ(Tx)=0  μ-a.e.                       (11)

**Proof.** If (9)=0, testing with φ gives ∫∇φᵀ(I−Aμ)∇φ dν=0. Its integrand is nonnegative, so (10) follows from positive semidefiniteness. Conversely (10) immediately makes (9) zero. Conditional expectation expresses that same nonnegative integral as ∫∇φ(Tx)ᵀ(I−M(x))∇φ(Tx)dμ; zero is equivalent to (11). QED.

There is no unnoticed divergence-free loophole: the positivity and admissible test by the objective are the ingredients eliminating it. Without contraction of T or without that testing justification, the iff is not claimed.

**Corollary 1.** At a fixed law μ, commutation for every smooth compactly supported coarse linear expectation objective ν↦νφ holds exactly when

    DT(x)DT(x)ᵀ=I_k  μ-a.e.                        (12)

Indeed (12) is sufficient. For necessity, for each positive integer R and coordinate j choose a compactly supported smooth φ equal to y_j on the ball of radius R. The zero-integral criterion forces the j-th diagonal of I−Aμ to vanish on that ball. A countable union over R,j and positivity yields Aμ=I ν-a.e. Then ∫tr(I−M)dμ=0 and positivity give M=I μ-a.e. Conversely (12) gives Aμ=I.

Consequently a smooth map commutes with all these gradients at every probability law if and only if its differential is coisometric everywhere. Necessity also follows from Dirac laws and prescribed test gradients. A coisometric map can discard whole spatial directions: equality (12) is not injectivity or recovery of the original law.

At a common state, the canonical coarse minus projected-fine energy-dissipation rate is exactly

    ∫∇φᵀ(I−Aμ)∇φ dν.                              (13)

This compares derivatives at one state. It does not compare values at equal later times. When (12) holds the fine and coarse gradient representations are both minimizing and have the same norm Bμ(φ∘T,φ∘T)=Bν(φ,φ). Thus this preservation is a verified gradient and norm statement, not merely Jensen equality.

### What a general map still needs to close

For all initial laws and all coarse test potentials, the projected tangent can be a function of ν alone precisely when M(x) is constant on each fibre of T. Necessity: apply the putative field to δ_x and δ_x′ with T(x)=T(x′)=y. Reactions vanish at a Dirac, and arbitrary gradients ∇φ(y), ∇ψ(y) identify all entries of M(x) from the derivative of the observable ψ. Sufficiency follows from (8) if M(x)=a(Tx): then Aμ(y)=a(y), ν-a.e., and the projected equation uses the declared anisotropic mobility a. This is an algebraic field-closure statement; smoothness, positivity or well-posedness of that possibly degenerate coarse geometry require separate hypotheses.

For an explicit failure, take T(x)=(2/3)sin x+(1/6)sin(2x). Its derivative is (2/3)cos x+(1/3)cos(2x), so |T′|≤1. Yet T(0)=T(π)=0 while T′(0)²=1 and T′(π)²=1/9. For a smooth coarse φ equal to y near 0, the two fine Dirac laws have the same coarse law δ_0 but projected spatial velocities −1 and −1/9. No autonomous law determined by ν alone can describe both. This is the continuous full-law counterpart of an inherited same-fibre mobility obstruction, not a new general philosophy of quotients.

## 4. A true full-tangent quotient under coisometry

Assume (12) at μ. For any coarse field k=(w,β)∈Hν define its horizontal lift

    Lμk=(DTᵀ w∘T, β∘T).                            (14)

Then CμLμk=k and ||Lμk||_Hμ=||k||_Hν, by DT DTᵀ=I μ-a.e. For every coarse tangent τ∈range Dν,

    min{||σ||²_μ : σ∈range Dμ, T_*σ=τ}=||τ||²_ν.     (15)

**Proof.** Equation (5), followed by minimization, gives ||T_*σ||_ν≤||σ||_μ for every fine tangent. Let k* be the coarse minimum representative and set σ*=Dμ Lμk*. Then T_*σ*=τ and ||σ*||_μ≤||Lμk*||_Hμ=||τ||_ν. The contraction lower bound supplies the reverse inequality. Equality holds and proves attainment. QED.

No assumption that a moment minimum also realizes a full tangent was used. Equation (15) is the least full-tangent cost among fine lifts; it does not say that every fine tangent with that image has the same norm, nor that coarse laws reconstruct their fine states, nor that intrinsic finite-family endpoint distances equal unrestricted ambient distances.

## 5. Orthogonal projection: actual continuing law, and a contraction control

Let x=(y,z), T(x)=y, with the standard product Euclidean metric. Then DT DTᵀ=I identically. Theorem 1 and (15) apply for every law, including correlated laws and singular laws. For any pulled-back objective Ē(ν), the projected fine equation is exactly its coarse negative gradient equation. Whenever the stipulated coarse equation has uniqueness in the solution class, the projected fine and coarse flows with the same starting marginal agree on their common existence interval. No general PDE uniqueness theorem is silently assumed here.

For the linear expectation objective Ē(ν)=∫φ(y)dν and a complete C¹ characteristic flow ψ_t generated by −∇φ, the identity is direct. On any interval where the weights are integrable and their normalizer is positive,

    w_t(y)=exp(−∫_0^t φ(ψ_s(y))ds),
    μ_t=(ψ_t×id)# [w_t(y)μ_0/Z_t],
    ν_t=ψ_t# [w_t(y)ν_0/Z_t].                       (16)

Thus the entire coarse continuation depends on ν_0 alone; no independence of z is required. Bounded C² φ with bounded first and second derivatives is a simple sufficient global-forward setting. More general objectives require their own existence and integrability conditions. When ψ_t is invertible, the conditional hidden law at y_t is the original conditional law at ψ_t^−1(y_t); this is transport of a hidden conditional, not its recovery from ν_t.

Deterministic contraction is weaker. Take T(x)=x/2, coarse φ(y)=y²/2, and fine initial N(2,4), so ν=N(1,1). The fine pulled-back potential is x²/8. The inherited Gaussian full-tangent formulas, or direct Gaussian differentiation, give

    (m′,v′)_projected=(−5/4,−3/2),
    (m′,v′)_canonical=(−2,−3).                       (17)

The two vectors are not collinear. No scalar change of time reconciles even their local Gaussian paths. This is a spatial-metric mismatch for the same pulled-back objective, unlike the objective mismatch in the next section.

## 6. Product-target KL: the exact hidden conditional obstruction

Let μ have a positive smooth density ρ(y,z), with ν(y)=∫ρ(y,z)dz and conditional density r(z|y)=ρ/ν. Let the fixed positive smooth target be π(y,z)=πY(y)πZ(z). Define

    ℓ(y,z)=log(ρ(y,z)/π(y,z)),
    h(y)=∫r(z|y)log(r(z|y)/πZ(z))dz.                 (18)

Assume the displayed quantities are integrable, ∫ρ|ℓ|<∞, the gradients and fluxes needed below are integrable, differentiation under the z integral is valid, and the integrated z-divergence vanishes. For the full action interpretation also require ℓ−μℓ and ∇ℓ in L²(μ). Along a smooth solution, impose these conditions locally in time. Positive Gaussian laws with a nondegenerate Gaussian product target satisfy all of them. These are stated calculation hypotheses, not a new general existence theorem.

The full KL negative-gradient equation is

    ∂tρ=div(ρ∇ℓ)−ρ(ℓ−μℓ).                          (19)

The classical KL chain rule gives

    μℓ=KL(ν||πY)+νh,
    E[ℓ|y]=log(ν/πY)+h(y).                         (20)

Also ∫ρ∇_yℓ dz=∇ν−ν∇logπY=ν∇log(ν/πY). Integrating (19) therefore gives the exact identity

    ∂tν=div_y(ν∇log(ν/πY))
         −ν[log(ν/πY)−KL(ν||πY)]
         −ν(h−νh).                                (21)

The first two terms are the canonical coarse KL flow. The final term is the exact obstruction. It vanishes if and only if h is ν-almost everywhere constant. This criterion is instantaneous; agreement on an interval requires its persistence along that full solution. A moment such as νh alone is insufficient, because the centered function h(y) controls the missing reaction.

The obstruction is not exclusive to entropy: even a linear expectation with F(y,z)=f(y)+g(z) has the additional marginal reaction −ν(E[g|y]−μg). The general issue is a full objective that is not a pullback, combined with hidden conditional variation. No contradiction with Theorem 1 is involved.

### Affirmative invariant case

If ρ_0(y,z)=ν_0(y)η_0(z) and the target is a product, take smooth solutions ν_t and η_t of the corresponding marginal KL equations. The product ρ_t=ν_tη_t satisfies (19): its score splits as log(ν_t/πY)+log(η_t/πZ), spatial fluxes split, and the centered reaction splits into the sum of the two separately centered scores. Under uniqueness in that solution class it is the full solution. Its h_t(y)=KL(η_t||πZ) is constant in y for all times, and both projections commute. This conclusion allows η_t≠πZ; initial product structure, not a hidden factor already at equilibrium, supplies the positive restriction.

## 7. Correlated Gaussian: an exact marginal failure despite global descent

Set π=N(0,I_2), ρ_0=N(0,Σ_0), and

    Σ_0=[[1,c],[c,1]],       0<|c|<1.                (22)

The first marginal is exactly πY=N(0,1). The conditional hidden law is N(cy,1−c²), so

    h(y)=[c²y²−c²−log(1−c²)]/2,
    h(y)−νh=(c²/2)(y²−1).                          (23)

The transport marginal is initially stationary, but the added reaction in (21) gives

    [d/dt ∫y²dν_t]_(0)=−(c²/2)(E[Y⁴]−E[Y²])=−c². (24)

The standalone coarse KL flow stays at πY. Hence two full states with the same observed marginal, for example c=0 and c≠0, have different future marginal derivatives under the same target and geometry. The observed marginal law alone does not determine continuation.

For an independent density-tangent check, at μ=N(m,Σ) and target N(0,I), write ξ=x−m. The centered score is

    ℓ−μℓ=mᵀξ+[ξᵀ(I−Σ⁻¹)ξ−tr(Σ−I)]/2.

Transport contributes m′=−m, Σ′=2(I−Σ); reaction contributes m′=−Σm, Σ′=Σ−Σ². Thus

    m′=−(I+Σ)m,       Σ′=2I−Σ−Σ².                  (25)

This ODE and the Gaussian reduced geometry are already classical: Liero–Mielke–Tse–Zhu, §3.4, Theorem 3.11 and equations (3.8a,b), with α=β=1 and Γ=I. We use this as an explicit control, not as a newly discovered Gaussian flow. [Primary WIAS paper](https://www.wias-berlin.de/preprint/3198/wias_preprints_3198.pdf).

For (22), the eigenvectors stay fixed and their variances b_± solve

    b′=(1−b)(b+2),       b_±(0)=1±c.

They remain positive and converge to 1. Solving (b−1)/(b+2)=e^(−3t)(b(0)−1)/(b(0)+2), and writing q=e^(−3t), gives

    Σ_t=[[a(t),c(t)],[c(t),a(t)]],
    a(t)=1−3c²q(1−q)/[9−c²(1−q)²],
    c(t)=9cq/[9−c²(1−q)²].                         (26)

The denominator is positive. Every finite t>0 has a(t)<1, while a(0)=1 and a(t)→1. This proves actual all-time noncommutation, not only a formal initial derivative. The Gaussian solution exists globally because its eigenvalues stay between their positive initial values and 1; substituting its density verifies the PDE.

The full KL derivative at t=0 is strictly negative:

    d KL(μ_t||π)/dt |_(0)
       =−[2c²/(1−c²)+c²]
       =−c²(3−c²)/(1−c²).                           (27)

The observed KL, initially zero, instead obeys

    KL(ν_t||πY)=[a(t)−1−log a(t)]/2
                 =c⁴t²/4+O(t³).                    (28)

Thus decreasing full objective does not force monotone improvement of an already-correct marginal. The first marginal KL derivative is zero at t=0, as it must be at its minimum; the variance derivative and positive second-order KL term are the appropriate controls. There is no contradiction with static KL data processing: the positive marginal KL remains bounded by the full KL.

## 8. Inheritance, evidence, and limits

The fixed-reference quadratic packet noetic-gradient-transport already owns its canonical-channel commutation iff, local quotient metric, and warning that divergence contraction is not dynamic commutation. information-geometry-transport and channel-natural-repair already own their Bregman/Fisher/data-processing comparisons. They are not replaced here. The spherical-atomic interface owns the moving-atom action and local-speed restriction; the Gaussian packet owns the local full-Gaussian-tangent calculation; both are now compared against the classical primary literature. The full-law action-tail result owns its polynomial-energy and moment bounds, which are not re-proved or enlarged here. Leafwise/Fisher and finite-audit packets already demonstrate abstract same-fibre mobility and objective-descent issues in different state and energy settings.

SOURCE_READING.json records the primary passages actually inspected. INPUT_BINDINGS.json binds the nine direct inherited reports and the parent's participating exact-control packet, including its preserved initial failed check and corrected receipt. The initial parent failure was an incorrect expected full-KL trace value, not the marginal obstruction; the corrected value is (27). Author controls here are separate from that participating check.

Run `python3 verify.py --output-dir private-locator:046fed374acdc0119f19`, optionally adding `--original-root ..` to verify original local bindings as well as snapshots. The controls check algebraic decompositions, the explicit maps, projection compatibility with Gaussian quadratic flows, the contraction example, Gaussian conditional KL, matrix dissipation, the exact finite-time solution and input identities. They supplement, and do not replace, the Hilbert minimization, distributional proofs, and the stated integrability arguments. No universal conclusion is inferred from a finite numerical test.

This packet supplies a conditional structure-preserving continuation and a sharply specified loss of that contract. It supplies no recovery of discarded hidden information, warranted objective, epistemic truth guarantee, cognitive identification, global all-laws smooth geometry, arbitrary PDE well-posedness, full-field novelty claim, protected integration, or T20 closure.
