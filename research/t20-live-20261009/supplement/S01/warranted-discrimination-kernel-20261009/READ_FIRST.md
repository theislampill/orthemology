# Canonical frontier theorem: kernel checked

`RESULT.md` gives the exact scope and boundaries. `CertificateFrontier.lean` proves the core inverse/canonicity theorem and all four clauses of the original Theorem 1 at the support/cost-pair level, including inventory and per-verdict wrappers.

`Controls.lean` proves counterexamples to cost-blind pruning, present-cost-only state, and collapsed infinite-price semantics. `mutations/` contains the matching deliberately false claims; replay requires their specific semantic rejection.

Run `bash replay.sh`. See `kernel.log`, `CHECK_RESULTS.json`, and `independent-review/REVIEW.md` for checks. `BINDING.json` identifies exact inherited inputs and frozen source hashes.

No semantic warrant, Bellman planner, proof-object reconstruction, or philosophical application is kernel certified. No integration or programme closure occurred. `development/` preserves exploratory diagnostics and is not part of the accepted proof surface.
