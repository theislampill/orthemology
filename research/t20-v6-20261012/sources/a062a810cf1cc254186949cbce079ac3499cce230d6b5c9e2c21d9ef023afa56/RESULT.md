# Correlated targets in the same fixed-marginal correction geometry

11 October 2026 UTC. Additive ordinary mathematics within ACTIVE T20. Accepted and frozen predecessor packets are unchanged. No protected edit, integration, formal-kernel proof, field-priority, empirical-noetic or closure claim. The parent proposed this correlated-target scope test and separately checked the multiplier and coordinate ODE. The investigator derived and verified the general conditional score, full-density projection, exact correlation-creating example and global convergence proof. The fixed-marginal mobility is inherited from the earlier independent review, not newly discovered here.

## 1. Positive result and exact scope

Fix the y-marginal N(0,1). On centred nondegenerate Gaussian laws write

    μ(b,s)=N(0,Σ(b,s)),
    Σ(b,s)=[[1,b],[b,b²+s]],       b∈R, s>0.

Supply an arbitrary centred Gaussian target with that same marginal,

    π=N(0,Γ),       Γ=[[1,β],[β,β²+τ]],       τ>0.       (1)

The target conditional law is N(βy,τ); it is generally dependent on y. Keep exactly the inherited unit full transport/centred-reaction tangent metric and the entire fixed-y-marginal constraint. Its constrained mobility in (b,s) coordinates is

    Mc(b,s)=[[1+2s+b²/3, −2bs],
             [−2bs, 2s(s+2+2b²)]].                    (2)

This geometry is independent of the target parameters β,τ. The conditional KL energy is

    E(b,s)=½[(s+(b−β)²)/τ−1+log(τ/s)].                (3)

The actual full-density projected flow is exactly −Mc∇E. It stays in this Gaussian family, preserves the entire N(0,1) y-marginal, exists uniquely for all forward times within the family, and converges to (b,s)=(β,τ) from every b0∈R,s0>0. Thus this geometry does not force independence: the product-target predecessor erased correlation because independence was part of its supplied target. A correlated target is stationary and attracts the present correction.

Only the y-marginal is conserved. The cross covariance b is not an extra invariant; even b=β can move temporarily if s≠τ. No claim of independently warranted target correlation, general-law PDE uniqueness, or a new convergence-rate programme is made.

## 2. Inheritance and primary ancestry

The bounded comparison inspected the files copied and hash-bound in INPUT_BINDINGS.json:

- fixed-marginal-correction-20261011/RESULT.md owns the full-tangent constrained projection, product-target weak resolvent and Gaussian global construction.
- fixed-marginal-correction-independent-review-20261011/REVIEW.md already derives (2), its positive definiteness and its full-tangent interpretation. This packet uses that metric for a different energy, and independently verifies the resulting full-density tangent.
- full-law-coarse-graining-20261011/RESULT.md owns the product-target conditional-KL obstruction and warns that a stipulated objective matters to transport.
- gaussian-primary-shk-comparison-20261011/RESULT.md owns the comparison to the classical arbitrary-Gaussian-target SHK covariance ODE and its entropy-sensitive interpretation.

The classical Gaussian operator is explicitly in Liero, Mielke, Tse and Zhu, *Evolution of Gaussians in the Hellinger–Kantorovich–Boltzmann gradient flow*, §3.4, Theorem 3.11 and (3.8a,b), with arbitrary positive-definite target covariance Γ. We use its unit/unit convention and derive the additional fixed-marginal compensation directly. [Primary source](https://www.wias-berlin.de/preprint/3198/wias_preprints_3198.pdf).

Constrained metric projection itself is classical. Bauer, Charon, Needham and Nishino, *Path constrained unbalanced optimal transport*, §3.2 and Remark 4.24, explicitly uses weighted-Sobolev projection of constraint potentials. [Primary source](https://arxiv.org/html/2402.15860v3).

No inspected predecessor already gives the present correlated-target fixed-marginal ODE and convergence statement. This is a targeted local comparison, not an exhaustive literature priority claim. The addition is a bounded application showing that the same full constrained geometry can correct toward a supplied dependent target, together with the exact score term needed to do so.

## 3. The missing term for a nonproduct target

Use the inherited definitions

    Dμ(v,α)=−div(μv)+μα,
    jμf=(∇f,f−μf),       Kμf=Dμjμf,
    Bμ(f,g)=∫∇f·∇g dμ+Covμ(f,g).

The norm of a density tangent is the infimum of ∫(|v|²+α²)dμ over all fields realizing that entire tangent, with μα=0. Admissible potential fields jμf attain this infimum by cutoff duality. Under orthogonal observation T(y,z)=y, the full-tangent constrained negative gradient is

    μdot=−Kμ(q−φ∘T),       Kνφ=T_*Kμq,               (4)

where q is the first variation modulo constants. This projection formula is inherited and applies to the present objective; a specialized formula for its right side must still be recomputed.

For a general fixed-marginal conditional target π(dy,dz)=ν(y)r*(z|y)dy dz and current law μ=νr, set

    q=log(r/r*),
    h(y)=Eμ[q|Y=y],
    m(y)=Eμ[∇y q|Y=y].

Under the same differentiation, integrability, flux and cutoff conditions as the predecessor,

    m(y)=−Eμ[∇y log r*(Z|y)|Y=y],
    T_*Kμq=−div_y(νm)+ν(h−νh).                        (5)

The first identity uses ∫r∇y log r dz=∇y∫r dz=0. The second follows by averaging the field representation, including its spatial flux. For a product target, r* is independent of y and m=0. For a correlated target, that cancellation generally fails.

Consequently the centred multiplier solves

    −div_y(ν∇φ)+νφ=−div_y(νm)+ν(h−νh),    νφ=0.       (6)

There is a corresponding weak solve in the predecessor's weighted Sobolev space: the right-side functional is ∫(∇ψ·m+(h−νh)ψ)dν. If m∈L²(ν) and h−νh∈L²(ν), it is bounded for the coercive bilinear form ∫(∇φ·∇ψ+φψ)dν. Riesz representation yields the centred weak solution, exactly as before. This is an instantaneous solvability statement, not a new general nonlinear PDE theorem. The present Gaussian multiplier is explicit.

## 4. Exact multiplier and full Gaussian density tangent

Put δ=b−β and e=z−by. Under μ(b,s), Y~N(0,1) and e~N(0,s) are independent. The score is

    q=½log(τ/s)+(e+δy)²/(2τ)−e²/(2s).

Its conditional mean and spatial y-score satisfy

    h(y)=½[log(τ/s)+s/τ−1+δ²y²/τ],
    h−νh=δ²(y²−1)/(2τ),
    m(y)=−βδ y/τ.                                     (7)

The y derivative here holds z fixed; it is not differentiation while holding e fixed. This distinction is essential.

Because ν=N(0,1), −∂y(ν k y)=kν(y²−1). Hence (5) gives

    T_*Kμq=γ ν(y²−1)/2,
    γ=δ(δ−2β)/τ=(b−β)(b−3β)/τ.

Since the centred quadratic y²−1 has eigenvalue 3 for the weighted operator −ν⁻¹∂y(ν∂y)+I,

    φ(y)=γ(y²−1)/6.                                   (8)

This reduces to the accepted product-target multiplier when β=0,τ=1. The alternative obtained by retaining only h−νh would use γwrong=δ²/τ. With that wrong multiplier, the full Gaussian y-variance derivative is

    (Σ′wrong)yy=2βδ/τ,                                (9)

so it fails to retain the specified marginal in general. The old product-target theorem is unchanged; (9) is a failed transfer of its specialized right side outside its hypotheses, repaired by (5).

Let

    A=Γ⁻¹−Σ⁻¹,       E11=diag(1,0),
    C=A−(γ/3)E11.

Up to constants, the projected potential q−φ is xᵀCx/2. Its negative-gradient minimum fields are

    v=−Cx,
    α=−½[xᵀCx−tr(CΣ)].                                (10)

They have finite action and justified polynomial cutoffs under every nondegenerate Gaussian. Direct density differentiation gives

    Σ′=−(CΣ+ΣC)−ΣCΣ
       =2I+Σ−Γ⁻¹Σ−ΣΓ⁻¹−ΣΓ⁻¹Σ
           +(γ/3)(E11Σ+ΣE11+ΣE11Σ).                  (11)

To check the entire density, not merely covariance moments, divide the Gaussian tangent by its density:

    ρdot/ρ=−½tr(Σ⁻¹Σ′)+½xᵀΣ⁻¹Σ′Σ⁻¹x.

Substitution of (11) equals

    tr C−xᵀΣ⁻¹Cx−½xᵀCx+½tr(CΣ),

which is exactly [−div(ρv)+ρα]/ρ from (10). The yy component of (11) is zero. Therefore the constructed trajectory retains the full Gaussian y-law, and the full density field stays tangent to the stated family. All means remain zero by the quadratic/linear form of the fields.

Reading the remaining entries gives

    b′=[b(s−τ)−δ(1+2s+b²/3)]/τ,
    s′=[2bsδ−(s+2+2b²)(s−τ)]/τ.                      (12)

This is an exact smooth ODE on R×(0,∞), with no moment-closure approximation.

## 5. Same full constrained metric, target-dependent energy

The differential of (3) is

    Eb=δ/τ,       Es=(s−τ)/(2sτ).

Multiplying it by the inherited matrix (2) gives precisely (12) with a minus sign. Moreover

    Mc,11=1+2s+b²/3>0,
    det Mc=(2s/3)(b²+2s+1)(2b²+3s+6)>0.              (13)

Thus Mc is positive definite for every b∈R,s>0. Its inverse is the induced full tangent metric on this fixed-marginal Gaussian family. Equations (4), (8), (10) and the full-density identity show more than coordinate steepest descent: the resulting vector is the actual projected full-law gradient, and the potential fields minimize among all representations of its full density tangent.

Along it,

    E′=−Dc,
    Dc=(∇E)ᵀMc∇E
       =tr(CΣC)+½tr(CΣCΣ).                             (14)

For completeness the minimum compensating horizontal correction costs

    Bν(φ,φ)=γ²/6,
    Bμ(q,q)−Dc=γ²/6.                                  (15)

These are instantaneous action identities in the same inherited metric, not an additional rate-optimization problem or a shortest-endpoint-path claim. The target parameters change the energy and its multiplier, not the geometry (2).

## 6. Global existence and convergence without a rate claim

Write u=s/τ. Then

    E(b,s)=δ²/(2τ)+½[u−1−log u]≥0.                    (16)

The scalar function g(u)=u−1−log u is continuous on (0,∞), has unique minimum zero at 1, and tends to infinity as u↓0 or u→∞. Therefore every finite E-sublevel has b bounded, s bounded above, and s bounded away from zero. It is a compact subset of the open Gaussian parameter domain.

Fix initial b0∈R,s0>0. Smooth local ODE existence and uniqueness applies to (12). Equation (14) holds on its maximal interval, so its state remains in the compact E(b0,s0)-sublevel. The vector field and its derivatives are bounded on a neighbourhood of that compact set; standard ODE continuation therefore gives a unique Gaussian solution for every forward time. If the initial energy is zero, it is the constant target solution.

The only critical point of E is (β,τ). By (13), Dc vanishes exactly there. Since E is nonincreasing and bounded below,

    ∫₀∞ Dc(t)dt≤E(b0,s0)<∞.

On the compact sublevel, Dc is smooth and the trajectory velocity is bounded, so Dc(t) is uniformly continuous. A nonnegative uniformly continuous integrable function tends to zero: otherwise infinitely many separated time intervals would carry a common positive amount of integral. Hence Dc(t)→0. The least eigenvalue of Mc has a positive lower bound on that same compact set, so ∇E(t)→0. Compactness and the unique critical point imply

    b(t)→β,       s(t)→τ,
    Σ(t)→Γ,       KL(μt||π)→0.                        (17)

This establishes global convergence for the explicitly invariant centred Gaussian class. It does not supply uniqueness among arbitrary full-law weak PDE solutions, non-Gaussian convergence, an empirical identification of the target, or a sharp quantitative rate.

## 7. Exact correlation-creating control and what is preserved

Take the independent initial state μ0=N(0,I) and the dependent target

    β=1, τ=1,       Γ=[[1,1],[1,2]].

At b=0,s=1, equations (7)–(8) give

    q=½y²−yz   up to a constant,
    m(y)=y,
    h−νh=(y²−1)/2,
    γ=3,       φ=(y²−1)/2.

The projected potential is −yz up to a constant. Its full minimum negative-gradient fields are

    v=(z,y),       α=yz.                               (18)

At the independent standard Gaussian, these fields give the exact density derivative 3yzρ. Thus

    b′=3,       s′=0,       (Σ′)yy=0,
    E=1/2,      E′=−3.

Correlation is created in the target's direction, while the observed marginal remains exactly correct. The global theorem carries this solution to Σ=Γ; the target itself has q=0, φ=0 and zero vector field. Reusing only the product-style h multiplier would instead yield y-variance derivative −2 in this example.

The preservation contract is exact but specific. At b=β with s≠τ, (12) gives

    b′=β(s−τ)/τ.

So the dynamics can temporarily change a cross covariance that already numerically equals its target while correcting other conditional structure. Only the specified y-marginal is constrained throughout; the whole dependent target is the terminal optimum. This prevents interpreting “retains desired correlation” as an additional unproved coordinate-invariance assertion.

## 8. Controls and boundaries

SOURCE_READING.json records the focused primary locators. DEDUP_SCAN.json records the bounded local comparison. Participating root checks are copied separately and labelled; they are not treated as independent review. verify.py checks the conditional-score term, exact multiplier, full Gaussian density derivative, both coordinate equations against Mc, dissipation and horizontal costs, product specialization, the correlation-creating example, stationarity, determinant factorization and frozen-input identities. These controls supplement the ordinary Hilbert projection and compact-sublevel convergence arguments; they are not formal-kernel proofs.

Run `python3 verify.py --output-dir private-locator:d6808ce252611792fe1b`, optionally adding `--original-root ..` from this directory. The compact-domain singular endpoint theorem remains a separate packet: its path-attainment statement is neither needed for, nor promoted to, this Euclidean Gaussian KL-flow theorem.

The result makes the role of the supplied joint target explicit. Independence is one target choice, not a consequence of the metric. Neither this statement nor objective descent authenticates a desired dependency, turns mathematical correlation into epistemic support, recovers an unknown joint target from its marginal, or closes T20.
