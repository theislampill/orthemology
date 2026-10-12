# Compiled criterion installation with guarded execution

An independently accepted conditional mathematical/reference-execution checkpoint. The corrected installed rule changes real acceptance behavior, and a separately authorized guarded operation subsequently restores the exact source draft.

Start with `ARGUMENT.md` for the result and assumptions, `PUBLIC_VERIFICATION.md` for checks, and `independent-review/REVIEW_V2.md` for the independent assessment. `Composition.lean` and the exact imported Lean sources are the proof and executable model.

## Reproduce

```sh
python verify_projection.py
python replay.py --lean /path/to/lean-4.19.0/bin/lean --output-dir /absolute/path/to/fresh-output
```

The replay rebuilds every module, emits C, links and runs the native executable. Expected result: 88 named native assertions, seven wrapper checks, and complete before/installed/repaired state and byte artifacts. The official Lean 4.19.0 installation must include `leanc` beside `lean`.

Optional packaging tests:

```sh
python -m unittest discover -s packaging-tests -p 'test_*.py'
```

## What this archive contains

This is an explicit public projection of the reviewed v2 packet, not that complete original packet. `PROJECTION_MANIFEST.json` identifies retained original paths and exact hashes, excluded administrative documents, separately copied independent-review evidence, and new packaging files. Retained scientific arguments, contracts, proof/code, fixtures and evidence are byte-for-byte unchanged.

Historical source manifests and replay receipts are preserved as evidence. They identify their original source trees and are not complete manifests of this archive. Use `PROJECTION_MANIFEST.json` for this archive. Primary replay is self-contained apart from the toolchain; historical review scripts retain their original review-tree paths and are not additional self-contained entry points.

If the complete original v2 tree is available, `python verify_projection.py --source-freeze /path/to/composed-execution-v2` directly compares original and public bytes. If the complete upstream restart tree is available, `replay.py` also accepts `--predecessor-root /path/to/tranche7-restart`; without it, only bundled dependencies are checked, and no full-upstream verification is claimed.

The result does not certify physical interlocks, root independence, real permission, source authenticity, clock fidelity, compiler correctness or bounded external service. Those remain explicit applicability premises. No N2/T0 theorem, R5 defeat, deployment or whole-program closure is claimed.
