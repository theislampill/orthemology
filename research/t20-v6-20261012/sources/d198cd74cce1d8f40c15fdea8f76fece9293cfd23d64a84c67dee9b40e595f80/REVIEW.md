# Independent internal AI semantic review

Reviewed 2026-10-09. Independent worker reviewed final sources and separately compiled all four new modules using the existing toolchain, writing only review outputs. This is internal AI review, not an external mathematical endorsement. The main package's full fresh dependency replay remains the authoritative reproducibility check.

## Outcome

No blocking semantic defect, circular minimum premise, assumed catalogue, universe mismatch, or vacuity error found.

Accepted scope:

- Shape constructs a finite syntax family from finite rule labels and each rule's finite ordered arity. Its decoded image is proved equivalent to branch height at most h, including nullary rules and height zero.
- With finite J and R, nonnegative rational occurrence prices, and an existing valid finite tree, `exists_minimum_exact` derives an actual same-judgement, exact-support global minimum over all valid finite trees. The height is `|J|(|S|+1)`. The proof selects a minimum only after constructing and establishing nonemptiness of the finite family.
- The inherited pruning argument preserves validity through equality of each ordered child support. It accommodates arbitrary, including nonmonotone, predicates of those supports.
- Ambient E genuinely need not be finite. The finite union of rule-local supports contains every tree support, yielding a uniform bound.
- Terminal cost thresholds and inventory-frontier thresholds correspond to unrestricted valid finite-tree witnesses. Reachable terminal costs attain a global minimum across eligible supports. Retained frontier pairs have actual original bounded-tree witnesses; residual support is correctly distinguished from original support.
- Controls are substantive: the finite example invokes attainment with E = ℕ and nonempty support; the infinite-rule example has positive rational prices, uniform height one, identical exact states, and no minimum.

## Scope restrictions

- Arbitrary guards means fixed predicates of rule labels and ordered child-support vectors, not predicates inspecting child syntax, child costs, derivation history or changing external inventory.
- Finite J is an explicit assumption of attainment and its displayed bounds.
- Supports are finite sets with union; costs count tree occurrences. Multiset/linear resources, DAG-sharing costs, infinite derivations and dynamically changing grammars are outside the encoding.
- Finite catalogues and filtering are classical/noncomputable. No effective guard decision procedure, executable enumerator or extracted witness-reconstruction algorithm is established.
- Inventory and future-acquisition inputs K and U are finsets. Terminal Pareto removal is justified after recursive guards have been validated; it does not justify substituting dominated supports inside arbitrary guards.
- No semantic/admission soundness, source authentication, original-discovery credit, metaphysical warrant, integration or closure follows.

## Independent verification

All four final new modules passed independent compilation with warnings treated as errors. The printed theorem dependencies contain only `propext`, `Classical.choice`, and `Quot.sound`, or subsets thereof. No admitted theorem, custom axiom, unsafe or partial declaration was found in the reviewed sources.

## Reviewed source SHA-256

- Catalogue.lean: 5cd7d3280d2c6f1399984d8cdb766bf8f27ea43113a4b2949d59e7e6887b476a
- Attainment.lean: 50a751c692ba04ca43574cf2c347f493531edb32b7fa2ac7d93aa6173b91b525
- Terminal.lean: 428dc2d2f37c4dca9470994f4fb9bdfdb332fd626fd2a0677017e861a376e69d
- Controls.lean: 5d7ada605582fdababff479cdfaf7a6fe460a489077e504b9fc6f6a9b51e3157
- frozen/GuardedTree.lean: 0a6faff768aa8aaa09dbddb48a155c7135d06b0762e522c7835d19d8c798d8b2
- frozen/Bound.lean: 8f7e1c4cc69a6354edb4d8e55f90aece93a22adf9c7ee733e685390f32c91a8c
- frozen/CertificateFrontier.lean: 5e799995b95e37105dff8dfe10e5ba78dfe44034334353bcf66107069e8a67e0
