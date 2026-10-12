# Separate verdict: affine transport plus killing

10 October 2026 UTC. Scope added explicitly by the parent after the heat review. Independent review of Section 4 of the stable comparison draft, SHA-256 c9170636819e8c10b3a94362bc446e5b4424b2a149079f4fc4b1eaeb339b30ac. The frozen Theorem V is used as an accepted dependency, not independently re-proved here.

## Verdict

The stated affine-transport-plus-killing corollary follows from Theorem V under the author's written hypotheses. No missing initial-measure premise, unjustified polynomial pullback, lost radial SOS certificate, or sign error was found in this bounded review. The conclusion is restricted to a supplied continuous affine velocity and a killing family satisfying V's uniform local SOS domination. It does not cover general nonlinear transport or diffusion-plus-killing.

## Proof obligations checked

Write v_t(x)=B_t x+b_t, with continuous B_t and b_t, and let Φ_t(y)=F_t y+d_t solve the stated affine flow with Φ_0=id. Standard linear ODE existence and the fundamental-matrix inverse give an invertible F_t on every finite supplied time window. On a compact window, continuity gives a positive uniform lower singular-value bound σ and a finite translation bound D. No claim of boundedness uniform on an infinite window is needed.

For a fixed polynomial q, p_t=q∘Φ_t^(-1) has fixed finite degree and C¹ coefficients. Thus M_t(q)=L_t(p_t) is C¹ by the finite coefficientwise product rule, even before any representing measure exists. Differentiating p_t(Φ_t(y))=q(y) gives

    ∂t p_t+v_t·∇p_t=0.

The derivative of L_t(p_t) is L'_t(p_t)+L_t(∂t p_t), and the two transport terms cancel exactly. With h̃_t=h_t∘Φ_t this yields V's normalized killing equation

    M'_t(q)=−M_t(h̃_tq)+M_t(h̃_t)M_t(q).

Affine substitution preserves squares, and M_t(1)=1. The degree bound and coefficient continuity of h̃_t follow from those of h_t,F_t,d_t.

The crucial transferred SOS domination is also correct. Assume h_t+C−c|x|² is SOS and |F_ty|≥σ|y|, |d_t|≤D on the chosen compact time window. Then

    h̃_t+C+cD²−(cσ²/2)|y|²
      = [h_t(F_ty+d_t)+C−c|F_ty+d_t|²]
        +(c/2)|F_ty+2d_t|²
        +(c/2)(|F_ty|²−σ²|y|²)
        +c(D²−|d_t|²).

The first term is SOS by affine substitution; the second is visibly SOS; the third is a positive semidefinite quadratic form and hence SOS; the last is a nonnegative constant. Direct expansion cancels every translation cross term and leaves exactly the left side. The new radial constant cσ²/2 is strictly positive, as V requires.

V consequently gives a unique initial probability μ with all absolute polynomial moments and

    K_t(y)=∫_0^t h_u(Φ_u(y))du,
    L_t(p)=∫p(Φ_t(y))e^(−K_t(y))dμ(y) / ∫e^(−K_t(y))dμ(y).

Recovering L_t from M_t uses p∘Φ_t, a polynomial for each time. The affine inverse makes the correspondence between full L and M paths reversible. V's unique initial law therefore remains unique for the transported path. V's positive-time determinacy also transfers: pull back any competing representing measure by Φ_t^(-1). The correspondence is at the level of actual measures and is not merely equality of finitely many moments.

The converse is justified on each compact time window. Affine coefficients and their first derivatives are bounded there, and h_t has a common finite degree with bounded coefficients. The transferred domination bounds e^(−K_t) from above uniformly. Both the integrand and its time derivative are bounded by a fixed polynomial in the initial variable times a finite constant. All absolute polynomial moments of μ then justify differentiation under the integral. The quotient rule gives the author's hierarchy. Continuation requires the future pair (v_t,h_t) to be supplied; an unspecified future coefficient schedule is not determined by the past.

## Density sign convention

The unnormalized weak test generator v_t·∇−h_t corresponds to

    ∂tν=−div(v_tν)−h_tν.

If instead the equation is written in non-divergence form as ∂tν=−v_t·∇ν+r_tν, integration by parts gives the test generator v_t·∇+(r_t+div v_t). Thus h_t=−r_t−div v_t is correct. Spatially constant divergence disappears under normalization; spatially varying divergence cannot generally be omitted. This verification is an algebraic convention check, not a proof of every PDE result cited by the author.

## Evidence limits

The exact controls test the radial identity with symbolic two-dimensional vectors, a nontrivial one-dimensional inverse-flow cancellation, and a moving-atom unnormalized hierarchy identity. The universal conclusion rests on the proof above plus the accepted V theorem, not on those examples. No nonlinear-flow, infinite-dimensional, formal-kernel, or field-priority conclusion is made.
