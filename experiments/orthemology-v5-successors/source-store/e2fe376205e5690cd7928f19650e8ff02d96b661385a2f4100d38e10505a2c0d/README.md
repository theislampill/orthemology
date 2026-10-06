# Ninth selector family: public sources and acceptance

Read `SCIENTIFIC_SCOPE.md` for the accepted statements and limits. This package
contains exact A1/A2/A3 scientific sources and reviewer controls, unchanged
original manifests and acceptance receipts, explicit per-entry projection maps,
and a portable replay wrapper. It contains no compiled objects, toolchain or
external dependency archives.

The two exact predecessor ZIPs are supplied separately. Their filenames, full
hashes, sizes and member counts are in `EXTERNAL_PACKETS.json`. They are not
duplicated in this archive. Obtain the Lean 4.19.0 and Mathlib revision recorded
in the core packet's `DEPENDENCY_PINS.json`, with its official dependency cache.
No command below downloads or modifies dependencies.

## Artifact verification

From any working directory, use the extracted package's verifier and the manifest
SHA-256 published with the archive:

```sh
python3 verify_artifact.py --root . --expected-manifest-sha256 MANIFEST_SHA256
python3 -O verify_artifact.py --root . --expected-manifest-sha256 MANIFEST_SHA256
```

The verifier can instead check the ZIP using `--archive SELECTOR_ZIP` and
`--expected-archive-sha256 ZIP_SHA256`. Supply the same expected manifest digest.
These checks verify files and original-to-public bindings; they do not run Lean.

## Out-of-tree replay

Use absolute arguments or paths relative to the current working directory.
Spaces in paths are supported. The output must not exist and must be outside all
protected inputs. The wrapper and verifier work under normal or optimized Python.

```sh
python3 replay.py \
  --expected-manifest-sha256 MANIFEST_SHA256 \
  --core-zip Eighth_Semantic_Controls_Core_20261002.zip \
  --literal-zip Eighth_Literal_Runtime_Counterexamples_20261002.zip \
  --lean-bin LEAN_BIN_DIRECTORY \
  --mathlib MATHLIB_SOURCE_DIRECTORY \
  --mathlib-archive EXACT_OFFICIAL_MATHLIB_ARCHIVE \
  --out "new replay output"
```

Without `--core-output`, the wrapper builds only the inherited positive runtime
closure, sequentially, using the exact predecessor core driver in runtime mode.
It does not run the historical cost/full-mutant probes. If an exact completed
core replay is already available, `--core-output CORE_OUTPUT_DIRECTORY` checks
its 167 source/object bindings, exact object census, absence of symlinks and
receipt status before reuse. Such reuse is reported as existing evidence.

It then freshly compiles 15 modules: three literal dependencies, eight A1/A2/A3
proof/readback modules, and four reviewer controls. It checks all 138 scientific
and 45 reviewer axiom declarations. Each Lean invocation uses `-j1`, has a
180-second wall bound, and adds no heartbeat options. The unchanged finite
arithmetic and original census-helper controls run in disposable output layouts.
Historical scripts using assertions run with optimization disabled explicitly;
the public wrapper's own guards remain active under `-O`.

For file-only intake use the same command with `--verify-only`, omitting Lean and
Mathlib arguments. This still requires a new output directory and both exact
external ZIPs, and creates a receipt explicitly recording no new kernel check.

`RESULT.json`, logs, temporary dependency extractions and new objects are written
only in the requested output. A failed or resource-limited stage remains a
separate result; it is not silently promoted to success or a theorem refutation.

## Projection contract

The six original source/review manifests are exact byte copies. Every listed
entry appears in its corresponding projection map with original size and hash.
PRESERVED_EXACT means a public file has exactly those bytes. OMITTED means its
public destination is null, a reason is explicit, and a public scope or receipt
view is identified. Omitted drafts are not synthesized or silently inserted into
old manifests. The new wrapper validates required scientific dependencies directly.

Historical replay scripts are preserved for source identity and guard controls,
not as supported public entry points: their original layouts included omitted
draft files. Use only the package-root replay.py for portable replay.

`PROOF_SOURCE_BINDINGS.json` binds every accepted scientific and reviewer Lean
module to the unchanged original manifests. `PACKAGING_VALIDATION.json` records
the projection checks and relocated wrapper exercise, separately from the
original independent scientific acceptance.
