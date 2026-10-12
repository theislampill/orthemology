# Independent public-projection and portable-replay review

2026-10-02 UTC. **PASS for public projection V5 at the publication/portability scope below.** This review awards no new scientific credit and supersedes the earlier V4 working report.

## Bound subject and resolved findings

Reviewed V5 `PUBLIC_MANIFEST.json`: SHA-256 `fe21c5379ea36fa47d5d49ba488ba5644e35ad417a59a001662b60fef8bbc252`. Immutable scientific archive: SHA-256 `df8f13aa634a7c00256d7dc253bcc997bea13ab53000af9b00130a24698546fb`.

Two distribution-only issues were resolved in preserved successors:

1. V3 replayed `ReviewChallenges.lean` but omitted the separately accepted V2 `ReservationDomain.lean` check. V4 adds both reviewer files to the wrapper loop.
2. V4 reread its manifests at the end without retaining their initial identities. Independently reproduced the gap: after the first compiled module appeared, a disposable copy's `HistoryModel.lean` was changed and the mapping/public-manifest hashes updated coherently; V4 still returned PASS. V5 captures manifest and mapping hashes before initial verification, checks both identities around final verification, and records the initial identities in its receipt. The same coordinated rewrite reached both reviewer files but was refused by V5 without a PASS receipt.

Each successor changes only `replay.py`, public `README.md`, and `PUBLIC_MANIFEST.json`. The original-to-public mapping and all scientific/review/source bytes remain identical. V3 and V4 originals are untouched. The final PASS applies only to V5's exact digest.

## Public projection

Independently reconciled all 176 original ZIP entries against original bytes, sizes, and hashes: 172 unchanged in place; the old top-level README and manifest relocated unchanged under `provenance`; exactly the root and frozen-candidate-v1 PLAN bodies omitted with their original sizes and hashes retained. Five new public files bring the payload to 179 files; the public manifest lists all 178 other files exactly. No symlink or unsafe archive path is present.

Searched every distributed file for either omitted body, whitespace-normalized bodies, base64/hex encodings, and long original paragraphs. No reproduction was found. The payload contains no nested compressed archive. Unchanged historical manifest references to absent plans are expressly reconciled by the public mapping. Acceptance, review, and candidate-snapshot bindings verify.

## Independent portable replay

Created a fresh V5 copy under the assigned review directory, setting all 179 files to mode 0644. Ran Python with explicit official Lean and Mathlib paths, a new output directory, deliberately invalid inherited LEAN_PATH, and paths containing spaces. The unchanged wrapper passed:

- Five modules compiled into a fresh isolated build directory.
- Both original fixtures compiled.
- All seven original false claims failed for the intended Lean false-proposition reason.
- All seven accepted-source Python scenarios passed.
- Both V2 reviewer proof files compiled with no warnings, errors, or proof-hole diagnostics.

The wrapper never selects `private-locator:351b8592ab6e0e21df70` internally, invokes no archive shell script, and requires no archive executable mode. Subprocess calls use argument vectors for the explicit compiler or active Python interpreter. LEAN_PATH is replaced by the fresh build and explicit dependency caches, excluding historical candidate builds. The original control generator's literal claim table is consumed without executing its workspace-dependent launcher.

Verified the compiler hash and release version. Independently reconciled all 6,816 Mathlib source-pin entries with both the supplied source archive and source tree. Full before/after snapshots of 58,914 entries across supplied Mathlib and Lean toolchain trees were identical in file content, modes, and symlink targets. Dependencies were neither modified nor rebuilt. Projected files and all eleven owner-source/review bindings are checked before and after; independent payload and scientific-archive hashes also remained unchanged.

## Refusal checks

Fourteen early-refusal probes against V5 passed: required argument omissions; wrong/missing compiler; corrupt/missing scientific source; corrupt wrapper or provenance README; either omitted plan path reintroduced; corrupt/missing Mathlib source; absent compiled cache; and nonempty output. The existing output marker was preserved. Every expected refusal produced no PASS receipt. The coordinated three-file late rewrite described above separately confirms that initial metadata identities cannot be redefined to make the final integrity check pass.

## Scope and distribution

PASS covers the exact V5 digest and observed publication/replay properties on the pinned Linux Lean 4.19.0 toolchain. Supplied compiled caches remain trusted read-only inputs; this is not an independent cache rebuild or universal operating-system portability claim. The immutable V2 scientific review and its original conditional finite-history/whole-table interface ceiling remain authoritative, with no added liveness, real-consent, physical-realization, or interface-transport credit.

`RECEIPT.json` binds only the compact decisive evidence in `publication-evidence-v5/`. Working payload copies, deliberately corrupted fixtures, full dependency snapshots, build binaries, superseded working reviews, and the original scientific ZIP must not be included as these public review sidecars. Add the listed sidecars under a separate outer package manifest without altering the reviewed V5 payload or public manifest. No material publication/portability gap remains for V5.
