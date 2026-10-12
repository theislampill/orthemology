# RandomizedFinite verification

Source: `RandomizedFinite.lean`
Namespace: `CoveringKernel.RandomizedFinite`
Source SHA-256: `54ef55ed2558f042c7abe3d577d728ade06f323eb4f9ea3434465f1c58d431ef`

## Compile evidence

Official Lean executable:
`private-locator:cb50f30cfa35bdf3a0cf`

Version: Lean 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release.

Mathlib: `private-locator:18d48e051fd31eaf177f` (read-only; no dependency edits).

`LEAN_PATH` consists of the closure directory, Mathlib's `.lake/build/lib/lean`,
and each dependency's `.lake/build/lib/lean`.

Command:
`lean -o RandomizedFinite.olean RandomizedFinite.lean`

Outcome: exit 0, empty stdout/stderr. `RandomizedFinite.compile.log` is empty
because Lean emitted no diagnostics. The compiled module is present.

A separate Lean `--stdin` process imported `RandomizedFinite` and ran
`#print axioms` for all ten theorems. Outcome: exit 0. Complete output is in
`RandomizedFinite.axioms.log`. Every theorem depends only on standard axioms
`propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx`, custom axioms,
`native_decide`, or trust-bypassing evaluator is used.

## Meaning and scope

- The finite AE intersection theorem requires only `[Finite W]` and an arbitrary
  measure. It imposes no event measurability assumptions.
- Extracting a coin outcome uses a probability measure to ensure the common
  conull event is nonempty.
- `exists_fixed_failure_not_ae_of_ae_cover` permits an AE cover by failures;
  the pointwise-cover and positive-measure results are convenient consequences.
- The numeric `1 / Fintype.card W` theorem uses finite subadditivity and
  `ENNReal.exists_le_of_sum_le`. It assumes `[Fintype W] [Nonempty W]`.
- Measures of arbitrary predicates mean outer measure. If the events are
  measurable, the numeric quantities are ordinary probabilities. The AE
  statements do not need those extra assumptions.
- `lower_bound_of_ae_cap` directly transfers a pointwise deterministic lower
  bound on some fixed member to a cap holding AE for each fixed member.
- No theorem promotes almost-sure success to success for every coin outcome.
  No theorem grants an adversary access to coins or requires coin-dependent
  instance selection in the final fixed-instance conclusion.

No commit, publication, or modifications to other source files were made.
