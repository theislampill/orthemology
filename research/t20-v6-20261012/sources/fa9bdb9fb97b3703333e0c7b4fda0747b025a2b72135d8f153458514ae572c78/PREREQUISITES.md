# Exact external prerequisites

## Tested replay platform

- Python 3.11+ using only the Python standard library for the package tooling and included finite control/norm probes
- Git, needed to read the exact official dependency commits and tracked cleanliness
- Official Lean 4.19.0, Linux x86_64, commit `6caaee842e94`
- The Mathlib checkout at `c44e0c8ee63ca166450922a373c7409c5d26b00b`, with its official transitive packages at the exact commits in `pins/lake-manifest.json`

The portable wrapper accepts `--lean` and `--mathlib`; it never guesses `private-locator:3210001b2e88c26a7f09...` paths, changes a repository, downloads dependencies, installs software, or silently substitutes another Lean version.

## Official toolchain acquisition

The official release URL and SHA-256 are in `pins/TOOLCHAIN.json`:

`https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst`

Archive SHA-256: `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`

Extract it only after checking the archive digest. The wrapper also checks the executable digest `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` and full version string. Other platforms/builds are not silently accepted; porting to them requires a separate compiler-identity qualification.

## Official dependency layout

Use an isolated Mathlib checkout at the pinned commit. Its transitive source repositories belong at `mathlib4/.lake/packages/NAME`, with the nine dependency source revisions enumerated in `pins/lake-manifest.json`. Mathlib itself is `--mathlib`; the eight other package directories are beneath it.

Use the pinned checkout's standard Lake/Mathlib cache setup to obtain official build artifacts, or build those official sources yourself. Do not update the lock file to newer revisions. The wrapper checks each repository's `HEAD` and tracked cleanliness before reading compiled official libraries. Packages that are only build-time tools may have no compiled-library directory; this is recorded, and a missing actually imported module still causes Lean to fail.

The replay environment contains only the newly compiled custom library and official package libraries. Ambient `LEAN_PATH` and `LEAN_SYSROOT` values are discarded. Existing custom build artifacts are never copied into the fresh output.

## What the dependency evidence establishes

This package has not duplicated the multi-gigabyte official toolchain/cache and does not claim a clean-network bootstrap was executed in the packaging environment. The provided replay can establish that all bundled custom modules compile from their sealed source bytes and that every listed declaration has its audited type and approved axioms under the pinned external official environment.

For a stronger cold-bootstrap result, obtain the pinned official sources on a new machine, build/retrieve their official caches through their standard upstream workflow, and run the same commands. Retain that machine's dependency acquisition receipts separately. No portability claim depends on copying a historical custom `.olean`.

## Preserved metadata nuance

The original P02 PR source-closure JSON retains its older 35-module `topological_module_order` field and adds the authoritative 43-module `topological_build_order`. Both are preserved unchanged. The portable suite independently computes the order from all 43 included source imports and checks it against the new 43-module field; it does not use the stale 35-module field to omit new sources.

The preserved Codec/Pi3 closure contains historical absolute source paths across P02, measure and tagged-row workspaces. The staged `sources/codec-pi3/` copies bind every file to the sealed SHA-256 and rebase module paths within one complete 49-module closure. The portable replay does not consult those historical absolute paths.
