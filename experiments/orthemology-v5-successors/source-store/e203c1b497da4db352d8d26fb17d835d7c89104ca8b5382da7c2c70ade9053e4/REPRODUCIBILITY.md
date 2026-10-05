# Public reproducibility and external prerequisites

## 1. Three separate checks

- **Public integrity:** `python3 verify_selection.py .` reads only this directory. It does not rerun research or validate sources.
- **Public Python model replay:** the commands below use the supplied model/fixture and standard library only. They do not retrieve or reinterpret primary sources.
- **Historical source and Lean evidence:** preserved receipts record earlier checks with their stated inputs and trusted environment. Repeating them has additional prerequisites. A missing prerequisite is not a passing or silently skipped stage.

Use a fresh disposable copy for all execution. Several unchanged scripts write beside themselves. Keep the selected public evidence pristine.

## 2. Occurrence supplied-model replay

From this public root, with Python 3.12 or later and a POSIX shell:

    PUBLIC=$(pwd)
    WORK=$(mktemp -d)
    cp -R "$PUBLIC" "$WORK/payload"
    cd "$WORK/payload"
    export PYTHONDONTWRITEBYTECODE=1
    CANDIDATE="$PWD/tranche10/research/occurrence-continuation/release-candidate-v1/checker"
    REVIEW="$PWD/tranche10/reviews/occurrence-checker"
    (cd "$CANDIDATE" && python3 -m unittest discover -s tests -v)
    (cd "$CANDIDATE" && python3 -O -m unittest discover -s tests -v)
    (cd "$CANDIDATE" && python3 exhaustive_validation.py)
    (cd "$CANDIDATE" && python3 source_and_release_validation.py)
    (cd "$CANDIDATE" && python3 semantic_mutations.py)
    python3 "$REVIEW/independent_models.py"
    python3 "$REVIEW/run_independent_review.py" --candidate "$CANDIDATE" --output "$WORK/independent-model-normal.json"
    python3 -O "$REVIEW/run_independent_review.py" --candidate "$CANDIDATE" --output "$WORK/independent-model-optimized.json"
    python3 "$REVIEW/run_independent_mutations.py" --candidate "$CANDIDATE" --directory "$WORK/mutation-copies"
    python3 tranche10/reviews/bounded-release-application/check_observations.py
    python3 -O tranche10/reviews/bounded-release-application/check_observations.py

These commands form an explicitly **model-only** replay. The unchanged `source_and_release_validation.py` uses `fixtures/source_roles.json`: its name does not turn supplied-annotation checks into a new primary-source inspection. The fixture, both sibling modules, all validation sources and tests are present. The independent review uses its local `independent_models.py`; it does not import omitted earlier programme code. Mutation results are written into the disposable review folder; no accepted source is edited.

The full historical `run_all_review.py` additionally invokes `run_source_fixture_review.py`. That stage requires two excluded original captures: Latin response SHA-256 `e5bc216a594116fa5e0c238012de9963990b07fafaea1cf40bfc0064366fdf67` and paired rendered record SHA-256 `6297d19569d8728d3bb14b49055303b4e2f9a45b4f9b1a1cf2704057a9a7b94f`. Its original default candidate path also names an excluded reviewer input copy. The full wrapper and original eight-group execution receipt are retained as historical evidence; **the public selection cannot replay the full wrapper**. Do not run it and call failure a source refutation, drop its missing groups, or substitute a new online fetch for those identities. The earlier complete execution receipt is distinct from a present public replay.

## 3. Lean source replay: external environment required

The uniform and nonuniform source packets and their readbacks are included, together with the separate accepted logs and reviewer controls. No `.olean` objects, toolchain executables, Mathlib source tree or dependency caches are bundled. There is no hermetic replay claim.

Required environment:

- Lean **4.19.0**; historical binary reports commit `6caaee842e94`.
- Mathlib source revision **c44e0c8ee63ca166450922a373c7409c5d26b00b**, with the dependency revisions in `dependencies/mathlib-lake-manifest.json` and compatible compiled dependency outputs.
- POSIX Bash, `timeout`, `sha256sum`, Python 3, and a configured Lean environment.
- Set `LEAN_ROOT` to the Lean distribution, `MATHLIB_ROOT` to the installed Mathlib checkout, add `$LEAN_ROOT/bin` to `PATH`, and set `LEAN_PATH` to Mathlib's `.lake/build/lib/lean` plus the corresponding paths for its pinned dependency packages. The packet script prepends its own `src` directory.
- In the disposable payload copy, provide `toolchain-restored/environment.sh` exporting those variables. Both unchanged `validate.sh` scripts resolve that path from the preserved public directory layout. Do not copy historical absolute paths as though they exist on a new machine.

The historical environment-script hash, Lean binary hash, Mathlib entrypoint/version/lock hashes, allowed axioms and dependency assumptions are preserved in `TOOLCHAIN_REQUIREMENTS.json` and component environment logs. Reconstructing configuration on another computer produces a new environment record; this selection has not certified that installation.

After the external environment is prepared, in the disposable payload root:

    bash tranche10/research/law-completion-correction/validate.sh public-replay-uniform
    bash tranche10/research/law-completion-correction/nonuniform/validate.sh public-replay-nonuniform

Run sequentially, one compiler lane, `-j1`, default heartbeats, with the scripts' 180-second module caps. Original source scopes remain in each `CHECKED_SCOPE.md`. For the additional reviewer interfaces, source the same environment, point `LEAN_PATH` at the freshly compiled relevant packet's `src`, then run `timeout 180 lean -j1` on that packet's included `ReviewerControls.lean`. The duplicate historical `AuthorReadback.lean` input is represented by the byte-identical author `readbacks/*.lean` and mapped in `PROVENANCE_MAP.json`. Review source-copy trees are intentionally absent.

Trust remains in the Lean compiler/kernel, standard axioms and installed Mathlib/dependency environment. Kernel checks do not establish the state-domain interpretation or philosophical application. Uniform and nonuniform receipts are separate; neither is inferred from the other.

## 4. Ordinary review and source inspection

Finite-limit acceptance is ordinary mathematical reasoning with recorded expected controls, not executed tests or a source-to-limit adapter. The included review identifies inherited ownership and a potential unary-evaluator hazard. Do not infer a checker from the word “certificate.”

Printed-source collation includes its accepted public addendum and public review only. Raw images, captures and private analysis are excluded, so their identity receipts attest historical inspections rather than make those inspections fully reproducible from this payload. The explanation-source-version note retains its bounded access failures and unresolved final-publication status. Missing captured inputs are declared limitations, not manufactured public success.
