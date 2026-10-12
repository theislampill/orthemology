# T20 cumulative evidence, v2 — 10 October 2026

**The original literal judgement `HasE [] c3 (W q)` remains OPEN.** This additive
archive preserves three independently reviewed results with separate scopes.
There is no mathematical novelty claim or new whole-HasE soundness claim.

## 1. Open-term full-PER standardness

In the finite open SKI-term reduct (with inert zero/one markers), Church membership
over **all conversion-saturated PERs** is equivalent to one uniform finite
iteration count: `Church n ↔ UniformIter n`. The isolated package supplies three
Init-only proof modules and its independent review. Fullness and fresh variables
are essential hypotheses; arbitrary Henkin universes are not covered.

## 2. Actual imported compiler and conservative raw conversion

The pinned **actual original compiler** and identity endpoint are related at the
ordinary extensional PER `N → N` in that open-term full-PER interpretation.
The source embedding is injective and preserves and reflects raw conversion.
The original endpoints remain raw-nonconvertible. This package includes all 83
original project sources, bridge proofs, pin evidence, and independent review.

This does not establish a fundamental theorem for all HasE rules in the newer
full-PER interpretation. Any whole-model conclusion retains the hypotheses in
the reviewed reports, including the specified identity convention.

## 3. Actual-context Raw-motive and reflection boundary

For the unchanged original endpoints p, q, type T = N → N, and B = Id_T(p,q):

- In the actual J context `theta [] T p`, coordinate 1 is the varying endpoint
  and **cannot** have type Raw, including indirect HasE derivations.
- Coordinate 0 is the identity-proof coordinate and **can** have type Raw by the
  actual proofErase rule. The context is formed and semantically inhabited.
- Therefore `Id_Raw(var 1,q)` is not formed as this J motive.
- Even in hypothetical context `[B]`, no proof polynomial derives `Id_Raw(p,q)`.
  Independent controls establish that this latter target is formed.

These results use **inherited all-rule F/G soundness**, not soundness of the new
full-PER interpretation. Semantic relatedness or assuming `[B]` does not produce
a closed HasE proof of B. This blocks one specific Raw-sensitive motive; it does
not validate all other motives or decide the original literal target.

## Frozen contents and preservation

Only manifest-listed files and each manifest are copied from the three packages:

- hase-open-term-standardness-20261010/: 30 payload files.
- hase-imported-compiler-transport-20261010/: 113 payload files.
- hase-raw-motive-boundary-20261010/: 20 payload files.

All preceding 143 payloads remain byte-identical. All three manifests are unchanged;
their expected SHA-256 digests are in verify.py. The RawMotive manifest SHA-256 is
`89fca9558ed54c9b2baa12f98903832f367cdc1e8b503a4c8b311706d5398725`.
The repository pin is
`theislampill/orthemology@7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`.

ARCHIVE_CONTENTS.json hashes every file except itself. The separate v2 receipt
binds the final ZIP, index, and extraction replay. No build objects, working
directories, symlinks, or dependency overlays are archived.

The previous v1 ZIP is unchanged (SHA-256
`344f49c9ccedd981913111cc3e073ce505d39de241a92482eba406386fcc73d7`).
Its exact receipt is retained as preservation/V1_ARCHIVE_RECEIPT.json.
The unchanged preservation/FRESH_EXTRACT_83_REPLAY.json and log document v1's
fresh 83-module rebuild plus nine proof/reviewer compilations. Original author
and independent receipts separately record their prior fresh 83+2 builds.

## Verify and replay the v2 addition

Run `python verify.py` in the extracted root to check all 163 frozen payloads,
three manifests, and every archive-indexed file without recursive traversal.
Then run the additive wrapper with explicit existing dependency paths:

```sh
python replay_raw_motive.py \
  --lean /path/to/lean-4.19.0-linux/bin/lean \
  --packages /path/to/pinned/.lake/packages \
  --dependency-objects /path/to/existing/mathlib-object-root \
  --project-objects /path/to/v1-preservation-built-83-module-output \
  --out /path/to/new-output-directory
```

Requirements are Python 3.9+, Git, Lean 4.19.0 (6caaee842e94), and existing external
packages listed in EXTERNAL_PACKAGE_MANIFEST.json; Mathlib is pinned to
c44e0c8ee63ca166450922a373c7409c5d26b00b. No installation is performed.
The dependency root supplies the two Mathlib prerequisite modules listed in
EXTERNAL_BUILD_PLAN.json, read-only.

The wrapper checks all 83 project-object hashes against the archived v1 fresh
build receipt and their source hashes against the extracted acquisition record.
It then compiles only RawMotiveBoundary.lean and IndependentBoundaryChecks.lean,
both with --trust=0, to a fresh external output directory. This v2 preservation
replay is **not another 83-module rebuild**. Dependency pins and the two
prerequisite-object hashes are checked.

replay_archive.py remains available for the two predecessor packages only, with
its explicit path arguments and optional --project-objects reuse mode. Historical
package scripts write into their own validation trees; use the additive wrappers
to keep reviewed evidence unchanged.
