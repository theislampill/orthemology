# Independent review of the partial nonautonomous whole-law bridge

10 October 2026 UTC. This is a separate ordinary mathematical assessment. The reviewer did not author the proof, does not modify the author packet, and makes no integration, formal-verification, or closure claim. The author confirmed the packet frozen before final assessment. All 15 frozen artifact entries were hash- and byte-verified; exact controls were replayed in a separate copy without changing the author packet.

## Verdict

PASS, ordinary mathematical review of the frozen stated scope. No blocking mathematical defect found in the complete proofs. There are no outstanding mathematical corrections. One attribution clarification was requested and incorporated: Putinar–Schmüdgen Theorem 31 assumes a strictly determinate base, whereas the present initial-time conditional argument uses the previously established equality of all signed projections and therefore does not assume initial-base strict determinacy.

## Positive theorem: independent checks

1. The finite cumulative bound follows from the backward fundamental-theorem-of-calculus expansion with an SOS remainder, using frozen energy polynomials at each step. Full square positivity is applied only to explicit SOS products. The argument does not substitute pointwise nonnegativity for SOS positivity and uses no infinite expansion before its convergence is established.
2. The active marginal factorial bounds yield Carleman in exactly d−1 coordinates. Theorem 25, printed p.24 of the retained arXiv:0810.0840v1 source, gives joint representability, not joint determinacy. I read that page's extracted text and inspected its retained image. The proof makes the correct restricted use of the theorem.
3. In the quadratic proof, the uniform weighted Gaussian estimate comes from applying monotonicity to the entire finite partial sum at an earlier interior time. The SOS product comparison gives the factorial bound needed to cancel the simplex volume. In the backward remainder the functional is evaluated at the latest simplex time; in the forward remainder it is evaluated at the earliest. Both displayed orderings are correct. Their geometric remainder estimates are local in time and are not applied to higher-degree energies.
4. The backward exponential identity uses a nonnegative series. The forward identity separately uses integrable absolute domination by q² exp(K). Thus neither direction is merely a formal power-series equality. The forward direction is essential for transporting an arbitrary earlier representative; the proof supplies it.
5. A finite partition of each compact positive-time interval uses one uniform pair of constants. Each propagated measure is again a representative, so the same uniform Gaussian estimate applies at the next step. This proves propagation of every chosen representative without identifying unrelated representatives. The monotone inverse-weight limit as time decreases to zero has the correct direction and recovers mass and every squared polynomial moment. Polarization plus squared integrability supplies all absolute polynomial moments.

## General SOS bridge: independent checks

1. Weighted variation of π_z*(y^j ν_t) is bounded using |y|^j ≤ (1+y^(2j))/2 and the weighted Gaussian bounds with q=1 and q=y^j. All these objects are finite signed measures. Active-space Gaussian tails determine their signed polynomial moments by absolutely dominated Fourier expansion. This makes each signed projection canonical without a measurable selection of joint laws.
2. The Fourier Taylor errors and their derivative errors have the stated factorial decay, including the fixed degree offset D. Local coefficient bounds supply a uniform polynomial majorant for g_t. Uniform convergence of functions and derivatives justifies the time derivative. Frequency-independent bounds justify Fourier inversion and dominated differentiation for compact smooth tests.
3. The time-dependent compact test product rule needs only the uniform variation bound, uniform differentiability of the test, and weak continuity against a frozen smooth compact test. These are all established. The compact integrating factor first gives equality of locally finite signed measures. Equality to the finite endpoint measure then proves global total-variation integrability of the inverse-weighted measure. No global inverse integrability is assumed in advance.
4. Reconstruction starts from one arbitrary joint representative. The even-hidden-power signed projections are positive, so the identities for R^m y^(2n) follow by positive integration and monotone convergence. They establish absolute and squared joint-polynomial integrability before signed mixed moments are transported. The subsequent signed projection identities are therefore legitimate. The zero-time argument again uses positive monotone convergence for q².
5. The converse is controlled by a polynomial Gaussian-free majorant under the initial P∞ law because exp(−K_t) ≤ 1 and coefficients/degrees are locally bounded. It gives coordinate C¹ regularity through zero with no time derivative of g required. The normalizer ODE proves the claimed fibre bijection.

## Identification, continuation, and examples

Equality of all finite signed initial projections is sufficient for equality along any of the stated controlled-variable schedules. Conversely, equality of a normalized full record at one positive time determines every active signed projection by Gaussian tails; inverse weighting is legal for the two known P∞ laws, and the j=0 mass equality fixes the normalizer. This establishes the exact equivalence and schedule-independent moment-coordinate continuation, without whole-law uniqueness.

The conditional-determinacy argument is sufficient only. It uses equality of Radon–Nikodym conditional moments, a countable union of null sets, and one-dimensional conditional determinacy. It makes no necessity or alternate-kernel measurable-selection claim. I read the retained continuous source text from §8, printed pp.29–31, including the hypotheses preceding Theorems 30–31. I did not re-inspect PDF images of those three pages.

The graph example is valid: equal m_0,m_1,m_2 give zero integral of (y−exp(z))² after verifying the cross term by Cauchy–Schwarz. The actual hidden marginal is lognormal and moment-indeterminate, while the joint law within the path's equivalence class is unique. The independent-hidden Stieltjes pair supplies genuine distinct full-support lifts. The active rank-one varying quadratic and quartic discriminator meet their respective hypotheses and demonstrate distinct scope boundaries.

## Sharpness addition

I read all of the imported full-polynomial-moment-countermodel-20261010/PROOF.md, rather than substituting finite-prefix calculations for its premise. Its specified infinite recurrence and universal induction do supply a normalized full-algebra functional Λ with strict square positivity and Λ(F)=−1 for an everywhere positive polynomial F.

Tensoring Λ with the Gaussian-killed active law is valid for every supplied controlled SOS schedule. Polynomial contraction is finite, Gaussian domination gives all coordinate derivatives, and positivity holds pointwise before integration. For a nonzero joint polynomial, at least one hidden-monomial coefficient is nonzero on an open set, so strict positivity survives integration against the everywhere positive active/extra-hidden Gaussian densities. The witness remains −1 at every time. The nonstationarity check freezes a nonconstant energy polynomial at one time and correctly uses strict variance positivity. This proves schedule-by-schedule failure of automatic representability with at least two hidden coordinates. The zero-hidden positive case remains an explicitly inherited result.

## Limits

This review concerns full commutative polynomial hierarchies, one fixed controlled subspace, SOS energies with cumulative active coercivity from zero at every positive time, and full coordinate C¹ paths. It does not certify finite truncations, a reconstruction algorithm, cross-hidden energies, moving controlled subspaces, an unspecified future schedule, formalization, field priority, or integration status. Exact finite controls are supporting checks of specific identities, not proofs of the universal analytic or full-functional claims.

## Frozen binding and executed controls

The author explicitly confirmed freeze on 10 October 2026 before this final review. Manifest SHA-256: e9df7038ce11766fec54df124a93c749f9044e6493ef87b7d0e16fe56dc668f5.

- RESULT.md: 047ec278a738cdc018b7118113afa93a8fa6d0aa1a315d33440f2aa0586a53ea
- GENERAL_SOS_BRIDGE.md: 9f20a6b0125b98a659d87b0a3758630b4e3ded99ba376e1bf4fbcc31d49765db
- SHARP_HIDDEN_BOUNDARY.md: 12d3e23f4f01f934cce554503368ccc2755ad8cef9055c432380f7b6271abd3f

The exact author script was inspected and then independently executed in review/replay with the source root explicitly fixed. At 2026-10-10T21:30:10.169996+00:00, Python 3.12.14 and SymPy 1.14.0 reported 615 checks passed, exit status 0. This is independent execution of the author's finite controls, not a claim to have independently authored their code. The replay's check names and pass results were compared with the frozen author results.

The controls cover distinct obligations: SOS telescoping; both finite Volterra orderings with wrong-endpoint countercontrols; factorial/simplex cancellation; weighted hidden-power domination; the varying rank-one Gram certificate and matrix noncommutation; genuine Gaussian reaction identities; Stieltjes cancellation and graph variance; failure of quadratic domination for the quartic example; and finite tensor hierarchy/strict-pivot/witness diagnostics for the sharpness construction. The count includes bounded instances within these families. The universal conclusions rest on the written arguments reviewed above, not the assertion count.

The original frozen manifest and all its entries were checked again after replay. No author artifact was modified by the review. No protected-source or integration target was edited.
