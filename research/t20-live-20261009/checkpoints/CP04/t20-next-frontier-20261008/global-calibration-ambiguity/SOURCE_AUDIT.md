# Source and novelty audit

## Frozen input

The immediate mathematical input is `../calibration-design-frontier/ARBITRARY_RATE_COUNT_BOUND.md`, SHA-256 `e68242d3052342b2c2cf029b3e9d65d3402e7005d6179f8a335ec1e5ad52daad`. It supplies the pure fixed-count conditional Bernoulli model and establishes an exact-calibration fixed-budget lower bound valid against arbitrary adaptive commands, with matching sampling order and a fixed-command calibration obstruction.

The source was read in full, together with that stage's review status, manifest, and the root research-control file. Their input identities are recorded in `INPUT_BINDINGS.json`. No source text was changed. The root candidate was independently checked and rewritten using an integer-power parameterization.

## New work relative to that input

1. The older calibration ambiguity fixes one command near 1/M. The new construction is a pair of fixed static calibration functions that agree observationally at every nominal command simultaneously.
2. The error bound is uniform over all commands, and the functions are continuous, strictly increasing, and endpoint preserving. The construction is not an adaptive error adversary or an arbitrary per-trial calibration sequence.
3. The maximal paired rate discrepancy has a closed exact maximum, yielding a sharp threshold rather than just an order bound.
4. A below-threshold command gives separated composite-hypothesis intervals. It proves the converse and furnishes a finite uniform test.
5. An interval-order argument extends the exact threshold to all fixed counts 0,...,M. This remains pure-count estimation, not mixture recovery.
6. Interpolating the boundary maps toward the identity and coupling adaptive transcripts proves that a fixed uniform budget must diverge as the threshold is approached from below.
7. The separately scoped efficiency appendix clips the boundary maps to the allowed radius. It yields an all-command adaptive exponential lower bound. A one-command Bernoulli-inequality construction supplies a matching characterization of the polynomial-budget tolerance scale, eta_M=O(log(M)/M^2), at fixed confidence for all sufficiently large M. It does not claim sharp polynomial exponents or sampling constants.

The new threshold is order 1/M. The older order 1/M^2 local ambiguity and order M^2 sampling result remain intact. The new command is near 1-e^(-1) for large counts, where no-hit events are exponentially rare. It is invalid to infer polynomial-efficiency robustness from the identifiability threshold or to call the old local order-1/M^2 scale the universal limit for every polynomial-sample procedure.

## Tools and evidence

The general claims are established by the explicit construction, monotonicity and derivative arguments, interval separation, adaptive coupling, elementary Lipschitz bounds, and Hoeffding concentration in `RESULT.md`. The concentration and total-variation arguments are standard mathematical tools; no external paper or empirical source is used as evidence for the new theorem. No field-wide novelty or priority is claimed.

The author controls use Python's standard-library `fractions.Fraction` for exact finite checks. They cover k=1,...,32, a rational parameter grid augmented by every exact maximizing point, multiple strict-below-threshold ratios, endpoint cases, full-catalogue ordering, interpolated maps, and genuinely history-dependent command policies. The adaptive transcript checks enumerate four-trial binary histories for k=1,...,4. These are deterministic algebraic diagnostics, not samples from a physical experiment, and they do not replace the written proofs.

## Nuisance-parameter interpretation

One unknown physical map is held fixed within each world. Nonidentifiability compares two different allowed parameter pairs (count, calibration). It does not require an instrument to alter its map when the count changes during an experiment. If a separate reference observation identifies the map, or the map is known a priori and held to that known function in both alternatives, the statistical experiment is different and the obstruction no longer applies as stated.

## Authority limits

No empirical calibration, root-independence, inventory-persistence, causal-adequacy, or source-admissibility premise is established here. No arbitrary-mixture recovery rate, multi-root universal theorem, expected-stopping-time lower bound, minimax efficiency constant, polynomial-efficiency result beyond the specified pure-count model, protected write, owner acceptance, integration, or T20 closure follows. Independent review is mathematical review of its specifically bound files only. The appendix receives a separate receipt; it is not included retroactively in the main theorem's review.
