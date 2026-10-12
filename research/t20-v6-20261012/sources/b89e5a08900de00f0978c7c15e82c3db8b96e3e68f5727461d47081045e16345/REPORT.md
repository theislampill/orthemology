# Independent review: fair recurrence and checked target operation

## Verdict and verified identity

**PASS_SCOPED.** The packet derives almost-sure recurrence for the actual finite-chain trajectory law and constructs local uniform retained-pair operation that wins parity for matching live models. No blocking defect was found in the proof or the advertised local-operation scope.

The reviewed manifest SHA-256 is `3b143fc2c7df13f68893a8de5d65ec7a7e7ea8721af6252e6fed06e433b26fa9`. All fourteen inherited modules were byte-compared against their declared originals. All seven new modules were read in full, together with the relevant inherited trajectory, graph, support, and target interfaces.

The independent cold replay compiled **21 fresh custom modules** and checked **272 registered declaration types and axiom readbacks**. Only `propext`, `Classical.choice`, and `Quot.sound` occurred. There were three ordinary inherited linter warnings and no proof-hole or compiler error. No new module emitted a warning. Official installed object caches remain trusted as disclosed; no author custom object directory was reused.

## Finite-path probability bound

`FiniteChainAvoidance.lean` starts from an actual finite transition table whose entries are nonnegative and whose rows sum to one. Its `avoid P target n s` is a backward recurrence for avoiding the target at the **n coordinates 0 through n−1**, with coordinate zero equal to the starting state s.

The proof does not assume a hitting bound. It establishes nonnegativity, an upper bound of one, and monotonicity in the number of coordinates. A concrete positive transition into a state with a strict finite-horizon hitting chance gives a strict finite-horizon hitting chance at its predecessor. Induction along a positive-support path gives such a horizon from each state. Finiteness then supplies a common horizon and a strict maximum avoidance factor r with 0≤r<1.

The block bound is derived from the normalized recurrence, not by assuming independence of successive avoidance blocks. `avoid_add_bound` factors a uniform future upper bound through an arbitrary earlier prefix; induction gives the geometric bound at k blocks. This works for periodic chains. Aperiodicity is not an implicit hypothesis.

## Actual trajectory law and indexing

The retained `ResetTrajectory.lean:70–94` defines the kernel sequence by applying the declared Markov kernel to the latest state in the acquired finite prefix. `markovTrajectory` is the genuine `Kernel.traj` construction starting with the given coordinate-zero state. Its finite-prefix marginal identity is an application of the Ionescu–Tulcea trajectory theorem, not a caller-supplied cylinder-law assumption.

`FiniteChainTrajectory.lean` constructs the transition PMF from the real row entries, proves normalization, and identifies every singleton transition mass with the declared probability. It then proves the backward dynamic program equals the integral under the actual finite trajectory composition.

The off-by-one contract is correct:

- `avoid … n s` and `pathAvoid … a n` inspect n coordinates
- `lmarginal_pathAvoid` inspects n+1 coordinates, from a through a+n, and integrates transitions through a+n while leaving coordinate a fixed
- The n=0 branch of that lemma therefore still checks one current coordinate
- `trajectory_interval_avoidance_bound` handles zero-length intervals separately, and the successor branch uses the corresponding n+1-coordinate formula

The arbitrary deterministic starting time a is handled by actual kernel composition from zero to a and then from a onward. No independently assumed Markov property of an already conditioned trajectory is used.

The independently authored Lean controls check the actual one-coordinate integral, showing it is zero when the initial state is already the target and one when the other state is the target. A deliberately false one-transition interpretation is rejected by Lean for the resulting arithmetic contradiction. A biased two-state chain also checks the exact avoidance values 1, 3/4, and 9/16 at one, two, and three coordinates, rather than only a deterministic periodic example.

## From finite windows to infinite recurrence

`InfiniteRecurrence.lean` proves that the recursive path readout is precisely the indicator of the finite avoidance-window event and establishes its measurability. Thus the numerical dynamic-programming bound controls the actual event probability.

For any deterministic time a, permanent avoidance from a onward lies inside every finite avoidance window beginning at a. Its probability is bounded by the geometric sequence tending to zero. Countably many deterministic start times then give almost-sure infinitely many visits to the target. Under finite strong connectivity the result applies to each state.

Recurrence is therefore a conclusion of finite positive paths, normalized rows, the constructed measure, and the geometric limit. It is not supplied as a premise under another name. The argument does not require a finite expected return-time bound, nor does it claim one here.

## Concrete stationary pair operation

`StationaryPairChain.lean` defines the transition from retained pair e to retained pair f as the full original probability of the successor state source(f), multiplied by the stationary probability of choosing f at that observed state.

Normalization is derived by regrouping the finite sum according to source states. The action weights sum to one **within each used state's action fiber**. Transitions to unused states have zero mass by the explicit full-row closure premise. There is no renormalization of the original transition row onto the retained state set.

The pair-chain support equals the positive original successor relation because every retained action has strictly positive weight. Concrete state-graph paths lift to pair-graph paths, including a final choice of the specified target pair. The end component's nonempty successor condition handles the first transition. This proves strong connectivity of the pair chain; recurrence is subsequently obtained from the actual finite-chain theorem.

`uniformChoices` supplies the stationary action weights explicitly as the inverse of the cardinality of the same-state action fiber. It is not an existential fairness assumption. Independent exact controls distinguish this correct rule from assigning equal weight globally across all pairs, which generally produces rows with mass less than one when states have different numbers of actions.

## Parity and the computed target

`FairComponentParity.lean` pushes the constructed retained-subtype trajectory onto the original pair alphabet by erasing only subtype proof fields. It proves the recurrent pair set is exactly the retained component almost surely. The even minimum of that set then gives actual parity success.

Higher odd priorities may recur infinitely often. The author's forced 2/3 cycle control explicitly proves parity success together with infinitely many odd-priority visits. No parity conclusion is obtained by deleting odd visits or by treating parity as a finite-cost objective.

`CheckedTargetOperation.lean` correctly connects this operation to the checked rational-row target:

1. Full-row matching transfers the qualifying candidate's no-exit property
2. For a matching **live** model, the no-exit adapter identifies its actual positive successors with the checked internal support graph
3. End-component properties transfer along that equality
4. The qualifying predicate supplies every matching live model's even-minimum condition
5. Uniform operation then wins under its actual transition law from every retained initial pair
6. The executable target equality supplies a qualifying component and a retained entry pair whose source is the returned state

This is stronger than the earlier stochastic bridge's `Valid` result alone: the present operational theorem uses the full `MarkovQualifying` information, including allowed membership and candidate no-exit. It does not silently omit those requirements.

The component and uniform action rule are common to the matching-model comparisons. The model indexes the actual transition law and hidden priority function; it is not passed into an observable policy decision rule.

## Scope that remains outside this acceptance

The operating process is a directly constructed pair-valued Markov chain. An identity with the arbitrary-private-seed action/history policy API is expressly not claimed. This review accepts the local operating law at that scope.

The certificate begins at a particular retained entry pair, with the correct source state. Every such retained initial pair is covered; a separately sampled initial-action mixture is not part of the packaged statement.

This packet does not derive navigation, statistical rejection, phase changes, proper-support handoffs, arbitrary adaptive-policy recurrent graph closure, or the full hidden-parity equivalence. The finite target implementation remains the exhaustive powerset reference. No polynomial MEC complexity claim follows from this review.

## Independent controls and reproduction

The review adds seven kernel-checked controls covering initial-coordinate indexing, actual trajectory integrals, a nonuniform strongly connected chain, exact weighted avoidance, recurrence, and the geometric bound. A false off-by-one numerical statement is deliberately rejected. These controls use only custom objects built by this review's cold replay and check their recorded object hashes before importing them.

The independent rational checker verifies 1,500 finite interval cases by directly enumerating path laws and comparing them with the avoidance recursion. It also tests biased geometric decay, state-fiber normalization, and failure of recurrence for disconnected or unfair examples. These bounded tests supplement, and do not replace, the general infinite recurrence proof.

`SOURCE_BINDING.json` authenticates every candidate file. `INHERITED_IDENTITY.json` records the fourteen original comparisons. `evidence/` holds the cold receipt, complete declaration readback, diagnostics and independent control results. `controls/` contains the authored control sources and runners.

The replay uses the inspected portable driver with `--suites fair_component_recurrence --no-reuse`, pinned Lean 4.19.0 and Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`, and an absent output outside the candidate. An initial command used the wrong suite identifier and was rejected before any replay output was created; the corrected command completed the full cold run.

No source amendments are requested. This scoped acceptance changes no canonical status and authorizes no publication.
