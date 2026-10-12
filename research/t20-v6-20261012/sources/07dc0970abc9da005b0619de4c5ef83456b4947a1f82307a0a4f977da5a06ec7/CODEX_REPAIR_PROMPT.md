# PR #33 — bounded owner-authorised review repairs; same PR, no merge

Continue your existing `theislampill/orthemology` PR #33 and branch. The reviewed head is `aba0bce3d651ab7f09cb9aa6a31c395e31e900fc`, based on `3a0bdeaa1394c656245cae9599adcb143e885059`. This message authorises the narrow corrections below. Do not restart the integration or create another PR. Keep this review packet, RLGWO and DAG private.

The independent review reconstructed the full 2,068-file public subtree and matched the actual GitHub tree. Preserve that successful work. This is a publication repair, not a new tranche, philosophy comparison or historical scientific replay.

## 1. Fix the exact remote CI failure

Both runs 37933144539 and 37932931210 failed the internal-reference gate. See `UPSTREAM_REFERENCE_FINDINGS.json`: four occurrences, three upstream paths, three CP21 files.

- `docs/auxiliary_axioms.md` in CP21 `REFERENCE_ONLY_CODE.json` and `spinoza-formal-transfer-screen-20261009/READING_LEDGER.json`.
- `docs/coverage.md` and `docs/gaps.md` in CP21 `spinoza-formal-transfer-screen-20261009/sources/README.md`.

These paths belong to `Nakammura/spinoza-ethica-lean@6d4c0461265e50a3bbedb640fe60d9ad292b50a7`. Qualify that external ownership in the derived public records with accurate pinned upstream locators. Preserve path-versus-URL field semantics; rename/add a field only where needed, and record the exact mechanical transformation. A URL's label must not inadvertently retain the same falsely native bare path. Original bytes and hashes remain private/historical.

Do not fix this by creating dummy root docs, excluding `research/` from validation, weakening tests, or making broad path exemptions. Do not merely repeat the failed Markdown escaping. Use the existing parsers to test the corrected occurrences.

## 2. Enforce the delivery/privacy boundary

`PRIVATE_METADATA_FINDINGS.json` is a values-free inventory of 217 opaque identifiers across 39 files. Withhold these two delivery-only records from the public projection, preserving them privately:

- `research/t20-live-20261009/checkpoints/CP21/prior-checkpoint-identities/T20_Resumed_Research_Intermediate_Checkpoint20_20261009.LIBRARY_DELIVERY.json`
- `research/t20-live-20261009/checkpoints/CP22/prior-checkpoint-identities/T20_Resumed_Research_Intermediate_Checkpoint21_20261009.LIBRARY_DELIVERY.json`

In other required reports, remove or neutralise private Library/file/message linkage values. Preserve substantive content and public source identities. Use consistent distinct aliases or archive/member hashes where equality/identity matters; do not collapse separate sources or JSON keys to one marker. Keep original-to-public mappings private and disclose the projection changes without re-exposing IDs. Check JSON validity, duplicate keys, affected bindings and counter totals.

These identifiers are not reported as passwords or access tokens. Do not launch a security incident, unrelated identity search or history rewrite. A corrective commit does not erase the old public commit. Stop for a separate owner decision only if a genuinely new sensitive-data or credential issue appears.

## 3. Restore the exact copied component's licence

Copy `UPSTREAM_LICENSE_TO_RESTORE.txt` byte-for-byte to:

`research/t20-live-20261009/checkpoints/CP21/spinoza-formal-transfer-screen-20261009/sources/LICENSE`

Expected SHA-256: `47b99d4833f7c801c29bdf0e0c8488a6e9f5f5fd26d0a54a816982b783b7e837`; 1,188 bytes. `LICENSE_RESTORATION.json` gives the original pin. This file already exists in CP21's private archive; no new source campaign or repository-wide licence choice is authorised.

## 4. Complete only the affected integration work

Update affected projection records, source/public hashes, checkpoint counts, omissions, publication notes and PR body. Keep original source/replay hashes scoped to originals; do not portray redacted records as newly kernel-verified. Preserve T20 ACTIVE and all stopped/deferred research boundaries. Retain the approved CSV exact-byte rule and previous small publication repairs.

Stage new/changed public paths before running the supported derived-state and release-manifest generators. Verify authored/scientific state remains unchanged. Do not modify frozen result/source registries, validators, CI configuration or dependency pins. If an additional existing file truly must change beyond the already authorised generated state/manifest, present the smallest patch and reason rather than expanding the programme.

Run locally, using the existing environment:

    python -B tests/test_internal_references.py
    python -B scripts/validate_internal_references.py
    python -B scripts/generate_current_state.py --check
    python -B scripts/validate_v5_successors.py
    python -B scripts/validate_repo.py

Also check the new public bytes against amended hashes, the exact licence, the values-free privacy inventory, JSON keys, unchanged source files and allowed diff. Preserve the already disclosed historical whitespace rather than rewriting proofs.

Push one narrow repair commit to the same PR and inspect required GitHub CI. Both original runs stopped before the PDF rebuild and final successor gate; those SKIPPED steps are not passes. If another gate fails, diagnose only that failure and disclose it. No replay of all checkpoints, no Lean installation for these publication changes, no broad parallel re-audit.

Return the new head, changed-path summary, scoped test results, exact CI URLs/status and remaining issues. **Do not merge or enable auto-merge, and do not tell Dot the new baseline is merged.** Return for review of this repair delta. Keep further live checkpoints outside this frozen PR unless I explicitly add them.
