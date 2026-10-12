# Probability transport: independent root derivation

9 October 2026. Ordinary finite-dimensional mathematics, not a claim about measured human cognition or field novelty. This note records the next discriminating operation after the reviewed nonseparable repair classifier. Independent workers are checking the results against the inherited source contracts.

## Three distinct preservation questions

Let K be a nonnegative column-stochastic matrix, with no zero output row. For any positive b, ordinary normalization commutes with K: N(Kb)=K N(b). This says nothing by itself about numerical divergence or objective-driven gradient dynamics.

For example, p=(3/8,3/8,1/4), q=(1/4,1/4,1/2), and K merging the first two categories give half-squared-Euclidean divergences 3/64 before and 1/16 after. A recovery map splitting the first output category equally recovers both distributions. The transformation is information-preserving on this declared submodel, yet it is not an isometry for these separately chosen Euclidean metrics. This does not refute an inherited injectivity or recoverability theorem.

## Transporting a reference measure repairs the quadratic obstruction

Supply a positive reference vector μ, not necessarily normalised, as part of the mathematical structure. Put ν=Kμ and δ=p−q. Define

    D_μ(p,q)= (1/2) Σ_i δ_i²/μ_i.

For each output j, weighted Cauchy–Schwarz gives

    (Σ_i K_ji δ_i)² ≤ (Σ_i K_ji μ_i)(Σ_i K_ji δ_i²/μ_i).

Divide by ν_j and sum. Column stochasticity proves D_ν(Kp,Kq)≤D_μ(p,q). Equality holds exactly when δ_i/μ_i is constant over all i with K_ji>0, separately for each output j. A common reverse stochastic channel recovering p,q,μ gives equality by applying contraction in both directions. This is an explicitly three-object statement. It is not obtained by silently substituting μ for the second probability argument of ordinary χ² divergence.

For the example above, μ=(1,1,1), ν=(2,1) restores exact pairwise-divergence equality 3/64. This is regret/geometry preservation, not equality of vertex-wise losses or absolute expected risks after changing the truth atoms. Replacing ν by fresh unit weights changes the geometry rather than faithfully transporting it. The mathematical repair does not independently warrant μ or establish that an actual noetic representation should use this score. Here μ is a fixed positive reference vector, not the repository's independently typed metaortheme symbol; it remains fixed along each flow.

## The full tangent dynamical question

On the probability simplex, f_μ(p)= (1/2)Σ p_i²/μ_i has positive tangent Hessian. Write M=Σμ_i. Its inverse tangent metric, expressed as a map on ambient covectors modulo constants, is

    G_μ=diag(μ)−μμᵀ/M.

Indeed x=G_μ g has zero coordinate sum, and for every tangent v, xᵀdiag(1/μ)v=gᵀv. Thus the negative gradient field for a smooth objective J is −G_μ∇J.

For a coarse objective Jbar and J=Jbar∘K, the projected fine velocity is −K G_μ Kᵀ∇Jbar. The canonical coarse metric determined by ν gives −G_ν∇Jbar. Their mobility difference is

    C=G_ν−K G_μ Kᵀ=diag(Kμ)−Kdiag(μ)Kᵀ.

For a vector z,

    zᵀCz=Σ_i μ_i [Σ_j K_ji z_j²−(Σ_j K_ji z_j)²] ≥0.

This is the weighted sum of categorical variances of each column distribution. Since μ_i>0, C=0 iff every column of K is concentrated at one output. Both mobilities annihilate constant vectors, so equality for all intrinsic coarse objectives is equivalent to equality of the displayed full matrices. Deterministic lumpings therefore commute with all these pulled-back objective flows; genuinely noisy channels generally do not.

For K=[[3/4,1/4],[1/4,3/4]], μ=(1/2,1/2), and Jbar(r)=r_1, the projected fine velocity is (−1/16,1/16), while the canonical coarse velocity is (−1/4,1/4). This is a dynamical discrepancy despite valid divergence contraction. Statements concern local trajectories remaining in the interior, not global positivity for arbitrary objectives.

## Faithful induced geometry

The pushforward cometric B=K G_μ Kᵀ always gives the correct projected velocity for the pulled-back objective. It is positive definite on the reachable tangent quotient; to obtain a metric on the whole coarse tangent space, K must map the fine tangent space onto it. Otherwise directions outside the reachable image cannot be assigned finite cost by this construction.

More precisely, minimise the fine quadratic energy hᵀdiag(1/μ)h over fine tangent h subject to Kh=v. For v in the reachable image, the unique least-energy lift is h=G_μ Kᵀ B⁺v, where B⁺ is the Moore–Penrose inverse in a chosen Euclidean representation. The minimum energy is vᵀB⁺v. To verify this, the proposed lift is feasible because BB⁺v=v. Its metric inner product with any feasible zero-output perturbation z is (Kz)ᵀB⁺v=0. Pythagorean expansion therefore gives the claimed minimum. The intrinsic quotient and its energy do not depend on the auxiliary representation used to write B⁺.

This supplies a constructive geometry transport, rather than an assertion that information preservation automatically preserves a preselected metric. It also leaves the earlier normalization-only radial field intact: that inherited field commutes with all mass-preserving K when its radial potential is held fixed. The deterministic restriction here concerns the newly considered tangent objective flow and the canonical reference-based coarse geometry.

## Classical ancestry and source-check boundary

Csiszár and Shields, *Information Theory and Statistics: A Tutorial*, §4, printed pp.447–448 (PDF pages34–35), defines χ² among f-divergences and proves lumping monotonicity via the convexity inequality in Lemma4.1. Root inspected that extracted section and proof, not the entire116-page work. The reference-weighted signed-difference inequality above is proved directly, rather than attributed verbatim to that lemma. No local PDF-byte hash was established.

Source: https://www.renyi.hu/~csiszar/Publications/Information_Theory_and_Statistics:_A_Tutorial.pdf

The reference-measure, natural-gradient and quotient constructions have classical mathematical ancestry. This note claims a proved conditional transport and a useful project discriminator, not a new discovery in the external literature, source authentication, cognitive identifiability, metaphysical warrant, or T20 closure.
