# 10 DAEE Implementation Boundary

Source-reader extracts for the 11 October 2026 catch-up. This is a reading aid, not a canonical T20 consolidation or a new research result. Original source wording and historical status are retained below; later documents may supersede earlier ones. Each source is identified by its original archive path and SHA-256.

---

## Source 1d3a7cb173

Original location: `T20bigupdateprev(1).zip!/noetic-recognition-guard-intermediate-20261009.zip!/noetic-recognition-guard-intermediate-20261009/README.md`

SHA-256: `1d3a7cb173ed369681edb5db365e2c4e29bb799a56f619c34e4e4985d3c0bee8`

### Original document

# Noetic recognition guard: intermediate research packet

**Status: T20 intermediate. No repository integration, protected change, release qualification, or T20 closure.** The patch is unapplied to the pinned source. Applying it to disposable local test copies is part of replay only.

## What this packet establishes

At pinned commit `c86b3c6673147b8802fe222373a165a37d4d24a8`, a complete-schema-valid advanced/strong control passes the custom validator. Changing only recognition to medium, weak, or none produces a complete-schema failure while both original custom CLI entrypoints still return success. A narrowly scoped seven-line candidate guard repairs those controlled false passes; strong, missing-field, and nonadvanced controls retain their intended outcomes.

The official embedded positive has a separate category-3/open-gate schema mismatch. It is retained and remains unfixed. Two necessary module-map entries are reconstructed from pinned compiler inputs. This is not a whole runtime rebuild, full CI run, complete-schema-coverage proof, live-model test, or finding about anyone's knowledge, willingness, restoration, or warrant. Existing runtime/interlocutor witness distinctions remain preserved in the bounded tests.

## Read first

- `STATUS.json`: machine-readable scope and intermediate status.
- `evidence/noetic-correction-semantics-20261009/REPORT.md`: author's finding and candidate repair.
- `evidence/noetic-guard-peer-review-20261009/REVIEW.md`: independent finding review.
- `evidence/noetic-guard-repair-peer-review-20261009/REPAIR_ADDENDUM.md`: independent, hash-bound repair review.
- `evidence/noetic-correction-semantics-20261009/UNAPPLIED_RECOGNITION_GUARD.patch`: exact unapplied candidate.

Original source bindings, fetched source copies, fixtures, test scripts, per-command logs, results, and original manifests are retained byte-for-byte. Python bytecode caches are omitted. Saved command paths in historical evidence describe the original execution locations; use the portable wrapper below for a new replay. Earlier philosophical reports mentioned by the author are inherited background and are not re-derived or required by these structural tests.

## Exact fresh-extract replay

Prerequisites: Python 3.12 (tested with 3.12.14), `jsonschema` 4.26.0, and the standard `patch` executable. This archive contains all task-specific source inputs, scripts, fixtures, and reports; it does not vendor the Python runtime or third-party package. No network access or repository checkout is needed for replay. The wrapper never installs dependencies or edits the archived evidence.

1. Extract the ZIP into a new directory and enter its `noetic-recognition-guard-intermediate-20261009` root.
2. Run: `python -B verify_and_replay.py --verify-only`
3. Run: `python -B verify_and_replay.py --work-dir private-locator:3ab79175a565ad0d292e`

Choose a work-directory path that does not already exist. Alternatively omit `--work-dir` to allocate a fresh temporary directory automatically. The wrapper verifies the root and original nested hash manifests, then creates three independent disposable copies. It runs the author's three scripts, the independent finding replay, and the independent repair replay. Each group gets an untouched evidence snapshot, so one group's regenerated result paths cannot invalidate another group's historical manifest.

Success prints a JSON receipt with `status: PASS`, all five command exit codes equal to zero, the manifest digest, dependency versions, source/patch bindings, and the fresh log/result paths. Individual intentionally failing validators are asserted inside those five successful test drivers. The receipt is written to the new work directory as `REPLAY_RECEIPT.json`. Archived files are hash-checked again afterward.

For an audit of exact commands, inspect the new work directory's `command-logs/` and each group's generated JSON results. Original scripts are also individually executable within their retained sibling-directory layout, but several overwrite their own result files; use the wrapper to preserve the historical evidence.

## Hash discipline

`SHA256SUMS` binds every packet file except itself. `EVIDENCE_SNAPSHOT.json` records the copied originals. Each evidence directory retains its original `SHA256SUMS`. Verify the ZIP's separate SHA-256 receipt supplied with the archive before extraction. Hashes are integrity bindings, not authenticated remote attestations.

Patch SHA-256: `ba1c28f70bc74b70451ae4a63910f49308a23d5b068d1a3e61c8cb0bf9c97a58`.
Checker preimage SHA-256: `ea6630a53ce8c77d6cc3102ae6ffd5aba0dc84539f1ffe5350fbc1aa4d9c4d1a`.
Checker candidate postimage SHA-256: `303297476f2d69b85019adf203949b49d6034a64d58ad7022321b999ac7d0059`.

