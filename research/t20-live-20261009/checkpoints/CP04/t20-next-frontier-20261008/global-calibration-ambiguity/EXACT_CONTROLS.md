# Exact author controls

Replay with `python exact_controls.py` from this directory or by its absolute path. The script reads `RESULT.md` only for a digest and writes its diagnostics to `results/exact_controls.json`; it does not modify the proof or predecessor files.

The completed run passed 14,125 exact rational assertions in 23 families. Coverage includes:

- Closed-form critical values and common means for k=1,...,32.
- Integer-power all-command identities at 572 rational parameter points, including every tested exact maximum.
- Signed uniform-error identities, rate domains, strict monotonicity, endpoint preservation, and attained error maxima.
- No-clipping and strict separation at six rational fractions of the threshold for each tested count.
- Every adjacent interval and gap recurrence for all catalogues through M=33.
- Decoder-threshold ordering and equality at the critical calibration radius.
- Admissibility and uniform channel-distance bounds for convex interpolation toward identity.
- Sixteen exact history-dependent adaptive transcript equalities and 48 exact total-variation bounds, with transcript normalization.
- The separate zero-versus-one endpoint case.

The exact rational parameterization avoids numerical fractional powers and rounding-dependent claims of equality. It uses no packages outside Python's standard library, no random simulated trials, and no empirical calibration data. Finite checks are diagnostic; the general proof in `RESULT.md` establishes the theorem for all commands and positive integer counts.

## Separately scoped efficiency appendix

Replay `python efficiency_controls.py` for the separate appendix. Its completed run passed 33,840 exact rational assertions in 24 families. These check the clipped maps and their exact range, monotonicity, error and endpoint conditions; the polynomial envelope d(x)<=x/(2k+1); the inactive-region identity and active-region probability sandwich; rational rare-event envelopes; history-dependent adaptive total variation; and the sufficient command, Bernoulli-inequality bracket, positive final gap and full-catalogue ordering through M=64.

The first author run exposed a diagnostic assertion that incorrectly required x-eta<x+eta when eta=0. The theorem's rate-domain argument did not impose this inequality; the assertion was corrected to allow equality and the entire script was rerun successfully. No proof statement changed. Exponential and asymptotic inequalities are established in the written appendix rather than tested by floating-point equality.
