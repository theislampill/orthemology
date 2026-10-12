# Executable guarded exact-support numeric compiler

9 October 2026. A new executable representation and correspondence construction, using the unchanged earlier guarded saturation and minimum-attainment mathematics. No discovery credit for those inherited theorems, integration, acceptance, owner closure, retrospective duration, or semantic/source-warrant claim.

## Established

`Executable.lean` and `FiniteTable.lean` supply ordinary computational Lean definitions for an ordered guarded candidate generator, rational minimum update, and materialized finite table compiler. They are not aliases to the predecessor's noncomputable recurrence. The compiler stores a finite set of exact `(judgement, support, rational price)` rows, using old-table reads synchronously at each step.

The kernel proves:

1. The executable generator enumerates every predecessor rule/support tuple and produces exactly the same candidate prices (`mem_choices`, `candidates_eq`).
2. The executable update and functional recurrence equal the unchanged predecessor update and every round (`step_eq`, `round_eq`).
3. Reading the actual materialized table equals that same predecessor round at **every** key, including supports outside the enumerated grammar universe (`compile_round_eq`).
4. Row membership itself equals a predecessor numeric entry (`mem_compileRounds`). Consequently each exact key has at most one price (`row_unique`); equality of the lookup is not concealing multiple stored prices.
5. With nonnegative local prices, the executable run at the inherited bound `|J| (|B|+1)` is globally correct, where B is the finite union of rule-local supports (`compile_correct`). Its numeric values are attained by valid finite trees and no valid competitor is cheaper. Both the entire stored row set and its lookup are stable thereafter (`compile_rows_stable`, `compile_stable`).
6. Equality of full consecutive stored tables transfers to global correctness (`full_table_stopping`). Equality of key sets alone is not used.

The bounded-round correspondence permits arbitrary rational local prices. Nonnegativity enters only the global minimum/stopping transfer through the inherited pruning theorem.

## Executable inputs and representation

Running the definitions requires actual executable values for:

- the fixed grammar's arities, ordered premises, heads, local finite supports, and rational prices;
- a `Fintype R` enumeration of rule labels and, for materialization, a `Fintype J` enumeration of judgement labels;
- decidable equality on judgements and evidence tokens;
- a function producing `Decidable (G.guard r s)` for every rule and ordered support tuple.

The theorem is generic over those inputs. It does not synthesize an algorithm for arbitrary Prop-valued guards or make a noncomputably supplied grammar/instance executable. The concrete control grammars supply executable definitions and guard decisions; Lean successfully code-generates and runs them. `E` need not be finite: all delivered examples use `Nat` evidence with finite local supports.

The predecessor's noncomputable `Fintype (RuleChoice G)` instance is deliberately bypassed. `choices` explicitly constructs a finite dependent sum over rule labels and a finite Cartesian product of the grammar-support powerset at each ordered premise position. A nullary rule has its one empty tuple. Membership completeness is proved independently before equating this enumeration with the predecessor's universal finite set.

The executable minimum uses decidable finite-set nonemptiness and rational order. `materialize` enumerates judgement/support keys and writes only reachable rows. `compileStep` reads a finite prior table and computes a fresh finite table; `compileRounds` recursively applies this from the empty table. `compile` performs exactly the inherited number of rounds. It does not enumerate proof trees. There is no intermediate support-inclusion Pareto pruning, floating-point rounding, unordered-premise encoding, DAG sharing discount, mutable guard, or external guard service.

## Kernel proof versus execution

Universal correspondence is kernel checked. Its proof may use the unchanged classical predecessor results and standard axioms (`propext`, `Classical.choice`, `Quot.sound`). The executable definitions themselves are ordinary `def`s outside classical sections. They compile without declaring noncomputability and without unsafe definitions or evaluator-based proof axioms.

`Controls.lean` separately runs actual `#eval` probes and 17 assertion-style runtime checks. `Main.lean` calls the same checks through `lean --run`; each failure throws an error, so the replay exits unsuccessfully on a mismatch. These observed executions are regression evidence, **not kernel proofs of the printed rational numerals**. No `native_decide` or similar native-evaluation theorem is used to bridge this distinction. Early development attempted kernel reduction for concrete controls; those failed attempts are preserved in development logs and are not accepted evidence.

Observed controls include:

- unsupported unary cycle: `none`;
- allowed nullary seed plus zero-price cycle: `some 0`;
- blocked nullary guard: `none`;
- ordered supports `{0}`, `{1}` with rational occurrence prices: `some 1`;
- two equal child-support occurrences: `some (7/6)`, charging both occurrences;
- reversed ordered guard: rejected;
- tempting cheap empty support retained alongside a dearer required exact support; the guarded conclusion cannot be obtained at empty support;
- identical reachable key sets with price 10 at round one and 1 at round two, and unequal full tables;
- complete row-set equality beyond the inherited bound;
- a negative-price cycle lowering 0 to -1, consistent with bounded correctness and showing why global stabilization needs nonnegativity;
- an unused external evidence token: unreachable.

Three expected-rejection mutations target actual code: dropping the source guard, excluding nullary rules, and dropping child occurrence costs. Their correspondence/completeness proofs fail with unsolved goals. They are rejected sources, not accepted proof dependencies.

## What is new and what is inherited

New construction: an executable finite candidate enumeration with proved completeness, executable rational update, materialized finite row representation, all-round full-domain correspondence, exact row membership/uniqueness, concrete runtime controls, and transfer to executable-table stability/stopping.

Inherited unchanged: valid guarded proof-tree syntax and costs, equal-state replacement/pruning, height bound, existence of bounded representatives and minima, the classical numeric recurrence and its height-inductive semantics, and its global stabilization mathematics. Frozen copies are source-identical and freshly rebuilt in this new directory. Predecessor files are never rewritten.

This is an executable **numeric** compiler. A stored price has a valid proof-tree witness by the kernel correspondence and inherited theorem, but no proof tree or reconstruction pointer is returned by this implementation. It is not a correspondence theorem for the earlier Python compiler or a complete proof-certificate serializer. No efficiency improvement, benchmark claim, worst-case sharpness, arbitrary-real-price implementation, or performance campaign is claimed.

Source authenticity, faithful rule admission, substantive guard soundness, psychological/metaphysical semantic adequacy, and applicability to a particular argument remain outside the formal result.

## Reproduction

Run `./replay.sh` in the existing pinned Lean 4.19.0/mathlib environment. It freshly compiles eight unchanged dependency sources and four new modules, treats warnings as errors, executes the checks in `#eval`, and invokes them again through `lean --run`. Run `./check-mutations.sh` for expected-rejection controls. Neither script installs software or accesses a network.

`BINDING.json` identifies frozen sources. `PREDECESSOR_HASHES.json` records predecessor baseline bytes. Final verification, independent internal semantic/code review, preservation, and content hashes are recorded in `CHECK_RESULTS.json`, `REVIEW.md`, and `MANIFEST.json`. Development logs are historical debugging records only.
