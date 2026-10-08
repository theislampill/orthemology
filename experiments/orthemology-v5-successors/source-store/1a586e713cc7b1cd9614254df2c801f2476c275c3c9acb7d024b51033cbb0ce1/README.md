# Fourteenth: combined Lean verification candidate

**Verified research candidate; no adoption of a changed calculus.** This source-only package preserves 53 inherited modules and all six accepted `IntensionalIdentity` modules byte-for-byte, then adds the six frozen `ExtensionalRepair` modules. The old negative results and the new positive result concern explicitly different typing judgments.

## Reproduce

Install the official [Lean 4.19.0 release](https://github.com/leanprover/lean4/releases/tag/v4.19.0), including Lake, following the [Lean installation instructions](https://lean-lang.org/install/). Git, Python 3, Bash, and network access to the dependency repositories are required. Select the supplied `lean-toolchain` and ensure its executables are on `PATH`.

From this directory:

```sh
sha256sum -c SHA256SUMS
export MATHLIB_NO_CACHE_ON_UPDATE=1
lean --version
lake --version
lake build
bash verification/run_checks.sh
```

For a genuinely clean replay, start with a fresh source-only copy with no `.lake` directory, no dependency checkouts, and an empty cache directory. The normal `lake build` acquires the pinned dependencies automatically. No cache-fetch command, manual `LEAN_PATH`, sibling dependency path, Mathlib shim, or precompiled project output is required. Do not run `lake update` to upgrade the supplied pins.

All **65 project source modules** are explicitly registered in three default build targets: `InheritedBaseline`, `IdentityVerification`, and `ExtensionalRepairVerification`. The audit module is included. Verification probes live separately under `verification/`; the deliberately ill-typed controls are excluded from default build and tested by the check script.

Mathlib is pinned to `c44e0c8ee63ca166450922a373c7409c5d26b00b` at its official Git repository. `lake-manifest.json` locks all eight transitive dependencies too. This is a network-reproducible source package, not an offline dependency or toolchain bundle.

## What is checked

The imported witness names are in `P01AC.Intensional`. They have the exact endpoints `atom I` and `atom ((S K) K)`, the proof polynomial `atom I`, and the carrier `All (Pi (param 0) (param 0))`.

- Current `P01AC.Has` and bridge-only `P01AC.Intensional.Plus.HasPlus` still have no proof polynomial inhabiting `separationB`. Their original all-polynomial noninhabitation theorems are unchanged.
- The separately named `P01AC.ExtensionalRepair.HasE` derives the exact imported `separationE : separationB`. `pointwise_evidence_has` checks the actual bracket-compiler polynomial `K I`; one PiExt application and one AllExt application complete the finite witness.
- `HasE` has exactly 20 typing constructors: the retained 18-rule Plus grammar and the two finite typed-extensional schemas. Context and formation remain 2 and 7 constructors. Conversion is the unchanged imported eight-constructor `PolyConvPlus`; no conversion generator is added.
- `ExtensionalRepair.has_sound`, `form_sound`, and `context_sound` establish the corresponding all-rule conclusions in the original `P01AC` F/G interpretation. The checks retain Pi's dependent cross-argument clause and both All endpoint-uniformity clauses.
- `ExtensionalRepair.raw_separation_no_has` excludes every proof polynomial from the formed Raw-indexed I/SKK identity. `closed_raw_identity_conversion` has no proof-polynomial scope premise and covers indirect J/elimination routes through all-rule soundness. Proof erasure gives Raw typing of the proof program; it does not change the identity's carrier.
- `strict_typed_identity_extension` combines the exact positive witness, the preserved current/Plus noninhabitation, the Raw obstruction, and endpoint polynomial nonconversion.
- The old `closed_typed_identity_iff` remains a theorem of **Plus** with its carrier formation, two endpoint typings, and two endpoint closure hypotheses. The package neither drops those hypotheses nor transfers that characterization to E.

These results do not establish general completeness, minimality, decidability, arbitrary structural closure of E, a full contextual quotient, physical identity, historical novelty, or adoption of the candidate. They do not formalize a separate undecidability argument.

## Reproducible checks and receipts

`verification/source-lock.json` binds all 65 source hashes and the nine official Git pins. `verify_sources.py` checks them, exact retained grammar copies, all default roots, and proof-token hygiene. Its checks were also tested against deliberate source, root, pin, and proof-hole mutations.

`CheckTheorems.lean` and `AxiomAudit.lean` retain the accepted intensional checks, including all 101 listed public theorem declarations. `CheckCombined.lean` checks exact positive and negative target interfaces, Raw obstruction, soundness conclusions, and every explicit premise of the two new schemas.

`CombinedAxiomAudit.lean` inspects the actual Lean environment: the extensional namespace has **156 constants, of which 58 are theorem declarations**. These counts include generated declarations; they are not a claim of 156 or 58 authored theorems. The 11 decisive named results are explicitly checked to be theorem declarations.

`IndependentKernelChecks.lean` additionally replays 54 compiled retained-constructor type comparisons, exact new-schema comparisons, literal old semantic clauses, the expanded witness, and proof-value dependency inspection. Its logical-safety traversal checks all 140 safe namespace roots and their 2,368-declaration dependency closure. No unsafe or partial declaration is used in that closure. The compiled environment contains 16 executable compiler auxiliaries for data definitions; these are distinguished from proof dependencies and source-level unsafe declarations.

Actual transitive axiom collection permits only ordinary Lean foundations: `propext`, `Quot.sound`, and inherited `Classical.choice`. The soundness and positive witness use the first two; obstruction and strictness results also inherit `Classical.choice`. No `sorryAx` or custom axiom is admitted.

Nine deliberate negative controls must fail with exactly one intended type error each. They test missing closure/scope arguments, conflation of current/Plus/E judgments, the wrong identity carrier, and reversed noninhabitation polarity. These are **interface-rejection tests, not logical independence proofs**. Genuine noninhabitation comes from the checked all-polynomial theorems.

The concise `verification/receipt.json` records the successful fresh-network build and check run, source bindings, toolchain provenance, warning counts, and review bindings. Raw private review reports and primary-source documents are not included.

## Execution and provenance limits

The independent bootstrap began from source files only, with no `.lake`, `.olean`, seeded dependency repository, or existing cache. Ordinary `lake build` automatically cloned all nine exact pinned dependencies and freshly compiled **65 project modules plus 54 dependency modules**. All source and configuration bytes remained unchanged. The full check script exited 0. The build retained **22 inherited linter warnings**, with zero warnings in either six-module addition.

The official Lean 4.19.0 executable, compiler commit `6caaee842e94`, was reused from the already downloaded official release; the toolchain itself was not rebuilt or downloaded again. Its recorded archive SHA-256 is a local digest of that HTTPS download. No independent vendor checksum was available.

Lake used the manifest's official HTTPS Git URLs through the execution environment's ordinary Git/network path, with no configured Git URL rewrite. This establishes working automatic dependency acquisition there; it is not independent authentication of direct vendor-network transport. Only the needed dependency module closure was compiled, not all of Mathlib.

No toolchain, dependency checkout, `.lake` state, binary cache, proof-object archive, or private machine path is distributed. `lean-toolchain` is the ordinary text version selector. Verification does not grant publication, deployment, merge, or amendment of the original calculus.
