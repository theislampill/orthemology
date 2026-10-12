# Independent atomic-membership bridge audit

REPORT.md gives the mathematical verdict, the exact scope, and countercontrols. SEAL_RECONCILIATION.json binds the independently rebuilt sources to the precise author archive. The receipt directory contains an isolated copy of all 53 custom sources, build commands/logs, theorem signatures, axiom reports, and control outcomes. Author object files were not used in the independent replay.

## Fresh replay

Use official Lean 4.19.0 (commit 6caaee842e94) and Mathlib at c44e0c8ee63ca166450922a373c7409c5d26b00b with its official dependencies/caches. Set SRC to the supplied receipt's sources directory, then run:

    python3 verify.py --p02-root "$SRC" --measure-root "$SRC" --tagged-root "$SRC" --bridge-root "$SRC" --mathlib-root /path/to/mathlib4 --lean-bin /path/to/lean-4.19.0-linux/bin --seal SOURCE_FREEZE.json
    python3 run_controls.py --mathlib-root /path/to/mathlib4 --lean-bin /path/to/lean-4.19.0-linux/bin

The first command writes a new receipt and LATEST_REPLAY.txt. The second consumes that new receipt (or an explicit --receipt path) and rebuilds the independent controls against its fresh library. The runnable controls deliberately test false mutations and require them to fail. Recovered Python code is used only to generate independent runtime comparison vectors; it is not a Lean axiom or part of the measure proof. Host resource limits are not semantic zero-output cases.

Development logs are retained separately from the final evidence. The original author archive is preserved byte-for-byte, and no canonical sources are edited. Uniform Mathlib Computable/hierarchy certification, the original soft/excess formula, and later stack-machine work are outside this sealed review.
