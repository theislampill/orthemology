# Independent review: stochastic exact inquiry

10 October 2026 UTC. **PASS_SCOPED, ordinary mathematics and exact executable controls.** No blocking defect remains in the reviewed finite fixed-kernel stopping theorem, its support algorithm, or the stated source-audit application. This is not kernel verification, empirical source calibration, philosophical warrant, general hidden-parity closure, scientific acceptance, repository integration, or T20 closure.

## Exact subject and review status

The accepted report is `snapshot/stochastic-exact-inquiry-20261010/RESULT.md`, SHA-256:

`5a6983eaeadb281736db29657b73145337e7194a2ceec017d436acb3d8d1ff7a`.

Accepted solver SHA-256:

`1f57b5053850190c5c9330ad01886610883d875ddc1935017ccb19bbb46f7135`.

Accepted input ledger SHA-256:

`849bbab790dd5a2b8284eaf868c2277940e441e2cce50eb35e872095725c5fa7`.

The complete snapshot bindings include the other tested code, author controls, source manifest, and exact copies of all ten bound inherited inputs. The author's manifest correctly records that independent review was pending when that author snapshot was frozen. This separate review supplies the subsequent scoped verdict; the frozen author manifest has not been rewritten.

The entire accepted report and solver were read. The review inspected the complete retained PD review, the relevant historical and controlled-restoration material, H-ICS's full labelled-belief theorem and destructive example, H-Continuation Theorem 2 and its proof, and the actual finite source-audit construction. The external primary comparison was the definitions and complete allowed-action/product-chain argument in §4.2 of arXiv:1411.3880v1. This is a bounded source comparison, not a corpus-wide absence proof.

## Mathematical checks

### 1. The target is initial-label knowledge in the stipulated sense

Augmenting a changing physical state with the immutable answer label is necessary. Two equal physical sinks with different initial labels remain distinct model states. Homogeneous support is exactly the zero-error reporting condition because every state of a finite feasible posterior support has strictly positive conditional mass. A mixed-support finite stopping event with positive probability therefore creates an error under at least one live initial label. Independent controller randomness cannot secretly select the correct label: its seed is independent of the hidden state, and conditional on the recorded actions and receipts it supplies no additional environment information.

The final report explicitly assumes that a common-label stopping declaration is always permitted. The permission menu guards inquiry actions. If declaring a verdict has another permission predicate, the terminal condition must be changed before using the theorem. Under the accepted contract, an initially homogeneous support with an empty inquiry menu is a legitimate rank-zero success; a mixed support with an empty menu is a dead end.

### 2. Fixed-point sufficiency is sound

For a retained region, only actions whose every positive-observation successor remains in the region are included. At a stable region, every actual-state/support pair has a finite directed path to a goal. Uniform choice among the retained actions is observation-based because the controller uses only its current support; the actual-state coordinate belongs to the offline analysis.

Under this fixed controller the augmented process is a finite, time-homogeneous Markov chain. Its positive transitions are precisely the graph used in the fixed-point check. A finite Markov chain with no reachable closed nonterminal class reaches its terminal set almost surely. Equivalently, finitely many positive finite paths provide a common positive probability of success within a common block length. Repeated block conditioning gives geometric decay of survival. The same argument gives finite mean stopping time for this constructed witness, without producing an optimal policy or a uniform numerical bound across arbitrary positive kernels.

This does not assume that support-to-support receipt probabilities remain bounded away from zero under changing posterior weights. The one-sided reveal control shows why that different assumption would be false.

### 3. Arbitrary-history completeness is sound

Let W contain the supports admitting an observation-history winner. Winning under any positive distribution on a finite support is equivalent, for the same policy, to winning from every constituent state. A positive finite continuation of a winner must still win from its entire posterior support: otherwise that continuation contributes positive failure probability to the original run. Thus every positive-probability action used by a winner keeps all its feasible successor supports inside W.

Starting at any actual state in a winning support, almost-sure finite stopping entails positive probability of stopping by some finite horizon. Finite branching supplies a positive finite path using these W-preserving actions. Hence every constituent pair has a goal path in the W graph, so W survives every pruning round. The greatest fixed point contains every history-dependent winner. Together with sufficiency this proves the equivalence, including arbitrary memory and independent randomization.

The finiteness, time-homogeneity, exact zero/positive distinctions, Markov conditional kernel, and observation-history restriction are substantive hypotheses. Neither unknown kernels nor drifting probabilities are covered.

### 4. Sure and almost-sure stopping are correctly separated

For pathwise sure finite termination, finite branching plus König's lemma supplies a uniform finite depth. A null-probability infinite supported branch still defeats that pathwise guarantee. The least attractor computes the corresponding finite depth. The two-sided reveal model is almost-surely solvable but admits arbitrarily long waits and is rejected by the sure attractor. The one-sided model has a genuine positive-mass nonterminating state and is rejected by both.

The fixed-point proof does not establish value-one attainment from a supremum, finite zero-error stopping from limiting statistical consistency, or a generic finite-memory result for hidden parity objectives.

## Two review findings corrected before this snapshot

1. The first positive non-PD fixture had behaviorally collapsible same-label states. The final fixture has two positive successors after the same action and `wait` receipt, but their next-wait probabilities are respectively 1/2 and 0. The successors have different future observation laws. This genuinely violates the inherited PD condition on the supplied model, rather than merely duplicating states. It does not establish impossibility of every alternative PD representation, and the report correctly disclaims that stronger assertion.
2. Reporting permission was initially implicit. The final contract makes its always-permitted stopping assumption explicit, and the independent boundary controls exercise both homogeneous and mixed empty-menu supports.

The final non-PD fixture's displayed survival formulas were independently checked for 64 prefixes using the actual substochastic evolution. Its positive stopping possibility follows from the proof, not the finite prefix enumeration.

## Independent executable evidence

Run `python replay_review.py` from this review directory.

`independent_controls.py` does not call the author's oracle or consume its computed support family, graph, safe menus, or elimination rounds to decide the reference answer. It represents supports as integer masks, enumerates every nonempty robustly legal stationary action subset, builds the resulting reachable finite product chain with positive rational weights, and uses exact Fraction elimination on I−Q for its nonterminal transition matrix. Nonsingularity is equivalent to transience of every reachable nonterminal state. Every accepted exact solution of (I−Q)t=1 is checked by substitution. This is a different decision computation from either graph-reachability implementation.

It covers:

- 2,025 cases: all 675 three-state, one-action, two-observation support models under three mixed initial supports
- 384 seeded three-state, three-action models with state-dependent permission menus
- 512 seeded four-state, one-action models, allowing hidden branching on both answer labels
- Seven named boundary/control instances and two skewed-positive-weight variants
- 10,202 exact policy matrices in total, across 2,930 model instances
- 459 winning controllers returned by the candidate solver, each independently re-evaluated without letting its action rule inspect the actual state

Controls include the one-sided shrinking-hazard trap, iterative loss propagation from a mixed absorbing trap, robust permission refusal, empty-menu goals/deadends, a second non-clone hidden branch, and an instance where neither deterministic stationary support action wins but uniform randomization does. In that last control the exact uniform expected query count is 4; almost-sure termination still does not give a sure finite bound.

`source_transport_controls.py` independently reconstructs the stipulated 16-state audit law, checks every state mass is positive, conditions on Y=1, and compares full-state and joint-target/audit projected laws on all 341 audit words of lengths zero through four. It separately verifies the known-Bad four masses, posterior 1/5, and the absence of any homogeneous fixed-audit support. For fresh imperfect verifiers it checks 511 binary words through length eight, each retaining positive likelihood under both labels, and the 1/(1+4^n) disagreement formula. It also checks the destructive initial-label example.

The author replay is separately identified: all seven unit tests pass; all 1,269 author oracle comparisons pass; all ten inherited-input hashes, including available Git blob hashes, pass. These replayed cases are not added to the independent counts above. Replaying the author verifier reproduces the frozen CONTROL_RESULTS.json byte-for-byte.

None of these finite computations proves the universal arbitrary-policy theorem by enumeration. The ordinary mathematical argument above, with its classical ancestry, supplies that claim.

## Source transport and attribution

The inherited PD review requires at most one successor for each hidden-state/action/receipt triple. The final positive example fails that condition on reachable transitions and has nonidentical future receipt laws. Thus the result genuinely covers a transition case excluded by that named descriptor embedding. Its stopping objective is narrower than the predecessor's general hidden acceptance objectives, so there is no claim that it subsumes the broader theorem.

The full hidden-model/observed-state control framework, initial-tag tracking, hard menus, exact finite-history zero-error obstruction, fixed-root versus fresh-source distinction, and known audit probabilities are inherited. The project-level increment here is their explicit transport to the supplied arbitrary hidden-state exact-stopping contract, with a directly executable witness criterion and a faithful audit application. No new field-level qualitative-POMDP mechanism is earned.

Direct external ancestry is [Chatterjee, Chmelík, Gupta and Kanodia, Optimal Cost Almost-sure Reachability in POMDPs, §4.2, Lemmas 5–6](https://arxiv.org/html/1411.3880v1#S4.SS2). Their allowed-action policy and actual-state/support chain closely match the central proof mechanism. The report credits this. Source shorthand about a belief-support MDP does not authorize arbitrary fixed probabilities on support edges; the substantive product-chain argument is the relevant dependency. No cost-optimization result or broad literature-priority claim is imported.

The fixed-audit impossibility is about a declared zero-error terminal verdict. It neither invalidates posterior 1/5 as a forecast nor implies that human knowledge, warranted action, or practical sufficiency requires posterior certainty. The final scope language keeps this distinction intact.

## Preservation and stopping boundary

All code execution and review additions occurred in scratch files. The source packet and its ten inherited inputs were hash-checked after review, and no prior packet or protected source was modified. Snapshot and replay receipts identify the exact accepted bytes. This review closes its assigned mathematical and executable review scope only; it does not grant publication, integration, philosophical closure, or new authority to any model input.
