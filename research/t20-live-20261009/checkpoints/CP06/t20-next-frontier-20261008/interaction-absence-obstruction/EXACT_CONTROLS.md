# Exact controls

The author script uses only Python integers, Fraction arithmetic and rational root intervals. It passes 65,208 assertions in 23 named families. No floating-point derivative estimate, generated physical sample or Monte Carlo evidence is used.

For N=1,...,64 it checks the exact rational maximum N^N/(N+1)^(N+1), the maximizing parameter, derivative sign, the uniform bound and endpoint/face cases. Parameterizing commands by a=1-t^N makes the hidden calibration value 1-t rational, so the independent-route law, raw-Q gap, probability range and common coordinate derivative bounds can be verified exactly. The calibration secant ratio 2^(N-1) records the failure of a common hidden-map modulus in this family.

The script implements one fixed total alternative oracle, with a coarse branch returning Q_0 and a fine branch using certified root bisection for Q_N. It checks both branches against exact rational true values. Sixty-four illustrative adaptive command/precision/stopping transcripts are reproduced unchanged under appropriate alternatives. A separate finite uniform seed control uses one fixed alternative name for every seed in a 7/8-probability absent-return event, illustrating the seed-independent transfer.

These finite transcript controls do not enumerate arbitrary algorithms or prove the general randomized statement. The written finite-transcript contradiction and increasing-event argument prove those universal claims. Independent review provides separately written exact controls and a hash-bound proof audit; replay of the author script is reproducibility evidence only.
