# Reproducibility dependencies for the proposed public selection

3 October 2026 UTC. Dependency inspection only; this review did not rerun another reviewer's mathematical test suite or compiler lane. No accepted code was edited.

## Distinguish three things

- Identity receipts identify prior findings and source owners; they need not redistribute their prose.
- Executable dependencies must remain present, or be explicitly named as external prerequisites, for a public replay claim.
- Private source-byte inputs can support a historical verification receipt without being copied into the public archive. A replay needing those bytes is not thereby self-contained.

## Occurrence author checker

Retain the entire current `release-candidate-v1/checker` source subtree, including `context_effects.py`, `read_cover.py`, all validation scripts, `tests/test_contract.py`, and the unchanged `fixtures/source_roles.json`. The standard-library imports and sibling imports require no earlier programme code. The fixture's relative primary_capsule locator continues to resolve when the compact replacement is staged at the component root. The public capsule replacement does not alter any imported module, event input or expected result.

The checker README's commands exercise supplied-model semantics. `source_and_release_validation.py` reads the JSON fixture, not the private raw HTML. Its claims must remain annotation consistency and constructed service calculations; it does not redo the source-language inspection or independently authenticate the capture.

The existing scripts write their logs, so replay should use a new copy or a new output location without overwriting the frozen evidence. This is a reproducibility condition, not a new test result.

## Independent occurrence review

Keep `independent_models.py`, `run_independent_review.py`, and `run_independent_mutations.py` together if distributing their replay source. The latter two accept `--candidate` and can be pointed at the one included current checker rather than another copied reviewer input tree. Their reference-model dependencies are local and standard-library only. Retain their associated accepted logs, counts and input identities as historical evidence. Reconstructable mutation copies need not be bundled as additional input copies.

The full `run_all_review.py` wrapper has a different dependency boundary. Its source-fixture groups invoke `run_source_fixture_review.py`, which additionally reads:

- the retained Latin response bytes identified by the fixture hash;
- the paired rendered-source record identified by the fixture hash.

Those raw inputs are excluded from the public selection. Supplying `--candidate` does not remove that dependency. Therefore the public archive must **not** advertise the eight-group wrapper as self-contained or silently describe a skipped source-binding group as passed in a public replay. It may retain the wrapper and the original complete execution receipt with an explicit prerequisite note, while documenting the model-only commands separately. An online re-fetch is not guaranteed to reproduce the historical bytes and cannot silently replace their identities.

The independent source-inspection projection preserves custody hashes and points to the public interpreted-content owner. It does not pretend those hashes contain the excluded bytes.

## Bounded-release independent controls

`reviews/bounded-release-application/check_observations.py` imports only Python standard-library modules and no candidate code. Preserve it and the source-bound review receipt if that independently replayable small-model evidence is included. The historical exact-candidate reexecution remains identified by its receipt; no separate copy of the philosophical source paper is needed inside the review folder.

## Uniform and nonuniform Lean packets

Preserve each packet's implementation `.lean` sources, readback `.lean` source, scope ledger, accepted validation logs, exact manifest, and replay script. The separate independent receipts, review control sources, and input identities should stay associated with the correct packet. Their declarations import Mathlib and their sibling modules, not predecessor philosophical prose.

Both current `validate.sh` scripts locate `toolchain-restored/environment.sh` relative to the common research root. They then use its existing Lean 4.19.0/Mathlib installation, `LEAN_PATH`, and trusted compiled dependency environment. Consequently one of the following must be explicit in the final package:

1. The same compatible environment/dependency layout is provided and bound as a runtime prerequisite; or
2. The portable source and historical replay records are supplied, with clear reconstruction prerequisites and no claim that the unchanged script runs in an arbitrary extracted directory.

A predecessor identity receipt is not a substitute for that environment script or dependency installation. Conversely, bundling an entire predecessor report/evidence archive is unnecessary merely to satisfy a code import. The `.olean` products are not a substitute for fresh source compilation, and the historical independent review did not use author-built module objects as proof of its own replay.

This review has made no toolchain installation, source modification, wrapper patch, or new portability certification. Final packaging should verify the declared path layout without upgrading the existing scoped verification claims.

## Explicit public model-only replay

Run from an extracted layout retaining the Tenth paths below. If staging uses different component names, set CANDIDATE and REVIEW to those included directories. This is a model-only route; it deliberately makes no source-byte provenance replay claim. The commands work in fresh temporary copies so they do not overwrite accepted logs.

```sh
CANDIDATE="$PWD/tranche10/research/occurrence-continuation/release-candidate-v1/checker"
REVIEW="$PWD/tranche10/reviews/occurrence-checker"
REPLAY=$(mktemp -d)
mkdir -p "$REPLAY/checker" "$REPLAY/review"
cp -R "$CANDIDATE/." "$REPLAY/checker/"
cp "$REVIEW/independent_models.py" "$REVIEW/run_independent_review.py" "$REVIEW/run_independent_mutations.py" "$REPLAY/review/"
(cd "$REPLAY/checker" && python -m unittest discover -s tests -v && python exhaustive_validation.py && python source_and_release_validation.py && python semantic_mutations.py)
python "$REPLAY/review/independent_models.py"
python "$REPLAY/review/run_independent_review.py" --candidate "$REPLAY/checker" --output "$REPLAY/review/model-results.json"
python -O "$REPLAY/review/run_independent_review.py" --candidate "$REPLAY/checker" --output "$REPLAY/review/model-results-optimized.json"
python "$REPLAY/review/run_independent_mutations.py" --candidate "$REPLAY/checker" --directory "$REPLAY/review/mutations"
```

The last command runs reviewer-authored mutants in the temporary review copy. Neither it nor the preceding commands establishes the historical byte binding to excluded primary captures. Do not label this subset as the historical full eight-group review. The historical wrapper, exact original logs and source-binding receipt retain their own stated input dependencies.

The standalone joined-release observation controls can be replayed independently with Python and Python `-O` using the included `check_observations.py`; they import no candidate package and write their result to stdout. The finite-limit endpoint has no admitted executable checker: its18 controls are written mathematical outcomes, not18 executed tests.

The Lean packets require the declared trusted Lean4.19.0/Mathlib environment and compatible layout. Their toolchain metadata and setup requirements must be bound in the final packet; no runtime bundle, hermetic build or fresh compiler-bootstrap verification is represented here.
