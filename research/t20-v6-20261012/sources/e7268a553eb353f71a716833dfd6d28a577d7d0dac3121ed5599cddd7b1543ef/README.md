# Orthemology v5: global hidden-parity necessity

This fifth-tranche packet proves the full support-changing necessity direction from a genuine common lawful almost-sure observed-state hidden-parity policy to an explicit finite support-recursive winning-region reference. It also proves that a negative computed result excludes any such common policy, uniformly over arbitrary measurable private seed spaces and unbounded observed histories.

The principal declarations are `HiddenParity.Necessity.winning_policy_mem_winningRegion` and `computed_losing_excludes_common_policy` in `GlobalParityNecessity.lean`. The contract in THEOREM_CONTRACT.md distinguishes the achieved direction from the open sufficiency/controller synthesis.

## Nine new modules
- StageTargetOrExit: exact positive support update and actual policy target-or-proper-exit dichotomy
- LawfulRestart: live history, explicit compatible-seed lawfulness and lawful posterior restart
- LawfulProbability: equivalence with zero actual illegal selection probability, including positive-history formulation
- SemanticWinning: genuine common seed/history policy, actual conditional-law winning restart and semantic region
- SemanticSafeActions: all-branch action safety derived from positive action/receipt histories
- HistoryStageSafety: actual licensing until the first support exit, and semantic target-or-exit composition
- RegionAlgorithm: executable finite reference, monotonicity, state descent stabilization, excess-fuel invariance and canonical-child fixed point
- GlobalParityNecessity: support induction, semantic postfixedness, global necessity and losing certificate
- RegionControls: exact executable semantic countercontrols and concrete arbitrary-policy impossibility

The nine newly authored modules are bound separately from inherited exact target, stochastic, recurrence, adaptive, and conditional-restart dependencies in SOURCE_ORIGINS.json. The earlier stochastic packet's phrase “not part of candidate-v1” refers to the earlier finite-target packet, not the present composite closure.

## Concrete controls
The executable controls check a revealing two-model branch with a losing alternative child, its two singleton children, a hard-menu dead successor, empty support, a winning recurrent 2/3 cycle, a losing recurrent 2/1 cycle, and excess-fuel invariance. The bad revealing branch also instantiates the real no-common-policy theorem, not merely a Boolean output test.

## Replay
    python tooling/replay_lean.py --root . --lean-bin /path/to/lean/bin --mathlib /path/to/mathlib4 --out /fresh/output --suites global_parity_necessity --no-reuse

Use the exact Lean 4.19.0 and Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b pins. Output must be absent and outside the frozen packet. All custom modules compile cold, all declarations are read back, and exact source/import ownership, file census and permitted axioms are checked. Official installed Mathlib/toolchain objects are trusted. No proof holes, custom axioms, unsafe declarations or native_decide are introduced. Proof-backed executable definitions may depend on the permitted standard axioms.

This is a necessary-condition solver with proved negative certificates. The converse, global synthesis and polynomial SCC substitution are not claimed in this packet.
