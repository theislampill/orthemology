# Exact second-order values for coupled and product truth hulls

2026-10-01. Rational primal/dual certificates for the same six-coordinate score pair in MIXED_RANK_COUNTEREXAMPLE.md. The optimized-regret conclusion uses the separately stated ordinary C³ asymptotic theorem.

Fix

    p=(1/4,1/4,1/2,1/2,1/2,1/2),
    h=(1,0,0,0,0,0).

The context lies in the relative interior of both hulls: for the coupled six-vertex hull, weights(1/4,1/8,1/8,1/8,1/8,1/4) are strictly positive and have barycenter p. For the product hull, both factor coordinates are interior. The common first-order correction is(1/2,1/2,0,0,0,0), with flag normal energy1/4 and zero high-block normal energy.

For a symmetric second correction

    w=(β,β,γ/2,γ/2,−γ/2,−γ/2),

the six distinct score/truth-class coefficients are

    G(0,0)=1/4−β/2−γ,
    G(0,1)=1/4−β/2,
    G(1,2)=1/4+3β/2+γ,
    F(0,0)=5/2−2β−100γ,
    F(0,1)=5/2−2β,
    F(1,2)=−7/2+6β+100γ.

The first argument is the flag truth and the second is the first-two high-coordinate sum. The four mixed high states share the middle rows for this symmetric correction.

## Coupled hull: positive optimum7/82

The correction

    β=12/41,     γ=3/164

has every row at least7/82. The active rows are G(0,0), F(0,0), F(1,2).

Put dual weights100/123,11/123,12/123 on those three rows respectively. They are positive, sum to one, and their weighted affine coefficient is identically7/82: the β and γ terms cancel. In the full four-dimensional tangent space, these same rows have symmetric high-coordinate gradients, so the weights cancel every tangent coefficient, not only the two symmetric coordinates. Equivalently the combined ambient gradient is exactly zero.

Thus the primal and dual values agree:

    τ*_coupled=7/82.

No symmetry assumption is imposed on possible competing repairs in the upper bound. The symmetric correction is only the exhibited optimizer.

## Product hull: negative optimum−1/26

In the product hull, flag truth and high-block truth vary independently. Take γ=0 and β=15/26. Every high-block correction is zero and the four flag/score rows have minimum−1/26, attained at G flag0 and F flag1.

For the dual certificate, use the opposite high truth vectors1100 and0011. Put weight6/13 on each of the two G flag0 rows, and weight1/26 on each of the two F flag1 rows. Their mass is one. Averaging opposite high truths cancels all high-coordinate terms; the remaining flag terms cancel as well. The constant weighted value is−1/26. Therefore

    τ*_product=−1/26.

Again the dual applies to every tangent correction, not only a symmetric one. The product's full set of twelve truth vertices contains these four selected tests.

## Exact asymptotic consequence

For the fixed declared loss units,

    R_coupled(ε)=−(7/82)ε²+o(ε²),
    R_product(ε)=+(1/26)ε²+o(ε²).

All affine and blockwise data, individual projected hulls, score generators, and Hessian projection fields agree between these two problems. Changing only their joint truth polytope changes a strict improvement into unavoidable worsening at the first nonzero asymptotic order.

The numerical values depend on the specified score units; their repair/nonrepair signs do not. These rational certificates supplement the actual finite-ε obstruction and nonlinear-repair theorems; they are not substitutes for the analytic optimized-regret bridge.
