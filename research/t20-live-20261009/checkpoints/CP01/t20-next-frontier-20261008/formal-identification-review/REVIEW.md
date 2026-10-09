# Independent Lean semantic and execution review

8 October 2026. This review covers the frozen four-file concrete two-root, finite-effect identification theorem. It does not cover the later arbitrary-root CRT theorem or any probability-space construction.

## Verdict and actual theorem

The formal statement matches the intended algebraic target. For any finite effect type E, H and K each contain five natural-valued histograms on finite subsets, with all empty-output coefficients fixed to zero. SamePanels compares the actual three rational panel expressions on every nonempty query. The conclusion identifies the complete five histograms.

There is no assumed decoder, assumed injectivity, assumed equality of hit counts or bounded-count enumeration hidden in the main hypothesis. Multiplicities are unbounded natural numbers. The empty effect type is covered as a degenerate normalized histogram, not excluded by a hidden nonempty-type premise.

All four deliverable Lean files were read. Calibration.lean proves the concrete three-factor code injective by valuations at 5, 3 and 2, then recovers the guarded hit counts from the solo exponents. HitTransform.lean partitions coefficients into complement-hit and subset mass, proves subset-mass injectivity by finite strong induction, and separates the invisible empty coefficient. CalibratedPanels.lean composes these proved statements. Verification.lean exports the intended signatures and checks their axiom dependencies.

## Independent execution

The four sources were copied byte-for-byte into the separate frozen/ directory. The isolated replay compiles new local .olean files there, so the author's deliverables are not rewritten and stale author-local compiled modules cannot substitute for these new sources.

- Full isolated replay: exit 0, warnings treated as errors.
- Separate Verification.lean replay with --trust=0: exit 0. Lean's help states that this setting checks imported modules rather than trusting them.
- Printed main-theorem dependencies: propext, Classical.choice and Quot.sound only. No sorryAx appears in successful verification output.
- Toolchain: Lean 4.19.0, commit 6caaee842e94.
- Mathlib checkout: c44e0c8ee63ca166450922a373c7409c5d26b00b; tracked working tree clean when checked.

An initial trust-zero command used the wrong working directory for the relative dependency paths and failed before loading Mathlib. That failed attempt is preserved separately. Running from the declared Mathlib directory fixed that invocation error; it required no source or dependency changes. The successful trust-zero log is a distinct receipt.

## Mutation controls checked beyond exit status

The original mutation script accepts any compiler error, so its return code alone would not establish the intended negative control. The independent runner tests each case at one identical path in three phases:

1. Original source compiles successfully.
2. Exactly one formula change is made. Compilation fails at the expected mathematical proof obligation, and the runner checks that the expected goal expressions are present and module/file loading errors are absent.
3. The original bytes are restored and compile successfully again.

Replacing the joint factor 5/6 by 1/6 fails at the intended p-adic valuation identity, displaying both distinct factors. Replacing intersection with query-independent nonemptiness fails at the hit-transform identities, displaying both distinct expressions. Both same-path baseline/mutation/restored sequences returned 0/1/0. Restored hashes equal the original source hashes.

The failed mutation environment prints sorryAx dependencies downstream from unsolved goals because Lean continues diagnostic elaboration after errors. Those failed files are never accepted as proved artifacts. The successful original and restored verification lists only the standard axioms above.

## Assurance boundary

This checks injectivity of explicitly defined rational panel expressions. It does not derive those expressions from a probability space, independently validate calibration or route independence, identify physical gates or numerical route tokens, recover unobserved effects, establish finite-sample performance, or warrant source-faithful interventions. It also does not certify the later arbitrary-root rank or CRT extensions. Those claims remain separate.

Reports, copied source hashes, full replay output and mutation receipts are retained here. No protected source changes, final integration, owner acceptance or research-time floor are claimed.
