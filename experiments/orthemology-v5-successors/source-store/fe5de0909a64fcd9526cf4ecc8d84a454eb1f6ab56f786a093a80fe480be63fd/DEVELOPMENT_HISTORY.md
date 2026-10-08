# Development history and evidence limits

The root approved the preserved design and mapping contract before source
implementation. No component source was edited, no download performed, and no
broad earlier suite replayed.

1. `development/001-api-red.log` records six absent declaration identifiers.
   This is only an API-presence development check. It is not a semantic red test
   or proof that every finite theorem followed a test-first chronology.
2. Fresh development objects were built from the four unchanged component cores
   with the existing official compiler and explicit trust zero. Their logs are
   `002` through `005`.
3. `006-JointFiniteInterpretation.log` records a source-authoring error: Lean does
   not accept the attempted namespace-alias syntax. The resulting downstream
   unknown-name/admission diagnostics are failed elaboration, not accepted
   proofs or premise countermodels. All aliases were replaced by full names.
4. `007-joint-full-names.log` records a second authoring error: multiline path
   terms needed correct layout and explicit endpoint parameters. This was
   repaired only in the new joint source.
5. `008-joint-path-terms.log` is the first complete joint-model development pass.
6. `009-joint-final-extra-boundary.log` passes the final model including the
   explicit dep/direct-support distinction. `010-acceptance.log` passes the
   acceptance module. `011-rejections.log` contains exactly four intended
   false-proposition diagnostics. These four are semantic overclaim rejections;
   the earlier authoring failures are not.
7. `012-readback.log` and `013-proof-readback.log` contain an unknown `pp.width`
   option error, despite producing the later readback text. Looking only at the
   tail initially concealed this failure; they are not passing receipts. The
   strict fresh runner correctly stopped at the same error and preserved
   `verification-final/FAILURE.json`. Lean 4.19's registered `format.width`
   option replaces it in both readback files. This is a readback-tooling repair;
   the already passing interpretation/proof source is unchanged.
8. `014-readback-option-fixed.log` is the clean corrected development readback.
   The authoritative `verification-final-v2/VERIFICATION.json` then records a
   full fresh pass: all five local modules, Acceptance, exactly four semantic
   rejections, 88 declaration types, 56 theorem axiom audits, 23 definition
   bodies, 15 theorem bodies and all 13 mapped component calls. The final
   current-source/diagnostic readback rechecked that receipt and its source
   identities. `harness/FINAL_TESTS.log` records 13 passing runner unit tests.

`development/check.py` is a small local development runner and its objects are
not the authoritative evidence. The separately tested `reproduce.py` runner
performs a cold local-core replay to a fresh directory, binds the existing
cached object bytes, checks all diagnostics, and refuses overwrite. The final
receipt, not a development log or successful tool return alone, determines the
packet's verification status.
