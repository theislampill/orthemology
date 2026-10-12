# Independent bounded final-handoff review

Review date: 2026-10-12 (UTC).

## Outcome

Accepted for the stated finite source-only package preparation and integrity-verification role after two consequential CLI bootstrap findings were repaired and independently replayed. This accepts the bounded implementation at the exact hashes below, not any final source selection, publication rights, scientific claim, or publisher authenticity. Actual selected-package delivery verification remains a separate root-owned step.

Reviewed final code:

- `final_handoff_tools/verify_handoff.py`: SHA256 `1b91ecebd2dc55e4018a38a9a3fb7a09f1f245b778cea493a6fb1fb60c61c0ef`
- `final_handoff_tools/prepare_handoff.py`: SHA256 `8ede41ebe43aa8f297184b1982e6de8102bd9332c81846d05b4422ce3fb4c31d`

Earlier helper contracts remained unchanged:

- `plan_selection.py`: SHA256 `c6cf6788ccd51f546e8a43464c211858dbd4d2cb14cd791358c33843e8dde238`
- `materialise_selection.py`: SHA256 `9b4f982297bb4b85e5e3331fc5b990c539d37e80491dc82ac809f75de7b25be4`

## Findings repaired

1. The original verifier allowed every import search directory below `sys.base_prefix`. A handoff extracted below that prefix therefore executed adjacent `tools/json.py` before verifying inventory. A temporary trusted Python home with its standard library linked to the existing installed standard library reproduced this under both normal Python and `-O`. Evidence: `IMPORT_PREFIX_RED.log`. The repaired CLI uses only the interpreter-reported standard-library directory and the narrow extension-module directory, without retaining arbitrary package or PYTHONPATH search roots. Independent regression covers a package beneath the interpreter prefix and a separate retained PYTHONPATH directory beneath that prefix.
2. The verifier's initial `from __future__ import annotations` executed before bytecode disabling and import hardening. A retained `tools/__future__.py` ran under normal and optimized Python, and Python created `__pycache__`. Evidence: `FUTURE_IMPORT_RED.log`. The unnecessary future import was removed; built-in `sys` is now first, followed by bytecode disabling and import hardening before non-built-in imports. The builder was also narrowly hardened: its CLI applies the same initial bootstrap and loads only the explicitly trusted sibling verifier by exact path.

The reviewer did not edit implementation files. Repairs were made by the implementer and then rerun independently.

## Independent evidence

All commands used the installed CPython 3.12 interpreter. Both normal and optimized execution passed:

- 36 final supplied handoff controls: `FINAL_NORMAL.log`, `FINAL_OPTIMISED.log`.
- 11 separately authored controls using manually constructed plan/map/receipt/CAS metadata, without the planner or materialiser as fixture producers: `test_review_handoff.py`, `INDEPENDENT_NORMAL.log`, `INDEPENDENT_OPTIMISED.log`.
- 102 existing parent-directory planner/materialiser/projection/received-public/scope controls: `EXISTING_NORMAL.log`, `EXISTING_OPTIMISED.log`.

The supplied copied-contract test compares 20 function ASTs, with only the materialiser's `p.` helper qualification removed. The separate static pass additionally compared all nine copied schema/regex/reason/basis/role constants exactly by AST: `STATIC_PARITY.log`. No verifier assertions were found, so validation is not removed by `-O`. Static source inspection found no subprocess, network, dynamic source import/evaluation, or filesystem-writing operation in verifier validation. The builder's only dynamic code loading is its explicitly trusted verifier harness.

Independent fixture observations include:

- Exact CLI invocation from a handoff root succeeds in normal and optimized modes with an explicit expected manifest digest.
- Both modes preserve all recorded source/package file bytes and modification times, and add no files or bytecode.
- Rebound plan, view-map, materialisation receipt, and manifest hashes cannot conceal a dropped dependency blocker, a missing dependency disposition, an invalid boolean source size, or contradictory curated-source identity.
- Adjacent `__future__`, argparse, json, pathlib, re, stat, unicodedata, and hashlib modules are not executed by the verifier.
- The builder CLI ignores adjacent `__future__`, argparse, json, pathlib, hashlib, and importlib modules and preserves source/helper bytes and modification times.
- Existing/overlapping targets are rejected; ordinary copy output inodes differ from a source hardlink and from each other.
- Supplied controls additionally exercise exact inventory, forbidden extra files and empty directories, symlinks, FIFOs, path traversal and platform-reserved names, alias prefix/casefold collisions, source size/hash drift, received-public semantic failures with outer hashes rebound, and unchanged original metadata.

`FINAL_HASHES.txt` records exact reviewed code, tests, helper contracts, and documentation hashes. Initial vulnerable versions are identified by `INITIAL_HASHES.txt`; the independent red logs establish that the two findings were observed, not hypothetical. `INDEPENDENT_POST_FIX_FIRST.log` and `BUILDER_INITIAL_CHECK.log` were captured after concurrent implementation fixes, so they are green observations and are not red evidence.

## Limits and release prerequisites

- The independently approved final selection remains a prerequisite. Eligibility labels and public plan metadata cannot independently establish rights, original authorship, the completeness of source/rights review, or truth of scientific claims.
- Validation proves byte consistency and declared custody relationships relative to the supplied exact manifest. An unkeyed manifest does not authenticate itself. The intended verifier and manifest must be trusted through an external boundary; the final archive hash and delivery check belong outside the archive.
- The verifier preserves earlier declared dependency and received-public rules. It does not discover undeclared dependencies, invent license/notice obligations, establish original/received equivalence, or independently prove that a declared complete-body reading actually happened.
- The source store, selected metadata, and explicitly declared curated aliases are the whole package. Every delivered tool must itself have a selected source identity and explicit alias; the builder adds no hidden tooling.
- The CLI requires a trusted interpreter exposing `sys._stdlib_dir`, trusted standard-library/startup behavior, and trusted verifier code. The builder additionally trusts its exact sibling verifier harness. The bootstrap runs only once the CLI script starts; interpreter startup and an importing caller's existing process/import environment are outside it. Windows, alternative interpreters, and zipped-only standard-library installations were not exercised here.
- The filesystem is trusted not to change concurrently. Symlink/path rejection is not a hostile-race sandbox. All selected payload bytes are read into memory; this is a finite declared-input tool, not an adversarial resource-exhaustion service.
- A failed builder write can leave a partial fresh output. Success requires final verification; the last-written manifest is not sufficient merely because it exists. Existing source/protected roots are never deliberately modified.
- No actual research source was executed, no network operation or repository edit/merge was performed by this review, and no final delivery archive was assembled by the reviewer. Synthetic sentinel files were used for controlled import regressions.
