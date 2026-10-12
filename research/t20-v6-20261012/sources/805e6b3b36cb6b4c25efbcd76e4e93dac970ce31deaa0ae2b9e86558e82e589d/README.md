# Geometry boundary delta audit

Read REPORT.md for the scoped result and changed frontier. MIXED_RANK_REVIEW.md supplies the independent ordinary geometric proof review; ZERO_SUCCESS_COMPARATOR.md closes the positive-comparator regularity issue. The previous polynomial audit seal is unchanged.

The author input is freeze-boundary-v2, verified by INPUT_MANIFEST.json and copied under author-freeze. Kernel scope consists of CriticalZero, FiniteLPCertificates and the author's BoundaryReadback, plus the independent exact four-row/dual-certificate binding module.

## Replay in the existing project workspace

    python tranche3/geometry-delta-audit/checks/critical_checks.py
    python tranche3/geometry-delta-audit/checks/mixed_rank_checks.py
    python tranche3/geometry-delta-audit/checks/replay.py

The replay script uses the already acquired tranche2/toolchain Lean 4.19.0 and pinned Mathlib tree, verifies its source state, and creates a fresh build directory. It does not install anything or reuse author oleans. The copied author script also supports explicit toolchain-directory environment variables for other filesystem layouts.

All successful source/axiom readbacks are in evidence. Four mutation builds intentionally fail and are excluded from accepted proof qualification. The mixed-rank extension and exponential positive comparator are ordinary results, not kernel theorems in this archive. Later mixed-rank formalization and full-jet flat-perturbation research are outside this seal.

MANIFEST.json covers portable sources, reports, controls and evidence, excluding itself, the delivery seal, ZIP, compiled builds and bytecode. Historical independent-test debugging logs are clearly labeled under evidence/development. RESULT.json records only the final accepted checks.
