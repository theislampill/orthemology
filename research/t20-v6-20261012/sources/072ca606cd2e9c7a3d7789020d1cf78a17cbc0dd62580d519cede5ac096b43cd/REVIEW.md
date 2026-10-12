# Independent semantic review

Verdict: PASS for the two literal implication exclusions in unchanged HasE, inherited by Has. No blocking mathematical defect found.

Frozen candidate CompletionSeparation.lean: fcda14a453a363f3d51a62549ea3e67f3690d29b9889179fc4f55fe3f0be7a07.
Reviewed RESULT.md: 9ed64aed3f8ead14e4522891426375f2120373778e8916bd651b48f822ef5be8.

## Proof audit

- The independent positive control checks the exact definitions of Eta (Pi over Sigma Raw Raw, with the literal pair-of-projections identity) and Rigidity (all endomorphisms preserving zero and successor). No compiler-specific surrogate replaces Rigidity.
- In the retained homogeneous Henkin interpretation, Raw is universal; hence the literal Eta validity proof uses True and K reduction. This is semantic validity only. The generic componentwise_eta theorem separately assumes saturation laws at A and at B in the fixed first-projection environment, exactly matching the dependent Sigma clause. It neither substitutes the second pair's first projection into B nor presupposes raw pair eta.
- henkin_result_empty correctly projects the underlying NT relation from the identity, applies it to the retained nonstandard nu, then the existing eligible atomPER and scalar step. The explicit I reduction transports the resulting conversion into the retained scalar_not_convertible contradiction. The source compiler endpoint is unchanged.
- henkin_rigidity_empty applies retained whole-HasE soundness to the included original Has derivation Rigidity → ResultAt(originalQ). The empty type environment has an explicit retained admissibility proof; the two zero term environments satisfy the empty context by reflexivity. No additional formation, parametricity, coherence, or extended-rule soundness hypothesis is introduced.
- no_eta_to_rigidity applies that same soundness theorem to an arbitrary hypothetical source proof, and feeds its arrow interpretation the Henkin Eta witness.
- no_eta_to_not_rigidity uses the retained FullPER soundness theorem and simultaneous literal Eta/Rigidity witnesses. Bottom is False. This proves external noninhabitation of the internal implication-to-negation type, not an inhabitant of a source negation.
- The opposite orientation Rigidity → Eta remains inherited from the prior tagged model. Tagged Raw is conversion and Sigma carries a tag; FullPER Raw is conversion but Sigma is componentwise; Henkin Raw is universal with a restricted polymorphic universe. The report discloses these differences and does not claim a faithful-Raw Henkin separator.

## Independent validation

Fresh isolated output directory, Lean 4.19.0, --trust=0. Candidate, supplied controls, and independent positive controls compile successfully. Printed axiom sets for all candidate named theorems contain only propext, Classical.choice, Quot.sound.

Three separately compiled expected-rejection files fail for the intended reasons: semantic Eta cannot be assigned a HasE typing; Henkin emptiness cannot be transplanted across different term carriers to FullPER; the universal-Raw Eta proof cannot be applied to TaggedPER. The model-transfer test is expressly a signature check, not a separate semantic separation result.

REVIEW_RECEIPT.json records exact candidate/report hashes, verified retained-source hashes, resolved hashes for twelve critical retained compiled modules, file/log hashes, and exit codes. Retained dependencies were not rebuilt. An initial setup probe for Boundary failed due to a missing TaggedPER search path, then the additive replay used the corrected retained paths; no retained source or binary was edited.

## Scope

The report's literal-premise conclusions are justified. Reading “independence” as independence of all full external completion-rule extensions would not be justified: the single Eta type does not quantify over all dependent types or motives, and these proofs do not establish soundness of an extended calculus. RESULT.md explicitly retains that limit. No closure, source reflection, completeness, or additional axiom is established.
