# Independent structural review and finite controls

Internal AI review, not external human validation.

Reviewed on 2026-10-09 against the source hashes below. This review covers `GuardedTree.lean`, `Bound.lean`, and the finite fixture in `Controls.lean`.

## Findings

- No replacement-validity tautology was found. `context_replacement` assumes validity of the original filled context and of the incoming subtree, together with equal subtree judgement and exact support. It derives validity of the newly filled context. Each surviving guard receives the identical ordered support vector; no guard monotonicity is assumed.
- `prune_equal_state` derives descendant validity from ancestor validity. Equal ancestor/descendant judgement and support are explicit pruning eligibility hypotheses. Proper-context structure proves strict occurrence-count decrease. Nonnegative rule prices prove that deleting wrapper and sibling occurrences cannot increase cost.
- `exists_reduced_representative` minimizes occurrence count among valid, same-state, no-dearer trees. A remaining repeated state would admit an even smaller member through context replacement. It does not assume a normalized family or a finite catalogue.
- `Bound.lean` correctly derives the numerical bound `|J| (|S| + 1)`: descendant supports are nested subsets, so equal cardinality forces equality on a branch. A reduced branch therefore cannot repeat a judgement/cardinality pair. `Branch` covers root-to-descendant prefixes, including complete branches. Length counts rule occurrences, including the root.
- The finite-evidence corollary `|J| (|E| + 1)` follows by the support-cardinality bound. The exponential exact-state bound is also proved but is weaker.

## Verified controls

`Controls.lean` compiles with warnings treated as errors. Its explicit finite fixture has two judgements, three evidence roots, and six rule labels.

- The two-child licence requires exactly `{alpha}` in position 0 and exactly `{beta}` in position 1.
- `guard_not_upward_closed` proves failure of upward monotonicity. `enlarged_candidate` and `support_enlarging_rejected` also realize the failure with an actual valid, matching-judgement proof with strictly larger support.
- `same_support_replacement` directly instantiates `GuardedTree.context_replacement` through a nonempty licence context. Replacing a padded alpha proof by the bare alpha proof preserves validity and the whole exact state. Separate theorems prove different tree shape and strictly lower whole-tree cost.
- `shrinking_candidate` proves that the proposed smaller-support replacement is itself valid and has the same judgement; `support_shrinking_rejected` proves that the resulting licence is invalid.
- `premise_reversal_rejected` proves that swapping the two valid premises is invalid. `reversal_same_total_support` proves that this swap preserves the total support union, isolating the need for ordered child-support guards.
- `negative_price_pruning_counterexample` exhibits a proper equal-state descendant with valid ancestor and descendant and strictly fewer nodes, but pruning increases cost from -1 to 1 because the removed wrapper has price -2.

All three deliberately false mutations were rejected on the final fixture:

- `mutations/SupportShrink.lean`: kernel-backed `decide` establishes that the required empty-versus-singleton guard proposition is false.
- `mutations/PremiseReversal.lean`: kernel-backed `decide` establishes that the reversed singleton support equalities are false.
- `mutations/NegativePricePruning.lean`: the asserted cost nonincrease reduces to an unsolved `False` goal.

See `controls.log`, `review-bound.log`, and `mutations/*.log`. The successful control and bound declarations print only `propext`, `Classical.choice`, and `Quot.sound` as axioms. No `sorry`, `admit`, custom `axiom`, or `native_decide` occurs in the reviewed project proof/control/mutation sources. `LocalFintypeProd.lean` was byte-compared with the installed mathlib source and is unchanged.

## Exact limits

- The general `Grammar` type does not require finite rule labels, finite evidence, or decidable guards. Each rule has finite natural-number arity and each tree is finite. The exact-root-support bound needs finite judgements; the uniform corollary additionally needs finite evidence. The control grammar itself is finite.
- The normal-form existence proof uses classical choice and is not an extracted executable normalization/search algorithm. There is no checked finite catalogue, effective guard evaluator, saturation recurrence, or global minimum-attainment theorem here.
- Prices are rational and occurrence-additive. The theorem assumes every rule price is nonnegative, a sufficient condition stronger than merely requiring some selected trees to have nonnegative total cost. Real-valued prices and shared-DAG costs are outside these statements.
- Supports are ordinary finite sets combined by union. They do not record multiplicity, provenance chains, or any semantics beyond the supplied rule metadata.
- Guards inspect the ordered immediate-child support vector and fixed rule identity. The model does not include history-sensitive or arbitrary ancestor-sensitive guards.
- The bound's numerical inequality is verified. No lower-bound construction or optimality/tightness theorem is proved.
- Source authentication, metadata correctness, substantive rule admission soundness, semantic interpretation, metaphysical truth, and broader audit closure remain outside this bounded result.

## Reviewed source SHA-256 hashes

| Source | SHA-256 |
| --- | --- |
| GuardedTree.lean | `0a6faff768aa8aaa09dbddb48a155c7135d06b0762e522c7835d19d8c798d8b2` |
| Bound.lean | `8f7e1c4cc69a6354edb4d8e55f90aece93a22adf9c7ee733e685390f32c91a8c` |
| LocalFintypeProd.lean | `272b57521233c0e371c9d6cccfe6612b9b148d6a461b96d1228f104fac46fe2d` |
| Controls.lean | `7514451ff7cf9638e7182ff53cb4ac2ca7efe1e06ba24fe6ce5b2bd7938683ee` |
| mutations/NegativePricePruning.lean | `a955b3b3e1348c241242ae4b0c61e69f17899d1bb6b7a0994c82a51a1958f1fb` |
| mutations/PremiseReversal.lean | `371a7189be8c5071f79f2ee24bbcfb26c930b46ba11333ee14feca1abf1039a0` |
| mutations/SupportShrink.lean | `236fbfbb70138b340ffb200a4a173bf5171d435b77318f2b6421161bbacc71da` |
