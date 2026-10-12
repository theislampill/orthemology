# Public Lean source replay

Result: **PASS**, completed 2026-10-03. This tests public packaging reproducibility under the already declared trusted external environment. It does not reopen the accepted mathematics or establish novelty, interpretation, primary-source applicability, full-programme closure, hermeticity, or toolchain certification.

## Exact candidate and unchanged inputs

- Public root: the exact selected payload identified by the manifest below.
- Tested `SELECTION_MANIFEST.json` SHA-256: `4a28ebe6b3de2a7c9d96370d0e4346341e88430cce99ba210623be2301d11c76`.
- Public verifier passes for 288 listed files (289 files including its self-excluded manifest).
- `PUBLIC_BEFORE.json` and `PUBLIC_AFTER.json` agree for the entire public directory.
- The new disposable `reader/` tree contains copies of exactly 14 selected public execution inputs: eight source modules, two author readbacks, two reviewer-control Lean files, and two unchanged validation scripts. No historical `.olean`, logs, omitted author/reviewer source-copy tree, or private research source was copied.
- `READER_INPUTS_BEFORE.json` and `READER_INPUTS_AFTER.json` agree with each other and the matching public manifest inputs.
- Initial fresh object count: **0**. Final fresh object count: **8**. Only these newly compiled packet objects were used for packet imports.

## Explicit execution setup and dependency boundary

Read `REPRODUCIBILITY.md` section 3 and `TOOLCHAIN_REQUIREMENTS.json` before running. Their required reader-local `toolchain-restored/environment.sh` was provided exactly at the location resolved by both unchanged scripts. This three-line configuration wrapper contains comments and:

```bash
source "$TRUSTED_LEAN_ENVIRONMENT"
```

Here `TRUSTED_LEAN_ENVIRONMENT` denotes the installed environment script whose exact digest is recorded below; this placeholder replaces its historical host location. The sourced file and all Lean/Mathlib binaries, sources, and compiled dependency outputs remain **outside both the verified public payload and disposable reader tree**. The wrapper is local execution setup, not an additional selected public file or bundled dependency. It points at the existing trusted installation; it does not download, install, bootstrap, rebuild, or certify anything. No canonical source or staging file was edited.

The existing external environment supplies Lean 4.19.0 (displayed compiler commit `6caaee842e94`) and the declared Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b` installation with the pinned dependency lock and compatible objects. `REPLAY_RESULT.json` records every dependency revision in that supplied lock. External identity anchors match all declared historical hashes:

- environment script: `1ff5b5d46f1e67ee0c007e658ef2cffb7270425f581237d76a5a64a645090129`
- Lean executable: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`
- Mathlib entrypoint: `b0518254279fabf0c6a920804e684536b0f5e2bd1cb6318d0609eb563413f20a`
- Mathlib toolchain file: `55e97be96000b5e9e290c9e74482e5e317861499a5540353ce845471bded8cea`
- Mathlib dependency lock: `5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752`

These anchors identify the supplied trusted environment; they are not a fresh audit or certification of its entire contents. The excluded original environment record is bound by identity in the projected result; installed versions and digests remain available there. Installed Mathlib/dependency outputs and the Lean kernel remain trusted dependencies.

Both unchanged `validate.sh` scripts prepend their own fresh `src` path to the external-only `LEAN_PATH`. Each reviewer command resets to the external dependency path and prepends only the corresponding fresh packet `src`. `commands.trace` and the validation environment logs record these paths. There is no original author packet path or private research tree on the import path.

Directory integrity and execution setup are separate claims: public integrity was checked against the pristine public directory, while compilation ran only in the disposable source-only reader tree with its added local configuration, fresh outputs, and logs. The reader tree is not represented as a byte-identical copy of the complete public directory.

## Actual commands and coverage

`prepare_reader.py` records the explicit copy allowlist and initial state. From `reader/`, the unchanged public commands were:

```bash
bash tranche10/research/law-completion-correction/validate.sh public-replay-uniform
bash tranche10/research/law-completion-correction/nonuniform/validate.sh public-replay-nonuniform
```

Both exited **0**. The scripts compile sequentially using `timeout 180 lean -j1 -o src/MODULE.olean src/MODULE.lean`, then execute the packet's author readback using `timeout 180 lean -j1 readbacks/NAME.lean`.

Fresh module coverage, all exit **0**:

1. `LawCompletionCore`
2. `LawCompletionCompact`
3. `LawCompletionCounterexample`
4. `LawCompletionBranches`
5. `IndexedCompletionCore`
6. `IndexedCompletionCompact`
7. `IndexedCompletionForgetting`
8. `IndexedCompletionDiameter`

The included reviewer controls were then run sequentially using the documented same environment/fresh-packet-path instruction:

```bash
source toolchain-restored/environment.sh
DEPENDENCY_LEAN_PATH="$LEAN_PATH"
export LEAN_PATH="$PWD/tranche10/research/law-completion-correction/src:$DEPENDENCY_LEAN_PATH"
timeout 180 lean -j1 tranche10/reviews/existential-completion/formal-review-20261003T1229Z/ReviewerControls.lean
export LEAN_PATH="$PWD/tranche10/research/law-completion-correction/nonuniform/src:$DEPENDENCY_LEAN_PATH"
timeout 180 lean -j1 tranche10/reviews/existential-completion/nonuniform-formal-review-20261003T1259Z/ReviewerControls.lean
```

Both exited **0**. Actual stdout/stderr, shell trace, exits and per-module times are retained. One compiler lane was used throughout, with `-j1`, default heartbeat/recursion limits, and 180-second individual caps. No failed stage was dropped, replaced or silently skipped.

Readback coverage was independently matched by the complete multiset of declaration names, not merely by success status or count:

- Uniform author: **51/51** axiom readbacks (50 standard-axiom, 1 no-axiom)
- Nonuniform author: **33/33** (33 standard-axiom)
- Uniform reviewer: **5/5** (5 standard-axiom)
- Nonuniform reviewer: **10/10** (8 standard-axiom, 2 no-axiom)
- Total: **99/99**, with no axiom outside `propext`, `Classical.choice`, `Quot.sound`

The duplicate historical `AuthorReadback.lean` is handled as documented, through the included author readback already selected in the public packet; omitted historical reviewer input-copy trees were not supplied.

## Finding and evidence

**No essential omitted reproducibility step was found for this declared environment.** The documented local environment-file reconstruction and fresh source paths were sufficient. No correction or extra runtime framework is proposed.

The machine-readable result is `REPLAY_RESULT.json`. `verify_replay.py` verifies all eight module exits and command flags, exact author/reviewer axiom-readback name coverage, allowed axioms, fresh output count, trusted identity anchors, unchanged public/reader inputs, and the final public integrity check. Supporting evidence includes `command-exits.tsv`, `commands.trace`, stdout files, reviewer logs, and the new validation logs under `reader/`.

## Public projection

This is a metadata projection of the historical replay narrative. Its original identity and exact changed-location scope are bound in `tranche10/reviews/cross-component/public-projection-v4/PROJECTION_BINDING.json`. The original command trace, host configuration, working scripts, copied reader tree and compiled objects remain historical execution evidence outside this selection. Their omission does not change the reported command results or expand the trusted dependency claim. Only files named by the outer selection manifest are distributed.
