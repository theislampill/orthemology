# Final independent Lean source and kernel replay review

Result: PASS. No source/statement mismatch or mathematical defect found within the scope below.

Reviewed source: `[OMITTED_PRIVATE_MACHINE_PATH]

SHA-256: `2f8b4df91a832fb3d656ee9d854b7a5d625236ecc127588bc574d051c4b2cf73`.

A byte-identical frozen copy was compiled independently in this review directory using Lean 4.19.0, `-t0`, and `-DwarningAsError=true`. Exit status was zero. The original source and its parent directory were not modified. Build products are confined to `lean-replay/`; inherited toolchain and mathlib are dependency inputs.

The five printed results, including `exact_steiner_cost` and `character_gate`, report only `propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx` or custom axiom is present in these dependency lists. Source inspection found no admitted proof or substituted optimum premise.

## Semantic source review

- `Grown Adj T` generates precisely finite nonempty connected vertex sets for symmetric adjacency. Each insertion attaches a previously absent vertex to an existing vertex, so generated sets are connected. Conversely, any finite connected induced subgraph has a rooted spanning-tree order, giving a `Grown` derivation. This semantic equivalence was independently checked in the source review; the file does not separately prove an equivalence against mathlib's `SimpleGraph.Connected` predicate.
- `Run.add` toggles an inactive adjacent slot into the mask. Its premises force the active source and new slot to be distinct.
- `Run.remove` toggles an active adjacent slot out of the mask and explicitly requires source and target to differ. The source therefore remains active, preserving mask nonemptiness.
- The second finite set records the union of visited slots: additions insert into it, removals and idles leave it unchanged. `active_subset`, `visited_grown`, and `visited_card_bound` enforce the relevant invariant and lower bound.
- `Run.idle` is deliberately an unconditional, unlabelled no-op. On an edgeless graph it is not a literal elementary gate. This does not change the up-to-horizon optimum: delete idles from any run, and the remaining add/remove moves are legal physical mask transitions of no greater length. The constructive synthesis proof itself uses no `idle` constructor. Exact positive word lengths without an identity command remain a separate convention.
- `SteinerMinimum` is defined solely by finite connected supersets and cardinality minimality, independently of `Run`; it does not assume the desired gate optimum. `exact_steiner_cost` is correctly conditional on this ordinary minimum witness and proves both attainment and global optimality over all roots and runs.
- The formal theorem permits a general vertex type and symmetric adjacency; it does not require global finiteness. This strengthens the finite-graph result for target sets having a finite minimum witness. Existence of that witness is a premise, not separately constructed by this file.
- `character_gate` proves the actual pointwise finite-product identity for `Function.update x i (x i * x j)` in a commutative monoid, assuming the relevant coordinate squares to one. This specializes to sign-valued Walsh characters. It is not merely an assumption of the mask rule.
- `character_gate` imposes no adjacency or distinctness premise because its algebraic identity is valid more generally. Its application to `Run` uses only the allowed off-diagonal adjacent gates. For simple graphs there is no mismatch.

## Exact kernel boundary

Kernel checked: visited-set bound, constructive synthesis, minimum run length under a connected-superset minimum premise, reachability versus connected supersets, and the local observable pullback identity.

Not claimed kernel checked by this file: a packaged correspondence theorem for whole physical gate sequences and `Run`; equivalence of `Grown` to a separately imported graph-connectivity predicate; continuous encoder dimension; topology/invariance of domain; probability-simplex moment geometry; finite-horizon Walsh dimension counts; disconnected component marginal characterization; or the tree saturation corollary. Those remain written arguments or independent finite checks. Their exclusion is consistent with the stated review scope.

## Replay records

- Frozen source: `lean-replay/GraphContinuation.lean`
- Replay script: `lean-replay/replay.sh`
- Successful output: `lean-replay/kernel.log`
- Dependency path output: `lean-replay/inherited-lean-path.txt`
- Machine-readable hashes and result: `lean-replay/binding.json`

Inherited mathlib commit: `c44e0c8ee63ca166450922a373c7409c5d26b00b`.
