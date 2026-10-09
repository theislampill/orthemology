# Executed controls and their scope

Run `python controls.py` in this directory. It prints CONTROLS_OUTPUT.json content without changing an existing frozen packet. The retained output was produced by that entrypoint. These are mathematical controls, not empirical sampling or practical runtime claims.

- 180 rational/algebraic cases: n in {1,2,3,5,10}; x=p^(n+1), y=q^(n+1), with six rational p,q values. Then x^c,y^c are exact rationals. The sole remaining algebraic power is enclosed by 160 exact rational bisections with integer-power comparison. Exact inequalities certify gap positivity, the double-integral envelope, the bounded-variable covariance envelope, c-to-1/2 comparison after integer powering, the tail contraction where relevant, and the loose all-rate chi-squared bound.
- 12 exact Sibuya series controls: positive recurrence weights and a rational total-mass remainder interval contain the entire 400-bisection algebraic interval for the generating function. The reviewer correctly noted that an earlier version checked only overlap; that weaker check was replaced before freeze. No finite mean or variance of the integer variable is assumed.
- 48 exact literal boundary controls check J1=AB and normalized four-cell laws.
- 12 exact rational four-cell cases check the summed chi-squared identity against its simplified expression.
- An exact rational Taylor enclosure for exp certifies 1.59362<u*<1.59363. The identity f(u*)=u*(2-u*) gives a rational enclosure for the limiting constant. The longer decimal display is an ordinary high-precision evaluation, not the certified bracket.
- 1,750 pairs of 80/160-digit evaluations check stable formula agreement, the appropriate central or tail envelope, and the global bound. This includes a finite logarithmic grid and selected highly asymmetric/tiny-rate cases. Grid maxima are expressly not true global maxima. The n=1 boundary-limit regime is retained rather than excluded.
- The naive 80-digit direct-subtraction failure is reproduced exactly as a numerical failure: it returns zero for S at n=1,u=1000,v=1. The stable formula returns strictly positive information and agrees at the two precisions.
- Five fixed-u* convergence displays illustrate approach to the proved limiting constant up to n=1,000,000. Five additional positive-cell KL calculations check KL<=chi-squared and the approach of their ratio to one half. No asymptotic proof is inferred from these numbers.

The universal arguments are in RESULT.md and ASYMPTOTIC_DESIGN.md. Finite checks neither establish universality nor formally verify the entire proofs. A fresh final reviewer separately checks their validity and instrument scope.
