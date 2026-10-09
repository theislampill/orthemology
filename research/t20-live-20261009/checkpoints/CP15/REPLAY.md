# Offline integrity checks and optional Lean replay

This procedure qualifies the preservation package. It does not re-establish primary-source comprehension, premise warrant, metaphysical adequacy, novelty, historical duration, owner acceptance or T20 closure.

## Verify and extract safely

1. Compare the ZIP SHA-256 with the external READ_FIRST/receipt from a trusted channel before executing packaged code. The manifest inside an untrusted archive cannot authenticate itself.
2. Inspect `PACKING/safe_extract.py` as inert text if obtaining the extractor from this ZIP. It is the reused checkpoint-14 standard-library helper. It rejects unsafe paths/file types, duplicate/missing/extra members, checksum failures and an existing destination; it verifies the manifest before writing. It does not execute archive code.
3. Using Python 3, run the inspected helper against the ZIP and a new empty-location pathname: `python -B safe_extract.py ARCHIVE.zip /path/to/new-extraction`.
4. In the extracted checkpoint root, run `python -B PACKING/check_manifest.py`. No original workspace or predecessor archive is needed for this payload/relationship check. External dependencies are explicitly optional provenance entries, not missing payload.
5. Optional packaging-negative checks: `python -B PACKING/integrity_controls.py /path/to/ARCHIVE.zip` and `python -B PACKING/binding_controls.py`. These create disposable altered copies and demand rejection; they do not modify the sealed ZIP or execute research proofs.

The manifest enumerates payloads; `MANIFEST.sha256` binds `MANIFEST.json`. It intentionally cannot bind its own bytes. The external archive digest seals both. Predecessor archive/member hashes were checked during assembly and are recorded without recursively embedding archives.

## Four-file Lean4.19 qualification

Use an already installed, trusted Lean **4.19.0** executable. Do not bundle/rebuild the toolchain, install dependencies or run historical proofs for this checkpoint.

From the extracted root, run:

`python -B PACKING/replay_lean.py --lean /absolute/path/to/lean-4.19.0/bin/lean`

The script first executes `lean --version` and rejects versions other than4.19.0. It verifies each file against the preserved root replay hashes, requires exactly `import Std`, rejects `sorry`, `admit` and `native_decide`, then runs only:

- `plural-explanation-theorem-audit/DependencyAudit.lean`
- `plural-explanation-theorem-audit/SupplementedControl.lean`
- `particular-explanans-bridge-audit/RestrictedBridgeControl.lean`
- `particular-explanans-bridge-audit/BridgeRepairs.lean`

All runs must return zero without `sorryAx`. Printed axiom dependencies are retained in the external qualification receipt. Standard logical axioms used by some results are disclosed; the files introduce no new dependencies. No `.olean` output option is requested, and fresh qualification uses disposable extraction. `source-noncirculation-feedback/sources/extract_reacquired.py` is retained historical extraction provenance only and is not run.

The regular-open realization is written mathematics, not formalized by these files. Successful replay verifies the exact formal statements under their stated assumptions. It establishes neither actual-world explanatory premises nor an actual Necessary Being or uniqueness. Internal review remains internal.
