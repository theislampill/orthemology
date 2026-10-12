# Operations

The package is separate from all prior sources. `PREDECESSOR_HASHES.json` was captured before construction. Eight dependency sources were copied byte-identically into `frozen/`; only this directory's generated `.olean` outputs are rebuilt.

`run-lean.sh` uses the installed predecessor Lean 4.19.0 toolchain and pinned mathlib tree without altering or installing either. Paths are local to this authorized workspace. `replay.sh` compiles all accepted sources with warnings as errors and invokes runtime checks in two ways. `check-mutations.sh` expects correspondence/completeness proof rejection and excludes missing modules, file errors, and resource-limit errors as acceptable reasons.

`development/` preserves failed attempts at kernel reduction of concrete computations and other intermediate proof attempts. An initial relative-path test invocation failed; the subsequently recorded red test failed for the intended missing theorem. Only final replay and reviewed-source receipts count as verification. `mutations/` contains deliberately rejected sources and error-recovery output; it is not imported by any accepted module.

No protected file edit, remote operation, publication, integration, or owner closure is performed. Timestamp fields are actual collection timestamps, never reconstructed work durations.
