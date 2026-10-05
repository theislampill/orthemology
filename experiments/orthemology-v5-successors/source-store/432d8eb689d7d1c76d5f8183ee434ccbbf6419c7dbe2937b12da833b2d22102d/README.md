# Portable public review helper

This is a packaging-only successor. Frozen acceptance reports, source identities, logs, and proof sources remain unchanged. The earlier helper's environment-script hash records provenance; it is not a requirement for a relocated external installation.

Set TOOLCHAIN_ENV to a readable regular shell environment file exporting LEAN_ROOT and LEAN_PATH for an independently verified Lean 4.19.0 and the pinned Mathlib c44e0c8 dependency environment. The helper aborts if sourcing fails and verifies the exact Lean launcher SHA256. It does not independently rebuild or verify every external dependency on each module invocation. The pinned dependency restoration evidence remains the prerequisite; a matching launcher alone is insufficient to establish matching Mathlib libraries.

From the review package root, invoke:

    TOOLCHAIN_ENV=/path/to/verified/environment.sh bash public-portable/scripts/reproduce-module.sh IndependentMixedControls

The helper resolves package files relative to itself, supports paths containing spaces, uses one serial `-j1` compiler process with a 180-second timeout and default limits, and writes new output only to sources/module.olean and fresh reproduction-logs directories. It never appends to frozen acceptance logs. Coordinate concurrent invocations to retain at most two global compiler processes; sequential invocation is recommended.

For a fresh scientific replay, copy only the manifest-bound .lean files into a fresh sources directory, excluding all .olean files; build the inherited sources in accepted-complete-order.txt order, then new sources in final-dependency-order.txt order, then AllReadback and the independent controls/readback. A single-module smoke with existing checked dependencies establishes wrapper portability, not a new clean scientific replay.

PUBLIC_LOG_PROJECTION.json records the sole historical transcript normalized for public distribution. The normalized file is explicitly labeled, preserves all diagnostic text and line order, and adds the exit code from the immutable command ledger. Only three machine-root strings are replaced by safe aliases. The original raw bytes remain privately preserved and hash-bound. This public normalization neither turns the historical failure into success nor changes the original acceptance evidence.
