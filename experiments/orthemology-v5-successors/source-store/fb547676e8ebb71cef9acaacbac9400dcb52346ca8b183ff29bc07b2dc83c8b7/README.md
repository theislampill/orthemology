# HasE dependency source-build supplement

This separate recipe provisions HasE dependencies from their exact official
source pins and replays the unchanged HasE evidence. It accompanies the sibling
`code-evidence/` package. The original exact-cache route remains unchanged.

The locally qualified route rebuilt 1,369 third-party objects, then checked the
84 unchanged HasE modules, eight selected controls, nine axiom readbacks and the
ordinary diagnostic's seven normalizer self-tests. See
`results/QUALIFICATION_SUMMARY.json` for the actual qualified execution and its
scope, and `results/DEPENDENCY_SOURCE_OBJECTS.json` for the path-free custody
projection. Do not infer completion of the eighteenth tranche or a stronger
mathematical claim from this provisioning result.

## What is and is not provided

The required dependency objects need not reproduce historical cache bytes. This
recipe creates a separate `SOURCE_BUILD_…` copy of the supplied consumer package
and changes only its HasE dependency inventory and outer manifest. Scientific
Lean/Python sources, official pins, controls, diagnostics and replay runner stay
byte-identical. Only this separately derived HasE lane is source-build qualified.

No dependency/compiler binaries, npm downloads, source Git checkouts or prior
custom proof objects are distributed here. The qualified execution used clean
local clones of already verified official checkouts and cached npm registry
downloads. A separate seed-free
preparation run also fetched all nine official repositories at the pinned commits
and verified all 7,507 files on this existing host, with zero proof objects or
node_modules. This is phase-specific acquisition evidence, not a clean-OS or
toolchain installation test or one uninterrupted all-online recipe run. See
`results/PREREQUISITE_ACQUISITION.json`. Source/registry availability remains a
prerequisite. A separate empty-cache online npm/widget attempt was interrupted
before a verified terminal result. It is unqualified and does not establish
registry unavailability. Online npm provisioning is not claimed to have succeeded.

This is not a full-Mathlib rebuild, a compiler bootstrap, native/FFI verification,
or a claim of byte-reproducible external objects. Official Lean/compiler,
standard-library and runtime components and npm registry JavaScript tools remain
trusted. The ordinary diagnostic is a finite calculation on exported exact
syntax, not a Lean theorem of beta-eta separation or compiler-image membership.

## Prerequisites

- Linux x86-64, Python 3, Git, Node and npm. The qualified run used Python 3.12.14,
  Node 24.19.0 and npm 11.9.0. Other versions/platforms remain unqualified.
- Official Lean 4.19.0 Linux toolchain:
  https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst
  Archive SHA-256:
  `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.
  Preparation checks the six executable/shared-library digests in the retained
  public toolchain identity map. Compiler and standard-library objects are trusted.
- The exact sibling `code-evidence/` package. Its manifest SHA-256 must be
  `9f2a0f116f90fc4189faacc79d5b7c02116e1d36735cc2cdffe4f9117406de95`.
  `FINAL_BASE_BINDING.json` records the exact metadata-only compatibility bridge.
  No arbitrary manifest or user-provided object inventory is accepted.
- An absent work directory and room for source/build outputs. The earlier
  retained dependency tree used about 1.4 GiB, npm cache about 70 MiB and official
  toolchain about 1.6 GiB. These are observed sizes, not peak-space guarantees.

For this bounded upstream-log adapter, the work and toolchain paths must not
contain whitespace or `:`. This does not alter the portable runner's separate
Unicode/spaces qualification. A run on the qualification host takes roughly
half an hour after prerequisites; slower hosts or acquisition delays may take
longer or fail.

## Recipe

Set these shell variables to absolute paths:

- `ROUTE`: this `hase-source-build/` directory
- `ORIGINAL`: sibling `code-evidence/`
- `TOOLCHAIN`: extracted official `lean-4.19.0-linux/`
- `WORK`: an absent work directory outside the supplied packages
- `DERIVED`: an absent directory outside the supplied packages, whose name starts
  with `SOURCE_BUILD_`

Run the commands below in order. Stop on any nonzero exit. Do not use Python
optimisation (`-O` or `-OO`); assertions are verification gates.

1. `python3 -E -S -B "$ROUTE/tools/prepare.py" --work "$WORK" --toolchain "$TOOLCHAIN"`
2. `python3 -E -S -B "$ROUTE/tools/source_closure.py" --work "$WORK"`
3. `python3 -E -S -B "$ROUTE/tools/run_build.py" --work "$WORK" widget`
4. `python3 -E -S -B "$ROUTE/tools/verify_widget.py" --work "$WORK"`
5. `python3 -E -S -B "$ROUTE/tools/run_build.py" --work "$WORK" dependencies`
6. `python3 -E -S -B "$ROUTE/tools/verify_cold_build.py" --work "$WORK"`
7. `python3 -E -S -B "$ROUTE/tools/derive_final_package.py" --work "$WORK" --original-package "$ORIGINAL" --derived-package "$DERIVED"`
8. `python3 -E -S -B "$DERIVED/replay.py" lean-hase --environment "$WORK/hase-environment.json" --output "$WORK/hase-replay"`
9. `python3 -E -S -B "$ROUTE/tools/final_verify.py" --work "$WORK"`

Step 1 optionally accepts `--source-seed /path/to/verified/checkouts` and
`--npm-cache-seed /path/to/registry/cache`. The qualified execution used both.
Without a source seed, Git clones the nine official URLs at the exact revisions
in `inputs/lean/lake-manifest.json`. All 7,507 tracked-file hashes are checked.
Local source seeds are clean-cloned; inherited proof objects and node_modules
are never copied. An npm seed copies only `_cacache` into a new writable cache
and forces npm offline. Without it, npm uses the registry.

The build uses unchanged upstream ProofWidgets `widgetJsAll`, its pinned npm
lockfile and corrected full package override. It then builds the known five-root
superset with two threads, proof-cache downloading disabled and isolated Lean
paths. The verifier requires one successful logged compiler command for each of
1,369 outputs and checks the log against its originating execution receipt.
Only the known generated ProofWidgets package-lock hash/trace metadata may be
restored after its generated bytes have been retained. Lean sources and actual
lockfile content must stay pinned.

Step 9 writes `FINAL_SOURCE_BUILD_QUALIFICATION.json` under the new work tree's
`evidence/` directory only after source/object/log and replay checks pass. Each
build attempt refuses to overwrite existing build logs or receipts. Failed or
interrupted attempts are not mathematical negative evidence.

## Reading the receipts

The original consumer package and unchanged runner retain their static
cache-oriented wording and `cold_dependency_build: false` field. The separate
source-build and derivation receipts identify the actual dependency custody for
this HasE run. Do not reinterpret other lanes as source-built.

The public object inventory is explicitly a selected-field projection, not raw
commands. It preserves relative source/object identity and every recorded compiler
`-D` option, omitting absolute commands, search paths and local timestamps. Its
exact raw inventory/build-log hashes bind it to the unchanged qualification
records. Full local raw execution logs and private review records are not
included. Running this recipe generates and verifies complete fresh logs for the
reader's own environment.

One unused historical acquisition receipt is omitted from the public inputs;
the public input manifest is the corresponding exact subset. All effective
source/compiler pin files and runnable verification code are unchanged.
`PUBLIC_MANIFEST.json` identifies the exact distributed supplement files.
