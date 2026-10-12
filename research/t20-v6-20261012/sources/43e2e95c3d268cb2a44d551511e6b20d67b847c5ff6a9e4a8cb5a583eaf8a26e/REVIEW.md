# Independent review: damped transport escape

Verdict: PASS, with the explicit scope limitations below. This is an ordinary mathematical review, not a formal proof-assistant verification or a literature-novelty determination.

## Exact reviewed result

Reviewed `transport-rank-boundary-20261010/RESULT.md`, SHA-256 `af3b82f3773723ef2f2ac9154983f06da385e06f29efc54b952f808cbf1e61a5`, plus its exact controls and the page 21–23 source images. The separate JSON receipt binds their final bytes and the independent controls. No changes to those source artifacts were needed.

## Independent mathematical derivation

Write x=(1−t)^(−1), c=exp((1−x³)/3) for t<1. Then x′=x² and c′=−x⁴c. Distributional multiplication gives −g∂xμ=−∂x(gμ)+g′μ, so g=x² and h=−x⁴−2x produce dual generator Lp=x²p′−x⁴p. Omitting the −2x term would produce the wrong weight equation.

For compact spacetime test ψ, the derivative of c(t)ψ(t,x(t)) equals c(ψ_t+x²ψ_x−x⁴ψ). Its terminal boundary value vanishes: the moving atom leaves any fixed compact spatial support before t=1. The stationary contribution integrates ψ_t(t,0) to zero. This proves the full spacetime identity, including the escape time, with no hidden time delta. Compact-time mass is bounded. The construction is also continuous through 1 in total variation, since the total variation of its difference from δ0 is c→0. It is not claimed to be total-variation differentiable while the atom moves.

For each integer k≥0, m_k=1_{k=0}+c x^k before 1 and 1_{k=0} after 1. Repeated differentiation sends cP(x) to c[x²P′(x)−x⁴P(x)], preserving the polynomial form. Every derivative therefore tends to zero at 1 by exponential domination. Extension by zero of the moving contribution is C∞ and flat. This proves all-order smoothness, not just the finite indices sampled computationally. The hierarchy is m_k′=k m_{k+1}−m_{k+4}, including k=0 and t=1.

The leading 2×2 minor is cx²>0 before 1. The measure has two distinct support points there, so its entire Hankel rank is two, while afterward it is one. Rank is uniformly bounded but not constant.

More generally, for fixed a,b>0, μ=aδ0+bcδx has mass N=a+bc and normalized moments q_k=m_k/N. Quotient differentiation yields q_k′=kq_{k+1}−q_{k+4}+q_4q_k. Thus ν obeys ∂tν=−∂x(x²ν)+(−x⁴+q_4)ν. In nondivergence form the reaction is −x⁴−2x+q_4. Its rank minor is abc x²/N². Distinct positive mixture ratios b/a give distinct normalized initial laws and all reach δ0 at t≥1. Distinct unnormalized initial measures with a fixed and b varying all reach aδ0. This demonstrates noninjectivity of the exhibited propagation, not nonuniqueness for a fixed initial datum.

For every fixed k≥0, the moving tail moment is bounded by exp(1/3) sup_{x>R} x^k exp(−x³/3), which tends to zero. For R³≥k the tail function is decreasing, and its supremum is bounded by exp((1−R³)/3)R^k. Consequently the entire time family is uniformly tight and has uniformly integrable moments of each fixed order. The generalized normalized family has the same property for each fixed a,b>0 by N≥a. This is not uniform over all possible initial mixtures when the stationary weight tends to zero. In particular a=0 is excluded: normalization then gives the escaping probability δx, which has no continuous probability extension at 1.

The stronger claims in the note also hold: exp(−x³/3+Ax) is bounded for fixed A>0 and tends to zero at infinity, while exp(−(1/3−B)x³) is bounded and tends to zero for 0<B<1/3. These give the asserted exponential and subcritical cubic-exponential moment bounds and continuity. They do not give a common compact support or a nonexplosive characteristic flow.

Along the moving orbit, accumulated killing is ∫x⁴dt=∫x²dx, which diverges at explosion. This is compatible with a smooth killing rate at every finite spatial point. It is unavailable in the fixed-support, locally integrable pure-killing argument. The example therefore does not contradict the killing-only finite-rank theorem.

## Additional time-reversed corollary

The revised note adds a valid, separate nonuniqueness result. For t>0 put x=1/t and c=exp(−1/(3t³)); before and at zero take only δ0. Then x′=−x², c′=x⁴c, and g=−x², h=x⁴+2x give dual generator −x²p′+x⁴p. The compact-spacetime pairing glues with no time delta at zero because the moving atom is outside every compact spatial support for sufficiently small positive time. The same polynomial-times-exponential derivative induction gives flatness of every moving moment at zero. Both the stationary solution δ0 and the solution with the incoming atom are global positive distributional solutions with identical initial measure and all initial moment time jets. They differ for every positive time, and their ranks there are respectively one and two.

Normalization gives q_k′=−kq_{k+1}+q_{k+4}−q_4q_k and the distributional PDE ∂tν=−∂x(−x²ν)+(x⁴−q_4)ν. In nondivergence form the coefficient is x⁴+2x−q_4. Both normalized paths solve this same nonlinear equation with identical initial probability law. Tail bounds, including the exponential bounds, follow exactly as before, now without the exp(1/3) multiplier. This is genuine forward nonuniqueness in the unrestricted distributional/smooth-moment solution class for these unbounded coefficients. It says nothing against uniqueness after an appropriate no-inflow or globally defined characteristic-pushforward solution-selection condition, nor against bounded-coefficient or killing-only theorems.

The final result was updated by its author during review. An attempted binding to the earlier hash correctly failed; no stale receipt was issued. This review and the completed binding instead cover the final revised result and controls, including the reverse-time corollary.

## Source verification and attribution

Independently viewed all three supplied PDF page images. Printed p.21 places Lemma 4.1 in the bounded-smooth class and gives the h+div g weight correction. Printed p.22 displays the weaker continuity assumptions in Theorem 4.2. Printed p.23 explicitly treats extension beyond bounded smooth coefficients and Example 4.5 gives x′=x² and finite-time escape, followed by the boundedness warning. Consequently a standalone reading of the displayed theorem hypotheses is too broad, but the section context and the authors' explicit escape discussion must accompany that statement. The damping hides escape from all fixed moment blow-up tests; no claim is made that these authors overlooked explosion or that this damping example is new in the literature.

The web tool could not fetch the arXiv HTML/PDF during this review. Source wording was verified from the exact local page images instead; this does not establish independent provenance of the entire PDF beyond the supplied artifact.

## Controls and preservation

Replayed the author's exact checks and verified all three published SHA-256 entries. Independently checked generalized a,b mixture algebra, normalized moment equations through order 9, rank minor, accumulated-killing antiderivative, and negative controls for an omitted divergence correction and omitted normalization compensation. All checks passed. The checks supplement the direct proof, and the reviewer did not edit any author/source files or any prior protected originals.

Final wording check: the forward noninjectivity section now explicitly limits its no-uniqueness-refutation disclaimer to that forward construction, avoiding conflict with the separate reverse-inflow nonuniqueness result. The author froze the final artifacts before this binding.
