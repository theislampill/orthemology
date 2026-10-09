# A sampled interaction ratio identifies a positive unary count

This is a separate finite-panel integer-recovery contract. The root need only participate in a promised positive interaction; its absolute calibration need not already be known. The result is developed once here and may be imported by bounded-interaction-detection. Equivalent author derivations are not separate discoveries.

## Inputs and observation

Let i belong to a positive multi-root support S. Its integer multiplicity n_S is known, or has already been recovered using the predecessor's four-isolated-value Cauchy procedure. Choose two strictly ordered interior commands x_1<x_2 for root i, holding every other coordinate of S at a fixed interior value. Inverting the two S contrasts gives the sampled ratio

rho=P_S(x_2)/P_S(x_1)=a_2/a_1>1,
a_l=r_i(x_l).

Assume the unary support {i} is promised positive, with unknown finite integer count n>=1. Its solo endpoint values are

Z_l=Q(x_i=x_l, all other coordinates zero)=(1-a_l)^n, l=1,2.

The same actual calibration r_i must apply to the unary routes and to S. Without that premise the predecessor's support-specific recalibration counterexample preserves all responses while changing the unary count.

## Strict cut theorem

For m>0 put

D(m)=1-Z_2^(1/m)-rho[1-Z_1^(1/m)].

Then sign D(m)=sign(m-n), with equality only at m=n.

Write c=n/m and H_c(z)=1-(1-z)^c. The determinant-like expression is

D(m)=H_c(a_2)-(a_2/a_1)H_c(a_1).

For c>1, H_c is strictly concave, H_c(0)=0, and H_c(z)/z is strictly decreasing for z in (0,1). Thus D(m)<0. For 0<c<1, H_c is strictly convex and that quotient strictly increases, giving D(m)>0. At c=1 it equals z and D(m)=0. These strict statements follow directly from H_c''(z)=-c(c-1)(1-z)^(c-2); they differentiate only the known H_c, not the unknown calibration.

Consequently H_c(a_2)/H_c(a_1)=a_2/a_1 at two distinct positive levels forces c=1. The interaction ratio rules out all alternative positive unary multiplicities.

## Terminating population-Cauchy procedure

Use only m=k+1/2, k=0,1,2,... . Since n is an integer, none of these D(m) vanish. Certified Cauchy access to the finite endpoint panel yields Cauchy access to Z_1,Z_2,rho through positive products, roots and division. At a half-integer, Z_l^(1/m) is the positive (2k+1)-st root of Z_l^2, so ordinary rational interval bisection supplies certified shrinking intervals without a transcendental oracle.

Refine until the D(m) interval excludes zero. This terminates at each cut because the true value is nonzero. Positive means n<=k, and negative means n>=k+1. Doubling k=1,2,4,... finds a finite upper bracket; integer binary search then returns n. Neither a known count ceiling nor an equality test at m=n is used.

Once n is known, a_l=1-Z_l^(1/n) gives absolute calibration values at those levels and any additional sampled solo command. In the incidence theorem this supplies an actual unit-row anchor, after the count inference has been proved separately.

The positive unary promise is essential for this interior sign procedure. If n=0, Z_1=Z_2=1 and D(m)=0 for every m, so refinement gives no guaranteed stopping rule. An isolated unary root without an independently available ratio retains its ordinary count/power-calibration ambiguity. This theorem alone does not decide absence or calibrate such an isolated root.

It is a finite set of distinct command vectors with arbitrarily refinable **population-probability** access. It is not exact count recovery from finitely many Bernoulli samples. Arbitrarily close command responses or extreme counts can require arbitrarily high precision. The boundary procedure separately uses a unit command to decide unary presence under its stronger endpoint-preservation contract.
