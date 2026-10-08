# Eighteenth: portable code and replay evidence

This package contains **independently reviewed code and replay evidence** at the exact prepared-environment scope. Qualification records are fixed snapshots with their own timestamps; they do not assert the current publication state or completion of the broader Eighteenth research. Component research reviews and this package's replay/packaging checks are separately identified.

## What is included

- The exact `reference-v1` and `efficient-v1` Python production sources, author tests, and selected independent test/oracle programs. Their relative layout is preserved, so the original files are byte-identical.
- A hidden-change Lean lane with **125 custom source modules**: 97 inherited, three finite-criterion, five actual-law, nine controller, ten necessity, and one combined semantic-endpoint module. It includes **64 selected control/audit files**.
- A separate HasE lane with **84 custom source modules**: 82 inherited modules, the existing `UArrowAndCompilerControls`, and the new `InhabitedEndpointControl`. It includes **eight selected control/export files**. The existing and inhabited results remain separately identified.
- Exact source hashes and custom import lists, external revision/object inventories, a configurable replay entry point, and public verification summaries.
- An optional ordinary normal-form diagnostic run after the HasE syntax export. This calculation is explicitly separate from Lean theorem checking.

No custom `.olean` objects, external dependency caches, source books/page images/extractions, private correspondence, raw internal review reports are included. Ordinary theorem documents are outside this code-evidence package.

## Quick start: Python only

Use Python 3.10 or later. Recorded executions use Python 3.12.14 on Linux. No package installation or network access is required. Run from this package directory:

```
python -E -S -B replay.py verify
python -E -S -B -m unittest discover -s tests -v
python -E -S -B replay.py python --output ../python-replay
python -E -S -B replay.py python-full --output ../python-full-replay
```

The short replay runs both author suites and the independent semantic, protected-production-path, and previous-adversarial suites. The full replay additionally runs the specified finite censuses and forged-negative comparisons. Each run copies the code to its new output directory before executing scripts that write results. It never writes into the distributed sources. Use `-E -S` at entry to disable ambient Python variables and site/customization startup. The initial interpreter and standard library are trusted; checks inside a running program cannot undo code that already ran during interpreter startup. Do not run with `-O`, `-OO`, or `PYTHONOPTIMIZE`: some original evidence programs use assertions.

Production entry points:

- Reference: `model.validate_model`, `synthesis.solve`, `certificates.check_positive`, `certificates.check_negative`, `controller.action_for_history`.
- Efficient: `efficient.solve` and `negative.check_negative`; it imports the hash-pinned sibling reference helpers.
- The exact Python data interfaces are in `tranche18/research/hidden-change/reference-v1/API.md`.

The efficient package's production source avoids the exhaustive reference solver and checker paths. Bounded differential tests support implementation fidelity; they are not a Lean proof of Python correctness or Python/Lean correspondence.

## Lean environment: supplied separately

The Lean replay is self-contained **for custom source**, not self-contained for its external toolchain. Supply the already provisioned Lean 4.19.0 Linux x86-64 release and both separately pinned external object sets. The package does not fetch, install, or build dependencies.

**New-machine limitation:** this tree does not distribute the external snapshots or provide a qualified byte-exact acquisition/rebuild recipe for a clean Linux host. A generic Lean/Mathlib installation is not enough to reproduce the required inventories. Readers without the matching snapshots can still run package verification and the self-contained Python lane; Lean replay requires a separately supplied, verified environment. No snapshot download is represented as published here.

The hidden-change inventory comes from the retained official-cache environment plus cache-client tooling. The HasE inventory comes from an earlier limited source build, and is treated here as a pinned prepared snapshot. Its 1,369 module names also occur in the broad hidden-change inventory, but **14 Mathlib object hashes differ**. This byte comparison does not establish the reason for those differences or general bit-for-bit build reproducibility. See `dependencies/ORIGINS_AND_AVAILABILITY.md` and `dependencies/INVENTORY_COMPARISON.json`.

Copy `environment.example.json` to a file outside this package and replace its example paths. A dependency root contains one directory per package, such as `mathlib`, `aesop`, and `batteries`. Each package is at its specified Git revision; its imported objects are under `.lake/build/lib/lean/`.

The lanes deliberately have different inventories:

- Hidden-change: **6,646 external `.olean` objects**, bound by `dependencies/hidden-change.json`.
- HasE: **1,369 external `.olean` objects**, bound by `dependencies/hase.json`.

Do not substitute one object set for the other simply because their source revisions agree. The runner checks every listed object digest and byte count, rejects extra or missing `.olean` objects in each specified cache root, checks source revisions and tracked cleanliness, and checks the Lean executable digest. A mismatch is an environment failure, never negative mathematical evidence. The example configuration is not an installer or evidence that another computer has these dependencies.

Then run:

```
python -E -S -B replay.py lean-hidden --environment ../my-environment.json --output ../hidden-replay
python -E -S -B replay.py lean-hase --environment ../my-environment.json --output ../hase-replay
python -E -S -B replay.py all --environment ../my-environment.json --output ../complete-replay
```

Every output directory must be absent and outside the package. Runs are serialized, with one Lean job and a configurable per-module timeout. A stopped or failed run is preserved. Use a new output directory for a retry; no prior custom object is reused. The runner's Lean search path contains only its fresh custom build directories and the explicitly configured external roots. Ambient Lean/Python search-path variables are removed. Direct Python children disable site initialization with `-E -S`; inherited `PYTHONNOUSERSITE=1` also protects the original tests’ nested subprocesses from user-site customization.

## Trust boundary and exact meaning of a pass

1. `MANIFEST.json` checks the package's exact file set, sizes and SHA-256 identities. It is an integrity inventory, not a digital signature or proof of publisher identity. Obtain its expected digest from the associated delivery/verification channel if authenticity matters.
2. `SOURCE_BINDINGS.json` binds copied production, inherited and test sources to their original bytes. Portable orchestration, tests and public summaries are separately authored packaging material. Historical receipt digests identify prior checks but are not substitutes for running the sources.
3. A Lean replay recompiles every module in that lane's custom import closure from the included source, then runs each declared selected control. It cannot silently skip a missing source or control. Controls with the same generic module name are isolated by group.
4. A positive run must actually produce a new object and must not report a placeholder proof. Specified axiom audits must print the exact expected number of distinct declarations, using only `propext`, `Classical.choice`, and `Quot.sound`. Inherited nonfatal warnings remain in the logs.
5. An expected failure is credited only at exit 1 with the declared mathematical/type-mismatch diagnostic; import, syntax, unknown-name, resource-limit and timeout failures are not credited. Failed controls test the displayed statement or implementation change, not unrestricted logical underivability.
6. The pinned external `.olean` caches remain trusted. Compiler/runtime/standard-library behavior remains trusted too. The executable digest and recorded official archive digest do not establish a cold compiler bootstrap or individually certify every runtime/shared-library file. No external dependency cold build, native compiler/FFI verification, Windows execution, or macOS execution is claimed.
7. Logs, commands, copied source hashes, fresh object hashes, audit outputs and a terminal result are written under the supplied output directory. A timeout, interruption, missing dependency or bad input means execution failed; it is never a valid negative certificate. A packaging replay does not by itself confer release or research-closure authority.

## Mathematical scope in brief

The hidden-change Lean endpoint joins the checked finite criterion, literal Lean controller sufficiency, and arbitrary lawful measurable private-seed policy necessity for the specified finite-rational two-mode model with one hidden irreversible change. It preserves full input and initial-state binding. The switch acts after the chosen action and before its receipt; governing priorities are associated with departure pairs. The policy sees public physical/action history. The final component review is accepted at that scope.

This does not establish Python/Lean representation or runtime correspondence, parser correctness, arbitrary-real effectivity, a general POMDP result, variable-mode-count behavior, finite-memory sufficiency, finite learning/stabilization time, or a physical deployment guarantee. Source-level polynomiality of the efficient Python solver is separate from the stochastic and Lean results. See `VERIFICATION_SUMMARY.md` for component-by-component status and limits.

The HasE result proves exact J transport to particular ordinarily typed, closed `N → N` endpoints using the existing rules and predecessor equality. It does not settle the literal frozen compiler `x/x+0` HasE target, which remains unresolved. The rejected endpoint cast has a reflexive target that is itself inhabited, even with the same J-shaped witness; the included independent positive control demonstrates this. Thus negative casts show exact-statement sensitivity only.

The HasE normal-form script independently reduces the exact exported SKI terms and checks distinct beta-eta normal forms with de Bruijn indices. It is a finite ordinary diagnostic, not a kernel theorem of beta-eta nonconvertibility, a new calculus model, or proof that those endpoints belong to the frozen unary compiler image.

## Reading the results

`VERIFICATION_SUMMARY.md` records historical component checks and excluded failed attempts. `COMPONENT_STATUS.json` records author/independent stages and source bindings. The author full replay passed. Independent package acceptance used a recovered composite: 187 retained hidden-change compilation/control units and 159 objects were individually verified; the remaining two controls were freshly compiled, and the full HasE lane was freshly replayed. The interrupted original receipts remain unchanged and nonterminal. This is not described as an uninterrupted independent full-runner pass. See `INDEPENDENT_PACKAGE_SUMMARY.json`.

Timestamped package-level qualification facts are recorded separately in `PACKAGE_STATUS.json`; they must not be inferred from a component's accepted status and do not track later archive creation or publication. The raw private reviews are intentionally not distributed.
