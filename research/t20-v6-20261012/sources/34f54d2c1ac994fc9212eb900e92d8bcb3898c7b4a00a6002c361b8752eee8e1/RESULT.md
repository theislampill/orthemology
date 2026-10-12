# Fixed-marginal KL correction in the full transport–reaction tangent metric

11 October 2026 UTC. Additive ordinary mathematics within ACTIVE T20. This packet preserves the accepted inputs. It makes no protected edit, integration, formal-kernel, empirical-noetic, field-priority, or programme-closure claim. The parent supplied the constrained-correction question and proposed subtracting the horizontal lift; the investigator derived and checked the formulas, proofs, exact controls and scope below. The parent separately supplied the global Gaussian barrier and checked the initial dissipation comparison. During review, the reviewing investigator supplied the stronger Gaussian entropy bound below; it is a participating addition, not independent certification of itself. These contributions are credited rather than treated as independent review.

## 1. Constructive result

Fix a probability marginal ν on Y and a positive target πZ on Z. The target on the product is the stipulated law π=ν⊗πZ. For a fine law μ with Y-marginal ν, use the same unit transport/centred-reaction metric as the accepted full-law coarse-graining packet.

The full minimum-action constrained gradient of KL(μ||π) is

    μdot = −Kμ(ℓ−φ∘T),      ℓ=log(dμ/dπ),
    Kνφ = T_*Kμℓ,           T(y,z)=y.                  (1)

This is an orthogonal projection of the genuine full-law tangent gradient. It is not deletion of the y coordinates. For smooth positive densities μ(dy,dz)=ν(y)r(z|y)dy dz, put h(y)=KL(r(·|y)||πZ). The centred multiplier is the weak solution

    [−ν⁻¹div_y(ν∇_y)+I]φ = h−νh,       νφ=0.          (2)

The zeroth-order term makes the weak problem coercive; no spectral-gap hypothesis on ν is needed for this solve. Subject to the stated chain-rule and existence assumptions, the flow preserves the entire specified marginal, decreases the full conditional KL, and has the exact constrained steepest-descent and minimum-action properties proved below.

A globally defined exact Gaussian construction makes this affirmative rather than merely formal. Starting from covariance [[1,c],[c,1]], 0<|c|<1, target I, the corrected flow stays Gaussian with covariance [[1,b],[b,a]], retains the y-marginal N(0,1) exactly, and converges to I. Its covariance is specified by the exact autonomous ODE

    s=a−b²,
    b′=−b(s+2+b²/3),       s′=(1−s)(s+2)+2b²,          (3)
    b(0)=c,                s(0)=1−c².

This is an exact ODE-defined solution verified against the full density PDE, not an asserted elementary closed form or a moment-only approximation. A closed-form fibrewise comparator is given in §7.

## 2. Declared geometry and inherited material

For a probability μ on R^d, let

    Hμ=L²(μ;R^d)⊕L²_0(μ),
    Dμ(v,α)=−div(μv)+μα,
    ||σ||²_μ=min{||u||²_Hμ : Dμu=σ},
    jμf=(∇f,f−μf),     Kμf=Dμjμf,
    Bμ(f,g)=∫∇f·∇g dμ+Covμ(f,g).                    (4)

All tangent statements are in the Hilbert quotient Hμ/ker Dμ, identified with range Dμ equipped with this norm. The kernel is closed because distributional test pairings are continuous; the minimum therefore exists for every represented tangent. Admissible potentials satisfy the L² function/gradient and cutoff conditions needed to pair with Dμ. Then jμf is orthogonal to ker Dμ, and is the unique minimum representative of Kμf. In particular ||Kμf||²_μ=Bμ(f,f).

The accepted full-law-coarse-graining-20261011/RESULT.md, §§2–4, proves the bounded-test extension, nonproper-projection cutoff argument, tangent contraction, and coisometric quotient. We use those results. Unbounded potentials below are understood by completion or by explicit cutoffs; positive Gaussian polynomial potentials satisfy the conditions by Gaussian tails.

The comparison is deliberately bounded. The four inspected reports are copied and hash-bound in INPUT_BINDINGS.json:

- full-law-coarse-graining owns the full tangent quotient, exact pulled-back-gradient transport, the conditional-KL marginal obstruction, and the unconstrained correlated-Gaussian control.
- noetic-gradient-transport owns its fixed-reference quadratic quotient metric and minimum-energy lifts; it already credits classical constrained Riemannian projection.
- leafwise-noetic-geometry owns evolving-Fisher moment obstructions and fixed exponential-leaf remedies. Its fixed log-density class is not the fixed entire marginal used here.
- gaussian-correction-geometry owns its full-Gaussian-tangent minimization and quadratic density-tangency proof. The subsequently inspected primary literature already contains Gaussian SHK geometry and the unconstrained Gaussian KL ODE.

The bounded addition is the actual fixed-marginal full-law correction, a solvable horizontal compensation equation, and an invariant globally convergent correlated-Gaussian construction with explicit action comparisons. It is not discovery of Riemannian projection, Gaussian invariance, SHK, or conditional entropy.

## 3. Full constrained gradient and the two minimum-action meanings

For a smooth coisometric observation T, let ν=T#μ and let R=T_* be the bounded tangent pushforward. The accepted quotient theorem says R is a coisometry: its adjoint R* is an isometric right inverse, RR*=I. In the potential class,

    R* Kνψ = Kμ(ψ∘T).                                 (5)

Indeed for every fine tangent σ, admissible duality gives

    ⟨Kμ(ψ∘T),σ⟩_μ = ⟨ψ,Rσ⟩
                       = ⟨Kνψ,Rσ⟩_ν.

The same identity extends from admissible coarse potentials to their tangent-norm completion. Alternatively, the adjoint is induced by the isometric horizontal lift of the coarse minimum field; the accepted quotient proof shows that lift is itself a fine minimum field.

Let E have admissible first variation ℓ and let G=Kμℓ. The vertical tangent subspace V=ker R is closed. Its orthogonal projection is P=I−R*R. Thus

    Gc=PG=G−R*RG                                        (6)

is the constrained positive gradient, and −Gc is the unique minimizer of

    σ ↦ ½||σ||²_μ + dEμ[σ],       subject to Rσ=0.       (7)

Proof: for σ∈V, dEμ[σ]=⟨G,σ⟩=⟨Gc,σ⟩, so (7) equals ½||σ+Gc||²−½||Gc||². This proves full tangent minimality, not merely minimality among chosen Gaussian fields or chosen coordinate controls.

If an admissible (possibly weak/completed) φ solves Kνφ=RG, (5) gives (1). Solvability in a smooth potential class is an additional issue; it is not inferred just from writing an inverse. Section 4 proves weak solvability for the fixed-marginal KL case, and §6 gives an explicit quadratic solution.

There are two related but distinct action statements:

1. To cancel the marginal drift of the unconstrained negative gradient −G, choose a correction δ with Rδ=RG. The unique minimum-norm correction is δ*=R*RG. Every other correction has δ=δ*+v, v∈V, and

       ||δ||²=||δ*||²+||v||².

2. For a prescribed instantaneous decrease d>0, minimizing ||σ||² over vertical tangents with dEμ[σ]=−d gives

       σ*=−d Gc/||Gc||²,     min action=d²/||Gc||²,     (8)

   provided Gc≠0. This is Cauchy–Schwarz with its equality case. If Gc=0, no vertical tangent achieves a positive first-order decrease. Without a prescribed decrease or the linear term in (7), the minimum-norm vertical tangent is simply zero.

Under the energy chain rule, along μdot=−Gc,

    E′=−Dc,
    Dc=||Gc||²=Bμ(ℓ,ℓ)−||RG||²_ν
                  =Bμ(ℓ,ℓ)−Bν(φ,φ).                (9)

These are instantaneous metric/action identities. They do not order energy values at equal later times for different flows or establish a globally least-action endpoint path.

## 4. Fixed marginal: coercive solve and actual invariant

Assume ν and πZ have positive smooth densities, μ=νr has positive smooth density, and q=log(r/πZ)=ℓ has the function/gradient integrability, differentiation-under-integral, vanishing z-boundary flux, and cutoff properties needed in the accepted KL calculation. In particular q modulo constants and ∇q belong to L²(μ). Put h(y)=∫r q dz. Conditional Jensen gives h∈L²(ν), modulo the same constant gauge.

Since ∫r dz=1,

    Eμ[∇_y q|Y=y]=0,
    T_*Kμq = ν(h−νh).                                  (10)

The second identity includes the distributional divergence and reaction. The first rules out a hidden marginal transport contribution at a fixed correct marginal; the full unconstrained marginal drift is instead −ν(h−νh).

Here is a concrete weak interpretation of (2). Let Wν be the closure of compactly supported smooth functions in the norm ∫(ψ²+|∇ψ|²)dν, with the usual closable weighted gradient for a positive smooth ν. Smooth cutoffs show that 1∈Wν. On Wν use

    a(φ,ψ)=∫(∇φ·∇ψ+φψ)dν,
    L(ψ)=∫(h−νh)ψ dν.

The Hilbert-space Riesz theorem gives a unique φ∈Wν with a(φ,ψ)=L(ψ) for all ψ∈Wν. Testing by 1 yields νφ=0. Hence a=Bν on this solution against arbitrary tests, and it solves Kνφ=ν(h−νh). Testing by φ and applying Cauchy–Schwarz gives

    Bν(φ,φ) ≤ Varν(h).                                 (11)

No Poincaré inequality is needed: the +φ term controls the L² norm. Lift φ by approximation with coarse smooth tests; the accepted nonproper-projection cutoff argument and the isometry give jμ(φ∘T) in the fine minimum-field closure. Thus the weak gradient is well defined. This does not claim classical regularity or full nonlinear PDE well-posedness.

For a sufficiently regular time-dependent solution of (1) on the slice, Rμdot=0. Consequently ∂t(T#μt)=0 in distributions, and testing in time shows T#μt=ν throughout its existence interval. This preserves the full law ν, not just its first moments.

Here “correct marginal” means equal to the declared target marginal, not independently authenticated reality. If one instead freezes an arbitrary ν against πY⊗πZ, the KL chain rule leaves the constant residual KL(ν||πY). The coarse log-ratio g=log(ν/πY) adds g−νg to the multiplier, so the constrained conditional correction is unchanged. Its conditional optimum is ν⊗πZ, which reaches the original full target only if ν=πY. This is an inherited KL-chain-rule consequence, not a new warrant theorem.

The minimizing fields generally do not fix individual y positions or make their conditional reaction zero. They are

    v=−∇q+∇(φ∘T),
    α=−(q−μq)+(φ∘T−νφ).

Their pushed fields are

    vbar=∇φ,     αbar=−(h−νh)+φ.                      (12)

These need not vanish separately. Their coarse transport and reaction cancel because −div(ν∇φ)+νφ=ν(h−νh). This cancellation is exactly the freedom lost by separately setting both coarse field components to zero.

If μ=ν⊗η, then h is constant, φ=0, and q depends only on z. A smooth hidden-coordinate KL solution ηt therefore gives the product solution ν⊗ηt. Under uniqueness in that solution class, this is an invariant product subclass. No justification of the stipulated target or marginal follows from its invariance.

## 5. The fibrewise control restriction, and conditional convergence

A simpler valid control rule is

    vy=0,        vz=−∇z q,        α=−(q−h(y)).           (13)

It preserves ν because E[α|Y]=0 and the z-divergence integrates to zero. The resulting equation is a unit SHK KL equation for each conditional r(·|y), with y treated as a parameter.

This is the negative gradient for a stricter **field-representation control class**

    F={ (v,α) : vy=0 and E[α|Y]=0 } ⊂ Hμ,

with its L² control action. It is not automatically a smaller set of attainable density tangents: in regular classes the same vertical tangent can admit a fibrewise representation, usually at a different cost. Nor does (13) generally minimize the ambient full-law action for its own density tangent. The displayed field is the projection of −jμq onto F and is minimum among F-representations of its tangent, because it is orthogonal to F∩ker Dμ.

Let Vfield=ker(RDμ), which contains ker Dμ, and let P_Vfield and P_F be its and F's orthogonal projections. Then F⊂Vfield and P_Vfield jμq=jμ(q−φ∘T). Pythagoras gives

    Du ≥ Dc ≥ Df,
    Du=Bμ(q,q),
    Df=∫|∇z q|²dμ+∫Var(q|Y=y)dν(y),
    Dc−Df=||P_Vfield jμq−P_F jμq||²_Hμ.                (14)

Thus at a common state the unrestricted constrained metric gives at least as much KL decrease per gradient clock as the restricted-control rule; for a prescribed decrease d, (8) costs d²/Dc instead of d²/Df in the respective action classes. These comparisons do not silently identify the fibrewise field action with its possibly lower ambient tangent norm.

More explicitly, using (10),

    Du−Df=∫|∇y q|²dμ+Varν(h),
    Dc−Df=∫|∇y q|²dμ+Varν(h)−Bν(φ,φ)≥0.              (15)

The full constrained dissipation can vanish only at the product target within this positive-density class. Indeed Dc=0 implies Df=0, so Var(q|Y=y)=0 for ν-a.e. y. Then q is constant in z for that conditional; strict positivity and normalization force r(·|y)=πZ. Conversely μ=ν⊗πZ is stationary.

A bounded general convergence implication is also available. **Assume** πZ satisfies

    KL(r||πZ) ≤ (1/(2κ)) ∫r|∇z log(r/πZ)|² dz          (16)

for the conditional densities under consideration, with the same κ>0. Integrating in ν and using (14) gives Dc≥Df≥2κE. Any global admissible constrained solution satisfying the energy chain rule therefore has E(t)≤E(0)e^(−2κt); the same implication holds for the fibrewise control equation. This is a direct consequence of the explicitly assumed inequality, not an existence theorem or a claim that every target satisfies it. The Gaussian construction below establishes global existence and convergence without importing a general nonlinear PDE theorem.

## 6. Exact Gaussian constrained construction and global convergence

Take ν=πZ=N(0,1), μ=N(0,Σ), and

    Σ=[[1,b],[b,a]],       s=a−b²>0.

The conditional is N(by,s), giving

    h(y)=½[s−1−log s+b²y²],
    h−νh=½b²(y²−1).

For ν=N(0,1), the centred quadratic y²−1 is an eigenfunction of the operator in (2) with eigenvalue 3. Therefore

    φ(y)=b²(y²−1)/6.                                    (17)

Let A=I−Σ⁻¹, E11=diag(1,0), and B=A−(b²/3)E11. Up to its irrelevant constant, q−φ is xᵀBx/2. The negative full-law fields are −Bx and −½[xᵀBx−tr(BΣ)]. Differentiating the Gaussian density verifies exactly that their density tangent is the Gaussian tangent with

    Σ′=−(BΣ+ΣB)−ΣBΣ
       =2I−Σ−Σ²+(b²/3)(E11Σ+ΣE11+ΣE11Σ).             (18)

This is a polynomial identity of the entire density derivative. It is not inferred just from matching covariance moments. The yy entry is zero. The remaining entries give

    b′=−b(a+2−2b²/3),
    a′=2−a−a²−b²+b⁴/3,

which become (3). The Gaussian family with this fixed marginal is therefore invariant for the constructed equation. Gaussian tails justify every quadratic pairing and boundary passage on compact time intervals where s>0 and a is bounded.

For any initial b0∈R and s0>0, the ODE (3) has a unique global forward solution with s>0. Here is a direct proof. Write r=b², m=min(s0,1)>0, and

    M=max(s0, [−1+sqrt(9+8b0²)]/2).

At s=m the derivative s′=(1−m)(m+2)+2r is nonnegative. While s>0,

    r′=−2r(s+2+r/3)≤−2(m+2)r,

so 0≤r(t)≤b0²e^(−2(m+2)t)≤b0². At s=M, the defining quadratic root makes s′≤0. These barriers can be justified by first-exit comparison, or by scalar differential inequalities. Thus m≤s≤M, b is bounded, and the smooth polynomial ODE extends globally without approaching the covariance boundary.

Set w=s−1. Then

    w′=−(s+2)w+2r.

Variation of constants gives, with k=m+2>2,

    |w(t)|≤[|w(0)|+2b0²/k]e^(−kt).                    (19)

It follows that b→0, s→1, a→1 and μt→N(0,I). The exact KL is

    E=½[b²+s−1−log s].                                (20)

The dissipation is strictly positive off b=0,s=1, by §5 or directly from (22) below. The elementary inequality log s≥1−1/s gives s−1−log s≤(s−1)²/s; hence Dc≥Df≥b²+(s−1)²/s≥2E. A sharper exact inequality is Dc≥6E throughout this Gaussian family. To verify it, set

    R(s)=(s−1)²(1/s+1/2)−3(s−1−log s).

Then R(1)=0 and R′(s)=(s−1)³/s², so R(s)≥0 for every s>0. Using (22),

    Dc−6E=R(s)+b²(s−1)²/s+b⁴/3≥0.

Consequently E(t)≤E(0)e^(−6t). This stronger inequality was supplied by the reviewing investigator and verified algebraically here; it is a participating extension, not independent confirmation of itself.

For the requested correlated example b0=c≠0, s0=1−c², the exact asymptotic exponent is 6. Indeed

    (log|b|)′=−3−w−r/3,

and (19) makes the last two terms integrable. Therefore e^(3t)b(t)→B∞≠0. Also

    (e^(3t)w)′=e^(3t)(−w²+2r)

is integrable because 2k>4>3. Hence e^(3t)w→W∞ and Taylor expansion of (20) gives

    E(t) ~ [B∞²/2+W∞²/4] e^(−6t).                     (21)

This rate statement is for this explicit invariant Gaussian family. It is not extrapolated to general laws or objectives.

## 7. Exact cost and rate comparison, including a closed-form comparator

At a common fixed-marginal Gaussian state, direct quadratic Gaussian integration gives

    Df=b²+(s−1)²/s+b²s+(s−1)²/2,
    Dc=Df+b²/s+b⁴/3,
    Du=Dc+b⁴/6.                                       (22)

The horizontal correction itself costs Bν(φ,φ)=b⁴/6. For b≠0 the inequalities Du>Dc>Df are strict. The lost full-gradient dissipation is the necessary marginal-preservation cost, while the further gap to Df is due to restricting the field controls.

Initially r=c², s=1−r, so

    Du=2r/(1−r)+r,
    Dc=2r/(1−r)+r−r²/6,
    Df=r/(1−r)+r−r²/2,
    Dc−Df=r/(1−r)+r²/3>0.                             (23)

For c=1/2 these are Du=11/12, Dc=29/32, Df=53/96. The full unconstrained y-variance derivative is −1/4; the full constrained and fibrewise derivatives are both zero. Initial covariance derivatives are respectively −3/2, −17/12, and −7/8. Both valid constrained rules decrease full KL, but only (1) is the gradient for the full declared tangent metric.

There is even a concrete nonminimal-representation control. At c=1/2 the fibrewise tangent covariance derivative is [[0,−7/8],[−7/8,−3/16]]. Its field action is 53/96, while solving the full Gaussian tangent equation produces quadratic potential matrix

    Bf=[[-235/924,17/42],[17/42,−43/231]],

whose negative-gradient fields represent that same tangent with full minimum action 2489/7392. The excess field cost is 199/924>0. Cutoff duality makes these potential fields truly ambient-minimal. This exact test prevents confusing restricted field action with full tangent action.

For (13), the conditional Gaussian mean and variance satisfy

    b′_f=−(1+s_f)b_f,       s′_f=(1−s_f)(s_f+2).

With the same correlated initial state and q_t=e^(−3t), they have the explicit global solution

    s_f(t)=[3−r−2r q_t]/[3−r+r q_t],
    b_f(t)=3c e^(−2t)/[3−r+r q_t].                     (24)

Its y-marginal is fixed, and its full KL converges to zero with

    E_f(t) ~ [9c²/(2(3−c²)²)]e^(−4t).

The accepted unconstrained Gaussian control converges with exponent 6 but disturbs the initially correct y marginal at every finite positive time. The full constrained construction has exponent 6 while retaining that marginal exactly. These statements compare these three exact examples; the instantaneous inequalities in (23) do not imply a general all-time energy ordering, nor do they assert one flow is a shortest endpoint path. Integrating energy identities can compare accumulated actions only in their properly declared metrics/control classes.

## 8. Ancestry, verification and limits

The general orthogonal-projection principle is classical: Alvarez, Bolte and Brahic, *Hessian Riemannian gradient flows in convex programming*, §2.2, equations (7)–(10), explicitly supplies metric-projected gradients under affine constraints. The present proof applies Hilbert quotient duality in the declared distributional tangent geometry; no originality is assigned to the projection theorem. [Primary source](https://arxiv.org/pdf/1811.10331).

Kondratyev and Vorotnikov, *Spherical Hellinger-Kantorovich gradient flows*, Remark 1.1 and Definitions 3.14–3.15, provide the centred Onsager convention and unit/unit action; their PDE hypotheses are not imported as existence for this constrained Euclidean equation. [Primary source](https://arxiv.org/html/1809.03430v2).

Liero, Mielke, Tse and Zhu, *Evolution of Gaussians in the Hellinger–Kantorovich–Boltzmann gradient flow*, §3.4, Theorem 3.11, equations (3.8a,b), supplies the classical unconstrained Gaussian SHK KL flow. We directly verify the additional multiplier and fixed-marginal density tangent here. [Primary source](https://www.wias-berlin.de/preprint/3198/wias_preprints_3198.pdf).

SOURCE_READING.json records these focused primary locators. This is not an exhaustive literature search. verify.py checks exact symbolic identities, full density tangency, Gaussian controls, dissipation differences, the rational example, closed-form fibrewise solution, barriers' algebra and bound identities, plus inherited file bindings. Finite symbolic controls supplement the ordinary Hilbert and ODE proofs; they do not prove general PDE existence or universal inequalities by testing. Run `python3 verify.py --output-dir private-locator:5198022b8c2d094ce857`, optionally with `--original-root ..` to check the original input files as well as snapshots.

The construction gives a conditional operation when a marginal and hidden target are supplied and retention of that marginal is required. It does not warrant the selected marginal, prove hidden target truth, recover discarded information, identify a cognitive state with a density, establish intervention authority, import universal PDE regularity, prove a global all-laws smooth manifold, replace the accepted obstruction, or close T20.
