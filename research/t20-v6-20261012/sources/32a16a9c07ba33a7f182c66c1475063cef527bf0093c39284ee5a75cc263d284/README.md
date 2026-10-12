# Literal rational-cell shift: checked Lean checkpoint

Read RESULT.md for the result and SOURCE_BRIDGE.md for the exact Python-to-typed-AST boundary. INDEPENDENT_REVIEW.md records the independent source review, fresh seven-module proof replay, and separate control replay. The eight new modules have 66 substantive exported theorems and seven positive control theorems.

The actual original sorted-register allocator and selector/replay expressions are retained. This is neither the earlier alternate unary-tag compiler nor another finite enumeration. It closes a specific kernel finite-output and pointwise-stream refinement gap. It does not kernelverify the Python runtime, exact original serialized bytes, explicit Set-event traces, or the measure/defect formula.

Sources and frozen observed proof objects/logs are preserved. The original prcodec.py and the relevant earlier ordinary proof/review documents are under inputs/. Prior ordinary universal correctness and PR construction are explicitly inherited.

Replaying the proof requires official Lean 4.19.0 (compiler commit 6caaee842e94) and Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b, with the exact dependency manifest under inputs/. Set LEAN_HOME to the official toolchain directory and LEAN_PATH to the corresponding Mathlib and dependency .lake/build/lib/lean directories. Then run:

    python -B build_prerequisites.py
    python -B verify_final.py

The first script rebuilds only the nine included unchanged prerequisite modules and binds fresh objects. The second creates a new isolated verified-* directory, copies only checked prerequisites, builds all eight new modules with --trust=0, queries every theorem type/axiom closure, and checks all four intended-false controls. Fresh attempts never overwrite the archived final observed run. These are real kernel replays and require the dependency environment; verify_integrity.py checks only file identity without Lean.

No default finite-resource Python execution guarantee is made. No original repository or protected source was changed. No integration, owner acceptance or T20 closure is claimed.
