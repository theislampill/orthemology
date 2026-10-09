# Kernel-checked finite route probability and histogram identification

## Main result

`RouteProbability.endpoint_law_identification` proves:

For two arbitrary finite route inventories over the same finite effect catalogue, equality of the full generated endpoint distributions at the three issued profiles A, B and AB implies equality of their complete anonymous five-class route histograms. The inventories may have different finite occurrence types and different route counts. There is no bound on those counts.

This extends the separately frozen rational-panel inverse. The forward probability law is now proved from a normalized finite assignment model rather than defined to equal the desired product.

## Declared generative model

Each route occurrence has one of five support/guard kinds:

- a: A-supported, unguarded
- b: B-supported, unguarded
- c: AB-supported, unguarded
- d: A-supported, enabled only when B is absent
- e: B-supported, enabled only when A is absent

Each occurrence emits one nonempty finite output bundle. Guards are evaluated on the issued profile. Independent route-success bits have failure probabilities 1/2 for a and d, 2/3 for b and e, and 5/6 for c. Those are the prescribed support-calibrated Bernoulli probabilities. One occurrence's single success bit governs its entire bundle, preserving joint-output correlation.

An assignment is a function from route occurrences to Bool. Its rational mass is the product of coordinate masses. A generated endpoint is the union of the bundles emitted by successful enabled routes. The full endpoint probability is defined by summing assignment masses over assignments generating that endpoint.

Disabled routes still have latent bits, but cannot emit outputs. Summing their two latent states contributes one. Nothing changes guard evaluation after the issued profile has been chosen.

## What the kernel verifies

1. All assignment masses are nonnegative and sum to one.
2. Summing all assignments in which selected routes fail yields the product of their failure probabilities.
3. A generated endpoint misses U exactly when every enabled occurrence whose output bundle meets U fails.
4. Counts of labelled occurrences group into their anonymous class/output histograms.
5. Assignment-summed absence probabilities equal the exact A, B and AB rational panels in the frozen inverse.
6. The endpoint distribution is nonnegative and normalized. Absence coordinates are marginals of that actual endpoint law.
7. Equal absence panels identify the histogram; equal full endpoint laws therefore do so as well.

Principal declarations:

- `sum_bernoulliWeight_all_false`
- `endpoint_absent_iff`
- `absence_probability_factorisation`
- `absence_A`, `absence_B`, `absence_AB`
- `generative_model_identification`
- `endpointProbability_normalized`, `endpointProbability_nonneg`
- `endpoint_law_identification`

All are quantified over arbitrary finite types. The verification source instantiates different finite route counts and the empty route inventory as additional checks.

## Files and verification

- `BernoulliAssignments.lean`: the assignment distribution and event factorization
- `HistogramGrouping.lean`: labelled-route counts and product grouping
- `Model.lean`: kinds, issued-profile enabling, success gates and emitted endpoint
- `GenerativePanels.lean`: assignment-summed absence probabilities, calibrated panel derivation and inverse composition
- `EndpointLaw.lean`: endpoint-law pushforward, normalization, marginalization and full-law identification
- `Verification.lean`: theorem signatures, dependency audit and edge instantiations

The sibling `../formal-identification` package is an immutable dependency. Its ten-file source manifest is checked before each full build, and its proofs are rebuilt. No original proof source or script is changed by this extension.

Run `./bootstrap.sh`, `./verify.sh`, and `./mutation_checks.sh`.

The same Lean 4.19.0 and Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b pins are used. Bootstrap remains workspace-local. The full verification treats warnings as errors and reruns the final imported-module check with `--trust=0`.

The principal theorem axiom dependencies are only `propext`, `Classical.choice`, and `Quot.sound`. No new axioms, `sorry`, `admit`, or `native_decide` occur in the delivered Lean sources.

The mutation suite uses disposable same-path original/mutated/restored module copies. It checks that reversing the success gate in endpoint generation breaks the event proof, and that changing the AB-supported route calibration from 5/6 to 2/3 breaks the derived AB-panel proof. Restored versions compile successfully. Module/import/path failures are rejected as valid mutation-test outcomes.

## Remaining external boundary

The finite probability model and its inverse are proved together. It remains external whether a physical or metaphysical situation is faithfully represented by this model: whether the indices denote distinct actual productive occurrences, independence and calibration hold, the interventions are admissible, the effect catalogue is complete, guards are fixed as specified, and exact population endpoint laws are available.

This package uses the explicitly permitted support-calibrated independent-route Bernoulli architecture. It does not separately formalize an incidence-gate architecture or prove an observational-equivalence theorem between physical gate implementations. Nor does it prove finite-sample recovery, general-root identification, source authentication or metaphysical uniqueness.

Installation, waiting, recovery and packaging receive no research-duration credit; no total active-research duration is certified.
