# T20 Hessian Continuation Research Checkpoint

9 October 2026. **Intermediate research checkpoint; T20 remains active.**

Start with [the integrated result](../abf6c6fede6b7f9e08ba3d469a9b0a0f97ec5b9d2ad12197d6383f226e912a94/combined-result.md), then [the final independent review](../25740e5fc024188a058bd68b043cdde26e0bbf2795816ce324fa87db628151ec/REVIEW.md). This additive packet preserves the scalar-closure classification, clock-dependent binary-log predictive-memory theorem, quadratic sum-plus-minimum guard repair, and binary-log forward flow/Bregman projection result at their stated assumptions. It retains corrected and original reports, source bytes, exact controls, reviews and provenance. It does not replace any earlier checkpoint.

## Reading order

1. [Integrated mathematical result](../abf6c6fede6b7f9e08ba3d469a9b0a0f97ec5b9d2ad12197d6383f226e912a94/combined-result.md)
2. [Scalar continuation iff](../5ce54702491ebc4568841d8e198b0db2cd0fcc9f5b14b785e7be8a5a656a1624/scalar-projectability.md)
3. [Binary-log memory proof](../e82a8b652f32e79de65c7423eefa6dd0c1e96493818aeb0fefc0f8d4760b7d51/binary-log-memory.md)
4. [Dual flow, clock and boundary proofs](../679e3049b498c19a0d9982ef30dc7a34483871dfdf21178dad1b45004485bb58/dual-flow-and-boundary.md)
5. [Source-linked noetic interface and residual](../4ab67c31065de47787a47b1864b941cc8dd824478a62285f651a28016b776be8/noetic-interface.md)
6. [Frozen review receipt](../../PUBLIC_BOUNDARIES.md#recovered-reference-113) and [root control replay](../../PUBLIC_BOUNDARIES.md#recovered-reference-114)
7. [External source-access ledger](../d0d1089f41194f9c0dbe10a8b7e552d0cee6c924cff8909a775853e057364445/SOURCE_ACCESS_LEDGER.md)
8. [Owner continuity update](../f5c7c94f2538aa3ddf79e4457b7b47850ebf47f37ef092c14ffa8f3f71bd087d/Orthemology_Dot_T20_Research_Continuity_Update_20261009.md) and [inherited master handoff](../93e812271e78a4f6bba594dd942571fed418b77a12b40c75f704dd056329e819/Orthemology_Master_Handoff_20261009.md)

The master handoff predates parts of this result and includes historical paths into its larger original handoff. Those references remain historical pointers, not a declaration that every earlier archive or guide is embedded here. The accompanying continuity update controls the inherited research-priority correction. A new, separately active general-admissibility investigation is excluded from this freeze.

## Exact integrity replay

From the extracted directory containing this file, run:

```sh
python3 -B replay/verify_portable.py --output ../hessian-integrity-receipt
```

The receipt directory must not already exist and must be outside the extracted package. Python 3.8+ and its standard library are sufficient. The verifier checks exact file/directory inventory, all payload sizes and SHA-256 hashes, checksum coverage, strict JSON parsing, path safety and 67 declared source/review bindings. It rejects changed, missing or extra files, extra empty directories, symlinks, duplicate paths and unsafe paths. It creates no success receipt on failure and does not alter the package.

To check the ZIP against these extracted bytes as well:

```sh
python3 -B replay/verify_portable.py --output ../hessian-archive-receipt --archive ../T20_Hessian_Continuation_Research_Checkpoint_20261009.zip
```

Add `--archive-sha256 HASH_FROM_THE_SEPARATE_GUIDE` to bind the ZIP to an independently obtained expected identity. The verifier rejects duplicate ZIP names, traversal, absolute and backslash paths, symlinks/special entries, unexpected roots, extra members and ZIP/payload mismatches. A 256 MiB uncompressed safety bound applies to this small packet. The delivered ZIP contains regular file entries only.

The manifest and verifier are inside the archive; an attacker who replaces the entire archive can replace both. Therefore use the separately delivered archive SHA-256 as the trust anchor. Integrity is not proof, source authentication or peer certification.

## Exact bounded research replay

The tested environment was Python 3.12.14, SymPy 1.14.0 and mpmath 1.3.0. Only the memory and independent symbolic controls require SymPy. No dependency binaries, Lean toolchain or Mathlib closure are bundled. For a clean environment, install the two pinned packages from `replay/requirements-replay.txt` using your normal trusted package process. No installation or network access occurs during integrity verification.

The original controls write result files next to themselves. Preserve this sealed directory by running byte-identical copies in a new sibling directory. From the package root, these are the exact POSIX-shell commands:

```sh
mkdir ../hessian-controls-replay
cp hessian-frontier-recovery-20261009/scalar_closure_controls.py ../hessian-controls-replay/
cp hessian-flow-memory-boundary-20261009/check_controls.py ../hessian-controls-replay/
cp hessian-flow-continuation-20261009/check_dual_controls.py ../hessian-controls-replay/
cp hessian-continuation-independent-review-20261009/independent_controls.py ../hessian-controls-replay/
python3 -B ../hessian-controls-replay/scalar_closure_controls.py > ../hessian-controls-replay/scalar.stdout.json
python3 -B ../hessian-controls-replay/check_controls.py > ../hessian-controls-replay/memory.stdout.json
python3 -B ../hessian-controls-replay/check_dual_controls.py > ../hessian-controls-replay/dual.stdout.json
python3 -B ../hessian-controls-replay/independent_controls.py > ../hessian-controls-replay/independent.stdout.json
```

Expected: all exit codes zero and status PASS; scalar finite algebra controls, 66 memory assertion groups, 46 dual-flow assertions and 29 independent controls. These are distinct suites, not a count of general theorems. Compare the JSON objects with the corresponding preserved component result files. The packaging replay did so exactly; see [fresh control replay receipt](../../PUBLIC_BOUNDARIES.md#recovered-reference-115). Different SymPy versions may change printed expressions, so use the pinned version for exact output comparison.

Run the portable verifier's bounded positive/negative suite separately:

```sh
python3 -B replay/test_portable_verifier.py replay/verify_portable.py
```

It creates temporary fixtures outside the package and tests 20 conditions, including two valid inputs and 18 rejection/refusal cases. A missing-implementation red run and subsequent green run are retained. These are bounded implementation tests, not a general security proof.

## What the evidence does and does not establish

- New universal mathematical claims have written proofs and independent internal mathematical review. Small symbolic/rational controls are corroborating finite checks; they do not prove analytic ODE, arbitrary-dimension or topological assertions.
- The dimensional lower bound concerns continuous real-coordinate encoders on the specified open incoherent chamber, exact prediction and the declared clock. It is not a bit, finite-sample, robustness, runtime or physical memory lower bound.
- Inherited `.lean` sources and their historical receipt are preserved. **No Lean execution is performed or newly claimed here.** Their transitive build prerequisites are not included, and this packet is not a self-contained Lean build.
- Full local source files used by the new arguments are included, including the earlier continuation proof at its original sibling path. Source pins/hashes establish retained-byte identity, not current branch state, independent authorship or source authenticity.
- External classical papers/book chapters are cited but not distributed. The external-access ledger states exactly what was read, what could not be viewed, and what was inspected later. In particular, Hermann–Krener primary Section III was not fully read; selected third-party reproduced excerpts do not become primary-source review. Hatcher's specified invariance-of-domain statement is an external theorem dependency.
- The general source map and original source-status file are included only to keep inherited direct links meaningful. Their statuses remain historical and do not confer fresh checks on every indexed result.
- Source-defined DAEE controls remain distinct from a numerical ODE. No licensed-operation adapter, deployed/runtime integration, empirical cognitive validation, or new philosophical warrant follows from the archive or controls. Prior positive philosophical assessments remain inherited at their original defeasible warrant level.
- No repository write, merge, adoption, owner acceptance, final T20 closure, field-wide novelty or historical six-hour research-duration certification is claimed. Packaging and verification are not credited as new research time.

## Preservation and provenance

`PRESERVED_INPUTS.json` binds all 75 pre-existing inputs copied verbatim. `BINDINGS.json` additionally rechecks final-review, source-manifest, Git-blob and replay identities. Supplemental navigation sources were fetched read-only at the same pinned commits; their provenance is in `provenance/READONLY_SOURCE_ADDITIONS.json`. Nested source directories are preserved. One exact report copy supplies an unchanged review snapshot's relative link, documented in `provenance/NAVIGATION_COPIES.json`.

The prior 109 workspace ZIP files are inventoried separately from this new archive. They were preserved unchanged; the final external validation receipt binds the before/after comparison. Earlier archives are not re-embedded or resealed. The new packet is self-contained for its reports, scoped local source copies and bounded Python controls once the documented Python dependencies are available. It does not claim to contain all historical programme material or all transitive source/toolchain dependencies.
