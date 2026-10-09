# What the quantitative promises exclude

These are mathematical failures of stronger statements, not empirical observations.

## 1. A weight floor only for positive counts does not recover zero presence

Compare the pure count-one law with (1-epsilon)delta_1+epsilon delta_0 at the same allowed calibration. The positive-count weights are at least 1/2 when epsilon<=1/2, but the zero atom is arbitrarily rare. Couple the latent labels in each group; a full group differs only if its rare zero label is drawn. For n independent groups, total variation is at most n epsilon regardless of the within-group length. No fixed sample budget uniformly recovers the zero flag as epsilon tends to zero. Replacing the rare count zero by count two similarly obstructs primitive-support recovery without a floor on every present component.

## 2. Mere interior calibration is insufficient, even at a fixed count ceiling

For M>=3, compare equal-weight mixtures on {1,2} and {1,3}. Their primitive vectors differ. If the actual common success rate tends to zero, every fixed finite collection of endpoints approaches the all-no-hit record under both models. If the rate tends to one, it approaches the all-hit record. Fixed positive weights and a finite count ceiling do not themselves give a uniform sample budget over arbitrary interior rates. The scaled interval in RESULT.md prevents these collapses at the required quantitative rates.

Conversely, if the count ceiling is removed while one actual t in (0,1) is held fixed, compare pure count n with the equal-weight mixture on {n,n+1}. Their primitive positive targets are (1) and (n,n+1). They have at most two components and satisfy any weight floor w<=1/2. A coupling gives total variation at most R(1-t)t^n/2 for one R-repeat group and at most G R(1-t)t^n/2 for G independent groups. This tends to zero for every fixed endpoint budget. The counterexample can retain a fixed rate inside any previously chosen nondegenerate window; what is no longer valid is its asserted upper bound on the actual counts. It does not rely on the frozen approximation countermodel's changing calibration.

## 3. Component-specific calibration can counterfeit support inside the rate window

For M>=3 set u=1-1/(3M). The first world has counts {1,2}, positive equal weights, and common survival u^3. The second world has counts {1,3}, the same weights, but count-specific survivals u^3 for count one and u^2 for count three. Their scalar atoms are identically {u^3,u^6}, so every held independent-repeat grouped law agrees.

All actual success rates, 1-u^3 and 1-u^2, lie in [1/(2M),3/(2M)]. The count ceiling, weight floor, interior window and latent persistence therefore do not repair the missing **common calibration across components**. These positive support vectors are not proportional.

## 4. Fresh resampling can counterfeit support inside the rate window

Take an equal-weight mixture on {1,2}, resampling its count before every endpoint, with t=1-1/M. Its no-hit mean is s=(t+t^2)/2. A pure count-one world with survival s produces the same independent endpoint process. Its actual success rate is

1-s=3/(2M)-1/(2M^2),

also inside the permitted window. Yet the primitive targets are {1,2} and {1}. Artificially grouping independently resampled endpoints does not create the conditional power moments required by the estimator.

Alternatively, hold the count but reuse one conditional Bernoulli draw throughout each group. Then every normalized factorial statistic has expectation m_1 rather than m_r, and the same mean-matching construction can counterfeit the constant-word grouped law. This isolates conditional repetition independence from simply retaining the latent count.

## 5. Absolute count ambiguity remains inside the model

The frozen global calibration construction for pure counts M-1,M has uniform error eta*<1/(2M), so both unknown static calibrations satisfy the present pointwise window at nominal command 1/M. Their full endpoint response curves agree at all commands. Their primitive targets are both (1), as the new theorem requires. Treating the recovered primitive vector as a gcd-one empirical discovery would incorrectly turn this exact ambiguity into an absolute count claim.

## 6. Computational and statistical claims remain different

The rational grid proves a finite decoder exists without an unknown-real equality oracle. Its enormous grid and conservative sample constant are not evidence of practical tractability. A sampling bound polynomial in M at fixed C,w is not a bound polynomial in log M, uniform in C, or optimized over instruments. Grid weights do not inherit the separate accuracy guarantee unless WEIGHT_ESTIMATION.md's larger budget and tolerance choices are used.

The frozen approximation-oracle obstruction concerns an unbounded count ceiling or a missing floor, while this theorem explicitly supplies M,C,w and a rate window. There is no contradiction. Independence of full groups is still required for concentration; correct marginal group laws alone do not supply it.
