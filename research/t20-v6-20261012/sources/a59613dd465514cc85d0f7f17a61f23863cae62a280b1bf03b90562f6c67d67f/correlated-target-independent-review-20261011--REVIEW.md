# Independent review: correlated-target fixed-marginal correction

11 October 2026 UTC. Bounded ordinary mathematical review. No protected edit, integration, formal-kernel, external peer-review, or closure authority.

## Finding

No blocking mathematical finding in the frozen correlated-target extension. The exact full-density projection agrees with the inherited constrained mobility, and the Gaussian global existence and convergence proof is valid. The result correctly separates marginal preservation from target choice and from conservation of a cross covariance.

Reviewed author RESULT.md SHA256:

    a062a810cf1cc254186949cbce079ac3499cce230d6b5c9e2c21d9ef023afa56

Reviewed author MANIFEST.json SHA256:

    cf3ccb1233fd76a7366591def614c6872e571ffe38a9033db9cdaf4a130e3bfa

REVIEW_BINDINGS.json records the complete author before/after hash map, the byte-identical copied candidate, manifest verification, and replay evidence. The author packet is preserved unchanged under author-snapshot/. The independent derivation and checker were prepared before reading the author checker; they import no author/root code. The parent supplied the proposed result and principal tests, so this is independent verification of those claims, not a blind discovery or independent certification of the parent's contribution history.

## Main checks

1. For q=log(r/r*), the general averaged y-score is m=−Eμ[∇y log r*|Y]. Therefore the coarse positive gradient is −div(νm)+ν(h−νh). The weak multiplier functional ∫(m·∇ψ+(h−νh)ψ)dν is bounded when m and h−νh are square integrable. The inherited coercive form gives a unique centered weak solution. This is an instantaneous weak solve, not nonlinear PDE well-posedness.

2. In the Gaussian family, m(y)=−β(b−β)y/τ. Hence the exact multiplier is φ=(b−β)(b−3β)(y²−1)/(6τ). Retaining only the product-target h term would instead cause y-variance drift 2β(b−β)/τ. The predecessor remains valid in its own product-target scope.

3. Direct substitution of the corrected fields into the density equation gives the exact polynomial density tangent, with parameter equations

       b′=[−(1+2s+b²/3)(b−β)+b(s−τ)]/τ,
       s′=[2bs(b−β)−(s+2+2b²)(s−τ)]/τ.

   This establishes the actual full projected density field and Gaussian invariance. It is not merely covariance closure. These equations are exactly −Mc∇E for the inherited mobility.

4. Independent Gaussian integration gives the full field action D=∇EᵀMc∇E, E′=−D, and horizontal compensation cost (b−β)²(b−3β)²/(6τ²). Mc is positive definite for every s>0, as checked through two equivalent exact determinant decompositions.

5. Every finite KL sublevel is compact inside R×(0,∞). It bounds b, excludes s↓0 and excludes s→∞. Energy decrease and smooth ODE continuation prove global Gaussian existence and uniqueness. The dissipation is uniformly continuous and integrable on the compact sublevel, so it tends to zero. Uniform positive definiteness of Mc and the unique critical point (β,τ) give convergence of the whole trajectory. The complete ordinary proof appears in INDEPENDENT_DERIVATION.md.

6. At b=0,s=τ, the flow has b′=β(1+2τ)/τ and s′=0. In the exact β=τ=1 example the fields are v=(z,y), α=yz, yielding density derivative 3yzρ and action 3. Thus the geometry can create correlation while preserving the entire y marginal. At b=β,s≠τ, b′=β(s−τ)/τ; the report properly disclaims any additional conservation of b.

## Replay and evidence

- The independent checker passes 36 exact controls under ordinary and optimized Python, with equal result files.
- The copied frozen author checker passes 64 exact and binding controls under ordinary and optimized Python, including live original-input bindings; its result files match each other and the frozen author's original outputs.
- Two intentionally corrupted copies of the independent checker are rejected under optimized Python: substituting the h-only multiplier fails the multiplier equation, and differentiating at fixed e instead of fixed z fails the conditional-score check. No author or original checker was changed.
- All author manifest entries and snapshot bytes are verified; the before/after author maps match.

These symbolic controls supplement the ordinary mathematical arguments. Their number or execution does not establish a general PDE theorem or a formal-kernel proof.

## Exact boundaries

The review covers the frozen displayed mathematics and its use of the inherited full-tangent metric. It does not independently redo the author's external primary-source or bounded-priority survey. The predecessor results are explicit dependencies, not newly proved here. The parent/root controls remain participating checks and are not presented as independent review.

The construction establishes global convergence only for this centered nondegenerate Gaussian class, for supplied β∈R and τ>0. It establishes no general-law PDE existence or uniqueness, new rate theorem, shortest-endpoint-path result, warrant for the chosen marginal or dependency, empirical noetic interpretation, protected-text integration, or T20 closure. It is a bounded extension of the valid product-target construction.
