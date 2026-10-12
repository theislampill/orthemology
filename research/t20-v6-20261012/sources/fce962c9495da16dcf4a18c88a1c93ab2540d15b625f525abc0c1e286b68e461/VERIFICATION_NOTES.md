# Verification notes

## Executed author evidence

The ordinary proof was checked algebraically against exact examples; no numerical approximation campaign was run.

- author-run/EXACT_CHECKS.json: 91 passed checks, consisting of 79 symbolic controls, six copied-input hashes and six unchanged-original hashes.
- portable-author-run/EXACT_CHECKS.json: 85 passed checks, consisting of the same 79 symbolic controls and six copied-input hashes.
- Runtime in both reports: Python 3.12.14, SymPy 1.14.0.
- A final execution after the last clarity edit to the script passed 91 checks in the separate nonconvex-atomic-limit-final-replay-20261010 directory; its report was byte-identical to author-run/EXACT_CHECKS.json.
- No failing control run occurred before these successful reports.

The script checks power-derivative and comparison identities, monomial trajectories, quadratic and double-well integrated excess energy, replicator normalization, exponential limiting prefactors and merging algebra, unequal-well basin signs and energy gap, an invariant stable trajectory to a saddle, pure extinction, the absent-basin crossover, a critical circle, and the polynomial-times-exponential regularizing envelope derivative.

It does not test a continuum by finite enumeration, prove a general analytic inequality, solve arbitrary basins, construct the semialgebraic sublevel polynomial P effectively, or establish a universal convergence rate. The proof of arbitrary-law convergence is a measure-theoretic argument in RESULT.md §5, and its polynomial envelope is proved there rather than inferred from one example.

## Source consultation

All entries below were consulted on 10 October 2026 UTC. These are source records and bounded descriptions; no full source papers are copied into this packet.

1. Absil, Mahony and Andrews (2005), author-hosted PDF, printed pp.533–535, Lemma 2.1 and Theorem 2.2. URL: https://sites.uclouvain.be/absil/Publi/Convergence_SIOPT/13-60526.pdf . The inequality convention there is ||∇φ||≥c|φ−φ(x*)|^μ with μ∈[0,1). The exact Euclidean gradient flow satisfies its angle and weak-decrease hypotheses. No discrete result is imported.
2. Author record and erratum: https://sites.uclouvain.be/absil/2005.901 . The reported defect concerns discrete Proposition 3.3, which is not used. The finite-length continuous argument is given directly in RESULT.md.
3. Łojasiewicz (1993), journal PDF, printed p.1592: https://aif.centre-mersenne.org/item/10.5802/aif.1384.pdf . It supplies historical primary context. The retrieved inequality-line OCR is imperfect; the operative general statement is the clear Absil–Mahony–Andrews lemma instead. The displayed local trajectory theorem's nonnegative-neighborhood assumption is not transferred to saddle endpoints.
4. Kurdyka (1998), journal PDF, §1, printed pp.771–772: https://aif.centre-mersenne.org/item/10.5802/aif.1638.pdf . Relevant facts are semialgebraic projection/quantifier closure and the finite points-and-intervals property on R. Its bounded-domain Proposition 2 is not used as a global critical-value result.
5. Sard (1942), primary article scan, printed p.883: https://webhomes.maths.ed.ac.uk/~v1ranick/papers/sard.pdf . Scalar critical-value nullity at sufficient differentiability combines with semialgebraic image finiteness exactly as described in RESULT.md §5.

The bounded local deduplication is recorded separately in LOCAL_DEDUP.json. The gradient inequality, finite-length convergence method, semialgebraic facts, Sard theorem, exponential normalization and standard coupling facts are classical. This packet's contribution is the explicit combination and transported limiting-law classification under its stated scope, without a field-priority claim.

## Status boundaries

This is an additive author mathematical packet. Independent review and preservation, if subsequently supplied, are separate evidence. The full-law theorem starts from an actual probability and its characteristic formula. It does not turn an arbitrary full-square-positive abstract hierarchy into that law. For an initial law without moments, moment claims concern positive times and the long-time limit, not finite polynomial coordinates at zero. Physical total variation convergence, global minimization, robust endpoint inversion, and finite support of the arbitrary-law limit are expressly ruled out by the appropriate controls.

No frozen predecessor, protected repository, authorization rule, or programme status was changed. T20 remains open.
