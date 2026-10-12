# Independent review: nonnegative-SOS moving-gradient escape

11 October 2026 UTC. Separate independent mathematical review of the root-authored stronger counterexample. The earlier signed-energy counterexample and accepted common-energy theorem remain unchanged.

## Verdict and frozen identity

PASS, with no unresolved mathematical findings, for `nonnegative-moving-gradient-escape-20261011/RESULT.md`, SHA256 `5bb21aa5aa388b3dff9a42cb48ad5e62a5b2c4da42971030a197caff583a980d`. The accepted manifest SHA256 is `6c38f26ec9573b8cb66951ca0aa3ffad447133515c6a51cc9aa4242e8fa293c4`.

One minor precision was corrected before this acceptance: the common-control argument now replaces a finite C by max(C,0) before bounding e^(Ct) by e^(CT). The previous proof bytes and manifest are retained in the author's immutable snapshot folder. The contradiction itself was otherwise valid; this review binds only the revised proof above.

The result genuinely strengthens the earlier example. Each frozen potential is nonnegative, SOS and coercive, with common minimum value zero; actual loss decreases to zero; the surviving unnormalized mass has a positive endpoint limit. Nonetheless the prescribed smooth changing-gradient trajectory escapes in finite time. It still does not refute a theorem retaining a uniform common coercive control.

Fresh isolated replay passes all 12 author controls and 42 independently written controls. All seven frozen author files and the three bound predecessor originals/copied review inputs remain unchanged. The portable replay and frozen receipt specify the exact evidence. Universal inverse-function, coercivity, ODE-uniqueness and Gronwall arguments are reviewed in writing, not purportedly proved by finite symbolic enumeration.

## 1. The schedule is smooth across the escape time

On 0≤s≤1/2, f(s)=1−5s⁵ satisfies 27/32≤f≤1. Consequently the defining integral has finite duration 1/2≤T≤16/27. Its derivative t′(s)=−1/f(s) never vanishes. The denominator remains positive on an open interval slightly larger than [0,1/2], so t(s) extends there as a smooth strictly monotone map. The inverse function theorem therefore supplies one smooth inverse s(t) on an open interval containing [0,T], including both endpoints. This is not merely one-sided regularity at T.

The inverse satisfies s′=−f(s), s(0)=1/2 and s(T)=0; in particular s′(T)=−1. It is positive for t<T. The schedule is specified independently of the state. Neither the vector field nor its coefficient family becomes singular at T; only the proposed solution 1/s does. The proof asserts smooth, not polynomial, time dependence. The common spatial basis is exactly x⁸,x⁹,x¹⁰.

## 2. Frozen coercivity, global minima and the actual trajectory

Writing a=s−s⁶, the potential is V=(x⁴−ax⁵)²/2. For 0<s≤1/2, a>0 and its degree-ten leading coefficient a²/2 is positive. It is therefore coercive on both spatial tails and is explicitly a sum of squares. At s=0 it reduces to x⁸/2, which is also nonnegative and coercive. The degree drop is compatible with the smooth coefficient family. Each frozen autonomous gradient is forward complete by its own compact energy sublevels.

For clarity, at t<T the global zero set contains both 0 and 1/a(t). The report correctly claims a common minimum at zero without claiming it is the unique minimizer before T. At T, x=0 is the only zero. This distinction matters: the additional zero branch moves to infinity.

Direct independent differentiation gives

    −∂xV = −x⁷(1−ax)(4−5ax).

At X=1/s, aX=1−s⁵ and x⁴−ax⁵=s, giving

    b_t(X)=f(s)/s² = X′,
    X(0)=2,
    V_t(X)=s²/2.

The field is smooth in time and locally Lipschitz in x. Local uniqueness makes X the actual solution from 2, not merely a compatible formal curve. It escapes to +∞ as t approaches the finite T; no finite continuous extension through T is possible.

The orbit is not itself a minimizer at any pre-endpoint time, since s²/2>0. Its loss does approach the global minimum value. An additional independent identity is

    1/a−X=s⁴/(1−s⁵)→0.

Thus it even approaches the moving zero branch in spatial distance while both points escape. This does not imply convergence to the common minimizer 0 or any finite minimizer of the endpoint objective. The result concerns attainment by the trajectory's limiting state, not existence of minima for the frozen objectives.

## 3. Energy accounting and fixed-objective comparisons

The displayed formulas check exactly:

    d[V_t(X)]/dt=−s f(s)<0,
    |∂xV_t(X)|²=f(s)²/s⁴,
    (∂tV_t)(X)=f(s)(1−6s⁵)/s⁴>0.

The last sign holds because 1−6s⁵≥13/16 on the stated range. The positive external-work term almost cancels the larger spatial gradient dissipation, leaving the negative total derivative. The proof neither drops that term nor misattributes escape to a negative time derivative.

The moving loss tends to zero, but the fixed endpoint objective evaluated on the same states is V_T(X)=1/(2s⁸), which tends to +∞. The fixed initial objective also tends to +∞ there. The time/state limits therefore cannot be interchanged, and decreasing moving loss is not a bound on any fixed initial or endpoint sublevel.

The orbit also rules out a uniform comparison V_t+D≥κH with any fixed nonnegative coercive H, finite D and κ>0: its left side stays bounded along X while H(X) diverges. In particular no fixed polynomial energy comparison of that form rescues the common-energy hypotheses. This is a direct consequence of the explicit orbit, not a failed certificate search.

## 4. Probability, killing and hierarchy

The actual law δ_(X(t)) defines a normalized full-square-positive polynomial functional. Every polynomial coordinate is finite and smooth on [0,T), with rank one. The reaction covariance vanishes for a Dirac law, so the ordinary chain rule proves the complete normalized hierarchy for arbitrary polynomial observables. The independent tests include a generic differentiable-observable identity rather than relying only on a finite monomial list.

The integrated killing is

    ∫₀ᵀ V_r(X_r)dr = ∫₀^(1/2) u²/[2f(u)]du.

It is finite and positive. The author's upper bound T/8 is valid because V_r(X_r)≤1/8. Independently, the speed bounds even give 1/48≤the integral≤2/81. No exact antiderivative is needed. Hence the unnormalized weight has a finite strictly positive endpoint limit and remains at most one. There is no negative killing, vanishing surviving mass or divergent normalization factor in this example.

A positive mass nevertheless escapes spatially. The first normalized moment 1/s diverges, so there is no finite coordinatewise-continuous moment extension to T. The Dirac probabilities are not tight and have no weak probability limit on R; compactly supported tests tend to zero while their masses remain one. The unnormalized laws similarly lose their positive surviving mass under vague spatial testing. This is a spatial-escape obstruction, not nonrepresentability of the pre-escape hierarchy.

## 5. No common coercive C¹ guard

The revised proof handles the sign of C correctly. Because H≥0, replacing C by max(C,0) preserves a proposed inequality b_tH′≤CH. Gronwall along the explicit orbit then gives H(X_t)≤e^(CT)H(2), with a bounded right side. Coercivity forces H(X_t)→∞, a contradiction. No division by H(2) is used, so a zero initial H value is covered.

This excludes every fixed nonnegative coercive C¹ H, whether polynomial, SOS-certified or neither. The independent quadratic-control ratio check, 2f(s)/[s(1+s²)]→∞ for H=1+x², is only supplementary. The universal conclusion rests on Gronwall, not that finite example.

Moving sublevels cannot be uniformly compact because they contain X_t with V_t(X_t)≤1/8. Pointwise frozen coercivity on the closed coefficient interval provides no uniform trapping set. This is the exact missing guard retained by the accepted nonautonomous theorem. A control with constants deteriorating on shorter intervals would not supply continuation through T.

## 6. Source, preservation and nonclaims

The parent authored the construction; this report and its independently written controls are the separate review. The three bound predecessor files are copied under the review's inputs directory for portable ancestry, and were checked against the unchanged originals. The author checker does not depend on those external workspace paths. The earlier signed-example and common-energy verifiers were re-run unchanged.

No new external theorem is needed beyond elementary smooth inversion, local ODE uniqueness, coercive fixed-energy trapping and Gronwall; their applicable hypotheses are explicit above. This is not an exhaustive literature or field-priority finding. It does not establish that every changing loss fails, that the retained common-energy certificate is necessary for every successful flow, or that frozen objectives lack minimizers. It asserts neither an empirical cognitive result nor a metaphysical interpretation. No protected integration, formal-kernel certification or T20 closure follows.
