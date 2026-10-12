# Independent review: pointwise-coercive changing gradients can escape

11 October 2026 UTC. Bounded independent mathematical review and exact controls. This is a negative continuation result, not a contradiction to the accepted common-energy theorem. All prior accepted packets remain unchanged.

## Verdict and frozen identity

PASS for `pointwise-coercive-gradient-escape-20261011/RESULT.md`, SHA256 `9190c25f200015ddd421e589cd39342a3fd8676487ee167b9815174736d29ffd`, with author manifest SHA256 `dc79e713fed0aed901152b7c8fad0c4dd0e73acf2db3279d3e35728fb7e78ac9`.

The exact target is valid: pointwise coercivity of every frozen potential, even with smooth time coefficients in a uniformly bounded polynomial degree, does not imply forward continuation of the changing-gradient flow through a prescribed finite endpoint. The counterexample does not satisfy a uniform common coercive control or a uniform lower killing bound through that endpoint. It does not refute any theorem that requires those guards or finite continuous endpoint moments.

The frozen proof and checker were inspected. Fresh isolated replay reproduces the 43 author checks and passes 50 independently written controls. The complete author snapshot and six original/copied inherited inputs remain unchanged. Full execution details and bindings are in REPLAY_RESULTS.json and REVIEW_RECEIPT.json. These finite controls supplement the written coercivity, uniqueness and Gronwall arguments; they are not a proof-kernel certification.

## 1. Exact orbit and coercivity

With s=1−t, the specified drift is exactly −∂xV_t, and substituting X=s^(−2) gives b_t(X)=2s^(−3)=X′. Its initial value is 1. An independent scaled-coordinate check sets Y=s²X and obtains

    Y′=Y(Y−1)[1+(2−Y)/s].

Thus Y=1 is invariant, recovering the proposed orbit by a different exact calculation. Local uniqueness holds because the time-polynomial drift is locally Lipschitz in x. The orbit tends to +∞ at t=1, so no finite continuous ODE extension through that time exists.

For every t<1, the quartic leading coefficient s³/4 is positive. Hence each frozen V_t is coercive on both spatial tails. At t=1 the cubic and quartic terms vanish and V_1=x²/2 remains coercive. The family is polynomial in time with a common degree-at-most-four basis; a drop in actual degree at the endpoint does not violate either property.

Each frozen autonomous negative-gradient ODE is forward complete by its own fixed-energy compact sublevel. Those compact sublevels depend on the frozen time, and no common compact trapping set follows. This is precisely the step that cannot be transferred to a genuinely changing potential.

## 2. The rank-one hierarchy exists until escape

Evaluation L_t(p)=p(X(t)) is normalized and positive on every polynomial square. Its moments s^(−2n) are finite and smooth at all t<1, including right derivatives at zero and uniform regularity on each strictly shorter compact interval. Every nonempty Hankel truncation is an outer product, and the mass is nonzero; the full Hankel rank is exactly one.

The selection covariance vanishes identically for a Dirac law, so the ordinary characteristic derivative gives every polynomial hierarchy equation. This is an actual represented path, not merely a finite moment construction. Normalizing the selection weight does not change its location or prevent escape.

The first moment diverges at t=1. Therefore no finite coordinatewise-continuous polynomial functional, and hence no C¹ hierarchy, can extend this path to that endpoint. The probability laws are not tight near t=1 and have no weak probability limit on R. Their integrals against compactly supported continuous functions tend to zero, which is a vague zero limit, not a mass-one law. No endpoint reset or probability at infinity is part of the theorem.

## 3. Energy decrease and the external-work sign

The independent calculations give the factored forms

    V_t(X_t)=(2s−9)/(12s⁵),
    d[V_t(X_t)]/dt=(8s−45)/(12s⁶),
    (∂tV_t)(X_t)=(8s+3)/(12s⁶),
    |∂xV_t(X_t)|²=4/s⁶.

For 0<s≤1 the first two quantities are negative and the third is positive. The moving energy therefore decreases strictly to −∞, while its explicit external-work term partially offsets a larger negative gradient-square contribution. The full chain rule is correct. It would be false to omit ∂tV or to explain the escape by claiming that this external-work term is negative.

As an additional separating control, the independent checker verifies V_0(X_t)→+∞ even while V_t(X_t)→−∞. Thus decreasing moving energy does not trap the trajectory in a sublevel of the initial fixed potential. The individually finite lower bounds of the frozen potentials are not uniform in time. Smooth coefficient convergence on compact spatial sets is compatible with the relevant negative-energy regions moving outward without bound.

The integrated killing J(t)=19/144+s^(−3)/18−3s^(−4)/16 has the correct derivative and zero initial value, and tends to −∞. Consequently the unnormalized Dirac mass tends to +∞; it remains finite and strictly positive at every t<1. Its normalized law is still the escaping Dirac. This is consistent with the failure of a uniform lower killing bound and does not supply a finite endpoint normalization.

## 4. The common-control obstruction is genuinely universal

Suppose H is any fixed nonnegative coercive C¹ function, not necessarily polynomial, and b_tH′≤CH with finite C for all x and t<1. The chain rule along the exact orbit and Gronwall give

    H(X_t)≤e^(Ct)H(1).

The right side is bounded on the finite time interval. Coercivity and X_t→∞ force the left side to diverge, a contradiction. This argument also covers H(1)=0 without division. It excludes all such C¹ controls; it is not an unsuccessful SOS search or an inference from finitely many polynomial candidates. A time-dependent coefficient with finite integrable Gronwall exponent gives the same contradiction.

For illustration only, the independent checks derive b_tH′/H along the orbit for H=1+x^(2m), m=1,2,3, as 4m/[s(1+s^(4m))], which diverges. These finite examples are supplementary and are not the proof of the universal C¹ assertion.

Likewise a uniform V_t+D≥κH with finite D, κ>0 and H≥0 is impossible because the left side tends to −∞ along the orbit. Thus both ingredients of the accepted common-energy guard fail for the endpoint window. Their possible validity with constants deteriorating on shorter windows [0,T], T<1, would not imply continuation through 1.

## 5. Scope, ancestry and evidence limits

The author correctly distinguishes this example from the earlier autonomous transport escape/rank-changing construction. Here every frozen drift is the gradient of a coercive potential, the actual pre-endpoint rank stays one, and moments diverge rather than being smoothly glued through escape. The autonomous completeness argument, pure-killing uniform-domination theorem and nonautonomous common-energy theorem keep their original scopes.

The review inspected the exact formula and all claimed identities, the full normalized hierarchy, the endpoint topology, and the common-control contradiction independently. The parent-supplied formula and the author's bounded local deduplication are acknowledged. Neither the parent's participating computations nor the local scan are treated as an independent review or a field-priority result.

No new external analytic theorem is imported beyond elementary local ODE existence/uniqueness, fixed-potential energy trapping and Gronwall, whose hypotheses and use are explicit. The packaged predecessor reports establish the ancestry and the exact theorem boundaries; no new raw primary-source archive is claimed. The existing nonautonomous review verifier was re-run without changing its accepted bytes.

The result does not deny positive-time representation of the displayed path, initial-law uniqueness for that path, frozen autonomous completeness, continuation under the stated common certificates, or a theorem assuming finite endpoint moment continuity. It establishes only the failure of continuation inferred from pointwise frozen coercivity and smooth time-polynomial coefficients. There is no formal-kernel verification, protected integration, empirical/noetic identification, finite-data detector, priority determination or T20 closure.
