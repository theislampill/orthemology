# Build and verification

## Pins and scope

Use official Lean 4.19.0, release commit 6caaee842e9495688c1567e78c0e68dbb96942aa, and Mathlib revision c44e0c8ee63ca166450922a373c7409c5d26b00b. TOOLCHAIN_PINS.json records the associated dependency source revisions. Python 3.10 or newer is sufficient for the standard-library tests and runner; author and review execution used Python 3.12.

Dependencies and compiled proof objects are intentionally absent. Source identity, dependency identity, a fresh source compilation and actual deployment are different assurance claims. The supplied historical checks reused 1,365 hash-verified dependency objects; they did not bootstrap Lean or cold-build all dependencies.

## Prepared dependency environment

With the pinned Lean binary on PATH and LEAN_PATH pointing to a compatible compiled pinned Mathlib/dependency environment, run:

    python3 replay.py --output /path/to/new-output-directory

Optionally set LEAN_BIN to the intended Lean executable. The output directory must be absent and outside this source package. The runner checks SOURCE_MANIFEST.json, verifies the Lean version, freshly compiles the six author modules and independent controls into its own initially empty object directory, compares the exact author readback, and runs both finite-check implementations. It performs no network access and does not overwrite package sources or retained evidence.

The runner's checks use the prepared environment's dependency objects. It records the effective Lean binary and direct-import hashes. A changed platform/toolchain/dependency environment needs its own review of those identities; a successful run must not be described as reproducing historical object bytes unless that comparison was actually made.

## Provisioning with Lake

The supplied lean-toolchain and lakefile.lean pin official Lean and Mathlib. In a separate working copy, ordinary Lake provisioning can obtain the declared dependencies:

    lake update
    lake exe cache get
    lake build GroundedAttestation
    lake env python3 replay.py --output /path/to/new-output-directory

Provisioning requires network access and may obtain the broader Mathlib cache. It was not rerun for this public projection; the location-independent runner was tested using the already qualified pinned environment. The Lake file was checked by the pinned Lean parser. Avoid interpreting cache acquisition as a cold source build.

## Failure interpretation

A failed source hash, Lean invocation, readback comparison or finite test stops the runner and leaves logs in the requested output directory. Missing dependencies are an environment failure, not rejection of a mathematical statement. The historical review-harness path-prefix failure is preserved and identified separately from candidate proof checks.

The root-cut search's general four-label lower boundary is a written proof supported by bounded search. The two displayed counterexamples are kernel checked. No general algorithmic refinement, live authority or physical action is certified.
