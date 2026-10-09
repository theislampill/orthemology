# Replay instructions and dependency limits

## 1. Extract and verify

```sh
python3 -m zipfile -e T20_Warrant_and_Empirical_Audit_Checkpoint_20261008.zip unpacked
cd unpacked/T20_Warrant_and_Empirical_Audit_Checkpoint_20261008
python3 PACKING/check_manifest.py
```

Optional system checksum check:

```sh
sha256sum --check MANIFEST.sha256
```

The root manifest enumerates this ZIP's actual payload. Original nested manifests remain unchanged and retain their historical scope. Their presence is not a claim that every ancestral dependency or source body is in this ZIP.

## 2. Replay the controls

Recorded environment: Python 3.12.14 and SciPy 1.17.0. Six controls use only the standard library and included local files. SciPy is required solely to recompute the seven printed t/F tail probabilities. It is not bundled or installed by the harness. Use an environment with the pinned package in `PACKING/requirements-arithmetic.txt`; Python/SciPy version changes can alter metadata or floating output bytes.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0 python3 PACKING/replay_python.py --output ../fresh-warrant-empirical-replay
```

The harness validates copied-file hashes, runs all seven commands in a temporary copied tree, compares four deterministic result files and the independent reason result with frozen versions, and confirms the checkpoint files are unchanged. Logs and a new receipt go outside this checkpoint. This protects original outputs from scripts that normally overwrite their own result files.

Exact command subjects:

1. `catalogue-mixture-sampling/exact_controls.py`: fifteen author control families.
2. `catalogue-mixture-review/frozen/exact_controls.py`: the same frozen author controls, as an independent snapshot replay; not fifteen further discoveries.
3. `catalogue-mixture-review/independent_checks.py`: five independent control families, including robustness extensions.
4. `catalogue-mixture-review/verify_receipt.py`: sealed review and author payload hashes.
5. `reason-causation-bridge/model/check_bridge.py`: finite implementation, interventions and two failing mutants.
6. `reason-causation-review/independent_checks.py`: independent truth-table/bit checks, frozen author output, nineteen payload hashes and thirteen predecessor bindings.
7. `fitrah-warrant-bridge/public-study-reanalysis/recompute_reported_statistics.py`: seven printed aggregate statistics, including two discrepancy assertions and unaffected significant controls.

All paths above are beneath `t20-next-frontier-20261008/`. The full invoked commands, exit codes and equality results are in `PACKING/REPLAY_RECEIPT.json`.

## 3. Checks deliberately not performed

- No inherited Lean `--trust=0` replay, dependency build or mutation-suite rebuild. The compact predecessor subset is insufficient for a full Lean environment. The preserved historical logs are not fresh packaging results.
- No actual hardware or human-cognition experiment, new empirical trial, participant-level reanalysis, or replication.
- No reacquisition or fresh reading of absent modern source bodies, complete source bibliography verification, or new citation-edition collation.
- No new philosophical adoption, historical active-duration certification, owner acceptance or closure.

`PACKING/INHERITED_INPUT_COVERAGE.json` lists the exact minimal hash dependencies and the missing members of copied ancestral Lean source manifests. These are deliberate scope limits, not unexplained corruption of the delivered payload.
