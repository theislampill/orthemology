# Independent review: changing polynomial objectives under uniform SOS domination

10 October 2026 UTC. Ordinary mathematical review, additive to the unchanged autonomous packets. No formal-kernel, empirical, canonical-integration, field-priority, or closure certification is supplied.

## 1. Verdict and binding

**PASS under the exact hypotheses stated in Theorem V. No substantive gap was found and no mathematical correction was requested.** The proof repairs the moving-objective interface through first-derivative inequalities and weak measure evolution, rather than assuming that the autonomous even-derivative argument still applies.

Reviewed final candidate: `time-varying-square-positivity-20261010/RESULT.md`.

    SHA-256: 7ffed76cdfb23ee725bd4030c22dd03bb1f66934d885a6800caf260fdb0741bd

The final version is copied byte-for-byte in `author-snapshot/RESULT.md`. The whole mathematical draft was read before this verdict. The only later change records the executed control count. The reviewer independently reconstructed the proposed route before reading the draft, then checked each transition in the written proof. This is not blind review or machine-checked proof.

## 2. Exact hypotheses and the first-derivative repair

The local-window hypotheses are sufficient and are used at the necessary places:

- A common finite polynomial degree and continuous coefficients on every closed window beginning at zero give bounded coefficients and continuous polynomial evaluations.
- Uniform c>0 and C≥0 with h_t+C−c|x|² SOS give algebraic inequalities before representation.
- No continuity, computability, or fixed number of squares in an SOS decomposition is needed.
- Coordinatewise C¹ moment paths supply the first derivatives and boundary continuity actually used. No derivative of h_t is assumed.

For the fixed window, g_t=h_t+C is itself SOS and pointwise nonnegative. Unnormalization is valid because t↦L_t(g_t) is a continuous finite sum. The quantities a_n=A_t(R^n), R=|x|², are nonnegative. Multiplying the certificate by the SOS polynomial R^n gives

    a_n′≤−c a_(n+1)≤0.

This is a legitimate application of square positivity. It does not apply a merely square-positive functional to an arbitrary nonnegative polynomial.

Reversing time gives b_n′≥c b_(n+1). Repeated integration retains the successive initial terms, and the terminal integral is bounded below using monotonicity of b_N. Thus the proof obtains the full partial-sum inequality

    Σ_(n=0)^N (cδ)^n a_n(s)/n!≤a_0(s−δ).

The inequality requires only first derivatives, despite the arbitrary index n. Taking δ=s is justified by one-sided C¹ regularity and continuity at zero. No higher time derivatives of the objective are hidden in this step.

## 3. Gaussian growth and measure existence

The polynomial R^n−x_i^(2n) is SOS by its multinomial expansion. The resulting factorial even-coordinate bound makes every marginal Carleman series diverge. Full square positivity therefore meets the classical Nussbaum–Carleman existence theorem's premises; it is not merely a determinacy theorem applied to an assumed vector law.

At every positive time, the representing finite measure ν_s is unique. The bound

    ∫exp(csR)dν_s≤1

is also correct **at the endpoint rate cs**. This stronger claim follows from the full partial-sum inequality and monotone convergence. Individual bounds a_n(s)≤n!/(cs)^n alone would establish only smaller exponential rates, so retaining the full sum matters.

On an interior time interval [η,H′], a single rate r=cη gives uniform Gaussian integrability and bounded masses. Cauchy–Schwarz plus the radial moments gives the stated bound ∫|x|^k dν_t≤sqrt(k!)r^(−k/2). There is no Gaussian assumption on the initial moment record.

## 4. Fourier continuation: order of limits and complex tests

Complex-linearly extending a real polynomial functional is harmless: the real and imaginary polynomial identities hold separately. The real-variable remainder for exp(iy) gives the claimed error for each fixed frequency ξ.

The common degree D and bounded coefficients control |g_t(x)| by B(1+|x|^D). The Gaussian radial bounds therefore control both the polynomial Fourier approximation and its g_t-weighted derivative approximation uniformly in time. The weighted error's consecutive-term ratio tends to zero exactly as stated. This works with continuous objective coefficients; their time derivatives are not involved.

Uniform convergence of functions and first derivatives proves F′_t(ξ)=−G_t(ξ). It also gives joint continuity on compact time-frequency sets directly from moment expressions. No measurability or continuity of an arbitrarily selected representing-measure family is assumed.

The order of operations is correct and important:

1. Obtain the exact Fourier identity at each fixed frequency using the Gaussian estimate.
2. Only then integrate that identity against the Fourier transform of a compact smooth test.

The final Fourier integrands are bounded by mass and ∫g_t dν_t, independently of ξ. These bounds are uniformly finite in time. Consequently an integrable Fourier transform suffices for inversion, Fubini, and dominated differentiation. The proof does not try to dominate a Gaussian-in-frequency Taylor bound by a merely Schwartz Fourier transform.

## 5. Weak reaction equation and compact integrating factor

The resulting fixed-test identity for every φ∈C_c∞ is a proved weak reaction equation. Its right side is continuous.

The time-dependent test rule is valid by the stated difference-quotient splitting. For the part changing ψ, uniform differentiation on the common support and bounded masses control the approximation, while continuity for the fixed test ∂_tψ_t gives the limit. For the part changing ν, the fixed-test weak equation applies to ψ_t. This requires no general measurable-kernel theorem.

The chosen test ψ_u=φ exp(∫_s^u g_vdv) has fixed compact support. Continuous finite-degree coefficients make it C¹ in time in the uniform norm, with compact smooth spatial derivative g_uψ_u. All needed spatial derivatives are bounded on that support and time interval. The apparently unbounded integrating factor therefore causes no admissibility problem in this step.

Equality against every compact smooth test identifies the locally finite positive measures

    exp(∫_s^t g_u du)ν_t=ν_s.

Since the identified right side is finite, this also establishes global finiteness of the inverse-weighted measure. It is not assumed beforehand. Rewriting gives the actual law-level reaction update in both directions.

## 6. Initial recovery, uniqueness, and future schedule

Only after actual measure equality has been obtained does the proof use unbounded square observables in the boundary passage. Because g_u≥0, the inverse weights increase as the earlier time decreases to zero. Monotone convergence and coordinate continuity give both initial mass one and every initial square moment.

Polarization and |p|≤(1+p²)/2 provide signed and absolute moments. Thus the recovered initial object is a probability with all polynomial moments, rather than an infinite measure or an assumed initial representative.

Positive-time determinacy identifies any two normalized tilted laws giving the same full path. Undoing the known positive likelihood and renormalizing identifies their initial laws. This also shows that different finite-window choices of C,c recover the same μ on overlaps.

For the converse, the uniform lower bound gives exp(−H_t)≤exp(CH) on a finite window. Bounded polynomial coefficients then give an integrable polynomial bound for time derivatives, including at zero. Dominated differentiation supplies the promised C¹ hierarchy for every initial law with all moments. Consequently the initial-moment-fibre/path correspondence is established, while initial moment indeterminacy can still yield several paths.

Continuation beyond a finite horizon is correctly conditional on a supplied future objective family satisfying the same hypotheses. The recovered law cannot determine an unspecified future objective schedule.

## 7. Countercontrol and scope limits

The moving-centre SOS identity is correct, and compact-window bounds cover continuous centres. Continuous positive-definite quadratic shapes similarly have a positive uniform eigenvalue bound on each compact window. Higher-degree objectives are covered only when the explicit uniform certificate holds.

The negative-even-derivative example remains valid even with the proof's particular admissible shift. With C=1/25, t=1/10, and atoms −1 and 0, an independent rational calculation gives respectively

    −51/80 and −79/400.

Both are strictly negative, while the atom weights are positive. Thus the repair does not claim to restore the old even-time-derivative sign argument. Its radial first-derivative inequalities are genuinely different.

The theorem does not cover arbitrary time-varying coercive polynomials merely because each frozen objective is coercive. In particular, the previous autonomous arbitrary-coercive theorem and this moving SOS-domination theorem have different hypotheses. Neither a finite collection of square tests nor scalar energy data replaces the full polynomial-square assumptions.

## 8. Classical input and executed evidence

The Nussbaum–Carleman input was independently inspected in [Putinar–Schmüdgen, Multivariate Determinateness](https://arxiv.org/pdf/0810.0840), Theorem 25 and its following attribution, printed p. 24, during the preceding review. It supplies existence and uniqueness from full positive semidefiniteness and all marginal Carleman conditions. The remaining analytic inputs are standard Taylor remainder, Fourier inversion, dominated convergence, and measure identification; the application-specific approximation and test arguments are explicit in the candidate.

- Fresh isolated author replay: **23 exact checks passed**, including 5 integrity checks.
- Independent reviewer controls: **36 exact checks passed**, including 10 original/copy integrity comparisons.
- The independent mathematical controls include full positive backward sums, a genuinely changing quartic objective, signed polynomial evolution, radial SOS slack, integrating-factor cancellation, Fourier-ratio decay, a continuous coefficient whose derivative jumps, and the two exact shifted negative signs.
- Both older autonomous author receipts were completely revalidated against their unchanged original files. This successor's author receipt was also revalidated.

The candidate checker was executed only in the separate review snapshot. No old result or author candidate was edited. All new review evidence is confined to this additive directory and bound by `REVIEW_RECEIPT.json`.

The finite controls supplement the ordinary universal proof review. They neither establish the representation theorem by sampling nor implement a general measure reconstruction. No formal proof kernel, empirical source, noetic identification, epistemic warrant, or metaphysical conclusion is certified.
