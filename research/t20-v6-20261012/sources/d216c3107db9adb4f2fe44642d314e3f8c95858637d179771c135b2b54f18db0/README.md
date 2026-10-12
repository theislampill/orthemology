# Completion and Bayesian commutation

RESULT.md classifies commutation of fixed-reference moment completion and Bayesian conditioning, distinguishing positive inputs, genuinely possible boundary branches, and equality of the entire feasibility-sensitive partial maps.

Run exact controls:

    python3 verify.py

Run a manifest-checked, byte-comparing replay into a new directory outside this packet:

    python3 replay.py private-locator:120db0ee311e37fa84df

Optional original-input verification:

    python3 replay.py private-locator:d8f5d3a106492c056dff --verify-original-inputs /path/to/workspace

Python 3 and SymPy are required. The two 80-likelihood sweeps use symbolic polynomial identities over arbitrary positive atom weights. The finite grid is a separate bounded support control. No numerical optimizer is used.

INPUT_BINDINGS.json contains six direct original hashes and portable byte-identical snapshots. One snapshot is the frozen face-stratified packet's manifest, recording inherited identity without rerunning its transitive files or claiming its independent review. MANIFEST.json binds this packet's files except itself. CONTROL_RESULTS.json and verification.txt are author outputs. The replay checks all manifest entries before execution and compares regenerated JSON and stdout byte-for-byte.

The inherited packets carry classical source attribution. This packet makes an elementary, explicitly proved composition of their model-preservation, normalized-record, and feasibility results; it does not claim field novelty, protected changes, implementation failure, independent mathematical review, or programme closure.
