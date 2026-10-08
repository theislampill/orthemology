# Preserved development and test history

- `development/001-api-contract-red.log`: preimplementation requested declarations absent; expected API red result (exit 1). The untouched original contract remains `tests/APIContract.lean`.
- `development/002-core-first-build.log`: general Init-only core compiled on its first build (exit 0).
- `development/003-finite-instances-first-build.log`: initial finite macro syntax and missing reduction errors; retained, not a semantic counterexample.
- `development/004-finite-instances-second-build.log`: elementary finite instances compiled after correction.
- `development/005-complete-controls-first-build.log`: conjunction-heavy finite propositions exceeded typeclass synthesis sizing; retained.
- `development/Diagnostics.lean` and `006-decider-diagnostics.log`: narrowed the issue; elementary quantified existential implications worked.
- `development/007-controls-expanded-instance-budget.log`: all controls compiled after increasing the finite typeclass synthesis size budget. This changes elaboration resources, not logical assumptions.
- `development/008-mediation-control-build.log` and `009-modal-ability-build.log`: explicit derived mediation and actual alternative-history ability controls compiled.
- `builds/20261007T091101.284295Z`: failed because Lean output compilation required source under the compilation root; fixed by using the package directory as compile working directory while retaining an isolated import/output directory.
- `builds/20261007T091119.289892Z`: readback used unsupported `pp.width`; replaced with supported `format.width`.
- `builds/20261007T091137.344212Z`: first intentionally false theorem was correctly rejected, but the build harness expected different Lean diagnostic wording. Tightened the acceptance marker to the actual `decide ... is false` diagnostic.
- `builds/20261007T091153.823692Z`: the direct constructor-inequality mutant stopped before decide because `simp only` had no work. Changed that one false test to direct ordinary `decide`; only logical false-proposition rejections are accepted now.
- `builds/20261007T091214.111813Z`: PASS, 58 declarations, all 18 intended semantic overclaims specifically rejected, 24 successful/expected-failure steps.
- `external-location/asb-replay-20261007-0918`: independent fresh-output replay PASS with the same 58 declarations and 24 steps; recorded below. This additionally exercised an output directory outside the packet.

These are retained error/build logs, not frozen copies of every intermediate source edit. The passing manifest binds the exact final sources. No development failure is counted as an intended successful negative test unless the final harness verified that ordinary kernel `decide` proved the proposition false.

## Field-restricted CND refinement requested during review

- `builds/20261007T092016.358954Z`: first refinement build exposed a harmless test macro sequencing error when simplification completely solved a qualification goal; the macro now runs decide on remaining goals.
- `builds/20261007T092053.858195Z`: PASS after the refinement, 63 declarations and the original 18 false-overclaim tests.
- `builds/final-field-cnd-v1`: final PASS, 63 declarations, 19 specifically false-proposition rejections, 25 total steps. This supersedes earlier receipts for current source identity only. It adds the field/global CND scope control and keeps every prior development artifact.
