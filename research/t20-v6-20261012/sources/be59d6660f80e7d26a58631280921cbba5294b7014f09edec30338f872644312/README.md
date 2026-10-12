# Literal shift probability checkpoint

Read `RESULT.md` for the exact theorem, original proof credit and remaining Python/host/bytecode boundaries. The five new modules are frozen in `SOURCE_PINS.json`.

This scoped supplement contains the five new source modules, the seven unchanged literal source inputs, the 34-source prerequisite build closure, source provenance, and observed author/independent-review logs and receipts. It does not duplicate the earlier ZIP or bundle the Lean/Mathlib installations. Compiled objects from the author/reviewer runs are intentionally omitted; their observed hashes remain in the receipts and all needed sources are included.

Independent review: `evidence/independent-review/REVIEW.md`. The root's main-module replay in `evidence/supplementary-root-main-check` is supplementary and is not another independent whole-dependency replay.

Run `python verify_integrity.py` (or `python -O verify_integrity.py`) to check frozen member bytes. This does not check mathematical proofs. To rebuild the proof, use a working copy, set the pinned Lean/Mathlib environment, then run `python build_prerequisites.py` and `python verify_final.py`. These are the portable replay entry points. The preserved independent-review script is the historical workspace harness and records its original paths; it is not the portable entry point.

The dependency acquisition record pins official Lean 4.19.0 and Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b. The original ordinary universal correspondence and probability proofs retain their credit. No protected repository edit, upload, integration or owner acceptance is implied.
