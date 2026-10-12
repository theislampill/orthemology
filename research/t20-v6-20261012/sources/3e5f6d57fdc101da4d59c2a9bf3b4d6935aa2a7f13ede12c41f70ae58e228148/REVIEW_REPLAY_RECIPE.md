# Replaying the independent covering/search review

## Original custody replay

In the original research workspace, with the accepted original source packages still present, run:

    bash tranche7-restart/reviews/covering-kernel-independent/replay_review.sh /absolute/new/output

The output directory must not exist. This runs both the frozen author suite and the independent reviewer suite and rehashes the original accepted packages and every Mathlib archive source file before and after execution. `check_bindings.py` intentionally requires those original files; it is a strict source-custody check, not a standalone public-archive wrapper.

The accepted frozen checkpoint is central-v2, manifest SHA-256:

    4b93bf89047342432837405ffacbff321da5c45f9bbc48e41ab58b2a173d0815

The authoritative local run is recorded in `FINAL_REPLAY.log` and `final-replay/FINAL_CHECKS.json`. Successful logs are separated from intentionally rejected mutant logs. Compiled local `.olean` files need not be distributed and must not be treated as proof-source substitutes.

## Portable replay from copied sources

A public wrapper may select different extracted file locations while preserving all source and review evidence bytes. Verify the checkpoint and review file manifests before executing. Requirements are official Lean 4.19.0 and Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b, with its pinned compiled libraries. Do not update dependencies.

Let CANDIDATE point to the extracted central-v2 directory, REVIEW to the directory containing these reviewer files, and OUT to a fresh absolute output directory. Set LEAN_419 to the official compiler and MATHLIB_C44 to the pinned Mathlib installation. Then:

    bash "$CANDIDATE/verify.sh" "$OUT/kernel"
    export COVERING_BUILD_DIR="$OUT/kernel"
    bash "$CANDIDATE/lean.sh" -o "$OUT/kernel/IndependentChecks.olean" "$REVIEW/IndependentChecks.lean"
    bash "$CANDIDATE/lean.sh" "$REVIEW/AllAxioms.lean"

For the primary-interface mutant tests, set LEAN_PATH exactly to the fresh kernel output plus the pinned Mathlib libraries and package-library directories, then run:

    python3 "$REVIEW/check_primary_mutants.py" "$CANDIDATE" "$OUT/primary-mutants" "$LEAN_419"
    python3 "$REVIEW/independent_semantics.py" "$OUT/SEMANTICS.json"
    python3 -O "$REVIEW/independent_semantics.py" "$OUT/SEMANTICS_OPTIMIZED.json"
    cmp "$OUT/SEMANTICS.json" "$OUT/SEMANTICS_OPTIMIZED.json"

Require exit zero for successful stages, six deliberately rejected primary mutants and six rejected author mutants. Successful proof logs must contain no errors, warnings or `sorryAx`. `AllAxioms.lean` prints 100 author declarations; dependencies are limited to propext, Classical.choice and Quot.sound, or no axioms. The independent theorem audit prints 14 selected reviewer theorem declarations with the same allowed axiom set. Deliberately rejected mutant logs contain expected errors and may print `sorryAx`; never import their output as trusted modules.

In the public wrapper, verify copied accepted input/dependency hashes against the preserved bound manifests, rather than claiming to have accessed unavailable original workspace locations. The independent receipt records the stronger original-workspace custody verification already completed. Preserve that distinction in replay reporting.
