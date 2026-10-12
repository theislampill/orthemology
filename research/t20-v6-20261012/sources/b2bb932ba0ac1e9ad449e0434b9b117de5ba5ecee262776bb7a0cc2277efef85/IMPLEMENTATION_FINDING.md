# Root implementation finding

Observed 2026-10-11 around03:00:51UTC in the developing gaussian_step.py before author freeze. The scalar target and state covariance were complex NumPy ndarrays, and the current mean was np.array([0+7j]). Passing them to gaussian_step with h=1 returned mean[0.] and four warnings that casting complex values to real discards the imaginary part. No exception occurred.

The mathematical theorem is about real Gaussian parameters. Silent removal of an imaginary component changes an invalid supplied input rather than rejecting it. Root requested an explicit complex-input check before float conversion, a real-step check, and a regression. This is an implementation validation repair, not a mathematical counterexample. No pre-repair source hash was captured during the reproducing call; do not manufacture one.

Reproduction used the imported current module in fibrewise-split-correction-20261011. The observed output was:

ACCEPTED_COMPLEX [0.] with four ComplexWarning messages.

The author and independent reviewer were notified. Final repair status belongs to their frozen verification record and a subsequent root check.
