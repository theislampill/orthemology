# Mixed rank kernel successor audit

Read REPORT.md and RESULT.json. The exact frozen author closure is copied under author-freeze and source, with hashes in INPUT_MANIFEST.json. The earlier polynomial/boundary audit seals are unchanged.

Replay in the existing workspace:

    python tranche3/mixed-rank-kernel-audit/checks/replay.py
    python tranche3/mixed-rank-kernel-audit/checks/supplement.py
    python tranche3/mixed-rank-kernel-audit/checks/check_lp_values.py
    python tranche3/mixed-rank-kernel-audit/checks/mixed_rank_checks.py

The first script builds all 15 frozen modules in a fresh directory using the pinned tranche2/toolchain. The supplement checks the additional high-only/readback module and four intentional source mutations. It must follow a successful replay because it imports only those newly built dependencies. Error, sorryAx and PANIC diagnostics fail accepted builds. Mutation logs are rejected proof attempts, not accepted source qualification.

The explicit arithmetic radius for the four-coordinate polynomial example is a separate successor. This mixed-rank theorem has an existential radius. General optimized-regret asymptotics remain ordinary mathematics.

MANIFEST.json excludes build products, bytecode, itself, archive and delivery seal. Historical auditor-only proof-normalization failures are preserved in evidence/development; no author change was required. Readable source closures and all accepted/rejected replay logs are included.
