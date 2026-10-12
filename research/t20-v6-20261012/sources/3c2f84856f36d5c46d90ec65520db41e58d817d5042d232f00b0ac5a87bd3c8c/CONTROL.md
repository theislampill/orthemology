# Fixed-target, broad-law sharpness control

Root analytic derivation, 11 October 2026 UTC. Supplementary to the conditional-entropy investigation. Ordinary mathematics, no formal kernel or empirical interpretation.

Let the whole observed marginal be fixed and independent of the latent variable. Target latent law is N(0,T), T>0. At current latent law N(m,s), s>0, the multiplier is zero because all observed conditional expectations are constant. For q=log(dμ/dπ), Gaussian moments give

E = 1/2[(s+m²)/T−1+log(T/s)],
I = m²/T²+(s−T)²/(sT²),
Var(q)=m²s/T²+(s−T)²/(2T²),
D=I+Var(q).

Set m=n, s=1/n, n→∞. Then E/n²→1/(2T), D/n²→1/T², hence D/E→2/T. Conditional Gaussian log-Sobolev supplies D≥2E/T for the full smooth class. The coefficient cannot be improved uniformly over this class despite the nonnegative reaction term.

This does not contradict a larger coefficient on the inherited centred Gaussian subfamily. It prohibits transferring that subfamily inequality to arbitrary means/laws. It is an instantaneous dissipation bound, not a calculation of the trajectory's asymptotic exponent. The target is supplied, not authenticated by this calculation.

## Global descent is not descent on every fibre

For the inherited centred standard-target Gaussian construction, conditional energy at observed value y is e_y=(s−1−log s+b²y²)/2. With b=1,s=11/10, the inherited exact flow gives b′=−103/30 and s′=169/100. Hence

e_y′=169/2200−103y²/30.

It is positive for |y|<sqrt(507/22660), an interval with positive observed Gaussian probability. Integrated energy derivative is −22153/6600<0. Thus preserving the whole observed marginal and decreasing total KL does not guarantee each conditional law's KL decreases. This is a conditional mathematical limitation, not an assertion that all legitimate correction ought to make every sub-assessment monotonically improve.
