# Exact-law injectivity does not apply to the floating-point output summary

The root invoked the inherited gaussian_step.py unchanged, with scalar T=S=1, target mean g=1, input means 1 and 2, and h=20. Both returned final Gaussian parameter pairs are mean 1 and covariance 1. In exact real arithmetic their corrected means differ by exp(−40)>0. Rounding the final mean therefore gives a concrete collision in the returned final law parameters. The diffusion intermediate remains different at h=20, so this is not a collision of the entire diagnostic dictionary.

At h=1000 the reaction exponent and diffusion coefficient themselves underflow to zero. These calls return finite output parameters rather than raising. The old implementation docstring's statement about raising on floating-point failures must not be read as a promise to detect all underflow or information loss; its executable checks are narrower.

This confirms the new report's existing scope limitation: its exact-law inverse is not an inverse of rounded parameter pairs. It does not refute mathematical injectivity, demonstrate a newly claimed stable inverse, or require changing the inherited approximate correction algorithm. A consumer demanding reversible audit transport must provide appropriate exact or error-controlled retained data. This test supplies no universal precision threshold or software repair.

FLOATING_COLLISION.json records the actual calls' results. These numerical observations supplement the exact mean-difference formula. No claim is made that floating-point limits themselves are novel mathematics.
