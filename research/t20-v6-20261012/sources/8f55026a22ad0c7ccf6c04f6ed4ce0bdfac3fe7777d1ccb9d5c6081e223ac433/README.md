# Shared-root finite-controller evidence

This source-only component contains the verified shared-store progress core,
its exact fixed-order sharpness witness, and a separate finite bad-store erasure
extension. Read ARGUMENT.md and EXECUTION_CLARIFICATION.md before interpreting
the bounds. Acceptance reports and final artifact checks are in the separate
acceptance companion.

No toolchain, Mathlib cache, compiled object, private planning file, or original
user document is included. Lean source bytes are projected unchanged from the
listed immutable scientific milestones. Historical metadata retain their original
author-time status; the acceptance companion records later independent review.

## Reproduce

Supply the exact pinned Lean 4.19.0 Linux x86_64 distribution and
Mathlib c44e0c8 source/cache snapshots
specified by dependencies/. The script neither downloads nor rebuilds them.
Python 3.10+ standard library is sufficient for the wrapper.

Run from any working directory:

python /absolute/path/to/Shared_Root_Controller/replay.py --lean-root /absolute/path/to/lean-4.19.0-linux --mathlib /absolute/path/to/mathlib-c44e0c8 --output /absolute/path/to/new-replay-directory

The output directory must not exist and must be outside the package and dependency
trees. The wrapper verifies all scientific/public bytes, exact dependency inventory
and pins, compiles source into a fresh build with one Lean job, audits the exact
new/reviewer theorem inventories, and verifies inputs again afterward. Read
REPLAY_RECEIPT.json; an error, warning, timeout or unexpected axiom is not a pass.

## Five cache-trace relocation records

Only Cache/Hashing.trace, IO.trace, Lean.trace, Main.trace and Requests.trace may
use the exact separately bound restored metadata bytes. For each permitted
mismatch, the wrapper checks the recorded current hash/size, confirms exactly one
recorded absolute-prefix occurrence, normalizes that prefix for comparison only,
and checks the original pinned hash/size. It does not edit the real files. Every
other dependency byte, including every .olean/.ilean, remains exact. This narrow
metadata allowance is not evidence of a current execution at the old path.

## Main source endpoints

- SharedAlias.Progress.seven_protected_window_progress
- SharedAlias.Progress.Witness.uniform_unknown_world_installation
- SharedAlias.Progress.Witness.twenty_one_attained
- SharedAlias.Progress.BadStore.finite_weave_erasure
- SharedAlias.Progress.BadStore.every_woven_installation_has_exact_effect

The replay's standard axiom allowlist is propext, Classical.choice, Quot.sound.
Separate reviewer controls include unconditional-progress obstructions, real-label
receipt/nonfabrication checks, fixed-program service independence, exact effect
counters, fixed-order prefix behavior, and finite-corruption checks.

## Compiler subprocess environment

Every version, compilation and axiom-audit subprocess receives a copied
environment with all LD_* keys removed, including LD_AUDIT and unknown future
LD_ names. The generated LEAN_PATH and existing LEAN_SRC_PATH/LEAN_SYSROOT
cleanup remain in force. Other ordinary variables are retained. This sanitation
does not establish trust in an already-started Python launcher or its host.

A bounded sanitation check (no Lean/dependency rebuild) is available as:

python /absolute/path/to/Shared_Root_Controller/controls/check_compiler_environment.py --output /absolute/path/to/new-check-directory
