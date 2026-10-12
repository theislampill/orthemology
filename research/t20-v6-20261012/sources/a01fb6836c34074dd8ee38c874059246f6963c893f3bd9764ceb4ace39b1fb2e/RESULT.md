# Synchronous guarded exact-support saturation: Lean verification

9 October 2026. Verification of the already written theorem in `source-sensitive-proof-compilation-20261009/RESULT.md`. No original-discovery, source-truth, metaphysical-warrant, adoption, integration, closure or historical duration claim.

## Checked result

The new Lean development defines an actual numeric-table update from the all-unreachable table and proves its semantics by induction on the number of synchronous rounds. It does **not** define round h as the minimum over height-h proof trees.

For a fixed grammar with finite rule labels, finite ordered rule arities, arbitrary fixed guards on ordered exact premise supports, finite local supports, and rational additive occurrence prices:

1. At round h, each reachable `(judgement, exact support)` entry is exactly the attained minimum price among valid trees of height at most h. Every numeric entry has an actual valid tree witness at that height. An unreachable entry means no such tree exists.
2. With finite judgement labels and nonnegative local prices, round `H = |J| (|B| + 1)`, where B is the finite union of all rule-local supports, gives the global minimum among all valid finite trees in each exact state. All later numeric tables are identical. Ambient evidence E may be infinite.
3. If E is finite, the originally stated bound `|J| (|E| + 1)` is also verified.
4. Equality of the entire numeric table at consecutive rounds implies permanent stability and, under the preceding finiteness/nonnegativity assumptions, global correctness. Equality of reachable-key sets alone is insufficient; a checked counterexample has unchanged keys but a price drop from 10 to 1.

Only the stabilization transfer requires nonnegative prices and finite J. Bounded-height correctness holds for arbitrary rational local prices and does not require finite J.

## Actual recurrence

A table is a function from a judgement and an exact finite support to `Option ℚ`: `none` means unreachable and `some c` records a finite price.

`Candidates.lean` constructs a finite rule-choice type consisting of a rule label and an ordered tuple of premise supports drawn from B's powerset. An enabled choice requires every relevant old-table entry to be reachable and the rule guard to hold on that exact ordered tuple. Its output support is the rule-local support union all premise supports. Its price is the rule's local price plus the sum of the old-table premise prices. Each occurrence is charged independently, including repeated equal premises.

For each exact head/support key, `candidates` is the union of the old entry, if present, and these enabled rule prices. `minimum` returns the least member, or `none` for the empty set. `step` uses that finite minimum at each key. `round` is primitive recursion: all `none` at zero and `step` of the preceding table at every successor.

The candidate generator does not examine proof trees. The finite grammar-support restriction drops no reachable premise state: `round_mem_candidates_iff` proves that, on generated tables, membership is exactly old-value retention or a guarded rule candidate over **any** ordered tuple of reachable supports. There is no intermediate support-inclusion Pareto pruning.

The recurrence is classical/noncomputable. Arbitrary Prop-valued guards do not supply a decision procedure. Finite enumeration and mathematical minimum selection alone do not certify an executable compiler.

## Why the proof is not definitional

`Saturation.lean` introduces a separate `Correct D h` invariant with two independently proved directions:

- Every `some c` entry has a valid height-h tree with precisely that judgement, support and price.
- Every valid height-h tree has a reachable table entry no dearer than its price.

`candidate_sound` assembles actual child witnesses from the preceding table. Equality of every premise support preserves the arbitrary ordered guard, and union and sum give the candidate's exact support and price. Retained candidates keep their prior witnesses.

`candidate_complete` decomposes an arbitrary height-(h+1) tree, replaces each child by its no-dearer old-table exact-support minimum, and proves that the generator includes the resulting candidate. It uses the actual recursive validity, support and cost definitions of the unchanged predecessor grammar.

`step_correct` combines those results with finite minimum selection. `round_correct` is an induction from the impossible height-zero tree case. `round_some_iff` and `round_none_iff` then establish exact minimum and reachability semantics.

`Stability.lean` applies the frozen bounded-representative theorem to arbitrary finite competitors, giving `round_global`. Two globally correct numeric tables are extensionally equal (`global_unique`), yielding `round_stable` and `step_fixed`. The earlier-stopping theorem separately uses determinism of the successor recurrence. The bound was established by predecessors; this package claims verification credit for the recurrence increment only.

## Theorem map

- `mem_candidates_iff`, `step_some_iff`: actual finite update characterization
- `candidate_sound`, `candidate_complete`, `step_correct`: one-step witness and minimum preservation
- `round_correct`, `round_some_iff`, `round_none_iff`: height induction, actual bounded witnesses, exact minima and unreachability
- `round_global`, `round_stable`, `step_fixed`: unrestricted minima and stability at the grammar-local bound
- `round_global_uniform`, `round_stable_uniform`: finite ambient-evidence bound
- `early_stopping`, `early_stopping_global`: complete-table stopping condition
- `round_retains`: reachable keys persist and retained prices cannot increase
- `round_mem_candidates_iff`: no reachable tuple is excluded by the finite support enumeration

## Controls

`Controls.lean` checks genuine rule-tree grammars:

- A sole unary unsupported self-cycle never becomes reachable in any round.
- An allowed nullary base enters at round one; an additional zero-price self-cycle preserves its zero minimum at every later round.
- A false nullary guard prevents any seed at any round.
- A nonnegative-price grammar seeds both judgement keys at round one and has identical reachable keys thereafter, but one price falls from 10 at round one to 1 at round two. This refutes key-only stopping.

Three fresh expected-rejection checks also fail for the intended logical/type reasons: claiming an unsupported cycle seeds a key, equating the 10 and 1 prices despite equal key sets, and removing the guard check from the actual candidate generator. These are negative controls, not accepted proof sources.

The general theorem covers nonmonotone and position-sensitive guards without additional assumptions. The predecessor's independently checked support-shrink, premise-reversal and nonmonotonicity controls remain unchanged; they are not reclassified as newly implemented controls here.

## Verification and trust

`replay.sh` recompiles five unchanged frozen dependency sources and four new modules with the installed Lean 4.19.0 toolchain and warnings treated as errors. The mathlib checkout is the unchanged pinned predecessor environment; no installation or download is required. Fresh receipts, source bindings, predecessor-preservation verification and independent internal semantic review accompany the final package.

Major theorem/control axiom reports use only `propext`, `Classical.choice` and `Quot.sound`. No admitted theorem, custom axiom, native-evaluation proof or `sorryAx` is accepted in the delivered sources. Failed intermediate development logs are not final verification evidence.

## Limits

No Python implementation correspondence, extracted executable witness algorithm, decidable arbitrary guards, efficiency bound, worst-case sharpness proof, arbitrary real prices or DAG-cost result is established. The table stores numeric prices; actual tree witnesses are established existentially, not returned by an executable witness-pointer implementation.

Correct rule admission, faithful judgement scoping, fixed metadata, source authenticity, substantive guard soundness, and applicability to philosophical or theological arguments remain outside the formal result. It does not prove unrestricted provenance-changing cut or certify the full FABLE calculus. Predecessor terminal-frontier results remain separate and unchanged.
