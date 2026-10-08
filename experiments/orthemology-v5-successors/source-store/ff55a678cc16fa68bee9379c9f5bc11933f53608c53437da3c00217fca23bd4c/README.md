# T20 generic Church identity-carrier probe

This source-only candidate proves a narrow positive result in the unchanged calculus. It does **not** decide the HasE identity between the literal compiled `x` and `x+0` endpoints.

## Exact checked results

`N` is the inherited erased polymorphic Church carrier. The new module proves:

1. Current `Has [N] I (Id_Raw(n I I, I))`, for the generic variable n.
2. Current typings of `F = abstract(n I I)` and `G = abstract I` at `N → Raw`.
3. `HasE [] I (Id_(N→Raw)(F,G))`, using the exact inherited J rule and the separate typed piExt constructor.

The domain and final carrier are inhabited. The underlying proof-coordinate J mechanism was already present in inherited positive controls; this module is a concrete Church-input specialization and extensional closure.

Source SHA-256: `43e824a746ef624e8d783e89d62d3dc95108042cb311f931cd868cbe5cf76028`.

All 46 new theorem declarations were checked. Forty-three depend only on `propext` and `Quot.sound`; three are axiom-free. No new axiom, sorry, semantic reflection, modified conversion rule or replacement compiler is introduced.

## Evidence boundaries

- Exact source, statement contract and J/piExt interface passed independent fresh Lean 4.19.0 checking with `--trust=0`.
- Three deliberate statement mismatches reject carrier promotion, changing these F/G endpoints to the `N→N` carrier, and laundering the closed HasE result into current Has. They are not noninhabitation results.
- `BeforeImplementation.lean` verifies that the probe declaration is absent when only predecessor modules are imported.
- Ordinary erased lambda analysis distinguishes `λn. n I I` and `λn. I` by beta-eta normal form. This distinction is not a Lean theorem in this package.
- The exact compiled `x` / `x+0` HasE judgement remains OPEN. The new Raw equality does not provide the missing graph projection-fusion equations. In particular, independently chosen numeral counts also satisfy `n I I = I`; this is not full parametric uniformity.
- Old T16 science-control registries remain NOT_RUN. Required inherited modules were compiled only as dependencies of the new proof, not as a broad historical replay.

## Inputs and portable replay

Required inputs:

- The unchanged `Sixteenth_Orthemology_Proof_Source_Recovered_v1` package, identified by `PREDECESSOR_CLOSURE.json`. Only its listed 55-module closure is compiled.
- Official Lean 4.19.0 for Linux x86_64, commit `6caaee842e9495688c1567e78c0e68dbb96942aa`.
- The nine exact official dependency checkouts in `lake-manifest.json`, prepared with the pinned official Mathlib cache for `Mathlib.Data.Bool.Basic`. `DEPENDENCY_OBJECTS.json` binds the 59 prepared dependency objects. This is an official cache setup, not a Mathlib source cold build.
- Python 3, Git, and a new output directory outside the inputs.

Run:

    python3 replay.py --predecessor PREDECESSOR --lean LEAN_EXECUTABLE --dependencies DEPENDENCY_DIRECTORY --output NEW_OUTPUT

The fixed-scope recipe checks source and object identities, freshly compiles the required inherited sources and new module, runs exact positive contracts and intended rejection controls, and writes a portable status receipt. It performs no installation or network access and never overwrites an existing output directory. Preparation of missing dependencies is a separate step using the official toolchain and exact supplied pins.

The package deliberately contains no toolchain, cache, binary object, provisioning log or absolute execution path. Detailed original execution/provisioning receipts remain separate; this candidate does not rewrite them as public records.
