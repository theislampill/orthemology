# Event-feasibility descent: bounded mathematical packet

Read RESULT.md for the theorem, proof, contract distinctions, and exact controls.

Run from this directory:

    python3 verify.py

Requirements: Python 3 and SymPy. The recorded run used the versions in CONTROL_RESULTS.json. No network access or numerical optimizer is used. The verifier checks the three direct inherited RESULT.md files at their bound neighboring paths before running its controls. Copying only this directory without those inputs is not a complete replay environment.

Files:

- RESULT.md: written general proof and interpretation boundaries
- verify.py: executable exact rational and symbolic controls
- INPUT_BINDINGS.json: direct inherited evidence hashes and bounded inheritance comparison
- CONTROL_RESULTS.json: 29 passing assertion groups, including 304 support classifications
- verification.txt: complete successful console output
- MANIFEST.json: SHA-256 bindings of these files, excluding the manifest itself

This is author-stage mathematical evidence. Any independent review, external integration, or broader closure decision is separate.
