# Orthemology v5: adaptive recurrent closure and stable-support parity necessity

Fresh fifth-tranche composition of actual policy laws, recurrent graph geometry, matching-rival parity transfer and the executable target solver.

## Main necessity result
`stable_support_path_to_computed_target` proves that a common measurable seeded state-consistent Markov policy yields an internal path from its initial observed state to an executable computed target, under these explicit hypotheses:
- the same policy satisfies its actual hidden parity objective almost surely under every live model
- under the candidate model it always selects pairs from the supplied lawful pair set
- every candidate-positive successor of each supplied lawful pair remains positive in every live model

The theorem derives a nonempty actual recurrent end component, its zero candidate exit, its minimum-even parity for every full-row-matching rival, and the path from the initial state. It does not assume end-component structure, probability transfer, a winning certificate or the desired target conclusion.

`support_preserving_policy_path_to_target` replaces global support stability on every supplied allowed pair with the direct policy condition that its actually selected pairs are allowed and have zero candidate-exit probability almost surely. Filtering to those pairs discharges stability, and the target solver's own zero-exit filter proves that its returned target set is unchanged.

These are scoped stable/no-exit necessity theorems. They are not labeled the full support-changing hidden-parity iff.

## Actual arbitrary-policy recurrence theorem
`canonical_markov_recurrent_end_component` proves that under every common measurable private-seed policy using the complete observed action/state history, the exact recurrent pair set is almost surely nonempty, closed and strongly connected in the actual positive-support graph.

The proof works for arbitrary adaptive gaps and unbounded memory:
1. In the actual independent per-pair raw tape experiment, every positive-probability symbol recurs infinitely almost surely, by the second Borel–Cantelli theorem applied to proved independent product coordinates. Every sampled symbol also lies in its row's positive support.
2. The actual pair sample counter increases by exactly one at each selected occurrence. Infinitely many selections consume every deterministic tape index. The argument does not condition an iid estimate on a chosen random sample count.
3. Hence every positive successor of a recurrent pair recurs as a next source state. After transient pairs disappear, this gives closure of the recurrent pair set. Supported finite segments between recurrent sources give its actual directed strong connectivity.
4. The retained all-stack/canonical law equivalence transfers this conclusion to the genuine seeded adaptive Markov action/history laws. Source-state consistency is enforced by the actual policy wrapper and checked in the proof.

## Composition with parity and targets
The necessity proof selects a positive exact recurrent-set event, obtains its concrete end component from the new almost-sure theorem, and uses the retained proved safe relative-tail transfer for matching rivals. Almost-sure parity under a rival forces that event's recurrent minimum to be even. The normalized-row support adapter makes its graph the same-support graph, and the previously proved executable target equality supplies the computed target. A supported actual finite prefix supplies the initial-state internal path.

`ParityTailInvariance` also proves equality of recurrent sets after deleting any finite prefix and the actual minimum-recurrent-priority parity shift equivalence.

## Controls
`AdaptiveControls` uses a policy alternating between pairs. The third physical step consumes the second sample from its selected pair's tape; that receipt differs from the erroneous physical-time-indexed cell. The proof establishes that recurrent symbols are still observed through adaptive gaps. A disconnected self-loop graph rejects an unsupported alternating physical transition and is not accepted as strongly connected.

## Limits
- The lawful allowed-pair set is supplied. This packet does not compute or prove all-branch lower-support licensing, proper-support winning regions, or the outer state-region greatest fixed point.
- The stable-support hypothesis is explicit. The support-preserving corollary assumes candidate-zero-exit pairs are chosen almost surely; it does not infer that property merely from one positive-probability no-exit tail.
- The new residual-prefix conditional law work is separate and is not silently assumed here. Combining finite-prefix residual winning and support-changing region induction remains open.
- The separately proved uniform component operation gives the local sufficiency piece. Statistical navigation, testing, rejected phases and recursive policy synthesis remain open for the full observed-state parity iff.
- Prior controlled-iid coBüchi recursive controllers are not renamed or claimed to establish parity. Higher odd priorities may recur forever; no finite odd-visit-cost conclusion is asserted.
- Full observed action/state histories are retained. No hidden model label or priority value is exposed as extra feedback.

## Replay
`SOURCE_ORIGINS.json` binds exact inherited third-return sources and the separate fifth target, killed-law and recurrence candidates. Seven modules are newly authored in this packet.

    python tooling/replay_lean.py --root . --lean-bin /path/to/lean/bin --mathlib /path/to/mathlib4 --out /fresh/output --suites adaptive_parity_necessity --no-reuse

Use Lean 4.19.0 and Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b; output must be absent and outside the immutable packet. Every custom module is cold-compiled, every declared target gets exact type/axiom readback, and file census, source/import ownership and pinned dependencies are checked. Only propext, Classical.choice and Quot.sound are permitted. No proof holes, custom axioms, unsafe declarations or native_decide are introduced. The official installed object cache is trusted, not rebuilt from all upstream source.
