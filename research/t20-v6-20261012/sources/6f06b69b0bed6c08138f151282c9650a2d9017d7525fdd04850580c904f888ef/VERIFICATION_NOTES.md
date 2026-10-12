# Verification notes

The formulas in RESULT.md are ordinary mathematical proofs; finite controls supplement them. No numerical control is labelled exact, and Python -O does not disable the mathematical check function.

The standalone implementation suite was written first. Its initial run failed because gaussian_step.py did not exist. After implementing the formula, all 11 original test methods passed. These tested a noncommuting rational fixture, singular and partial-rank inputs, a fixed target, translation covariance, and input rejection.

The parent then found a real implementation defect: NumPy's float cast could discard imaginary parts of complex array inputs before validation. The independent reviewer reproduced it. New regressions for all four array arguments and complex-valued time were run before the fix; that run failed with six failures and one error. The fix rejects complex arrays before conversion and requires a positive finite numbers.Real step. All 13 test methods pass after the fix. This is an input-validation repair; the real-valued mathematical theorem and its formulas did not change. The red and green logs are retained under validation/.

Strict array symmetry and computed-eigenvalue checks may reject valid exact-real semidefinite inputs when roundoff has altered their representation. Ill-conditioned matrices, floating-point overflow/underflow, or extreme time steps carry no performance or certified-accuracy guarantee. Cholesky checks protect the computed intermediate/output covariance, but are not a proof about exact input data under arbitrary numerical perturbations.

The mathematical checker uses exact rational matrices at h=log4 and T=diag(1,2) so both OU exponentials and the reaction exponent have rational values. It verifies full Gaussian density square completion and tangent identities, not only first moments. A separate high-precision two-atom-to-density example checks the non-Gaussian law-level reaction and entrance bounds by quadrature. The raw Euler countercontrol concerns the OU moment substep at a Dirac; it does not assign an undefined KL reaction score at that singular law.

The source investigation found direct prior art for the basic scheme, so the report credits Crucinio–Pathiraja rather than claiming a new algorithm. Their current v3 assumptions are used. The optional old-v1 source wording is not treated as a live objection to v3. The fixed-marginal application and singular-input proof are kept distinct from their smooth-density splitting analysis.
