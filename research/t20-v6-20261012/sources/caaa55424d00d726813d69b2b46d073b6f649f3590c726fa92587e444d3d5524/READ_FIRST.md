# Constructive guarded witness kernel

`Witness.extract` returns actual finite minimum-cost trees for exact judgement/support keys, under the hypotheses in `SPEC.md`. `Witness.extractRound` gives bounded-height output. `Witness.accept` is an executable recursive tree verifier. The new constructive part is an exhaustive ordered-list reference extractor; it is potentially extremely expensive and is separate from the inherited dynamic-table method.

Read `RESULT.md`, `SPEC.md`, `REVIEW.md`, and `BINDING.json`. Run `./replay.sh` and `./check-mutations.sh` in this directory. The scripts use the pinned workspace Lean 4.19.0/mathlib installation. Dependencies are byte-identical copies under `frozen/`; predecessor directories are not edited.

Accepted source: `Enumeration.lean`, `Witness.lean`, `WitnessControls.lean`, `Main.lean`, and listed frozen dependencies. `development/` records failed/intermediate attempts; `mutations/` contains deliberately rejected alternatives. Neither is accepted proof evidence. Review outputs are separately bound to the exact reviewed accepted-source bytes. This package does not claim integration or closure.
