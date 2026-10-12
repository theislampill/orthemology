# Result

A constructive reference extractor now returns actual finite guarded proof trees with the same minimum prices as the executable numeric table compiler. This closes the numeric-output-to-returned-witness gap at the level of the fixed finite grammar semantics.

## New checked work

- `Enumeration.lean`: explicit complete rule lists; ordered Cartesian list enumeration (including one nullary tuple); decoding and bounded-tree coverage without equality on trees.
- `Witness.lean`: executable structural validity checker and exact key/cost verifier; first-match search; bounded soundness/completeness; exact numeric output projection; global minimum and no-tree equivalence under nonnegative prices.
- `WitnessControls.lean`: runtime inspection and verification of actual returned trees, with corrupted-tree rejection.

The global semantic bridge, rational dynamic-table minima, and finite grammar height bound are inherited from the separately frozen predecessor. The new contribution is executable constructive output and its correspondence proof, not a new proof of those inherited mathematical results.

## Runtime observations

The local fresh replay checks eleven frozen and four new Lean modules with warnings as errors. Twenty-three witness runtime checks pass twice, through `#eval` and `--run`; the frozen numeric controls also run. Concrete returned trees include:

- Ordered children: `3(0(),1())`, cost `1`, three rule occurrences.
- Repeated premise occurrence: `4(0(),0())`, cost `7/6`, three occurrences. The repeated leaf is charged twice.
- A cheaper global proof: `2(0())`, cost `1`, replacing a price-10 one-node proof.
- Seeded zero cycle under reversed rule order at height four: `true(true(true(false())))`, cost `0`, four occurrences. The same rule order at height one returns `false()`, cost `0`, one occurrence.

Unsupported zero cycles and false nullary guards return no tree. Validity verification rejects reversed premise order, incorrect repeated cost, wrong exact support, wrong root judgement, wrong child judgement, and a false nullary guard. Both a free empty support and a dearer required exact support remain available. Height-zero and empty Cartesian-product boundaries are checked. Negative prices are tested only for bounded rounds; the global theorem requires nonnegativity.

Three changed semantic implementations are rejected by the kernel at their correspondence/completeness obligations: dropping validity checks, removing the nullary tuple, and weakening exact support equality to subset inclusion. Rejected mutation files may contain error-recovery `sorryAx` output; no accepted-source replay contains it.

## Limits

This uses exhaustive bounded tree enumeration after computing a numeric price. The tree catalogue can be prohibitively large. Global runtime controls use tractable examples; the ordered/repeated controls use height two, not their much larger global tree enumeration. No practical scalability, reconstruction efficiency, or shared resource-cost claim is made.

The checker independently validates a tree and its claimed metadata/cost. The extractor's correspondence theorem supplies minimality. Guards may be arbitrary decidable functions of the fixed ordered child supports; no monotonicity is needed. No unsafe support pruning or DAG/shared-node reinterpretation is used.

First-match ties minimise cost only. Increasing the requested round can change tree identity and increase its size even after numeric prices stabilise. There is no node-minimality, canonical proof, or witness-stability claim. The fixed-bound global extractor is deterministic relative to the complete rule-list order.

This establishes grammar-internal structural/cost correctness only. It does not establish source truth or authenticity, domain-semantic warrant, admission soundness, correspondence with the Python prototype, integration, adoption, or research closure. No predecessor is modified and no historical work duration is inferred.

Independent final source review status is recorded separately in `REVIEW.md` and its bound receipt; it must be consulted before treating the package as fully verified.
