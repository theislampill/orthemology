# Hidden-change official-cache setup

The missing acquisition step for the hidden-change Lean lane has now been qualified independently. A fresh isolated run reproduced all **6,646 exact dependency object names, byte counts and SHA-256 values** in the unchanged consumer base: 6,641 official cached outputs and five freshly compiled Cache tooling modules. A fresh `import Mathlib` smoke then passed through the generated explicit environment.

The sole acquisition completed in **719.121 seconds**, within a 30-minute limit. All nine official source revisions, 7,507 tracked source hashes and six previously qualified toolchain files were checked. The original scientific sources, runner and inventory were not changed. `PUBLIC_SUMMARY.json` binds the result and its independent review.

## Scope and prerequisites

This is a source-only recipe, with no dependency objects, archives, compiler, raw logs or machine-local environment bundled. It was qualified on the existing Linux x86-64 host, using clean local clones of the separately verified official source trees and the already verified official Lean 4.19.0 toolchain. It is not a new-host installation test, compiler bootstrap, dependency theorem cold build, or another full 125-source/64-control hidden-change replay. The qualification target is byte identity to the environment used by the earlier reviewed replay.

Provide:

- The unchanged consumer base whose `MANIFEST.json` SHA-256 is `9f2a0f116f90fc4189faacc79d5b7c02116e1d36735cc2cdffe4f9117406de95`.
- A directory containing the nine official Git checkouts named in `recipe/inputs/pins.json`. Their tracked contents must match the included source inventories. ProofWidgets must include tag `v0.0.57` at the pinned commit. The official-URL preparation command supplied in sibling `hase-source-build/tools/prepare.py` can prepare these source trees, as shown below; this recipe does not substitute historical proof objects for missing sources.
- The official Lean 4.19.0 Linux x86-64 toolchain matching `recipe/inputs/toolchain-files.json`.
- Python 3.11 or later, Bash, Git and curl at the system locations used by the recipe, HTTPS access to the official services, and at least 10 GiB free before acquisition. Existing compiler/native-runtime and host tools remain trusted.

## Run

The source trees do not require access to the earlier workspace. If you do not already have the exact official source checkouts, run only the sibling's official-URL preparation step, with no source seed. It was separately qualified to retrieve and verify these nine repositories without producing proof objects. Its preparation tool also checks available Node/npm versions, but this step does not build widgets or acquire npm packages. Read that sibling's prerequisites; for its bounded adapter, source-work and toolchain paths must not contain whitespace or `:`.

Run from this supplement directory, replacing the placeholders with absolute local paths. Both work directories must be absent and outside the consumer base and toolchain:

```sh
TOOLCHAIN="/your/path/to/lean-4.19.0-linux"
SOURCE_WORK="/your/path/to/absent-official-source-work"
python3 -E -S -B ../hase-source-build/tools/prepare.py --work "$SOURCE_WORK" --toolchain "$TOOLCHAIN"
SOURCES="$SOURCE_WORK/dependencies"
```

Stop if preparation fails. Do not run the sibling's later widget, source-build or derived-package stages for this hidden-change cache recipe. Our recorded cache qualification clean-cloned the source trees produced by that separately qualified official acquisition; it did not combine the two runs into a new all-online/new-host qualification.

Then set the unchanged consumer base and another absent work directory. Keep `SOURCES` and `TOOLCHAIN` from the successful preparation (or point `SOURCES` at independently obtained, exact official checkouts):

```sh
BASE="/your/path/to/consumer-base"
WORK="/your/path/to/absent-cache-work"

python3 -E -S -B recipe/provision.py prepare --base "$BASE" --sources "$SOURCES" --toolchain "$TOOLCHAIN" --work "$WORK"
python3 -E -S -B recipe/provision.py acquire --base "$BASE" --sources "$SOURCES" --toolchain "$TOOLCHAIN" --work "$WORK"
python3 -E -S -B recipe/provision.py verify --base "$BASE" --sources "$SOURCES" --toolchain "$TOOLCHAIN" --work "$WORK"
```

Run each next line only if the preceding stage exits successfully. `prepare` clones source-only Git checkouts and builds only the five-module upstream Cache client. Its five exact object identities must pass before `acquire` downloads anything. `acquire` obtains and checks the pinned official leantar helper, then invokes `lake exe cache get Mathlib` once. The unchanged upstream client obtains the exact-tag ProofWidgets release prerequisite and the official Mathlib cache. Only its built-in download retries are allowed; helper acquisition and the cache command share one 30-minute clock.

`verify` requires the original exact object set, clean source pins, toolchain identities and no partial archive before compiling a small fresh smoke. A passing local `evidence/QUALIFIED.json` identifies the result; `environment.json` and `build_env.sh` then point explicitly to the new dependency environment. The configuration supplies the hidden-change lane only. It does not replace the separately qualified HasE dependency environment.

For a later, separately chosen full hidden-change replay, the unchanged base runner accepts the generated configuration:

```sh
python3 -E -S -B "$BASE/replay.py" lean-hidden --environment "$WORK/environment.json" --output "path/to/absent-proof-output"
```

That full replay was not repeated for this acquisition qualification.

## Failure and custody

Stop on any permission denial, source/tag/toolchain change, mismatch, unresolved official download or timeout. Keep partial outputs and logs. Do not relax the original pins, reuse old cached objects, switch mirrors, fall back to a broad source build, or repeat the cache invocation. The recipe refuses an existing preparation destination and an already-started acquisition without modifying their retained receipts; the included small regression checks cover those refusal cases.

Successful acquisition at the recorded time is not a promise of future service availability. The immutable base retains its original prepared-environment statements; this separately reviewed supplement records the subsequently qualified acquisition route without rewriting that historical record.
