# Source audit and attribution

8 October 2026 UTC. This is an account of sources inspected and proof dependencies, not an active-duration certificate. Historical floor remains UNVERIFIED. All writes are confined to this new sibling; log-four, other predecessors, archives, and protected repositories are unchanged.

## Prior-art findings actually checked

- [Last–Molchanov, Poisson hulls, arXiv:2212.02150v4](https://arxiv.org/html/2212.02150v4). Directly inspected the Pareto-minimum example, Theorem 3.2 and its proof, and Theorem 5.1 and its conditional-variance proof. These establish the relevant general posterior and weighted variance results. Theorem 3.2 cites another spatial-Markov theorem; no recursive verification of that citation is claimed. The present RESULT independently proves its finite-square specialization from skyline densities. No normal-approximation theorem is used.
- [Last–Molchanov, Efron type identities for stopping sets and Poisson hulls, arXiv:2608.06038v1](https://arxiv.org/html/2608.06038v1). Directly inspected Theorem 4.7 and its full proof, Corollary 4.8 and its coefficient argument, and Example 8.4. These confirm the exponential-identity attribution and Pareto match. This is the 2026 preprint. Its older antecedent was not read directly here; attribution remains mediated by this source.

The prior-art sibling supplied discovery and a more extensive source review. Its inspected RESULT, SOURCE_AUDIT and independent review are separately digest-bound. This sibling does not claim a second literature search, exhaustive novelty assessment, new source discovery, or a read of every text cited in that report. It uses no convex-hull-only transfer theorem.

## Proof dependencies and roles

- retained-skyline-likelihood/RESULT.md: exact fixed-count ordered-stratum law, family/density definition, common-support likelihood, singular stratum and factorial mass bound. These are inherited results; the finite-Poisson law is derived by mixing that exact law.
- skyline-count-information/RESULT.md: baseline record representation and the actual Joe conditional-quantile coupling. Independence is used only for the ordinary uniform record indicators. The count-test upper bound is a comparator, not an optimality result.
- skyline-likelihood-score/RESULT.md: localized deterministic expansion with the original constant 40. Its global-boundary limitation is preserved.
- full-skyline-reverse-kl/RESULT.md: dyadic height strategy, both-world entropy window, global log bound, positive singular correction, and actual-action adaptive transport. This sibling restates and checks the pieces it uses and sharpens only the integrated baseline local score.
- full-skyline-reverse-kl-review/REVIEW.md and REVIEW_RECEIPT.json: completed independent verification of the preceding log-four theorem. Its verdict explicitly excludes the new log-squared strengthening, so no review approval is transported to this sibling.
- skyline-probability-prior-art/RESULT.md and SOURCE_AUDIT.md: discovery and mapping of general Poisson hull identities, and the separate fixed-count area-MGF corollary. The latter is acknowledged but is not required for this proof's dyadic raw-moment and tail estimates.
- skyline-probability-prior-art-review/REVIEW.md and VERIFICATION_MANIFEST.json: inspected source-mapping review; it does not certify this sibling's fourth-moment or KL result.

SOURCE_BINDINGS.json contains the exact byte hashes and these roles. The proof's finite-Poisson posterior, constant restricted density comparison, fourth-moment inequality, and weighted-tilt identity are given explicitly, avoiding an unqualified transfer after conditioning. Both the empty Poisson stratum and the fixed-count bad-area event are treated.

## Supplied candidate versus this packet's work

The parent supplied the candidate rate and the central route: posterior-conditioned skyline ratio, local uniform density domination, fourth differentiation, Cauchy–Schwarz, weighted compensation, residual L2 bound, and entropy/stopping reuse. During the work it supplied the inhomogeneous intensity tilt as an especially direct weighted-identity check. The parent also warned that these suggestions were candidates until proved and were not fresh research credit merely because a worker restated them.

This packet checked all those steps, furnished explicit finite inequalities and constants, wrote the complete proof, independently checked the weighted identity through both density tilting and conditional total variance, and built deterministic controls without importing predecessor code. This is bounded verification and synthesis of the supplied route. General Poisson compensation and variance formulas remain attributed to the cited prior art, even though their specialized proofs are reproduced here. No field-wide novelty is asserted.

The separate reviewer identified two wording inaccuracies before final freeze: a floor(v) inequality chain that failed for 1≤v<2, and a sentence incorrectly ascribing the empty-stratum zero to the negative-integer pmf convention. The first had also been independently noticed by the author; both are corrected. They did not change any displayed rate, constant, or proof mechanism. The reviewer has not been credited as discovering the parent-supplied theorem.

## Executable controls and what they establish

controls.py was run successfully and its stdout is retained. It checks:

1. Symbolic derivatives and rejection of the wrong mixed-moment sign.
2. Exact formal Poisson-intensity coefficients through order five, by direct integration over ordered skyline strata k=0,…,5. Higher strata cannot contribute to those coefficients. Skyline normalization, the fourth-moment identity and the weighted-variance identity all match exactly; omitting the empty atom fails.
3. The exact posterior/direct-density algebra at 156 deterministic configurations, plus 40 numerical maximum-mass bounds.
4. Six high-precision weighted integrals against the proved elementary envelope.
5. Exact sixth-power falling-factorial coefficients and 64 exact rational record distributions, checking second and sixth raw-moment bounds.
6. Seven finite scale diagnostics for already-proved asymptotic comparisons.

The coefficient integrations use rational arithmetic and independent ordered-simplex monomial formulas. The density and quadrature diagnostics use high-precision floating-point arithmetic, not interval certificates. None is a random simulation or empirical experiment. Tests cannot replace the written proof of an all-n asymptotic or all-policy information inequality. This packet's own independent review is required after the final digest freeze.

## Boundaries

No mutation of another packet, no GitHub use, no integration, no historical-duration certification, no physical-access assertion, no unconditioned finite forward KL, no Θ result, no leading lower constant, no matched logarithmic optimality, and no audit closure. The written lower bound uses E0 started vectors and unconditional terminal correctness. No finite exact skyline reconstruction is asserted.
