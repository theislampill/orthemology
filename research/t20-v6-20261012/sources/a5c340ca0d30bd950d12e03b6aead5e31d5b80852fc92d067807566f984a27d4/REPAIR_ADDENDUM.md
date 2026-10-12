# Independent repair addendum

## Bounded verdict

The saved, unapplied seven-line recognition guard passes independent before/after replay in a fresh local copy. It is suitable to retain as an **unapplied candidate repair with this test evidence**. This is not repository integration or release qualification.

## Exact bindings

- Pinned commit: `c86b3c6673147b8802fe222373a165a37d4d24a8`
- Candidate patch SHA-256: `ba1c28f70bc74b70451ae4a63910f49308a23d5b068d1a3e61c8cb0bf9c97a58`
- Checker preimage SHA-256: `ea6630a53ce8c77d6cc3102ae6ffd5aba0dc84539f1ffe5350fbc1aa4d9c4d1a`
- Checker preimage Git blob SHA-1: `469a1d4e60520671171caf4989353460eada7a8b`
- Checker postimage SHA-256: `303297476f2d69b85019adf203949b49d6034a64d58ad7022321b999ac7d0059`
- Original finding report SHA-256: `1c0cfe14a7cf031eb8c9898e080f2676275013ef3269fd859c7a87f01e5bf981`
- Original evidence manifest SHA-256: `6cadd57bae9e8ca1e9e9f9898f0eaf6df5d5b99fca7f6f651408b33692b1a788`
- Repair results SHA-256: `99d6bfc2166a296698aa456aefbda3851f15cd05f58fcc2f9074a8dc6a74e599`

The patch applies with `patch --fuzz=0` after a successful dry run. Removing exactly its seven inserted lines reproduces the byte-identical pinned preimage. The original report, inputs, results, logs, and manifest remain unchanged: 46 original evidence files verified before and after.

## Independent outcomes

Each condition was tested through `validate_instance`, the main custom CLI, the compatibility CLI, and the complete JSON Schema:

| Condition | Patched custom API and both CLIs | Complete schema |
|---|---|---|
| Advanced / strong | Pass, exit 0 | Pass, exit 0 |
| Advanced / medium | Reject, exit 1 | Reject, exit 1 |
| Advanced / weak | Reject, exit 1 | Reject, exit 1 |
| Advanced / none | Reject, exit 1 | Reject, exit 1 |
| Advanced / recognition missing | Reject, exit 1; existing required-field error | Reject, exit 1 |
| Nonadvanced (`blocked`) / none | Pass, exit 0 | Pass, exit 0 |

Before applying the candidate locally, medium/weak/none reproduce the original custom false pass. The strong and nonadvanced controls remain accepted before and after. Missing recognition remains rejected before and after. The 54 embedded negative self-checks pass before and after; the candidate introduces no failure in that embedded suite.

The guard is limited to advanced alignment and does not replace or weaken the unconditional required-field check. Only the three intended recognition mutations acquire the new guard error in this experiment.

## Limits and evidence

The complete-schema-clean synthetic control and the two-entry compiler-derived module-map projection retain all limitations in the original finding review. The unrelated category-3/open-gate schema inconsistency is explicitly rerun and still fails; this candidate does not repair it or establish complete schema coverage. No protected source was changed, no complete runtime was rebuilt, and no whole-CI, live-model, knowledge, willingness, recovery, or warrant claim follows.

Command: `python -B noetic-guard-repair-peer-review-20261009/replay_repair.py` (exit 0).

`REPAIR_PEER_RESULTS.json` records both stages, hashes, and results. The fresh replay directory named in that file contains exact fixtures, the locally patched copy, and each command's exit code, stdout, and stderr under `logs/`. `SHA256SUMS` binds all addendum files. The patch remains unapplied to the original pinned source.
