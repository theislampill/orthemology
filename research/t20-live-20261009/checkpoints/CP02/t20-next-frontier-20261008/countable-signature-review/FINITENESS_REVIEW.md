# Finitude: infinite aliases and a conditional restriction certificate

8 October 2026. This extends the model for the purpose of testing the finite theorem's boundary. It does not infer actual infinite agents or an infinite physical actuator from the arithmetic construction.

## An infinite positive-product alias

Let f_e=1-4^(-e), fix E>=1 and target q=f_E. Begin with Q_E=1. For e>E, choose the largest integer n_e>=0 with Q_(e-1)f_e^n_e>=q. The next additional copy would cross below q, so

    q <= Q_e < q/f_e,
    0 <= Q_e-q < q/(4^e-1).

Thus the finite prefixes converge to q with an explicit computable error bound. No prefix equals q: a finite equality would contradict the proved finite multiplicative independence, since every prefix uses only exponents greater than E. Infinitely many n_e are consequently nonzero.

The digits satisfy n_e<=4. For t=4^(-e)<=1/16, (1-t)^5<=1-5t+10t²<1-4t, hence f_e^5<f_(e-1). Together with the preceding greedy remainder bound, five copies would already overshoot. Therefore the sum of route-success probabilities is at most 4·sum_(e>E)4^(-e), which is finite. This is a positive infinite product, not a zero-probability saturation trick.

Under the expanded countable independent-route law, its no-effect probability is exactly q. A single finite-model decoder applied to that rational returns a finite candidate but does not prove that the actual expanded-model inventory is finite. Real convergence does not preserve rational prime valuations: every added base-4 factor contributes a positive 3-adic numerator valuation, while the real limit f_E has fixed finite valuations.

The independent code checks finite prefix bounds through e=40 for E=1. It never labels a finite prefix as the infinite model or infers the general limit solely from numerical convergence.

## Sound second-profile certificate

Suppose the full-profile oracle supplies a positive exact rational q that has a finite candidate H. Let R0 be the finite union of H's positive supports. Obtain the response q_R0 when only R0 is issued, keeping those ports' calibration unchanged.

Assume the expanded model is unguarded, every route has a nonempty finite positive support, route successes have the specified independent law, and every route affects the absence event being compared. In the present single-effect model every route emits that designated effect. For a multi-effect reformulation, comparing no output anywhere in a complete catalogue would provide the corresponding visibility condition. Merely emitting some nonempty output is insufficient if the compared query omits it.

If any actual route touches outside R0, its success probability s is strictly positive and its failure is independent of the inside no-effect event. Thus q_full<=q_R0(1-s)<q_R0 whenever q_full=q_R0>0. Exact equality excludes all outside-support routes.

There are only finitely many nonempty support types inside R0. Infinitely many remaining independent occurrences would give some support infinite multiplicity; its fixed failure factor is below one, forcing q_R0=0. Positivity therefore makes the actual inventory finite. The finite theorem then identifies it with H.

Finiteness of each route's support, positive success factors, independence, correct occurrence aliasing and visibility are all load-bearing. If q=1, the unguarded model already has no routes: any route would make the full absence probability strictly smaller than one. The second query is redundant in that degenerate case; no minimal two-query claim is made.

The certificate concerns the route inventory affecting the compared output. It does not prove that the port alphabet, the set of existing beings, or the set of merely capable but unused agents is finite. Unused ports remain outside the recovered productive histogram.

## Guard semantics defeat an unqualified extension

For the greedy mimic of f_E, every support code exceeds E and cannot be a subset of the binary support P0 of E. Restricting the issued profile to P0 therefore disables the whole tail and gives q_P0=1.

Now add a route supported by P0 with an absence guard at an index outside P0. It is disabled at the full profile and enabled when only P0 is issued. The full-profile infinite tail and the restricted-profile guarded route both give f_E. The two responses agree although infinitely many tail routes are enabled in the full profile.

This counterexample changes the issued profile and reevaluates guards. Merely setting outside incidence rates to zero while keeping all ports issued would leave that guarded route disabled and would be a different intervention. Arbitrarily many dormant guarded routes can also remain invisible at both profiles. The certificate thus cannot become a general guarded census theorem.

## Precision and oracle qualification

No fixed positive near-equality tolerance works uniformly over unbounded indices. Taking E=2^i makes the restriction gap between a finite candidate and its infinite mimic equal to 4^(-2^i). Finite empirical frequencies do not become exact population comparisons.

A stronger necessity claim about an exact second measurement would be unwarranted. If q_full=q_H is already exact and R0 is fixed, q_R0>=q_H implies finitely many possible inside histograms: with f_max<1 the largest inside failure factor, q_R0<=f_max^N bounds their route count N. Their possible rational responses form a finite set, with a candidate-dependent positive gap above q_H. In principle a sufficiently narrow warranted error interval for the second response could establish equality using that extra gap argument. Ordinary samples would support only the corresponding confidence statement. This does not give a uniform tolerance or rescue approximate access to both readouts without additional restrictions.

The protocol presumes a supplied exact rational full response and a verified finite candidate. It is not a decision procedure for rationality of arbitrary real infinite products, and the comparison function does not authenticate that supplied numbers came from the specified profiles. Model-to-world and source-level admissibility remain external.
