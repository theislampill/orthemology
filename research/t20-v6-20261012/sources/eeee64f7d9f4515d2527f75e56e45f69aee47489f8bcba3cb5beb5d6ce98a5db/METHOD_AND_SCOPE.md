# Method and scope

1. Verify the recovered core archive identity: SHA-256 40c77652d3938e95f832023f32f018e1e394ffbd57adcc7d918d07d578e8a3a2, 376 files. Independently copy the nine source checkouts at the exact revisions in its lake-manifest.json. Verify their Git trees and 7,507 tracked files. Begin without dependency-library or project proof objects.

2. Use the official Lean 4.19.0 compiler. Bind its executable, Lake and shared libraries to the official release archive. Recursively parse imports using --src-deps; independently scan all distributed mathematical and control sources. This yields exactly five external root imports and 1,369 required third-party modules, matching every packaged source hash. Official toolchain imports are inventoried separately and remain trusted.

3. Rebuild the upstream ProofWidgets JavaScript assets with its unchanged Lake target and pinned npm lockfile. Force the authoritative Batteries source pin through package overrides. JavaScript build tools are registry distributions, not source-bootstrapped infrastructure. All 19 generated assets are hash-recorded; the three embedded inputs needed by the proof closure are present.

4. Build from the isolated Lake driver with cache downloading disabled, empty initial LEAN_PATH, and the original package-specific compiler options. The exact source-build command is:

lake --no-cache --rehash --verbose build +Mathlib.Algebra.BigOperators.Fin +Mathlib.Algebra.MvPolynomial.Funext +Mathlib.Algebra.Order.BigOperators.Group.Finset +Mathlib.Computability.PartrecCode +Mathlib.Data.Bool.Basic

The environment sets LAKE_NO_CACHE=1 and MATHLIB_NO_CACHE_ON_UPDATE=1. Lake runs with two threads. The verbose log binds one fresh official compiler invocation to each expected output and records every effective import path. No unexpected library proof outputs were accepted. Generated widget hash metadata was recorded, then restored to pinned bytes before replay; no Lean source or actual package-lock content changed.

5. Run the archive's unchanged replay.py with --lean selecting the official binary, --dependencies selecting only the new dependency tree, and --output selecting an absent directory. Its own project/control compiler invocations use one thread and lane-isolated fresh output paths. The complete replay compiled 111 mathematical modules plus inherited audit support and passed 220 designated controls, four additional integration controls, two aggregate audit/inventory invocations, and 22 Python reference tests.

6. Recheck all dependency source/object identities, both source trees, all archive entries, and trusted toolchain inputs after replay. Compare against the prior prepared-cache replay: 14 dependency object bytes differ, but all resulting project inventories are byte-identical and all 226 control/audit contracts match. The specific byte-difference cause is not established.

7. Preserve original receipts verbatim. The immutable replay's cache-oriented strings are static; the detached receipts bind its actual dependency hashes to the fresh source build. The exact historical execution-helper hashes are retained in the version inventory. Source, output, command, option and result evidence is unchanged.

Scope: the entire actual required third-party Lean closure for core111 was rebuilt. This is not a full-Mathlib rebuild or a compiler bootstrap. Official Lean/Init/Lean/Std/Lake, the operating system/runtime, and registry JavaScript build tools remain trusted. Native compiler/FFI correctness and broader mathematical claims are not asserted. Signed116 retains its separately reported dependency-cache scope.
