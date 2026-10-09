# Safe extraction and reproducible bounded controls

Use Python 3.12.14 with mpmath 1.3.0 and sympy 1.14.0 for the observed exact diagnostic bytes. This packet downloads or installs nothing. High-precision floating output is environment-specific evidence, not interval-certified proof.

Check the external ZIP SHA-256 against the delivery identity before executing archive code. Internal consistency does not establish trusted provenance. From an extracted checkpoint root:

    python3 PACKING/check_manifest.py
    python3 PACKING/replay_python.py --output [OMITTED_PRIVATE_MACHINE_PATH] --ninth-archive /path/to/T20_Retained_Readout_and_Interior_Boundaries_Intermediate_Checkpoint_20261008_Scope_Clarified.zip --tenth-archive /path/to/T20_Skyline_Information_and_Finite_Readout_Intermediate_Checkpoint_20261008.zip

The output directory must be outside the extracted root and contain no existing REPLAY_RECEIPT.json. The replay harness validates both exact predecessor archive hashes. It hydrates only three declared RESULT members from those archives into the disposable copy, with exact per-member digest checks, to satisfy author/reviewer dependency checks. Those predecessor files are never executed, edited or rebundled. Missing/wrong predecessors cause failure, not substitution from unverified local files.

The harness deletes generated outputs only inside its temporary copy, enables assertions, and runs eight mathematical control programs followed by three binding verifiers. All eleven declared JSON outputs must be byte-identical to their frozen targets; no timing or mathematical fields are ignored. The log-squared reviewer moved elapsed runtime to CONTROL_RUN.log before freeze. Stdout/stderr are retained externally as fresh logs and are not confused with the historical logs copied in the packet. The reviewer copies of author programs/results are retained as provenance but the duplicate author programs are not executed a second time.

The prior-art source review reports source/PDF and finite-grid checks, but does not supply a standalone script for them. Those results are preserved as reported review evidence and are not included in the fresh replay count. No source-body reread, old unrelated science, predecessor proof verification or Lean replay occurs.

From an already trusted helper, safe extraction into a new directory is:

    python3 PACKING/safe_extract.py /path/to/checkpoint.zip [OMITTED_PRIVATE_MACHINE_PATH]

The extractor rejects duplicate, unsafe, traversal, backslash and absolute names, symlinks, unusual file types, encrypted entries, multi-root and undeclared members before writing. It validates exact inventory, manifest digest and all payload bytes without executing archive code. The separate manifest checker then validates native manifests/sum lists, current source bindings, exact author-review pairing and contribution/dependency mappings.

Expected-rejection tests use only disposable mutated copies:

    python3 PACKING/integrity_controls.py /path/to/checkpoint.zip
    python3 PACKING/binding_controls.py

Ten archive-integrity controls test payload mutation, missing/extra members, manifest mutation, traversal, absolute/backslash paths, duplicate members, symlinks and multiple roots. Six additional binding controls test wrong author-review pairing, wrong review file, wrong/missing external dependency, wrong receipt binding and omitted stage acceptance. The latter rehash the top inventory deliberately so the rejection checks relationships beyond a stale top hash. They do not certify mathematical truth.

MANIFEST.json lists every payload except itself and MANIFEST.sha256. MANIFEST.sha256 binds that manifest. The external validation receipt binds the final ZIP and fresh validation without a circular self-hash. Frozen sources, prior archives, prepared payload and extracted inputs are all checked unchanged before completion.
