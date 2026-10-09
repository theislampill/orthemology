# Portable replay

From an extracted checkpoint root:

    python3 PACKING/check_manifest.py
    python3 PACKING/replay_python.py --output [OMITTED_PRIVATE_MACHINE_PATH]

The output directory must be outside the checkpoint. The runner creates a disposable copy, deletes only declared generated outputs there, enables assertions, runs the six commands in CONTROL_PLAN.json, compares generated files and frozen stdout, and checks that the original checkpoint stayed unchanged. Author tensor snapshot is an exact duplicate, not another independent suite. Adaptive review binding output is checked semantically for status PASS and count 18; it has no historical stdout file.

Python 3 is required. Tensor controls and identity checks use its standard library. Adaptive numerical controls additionally require mpmath 1.3.0, recorded in requirements-controls.txt. No packages are bundled or installed by the runner. No network, source acquisition, Lean build, empirical collection or GitHub operation is performed.

The included source extraction script is NOT in the run plan because its raw HTML is omitted. Do not run original source-body or historical predecessor verifiers expecting the reduced archive to satisfy missing inputs. EVIDENCE_BOUNDARIES.json classifies these as UNREPLAYED. PACKING/ORIGINAL_AND_REVIEW_BINDING_CHECKS.json records packing-time local digest checks, not a portable full-source verifier pass. Original source paths and absolute paths are historical evidence; SOURCE_COPY_BINDINGS.json maps included copies.

Checks and packing timestamps provide delivery assurance only. They do not certify source-reading duration, universal proof validity, metaphysical truth, owner acceptance, integration or T20 closure.
