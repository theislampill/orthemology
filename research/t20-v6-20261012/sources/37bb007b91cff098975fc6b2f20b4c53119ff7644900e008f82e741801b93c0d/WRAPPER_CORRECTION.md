# Source-only wrapper correction v2

No mathematical source, theorem, premise, scientific scope, dependency pin, or scientific review changed.

The first public wrapper candidate (manifest `a02c84d1091a284f4de92d056e8c2b25a9b6a3abd92e7678777398b4f1a323cb`) rejected every warning from positive stages. Its isolated full replay failed closed at the exact historical `ReviewerControls.lean`: Lean reports two harmless `linter.unnecessarySimpa` suggestions at 66:44 and 75:8. The independent model review already recorded them; all proof checks and standard-axiom checks passed there. This was a wrapper diagnostic policy mismatch, not a new scientific defect or new scientific credit.

Version 2 preserves every reviewed Lean byte and permits only those two exact diagnostics:

- Stage name must be `ReviewerControls`.
- Source SHA-256 must be `db9737455bc7109fd40e7ff10812604000d18d650bb4868f1007790db1c9ebe8`.
- Actual source path, line/column, complete warning and following note must match.
- Each permitted diagnostic must occur exactly once.
- After removing only those two full records, any warning, error or sorryAx still fails.

Four regression tests exercise the actual historical log, wrong stage/hash, altered/extra diagnostics and missing/duplicate occurrences. Other wrapper boundary tests are retained. All 20 tests pass.

`ORIGINAL_TO_PUBLIC.json` now also maps the complete original wrapper-v1 manifest into this packet, with its changed helper/README/mapping/test bytes preserved under `historical/wrapper-v1/`. That directory includes the original failed replay receipt, terminal output and reviewer-control compiler log. The current replay never runs the old helper. This wrapper correction is additive to the unchanged scoped scientific acceptances; it supplies no progress, opacity, physical implementation or tranche-closure result.
