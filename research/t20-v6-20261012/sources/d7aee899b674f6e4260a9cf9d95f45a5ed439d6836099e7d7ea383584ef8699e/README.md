# Orthemology v5: verified hidden-parity target pruning

Fresh fifth-tranche research, 2026-10-01. This source packet proves and executes the finite target construction from the fourth research return. It does not supersede or modify any frozen predecessor or canonical source.

## Achieved statement
For a finite set of allowed state/action pairs, finite live-model set, finite observed-state type, normalized nonnegative rational full transition rows, a live candidate, and model-dependent natural-number priorities, the executable reference returns exactly the states contained in some zero-candidate-exit, internally closed, strongly connected component whose minimum priority is even for every full-row-matching live model. The returned pair components are exactly the maximal qualifying components.

The proof derives the central deletion invariant: matching an enclosing component implies matching every subcomponent; a qualifying subcomponent cannot contain a pair at the enclosing component's odd minimum. It also proves the graph union lemma needed to show that every maximal component intersecting a protected component contains it. All valid components survive every round. Recomputing components and matching rivals stabilizes after at most the initial number of retained pairs, independently of priority magnitude. Stable maximal components are valid. Preservation plus maximality proves the exact output characterization.

The executable finite reachability procedure is proved sound and complete against unbounded reflexive-transitive graph reachability. The executable pruning reference is proved equal to the abstract construction. The Markov adapter derives the internal successor graph from the same full rational transition table, selects allowed zero-exit pairs, and proves zero exit equivalent to internal probability mass one. For a live candidate, its internal successors equal its actual positive-support successors on these pairs.

## Exact scope boundaries
- The exhaustive maximal-component selector enumerates powersets. This is an exponential executable reference. The fourth return's polynomial SCC/MEC implementation and bit-complexity upper bound have NOT been kernel-verified here.
- The abstract `PruningKernel` works for a component family, but its union/nonempty properties are discharged for actual end components in `EndComponents`; they are not unproved assumptions in the end-to-end graph theorem.
- The abstract core permits arbitrary full-row values and a separately given successor graph. `MarkovSupportAdapter` closes that interface for normalized rational transition tables. Use a live candidate θ∈B for the intended hidden-model application; `noExit_internal_eq_candidate_support` explicitly takes that premise.
- Allowed pairs are supplied. Bottom-up support recursion, hard-menu licensing, proper-support winning-region computation, policy synthesis, sampling/concentration, all-history law transfer, and the almost-sure hidden-parity iff are NOT newly formalized by this packet.
- Parity means minimum priority recurring infinitely often is even. This packet verifies target construction, not infinite-run recurrence. No finite odd-visit-cost claim follows. Higher odd priorities may be essential to a qualifying component.
- CoBüchi is good=2/bad=1. `CoBuchiSpecialisation` proves both qualification and deletion specialize exactly to all-good and delete-bad conditions. The 0/1 alternative differs.
- This is a normalized finite-table mathematical input interface, not a validated external-file parser or production solver API.

## Source map
- `PruningKernel.lean`: independent match/minimum/validity predicates; finite maximal coverage, preservation, stabilization and exact output
- `EndComponents.lean`: actual directed graph closure/connectivity, union, target-state equality and disjoint maximal state sets
- `FiniteReachability.lean`: executable closure with soundness and completeness
- `ExecutablePruning.lean`: exhaustive executable MEC selector and full refinement proof
- `CoBuchiSpecialisation.lean`: general 2/1 specialization
- `MarkovSupportAdapter.lean`: normalized full-row/internal-support adapter and target equality
- `ControlTests.lean`: kernel-checked cascade, matching-rival, graph-split, full-row, coBüchi, higher-odd, empty and closure controls
- `AdapterTests.lean`: normalized-kernel controls including real revealing exits

Every declared source target, including definitions and instances, is listed in the replay registry and gets exact type and axiom readback. Permitted foundational axioms are only propext, Classical.choice and Quot.sound. There are no proof holes, new axioms, unsafe declarations or native_decide uses. Concrete theorems use ordinary decide and kernel proof reduction.

## Reproduce
Supply the exact pinned official external Lean/Mathlib installation. Do not write inside this immutable packet; choose a fresh absent output directory outside it.

    python tooling/replay_lean.py --root . --lean-bin /path/to/lean-4.19.0-linux/bin --mathlib /path/to/mathlib4 --out /fresh/output --suites hidden_parity_pruning --no-reuse

The driver validates the exact file census and hashes, source import closure, compiler binary, version, pinned tracked-clean dependency source revisions, and direct official import ownership. It cold-compiles every custom source, then reads back every declaration's type and axiom dependencies. The installed official object cache remains trusted, as in the environment-restoration addendum. No upstream source bootstrap is claimed.

## Baseline provenance
The mathematical starting point is the final fourth Library readback ZIP `Orthemology_v5_Fourth_Research_Return_20261001.zip`, SHA256 d0d3dffa3947bd06b101f267ef9cabeb559bd4e2d2ad4c3df7f80038307efd91, and its ordinary hidden-parity criterion/pruning review. Its report SHA256 is 38fd8b23e9ca286d80e1562080eb4fb376d473513674a24e46ae87ab20434938. These Lean modules are fresh successors, not a reconstruction of missing old imports. The replay driver/helpers are unchanged retained third-return verification tooling; their packet hashes make that boundary auditable.
