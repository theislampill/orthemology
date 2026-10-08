# Eighteenth public code and replay evidence

This archive contains the reviewed custom sources, executable checks, and separately qualified dependency-setup recipes for the Eighteenth work. Qualification records are timestamped snapshots. They do not by themselves determine completion of the broader research or imply stronger mathematical claims.

## Start here

- **code-evidence/** contains the unchanged exact Python reference and efficient implementations; the 125-module hidden-change and 84-module HasE custom Lean source closures; selected controls; exact dependency bindings; the portable replay runner; and public verification summaries.
- **hase-source-build/** provides the separately reviewed HasE dependency source-build recipe. It is pinned to the exact sibling code-evidence manifest and produces a clearly labelled derived copy with source-build custody.
- **hidden-change-cache-setup/** provides the separately reviewed official-cache acquisition recipe for the original hidden-change dependency inventory. Its source-acquisition preparation uses the supplied hase-source-build sibling. Keep the setup and code-evidence directories together.
- **four-state-stress-control/** adds one small, separately reviewed implementation check against unchanged code and independent exhaustive oracles. It targets simultaneous threshold-induced splitting into two nontrivial two-state MECs.

The immutable base manifest is:

`9f2a0f116f90fc4189faacc79d5b7c02116e1d36735cc2cdffe4f9117406de95`

Both setup supplements bind this exact base. The base’s original prepared-environment wording is intentionally preserved; the sibling setup recipes record the subsequently qualified provisioning steps. No scientific source, control, runner or original dependency pin was changed to accommodate setup.

## Python: no Lean environment required

From this archive’s top directory, use Python 3.10 or later:

```sh
python -E -S -B code-evidence/replay.py verify
python -E -S -B code-evidence/replay.py python-full --output ../eighteenth-python-replay
```

The output directory must not already exist. This runs the author/independent suites and specified finite campaigns using only Python’s standard library. It is evidence of bounded executable fidelity, not a Lean proof of Python/Lean correspondence.

## Lean: choose the relevant setup recipe

Read each supplement’s README and prerequisites before running its commands. The archive does not contain the external toolchain, source Git checkouts, dependency objects or npm downloads. Each recipe requires explicit local paths and new work directories outside the supplied packages.

**Hidden-change lane.** The cache recipe’s qualified run checked five freshly compiled Cache tooling identities before its sole official acquisition, then matched all 6,646 original dependency-object names, sizes and hashes and passed a fresh Mathlib import. Its generated environment is for the unchanged hidden-change lane. This is official-cache acquisition and exact-byte verification, not a dependency theorem source rebuild or an additional full hidden-change proof replay.

**HasE lane.** The source-build recipe rebuilt 1,369 third-party objects from pinned sources, then replayed all 84 unchanged custom modules and eight selected controls/exports. It changes only the HasE dependency inventory and manifest in a separate SOURCE_BUILD-derived copy. Follow that recipe’s derivation and replay steps; do not silently replace the base inventory or use the broad hidden-change cache as the HasE environment.

The source builds/acquisitions were qualified on the existing specified Linux host, with trusted official compiler/runtime tools. The HasE build used clean local clones and cached npm registry downloads. A separate official-URL source-preparation phase retrieved and verified all nine repositories, but an empty-cache online npm/widget attempt ended without a qualified terminal result. No clean-OS installation, new-host end-to-end provisioning, or one uninterrupted all-online recipe is claimed. Service availability and the listed prerequisites remain external conditions.

## What the verification says

The author full custom-source replay passed. Independent base-package acceptance used a recovered composite: retained source/log/object evidence was individually checked, two missing controls were freshly completed, and the complete HasE lane was freshly replayed. The original interrupted receipts were preserved unchanged, not relabelled as an uninterrupted success. The public summaries explain the exact scope, counts and receipt digests.

The setup supplements received separate source/custody and public-content review. The HasE ordinary normal-form diagnostic remains a finite ordinary calculation, not a kernel theorem. The literal frozen compiler x/x+0 HasE question remains unresolved. No Python/Lean correspondence or kernel-checked arbitrary-real effectivity is claimed; nor is there a general finite-memory or learning-time guarantee or physical deployment assurance.

## Bounded four-state stress control

Archive revision 2 adds only this stress-control sibling and the corresponding outer guide/manifest update. All three previously reviewed sibling trees are byte-identical to revision 1.

The single capped campaign checked 32 distinct complete inputs: eight fixed labelled templates, each with four initial states. All comparisons passed, yielding 30 positive and two negative checked bodies. The structural anchor removes low-odd bridge actions at an attained-even threshold and exposes two simultaneous nontrivial two-state maximal end components. Variants check separate even witnesses, numerical versus support equality, bridge removal and matched/revealing exits.

This is modest bounded implementation evidence, not 32 different graph structures, an exhaustive four-state census, a theorem extension or a change in baseline acceptance. The supplement includes exact inputs, results, source bindings and a replay harness capped at 180 seconds. Its 12 implementation/oracle/census copies match the unchanged code-evidence sibling byte-for-byte. No original campaign or build was repeated to package this addition.

## Integrity and contents

OUTER_MANIFEST.json binds every supplied file except itself. Each sibling also has its own exact manifest. These are integrity inventories, not digital signatures; use the archive hash supplied with delivery to bind the received file to that delivery record. The supplement pins the inner base manifest, not this outer archive’s hash, so there is no self-referential archive binding.

Only reviewed public source, setup code, tests, inventories and summaries are included. External dependency caches and binaries, generated custom objects, raw private reviews, correspondence, source books/images/extractions and private source-accounting material are excluded. Running the recipes creates full local execution logs for the reader’s own environment.
