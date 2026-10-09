# Exact control receipt

Run `python exact_controls.py` from this directory. Python's standard library is sufficient. The run writes results/exact_controls.json; the observed stdout is in results/exact_controls.log.

Seventeen control families pass:

1. The all-rate one-trial mixture identity as an exact bivariate polynomial.
2. The swapped-interior four-by-four determinant identity by independent polynomial expansion over all 24 permutations.
3. Equality of A/B count-compressed laws at arbitrary swapped rates, as polynomial identities.
4. The exact corner-code bijection.
5. 128 combinations of box-extreme rate settings, four histograms and the two Frechet-extreme couplings, all satisfying the 2 eta code-error bound at eta=1/48.
6. A valid disjoint-error coupling attaining 2 eta and violating the unjustified product improvement 2 eta-eta^2.
7. Exact physical rate uncertainty producing the same code law for two different catalogue supports.
8. Exact rational weight-floor and Chernoff constant comparisons.
9. A 32-term positive Taylor certificate that exp(211/48)>80, verifying the stated 211-group budget without a floating logarithm.
10. Exact rank three for the fixed base4 two-repeat panel and rank four for its three-repeat panel.
11. Exact reconstruction of the same four-label base4 three-repeat count contrasts. Their ranges are 368,1584/5,34432/135,5504/27. These describe that estimator's conditioning, not an optimal-sample lower bound.
12. Corner equality and interior separation of one A route, two A routes, and A plus AB.
13. 5,940 exact rational checks of the count chi-square upper bound on a finite n/rate grid. The written arbitrary-rate argument, not this grid, proves the theorem.
14. Exact tuned-rate minimum gaps for K=2,...,100.
15. Exact rational power-calibration confounding controls for K=2,...,12. The controls use rational survival bases to keep both worlds rational; the tuned-command real-power obstruction has its own analytic proof.
16. Exact six-group latent-label overlap at rare weight 1/4.
17. Equality of the freshly resampled crossed laws for the fixed alternative mixtures.

No random observations, numerical optimization, physical intervention, or benchmark was performed. Finite enumeration does not certify unmodeled independence, calibration, or inventory persistence. The extreme-coupling controls check the strengthened proof's intended interpretation rather than replacing its union-bound argument.
