# Independent effective-index evidence

Read REPORT.md first. This bundle records a bounded technical PASS, not whole-obligation or hierarchy-completeness closure.

## Key evidence

- SOURCE_MATCH.json checks the author seal, all 49 custom source hashes, compiler version, and official dependency checkout identity
- receipts/20260930T161345Z/RESULT.json records the fresh 49-module build and initial 73-name scan
- CONTROLS_RESULT.json and CompleteAudit.log supersede the partial name scan with all 82 names and their axiom footprints
- Differential.log records 758 passing executable comparisons against independently extracted recovered Python
- BoundaryControls.lean and negative-controls/ contain the supplemental Lean controls
- recovered/ binds the exact archive and source member
- author-seal/ preserves the reviewed author seal, scope, and source-closure manifest

All custom Lean source is included under receipts/20260930T161345Z/sources. Compiled binaries are intentionally excluded from the evidence ZIP. No author custom build output was used as a dependency cache.

## Replaying in the original workspace layout

Run verify.py with --p02-root private-locator:6e1cdd2685640ba2eef0 --measure-root private-locator:67a0368f452b0a176f36 --tagged-root private-locator:1dc07ecc133a6053717a --mathlib-root private-locator:41bd9f979012c8bbc235 --lean-bin private-locator:d97af50b47918e94879b. The script always creates a fresh source and binary closure and prints its receipt path. The three custom source roots can instead all point to the bundled frozen sources directory; duplicate equal source paths are harmless.

The recorded run_controls.py targets the recorded receipt directory and original Mathlib/Lean locations. For a portable replay, the package integrator should set those three paths to the fresh verify.py receipt and supplied official installations, then run the same command sequence. The source-level controls do not otherwise depend on the author's workspace. make_differential.py deterministically regenerates Differential.lean from the recovered Python source.

The original large single-function differential harness passed in about 122 seconds. DifferentialSmall.lean was a seven-check timing diagnostic and passed. DifferentialBatched.lean was prepared as an alternative but was not executed or counted; it is excluded from the sealed bundle.

## Retained audit-harness failures

controls.initial-before-receipt.log records starting the supplemental stage before the fresh receipt existed. BoundaryControls.initial.log and controls.initial-proof-harness.log record decide getting stuck on well-founded definitions and one unsimplified List.append_nil. The corrected harness uses already-proved universal interfaces, with no candidate source edits. These initial failures are not candidate counterexamples and are not concealed.
