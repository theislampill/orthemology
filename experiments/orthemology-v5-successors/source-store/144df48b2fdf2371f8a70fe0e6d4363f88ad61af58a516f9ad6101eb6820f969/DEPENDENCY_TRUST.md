# Compiler and library trust boundary

The source endpoint is pinned to Lean 4.19.0 and Mathlib revision c44e0c8ee63ca166450922a373c7409c5d26b00b, with the exact Lean binary digest and package revisions in DEPENDENCY_PINS.json. The public runner checks the Lean binary/version and exact official Mathlib source identity (clean pinned Git checkout or the supplied exact official source archive), and checks each dependency package's clean pinned source identity.

The public portable runner explicitly trusts the supplied official Lean/Mathlib object cache; it does not independently rebuild all of Mathlib or prove the compiler. This is separate from rebuilding every selected custom cost module and every new scientific module from the included source. No historical or author custom object is reused by the portable replay.

In the actual author/reviewer environment, restoration verification additionally checked 5,065 Lean distribution entries, 34,230 Mathlib cache entries, and 6,816 Mathlib source entries. Five documented cache trace files differed only because of relocated source paths:

- .lake/build/lib/lean/Cache/Hashing.trace
- .lake/build/lib/lean/Cache/IO.trace
- .lake/build/lib/lean/Cache/Lean.trace
- .lake/build/lib/lean/Cache/Main.trace
- .lake/build/lib/lean/Cache/Requests.trace

These path-only metadata deltas were accepted in the pinned environment; no custom theorem or source alteration was justified by them. The independent review records its own full environment checks. This environment-specific stronger check is not silently attributed to the portable source verifier.

Generated C is evidence of successful Lean codegeneration for the finite checker. The trusted runtime primitive leaves reported by the dependency audit remain part of the execution substrate. No linked standalone executable, compiled-binary refinement, formal bit-cost theorem or raw-byte parser theorem is claimed.

## Retained source resource settings

All eight new modules use Lean's default heartbeat budget, and neither author nor portable replay adds a heartbeat override. Two exact inherited modules already contain `set_option maxHeartbeats 800000`: `FiniteChainTrajectory.lean` (line 5) and `GeneratedParitySuccess.lean` (line 4). Those settings were preserved with the inherited source bytes. They must not be described as default-heartbeat executions. Every replay command remains sequential `-j1` with a 180-second wall cap; this artifact adds no resource-budget escalation.
