# Exact replay instructions

## 1. Unpack and verify

Prerequisites: Python 3.12 (the recorded version) and its standard library. No Python package installation is required.

From the directory containing the ZIP:

```sh
python3 -m zipfile -e T20_INTERMEDIATE_RESEARCH_CHECKPOINT_20261008.zip unpacked
cd unpacked/T20_INTERMEDIATE_RESEARCH_CHECKPOINT_20261008
python3 PACKING/check_manifest.py
```

Optionally also run `sha256sum --check MANIFEST.sha256` on a system with that command.

## 2. Portable scoped Python replay

Run from the checkpoint root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 PACKING/replay_python.py --output ../fresh-python-replay
```

The harness copies the entire compact evidence tree into a temporary directory. Commands that produce results write only to that disposable copy. New logs and a receipt go to the requested output directory, which must be outside this checkpoint. Original archived results remain unchanged.

Included checks:

1. Exact nonabsorption diagnostic.
2. Seven wise-determination adapter tests, with the retained reactive model.
3. Eligibility premise-removal and quantifier audit.
4. Twenty two-root author tests.
5. Eight general-root author tests.
6. Eleven CRT author tests.
7. Seven independent two-root v2 control groups.
8. Five independent general-root control groups.
9. Four independent CRT control groups.
10. Independent CRT/author-constructor crosscheck.
11. CRT evidence verifier, including its isolated replay and predecessor hash checks.
12. Productive-identifiability export, required byte-equal to the frozen result.
13. CRT export, required byte-equal to the frozen result.

The exact invoked commands, exit codes, test counts where printed, and limitations are recorded in `PACKING/python-replay/PYTHON_REPLAY_RECEIPT.json`.

### Deliberately limited replay

- `productive-identifiability/src/verify_evidence.py` checks eight historical/source input hashes before its tests. Five inputs are omitted here: two `t20-continuation-20261008/effect-production` predecessor files, the recovered `causal-abstraction/RESULT.md`, the recovered `tensor-geometry-lineage/README.md`, and raw `nonabsorption/sources/majmu20-item2031.txt`. Their hashes and original verification receipt are preserved. This compact archive replays the exact test code/export with its two actual runtime dependencies, without pretending to replay that complete provenance wrapper.
- `wise-determination/review/transport_probe.py` has a hard-coded `[OMITTED_PRIVATE_MACHINE_PATH] root. No rewrite is made. Its original exhaustive transport result and bindings are included; this script is not portable as written and is not rerun by the packaging harness.
- Development failures and older review v1 files are historical negative evidence. The current exact mathematical replay uses frozen v2.
- These scripts do not replay primary-source reading, independently authenticate source text, or settle the pending philosophical reassessment.

## 3. Optional fresh Lean author replay

This is not an offline/self-contained step. Use a disposable extraction/copy. Requirements: Linux x86-64, Bash, curl, Git, tar with zstd support, and network access to official Lean/Mathlib release/cache hosts. The official pinned bootstrap installs into the copied package only. Dependency downloads are large and are deliberately excluded from this ZIP.

From the copied checkpoint root:

```sh
cd t20-next-frontier-20261008/formal-route-probability
bash bootstrap.sh
bash verify.sh
bash mutation_checks.sh
cd ../formal-identification
bash verify.sh
bash mutation_checks.sh
```

The forward bootstrap first validates the frozen inverse source manifest and installs the inverse's pinned toolchain/dependencies, then obtains the added Mathlib imports. Pins: Lean 4.19.0; official archive SHA-256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`; Mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`. Full dependency details are in `formal-identification/DEPENDENCY_MANIFEST.json`.

The inverse is an immutable sibling dependency of the forward proof. Do not flatten directories. Do not treat a dependency/network/import error as a valid semantic-mutation rejection.

## 4. Optional fresh independent Lean review replay

After the bootstrap above, from the copied `t20-next-frontier-20261008` directory:

```sh
bash formal-identification-review/replay_frozen.sh
bash formal-route-probability-review/replay_frozen.sh
```

Run the inverse review first so the reviewed inverse modules are rebuilt before the forward review imports them. The scripts derive the dependency paths from their own locations. The forward review includes a `--trust=0` final check. Existing independent mutation receipts and failure/restoration logs are included; their detailed setup is preserved in the review scripts and reports. The author mutation scripts above provide a standalone setup path for fresh mutation checks.

The two original delivered source tarballs remain included unchanged under each formal component's `deliverable/` directory. Their hashes are listed in `COMPONENT_STATUS.json`; they contain no toolchain or Mathlib tree.
