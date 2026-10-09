# Source and attribution audit

## Exact local inspection

The following three source files were read in full before deriving this packet. Their pre-work hashes and byte lengths are in SOURCE_BINDINGS.json; final verification checks that they remain unchanged.

1. full-face-threshold-information/RESULT.md, SHA-256 ced60a6b7b98f2b0d181e92f194ca64d201fec2278d61c502e2d13887e803f17. Supplies the exact two-minimum CDFs, common Beta(n,1) margins, strictly positive interior densities with no singular/boundary remainder, global density envelope, finite forward KL, and infinite chi-square. The author also received the contributing worker's confirmation that this result was frozen and subsequently passed its own independent review. This packet does not replace or revise that proof.
2. arbitrary-face-replay-design/RESULT.md. Supplies the exact fixed-threshold worlds, positive finite-difference integral, two-face observation contract, uniform all-rate bound, and sequential-information argument. Its source audit was not independently repeated here.
3. arbitrary-face-replay-design/ASYMPTOTIC_DESIGN.md. Supplies the earlier compact-uniform CDF/finite-cell expansion and sharp nonadaptive two-face KL coefficient 0.2096995101.... That expansion is not treated as a proof of the current density expansion.

The derivative bounds, common transformed density formula, entropy-tail estimate using exponential margins under arbitrary dependence, centered entropy calculation, and face-only kernel scope were checked directly in this packet. The exact transformed density reconstruction is also checked with independent high-precision differentiation in controls.py.

## External-source scope

No external web page or new bibliographic source was opened for this bounded mathematical successor. No external literature search, completeness claim, or new empirical verification is implied. The predecessor documents the Joe/Sibuya ancestry. This packet treats Taylor's theorem, differentiation under compact finite integrals, the layer-cake identity, KL data processing, the KL chain rule, and lower semicontinuity as ordinary inherited mathematics and writes the needed calculations explicitly.

## Contribution and authority boundary

The parent supplied the candidate common-transform/growing-box proof, expected coefficient 1/2, and the crucial dependence-safe tail idea. The author attacked that proposal, supplied a polynomial C2 remainder, used centered entropy to handle first-order mass cancellation exactly, wrote the finite-word and stopping scope, and ran bounded deterministic diagnostics. The fresh reviewer did not contribute to this proof before its first frozen hash was sent for review.

This is an information-channel theorem for an inherited stipulated pair of models. There is no global novelty claim, protected integration, empirical sampling, observed physical/psychological validation, or T20 closure. An accepted scratch proof is not a project closure decision.

## Controls and what they do not establish

controls.py contains exact symbolic identities for the survival-to-density derivative, entropy Taylor coefficient, and exponential moments; 75-digit comparisons of the closed density with separately differentiated H; bounded derivative checks on logarithmic boxes; and two-order deterministic Gauss-Legendre bulk entropy quadratures. CONTROL_RESULTS.json records 511 assertions in the initial run and binds them to RESULT.md. Any later rerun's recorded count is authoritative.

The proof is analytic. Finite grids cannot verify a uniform C2 bound, asymptotic limit, or an entropy-tail theorem. Quadrature-order agreement is a diagnostic, not interval-certified integration error. The tail bounds attached to the numerical quadratures come from the analytic proof and are rigorous, but the numerical bulk values themselves remain diagnostics. No Monte Carlo sampling is performed.
