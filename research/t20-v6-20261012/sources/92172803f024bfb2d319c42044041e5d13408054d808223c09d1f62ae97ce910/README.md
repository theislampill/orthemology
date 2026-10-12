# Independent cooperation review

Read `REVIEW.md` for the semantic verdict and `FINDINGS.json` for dispositions. `VERIFICATION.json` records exact independent commands and receipts. `SOURCE_BINDINGS.json` limits the direct source-reading claim.

The review binds author manifest SHA256 ebd5775a8177a33884aceb0f07da982232aed1526dec662ea0330893da3d727b. `frozen-author/` contains the bound packet; `replay/` contains reviewer-owned execution copies and generated outputs. No original author or historical artifact was modified.

The seven new Lean controls are in `src/IndependentScope.lean`. Independent finite calculations are in `src/independent_checks.py`. To reproduce, use a fresh workspace copy retaining the sibling author packet and existing Lean 4.19.0 location, then run `python src/verify_frozen.py` from this review directory. This refreshes review-local receipts; do not run it over the sealed review if preserving its final bytes matters. It checks the author packet read-only and executes copies only.

The verdict is bounded research completion with a narrowed philosophical residual. It is neither full-model certification nor universal impossibility.
