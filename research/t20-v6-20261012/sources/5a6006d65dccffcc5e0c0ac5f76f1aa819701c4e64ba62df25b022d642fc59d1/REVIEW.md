# Independent reference-gradient review

2026-10-11. Verdict: PASS, no blocking mathematical finding for the bounded claims reviewed.

Reviewed artifact: reference-gradient-descent-classification-20261011/RESULT.md
SHA-256: 097e12106db027914a1a05795c8d4dde647e9c73e52882562eef5f546f6d7c18

## Mathematical checks

- Independently derived the constrained diagonal-Hessian cometric and gauge invariance. Positive weights give the required tangent duality, and linear objectives exhaust covectors modulo constants.
- The universal deterministic equivalence is valid. The aligned representative proves that all-objective fibre constancy forces canonical agreement. The anchored binary mobility is injective, and the normalized three-input buffer reaches arbitrary positive density ratios and all convex weights. Quantification over varying references is essential; a single fixed reference cannot test the whole positive half-line. The theorem correctly includes that quantification.
- Positivity of an affine reciprocal curvature on the entire positive half-line forces both coefficients nonnegative and excludes the zero pair. Generator integrations, endpoint cases and affine-gauge freedom are correct.
- Both reported same-fibre fixtures give the stated signed velocities. The distinction between same-time failure and unparametrized trajectory failure is correctly retained.
- The reference-aligned section is invariant for each pulled-back objective. C3 generator and C2 objective supply a C1 local vector field, hence local uniqueness; only common positive existence intervals are claimed.
- The full stochastic decomposition is correct for nonnegative column-stochastic K with no zero row and concave positive r. Rowwise Jensen yields V >= W. The weighted-square identity proves the first matrix gap is PSD; the column-variance identity proves the second is PSD. For at least two outputs, all-objective equality forces V=W and deterministic columns. The one-output exception is indispensable and present. Single-objective survival is explicitly distinguished from full matrix equality.
- The affine-blend Fisher pullback and KL factor M/a² are correct for a>0. The restricted image for b>0 and the warning against promoting blended recovery to original-law recovery are appropriate.

## Independent discriminating controls

Executed independent_controls.py in this review directory, without rerunning the author's test suite. Six exact SymPy groups passed:

1. G_(1,1)=G_(2,2/3), rejecting an unrestricted binary weight-injectivity inference.
2. W=(1,1,1), V=(2,1,1), g=(0,1,-1) gives zero individual-objective gap with unequal matrices.
3. A genuinely noisy concave-r example independently verifies both terms of the decomposition and a positive gap.
4. At a reference-aligned noisy-channel state, the Jensen gap vanishes but the channel-variance gap remains.
5. One output has equality of zero tangent fields despite unequal Jensen weights.
6. For convex r=t², a deterministic merge reverses the proposed PSD direction, confirming the need for concavity in the stochastic comparison.

## Ancestry and boundaries

Read the relevant local passages of the four inherited reports. Their stated ancestry supports the use of the constrained inverse-Hessian formula, the constant-quadratic/noisy-channel discriminator, fibre-constancy criterion, and conditional leaf remedy. The new result is accurately separated from inherited divergence contraction. No new external priority or primary-source verification is claimed in this review. The packet explicitly disclaims source authentication, cognitive realization, objective/reference authenticity and programme closure.

All MANIFEST.json artifact bindings and INPUT_BINDINGS.json inherited-source bindings matched the current bytes when checked. No protected files or author artifacts were changed. This is ordinary independent mathematical review with exact finite controls, not formal-kernel certification.

Final punctuation-only rebind: removing the two added commas from the verification-coverage sentence exactly reproduces the previously reviewed SHA-256 538088001dc8f0d4ee9d36ef8a99380ec55a6a8de255663fbad037bb6302574a. All final artifact and input bindings rechecked successfully; review scope and independent controls unchanged.
