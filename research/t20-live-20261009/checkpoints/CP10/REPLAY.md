# Portable replay, without modifying frozen work

Use Python 3.12.14 with numpy 2.3.5 and mpmath 1.3.0 to reproduce the observed byte outputs. The standard-library finite programs require neither third-party package. This packet installs or downloads nothing. Exact floating output matches are environment-specific diagnostics, not interval-certified numerical theorems.

From the extracted checkpoint root:

    python3 PACKING/check_manifest.py
    python3 PACKING/replay_python.py --output [OMITTED_PRIVATE_MACHINE_PATH]

Use an output directory outside the extracted root, without an existing REPLAY_RECEIPT.json. The harness copies all payloads to temporary scratch, preserving sibling paths, deletes generated outputs only in that copy, executes exactly five programs, records stdout/stderr and output hashes, and checks that frozen inputs stayed byte-identical. Assertions are enabled. No historical predecessor science or Lean code is rerun.

For a fresh safe extraction from an already extracted trusted helper:

    python3 PACKING/safe_extract.py /path/to/checkpoint.zip [OMITTED_PRIVATE_MACHINE_PATH]

The extractor requires a new destination and rejects duplicate/unsafe names, traversal, backslashes, absolute names, symlinks, unusual device files, encrypted entries, multi-root or undeclared members before writing. It verifies the manifest and all member hashes without executing archive code. Then run the separate manifest checker for final result/review relationships. Internal consistency alone is not trusted provenance; check the external archive hash against the expected delivery before executing its scripts.

To repeat the expected-rejection tests, using a trusted helper:

    python3 PACKING/integrity_controls.py /path/to/checkpoint.zip

MANIFEST.json hashes every payload except itself and MANIFEST.sha256. MANIFEST.sha256 binds that manifest. The external validation receipt binds the ZIP hash, manifest identity, safe extraction and fresh replay without circular hashing. The external receipt also records deliberate mutation, missing/extra-member, traversal, absolute-path, duplicate-member and symlink rejection controls.

Current shared review bindings govern likelihood/count acceptance. Historical initial bindings remain included unchanged and are explicitly superseded. Finite review binds the final RESULT hash 6687a8f2f56290427297bba1cfef6c8c14a58878ffa0010805550f0cd632b0d5. External predecessor source hashes were checked against the ninth Scope_Clarified archive or its delivered guide; none of their mathematics is bundled again or newly replayed.
