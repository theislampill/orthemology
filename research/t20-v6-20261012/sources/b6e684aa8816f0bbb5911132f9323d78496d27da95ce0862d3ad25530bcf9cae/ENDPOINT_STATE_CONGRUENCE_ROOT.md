# Endpoint state congruence: participating root deduction

2026-10-10 UTC. Ordinary mathematical deduction submitted for author/reviewer consideration. No independent-review, kernel, field-priority, empirical, or research-closure credit.

## Ancestor

The complete `measure-moment-continuation-boundary-20261009/RESULT.md` supplies a distinct lognormal Stieltjes pair nu+ and nu- with identical finite moments of every integer grade, but different future means under some positive normalized exponential tilt. The present deduction does not discover that classical pair again. It embeds the existing obstruction at the endpoint of the newly examined positive-exponential-moment domain.

## Construction

For a fixed computable a>0 and each sign s, put

D_s = integral exp(-a*x) d nu_s,
mu_s(dx) = exp(-a*x) nu_s(dx) / D_s.

The inherited explicit lognormal densities give computable probability laws: writing z=log x, their densities are the standard Gaussian density times 1 plus or minus a fixed computable bounded sine perturbation. Truncate to [-R,R] with R>=1; the tail is bounded by (1+epsilon) times 2 exp(-R^2/2)/(R sqrt(2 pi)). On the compact interval the density and each required test have effective bounds and continuity moduli, permitting certified quadrature. The tail tends effectively to zero. Therefore D_s is a computable positive real (bounded computable Lipschitz integration); its reciprocal is computable without a supplied rational lower bound, by positive lower-bound search. For each integer r, x^r exp(-a*x) is a bounded computable function with effectively obtainable bound and modulus. Thus the moments of mu_s are uniformly computable in r and precision. One may choose a common computable rational M greater than both 1/D_s. Then

integral exp(a*x) d mu_s = 1/D_s < M.

Every original mu_s is in the positive-exponential-moment input class. Its endpoint tilt T_{-a} mu_s equals nu_s and has all polynomial moments finite and uniformly computable. Both endpoint moment records are exactly the same.

Nonetheless for some positive v, the means of T_v nu+ and T_v nu- differ by the inherited result. Consequently equality of full endpoint moment records does not imply equality of their future observable continuation. In initial coordinates these are the interior states T_{v-a} mu_s.

There is no contradiction with the interior theorem: the original moment records of mu+ and mu- are different, since both originals are exponentially moment-determinate and the laws cannot coincide (their reverse tilts would then coincide). The theorem never says that their initial inputs are equal.

## Operational interpretation limited to this mathematical model

Taking a normalized full moment record as the entire state works for continuation within the certified positive-exponential-moment class. Permitting the endpoint can erase the state distinction necessary to continue, even when the endpoint law and all moments happen to be computable. This is separate from the endpoint computability obstructions: it is a failure of the moment equivalence relation to remain a continuation congruence on the enlarged class.

Keeping the actual law, its Laplace profile, or a sufficient inherited state identifier prevents that particular information loss. No claim is made that any one such mathematical representation supplies epistemic warrant, productive sourcehood, or an actual psychological implementation.
