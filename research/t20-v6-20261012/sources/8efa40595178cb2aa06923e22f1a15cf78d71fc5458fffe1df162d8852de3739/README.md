# Shared-root typed-history safety checkpoint

A literal shared-store pullback does not refine the accepted label-local history machine. This checkpoint proves a weaker, useful result: an explicit actual-root shared-store model has a forward safety simulation into that history machine, with exact real label receipts and extra concrete vetoes. It then transports typed source admission, full effects, custody, counters, cancellation safety and fixed-action rejection.

Wrapper correction: `WRAPPER_CORRECTION.md` records the failed-closed v1 run and the narrowly source-bound v2 lint exception.

Start with `RESULTS.md` and `review/TYPED_V1_REVIEW.md`. The immutable scientific milestone has SHA-256 `1b88370e522b085349c6da4c0aab1b3763b557e02c3c4eb6d631f9d4ab4636d7`. Its 88 scientific declarations and 18 additional reviewer declarations use only standard Lean logical axioms. Model, simulation and typed reviews have distinct bounded scopes.

This is a mathematical reference realization and typed source-gate adapter. It is not an executed 21-path controller, whole unchanged-runtime refinement, physical implementation, progress/service guarantee, map-secrecy theorem, opaque-search theorem, optimality transfer or tranche-completion certificate. No R5 enlargement or N2/T0 conclusion follows.

## Contents

- `science/`: 12 exact reviewed new Lean modules
- `imports/common/`: exact accepted typed-history-v2 and its predecessor modules
- `imports/attribution/`: exact accepted one-class attribution dependencies
- `controls/`, `mutants/`: positive targets, complete scientific axiom audit and five isolated source mutants
- `review/`: the three independent scientific reviews, exact replay receipts and reviewer Lean controls
- `dependencies/`: byte inventories, with no compiler or compiled cache included
- `provenance/`, `historical/`, `ORIGINAL_TO_PUBLIC.json`: exact immutable scientific-manifest mappings, including old helper/evidence identities
- `replay.py`, `test_replay.py`: the current standalone replay and its boundary tests

Historical helpers are evidence only. They may name the original working layout and are never invoked by the current replay. Private design plans, working notes, build outputs and compiled caches are excluded.

## Standalone replay

Run from any working directory with Python 3.9 or newer (tested with Python 3.11):

    python /path/to/checkpoint/test_replay.py
    python /path/to/checkpoint/replay.py \
      --lean-root /path/to/lean-4.19.0-linux \
      --mathlib /path/to/mathlib-c44e0c8 \
      --output /path/to/an-absent-replay-directory

The output path must not exist and must lie outside the checkpoint, Lean distribution and Mathlib trees. Symbolic-link resolution is included in those checks. Source and dependency trees are read-only. No download, package update, network request or dependency rebuild is performed.

Required external bytes:

- Official Lean 4.19.0 Linux distribution, release commit `6caaee842e94`. The supplied release archive SHA-256 is `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`; all 5,065 distribution entries were compared with that archive before the manifest was produced. The replay verifies the complete pinned distribution, including its libraries, rather than only the small launcher binary.
- Mathlib source revision `c44e0c8ee63ca166450922a373c7409c5d26b00b`, source archive SHA-256 `9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425`. All 6,816 source records are checked.
- The corresponding supplied precompiled library trees. `MATHLIB_CACHE_PIN.json` binds 34,230 entries totaling about 4.55 GB, including Mathlib and its seven package-library roots. A different cache fails closed even if it reports the same source revision.

The pinned precompiled libraries remain trusted dependencies. Checking their bytes is not rebuilding them or proving compiler, runtime, OS, hardware, authentication, clock or physical-device correctness. The host Python, OS and system dynamic loader remain part of the execution environment. The wrapper removes inherited Lean-path and dynamic-library override variables before compiler execution.

The replay compiles all 35 exact predecessor/new scientific modules from source into a fresh build directory, plus three reviewer modules and four positive target/audit files. It audits the exact 88 scientific and 18 reviewer theorem-name inventories. Positive-stage diagnostics are rejected except the two exact historical unnecessarySimpa advice messages in the hash-pinned ReviewerControls source; the exception is stage-, hash-, location-, text- and occurrence-count-bound. It then checks five mutants separately, requiring their intended diagnostics. A timeout, missing module or other resource/infrastructure error is never credited as semantic mutant rejection.

`--stage-timeout` defaults to 300 seconds per compiler process and accepts finite values greater than zero and at most 600. Partial timeout output is retained. Successful replay writes `RECEIPT.json` only at the end. A failure after creating a valid output directory writes `REPLAY_FAILURE.json`; source-package, invalid-argument and protected/existing-output refusals happen without creating output. Inconclusive mutant runs are labelled as such and produce no success receipt.

The exact packet inventory is checked before and after replay. All pinned dependency bytes and Mathlib source records are rechecked at the end. The wrapper does not rely on the old accepted common-model `.olean` build: those custom predecessor sources are recompiled here. Dependency hashing reads several gigabytes and may take noticeable time.
