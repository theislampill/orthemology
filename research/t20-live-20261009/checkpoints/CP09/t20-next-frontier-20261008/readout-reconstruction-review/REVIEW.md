# Independent review: exact readout experiment incomparability

8 October 2026 UTC. Scratch-only independent review. Verdict: **ACCEPT for the stated conditional, pair-specific exact-law postprocessing theorem.** No protected integration, T20 closure, physical-access conclusion, or new Lean assurance is authorized by this review.

## Reviewed claim and acceptance boundary

The author’s `readout-reconstruction-boundary/RESULT.md` proves that the exact two-coordinate-minima experiment and the specified fixed, strictly interior, 2n+1-query staircase experiment are incomparable under a common world-independent Markov kernel, for each integer n>=1 in the inherited n-product-uniform versus n+1-iid-Joe hard pair. It also proves a baseline-exact minima-to-panel total-variation error lower bound p, the staircase certificate probability.

This review binds the author’s complete two-file packet and its three cited local source files in `SOURCE_BINDINGS.json`. The review receipt binds this review and its independent controls. The author RESULT digest reviewed is e6a82d4061b3e91af3c2b2a34bb4c836cdd5240caa1a95ff5d1b642b6971de50. Later edits require renewed review; this is not approval of future revisions.

## Mathematical checks

1. **Minima to panel:** The nonnegative-integral proof that absolute continuity is preserved under a Markov kernel is correct for arbitrary measurable output events. Since M1<<M0, a kernel reproducing Q0 must assign E zero probability under M1 as well. Thus exact reproduction of Q1 is impossible and TV(M1K,Q1)>=p follows with the stated supremum-event convention. No measurability shortcut, deterministic-decoder assumption, or unprovided conditional density is used. The bound is explicitly conditional on exact baseline reproduction; there is no claim of a p lower bound when both outputs may be approximate.

2. **Panel reverse support and domination:** A baseline-positive atom contains an open-square realization avoiding every finite query coordinate line, since the omitted set is baseline-null. Its finitely many route/query comparisons have a common positive stability radius. Duplication of one of the n routes preserves every endpoint OR. Independently perturbing all m route copies in their corresponding small neighborhoods preserves that transcript and gives positive iid-Joe probability. The positivity comes from the Joe density throughout the open square, not from assigning positive probability to the exact duplicated vector. This covers n=1 and all transcript atoms, including all misses. Finite support then yields a finite C with Q0<=C Q1; integrating any nonnegative kernel preserves the inequality. The author's modest extension of this domination lemma to any fixed finite endpoint panel is justified by the same proof. It does not assert incomparability for every such panel.

3. **Uniform strip bound:** The inherited derivatives are valid and positive on the open square. On y in [1/3,2/3] and 0<x<1/2, z>=1/3 gives the explicit constant A=c·3^(2-c), with S_xy<=A. The expression for S_y extends continuously and differentiably in x to x=0 on this strip, equals zero there, and hence S_y<=Ax. Together with S<=x^c and S_x<=c x^(c-1), this gives f1<=A[m(m-1)c+m]x^(c(m-1)). Since c(m-1)=n-c and f0>=n²3^(-(n-1))x^(n-1), one may take B=3^(n-1)A[m(m-1)c+m]/n². All constants are uniform in x,y on the declared strip, at fixed n. The proof does not require them to be uniform in n.

4. **Essential, not merely pointwise, obstruction:** For any C>0 choose epsilon>0 small enough that CB epsilon^(1-c)<1 and epsilon<1/2. The positive-area rectangle (0,epsilon)×(1/3,2/3) then satisfies f0>Cf1 everywhere. Both laws have strictly positive densities there, so M0<=CM1 genuinely fails as a measure inequality. For C=0 the failure is immediate. This closes the distinction between a null-line limit and essential unboundedness.

5. **Boundary/singular mass and n=1:** The inherited full-face source proves its densities account for all mass, with continuous margins and no residual boundary or interior singular component. Thus the density comparison applies to the entire readout laws. At n=1, m=2, c=1/2, the factor S^(m-2) is S^0=1 on the open square, f0=1 and 1-c=1/2. No step silently needs n>1. The continuous Joe marginal convention also makes staircase equality-line and axis choices null; the inherited certificate source handles these explicitly.

6. **Direction separation:** The first argument alone would not prove incomparability; the author supplies the independent reverse-domination obstruction. A finite output alphabet does not by itself preclude randomized continuous output, and the proof correctly uses domination rather than that false shortcut. Common kernels cannot depend on the unknown world index, as explicitly required.

## H-source and attribution boundary

I directly inspected the inherited local manuscript’s Theorem 4.2, Proposition 11.1, and Theorem 11.2. The two displayed two-route configurations have identical minima but different interior bits. They are a valid deterministic fibre counterexample to factorization and an illustration of present-versus-expanded-observable adequacy. The author expressly does not treat these individual, null configurations as a continuous-experiment proof. Theorem 11.2 concerns deterministic update descent and is expressly excluded as a stochastic reconstruction theorem. The new kernel statements are proved directly instead. The source binding’s section descriptions match the inspected text.

The Joe law, full-minima density/absolute-continuity results, and positive certificate probability are inherited with exact local-source attribution. The elementary kernel lemmas and strip argument are written derivations. Neither this reviewer nor the author claims field-wide novelty or a new external literature review. No external source is necessary for checking these self-contained elementary claims.

## Independent executable controls

`REVIEW_CONTROLS.py` independently builds one-route transcript laws by rectangular Joe/product-uniform CDF increments and combines routes by exact transcript OR convolution using 90-digit arithmetic. For equally spaced staircases, n=1,2,3, it checks normalization, strictly positive cell masses, Q0 support inclusion in Q1, and the baseline-null/alternative-positive certificate. Observed support sizes are 4 versus 5, 12 versus 13, and 33 versus 34. The n=1 certificate agrees within 10^(-80) with (30-8 sqrt(14))/9. It also tests the explicit derivative and ratio envelopes at 36 strip points covering n=1,2,5,20. All controls passed; details are in `REVIEW_CONTROL_RESULTS.json` and the execution log.

These finite high-precision controls are diagnostics, not exact-arithmetic or kernel proofs and not evidence for a general all-panel incomparability claim. The written arguments establish the all-n and continuum statements.

## Exclusions and resolution

No substantive author correction was required. Acceptance excludes arbitrary larger-count laws, noisy or adaptive readout, repeated or approximately simulated experiments, sample-complexity exponents, efficient count reconstruction, finite physical exact-real readout, actual route architecture, productive or metaphysical conclusions, and T20 closure. The baseline support proof permits a finite-panel lemma; the opposite direction remains tied to a panel with the inherited positive certificate. The existing Lean artifact establishes only the inherited deterministic counting theorem and is not relabeled as a proof of these new measure-theoretic claims.
