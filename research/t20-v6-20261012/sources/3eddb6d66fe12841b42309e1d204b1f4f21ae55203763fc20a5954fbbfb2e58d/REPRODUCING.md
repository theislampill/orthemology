# Full public replay

Requirements: Python 3, official Linux x86_64 Lean 4.19.0, and the exact pinned
Mathlib checkout with its official compiled cache and dependencies. Paths are
provided explicitly; no `/workspace` path or original working tree is required.
The runner does not download, install, update or modify any dependency.

Pinned inputs are in `DEPENDENCIES.json`; `dependencies/mathlib-lake-manifest.json`
pins each dependency revision. `dependencies/SOURCE_MANIFEST.json` binds all
6,816 Mathlib archive files plus 690 installed dependency source files. The
runner verifies all 7,506 before proof replay. It trusts existing compiled
Mathlib/dependency libraries, matching the independent review; it does not
claim to rebuild all Mathlib. No custom compiled object is reused.

Obtain official Lean v4.19.0 from its release page and the specified Mathlib
revision from the links in DEPENDENCIES.json. Prepare that revision's dependencies
and official cache using its documented Lake workflow (`lake exe cache get`).
Do not run a dependency update or select a newer commit. The exact tested
Linux binary hash is enforced; other platform builds are not attested here.

First verify the extracted packet:

    python3 replay.py --verify-only

Then run the complete entrypoint, supplying local dependency paths and a NEW
output directory outside the extracted packet:

    python3 replay.py --lean /path/to/lean-4.19.0/bin/lean \
      --mathlib /path/to/mathlib-c44e0c8 \
      --output /path/to/new-attribution-replay

The output directory must not exist. The runner verifies immutable bindings,
compiles into a fresh build directory, checks every successful log for errors,
warnings and sorryAx, validates the standard axiom set, and requires exact
classes of error diagnostics for the three invalid mutants. A final
`REPLAY_RECEIPT.json` records source hashes, all stages and outcomes.

Expected successful stages: three legacy modules, six central modules,
TargetA/B/C, Regression, RootCosts, FamilyDeletionControls, IndependentChecks,
DeletionControls and AxiomAudit (18 total). Three additional stages must be
rejected: label-as-root substitution, removal of c positivity and removal of B
positivity. Their failure logs can contain sorryAx because compilation failed;
those files are never imported into a successful build.

Historical `sources/*/verify.sh`, `lean.sh`, `test-controls.sh`, and `review/*`
scripts are preserved unchanged for audit. They reflect their original layout.
Use public `replay.py`, which additively resolves that layout and includes
Regression and the entire controls supplement. None of the accepted scientific
statements or original helpers is patched during replay.
