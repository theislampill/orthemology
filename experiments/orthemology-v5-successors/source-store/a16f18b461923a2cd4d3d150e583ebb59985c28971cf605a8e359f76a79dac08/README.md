# Recursive dependent All context completion

The package contains unchanged accepted source dependencies plus a new recursive dependent-All calculus, proofs, exact-code interpretations, compatibility translations, and controls. `PROOF_GUIDE.md` explains the mathematical dependency order and precise scope. The complete frozen bounded contract is independently accepted in `review/REVIEW.md`, with exact evidence in `review/VERIFICATION.json`. This is automated independent qualification, not human-specialist validation or U11 closure.

## Reproduction

Required existing environment:

- Lean 4.19.0, executable SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`
- Mathlib revision `c44e0c8ee63ca166450922a373c7409c5d26b00b`
- An existing environment script exporting `LEAN_ROOT` and the pinned dependency `LEAN_PATH`

Set `TOOLCHAIN_ENV` to that script, then execute `scripts/reproduce-all.sh`. No helper installs, downloads, bootstraps, or repairs the toolchain. Each module invokes the exact verified binary through `LEAN_ROOT`, uses `-j1`, default heartbeat/recursion limits, and a 180-second timeout. Fresh timestamped `reproduction-logs/` entries contain source digests and process exits; preserved scientific `logs/` are never modified. Historical scientific replay helpers remain under `historical-scripts/`; `FINAL_REPLAY.json` refers to that scientific run, while `PACKAGING_SUCCESSOR.json` separately binds the public helper successor. The scripts are independent of the extraction directory and do not call an unverified `lean` found on PATH.

`dependency-order.txt` lists source modules in import order. `SOURCE_IDENTITIES.json` binds exact source bytes. `ACCEPTED_INPUTS.json` identifies the unchanged 47-module accepted nucleus dependencies. Source-only archives exclude `.olean` and other compiled caches.

## Interpretation boundary

This is an explicit extension up to grammar translation. Old nucleus AllFinite becomes recursive All; source polynomials remain literal. The broader legacy comparison applies to support-certified retained Type-valued derivation trees, not arbitrary hidden provenance in Prop-valued typing or conversion proofs.

No universe, Type:Type, normalization, canonical unary carrier repair, source equality reflection, arbitrary frontend, full U11 closure, or real-bearer identity claim is made. Standard Lean axioms are allowed; sorry, custom axioms, and unsafe substitutes are not.

## Independent checks and public projection

The complete independent review and exact bound sources are under `review/`. Use `review/public-portable/scripts/reproduce-module.sh` for fresh public review-module reproduction, after the manifest dependencies have been built. The historical review wrapper bodies are omitted from this public selection; their exact hashes remain in the acceptance receipts and their originals remain in the accepted private archive. Use the portable public helper for reproduction.

The public archive is a separately identified projection of immutable accepted source/evidence. All proof sources and acceptance reports remain exact. One failed historical transcript containing machine installation roots is omitted; its clearly labeled normalized transcript preserves all diagnostics and the failure exit. `review/public-portable/PUBLIC_LOG_PROJECTION.json` binds original and normalized hashes and safe-alias replacement counts. This does not turn that historical failure into success. The original raw transcript and accepted private archive remain preserved separately and are not embedded in the public archive.
