# Read first

This sibling stage proves a sharp global calibration identifiability boundary for fixed pure one-root counts. Every predecessor is preserved.

- `RESULT.md`: exact adjacent-count threshold, all-command static monotone ambiguity, strict-below-threshold finite-sample decoder, full fixed-count catalogue extension, necessary budget divergence near the boundary, and scope limits.
- `POLYNOMIAL_EFFICIENCY_APPENDIX.md`: separately scoped clipped-map exponential lower bound and a matching polynomial-regime upper construction. For fixed confidence and all sufficiently large M, polynomial-budget uniform identification is possible exactly when eta_M=O(log(M)/M^2).
- `exact_controls.py` and `results/exact_controls.json`: 14,125 exact rational assertions across 23 families. No simulated observations and no physical calibration data.
- `efficiency_controls.py` and its results: a further 33,840 exact rational assertions across 24 families for the separately reviewed appendix.
- `SOURCE_AUDIT.md` and `INPUT_BINDINGS.json`: predecessor relation, source identity, and what the new result does and does not add.
- `REVIEW_STATUS.md`: independent review and its exact bound source identity.
- `MANIFEST.json`: author-stage checkpoint hashes, with separate reviewer references.

The exact threshold for counts k and k+1 is eta_k^* = [k/(k+1)]^k/[2(k+1)]. At and above it, two static continuous strictly increasing calibrations yield identical endpoint response curves at every command. Below it, one repeated command separates the feasible mean intervals. For counts 0,...,M with M>=2, the exact threshold is eta_(M-1)^*.

The main order-1/M threshold is for identifiability. The appendix establishes a polynomial-efficiency tolerance scale only for this pure fixed-count conditional model, without sharp polynomial exponents. Neither result replaces arbitrary-mixture recovery, validates a physical instrument, authorizes integration, or closes T20.
