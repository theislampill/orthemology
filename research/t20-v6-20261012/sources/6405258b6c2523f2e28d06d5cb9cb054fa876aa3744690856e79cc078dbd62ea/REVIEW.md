# Independent review: cumulative SOS coercivity

10 October 2026 UTC. Ordinary independent mathematical review. No field-priority, empirical, proof-kernel, protected-integration, audit-lifecycle, release, or closure authority is asserted.

## Disposition and exact scope

**PASS under the exact hypotheses of Theorem V_c. No unresolved substantive or presentation defect remains.** The whole proof, including its inherited polynomial-coordinate corollary, has been checked.

Final frozen candidate: `author-snapshot/RESULT.md`, SHA-256 `a530a5341497e3416345a7ec325e986a7e54f2c254954f80fd32f1f596e6244f`. It matches the current author source. The initial frozen candidate is retained in `inputs/candidate-RESULT.md`, SHA-256 `468dac5cdd3c4368c12cb7db2bb6cc7f5267b7dee8035d65911962e40042950d`. The exact two-change delta is preserved in `FINAL_DELTA.patch`: one compact-test smoothness clarification and a version-pinned source URL. The review receipt binds all evidence.

The reviewer received the proposed route from the parent, independently reconstructed its algebraic and analytic bridge before reading the candidate, and then read the entire frozen proof, accepted V, and the accepted polynomial-coordinate transport source. This is independent mathematical checking, not blind review. The parent and author developed the candidate; neither is treated as its independent reviewer.

The necessary hypotheses are full polynomial-square positivity, all polynomial moment equations with coordinatewise C1 regularity through zero, finite polynomial degree and continuous coefficients on compact time windows, an SOS scalar-shifted instantaneous rate, and an origin-to-every-positive-time cumulative SOS radial certificate. No representation, initial determinacy, initial Gaussian tail, differentiable rate, regular certificate selection, or instantaneous radial coercivity has been silently added.

## 1. Finite backward expansion, time order, and sign

The exact expansion is valid for every fixed finite order. Starting with the fundamental theorem of calculus for a fixed polynomial, each substitution freezes the previously chosen rate polynomials and moves from the latest existing time to a later time. Its residual is therefore evaluated at the **latest** simplex time:

    E_(N+1) = integral_(s≤u1≤...≤u_(N+1)≤t)
                 A_(u_(N+1))(q² g_(u1)...g_(u_(N+1))) du.

The degree and continuity assumptions suffice for each finite-dimensional integral and Fubini interchange. Products commute algebraically. Hence the terminal integrand is symmetric, and integration over ordered simplices produces exactly K_(s,t)^k/k!. The formula is not an unjustified time-ordered exponential or a higher-time-derivative expansion.

Every residual integrand is nonnegative because the product of SOS polynomials, multiplied by q², remains SOS. This requires no continuous choice of square factors. No initial or intermediate representing measure is used here. Nor is square positivity applied to an arbitrary merely nonnegative polynomial.

The candidate correctly retains the residual only by sign. It does not assert that the residual tends to zero or that the infinite Taylor series equals the initial functional.

An independent wrong-order control matters: for g=1, A_u(1)=e^(−u), s=0, t=1 and N=1, the correct latest-time residual gives the exact identity 1=2/e+(1−2/e). Replacing it by the earliest-time value gives 3/e, with nonzero error 3/e−1. Positivity alone would not detect that ordering mistake. The candidate has the correct order.

## 2. Cumulative radial control and existence without circularity

At any positive t, write K=cR+S, where c>0 and S is SOS. Both K and R are SOS, and K^n−c^nR^n is SOS by the finite difference-of-powers identity. Applying square positivity term by term to the finite Volterra inequality gives the full partial-sum estimate

    sum_(n=0)^N c^n A_t(q²R^n)/n! ≤ A_0(q²).

In particular the initial mass is one, so the q=1 bound supplies factorial radial moments. The multinomial SOS difference R^n−x_i^(2n) gives all marginal factorial moment bounds after division by the strictly positive unnormalizing mass a(t). Every marginal Carleman series diverges. The inspected Nussbaum–Carleman theorem then gives both existence and uniqueness of the positive-time joint measure. There is no use of a determinacy-only result to assume existence.

Once the measure exists, the full partial-sum estimate and monotone convergence give the Gaussian bound at the endpoint rate c, including its polynomial-square-weighted form. Merely individual factorial bounds would not suffice to infer integrability at that exact endpoint; the candidate correctly retains the whole sum.

## 3. Interior uniformity requires no regularity of c(t)

Each A_t(R^n) is nonincreasing because g_tR^n is SOS. Fixing one interior time η and taking its single certificate r=c_H(η)>0 therefore propagates the full Gaussian partial-sum bound to every later time in the compact window. This establishes a common Gaussian rate and a common mass bound before extending the moment dynamics to Fourier tests.

The argument never takes a minimum of c_H(t), assumes its measurability, or requires radial coercivity on every interior subinterval. A certificate at every positive origin-to-time interval suffices to reach every positive time and then propagate bounds forward.

An independent adversarial example checks this last distinction. Let g_t=(x+min(t,1)y)². For 0<t≤1 use the candidate's rank-one cumulative certificate. For t≥1,

    K_(0,t)−(x²+y²)/16
      = (15/16)(x+8y/15)² + y²/240 + (t−1)(x+y)².

Thus the theorem's hypotheses hold, although every interval [s,t] with s≥1 has only the rank-one integrated rate (t−s)(x+y)². The coefficient path is continuous and has a derivative jump at one. Both facts are permitted by the proof.

## 4. Fourier and compact-test identification

The inherited Fourier approximation argument remains valid with this weaker source of uniform Gaussian control. The degree bound controls multiplication by g_t. The real-variable exponential remainder gives uniform convergence of polynomial Fourier approximations and of their derivative-side approximations for each fixed frequency, uniformly also on compact frequency sets. The ratio of the weighted error terms tends to zero for each fixed polynomial degree. No analyticity in time or derivative of g_t is involved.

Uniform convergence of functions and first derivatives gives the Fourier evolution and joint time-frequency continuity. Thus no measurable family of arbitrarily selected measures is presumed. Only after the fixed-frequency identity is proved does the argument integrate against the Fourier transform of a compact smooth test. The final Fourier expressions have frequency-independent bounds by mass and A_t(g_t), so that inversion, Fubini and differentiation are justified. Integrating the frequency-growing Taylor error over all frequencies would be unsafe; the candidate does not do that.

The compact integrating factor has common compact support, uniform C1 time regularity, and smooth compact spatial time derivative. Therefore the time-dependent test rule applies. It identifies actual locally finite measures, not just polynomial moments. The inverse-weighted measure becomes globally finite because it is identified with an already finite measure.

### Minor clarification requested and resolved

In the initial candidate, the generic family test rule assumes spatial smoothness of each ψ_u and C1 regularity only in the uniform norm, but its proof invokes continuity against the fixed derivative ∂uψ_u as if that derivative were smooth. The derivative is certainly continuous and compactly supported, but need not be smooth under the stated generic assumptions. Either require the derivative to be smooth, as accepted V did, or extend weak continuity from compact smooth to compact continuous tests by uniform approximation and the already uniform mass bound. The actual exponential test already satisfies the stronger condition, so this is a presentation-level lemma gap, not a defect in the theorem or its actual application. The final candidate explicitly requires each spatial time derivative to be compact smooth. The reviewer checked this exact correction and verified that the actual integrating factor satisfies it. This resolves the issue without strengthening the theorem's hypotheses or changing its proof mechanism. The only other proof-file change pins the classical source URL to version v1, which was independently re-opened and inspected.

## 5. Boundary recovery, uniqueness, converse, and continuation

With the actual measure identity established, nonnegativity of g makes inverse weights increase as the earlier time decreases to zero. Monotone convergence and coordinate continuity recover initial mass one and every initial square moment. Absolute polynomial integrability and signed moments follow from the displayed elementary inequalities and polarization. No tightness shortcut, initial representative, finite mass assumption on an inverse tilt, or missing tail passage is hidden here.

Positive-time determinacy identifies any two normalized tilted laws with the same path. Undoing the known strictly positive likelihood and renormalizing identifies the initial laws. The same argument proves consistency of local scalar shifts and overlapping windows.

The converse is valid for every initial all-moment probability: the continuous scalar shift gives a uniform bound on the exponential over a finite time window, and bounded polynomial coefficients give integrable polynomial derivative majorants. Dominated differentiation establishes coordinatewise C1 regularity through zero. The fibre/path correspondence and unique extension along a supplied future schedule follow. There is no claim that the initial moment record is determinate or that an unspecified future energy can be inferred.

These Fourier, compact-test, boundary, and uniqueness arguments are inherited from V. They have been rechecked under the new hypotheses; they are not counted as new mathematical contributions.

## 6. Strict extension and the inclusion of V

For g_t=(x+ty)² the integrated Gram matrix has determinant t⁴/12 and trace t+t³/3. The candidate's rate c=t³/[4(t²+3)] and its explicit SOS decomposition are exact. At each instant, the ray λ(−t,1) makes g_t vanish while every positive radial term grows quadratically. No finite scalar shift can repair instantaneous radial coercivity. This establishes the claimed strict extension of V, rather than only a new proof of V.

The rotating trigonometric example also checks: its accumulated eigenvalues are (t±|sin t|)/2, positive for t>0, while each instantaneous matrix has rank one. No spectral statement about the actual probability law follows. A point mass still gives zero covariance and a constant normalized hierarchy.

The literal inclusion of V uses integration of fixed-degree SOS polynomials. The candidate supplies a valid finite-dimensional cone-closure proof: the unit-ball moment matrix of the monomial vector is positive definite; integrating an SOS polynomial bounds the trace, hence norm, of any positive-semidefinite Gram matrix; a convergent subsequence yields a Gram matrix for the coefficientwise limit. No continuous choice of Gram factors is required. This ancillary closure proof is not used in the main cumulative estimate or uniform-interior argument.

## 7. Inherited polynomial-coordinate transport

The supplied inverse polynomial paths preserve the polynomial algebra, square positivity, finite-degree regularity, and the finite-sum chain rule. Pullback cancels the transport term and gives the killing-only hierarchy. The cumulative certificate is correctly imposed in the pulled-back coordinates. The forward formula, converse, and determinacy of the original joint law then follow exactly as in the accepted transport packet.

The triangular example pulls its original rate back to (u+tz)², so the new cumulative theorem applies. The inverse flow is explicit and polynomial; no general polynomial-flow existence claim is made. The original-coordinate rate also has an unbounded zero curve y=t x^m−x/t for t>0, confirming failure of its own instantaneous radial certificate. The Gaussian claim is confined to the pulled-back coordinates, as required under nonlinear polynomial maps.

This transport mechanism is inherited. Its new applicability under cumulative damping is a conditional corollary, not a second newly discovered characteristic-transfer principle.

## 8. Executed controls and limits

The independent checker passed **55 exact checks**: the supplied accepted-V digest; cumulative rank-one Gram and explicit radial-slack identities; stopped-rotation and nonsmooth-time controls; ordered-simplex factorials through degree four; a latest-versus-earliest residual discriminator; changing-rate residual endpoint and derivative identities through order five; radial SOS power identities; fixed-degree Fourier-ratio limits; SOS multiplication; and triangular cumulative pullback/transport identities.

These finite exact checks supplement the ordinary whole-proof argument. They neither certify universal measure representation by examples nor implement a general reconstruction of an infinite moment sequence. A clean isolated replay of the author's checker also passed **118 exact checks**, comprising 89 algebraic controls, 14 copied/current input-integrity checks, and 15 predecessor-receipt checks. The author's 14-file receipt was independently revalidated in both the current source and the copied snapshot; the snapshot's replay output is byte-identical to the bound author output. The final receipt records these results and all frozen input/output hashes. No protected files or author files are edited by this reviewer.
