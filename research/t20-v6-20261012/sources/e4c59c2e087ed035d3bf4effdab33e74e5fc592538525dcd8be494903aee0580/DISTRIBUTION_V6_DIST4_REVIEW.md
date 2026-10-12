# Independent distribution review: operational-model v6 dist4

Verdict: **PASS for the exact source-only archive and its portable replay route under the disclosed trusted-toolchain/cache boundary.** This is distribution acceptance, separate from the prior scoped scientific acceptances. It adds no theorem or whole-program/progress claim.

Accepted archive: `Eighth_Operational_Model_Checkpoint_v6_dist4.zip`, 609,505 bytes, SHA256 `e7b9f11be186b9e1d57b9ecdcaa4fbc0b066a74a0463cd1d3c0b65800274b2cd`.

Public manifest SHA256: `395d3beddf9075d7edde1a148699b0e2e35c8a378c390a61608150cc9a0012b5`.

Scientific manifest SHA256: `58798e94a43d42595c58f61de8c0ec42be89275530d00b52e4f31024b4e7f611`.

## Exact archive and projection

The review read and safely extracted the actual ZIP, rather than treating an author source directory as the package. All 105 entries are unique canonical relative paths and regular mode-0644 files. There are no encrypted, traversal, symlink, or compiled-object entries; ZIP integrity checks passed. All 56 frozen scientific files, including their manifest, match the independently accepted v6 snapshot exactly.

The 39 projected review artifacts match the original reviewer files byte-for-byte. This includes the current v6 and v5 receipts, corrected v4 receipt/report, original v4 records, explicit reporting correction and delta, older scoped reports, challenge sources, and bound successful evidence. The corrected 64-character native-source digest is authoritative; the older mistyped records retain their historical provenance role. The exact 3,013-byte native input and its embedded Lean byte list remain bound and verified.

Four historical review drivers are explicitly omitted by `PROJECTION_MAP.json`, with their original byte counts, hashes, and provenance roles retained. Their omission is not represented as byte preservation of included files. The portable top-level `replay.py` replaces those historical entry points. The five historical `AllAxioms.lean` files and their logs are provenance evidence; the portable route generates a fresh aggregate audit for the current package.

The archive contains no custom build objects, build directories, private design/process notes, or failed exploratory logs. Historical absolute command paths inside proof receipts are evidence of those runs and are not executable replay inputs.

## Packaging correction lineage

Preserved dist3 has SHA256 `ea2df4fe8e71a000342fce8bf3e29e5be635398a6d8be1de47bd868b74b5728e`. Its static projection and wrapper controls passed, but its README described an “invertible state/event translation.” That wording overstated the event result: arbitrary common timestamp annotations are erased, and the chosen reverse lift introduces zero annotations.

Dist4 changes only `README.md` and `PUBLIC_MANIFEST.json`. The README now says “Inverse state translations and event correspondence up to timestamp erasure” and explicitly explains the chosen zero lift. All scientific, reviewer, wrapper, and test bytes are unchanged. The dist3 archive and extraction remain preserved; distribution acceptance applies to dist4's exact digest.

The earlier archive with SHA256 `375bf13ad4e1b2301620af8cdbfe4cc049c0b8d69242b769f2026c43d63c3cba` is also preserved. The package's distribution correction describes the earlier overly broad cache requirement for unused Cli. The accepted route explicitly distinguishes the seven required package caches from that unused pinned package.

## Independent full replay

The reviewer launched the extracted dist4 `replay.py` from an unrelated working directory into a new absent output directory. Deliberately invalid `LEAN_PATH`, `LEAN_SRC_PATH`, and `LEAN_SYSROOT` values were inherited by the launcher. Invalid object-file sentinels with custom module names were placed in both the caller directory and the poisoned import directory. Their bytes remained unchanged, and they were not used by the successful replay.

All 47 stages were built freshly: nine accepted imports, 32 scientific modules, five independent reviewer challenge modules, and one newly generated aggregate axiom-audit module. No previous custom proof objects were supplied. The fresh aggregate audit covers all 312 scientific and 40 reviewer theorem declarations, for 352 checked closures. Each closure depends only on a subset of `propext`, `Classical.choice`, and `Quot.sound`. The proof-token checks and every compiler stage completed without warnings, errors, or `sorryAx`.

The route used official Lean 4.19.0, commit `6caaee842e94`, executable SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, sequentially with `-j1 -s65536`. It verified all 6,816 pinned dependency source records and the exact native source embedding. Every stage uses an explicit source root and checkpoint working directory; all generated objects and logs are placed outside the package. The package identity was reverified after compilation. The outer ZIP digest was independently checked again after the run and remains unchanged.

The independent run completed successfully at `2026-10-02T22:30:33.253697+00:00`. Its receipt is `distribution-v6-dist4-review/fresh-replay/RECEIPT.json`, SHA256 `fb8e737d5e1d2a70b630dc0c50a5d167f3c69d31b87fbd954cd3d0711b09e741`. Launch, exit, successful stage logs, source hashes, command lines, and a fresh all-theorem audit are separately retained as evidence.

## Wrapper controls and cache boundary

All twelve supplied lightweight boundary tests passed when invoked from the unrelated directory. Nine additional independent control groups passed against the extracted package, including:

- Resolved output-parent symlinks cannot enter protected input trees; broken output symlinks are rejected.
- Each of the seven required package caches independently fails closed when absent. This was checked for every named cache, not just the first one.
- Present unused Cli and unlisted package caches are excluded from the import path.
- Duplicate package identities and public inventory paths are rejected.
- The actual package verifier rejects unlisted empty directories and altered review receipt identity.
- The actual CLI rejects existing output before compiler or dependency access and preserves an existing sentinel.
- The actual CLI rejects nonpositive, excessive, and nonfinite timeout values before output creation.

The required caches are exactly `LeanSearchClient`, `Qq`, `aesop`, `batteries`, `importGraph`, `plausible`, and `proofwidgets`. Their expected set is checked against the pinned Lake manifest, itself included in the independently hashed dependency source pin. Cli's compiled cache was absent in the supplied installation and explicitly recorded as unused; it was not silently treated as an arbitrary missing dependency. Unlisted directories do not enter the import path. Missing required transitive objects would still fail the compiler stages. No dependency was downloaded or rebuilt.

Existing-output, protected-output, source corruption, inventory, source-path, fatal-diagnostic, and timeout guards are fail-closed for the tested conditions. Timeout diagnostics are retained, and a failed stage cannot create a PASS receipt in the fresh output. The caller's inherited Lean import/source settings are replaced or removed before compilation.

The compiler and supplied compiled dependency/standard-library toolchain remain trusted inputs. Source pin verification does not prove that cached objects were independently reproduced from those sources. This distribution review does not claim a full bootstrap, a dependency-cache rebuild, hardware verification, or resistance to a concurrent adversary modifying the trusted toolchain. The package accurately discloses this boundary.

## Acceptance ceiling

The README and theorem guide preserve the accepted scientific limits: full-envelope identity, raw base 2→3, complete policy/certificate alignment, fixed lifetime faults, partial preparation and cancellation effects, one-way cancellation certification, and the newly named monotone reference-clock class. Set-now is not an existing service operation; weak numerical monotonicity allows stalling and unbounded jumps. The four-root witness is not a fault-discovery strategy. Physical time, actual authority/reservation, authentication, source interpretation, atomic live mediation, progress, runBatch, alias transport, and N2/T0/R5 remain outside the demonstrated result.

No further correction is required for this exact dist4 archive and route. This acceptance record is external to the tested ZIP; the ZIP has not been edited to include its own later acceptance.
