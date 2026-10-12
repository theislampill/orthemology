# Quartic variance: matching the first derivative does not give exact continuation

11 October 2026 UTC. Root participating written calculation with five exact symbolic checks. Separate from the frozen Gaussian geometry report; no independent acceptance yet.

Take F(x)=x^4/4 and initial law N(0,v), v>0. The full normalized gradient/killing law remains symmetric. Its variance is therefore m2. For raw moments the exact identities are

    m2' = -2m4 -(m6-m4 m2)/4,
    m4' = -4m6 -(m8-m4²)/4,
    m6' = -6m8 -(m10-m6 m4)/4.

At the initial Gaussian, substitute m2=v, m4=3v², m6=15v³, m8=105v⁴ and m10=945v⁵. The full and restricted Gaussian gradient models both have initial variance derivative

    f(v)=-6v²-3v³.

Differentiating the full moment identity before substituting Gaussian moments gives

    v_full''(0)=120v³+186v⁴+48v⁵.

Differentiating the Gaussian restricted ODE gives

    v_Gaussian''(0)=f'(v)f(v)=72v³+90v⁴+27v⁵.

Their difference is

    3v³(v+4)(7v+4)>0.

Hence v_full(t)-v_Gaussian(t) = (3/2)v³(v+4)(7v+4)t²+o(t²), strictly positive for every sufficiently small positive t. At v=1 the second-derivative difference is165; the leading variance error coefficient is165/2. The result concerns this exact declared operation and projection, not a general prohibition of approximation or Riemannian modelling.

The differentiations concern actual laws. The exact full characteristics are X_t=x/sqrt(1+2tx²), with weight exp[-t x⁴/(4(1+2tx²))]. For t≥0 the positions are bounded by |x| and the weights by1; near zero their first two time derivatives are bounded by fixed polynomials in |x|. Gaussian moments supply domination, and the positive normalizer stays away from zero on a small interval. Thus the displayed moment derivatives and the second-order expansion are legitimate. The restricted ODE has a smooth local solution at every v>0.

This supplies a concrete observable consequence beyond the nonzero fourth-Hermite density residual in the Gaussian geometry packet. Agreement on the first instantaneous mean/variance derivatives does not establish an invariant family. The exact quadratic invariance theorem is unchanged.

The first checker used structural equality for two differently factored equal polynomials and reported one false assertion. The original checker and receipt are retained in snapshots/. Replacing that check with an exact expanded polynomial equality makes all five checks pass; none of the mathematical expressions changed. This is a checker-expression correction, not suppression of a counterexample. These controls corroborate the written calculation, rather than establishing its analytic hypotheses by enumeration.
