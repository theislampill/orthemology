# A route-specific-marginal alias for the same finite panel

8 October 2026 UTC. Separate prospective scratch addendum. This does not alter the frozen finite-panel-replay/RESULT.md, whose SHA256 is

    327b6fb25944ac90e7ecd6010a427993b69400fbdc9b79928d731120b6d62243

## 1. Result

The common-across-routes marginal-calibration premise is substantive. If that premise is dropped, even the specific four-probability panel in RESULT.md admits a larger-count alternative with genuine fixed threshold couplings, coordinate-only homeomorphic calibrations, and mutual independence between all route occurrences.

Fix n>=1 and t=1/[3(n+1)]. Replace each of the n reference routes by two independent routes, so the new count is m=2n. At the tested coordinate t, prescribe the following two valid Bernoulli tables, in 11,10,01,00 order:

    Type I:  (t^2, 0, 0, 1-t^2).
    Type II: (0, t/(1+t), t/(1+t), (1-t)/(1+t)).

All cells are nonnegative and each table sums to one. The common A/B marginal within Type I is t^2; within Type II it is t/(1+t). These values differ at the low t used by the certificate. Marginals are therefore shared within each type but not across all route occurrences.

For one Type I/Type II pair, the A-face absence product, and identically the B-face absence product, is

    (1-t^2) [1-t/(1+t)] = (1-t^2)/(1+t) = 1-t.

The fresh diagonal absence product is

    (1-t^2)(1-0) = 1-t^2.

The same-gate paired-face absence product is

    (1-t^2) [(1-t)/(1+t)] = (1-t)^2.

Take n mutually independent copies of this pair, with independence also between the two members of each pair. Raising these three products to the n-th power gives exactly all four reference probabilities in RESULT.md. Thus the same panel has an m=2n alias when route-specific marginal calibrations are allowed.

## 2. Concrete fixed-threshold realization

For any 0<t<1 and 0<w<1, define the endpoint-preserving piecewise-linear homeomorphism

    g_(t,w)(z) = w z/t,                         0<=z<=t,
               = w+(1-w)(z-t)/(1-t),           t<=z<=1.

Both slopes are strictly positive and the two pieces agree at t. Put

    g_I = g_(t,t^2),
    g_II = g_(t,t/(1+t)).

For every Type I route draw one uniform U on [0,1] and use

    A(a)=1{U<=g_I(a)},
    B(b)=1{U<=g_I(b)}.

This is the fixed comonotone coupling; the joint success is min(g_I(a),g_I(b)). At a=b=t it gives the Type I table.

For every Type II route draw one uniform V on [0,1] and use

    A(a)=1{V<=g_II(a)},
    B(b)=1{1-V<=g_II(b)}.

This is the fixed countermonotone coupling; the joint success is max(0,g_II(a)+g_II(b)-1). Since 2t/(1+t)<1, the diagonal joint success at t is zero, giving the Type II table.

Draw every U and V independently across all occurrences. Each gate depends pathwise only on its own command, each calibration is fixed and endpoint-preserving, and the very same U or V is retained across a paired replay. Thus no route-to-route dependence, gate resampling, state mutation, command cross-talk, random inventory, or endpoint failure is being used.

The panel agrees exactly, but the construction is not asserted to agree at untested commands. This is a sharp premise-isolation control for the finite certificate, not a global equivalence theorem.

## 3. Attribution and limits

During adversarial review, the reviewer independently supplied the clean general replacement construction above. The author had separately found a less simple numerical instance at n=1 and t=1/6. This addendum records the reviewer's stronger and simpler all-n version, with explicit homeomorphic threshold realization.

The result establishes the logical necessity of retaining a common-marginal restriction for this finite-panel theorem against the indicated enlarged class. It does not establish that this is the weakest possible sufficient restriction, invalidate the certificate under its declared hypotheses, or claim T20 closure, protected integration, empirical validation, or an elapsed research duration.
