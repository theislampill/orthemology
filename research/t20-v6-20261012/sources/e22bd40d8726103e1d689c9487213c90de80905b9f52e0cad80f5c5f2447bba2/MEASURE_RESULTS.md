# Measure research: qualified results and interpretation

This successor adds checked measure-theoretic structure to the recovered P02 programme while retaining its actual positive-singleton definitions. It is a research shadow at main 03e2604dfcef278b01c60d19b05370fcec4194b6, not canonical adoption.

## 1. Robustness of the whole classification law

The positive-mass events depend on the input law. The proof does not pretend that the two laws use the same classifier. A union of their countable positive supports gives a shared representative under each law, enabling a genuine total-variation contraction. It covers the whole countable pattern and its measurable decoders, including initial loss, finite loss stage, infinite residual and retained full-history atom.

The convention is TV = supremum over measurable events, without the factor two of signed total variation. First loss 0 is initial diffuseness; first loss n+1 is CV-R loss L_n under coherent refinement. Residual and finite-stage mass identities connect these labels to the actual P02 events.

The resulting pattern-law operator is additive on finite measures and homogeneous for nonnegative real scalars. Nevertheless there is no single law-blind measurable classifier of one realised point that reproduces it for all laws. The stronger expected-value obstruction covers randomized single-point tests too. This does not prohibit model-dependent classification or inference from additional independent acquisitions.

## 2. Exact finite-horizon non-identifiability

For every chosen finite horizon N and every r in [0,1], an explicit probability law has the same finite-prefix distributions as fair Cantor input through N, but its defect is exactly r. The law depends on N and r. It is not one different law agreeing at all finite horizons simultaneously.

The endpoints are a finitely supported truncated fair law and the fully diffuse fair law; their full-law event TV is exactly one. Convex mixtures give the entire interval. Thus finite-prefix agreement cannot replace the full-law TV premise of the robustness theorem.

## 3. Two generalisation guards

An arbitrary-index product-sigma-law version is also checked, using finite-cylinder uniqueness. Simultaneous almost-everywhere equality of all coordinates is not claimed. A concrete fair-Cantor spike map has the same product-sigma law as an all-zero constant map while differing from it at every point. The all-zero singleton is then nonmeasurable, so it is not an admissible decoder test.

On general measurable spaces, positive-singleton mass differs from unrestricted measure-algebra atomicity. The checked countable-cocountable example has a whole-space measure atom and singleton defect one. See PointAtomBoundary.md for the classical source and exact scope. Standard Cantor-space uses avoid that pathology.

## Evidence and reuse

The primary fresh receipt qualifies thirteen frontier modules and 84 named theorem targets, including six explicitly overlapping helpers from PositiveMass.lean. The independent reviewer rebuilt all eighteen local modules including P02/Q8 dependencies, using only pinned official Mathlib caches. All targets use only propext, Classical.choice and Quot.sound.

The archive includes that full custom dependency source closure, both receipts and the independent audit readback. Lean is 4.19.0, compiler commit 6caaee842e94; Mathlib is c44e0c8ee63ca166450922a373c7409c5d26b00b. Historical filesystem paths in receipts describe the observed run; the tranche's portable wrapper supplies relocated replay commands. No historical novelty or general learnability claim is inferred from these kernel checks.
