# Constructive guarded witness extraction

## Contract

Given a fixed finite-rule grammar, finite judgement type, decidable evidence and judgement equality, a computational decision procedure for each fixed ordered support guard, and a complete explicit ordered list of rule labels, return an actual finite `Tree G` for every reachable exact judgement/support key. The tree's recomputed cost must equal the numeric compiler's minimum at the same round. At `grammarBound G`, nonnegative rational rule prices suffice for unrestricted minimum cost over all valid finite occurrence trees. An unreachable key returns `none`.

`Fintype R` and `Fintype J` are the numeric compiler's finite enumeration inputs. `RuleList R` is a separate computational list plus a completeness proof; duplicates and arbitrary ordering are allowed. Tree equality and finite ambient evidence are not required. Grammar fields and guard decisions must be executable for runtime use. No decidable equality on rule labels is assumed beyond whatever the supplied numeric finite instances require internally.

## Reference algorithm

1. Materialize the inherited dynamic-table result for the requested round/key.
2. If absent, return `none` without constructing a tree list.
3. Construct ordered finite syntax shapes at the round's height. Cartesian power zero has one empty tuple, so nullary rules seed the process. Decode shapes into finite occurrence trees without deduplication.
4. Recompute recursive validity, exact judgement/support, and occurrence-additive rational cost. Return the first accepted tree at the compiled cost.

The returned value is `Option (Tree G)`, not a proposition, an existential witness selected by classical choice, a cyclic graph, or a DAG with shared-node prices. Equal-price ties follow the supplied rule-list order. Selection requires no equality comparison between trees. The global fixed-bound extractor is deterministic relative to that order. When callers increase `extractRound` height, witness identity and size need not stabilise even if numeric prices do: a seeded zero-cost cycle may produce progressively longer tied trees. First-match selection minimises price; it does not minimise nodes or select a canonical proof identity.

## Proof boundaries

`mem_trees` identifies list membership with height-bounded tree syntax. `accept_iff` identifies the executable verifier with recursive `Tree.Valid` and exact key/cost. `search_sound` and `search_complete` justify selection. `extract_sound`, `extract_complete`, and `extract_cost_eq` prove actual output correspondence to every numeric round. `extract_global_cost_eq` projects the global output to the existing compiled table. `extract_global` and `extract_none_iff` give unrestricted minimum validity and unreachable-key completeness under nonnegative prices.

Classical reasoning appears in erased correctness proofs and inherited proof infrastructure, including the existence/normalization theorem. Accepted computational definitions are not marked noncomputable and execute in the Lean evaluator. They never call a choice operation to obtain a tree from the numeric compiler's existential correctness theorem. Axiom reports may include `Classical.choice`, `propext`, and `Quot.sound`; absence of `sorryAx` is checked. No `native_decide`, unsafe code, new axioms, or evaluator oracle is used to prove correctness.

## Cost and scope

This is an exhaustive bounded reference extractor, not efficient reconstruction. Its entire tree catalogue can grow extremely quickly and be impractical even for small grammars. No benchmark, complexity improvement, or practical scalability claim is made for either this extractor or the separate dynamic-table method. The implementation does not identify their resource costs. Runtime controls use tractable global examples and height-two ordered/repeated-premise examples; unrestricted correctness is the general kernel theorem, not a claim that the large global ordered example was evaluated.

The standalone verifier certifies validity and claimed metadata/cost; it does not independently certify minimality. Minimality of extracted trees comes from the proved correspondence to the numeric compiler. No semantic truth, source authenticity, admission policy, Python compiler correspondence, integration, adoption, or research closure follows.
