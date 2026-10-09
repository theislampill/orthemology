# Replay without modifying frozen work

Use a fresh extraction and keep outputs outside its root. No replay script installs packages, downloads dependencies, or writes into the archive's source tree. The declared Python environment is Python 3.12.14, mpmath 1.3.0, sympy 1.14.0, numpy 2.3.5 and scipy 1.17.0. The standard-library-only minimal-panel programs do not need those third-party packages, but the combined runner does.

From the extracted checkpoint root:

    python3 PACKING/check_manifest.py
    python3 PACKING/replay_python.py --output [OMITTED_PRIVATE_MACHINE_PATH]

The output directory may exist but must not already contain a replay receipt. The runner copies payloads into temporary scratch, executes the nine programs declared in PACKING/CONTROL_PLAN.json, compares generated outputs and stdout, and verifies frozen bytes are unchanged. Eight programs use exact output bytes. The minimal-author program alone emits run timestamps; its JSON comparison excludes only started_utc and completed_utc and records both actual hashes and the non-byte-identical result. No frozen timestamp is edited. Numerical quadrature remains a diagnostic, not interval-certified proof.

## Optional Lean replay with pinned external dependencies

Provide an external research root containing formal-identification/mathlib and formal-identification/toolchain/lean-4.19.0-linux with the exact recorded source/binary identities. Matching-version names alone are insufficient. The original installed dependency tree can be used read-only; alternatively reconstruct it separately using official Lean 4.19.0 and mathlib commit c44e0c8ee63ca166450922a373c7409c5d26b00b with the included lake-manifest package revisions and matching caches. This packet does not perform or certify that reconstruction.

    python3 PACKING/replay_lean.py --external-research-root /absolute/path/to/dependencies --output [OMITTED_PRIVATE_MACHINE_PATH]

The harness verifies the inventory's 3,596 imported source/olean hashes and 11 declared compiler/runtime/metadata bindings, confirms the mathlib commit, constructs LEAN_PATH from the pinned path record, then invokes the existing lean binary directly. It never runs lake build or changes the dependency tree. In a fresh temporary output directory it checks the source at -t 0 with warnings as errors, obtains the axiom report, reproduces all 1,798 import names and tests two deliberately false mutations. It rehashes external dependencies afterward. Temporary compiled proof artifacts are deleted with the temporary directory; logs and the receipt remain in your output directory.

This is a fresh check using an already existing compiler and imported libraries, not a bootstrapped compiler or upstream source rebuild. Only the deterministic certificate is formalized. Original CWD-sensitive verify_kernel.sh and reviewer VERIFY_BINDINGS.py are preserved as historical evidence; use the parameterized portable harness instead. The preserved reviewer author-code copy is a duplicate, not a tenth independent program.

## Integrity boundaries

MANIFEST.json hashes all payload files except itself and MANIFEST.sha256. MANIFEST.sha256 binds that manifest. The external validation receipt binds the final ZIP, manifest, fresh safe extraction, exact member inventory and portable replay receipts without a circular ZIP self-hash. Original/review manifests remain byte-identical; normalized included/external mappings live in PACKING/ORIGINAL_AND_REVIEW_BINDING_CHECKS.json. Excluded compiled artifacts retain their historical digest references.

No source PDFs, OCR, page images or raw retrieval bodies are available for source-body validators. Those checks are UNREPLAYED; local hash assurance does not substitute for source inspection. The H deterministic-lineage source is in the referenced eighth checkpoint, not bundled again. No physical experiment, empirical observation, broad sample-optimality test, all-project kernel proof, integration or closure is claimed.
