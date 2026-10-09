# Exact replay instructions

## Unpack and check the delivered payload

Python 3.12 was used. No third-party Python packages are required.

```sh
python3 -m zipfile -e T20_Additional_Mathematics_and_Source_Checkpoint_20261008.zip unpacked
cd unpacked/T20_Additional_Mathematics_and_Source_Checkpoint_20261008
python3 PACKING/check_manifest.py
```

On systems with `sha256sum`, also run:

```sh
sha256sum --check MANIFEST.sha256
```

The root manifest describes the actual ZIP payload, not the full contents of every historical source manifest. `PACKING/check_manifest.py` rejects changed or unexpected payload files. Original source-body omissions are explicitly described separately.

## Scoped Python replay

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0 python3 PACKING/replay_python.py --output ../fresh-additional-replay
```

The harness copies the compact evidence tree to a temporary directory and runs unchanged source scripts there. Original scripts that write their own metrics therefore cannot change this checkpoint. Output logs and a new receipt are written to the requested directory outside the immutable checkpoint.

The exact command inventory is visible in `PACKING/replay_python.py` and, for the subsequently frozen independent grouped review, `PACKING/ADDITIONAL_REPLAY_COMMANDS.json`. The delivered `PACKING/REPLAY_RECEIPT.json` lists every executed command and exit status.

The base checks are:

- Noise-aware author suite: 11 groups.
- Independent noise controls, restricted-mask lower-bound check, and frozen-decoder crosscheck.
- Countable author suites: 15 finite/countable groups, 6 gcd groups and 8 oracle/extension groups.
- Independent countable, gcd, arithmetic-boundary and frozen-decoder controls.
- Grouped-mixture author controls: 10 exact families.
- The frozen grouped author replay (10 families), independent grouped controls (5 families), and complete grouped receipt verification.
- Both noise-aware and countable deterministic exporters, whose output bytes must equal the included frozen `results/RESULTS.json` files.

The harness verifies copied-file hashes before replay and confirms that the immutable evidence remains unchanged afterward. Controls use exact finite arithmetic; no empirical trial set or new primary-source rereading is performed.

## Why the complete historical wrappers are not run

`noise-aware-calibration/src/verify_evidence.py` first checks historical productive-identifiability and single-calibration files. This additive checkpoint identifies the original predecessor archive and component digests rather than duplicating those reports.

`countable-signature-identification/src/verify_evidence.py` likewise checks predecessor files and expects the public-domain original Zsigmondy PDF when its metadata says `public-domain-original`. That body is deliberately omitted here for compactness. The script itself is preserved unchanged; this checkpoint does not alter it to conceal the missing provenance inputs.

The portable harness directly runs the exact author suites, independent controls and exporters with all of their actual local runtime dependencies. Running the complete historical provenance wrappers requires restoring all originally bound inputs at their exact paths from their identified sources. A missing-source error from those broader wrappers is not evidence that the included mathematical controls failed.

## No implicit Lean verification

There is no new Lean source/toolchain in this additional checkpoint. No Lean commands are run by the packaging harness. The earlier source-only Lean packages and their assurances remain in the prior checkpoint; this archive's new written mathematical deductions are not labelled kernel-checked.
