# Source reinspection, 10 October 2026 UTC

This is an independent rereading of already identified primary sources and inherited project arguments. It is not a claim of first acquisition, first reading by the project, field novelty, or a comprehensive literature review.

## Putinar–Schmüdgen

M. Putinar and K. Schmüdgen, *Multivariate Determinateness*, arXiv:0810.0840v1.

- Primary record: https://arxiv.org/abs/0810.0840v1
- Primary PDF: https://arxiv.org/pdf/0810.0840v1
- Primary HTML rendition: https://arxiv.org/html/0810.0840v1
- Reread Theorem 25, its complete proof, and the following Nussbaum paragraph, printed p. 24, through primary parsed PDF and HTML text. Visually inspected the retained rendering of printed p. 24.
- Exact hypothesis distinction: full positive semidefiniteness plus Carleman in the first d−1 marginals implies existence; the additional final marginal condition supplies determinacy. The source does not assume prior multivariate representability.
- The PDF used by the author is byte-identical to the retained diffusive-coercive-realizability copy, SHA-256 9e551b5856cdf1065f1170641bed91a1d0f40c1d19368c9187f0c3d16661ac94. No new local download is claimed.

## Schmüdgen textbook

K. Schmüdgen, *The Moment Problem* (2017), primary book text at https://www.imath.kiev.ua/~golub/ref2/The-Moment-Problem.pdf .

Reread the full parsed Proposition 13.4–13.5 passage and proof, printed pp. 318–319, plus the statement of Hamburger Theorem 3.8, printed p. 63. Proposition 13.5 supplies a full square-positive nonmoment functional, normalized at 1, and gives the value −1 on p₁=1+u⁴v²+u²v⁴−u²v². Proposition 13.4 gives its nonnegativity. The infinite functional and its positivity proof remain imported classical mathematics; no full coordinate implementation is claimed. Theorem 3.8 supplies the isolated d=1, r=0 existence case without interpreting Theorem 25 vacuously. Book PDF screenshot retrieval failed, so no visual book-page verification is claimed.

## Inherited project proof dependencies

- Read tensor-realizability-extension-20261010/RESULT.md, especially §§2–6: joint-square factorial estimates, one-positive-time representative exhaustion, exact noncoercive law equivalence, and coercive determinacy.
- Read moment-evolution-source-comparison-20261010/RESULT.md §3 and its SOURCE_MANIFEST.json and READING_BOUNDARIES.md. Its nonmoment-functional dependence was expressly inherited from the coercive packet; its manifest records other heat/PDE sources, not a retained textbook PDF.
- Read coercive-square-positivity-20261010/SOURCE_CHECKS.md and the nonmoment discussion in its RESULT.md. These already cite Proposition 13.5 and Hamburger/Haviland.

The review independently checks their application to partial quadratic damping. It does not replace the classical representation theorems with finite control output.

## Historical exclusion guard

Read lean-truncated-moment-obstruction-20261010/Controls.lean and RESULT.md, plus polynomial-moment-certificate-independent-review-20261010/RESULT.md and its seal. They establish the specified zero continuation’s failure at (x³−x)², value −96. Exact copies are recorded in HISTORICAL_EXCLUSION_BINDINGS.json. This is a scope exclusion; the rank proof imports the separate classical full-functional R² counterexample. No fresh Lean compilation or broad revalidation of the historical packet is claimed.
