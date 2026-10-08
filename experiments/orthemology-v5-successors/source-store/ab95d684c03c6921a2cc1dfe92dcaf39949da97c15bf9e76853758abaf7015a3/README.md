# Sixteenth Orthemology proof sources: recovered-v1

This is a new post-reset integration of 111 exact frozen mathematical sources: the 88-module delivered Fifteenth baseline plus nine unary/HasC, six effective-renewal, three finite-lookahead and five policy-synthesis modules. Mathematical bytes and names are unchanged. See SCOPE.md for theorem boundaries and RECOVERY_SCOPE.md for the distinction between historical acceptance, exact recovered records and new verification.

## Preparation and replay

Install the official Lean 4.19.0 toolchain (elan identifier leanprover/lean4:v4.19.0), Python 3.8+ and Git. Run Python without -O/-OO or PYTHONOPTIMIZE; optimized mode is deliberately refused because verification checks must stay active. Mathlib is pinned to c44e0c8ee63ca166450922a373c7409c5d26b00b; all eight transitive dependency revisions are preserved in lean/lake-manifest.json.

Prepare dependencies outside the sealed source tree. The supplied helper uses only the exact official GitHub pins and the pinned official Mathlib cache client:

    python3 "/path/to/recovered-v1/prepare_dependencies.py" --directory "/path/to/new preparation"

This creates separate dependencies, cache and preparation logs. The directory must not already exist and must be outside this package. It never rewrites the delivered lake-manifest.json. Its official cache client also acquires the version-pinned leantar and ProofWidgets releases required by that client. A source cold build is not claimed. If the cache or network is unavailable, the helper reports a failure rather than silently changing revisions or claiming complete preparation.

The author independently exercised the same exact-pin acquisition and official-cache flow in the post-reset environment: all nine revisions were clean, 1,369 dependency objects were obtained, and the combined import smoke test passed. Those are newly acquired dependency objects, not recovered historical objects.

From any working directory, including one unrelated to the extraction, run:

    python3 "/path with spaces/recovered-v1/replay.py" --dependencies "/path/to/new preparation/dependencies" --output "/path/to/new replay output"

Options:
- --lean: explicit official Lean executable; default is lean on PATH
- --dependencies: prepared parent containing the nine pinned package directories; default is this package's lean/.lake/packages for users who have deliberately prepared that layout without changing locked files
- --source-only: verify source/file locks without building

Relative supplied paths resolve from your current directory; the script finds its package relative to itself. Output must not already exist and must be outside the package. Replay never deletes prior output. Failed runs remain evidence; use a new output path for a fresh retry.

A successful full run ends with RECOVERED_SIXTEENTH_SOURCE_PACKAGE_REPLAY_PASS and writes REPLAY_RECEIPT.json in the new output directory. It includes exact dependency object bindings, fresh project compilation, every actual packaged control, declaration/theorem coverage and constructor retention. The earlier stage receipts inside provenance/ are labelled author observations, not substitutes for your replay. The standalone compile_project.py and run_controls.py provide explicitly separated build/control stages; only replay.py is the complete fresh-package entry point.

## Audits and integrity

MATHEMATICAL_SOURCE_LOCK.json locks every mathematical source. CONTROL_MANIFEST.json lists actual packaged fixtures and expected diagnostics. CONTROL_RECOVERY_REGISTER.json also records historical slots and restoration status; an unavailable historical fixture is never counted as executed. FILE_INTEGRITY.json lists every other delivered file and its SHA-256.

All 111 modules are imported by a new complete-inventory wrapper. Every theorem declaration is a proof-audit root, including generated theorem declarations. Nonproof compiler/runtime auxiliaries are explicitly listed. Import-only modules are checked separately rather than silently omitted from coverage. Original lane-specific proof/runtime audits remain separate, while unknown-opaque rejection remains mandatory in the separately replayed computational/HasC lanes. The aggregate logical proof audit explicitly inventories safe opaque declarations without claiming executable totality. HasC constructor retention compares the actual packaged AllSyntax and UnaryCertificateSyntax.

Generic renewal and policy KernelAudit/RuntimeAudit names have separate output roots. Lookahead sees renewal's auditor; policy never shadows it. All inherited verification.* support modules are built into one coherent inherited verification namespace. Accepted audit sources are unchanged; wrapper routing is documented in INTEGRATION_CHANGES.md.

The archive contains source, concise documentation, manifests and receipts only. It contains no toolchain, native executable, compiled object, cache, dependency checkout, external symlink, primary paper, participant data or private assessment. No canonical adoption, publication or public P01DF transfer is performed.
