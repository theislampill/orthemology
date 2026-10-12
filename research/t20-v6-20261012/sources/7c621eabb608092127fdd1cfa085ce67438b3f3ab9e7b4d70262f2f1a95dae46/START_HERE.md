# Computable closed-input extraction: complete developments

10 October 2026. Independently reviewed PASS for this exact bounded addition.

The new Lean definition computes the count for a supplied actual closed derivation
`HasE [] n N`, using complete developments on the unchanged generic-open carrier.
Its positive finite certificates reconstruct actual source scalar instances for the
unchanged n and original Q. A separate finite rejection theorem can refute the
closed Church-input typing premise when a checked non-iteration normal form is
reached. It does not reject the scalar-instance target.

Read the frozen author `RESULT.md` and independent `REVIEW.md` in their named
subdirectories. The general termination theorem is distinct from the ten concrete
certificate controls and 266 reviewer implementation examples.

**No normal-order completeness theorem, strong-normalization theorem, complexity
bound, global Python verification, or universal typing decision is claimed.
The universal bound-variable `HasE [] c3 (W originalQ)` and its negation remain OPEN.
There is no T20 closure claim.**

## Exact predecessor archives, deliberately not duplicated

Supply both previously preserved ZIPs and their extracted top-level directories:

- `hase-type-completion-evidence-20261010-v3.zip`
  SHA-256 `f44195e0f2bf4d41efda7bd22eab6c61afecb100779e6e6d16cac82b3e329f60`
- `hase-source-continuation-20261010.zip`
  SHA-256 `20f498636b5ed387a703c24d7fad94b1ff51bb201df88dedcb039793ee37a76b`

This archive plus those two extractions contains every project source and
source/receipt record required by this wrapper. The old P01/P03 frontend inspection
paths in the author's immutable INPUTS are external historical provenance, not
runtime inputs; REUSE_CONTRACT explicitly identifies those two exclusions. The
Mathlib Nat.find inspection is mapped to the supplied pinned package directory.
Toolchain, external package source/build libraries, and checked project objects
are external runtime dependencies, not supplied by extracting the archives.

## Efficient verified-object replay

Requirements: Python 3.9+, Git, the exact Linux x86_64 Lean 4.19.0 binary and its
standard libraries, pinned external package checkouts/build libraries, and the
94 retained checked objects identified by author INPUTS.json. Pass their locations
explicitly; no original absolute workspace path is required.

- `--prerequisite-objects`: tree containing 92 exact baseline/model objects under
  module-relative paths. This was `hase-full-per-review-20261010/fresh-lib` here.
- `--closed-objects`: tree containing the exact author
  `ClosedProofCanonicalisation.olean` and `ClosedScalarInstances.olean` bound in
  INPUTS. This was `hase-closed-scalar-instances-20261010/validation` here.
- `--packages`: pinned `.lake/packages` directory, with package `.lake/build/lib/lean`
  trees. Exact Git revisions are in v3's EXTERNAL_PACKAGE_MANIFEST.json.
- `--lean`: executable path in the retained Lean distribution.

Example (substitute your own paths):

```sh
python3 replay_extractor.py \
  --v3 /evidence/hase-type-completion-evidence-20261010-v3 \
  --v3-archive /evidence/hase-type-completion-evidence-20261010-v3.zip \
  --continuation /evidence/hase-source-continuation-20261010 \
  --continuation-archive /evidence/hase-source-continuation-20261010.zip \
  --lean /toolchains/lean-4.19.0-linux/bin/lean \
  --packages /retained/.lake/packages \
  --prerequisite-objects /retained/checked-baseline-objects \
  --closed-objects /retained/checked-author-closed-objects \
  --out /replays/new-absent-output-directory
```

Use `--verify-only` and omit `--out` for prerequisite verification alone. The wrapper
checks both exact predecessor ZIP hashes and every extracted archive entry,
all bundled indexed bytes, frozen author/reviewer source manifests (with explicit
historical-object omissions), source/receipt bindings, compiler hash/version,
package revision pins, and all 94 recorded object digests. It rechecks these after
replay. The inherited 83-module closure is not rebuilt.

The wrapper copies byte-identical addition sources into new output directories,
compiles 10 author modules and 5 reviewer controls/audits with `--trust=0`, re-exports
the actual source AST, runs 15 Python adversarial tests, regenerates ten concrete
certificates byte-for-byte, and regenerates/checks 266 reviewer cross-language
examples (532 Lean equations). It also reruns two intentionally false Lean files
and requires nonzero exits. Their error-recovery `sorryAx` output is rejected
command evidence, never an accepted theorem or imported object.

All replay output is separate from frozen inputs. The original author/reviewer
scripts and their historical workspace paths are preserved unmodified as evidence;
use this top-level wrapper for portable explicit-path replay.

## What a fresh machine does and does not have

Extracting these three source archives alone is **not** a standalone executable
build. A fresh machine must obtain the exact compiler and pinned package libraries,
and either transfer the retained 94 exact checked objects or build the prerequisite
closure once from the preserved source with trust-zero checks and a new receipt.
This wrapper implements only the first, exact-recorded-object reuse path.

A relocated fresh source compilation may produce different `.olean` bytes because
Lean records build-location information. It must not be accepted by silently
replacing recorded hashes or calling the result a verified reuse. A fresh-build
route needs its own explicit dependency rebinding and verified trust-zero receipt;
that bootstrap/rebinding workflow is not implemented or certified here. Prior
archive scripts/receipts supply the source/build history, not a guarantee that
all historical scratch scripts run unchanged on a new machine.

The preservation receipt establishes fresh extraction and executable addition
replay against retained checked objects in this environment. It does not claim a
recipient already has those objects, that all external libraries were rebuilt,
or that the compiler was bootstrap-verified.

## Resource and preservation limits

The mathematical Lean extractor is total on its supplied closed HasE domain.
The Python diagnostic is resource-bounded: fuel, nodes, steps, memory and host
recursion exhaustion are inconclusive. In particular numeral 6 exceeds the
200,000-node allowance, then succeeds with 5,000,000 nodes; zero development
rounds and an eight-round Omega run are retained refusals. A finite successful
non-iteration rejection is a separate kernel-checked partial domain result.

The full frozen author manifest (41 bound files plus manifest) and all reviewer
source/log/receipt files are preserved. Twelve historical reviewer `.olean`
snapshots, totaling about 10 MB, are omitted explicitly in REUSE_CONTRACT. Their
original hashes remain in the unmodified reviewer manifest and receipt, but the
archive does not claim to include or reverify those absent object bytes. They are
never runtime prerequisites. New reviewer objects are freshly compiled instead.
No predecessor archive or receipt is changed. No upload is performed.
