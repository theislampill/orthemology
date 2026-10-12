# Explicit polynomial scale audit

Read REPORT.md and RESULT.json. INPUT_MANIFEST.json pins the copied frozen author closure. The original four-coordinate example receives a new arithmetic radius; the mixed-rank theorem is not strengthened by this packet.

Replay in the existing workspace:

    python tranche3/explicit-scale-kernel-audit/checks/replay.py
    python tranche3/explicit-scale-kernel-audit/checks/supplement.py
    python tranche3/explicit-scale-kernel-audit/checks/scale_checks.py

The first script builds 11 author modules freshly against the existing pinned tranche2/toolchain. The supplement evaluates a literal radius fixture, reads exact definitions/types/axioms, and rejects four source mutations. It uses only the independently built dependencies from the first command. Accepted builds reject PANIC as well as errors and sorryAx.

The exact-rational evaluator covers all twenty actual constraints; numerical approximation is not used. It reuses a copied independent polynomial oracle from the prior audit as a test helper. No universal Python runtime/refinement result is claimed.

MANIFEST.json excludes compiled builds, bytecode, itself, archive and delivery seal. Historical auditor-only normalization failures are retained separately under evidence/development. All previous seals remain unchanged.
