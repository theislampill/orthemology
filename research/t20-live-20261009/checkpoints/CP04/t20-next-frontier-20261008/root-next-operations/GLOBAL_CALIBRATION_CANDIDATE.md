# Prospective all-command calibration ambiguity

2026-10-08 12:54 UTC. Candidate sent for independent development and review; not a verified theorem yet.

Adjacent fixed pure counts k and k+1, k>=1. Nominal success command x∈[0,1]; actual calibration is an unknown static monotone endpoint-preserving map r(x), uniformly within eta of x. Each fresh endpoint has no-hit probability (1-r(x))^count, conditionally on the commanded rate and past.

Set alpha=k/(k+1). Parameterize t∈[0,1], with x=1-(t+t^alpha)/2. This is a strictly monotone bijection reversing t. Define true rates r_k(x)=1-t and r_(k+1)(x)=1-t^alpha. These maps both increase with x and preserve endpoints. They yield identical no-hit curves t^k at every command, since (t^alpha)^(k+1)=t^k. Their maximum command errors both equal eta_star=Delta_k/2, where Delta_k=max_t(t^alpha-t)=(1/(k+1))(k/(k+1))^k.

Thus eta>=eta_star should permit two fixed distinct-count worlds observationally identical under every adaptive endpoint-only protocol with the stipulated conditional kernels. This requires no time-varying adversary or nonmonotone calibration.

Conversely choose t_star=(k/(k+1))^(k+1), x_star=1-(t_star+t_star^alpha)/2. At eta_star, the closest competing no-hit means coincide at t_star^k. For eta<eta_star, lower mean for countk is (1-x_star-eta)^k, strictly greater than upper mean for countk+1, (1-x_star+eta)^(k+1). Both survival endpoints lie strictly within[0,1] in this regime. Therefore finite repeated observations at this one command can distinguish the two count classes, provided fresh conditional trials and a known error promise. A Hoeffding gap bound gives a finite sufficient sample budget; it is not an efficient polynomial-in-k guarantee.

The threshold is asymptotic1/(2ek), unlike the earlier K^-2 calibration budget at command1/K that preserved polynomial count estimation. Here the threshold-optimal command approaches1-e^-1, and no-hit probabilities near the threshold are exponentially small in k. Identifiability and efficient stable estimation must stay distinct. This is a pairwise count result, not arbitrary mixture recovery or actual calibration warrant.
