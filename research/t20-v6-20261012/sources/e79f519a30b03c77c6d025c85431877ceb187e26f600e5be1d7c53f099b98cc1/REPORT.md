# Independent review: conditional phase stabilization

## Verdict and source binding

**Accepted as a deterministic conditional arithmetic supplement.** All five author theorems are sound at their stated interfaces. They supply a useful stabilization step for a controller proof after the caller establishes the required transitions.

The exact author manifest is `41e68181104c0734066fc0dd8335d6f7e22f7d3f6ec0772a2fa7de8db261cd0e`; author archive SHA-256 is `59af1e72d1f4faaef533fac088eb3a3b1883949b18aeb1a31b75427005b52266`. The sole new source, [PhaseStabilization.lean](../../../../experiments/orthemology-v5-continuations/source-store/b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183.lean), has SHA-256 `b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183`. This verdict is independent of, and separate from, the empirical-row review.

## Checked argument

The bounded monotone-tail lemma chooses the greatest **attained** natural value, then uses monotonicity and maximality to establish constancy. It does not assume the upper bound itself is attained.

The cycle barrier is derived from the retained `cycleAction` and `Fintype.equivFin` definitions. Membership of the designated model gives a nonempty finite menu. The selected cycle index exceeds any requested bound. The proof does not assume an enumeration order or a surjectivity axiom.

The phase theorem selects such a barrier above both the initial tail phase and the rejection threshold. Zero/one increments cannot cross that barrier once increments are forbidden there. Induction therefore bounds every future phase, and monotonicity yields constancy. The controller's zero/one increments and non-rejection premise must be proved independently; neither is smuggled in as an almost-sure conclusion.

The option-valued result needs no finite mode type: either no mode ever appears after the cutoff, or one appearing mode persists forever. The combined theorem takes the maximum of the phase-constancy cutoff and the retention cutoff. That supplies the unchanged-phase guard required for mode persistence.

## Verification

The [compositional receipt](../../PUBLIC_BOUNDARIES.md#recovered-reference-140) records **one fresh author module, one fresh eight-probe reviewer module, 30 reused qualified dependencies, and 369 exact declaration/axiom readbacks**. This is not a fresh 31-module cold closure. Each reused dependency is bound by source hash, object hash, and transitive source fingerprint to the completed independent target70 cold run, whose retained receipt is included. Its input manifest is `50e6a8ccec70ac8737b9cfef91def37570a660a56397ed46451b69c9151a1741`. No extra reviewer object from that other build was admitted. Official Mathlib caches remain trusted.

The [eight independent Lean probes](../968f2bb2fa71eba291ca4049fd685d9cd6982aeffd3c2ad950c422a9ff3ebd6b/IndependentPhaseProbe.lean) formally check the important non-conclusions using the actual retained cycle enumeration. A two-step sequence can skip the designated model forever, a bounded oscillation can fail to stabilize without monotonicity, and a changing present mode can fail without retention. A constant wrong-model phase and permanent absent mode satisfy the actual interface. Unit increments can occur arbitrarily late in physical time. The first reviewer probe pass exposed a missing natural-number binder annotation; the corrected probe and unchanged author source pass in a separate output, preserving the failed attempt as reviewer development evidence.

The [independent finite graph controls](../../PUBLIC_BOUNDARIES.md#recovered-reference-139) pass **120,394 assertions** across permuted finite cycles, reachable barrier graphs, persistent-mode graphs, and boundary controls. The author's distinct 120,305-assertion output replays identically. Finite graph tests corroborate the formal arguments; they do not prove infinite stabilization on their own.

## Exact limits for the global composition

- Eventual constancy of the phase does not establish that its selected model is the true model; a wrong model can remain forever if nothing forces its rejection
- The retained mode may remain `none` forever; reaching a permanent target mode requires an additional argument
- The arithmetic result contains no probability measure, row-learning theorem, fairness theorem, lawful-policy construction, support recursion, or parity-winning conclusion
- The caller must establish that support changes, resets, or multi-step phase jumps cease before using the unit-increment tail theorem
- No deterministic upper bound on physical stabilization time or finite-time certificate of permanent constancy follows

These boundaries are accepted scope, not defects in the five claims. The supplement's intended use is conditional composition with separately verified controller transition and statistical facts.

## Replay

Run `python -B replay_compositional.py --qualified <independent target-policy review directory> --environment <pinned environment directory> --out <fresh absent output>`. The script verifies the target70 terminal receipt, exact source manifest, all selected source/object hashes and transitive fingerprints, and only then compiles the new source and probes. A full 31-source cold replay is also possible through the bundled author driver, but was not the check claimed here. The later global-controller closure may check the combined source graph once without changing this compositional receipt's meaning.
