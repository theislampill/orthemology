# Independent review: extracted source-v3 replay deliverable

Disposition: PASS for the scoped standalone source-only replay packet and its
Linux/pinned-dependency execution contract. The earlier wrapper findings W1 and
W2 are resolved in this exact candidate. The mathematical scopes remain those
of the separate model-v1, simulation-v1 and typed-v1 reviews; no tranche closure,
release authorization, physical implementation, progress, opacity or optimality
claim is made here.

## Exact deliverable

- Frozen packet: `tranche8/research/alias-runtime/public/source-v3`.
- PUBLIC_MANIFEST SHA-256:
  `38822e275751da5bcd9d7f3eab7776e373dba662f64bcc7cb27a654a962e5ad2`.
- Archive: `Eighth_Shared_Root_Safety_Source_Only_v3.zip`.
- Archive SHA-256:
  `ebdc889de82056029b16edb65de4af5c5503b0d83f7b49977f6340cac27c950b`.
- Archive size: 2,441,464 bytes, with 114 exact files under
  `Eighth_Shared_Root_Safety/`.
- Scientific typed milestone remains
  `1b88370e522b085349c6da4c0aab1b3763b557e02c3c4eb6d631f9d4ab4636d7`.

The reviewer verified the archive hash, unique canonical safe member paths and
absence of symlink entries, extracted into a fresh review tree, compared every
extracted file byte-for-byte with the frozen packet, and ran the extracted
packet's complete inventory/historical-mapping check. All matched. The archive
was rehashed after the full replay and remained unchanged.

## Wrapper corrections

### W1: exact historical lint allowance

The v1 wrapper could not complete because its strict warning filter rejected
two harmless warnings from the exact reviewed `ReviewerControls.lean`. The
correction preserves all reviewer proof bytes and allows only the two complete
known warning-plus-note messages. It is bound to the stage, source SHA-256,
actual source path, line/column, exact text and exactly one occurrence each.
Any leftover warning, error or sorryAx remains a failure. Independent controls
reject altered stage/hash/path/location/linter/note text, extra diagnostics and
missing/duplicate occurrences.

### W2: caller working directory

The v2 author's original-workspace replay passed, but the independent `/tmp`
run failed at the first source because Lean inherited the caller's root.
Version 3 explicitly sets `cwd=ROOT` in the single runner used for all version,
positive and mutant stages and records that value in each receipt row. Output
and logs remain absolute, separate paths. The unrelated-cwd and separate-output
regression tests pass. Both the old author workspace-only PASS and the actual
independent `/tmp` failure are preserved as distinct historical evidence.

All 22 wrapper tests passed independently from `/tmp`. Every mathematical,
predecessor, reviewer, positive control, mutant and dependency byte remains
unchanged from v2; the correction is confined to wrapper behavior, tests,
documentation and historical mappings.

## Independent end-to-end replay

The independent full run used the freshly extracted ZIP, not the author's
original packet tree. It was invoked from `/tmp`, with absolute paths to the
official Lean 4.19.0 distribution and pinned Mathlib c44e0c8, and a previously
absent output at `tranche8/reviews/alias-runtime/source-v3-delivery-replay`.

Terminal outcome: PASS, shell exit 0.

- 35 exact predecessor/new scientific modules compiled from source.
- 3 reviewer modules and 4 positive target/axiom modules compiled from source.
- All 42 positive source stages exited 0.
- Compiler version probe passed.
- All 5 isolated mutants exited 1 with their required intended diagnostics.
- Exact 88 scientific and 18 reviewer theorem inventories were audited.
- All 106 audited closures used only propext, Classical.choice and Quot.sound,
  or subsets.
- Exactly the two expected historical lint diagnostics were accepted, solely
  at the exact ReviewerControls stage.
- All 48 logged stages recorded the extracted packet root as compiler_cwd;
  none timed out. The largest measured compiler stage was 16.504 seconds.
- Source packet identity, full Lean distribution bytes, Mathlib source records
  and full pinned library-cache bytes were verified before and after.
- The final output contains a success receipt and no failure receipt.
- The reviewer rechecked every recorded log hash and every stage exit status.

Final independent receipt:
`tranche8/reviews/alias-runtime/source-v3-delivery-replay/RECEIPT.json`

Receipt SHA-256:
`596e7263fe3ecf3ab6fa1cc1c52e914c4de6949fb2941fbc360d3b6a6a355336`.

Additional evidence is in `source-v3-wrapper/`: boundary tests, archive
extraction receipt, static correction receipt and full-replay terminal log.
The author also completed a separate successful v3 run from `/tmp` before the
reviewer's run; they did not run competing full rebuilds concurrently.

## Fail-closed and trust boundaries

The wrapper checks exact packet inventories including historical mappings,
rejects extra files/directories and source symlinks, verifies pinned dependency
inventories and bytes, and refuses existing/protected/symlink-resolved output
locations. Inputs and dependency trees remain read-only. No package download,
network fetch or dependency update is performed.

All custom predecessor sources are rebuilt in the fresh output; the replay does
not rely on an old accepted custom-model `.olean` build. Precompiled Mathlib and
package libraries remain explicit, byte-pinned trusted dependencies. Hashing
them is not rebuilding them or proving the compiler/runtime/OS/hardware correct.
The tested host is Linux/Python 3.11 with the supplied pinned Linux Lean 4.19.0
and Mathlib/cache bytes. No broader platform compatibility is inferred.

Expected mutant rejection requires intended proof diagnostics. Timeout and
recognized resource/import/infrastructure failures are not credited as semantic
rejection. These checks remain bounded source-sensitivity controls, not a claim
that every alternative implementation or adapted proof is impossible.

Literal gate representation is still separated from reachable weak simulation.
No runtime preparation/cancellation/certification macro refinement, native
21-path controller, physical routing/control implementation, clock/service
bound, map secrecy, opaque-search theorem or optimum transfer is introduced by
this successful packaging/replay result.

The immutable ZIP/packet were not modified to include this later review or
receipt. They can be supplied as external evidence without changing the tested
deliverable identity. No canonical source, dependency or user product was
modified by this review.
