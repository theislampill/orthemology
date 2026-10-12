# T20 type-completion evidence, preserved 10 October 2026

This additive archive preserves two independently reviewed packages byte for byte.
The literal original judgement **`HasE [] c3 (W q)` remains OPEN**.

## Exact result and boundary

- In the finite open SKI-term reduct (with inert zero/one markers), membership in
  the Church interpretation over **all conversion-saturated PERs** is equivalent
  to one uniform finite iteration count: `Church n ↔ UniformIter n`.
- The imported, pinned **actual original compiler**, not only a formula mirror,
  is related to the original identity endpoint at the extensional PER `N → N`.
- The source-to-open-term embedding is injective and preserves and reflects raw
  conversion. The original endpoints remain raw-nonconvertible. Typed PER
  agreement does not assert raw conversion of the compiler to identity.
- This does **not** establish soundness of all HasE rules for that full-PER
  interpretation, a derivation or nonderivability of the literal target, or a
  mathematical novelty claim. Any whole-model exclusion retains the hypotheses
  specified in the two reviewed reports, including the identity convention.

## Contents and provenance

The two original `RESULT.md` reports and independent reviews give the complete
scope. Only their manifest-listed files plus their manifests are included:

- `hase-open-term-standardness-20261010/`: 30 listed files, three Init-only proof
  modules, source bindings, and independent review.
- `hase-imported-compiler-transport-20261010/`: 113 listed files, the imported
  bridge, all 83 original project modules, pin evidence, and independent review.

The original repository pin is
`theislampill/orthemology@7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`.
The isolated manifest SHA-256 is
`887852b8eecc09e105306403c31a91beed5e9190e9dabc1cd9a8c7113f27ac86`.
The imported manifest SHA-256 is
`53c1303c989753f5c290ce587cc986424a75d53723795a4471c90468af023e38`.

No build outputs, replay working directories, library overlays, or symlinks are
archived. Earlier archives and both original evidence directories are unchanged.
`ARCHIVE_CONTENTS.json` hashes every delivered file except itself. A separate
archive receipt binds that index, the final ZIP digest, and the final-extraction
replay. The additive `preservation/` receipts document this archive's replay;
they do not replace or edit the retained author or independent-review receipts.

## Verify and replay without altering reviewed evidence

Run `python verify.py` in the extracted archive root. It reads only explicit
manifest/index paths. To replay, use the additive wrapper rather than the retained
historical replay scripts, which originally wrote into their own validation trees.

Requirements are Python 3.9 or later, Git, the retained Lean 4.19.0 release
(commit `6caaee842e94`), and the already-built external packages pinned in
`EXTERNAL_PACKAGE_MANIFEST.json`. Mathlib is pinned to
`c44e0c8ee63ca166450922a373c7409c5d26b00b`.
These external toolchains and dependency objects are not bundled or installed.
The dependency object root must provide the two Mathlib modules listed in
`EXTERNAL_BUILD_PLAN.json`; all paths are supplied explicitly:

```sh
python replay_archive.py \
  --lean /path/to/lean-4.19.0-linux/bin/lean \
  --packages /path/to/pinned/.lake/packages \
  --dependency-objects /path/to/existing/mathlib-object-overlay \
  --out /path/to/new-output-directory
```

The default replay rebuilds the three isolated modules, their reviewer checks,
all 83 extracted original project sources, the four imported proof modules, and
their reviewer checks: 92 compilations. All nine proof/reviewer compilations use
`--trust=0`. Existing pinned external Mathlib/package objects are reused read-only;
the two prerequisite Mathlib objects are not freshly rebuilt by this wrapper.
No dependency/build overlay is recursively traversed or copied.

For a shorter artifact replay, add `--project-objects /path/to/already-built-83`.
The receipt then explicitly records reuse of those 83 objects and hashes each;
only the nine proof/reviewer compilations are performed anew. This is distinct
from the original retained author and independent clean builds, which each
rebuilt all 83 original modules plus the two external Mathlib prerequisites.

During preservation, a fresh extraction received the default 92-compilation
replay. The final archive received another fresh extraction, complete hash
verification, and the shorter nine-compilation replay using those newly built
83-module outputs. No new whole-HasE or literal-target claim follows from either.
