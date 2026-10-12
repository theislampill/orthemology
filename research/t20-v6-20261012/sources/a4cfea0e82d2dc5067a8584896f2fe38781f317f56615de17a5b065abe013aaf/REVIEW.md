# Independent full-E Sigma equivalence review

Verdict: PASS for the stated conditional, external-schema equivalence and its exact pointwise version. No blocking issue found. This is not derivability of eta or unrestricted elimination, not an internal source encoding of universal schemas, and not a new model.

## Meaning and scope

The three frozen candidate Lean modules were copied independently and compiled into this review's own lib with Lean 4.19.0 and --trust=0. Existing imported objects were reused; no baseline rebuild or protected change was made. Candidate hashes match the author's final freeze; reviewed-hashes.json binds candidate sources/report/check.sh, relevant retained sources, and all retained non-package objects on the replay search path. Package dependencies remain retained compiled dependencies, not a fresh baseline verification.

The central eliminator, reconstruction, branch substitutions and eta motive are literally imported SigmaCompletion definitions. FullE.elim_of_eta accepts only actual CtxE/FormE/HasE premises, including motive, dependent branch and input. Its full-E structural substitution and J transport have no original-Has restriction. Reverse implication instantiates the formed eta motive and canonical typed pair branch, giving the exact eta identity. IndependentPositive.lean composes both pointwise and uniform weak/strong equivalences and checks a fully arbitrary actual-E application.

Strong elimination includes raw PolyConv erasure to the branch on the projections. It is not a claim that this branch is independently typed at P(z). The separately proved canonical-pair identity supplies both endpoint typings. The raw erased computation is axiom-free; typed conversion is neither inferred from arbitrary raw erasure nor reflected back from HasE identity. RejectRawAsTyped.lean is a genuine expected type-mismatch rejection.

## Boundary and controls

The inherited no_eta_under_rigidity target is definitionally identical to the candidate target at [SigmaRaw,R], var 0. IndependentPositive checks that exact application and the actual var 1 proof of literal R. Inspected TaggedPER.has_sound/form_sound induction follows actual source recursors, including piExt/allExt. Thus the existing all-rule countermodel covers the new interface without re-proving soundness. Two-sided source nonderivability remains only the inherited R-to-Eta / R-to-not-Eta statement, not an unproved identification with external schemas.

The E-only context exclusion, motive exclusion in an original well-formed context, branch exclusion in an original well-formed telescope, and closed input-type exclusion are kernel-proved propositions. IndependentPositive rechecks all four plus combined elimination. RejectOriginalScope fails because the old interface requires original Ctx. The positive exclusions, not that elaboration failure alone, substantiate strict expansion. These canonical pair/constant-motive controls do not pretend to establish necessity for one particular branch; necessity is the all-motives converse.

## Replay and axioms

- replay.sh: all three copied modules pass --trust=0.
- test.sh: IndependentPositive passes; RejectOriginalScope and RejectRawAsTyped each fail with the expected type mismatch.
- Central pointwise/uniform equivalences and typed canonical computation: propext, Quot.sound only.
- Raw erasure and pair computation: no axioms.
- Inherited scope/model controls: propext, Classical.choice, Quot.sound.
- No sorryAx or new axiom appears in checked closures.

Logs are under logs/. Replay depends on the exact retained workspace ancestry listed by lean_path.txt and reviewed-hashes.json; it is intentionally not a standalone baseline build.
