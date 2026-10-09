# Retained-interior certificate: scope and replay

Read RESULT.md for the mathematical statement and proof. Main outcome: a fixed 2n+1-probe staircase on one unchanged threshold vector has a Joe-positive, baseline-zero transcript. This gives infinite forward panel KL but only a one-sided route-count certificate, with no faster-sampling, physical-access, integration or T20-closure claim.

- controls.py and CONTROL_RESULTS.json: deterministic exact-grid, rational probability, symbolic radical and high-precision numerical checks; no simulation or empirical data.
- RetainedInterior.lean: source-specific connector implication, witness injection and count inequality only.
- verify_kernel.sh and kernel-replay/: isolated Lean4.19 trust-zero replay plus two rejected falsified edits.
- KERNEL_DEPENDENCIES.json and IMPORTED_MODULE_BINDINGS.json: exact local compiler/runtime and imported module/source provenance.
- SOURCE_AUDIT.md and SOURCE_BINDINGS.json: precise inspected-source scope and predecessor identities.
- NEGATIVE_CONTROLS.md: boundaries, failed transports and assurance limits.
- RESEARCH_EVENTS.jsonl and RESEARCH_ACCOUNTING.json: prospective active work only; waits and packaging excluded.
- REVIEW_STATUS.json: final separate adversarial review status and bound hashes when available.

Replay from this directory with python controls.py and bash verify_kernel.sh. The existing sibling formal-identification toolchain/mathlib must remain available; no installation or network retrieval is performed. Pass a fresh output directory as the sole verify_kernel.sh argument to preserve prior replay logs.

The kernel source is not a probability formalization. The written mathematics and executable controls supplement it, and the separate review checks both layers. No acceptance, integration or closure authority is conferred by these artifacts.
