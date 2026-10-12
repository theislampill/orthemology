# Separate sharpness corollary: tensoring the full nonmoment functional

10 October 2026 UTC. The parent proposed this tensor-product construction. The full strictly square-positive nonmoment functional is imported from the separately proved full-polynomial-moment-countermodel-20261010/PROOF.md, which retains its classical Friedrich/Schmüdgen dependencies and ordinary-versus-formal verification boundaries. It is not constructed or independently certified again here. The present corollary checks its tensor interaction with the supplied nonautonomous damping. This does not replace or modify the earlier Gaussian-mixture obstruction.

## S1. Statement

Fix r≥1 and any controlled-variable SOS schedule g_t(z), z∈R^r, satisfying GENERAL_SOS_BRIDGE.md. Let the hidden space have dimension k. Then:

- k=0: every full normalized square-positive hierarchy has one unique whole-path law lift and determinate positive-time full records, by the accepted full-dimensional cumulative theorem.
- k=1: every such hierarchy has a whole-path lift, but universal law identification fails, by RESULT.md and GENERAL_SOS_BRIDGE.md.
- k≥2: for this very supplied schedule there is a global-on-its-supplied-domain, normalized, coordinate-C¹, strictly square-positive hierarchy with no representing law at any time.

Thus the existence threshold remains exactly one hidden coordinate for this broader nonautonomous fixed-controlled-subspace class. The negative direction is schedule-by-schedule, and does not require a common zero of the energy. Among paths already known to have probability lifts, universal law identification still fails whenever k≥1 by the independent hidden Stieltjes pair.

## S2. Exact inherited full-functional input

Use a real functional Λ on R[u,v] satisfying

    Λ(1)=1,
    Λ(q²)>0 for every nonzero polynomial q,
    F(u,v)=1+u⁴v²+u²v⁴−u²v²≥3/4,
    Λ(F)=−1.                                      (37)

All values are finite. The bound input supplies Λ on the entire polynomial algebra by a specified infinite recurrence and ordinary universal proof. A finite moment prefix is not substituted for (37). No representing law for Λ is assumed or exists.

For k>2 write the remaining hidden coordinates as w∈R^(k−2). For k=2 omit w and its integration. Let γ_r and γ_(k−2) be full-support standard Gaussian probabilities. Put

    K_t(z)=∫₀ᵗg_s(z)ds,
    Z_t=∫e^(−K_t(z))dγ_r(z)>0,
    A_t(p)=∫∫Λ_(u,v)[p(z,u,v,w)]
                    e^(−K_t(z))dγ_r(z)dγ_(k−2)(w),
    L_t(p)=A_t(p)/Z_t.                            (38)

For a polynomial p, applying Λ to its finitely many hidden monomials leaves a genuine finite polynomial in (z,w). Hence the integrals are finite, because e^(−K_t)≤1 and Gaussian measures have every polynomial moment. Formula (38) is a tensor product of a positive polynomial functional and genuine measures, not an underlying joint probability construction.

## S3. Full square positivity, including strictness

For every fixed (z,w), q↦q(z,·,·,w) is a polynomial substitution. Thus

    Λ[p(z,·,·,w)²]≥0

by (37). Integrating against the positive weights gives A_t(p²)≥0.

If the joint polynomial p is nonzero, at least one coefficient in its expansion in u,v is a nonzero polynomial in (z,w). That coefficient is nonzero on a nonempty open set. At every point of that open set, p(z,·,·,w) is a nonzero polynomial, so strict positivity in (37) gives Λ[p(z,·,·,w)²]>0. The integrand is a continuous polynomial in (z,w), and the Gaussian factors times e^(−K_t) have positive density everywhere at every finite t. Its integral is strictly positive. Therefore

    L_t(p²)>0 for every nonzero joint polynomial p. (39)

Normalization follows from A_t(1)=Z_t.

## S4. The hierarchy and the all-time obstruction

On a compact time window, coefficient and degree bounds give a polynomial majorant for g_t(z). The derivative of the integrand in (38) is −g_t(z) times a fixed polynomial in (z,w), multiplied by e^(−K_t)≤1. Gaussian domination therefore gives continuous first derivatives through time zero and

    A_t′(p)=−A_t(g_t p),
    Z_t′=−A_t(g_t).

The quotient rule gives precisely

    L_t′(p)=−L_t(g_t p)+L_t(g_t)L_t(p).              (40)

Since F is independent of z,w and Λ(F)=−1,

    A_t(F)=−Z_t,   L_t(F)=−1                      (41)

at every time. But F≥3/4 everywhere in the full joint space. A positive representing probability would give L_t(F)≥3/4, contradicting (41). Thus the full hierarchy is forever nonmoment on the whole supplied time domain despite strict square positivity.

If a schedule has some time t at which g_t is a nonconstant polynomial, this path is nonstationary. Freeze the polynomial p=g_t at that t; the hierarchy and (39) give

    (d/du)L_u(p)|_(u=t)=−L_t((p−L_t(p))²)<0.

Cumulative radial coercivity with r≥1 guarantees that the energy is nonconstant at at least one time. This argument does not differentiate the time-varying energy itself and does not assume differentiable coefficients.

## S5. Boundaries

The full-functional premise (37) is essential. The nearby finite-degree nonmoment controls do not suffice and are not used. The tensor construction introduces no law for Λ, no hidden-coordinate tail hypothesis, and no zero-set requirement on the energy. It does not turn a signed or nonmoment functional into a probability law.

The result classifies automatic existence versus identification for the specified fixed controlled-variable SOS family. It does not cover energies coupling the controlled and hidden variables or a moving controlled subspace. Its ordinary proof and exact finite tensor controls do not constitute formalization of the imported infinite functional.
