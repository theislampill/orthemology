# Actual batch/controller source component

This source-only component preserves the accepted common-v6 proofs and the complete actual-batch-v4 scientific lineage. No compiled custom proof object is included. The separate acceptance companion binds this component's exact ZIP and contains the independent reviews and portable reviewer-control replay.

## Results and exact boundaries

- The unchanged `runBatch` has a common finite primitive history and full final alignment from its explicit aligned/reachable input conditions.
- Its four recorded paths/nonces are fixed by source. Literal `badOpen=false` gives at most one landing without a fault-budget premise.
- Separate source-level readiness conditions give bounded stable completion and the entire exact successor.
- The final iff characterizes one landing by existence of one predicted complete envelope whose selected path is all-good and has no prior exact tombstone there. Stored-actor and actual-world admission plus matching unrevoked good-root policies remain explicit. This is a proof-side initial-state condition, never actor input or a path-choice oracle.
- The pinned 3013-byte raw2-to3 installation/repair controller is tied to the accepted source let-sequence, with complete versions, audit histories and custody retained.
- Native controls distinguish genuine cleanup from synthetic closed logs, delayed-delivery retry failure, fresh-envelope recovery, same-nonce/different-command recovery, selected cancellation and partial-write boundaries.

There are 476 cumulative author theorems (312 inherited common-model theorems and 164 batch-extension theorems). The replay audits every named explicit declaration in all 61 custom source modules, including the imported exact runtime definitions. Anonymous compiler-generated names are not individually enumerated. All audited closures must contain only `propext`, `Classical.choice` and/or `Quot.sound`.

The scope is the exact stable source model. It does not prove authentic clocks/observations, real policy issuance, physical/asynchronous service completion, external nonce allocation, actor knowledge, unbounded/interleaved controller progress, shared-alias lifecycle composition, or deployment/semantic warrant. All-good-path necessity is specific to the literal withholding controller.

## Current reading order

1. `science/BATCH_SURVIVAL_ARGUMENT.md`: final iff and its premises
2. `science/BATCH_SUCCESSOR_ARGUMENT.md`: actual aggregate admission, cleanup and native composition
3. `science/reader-corrigendum/BATCH_RETRY_ARGUMENT_CORRECTED.md`: current retry discussion
4. `science/BATCH_ARGUMENT.md`: preserved earlier core scope

The original `science/BATCH_RETRY_ARGUMENT.md` is frozen for scientific/review identity. Its phrase “necessary high-water bound” has an explicit accepted one-sentence correction: high-water is a sufficient premise of the conservative proof, not necessary for recovery. The corrected reader note, projection map and review binding are preserved under `science/reader-corrigendum` and `science/review`.

## Standalone fresh replay

Requirements: trusted Python 3.10+, the official Lean 4.19.0 distribution at release commit `6caaee842e94`, and a pre-existing Mathlib checkout/cache at commit `c44e0c8ee63ca166450922a373c7409c5d26b00b` matching the bundled inventories.

From any working directory:

    python -B /path/to/component/replay.py \
      --lean-root /path/to/lean-4.19.0-linux \
      --mathlib /path/to/mathlib-c44e0c8 \
      --output /path/to/absent-replay-output

The output must not already exist and must be outside the component and all dependency trees. `--stage-timeout` defaults to 300 seconds and must be finite, positive and at most 600 seconds. Each compiler stage uses `-j1 -s65536`.

The wrapper does not download, update or rebuild dependencies. It verifies the complete 5,065-entry Lean distribution, 6,816 Mathlib source records and 34,230 cache entries before and after execution. Every scientific dependency `.olean`/`.ilean` must match the original pin. Only the same five declared official cache-fetcher `.trace` files may differ. The original bytes and exact known restored variants are accepted. For a fresh location, exactly one occurrence of the canonical supplied and fully verified Lean launcher path may be compared with the exact historical launcher path; normalized bytes and size must equal the original pin. Raw hashes and that exact transformation are recorded. No other path, log argument, depHash, metadata field or proof object may change, and files are never rewritten. These metadata variants are not presented as evidence of current execution.

All 61 custom modules are built from the supplied verified source into an empty isolated output. All inherited LEAN_*, LD_* and DYLD_* variables are cleared before the exact proof search path is installed. No author or earlier review build directory is used. Source, object and dependency identities are checked; unexpected source files/symlinks, changed pins, proof escapes, compiler warnings/errors, unexpected axioms and incomplete declaration audits fail closed. Timeouts/resource failures are inconclusive, never successful proof evidence.

A successful run writes `RECEIPT.json`, fresh objects and logs only in the chosen output. A failed run writes `REPLAY_FAILURE.json` when output creation was reached and never writes a success receipt. Invalid source packages and existing/protected outputs are rejected before output creation.

## Wrapper contract tests

    python -B /path/to/component/test_replay.py

These tests exercise path/output refusal, unexpected files, symlinks, exact metadata relocation, byte tampering, timeout validation and axiom inventory checks. They are wrapper tests, not substitutes for the full Lean replay. The distribution acceptance companion records the actual-ZIP, unrelated-working-directory replay and additional adversarial checks.
