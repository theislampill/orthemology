# Model contributions (sanitized public summary)

This project was developed by its owner working with AI assistants under explicit gating: the owner set scope, supplied worked examples, adjudicated disagreements, and made every recorded decision; assistant output only became canonical after review gates.

- **Drafting/formalization:** Claude Opus 4.8 and Claude Fable 5 (Anthropic), across owner-directed sessions in July 2026. The corpus records, honestly, that some passes initially misattributed their model identity; those incidents were caught by the owner, corrected with per-document provenance notes, and later verified from raw records. Attribution authority is the owner-observed harness, not cryptographic proof.
- **Reconciliation R1 (2026-07-19):** owner decisions D1/M1/O2 (see `../decisions/`) implemented by Claude Fable 5, with byte-exact patches, change ledgers, deterministic validation (29 checks), and hash-verified promotion. The exact private working-tree paths, session identifiers, and recovery records are intentionally not published; the public patches in `../../archive/reconciliation/` carry sanitized path labels.
- **Integrity:** current file hashes are in `RELEASE-MANIFEST.sha256` (verified by `scripts/validate_repo.py` in CI). The reconciliation patches reproduce the exact pre→post transformations of the three governed files.

No empirical claim in this repository originates from a model's self-assessment; experimental validation has not been performed by anyone, model or human.
