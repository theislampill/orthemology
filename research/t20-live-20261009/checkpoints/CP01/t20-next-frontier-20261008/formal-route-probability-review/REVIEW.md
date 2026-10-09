# Independent review of the finite forward probability bridge

8 October 2026. All six frozen Lean modules were read and replayed independently. This review is separate from the previously frozen inverse and CRT reviews.

## Verdict

The forward bridge closes the identified algebraic probability-law gap for the explicitly declared independent whole-route Bernoulli model. Equality of the three generated full endpoint distributions implies equality of the anonymous five-class/output-bundle histogram, even when the two models use different finite occurrence types and route counts.

No hidden decoder assumption, fixed route-count bound, same-carrier restriction or assumed probability-factorization premise appears in the main theorem. No mathematical or semantic mismatch with this stated target was found.

## Definitions and quantification checked

The type R indexes route occurrences, not additional original roots. The root signature is still the fixed A/B signature represented by the five kinds a,b,c,d,e. Profile has exactly A, B and AB. The theorem is general in the finite occurrence carriers R and R' and in the shared finite effect catalogue E; it is not the arbitrary-root CRT theorem.

Each occurrence has a kind and a nonempty output bundle. Nonemptiness is a field of Model, and it is used to prove the five histogram empty-output coefficients vanish. Empty-output occurrences would be invisible, so this premise is essential. Empty route inventories are allowed. If E itself is empty, nonempty outputs force any admissible occurrence inventory to be empty.

An assignment maps each occurrence to a success/failure bit. Its mass is a product of coordinate masses. Normalization is proved by a finite product-of-sums identity; nonnegativity is separately established from the calibrated factors lying in [0,1]. The general normalization lemma allows arbitrary rational coordinate values algebraically, but assignment_distribution supplies the positivity premises for the actual model, so signed weights do not leak into the probability claim.

The generated endpoint unions the entire bundle of each successful enabled occurrence. A single bit controls the whole bundle. Guards depend only on the fixed issued profile. Disabled occurrences retain latent bits that cannot emit; summing those coordinates contributes a factor one. The proved endpoint_absent_iff identifies exactly the assignment-level event in which all enabled routes hitting the query fail.

Probability is defined by summing assignment masses over that event. The all-failure product formula is then proved and grouped by class/output histogram. The three calibrated panel equalities are derived from that grouping. Thus the result does not define probability to be the desired final absence product and then restate the definition.

The full endpoint law is independently defined as a pushforward sum over assignments. Its nonnegativity, normalization and absence marginal are proved before composition with the inverse. Exact law agreement is a population-law premise, not equality of finitely observed empirical frequencies.

## Independent verification

Sources were copied into this review's frozen/ directory and compiled into new local .olean files. The dependency path uses the separately reviewed frozen inverse modules and the pinned Mathlib checkout. Author deliverable sources and compiled files are not used as substitutes for the newly compiled forward modules.

- All six copied modules compile with warnings treated as errors.
- Final imported-module verification with --trust=0 passes.
- Every principal printed dependency list contains only propext, Classical.choice and Quot.sound.
- All twelve files in the author's frozen manifest match before the independent replay; the final hash check is preserved separately.

Two independent same-path mutation controls were also executed in this review's own workspace. Reversing the endpoint success gate fails at the intended membership/event proof, with an actual x-in-output proposition confronted by False. The original model compiles before and after that mutation. Changing c-class failure from 5/6 to 2/3 yields a well-formed modified model but breaks the derived AB panel at the exact incompatible powers (2/3)^hit_c and (5/6)^hit_c. Restoring the model restores the successful panel proof. The runner checks those specific goals and rejects environmental/import failures as evidence.

## Remaining boundary

Independence is built into the product-assignment model. This proof does not establish that actual productive occurrences obey that model. It also does not establish that occurrence indices are correctly individuated, aliases were removed, rates are physically calibrated, guards remain fixed in the intended source interpretation, the observed effect catalogue is complete, or the proposed interventions are admissible.

The model uses one independent support-calibrated success bit per route. It does not formalize a physical incidence-gate architecture or prove that the observations identify that architecture. Different gate implementations can still induce these same laws. No numerical route IDs, complete unobserved causal history, original intrinsic perfections or metaphysical uniqueness are recovered.

The mathematical factorization obligation has been discharged inside this explicit finite generative model. The independence choice and faithful model-to-world/source interpretation remain external. The Lean result does not prove finite-sample recovery, the arbitrary-root rank/CRT results, or the later bounded-count statistical theorem.

No protected edits, integration, owner acceptance, global-priority assertion or active-research duration certificate follows from this review.
