# Independent digest-bound mathematical review

## Verdict and binding

PASS for the mathematical claims and stated observation model in the final author file:

- File: `../global-calibration-ambiguity/RESULT.md`
- SHA-256: `ec620e491fd1c58cdc9dc0bcc8700784b79b4b399247ca1e2a235438138cf827`
- Reviewed author script: `../global-calibration-ambiguity/exact_controls.py`
- Script SHA-256: `867de73098d4eb210ef4fbbf5758c728efeb4dbe46982bd80941630fed00a2d2`
- Reviewed author output: `../global-calibration-ambiguity/results/exact_controls.json`
- Output SHA-256: `1115ba405c6e115f15cc0b7c748a307e2335f2cb4d106cd6a03bf502aab8e596`

This review independently read the complete named result, inspected its control program and output, rederived its main claims, reran its controls from a copy in this review directory, and ran separately implemented controls. It is a scoped mathematical assessment, not release, integration, or closure authority. It binds only these bytes; it does not bind later additions or edits.

## Reviewed claims

1. **Sharp adjacent-count threshold.** The integer-power parameterization covers every nominal command exactly once. The two induced maps are continuous, strictly increasing, endpoint-preserving, and have signed deviations `±u^k(1-u)/2`. Differentiation gives the asserted maximum at `u=k/(k+1)`. Their Bernoulli parameters coincide identically, proving admissibility and all-command ambiguity at the claimed inclusive threshold.

2. **Adaptive and stopped transcript equivalence.** The conditional Bernoulli kernel is the complete observation model. A shared policy seed and shared fresh uniform draws produce the same histories and commands recursively. The resulting full transcript and any measurable stopping/decision rule have equal laws. With failure defined as anything other than returning the correct count, two correct-decision probabilities sum to at most one. The binary minimax failure lower bound of one half follows. Equality of unconditional one-trial means alone would not suffice; the author correctly assumes the conditional law.

3. **Uniform finite-sample separation below the threshold.** For the specified midpoint command, `0<t_*<A<=B<s_*<1` holds, including `eta=0`. Thus clipping is inactive and `A^k>B^(k+1)`. The one-sided Hoeffding constant and binary sample bound are correct. The proof does not require continuity of every admissible map and therefore covers the stated nondecreasing class.

4. **Whole fixed-count catalogue.** `A^j/B^(j+1)` is nonincreasing in `j` (constant when `eta=0`). Positivity of the last gap implies positivity of all earlier gaps. The recurrence makes positive gaps strictly decrease because `A<1`. Midpoint thresholds consequently classify all counts using one empirical mean; the two-sided Hoeffding bound needs no catalogue-size union factor. The final adjacent pair proves necessity. The separate `{0,1}` endpoint exception is correct and avoids an inappropriate `0^0` interpretation.

5. **Divergence at the boundary.** Convex interpolation with identity preserves the map class. The stated Lipschitz estimate gives per-command total variation at most `(2k+1)(eta_k^*-eta)`. Coupling through the first mismatch gives the stated bound for protocols with at most `N` trials, and binary testing then gives the proposed divergent lower bound. The author properly excludes an expected-stopping-time claim, a sharp divergence rate, and a growing-`k` rate from this argument.

6. **Asymptotics and interpretation.** The threshold is asymptotic to `1/(2e k)`, the midpoint command tends to `1-e^-1`, and its common boundary no-hit probability has logarithm `-k+O(1)`. These establish a global identifiability result without certifying polynomial sampling. The distinction from the earlier command `x` of order `1/k` is mathematically sound. The statements about predecessor provenance and protected status were not independently audited against predecessor files.

## Correction resolved before final binding

The initially supplied digest `90c2aef5fec3e615efaf0c965aa459c664074da0bfc73541e562604dc7662049` defined error as the probability of reporting a wrong count while also discussing potentially nonterminating procedures. Taken literally without an output requirement, a never-returning procedure could avoid reporting a wrong count. This was reported to the author before final binding. The final Section 1 explicitly counts abstention and nontermination as failure, or permits restriction to procedures that return a count almost surely. The correction resolves the ambiguity. No remaining mathematical correction is required.

The author's update arrived while the independent controls still expected the initial digest. Their digest guard failed before mathematical checks ran. This was a stale-input guard success, not a mathematical test failure. The final-only run was then rebound and passed.

## Independent controls actually run

- Author program rerun from `replayed_author_controls/`, never in the author directory: **14,125 assertions passed**. The reproduced output is byte-identical to the final author output and binds the final result hash.
- Separately implemented `independent_controls.py`: **17,480 assertions passed**. Exact-rational checks cover counts `1,...,40,64,127`, additional rational commands, interpolation levels, catalogue gaps, decoder margins, and boundary touching/overlap.
- Independent inverse-command checks start from 50 nominal commands across five counts, solve the parameterization by 400 bisection steps at 110-digit Decimal precision, and verify residuals, calibration bands, response equality, and strict monotonicity.
- A different randomized, history-dependent, early-stopping protocol was exactly enumerated for counts `1,2,4,7` and maximum depths `2,4,6`. Boundary laws agree, normalize exactly, and the near-boundary TV bound holds for the selected interpolation levels.
- Source digests were checked before and after controls. There were no author or predecessor edits by the reviewer.

These finite controls are diagnostics, not proofs of universal quantifiers or stochastic simulations. The mathematical derivations above supply the general assessment. Detailed control families and program digest appear in `independent_controls.json`; the machine-readable binding is `REVIEW_RECEIPT.json`.

## Scope cautions and exclusions

The order-`k^-2` calibration scale applies to the chosen efficiently tuned command and does **not** define a universal polynomial-efficiency threshold. For example, commands of order `log(k)/k` can have polynomially rare no-hit events while tolerating calibration of order `log(k)/k^2`. The reviewed author text is appropriately restricted to its chosen-command distinction and does not make the stronger, incorrect claim.

This review does not certify physical calibrations, independent root-route assumptions in an actual system, causal identification, empirical source admissibility, mixture recovery, enriched multi-root joint observations, actual-calibration side information, constrained derivative/relative-error/parametric classes, sharp near-boundary efficiency, expected stopping budgets, external priority, protected integration, or T20 closure. A proposed separate clipped-map efficiency appendix is expressly outside this binding.
