# Independent supplemental review: quartic variance continuation

Accepted as a separate bounded mathematical diagnostic. The reviewed root RESULT.md has SHA256 0733507b41f874411d01590d337cbb2911351e3c708443029b85b23c5446d251. No files in the frozen Gaussian geometry packet or its accepted review were altered.

## Independent calculation from the actual law

Fix initial law N(0,v), v>0, and F(x)=x^4/4. Put d=1+2tx². The exact transport characteristic and its accumulated reaction factor are

X_t=x/sqrt(d),   w_t=exp[-t x^4/(4d)],   t≥0.

The characteristic satisfies X_t′=-X_t³, and the exponent derivative is X_t⁴/4. Normalizing the weighted pushforward therefore gives the stated centered transport/reaction evolution. Symmetry persists because X_t is odd and w_t is even.

Let Z(t)=E[w_t] and N(t)=E[X_t²w_t], so the true variance is V(t)=N(t)/Z(t). Direct derivatives at zero give

w_0′=-x⁴/4,
w_0″=x⁶+x⁸/16,
(X_t²w_t)′|_0=-2x⁴-x⁶/4,
(X_t²w_t)″|_0=8x⁶+2x⁸+x¹⁰/16.

Using centered Gaussian moments and differentiating the quotient yields

V′(0)=-6v²-3v³,
V″(0)=120v³+186v⁴+48v⁵.

This calculation is independent of the root checker's differentiation of the moment hierarchy. That hierarchy is also correct: M_k′=-k M_(k+2)-(M_(k+4)-M_k M_4)/4. Its k=2,4,6 cases produce the same result.

For the restricted Gaussian ODE V_G′=f(V_G), f(v)=-6v²-3v³, differentiation gives

V_G″(0)=f′(v)f(v)=72v³+90v⁴+27v⁵.

Hence

V″(0)-V_G″(0)=3v³(v+4)(7v+4)>0.

At v=1 this is 165, and the leading variance separation coefficient is 165/2.

## Analytic right-time justification

These are derivatives of actual normalized laws. Only right-hand regularity at t=0 is needed or claimed. For t≥0, d≥1 and 0<w_t≤1. If A=t x⁴/(4d), then

A′=x⁴/(4d²),   A″=-x⁶/d³,

so |w_t′|≤|x|⁴/4 and |w_t″|≤|x|⁸/16+|x|⁶. The factor X_t²=x²/d and its first two derivatives are bounded in absolute value by |x|², 2|x|⁴ and 8|x|⁶, respectively. Product differentiation consequently bounds the weighted second-moment derivatives by fixed polynomials through degree ten. All such bounds are Gaussian-integrable.

Dominated differentiation and dominated continuity prove that N and Z are right-C² at zero and C² on a small closed forward interval. Since Z(0)=1, continuity bounds Z away from zero there, so V=N/Z has the same regularity. The restricted ODE is smooth locally at every v>0. Right Taylor expansion gives

V(t)-V_G(t)=(3/2)v³(v+4)(7v+4)t²+o(t²).

For each fixed v>0 there is therefore an epsilon(v)>0 such that V(t)>V_G(t) for every 0<t<epsilon(v). No uniform epsilon over all variances, backward Gaussian flow, or large-time comparison is asserted.

## Checker history and verification

The original checker was replayed and returned its expected exit code 1. Its JSON exactly matches the preserved failure record, with only `positive_gap_factor` false. The corrected checker returned exit code 0 and exactly matches the recorded five-check pass. The mathematical `values` objects are identical in both runs. The sole source change replaces structural equality of differently factored expressions with zero testing of their expanded polynomial difference.

This is a checker-expression defect, not a mathematical counterexample. The original source, failing JSON, and newly captured failure stderr remain preserved. The root also retained the report and manifest from before the right-time clarification. The independent weighted-characteristic suite passes 12 checks. Finite symbolic checks corroborate the analytic argument; they are not a substitute for it.

## Scope

The diagnostic strengthens the existing nonzero fourth-Hermite residual by showing a genuine first observable variance discrepancy at second order in time. It leaves the exact quadratic Gaussian invariance result intact. It neither rules out approximation nor extends the inherited geometry claims. There are no mathematical findings requiring repair, and no project or audit closure is inferred.

Replay the independent suite with `python3 independent_check.py` using SymPy. The separate root suite is `python3 ../gaussian-quartic-variance-root-20261011/check.py`. Initial failure replay is deliberately nonzero and must not be represented as an unexpected current test failure.
