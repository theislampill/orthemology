# Independent review: literal Sigma/Pi cross-typing observer

10 October 2026. **PASS for the bounded dual-typing source construction and its explicitly conditional semantic obstruction.** No author theorem defect was found. This review is separate from the earlier fixed-carrier core review.

## Exact reviewed artifact

The author confirmed the frozen source hash `10051b9df50fce7fef173bbe1cffe111cdc70529a29386753b8c872bf4789ba8` for CrossTypedObserver.lean and the historical fresh-object hash `c3b3addcf23fb3e8b2d6885cf9f3b980dbf793a650125cc914f7c8cd1e46e5ac` before independent replay. Both matched. The frozen source was copied into this review, and the author manifest was independently verified.

Only the new cross-typing author module and two new reviewer modules were compiled. The typed-observer core, InternalGraph, and baseline objects were reused without rebuilding or modifying them.

## Source construction audit

The generic input hypotheses are original P01AC.Has derivations n:N, a:B, b:B in an actual source telescope. B need not be term-independent, type-closed, or Raw. The final identities are actual HasE judgements via the existing inclusion. This is not a generic theorem taking arbitrary HasE input proofs.

The source definitions and both typing paths were read directly:

1. Product(B) is Sigma B (wk B), not Sigma B B when B has term dependencies. Its second component type in Sigma introduction is appropriately instantiated through inst_wk.
2. ChurchPair(B) is (B→B→B)→B. The proof gives the **existing literal pairPoly** this type using typed I, K, S, and typed Pi applications. It neither substitutes another encoding nor assumes an isomorphism or a conversion bridge between the carriers.
3. The exact step K(pairPoly b b) and seed pairPoly a a are typed at both carriers. n is instantiated at each source-formed carrier separately through the retained actual allElim proof.
4. The Sigma route ends in sigmaFst. The Church route applies the result to a typed K selector. Since fstPoly is literally application to K, both routes have exactly the same original polynomial and result type B.
5. same_endpoint_identity directly supplies these two endpoint derivations to actual HasE.identityIntro and reflexive PolyConvPlus. The executable dependency audit confirms all four direct references. It is not merely a separately stated equality of pretty-printed expressions.
6. Numerals zero and one produce open source conversions to a and b. All endpoint typings and formations are then supplied to actual HasE identities at B. The first displayed source identity uses the Sigma typing, and the second uses the Church typing.

Inspection of all 68 direct declaration bodies in the new author namespace finds no original or extended Raw typing/erasure rule. As in the predecessor review, this is a direct-body and actual proof-path claim, not an assertion that structural induction infrastructure omits every constructor of the old grammar from its transitive dependency graph.

## Independent source controls

CrossReviewControls.lean expands the final endpoint as the literal application tree

`((n (K (pairPoly b b))) (pairPoly a a)) K`.

Its equality with the author observer is definitional (rfl), and the exact tree receives both typing routes.

A formed dependent source type B=Id_(param 0)(var 0,var 0) in Γ=[param 0] checks the nested arrow and Sigma bookkeeping. The controls construct both pair typings, both constant-step typings, both final observer typings for every source numeral, the same-endpoint HasE identity, and the exact zero/one HasE identities. The Product second component demonstrably contains var 1. A fixture incorrectly leaving it at var 0 is rejected. A separate fixture identifying the Sigma and Pi carrier syntaxes is also rejected.

## Semantic boundary

The set-level rejection assumes the displayed equality

`sigmaObservation ns a b = churchObservation nc a b`.

Together with a≠b and the opposite zero/one computations, the contradiction is direct and has no axioms. The source dual typing explains why a candidate interpretation with the stipulated compositional equations and derivation-independent judgement values must provide that equality. The Lean source theorem does not itself construct such a semantic interpretation or derive that equality from arbitrary unary membership soundness.

The report's alternative identity-soundness route is likewise explicitly sufficient: the interpretation must assign equality-valued meaning to the particular identity while interpreting the two endpoints according to the two supplied typing routes. The reflexive source endpoint alone is not silently turned into that semantic contract. No arbitrary isomorphism naturality, graph preservation, carrier-set equality, or generic parametricity premise was found in the source theorem.

An independent local control admits the incompatible zero/one operations in unrestricted unary membership predicates at the two displayed function spaces, while their observations remain distinct. This is only a countercontrol to the claimed inference from bare membership; it is not a model of the complete source grammar. A fixture asserting equality of those opposite observations is rejected. With singleton D, the split does agree, confirming that a≠b is essential.

The ordinary full function spaces in the displayed set calculation do not establish full-function-space admissibility in a Henkin model. Such a model must provide the actual required elements and interpretation equations. Likewise the author's Unit-as-Raw conjunction is a local set control, not a whole-source singleton-Raw model.

## Sharp retained limitation

The review proves that **all positive counts agree for this particular constant-update observer**. In particular, Sigma count 1 and Church count 2 have equal Bool-valued observations despite their unequal counts. Zero returns a; every positive count returns b because the update discards its argument.

Thus this observation rejects a zero/positive split under the stated coherence contract. It does not classify all coordinate counts, establish count uniformity, or rule out candidates assigning different positive counts. This is a boundary control only; no additional observer variant or count-classification task is pursued here.

## Replay and custody

Positive compilation order:

1. frozen/CrossTypedObserver.lean
2. CrossReviewControls.lean
3. CrossReviewDependencies.lean

All three compile with Lean 4.19.0 --trust=0, with no warnings, errors, or sorryAx. The executable full dependency audit permits only inherited propext, Classical.choice, and Quot.sound. Both author no-shape-split implications and the review's positive-count control have no axioms.

Three intended rejection fixtures fail at the expected boundary:

- RejectCarrierIdentification: Sigma/Pi carrier identification is not definitional equality
- RejectMembershipAsCoherence: opposite Bool observations are unequal
- RejectUnshiftedProduct: B's dependent second component requires wk

The replay binds 95 inherited source/object pairs to historical receipts, verifies the Lean binary and retained prerequisites, and checks 235 original file pins before and after execution. No typed-core or baseline module is rebuilt. The author packet, completed core review, and all checked predecessors remain unchanged. Independent rebuilt objects receive their own hashes; relocated outputs are not falsely required to have the historical object digests.

Run `python hase-cross-typing-review-20261010/replay.py` from the shared workspace. This writes only a fresh directory beneath this review's validation directory. REVIEW_RECEIPT.json identifies the final evidence. This review introduces no protected edit, integration, audit acceptance, closure, publication, or field-novelty claim.

## Open frontier

The original graph projection bridges, universal HasE W, and its negation remain OPEN. This packet supplies neither a whole-source model nor a whole-source model refutation, arbitrary naturality, scalar fusion, or source noninhabitation.
