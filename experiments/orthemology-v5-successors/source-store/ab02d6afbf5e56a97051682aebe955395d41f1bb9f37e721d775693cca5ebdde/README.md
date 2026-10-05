# Syntactic substitution admissibility

Start with `CHECKED_SCOPE.md`. Both targets are independently accepted. `FINAL_DISPOSITION.json` binds the accepted result; `CANDIDATE_v1.json` preserves the frozen pre-review candidate record.

## Files

- `sources/SubstitutionSyntax.lean`: literal two-sort substitution algebra.
- `sources/SubstitutionAdmissibility.lean`: both universal Has transformations, finite support and composition.
- `sources/SubstitutionControls.lean`: discriminating capture/J/opaque-atom controls and concrete proof reuse.
- `sources/AdmissibilityContract.lean`: exact target signatures.
- `sources/SubstitutionReadback.lean`: original-definition, theorem and axiom readbacks.
- `review/`: exact independent report, identities, compiler outputs and additional controls.
- `INPUT_SOURCE_MANIFEST.json`: accepted import hashes and original source-map members.
- `ENVIRONMENT_AND_DESIGN_INPUTS.json`: exact toolchain and admitted-design identities.
- `logs/commands.tsv`: every compilation's phase, module, source hash, UTC start/end and full exit code. Matching `.log` files retain complete compiler output.
- `BASELINE_CONTRACT.lean.txt`: expected-rejected original-only target check.

## Reproduce

From this package directory:

```sh
python3 scripts/verify-inputs.py
TOOLCHAIN_ENV=/path/to/restored/environment.sh bash scripts/verify.sh
```

Set `TOOLCHAIN_ENV` to the already trusted restored environment script; it performs no download, installation or bootstrap. It compiles only the actual import closure and the five extension/check modules and independent controls, with one worker and a 180-second per-module timeout. It leaves default heartbeat and recursion limits intact. The exact module command is:

```sh
timeout 180 "$LEAN_ROOT/bin/lean" -j1 -o "$module.olean" "$module.lean"
```

`LEAN_PATH` prepends this package's `sources` directory to the trusted environment's existing Mathlib/dependency paths. `scripts/check-module.sh` records fresh invocations and exits under `reproduction-logs/`, leaving all historical logs unchanged. The full dependency order is `dependency-order.txt`.

This public projection includes all exact accepted dependency sources, so no preparation-layout access is required. `TOOLCHAIN_ENV` is mandatory and must name a readable, already trusted environment script exporting `LEAN_ROOT` and `LEAN_PATH` for the pinned Lean/Mathlib installation. Neither helper discovers, downloads nor installs a toolchain.

Paths retained inside custody manifests, original design/toolchain identities, review records and historical compiler records identify where the original evidence was obtained. They are historical provenance only, not paths that reproduction follows. The public verification route uses only files in this package plus the explicitly supplied trusted environment. Preparation-only reconstruction and packaging helpers are omitted; `PUBLIC_PROJECTION.json` and `PROJECTION_DIFFS.patch` bind the exact omissions and executable/documentation changes.

The original-only contract's expected exit is 1, specifically for the two unknown theorem names. All final proof/check modules and all actual dependency modules have exit 0. Reproduction logs use a separate `reproduction-logs/` directory and the `reproduction` phase; they do not modify the historical development diagnostics.

The preserved `PACKAGE_VERIFICATION.json` records the predecessor helpers and is historical. `PORTABILITY_VERIFICATION.json` records the new public-helper tests. This package does not provide a hermetic Lean/Mathlib bootstrap; the explicitly supplied external trusted environment remains required.
