# Independent review: verified hidden-parity target pruning

**PASS_SCOPED: fresh independent kernel/source review and finite implementation checks.**

## Bound candidate and accepted subject

Candidate `candidate-v1/MASTER_MANIFEST.json`, SHA256 `df5debf8f034fe4f9c2647b8948ef3dfdc542b50e91f5774ed91d1c34e8f90e9`, contains eight fresh Lean modules. All eight modules were rebuilt from the full candidate in an empty reviewer build directory. Only pinned official dependency objects were used. No author custom object was imported into the replay.

The accepted mathematical subject is finite hidden-parity **target extraction**. Given normalized nonnegative rational full transition rows, a finite live-model set, a candidate model, a supplied finite allowed-pair set, a source state for each pair, and model-dependent natural priorities, the executable reference computes the states occurring in some qualifying zero-candidate-exit end component. Its underlying pair components are precisely the maximal qualifying components. For the intended hidden-model interpretation, the candidate belongs to the live set.

The proof is local to this finite target construction. The allowed-pair set is not proved to be the result of hard-menu/all-successor licensing, support recursion, or the outer winning-region fixed point. There is no newly formalized common-policy stochastic iff, observation-law coupling, statistical sampler, infinite-run recurrence, or policy compiler in this candidate.

## Exact Lean assumption boundary

- The abstract kernel needs decidable equality on `Pair`, finite sets `U : Finset Pair` and `B : Finset Model`, an arbitrary `row : Model → Pair → Row`, priorities, a candidate, and the explicit component-family nonempty/union laws. Neither `Pair` nor `Model` needs a global `Fintype` instance.
- The graph specialization supplies the component-family laws from a source map and finite successor sets. The executable refinement additionally needs a finite enumerated state type and decidable equality on states, pairs and row values.
- The normalized adapter replaces arbitrary row values with full finite rational rows carrying nonnegativity and normalization proofs. Its `markovTargetStates_exact` statement itself does not require `theta ∈ B`; that premise appears explicitly in `noExit_internal_eq_candidate_support` and is required for the intended live-candidate stochastic interpretation.
- Empty `B` is allowed by the generic formal statement and makes the matching-model parity requirement vacuous. No default action, inhabited action type, seed space or probability law is manufactured by the construction.

## 1. Independent semantic definitions

`Match` compares complete supplied row values on every used pair. In the normalized adapter those values are entire functions from successor state to rational probability. It does not compare only an internal coordinate or a row conditioned on no exit.

`IsMinimum` requires both an attained priority and a lower bound on every used pair. `Valid` requires a component and an even minimum for every model in the finite live set that matches the candidate on that component. Thus the conclusion is not built into the pruning predicate.

The abstract `ComponentFamily` carries nonemptiness and union under pair intersection. Those are explicit graph hypotheses at that layer. `IsEndComponent` independently requires a nonempty finite pair set, nonempty successor sets for each used pair, closure in the used source-state set, and ordinary directed reflexive-transitive reachability between every two used states. Its union theorem is proved when two components share a state, which discharges the weaker pair-intersection property needed by the abstract kernel. The end-to-end graph theorem has no assumed parity-preservation or MEC-correctness premise.

The zero-length reachability convention does not allow dead singleton components: nonempty successor sets and closure are separate requirements. The source map need not be injective, so multiple actions at one state are represented correctly.

## 2. Deletion invariant and global containment

If a rival matches an enclosing component D, it also matches every subcomponent E. Suppose its minimum on D is odd d. A valid E contained in D cannot contain a priority-d pair: d is then also attained on E, no smaller priority occurs there, and its minimum would be odd. `valid_avoids_odd_minimum` proves this directly from the independent definitions.

A subtle global point is handled rather than assumed. A pair of protected E might be considered for deletion by a different current maximal component F. Since E and F share that pair, their union is a component inside the current retained set. Maximality forces the union to equal F, hence E is contained in F. The odd-minimum argument therefore applies to every possible deletion witness. This is the role of `component_subset_of_intersects_maximal`, not merely the simpler existence of some covering MEC.

Finite cardinal maximization proves every component is contained in a maximal one. Combining coverage and the exclusion argument proves every valid component survives an entire round, including removal of pairs outside all current MECs.

## 3. Recalculation, termination and exact maximality

Each round recomputes the maximal components, row-matching rivals and their minima using the current pair set. Removing a discriminating row can create a newly matching rival; removing one odd layer can expose another odd minimum. The definitions preserve that dependence at every iteration.

Every step is a subset of its input. If a step is not fixed, its cardinality strictly decreases. Induction gives stabilization after at most the original number of retained pairs. The bound counts possible strict pair deletions; it does not iterate numerically through priority values. The reviewer has a kernel-checked three-pair all-odd example where two rounds leave an invalid singleton and the third round removes it, so reducing the bound by one is not generally sound.

At a stable set, every maximal component is valid: an odd matching-model minimum would furnish a concrete removed pair, contradicting stability. Preservation places every original valid component inside the stable set. A returned component cannot have a strictly larger original valid extension, since that extension would also survive and contradict its graph maximality. Conversely, every original maximal valid component is contained in a returned valid component and hence equals it. The resulting iff is inclusion-maximality, not maximum cardinality, policy optimality, or a probability/cost optimum.

The state-target equivalence includes nonmaximal valid components by coverage. Distinct returned components have disjoint used-state sets: any shared state would yield a larger graph component in the final retained set. No false general monotonicity of parity validity under arbitrary deletion or enlargement is used.

## 4. Executable refinement

`FiniteReachability.reachable` grows a finite reached set for a fixed cardinal fuel. Every added vertex has a genuine finite directed path. Cardinal stabilization makes the final set edge-closed, so induction on an arbitrary reflexive-transitive path proves completeness. The executable end-component check is then proved equivalent to the independent graph definition.

The executable MEC selector enumerates the current powerset and tests maximality over that powerset. Its equality to the abstract finite maximal-component selector is proved. The executable step, iteration, output and target-state union are each proved equal to their abstract counterparts. Thus the finite program is actually connected to the theorem, rather than being a separately tested implementation with the same intended name.

This is an **exponential exhaustive reference** in the retained pair count. It is not a kernel qualification of a polynomial SCC/MEC implementation or the fourth ordinary theorem's global bit-complexity bound. The generic row equality instance has no supplied complexity guarantee. Under normalized finite rational rows it is a concrete finite comparison, but that does not turn powerset enumeration into a polynomial algorithm.

## 5. Normalized row/support adapter

`RationalKernel` includes proofs of nonnegativity and finite row sum one. `internalSuccessors` consists of exactly those outcomes positive under every live model. The reviewer additionally proves in Lean that this is equivalent to the exact filtered live-support update being the entire old live set.

`NoExit` requires every positive candidate successor to be internal. The adapter proves this is equivalent to candidate probability mass one on the internal successor set. Normalization and nonnegativity, including the zero-mass complement argument, are used explicitly. Consequently a no-exit pair has at least one internal successor. Full-row matching transfers no exit to every matching model.

For a live candidate, the internal successors on a no-exit pair equal the candidate's actual positive support. The live-candidate premise matters: a reviewer countercontrol takes a deterministic candidate excluded from a singleton live set whose model has two positive outcomes. No exit still holds, but the internal set contains an extra state. The author's equality theorem correctly requires candidate membership. Its more generic target equivalence remains valid even without that premise, with its purely stated definitions.

The adapter filters the supplied allowed pairs by no exit, uses the same rational rows for matching, and proves the original explicit `MarkovQualifying` predicate is equivalent to the graph-kernel predicate on that filter. `markovTargetStates_exact` follows by the verified executable target theorem. A reviewer assembly theorem also checks the README's maximal-qualifying-pair endpoint directly from these two adapters.

Exact zero probabilities are input facts. A reviewer fixture changes a normalized row entry from zero to one millionth and changes the zero-exit/target result. No finite observed absence of an outcome certifies the zero case. The proof-carrying normalized table is not a validated arbitrary JSON/Python-object parser. An empty state type cannot support a normalized row for an actually supplied model/pair; vacuous dimensions do not create a stochastic controller.

## 6. CoBüchi and infinite-objective boundaries

The general coBüchi specialization is proved with good priority 2 and bad priority 1. An even minimum on a nonempty pair set is then equivalent to every pair being good, and the odd minimum layer is exactly the bad pairs. These are universal qualification/deletion equivalences, not only concrete tests.

A component with recurrent priorities 2 and 3 is valid and can require both pairs for graph closure. Removing every odd pair is unsound, and parity success does not imply a finite count of odd-priority visits. Priority 0 for good and 1 for bad encodes a different objective. The candidate establishes no infinite recurrence/fairness statement: the fourth ordinary stochastic theorem requires full-pair recurrence in a permanent operating component, which cannot be inferred merely from remaining inside it.

## 7. Foundations and execution trust

The cold replay uses Lean 4.19.0, binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, and Mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The replay verifies exact custom source identities, import closure, pinned tracked-clean official sources, direct official import ownership and every registered declaration's type and axiom dependencies.

Only the standard foundational axioms `propext`, `Classical.choice` and `Quot.sound` appear. There are no `sorryAx`, custom axioms, unsafe declarations or `native_decide` proof shortcuts. Even the executable top-level definitions report some standard axioms through proof-backed decidability. They are executable after proof erasure; they are not advertised as axiom-free definitions. Operational finite tests use concrete Fin types and computable instances; executing a caller-supplied noncomputable enumeration or equality oracle is outside those tests.

The installed official object cache is explicitly trusted. This is a cold custom-source rebuild against pinned dependencies, not a fresh source bootstrap of Lean and all Mathlib objects. Native evaluations are finite tests; ordinary `decide` controls are kernel-checked propositions. Those evidence types remain separate.

## 8. Review findings and limits

The reviewer did not author or edit the candidate proof. There was pre-freeze coordination about scope and the row/support interface; this is a separate-source independent replay and adversarial review, not a claim of blinded review. No author source correction was required in candidate v1. The row/support application interface raised during the initial four-module read is closed by the separately added normalized adapter in the full immutable candidate. Hard-menu licensing remains an explicit external input, as the README states.

The first reviewer attempt at a very small rational fixture encountered opaque library arithmetic under `decide`; its failing log is retained. Replacing the fixture's computed rational subtraction with explicit reduced rational constants, while proving the same numerical values and normalization, resolves proof reduction without a trusted native shortcut. This is reviewer test construction, not an author theorem defect.

The final receipt records all replay counts and exact source identities. Finite comparisons and mutations do not establish stochastic necessity/sufficiency, polynomial runtime, or historical novelty. Any later stochastic bridge requires a separate immutable candidate and review.

## 9. Final evidence census and replay

The qualified combined run passed:

- Eight fresh candidate module builds and 148 exact type/axiom readbacks
- Two fresh reviewer modules and 32 reviewer theorem readbacks, including the explicit support-update and normalized maximal-component assembly endpoints
- 4,096 generic finite executions compared with direct exhaustive valid-component maxima and independent Warshall graph closure; every four-pair/two-state directed support tuple appears in the corpus
- 512 normalized rational-table executions compared with the independently derived exact internal supports, zero-exit filter and exhaustive target oracle
- 1,509 independent finite baseline cases; nine semantic shortcut alternatives each refuted by a stored counterexample
- Five altered-core source builds rejected with affected sources rebuilt and only hash-checked unaffected reviewer-fresh objects reused
- Six separately authored false-proposition controls freshly replayed and rejected by ordinary kernel `decide`

The five core mutations change an odd deletion layer to even, remove one iteration of fuel, force zero reachability fuel, replace intersection of live-model supports by a union, or swap the coBüchi encoding. These are source-proof rejection controls. The nine independent semantic alternatives and the six authored false-proposition controls provide separate concrete semantic evidence; the counts are not combined into a misleading single independent corpus.

`evidence/qualification/RESULT.json` binds the qualified run, and its nested cold receipt binds the candidate/compiler/dependency identities. The exact current reviewer source matches the copied source compiled in that run. All eight author modules remain byte-identical to the supplied immutable candidate. The source-only packet contains the current replay scripts, proof sources, generated finite corpora, logs and predecessor scope references; it contains no custom compiled objects.

Run `python checks/verify_packet.py` for exact file identities, then `PYTHONDONTWRITEBYTECODE=1 python checks/replay_review.py --env /path/to/restored/environment --out /fresh/absent/output`. The environment directory must contain the pinned `toolchain/lean-4.19.0-linux/bin` and `mathlib4` paths. A sealed packet requires replay output outside itself. No installation, network access or author object cache is required; the pinned official object cache remains the stated dependency trust boundary.
