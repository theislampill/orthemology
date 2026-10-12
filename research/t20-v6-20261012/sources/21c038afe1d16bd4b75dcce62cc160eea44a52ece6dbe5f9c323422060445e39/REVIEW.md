# Independent internal semantic review

9 October 2026. Verdict: pass for the bounded specification; no material semantic defect found. This is an independent internal AI review, not human validation, adoption, integration, programme closure, or authority to make those decisions.

## Scope and evidence

Read the complete four new Lean modules, SPEC.md and the final RESULT.md, and inspected the imported frozen grammar, branch-bound, catalogue and attainment definitions and proofs relevant to the result. Independently compiled copies of all five frozen sources and all four new modules, in dependency order, with Lean 4.19.0 (commit 6caaee842e94) and `-t0 -DwarningAsError=true`. All nine compilations exited successfully. The outputs and per-module axiom reports are under `review_semantic/`; this replay used those fresh outputs ahead of the installed mathlib search path, rather than the delivered modules' pre-existing oleans.

The installed mathlib checkout reports commit c44e0c8ee63ca166450922a373c7409c5d26b00b. All theorem/control axiom reports from the successful replay contain only `propext`, `Classical.choice` and `Quot.sound`. Inspection of the nine accepted source files found no admitted theorem, custom axiom, unsafe declaration, native-evaluation proof or implementation override. The installed compiler and mathlib environment remain trusted dependencies; this review is not a bootstrap or independent foundational audit.

Independently checked all 114 entries in PREDECESSOR_HASHES.json against current predecessor files: zero missing and zero changed. Each of the five frozen source copies also matches its named original byte for byte. The review did not modify delivered implementation sources or any predecessor. Separate replay copies and outputs were written only under review_semantic, together with this review.

## Semantic findings

1. **Actual numeric recurrence.** Candidates.lean:10–44 defines a table as `J → Finset E → Option ℚ`, generates numeric candidates, selects their finite minimum and updates each exact key. Saturation.lean:8–10 starts with all `none` and recursively applies that update. Neither definition uses bounded trees, a tree catalogue, an attainment theorem, or the correctness predicate to define its result.

2. **Finite, ordered and guarded choices.** RuleChoice is a dependent rule label plus a function indexed by `Fin (arity r)`, so premise positions are retained. Each premise support ranges over the grammar-support powerset. Enabled candidates require every old-table premise to be `some` and the arbitrary Prop guard to hold on the exact ordered tuple. The `getD 0` expression in outputCost cannot seed an unreachable premise: mem_candidates_iff proves that enabled values are actual `some` prices. Nullary rules retain their guard check on the empty tuple.

3. **Exact support and occurrence cost.** Outputs are local support union all child supports; prices are local price plus the sum indexed by all premise occurrences. Equal premise states at distinct positions are still charged separately. The old value is included before taking a minimum. Candidate price deduplication occurs only after matching an exact head/support key, and does not merge distinct support states or remove a larger support in favor of a subset.

4. **Soundness and completeness are proved, not assumed.** Correct requires both an actual realizing bounded valid tree for each numeric entry and a no-dearer table entry for every bounded valid tree. candidate_sound constructs children from prior witnesses, derives validity using equality of the whole ordered support tuple, and proves the resulting union and sum equal the numeric candidate. Retained values keep their old witness. candidate_complete decomposes any bounded successor tree, uses old-table values at each child's exact state, and applies additive monotonicity. No sign assumption is used. The separate step_correct and round_correct proofs establish the invariant from the impossible height-zero tree case. round_some_iff and round_none_iff yield attained exact minima and the claimed absence-of-witness equivalence.

5. **Enumeration excludes no generated premise.** The powerset restriction is justified by support_subset_grammarSupport. Stability.lean:90–109 proves that on generated tables, candidate membership is equivalent to the unrestricted ordered reachable-tuple formulation. This equivalence is correctly restricted to generated tables; it does not pretend arbitrary input tables have no out-of-grammar entries. No support-inclusion Pareto pruning is present.

6. **Global bound and assumptions.** The frozen grammarBound is exactly `|J| (|B| + 1)`. Its representative theorem preserves judgement and exact support and cannot increase cost under nonnegative local prices. The inherited pruning proof replaces equal-state ancestor/descendant occurrences, preserves surviving guards by exact support equality, strictly decreases node count even with zero prices, and uses nested support cardinalities for the branch bound. round_global legitimately transfers the independently proved bounded semantics to all finite trees. global_unique gives equality of the entire Option-rational tables; round_stable and step_fixed follow. The finite-E corollaries use `|B| ≤ |E|`. Finitude of J and nonnegative local prices are confined to these global transfers; bounded-height correctness requires neither finite J nor nonnegative prices. Ambient E need not be finite.

7. **Stopping condition.** early_stopping is an induction using deterministic equality of consecutive complete numeric tables. early_stopping_global transfers global correctness through that equality under its stated assumptions. It does not substitute equality of reachable-key sets.

8. **Controls and report alignment.** The unsupported unary self-cycle has no finite tree at all; its entries remain unreachable. The allowed nullary base enters at round one and its zero-price cycle preserves minimum zero at all later rounds. A false nullary guard prevents the seed. The priceDrop grammar is nonnegative, has the same reachable exact keys at every positive round, and changes the true/empty-support value from 10 at round one to 1 at round two. The checked controls therefore refute key-only stopping. The final RESULT.md describes the formal numeric-table result and its limitations accurately.

## Independent expected-rejection checks

Re-ran all three supplied negative sources against the independently compiled modules, keeping their output in review_semantic/mutation-*.log. UnsupportedSeed and KeyOnlyStops each fail with an unsolved `False`; DropGuard fails because `True` is not a proof of the actual guard in mem_candidates_iff. These are the intended logical/type failures, not missing-import failures. The `sorryAx` printed during Lean's error recovery for the rejected DropGuard source is not accepted theorem evidence and is absent from all successful-module axiom reports.

## Limits

This verifies the stated classical, noncomputable, rational occurrence-additive tree recurrence. Arbitrary Prop guards are not executable decision procedures. It establishes existential realizing tree witnesses, not executable witness-pointer production. It does not certify Python correspondence, real-price generalization, complexity, worst-case sharpness, DAG optimization, source authenticity, rule-admission soundness, philosophical or theological applicability, unrestricted provenance-changing cut, or the full FABLE calculus. Predecessor results remain inherited rather than newly discovered or re-credited.

## Reviewed SHA-256 bindings

- Candidates.lean: `0beb06d67a2f88a0e128e70e4f39e9f6a7bbc32d34092be4cf8942684ba6ab6d`
- Saturation.lean: `4204ba26af1c7ce0a48ad954843ffad0080c01c1be616250150c6055474bc839`
- Stability.lean: `72e056296a829719fada2820ca3b992ebe6a65a6c61698b16a50b38c2c2af6ef`
- Controls.lean: `5ed9d08a7fa04bc6fa6c1f66aaea0e2e4d3e6f93b3234fb948cd50bd01c090ec`
- RESULT.md: `a01fb6836c34074dd8ee38c874059246f6963c893f3bd9764ceb4ace39b1fb2e`
- SPEC.md: `d6d25b0a4631086b54eaf0bb62936e48bd33a6730111cba9df6eb4d091820586`

Frozen imports:

- frozen/LocalFintypeProd.lean: `272b57521233c0e371c9d6cccfe6612b9b148d6a461b96d1228f104fac46fe2d`
- frozen/GuardedTree.lean: `0a6faff768aa8aaa09dbddb48a155c7135d06b0762e522c7835d19d8c798d8b2`
- frozen/Bound.lean: `8f7e1c4cc69a6354edb4d8e55f90aece93a22adf9c7ee733e685390f32c91a8c`
- frozen/Catalogue.lean: `5cd7d3280d2c6f1399984d8cdb766bf8f27ea43113a4b2949d59e7e6887b476a`
- frozen/Attainment.lean: `50a751c692ba04ca43574cf2c347f493531edb32b7fa2ac7d93aa6173b91b525`

Rejected negative-control sources:

- mutations/UnsupportedSeed.lean: `fb58b86bed02924b0a2234afcae9cda6225f0d595db7ddc441b94f76c3e7ef73`
- mutations/KeyOnlyStops.lean: `548ad3c06ceb8015f68cefe1520e091e16970c3dec92ab70f694298424da902c`
- mutations/DropGuard.lean: `f2b285d7ee5485a0dc07c033bda21a07c944b50571c2618fec3a0c13938e79b9`
