# Restoring under ongoing disturbances: hidden-history acceptance and licensed continuation

**Status:** Consolidated research result, conditional on a declared finite model; no repository adoption or actual-world adequacy claim. Repository inspected at `03e2604dfcef278b01c60d19b05370fcec4194b6`. This extends the intermediate `frontier-programme.md` result rather than treating that checkpoint as the final frontier.

## 1. The obstruction is not only core entry

The previous checkpoint proved equivalence of eventual target persistence and forced finite entry into a belief-invariant target core only for **finite initial uncertainty with deterministic subsequent evolution**. Ongoing disturbance invalidates its finite-complete-trajectories argument.

There is a further, distinct failure: under hidden target status, running an ordinary co-Büchi algorithm on the belief arena with the universal target lift is still incomplete.

### Countermodel H1: every concrete path settles, but knowledge never settles

Use the Round-14 graph, with one permitted action:

- 0 goes to 0
- 1 goes to 0
- 2 goes to any of 0, 1, 2

All states are safe; target states are 0 and 2; every state emits the same observation; the initial state is 2. Every concrete path has at most one bad visit, namely a visit to 1. Thus the only policy wins sure co-Büchi restoration.

Its belief sequence is `{2}, {0,1,2}, {0,1,2}, …`. The belief always retains a possible present bad state. Consequently co-Büchi on `Target# = {B : B ⊆ Target}` rejects that policy. The actual temporal assertion is

> Every compatible infinite hidden history has finitely many bad positions.

It is not

> After one publicly detectable point, every currently compatible state is target.

Fresh hidden histories can supply the bad alternative at arbitrarily late positions even when no one hidden history has infinitely many bad positions. This is quantifier noncommutation, not an inaccurate belief update.

### Countermodel H2: memory beyond exact belief is necessary

There are three safe states, `Target={0,2}`, one observation, and initial belief `{0,1,2}`. Both actions are warranted and eligible everywhere:

| State | a-successors | b-successors |
|---|---|---|
| 0 | {2} | {2} |
| 1 | {1} | {2} |
| 2 | {0} | {0,1} |

Both actions preserve the full belief. A deterministic belief-stationary policy therefore plays one fixed action forever:

- `a` forever loses on the self-loop at bad state 1
- `b` forever loses on the bad cycle `1→2→1`

Yet alternating `a,b,a,b,…` is sure winning. In the six-state product with phase `A/B`, its only recurrent strongly connected components are the target cycles

- `(0,A)→(2,B)→(0,A)`
- `(2,A)→(0,B)→(2,A)`

The only connection through bad states is `(2,B)→(1,A)→(1,B)→(2,A)`. Every path has at most two bad visits. The controller requires one phase bit that is not recoverable from the constant belief.

Randomization over a fixed belief does not repair sure winning: any supported repeated-action sequence remains an allowed outcome. With fixed positive randomization and equal positive probability on each listed plant edge, the resulting three-state Markov chain is irreducible whenever both actions occur with positive probability; its bad state is recurrent. Either pure stationary extreme also has a bad recurrent class. Thus this same fixture separates a two-memory pure sure winner from every stationary randomized belief policy under that specified kernel.

These two examples have different purposes. H1 disproves a naive acceptance condition, even for a policy with no memory requirement. H2 disproves belief-stationary strategy sufficiency.

## 2. A finite licensed disturbance model

Let `X` be finite hidden configurations, `C` finite public custody/authority states, `A` finite actions, and `O` finite observations. Hidden configurations may include:

- the current physical/noetic state
- a fixed candidate model, or a currently switching standard
- persistent root-corruption flags and other causally relevant latent state
- bounded environment or membership modes

For each `(c,x,a)`, a finite nonempty relation

`Δ(c,x,a) ⊆ X × O`

lists all permitted successor-hidden-state/observation pairs. The public update `u(c,a,o)` is deterministic. No independence between successor state and observation is assumed. Adversarial observations are permitted precisely through this relation; calling a report authenticated does not authenticate it.

An exact support belief is updated by

`U(c,B,a,o) = {x' : ∃x∈B, (x',o)∈Δ(c,x,a)}`.

The licensed action menu is

`Γ(c,B) = {a : J(c,B,a) and ∀x∈B E(c,x,a)}`.

`E` is the supplied pointwise authority/version/capability/semantics predicate. `J` is a checkable judgment available from public information. Both retain their warrant burden. If the warrant process needs unbounded history, a faithful finite public abstraction must be proved before this theorem applies. Hidden eligibility cannot be used as an oracle. Every actual successor remains in the relation, including unsafe or inconvenient outcomes. An absent permitted continuation loses unless a terminal behavior has explicitly been represented.

Let `Safe(c,x)` and `Target(c,x)` be supplied, with target implying safety. A policy observes its actions and received observations, hence computes `c` and `B`; it does not observe `x`. All results below require safety and licensed action use on every admitted finite history.

### Two standard-switching interpretations that must remain separate

1. **Currently active standard:** take `x=(h,s,…)`, allow `h` to change in `Δ`, and define `Target(c,x)` using `T_h`.
2. **Robust simultaneous satisfaction, as in Deep CQ:** define the target using `s∈∩_{h∈H}T_h` and retain common eligibility. Standard switching controls successors, but does not weaken the target to just the currently selected standard.

They are distinct specifications. The model supports either after its meaning has been declared; one cannot silently substitute the first for Deep CQ's second.

## 3. Exact bounded-visit synthesis

Fix a nonnegative integer `k`. At every public history maintain a function

`f : X → {−1,0,…,k}`,

where `−1` means unreachable and `f(x)` is the **largest number of bad-state visits among compatible finite hidden histories currently ending at x**, including the current position. Initially,

`f₀(x)=1[¬Target(c₀,x)]` for admitted `x`, and `−1` otherwise.

For a successor observation `o`, let `c'=u(c,a,o)` and set

`f'(x') = max{f(x)+1[¬Target(c',x')] : f(x)≥0 and (x',o)∈Δ(c,x,a)}`,

with the maximum of the empty set equal to `−1`. Any value above `k` leads to a losing overflow state. The support of `f` is exactly `B`. Any support containing an unsafe possibility is losing. Choices are restricted to `Γ(c,supp f)`.

This is a finite, perfect-information **safety game** on `(c,f)`. Its winning set is the greatest fixed point

`S_k = νY.{(c,f) : safe support, no overflow, and ∃a∈Γ(c,supp f), every nonempty observation successor is in Y}`.

### Theorem D1 — bounded visits, with no target-observability assumption

The initial `(c₀,f₀)` belongs to `S_k` if and only if an observation-based licensed policy keeps every admitted path safe and gives every path at most `k` bad visits. A policy memoryless in `(c,f)` suffices.

**Proof.** Induction on public histories proves the displayed max update exactly records compatible finite histories and their bad-visit maxima. In particular, overflow occurs exactly when some compatible history has more than `k` bad visits; safety failure occurs exactly when some compatible actual history is unsafe. No hidden run is pieced together from inconsistent adjacent histories: each counted predecessor has an actual compatible finite witness, extended by the declared successor edge. Thus bounded restoration is precisely safety in this finite counter game. Greatest-fixed-point safety-game coinduction and the usual outside-the-kernel spoiling argument prove both directions and yield memoryless choices in `(c,f)`. Every infinite observation branch of the resulting arena has a compatible hidden path by finite branching and König's lemma. ∎

A counter function is not a posterior probability and does not count reports. It remembers the temporal burden carried by each still-possible hidden history. H1 succeeds at `k=1`; H2 succeeds at `k=2` and fails at `k=1`.

## 4. From bounded synthesis to general sure restoration

The general objective is `Safe forever ∧ finitely many bad visits`. It does not impose a uniform last-bad time.

### Theorem D2 — effective exact sure-restoration characterization

For the finite model above, the following are equivalent:

1. Some deterministic observation-history policy wins sure restoration
2. Some finite-memory observation-based policy wins sure restoration
3. `(c₀,f₀)∈S_k` for some finite `k`

For support-based sure winning, randomization adds no existence power: choosing a supported action deterministically at each public history only removes outcomes. There is an effectively computable finite cutoff for `k`. The cutoff comes from finite ω-regular synthesis, not from the number of ordinary belief states.

**Proof.** The implications 3→2→1 follow from D1. For 1→2, construct a nondeterministic Büchi word automaton over action/observation histories. Its states track one compatible hidden configuration and public custody state. It accepts a word when some compatible infinite hidden history visits bad states infinitely often. Infeasible observation words are excluded by the exact support arena. Safety is checked separately on the universal support at every finite prefix; an unsafe support leads to a losing sink.

Determinize this automaton to a deterministic parity monitor and complement its parity acceptance. Take its product with the public `(c,B)` arena, retaining exactly the licensed menu `Γ` and the support-safety check. The resulting finite perfect-information parity game enforces safety on every compatible finite history and rejects exactly the feasible observation words admitting a bad-infinite hidden history. Finite parity games admit positional winning strategies. Such a strategy in the product is a finite-memory observation strategy in the original game.

For 2→3, fix a finite-memory winner. Its reachable concrete controller product is a finite directed graph. No reachable directed cycle contains a bad vertex, since that cycle could be repeated by the adversary. Therefore a path cannot repeat a bad product vertex. The number of bad visits is bounded by the number of reachable bad product vertices. D1 then applies for that finite bound.

For an explicit computable, deliberately loose cutoff, let `P` be the number of public information states `(c,B)`, and `d` the number of states of the determinized parity monitor actually constructed. A positional product policy has at most `Pd` memory states, and the concrete product has at most `|X|Pd` vertices. Taking `k=|X|Pd` is sufficient whenever the problem is sure winning. ∎

**Important quantifier:** D2 is about existence of a winning policy. It does not claim that every infinite-memory sure-winning policy has a uniform bound on bad visits. Nor does it give a uniform bound on when the last bad visit occurs. Target cycles may stutter indefinitely before a final exit to a bad state; H1 already shows that.

The executable solver in this lane implements D1 for an explicitly supplied bound. It does not implement the parity determinization or the global cutoff construction; a losing bounded instance alone is not a general impossibility certificate.

This construction is standard universal-co-Büchi/bounded-synthesis mathematics specialized to a licensed partially observed restoration model. It is not a claim of new general automata or game theory.

## 5. Why almost-sure restoration requires different evidence

**Sure** means every path allowed by the declared transition support satisfies the objective, including probability-zero infinite paths. **Almost sure** means the objective has probability one under the declared kernel (and, for a stochastic game, against every admitted adversary). Merely supplying support edges does not supply probabilities, independence, stationarity, or fairness.

For a fixed finite-memory controller and a fixed finite time-homogeneous stochastic plant, form the finite Markov chain on actual state and controller memory. Then:

- sure co-Büchi holds exactly when no reachable directed cycle contains a bad state
- almost-sure co-Büchi holds exactly when every reachable bottom strongly connected component contains only target states
- safety almost surely is equivalent to absence of a reachable unsafe state when every listed edge has positive probability

The first criterion examines all recurrently repeatable support paths. The second examines the classes in which the finite chain can actually remain with nonzero probability. The distinction cannot be removed by calling unlikely edges adversarial.

### Countermodel P1: geometric repair

A bad state `b` moves to itself with probability `1/2` and to an absorbing target `g` with probability `1/2`. There is one action, one observation, and initial state `b`. Restoration is almost sure. It is not sure, because `b,b,b,…` is a support path. No finite bound on the number of bad visits is guaranteed: for each finite `k`, more than `k` visits has positive probability. The belief continues to contain `b` at every finite time.

### Countermodel P2: adversarial choice of probabilities

If a disturbance controller can choose kernels whose exit probabilities shrink summably, the same support graph no longer guarantees almost-sure repair. Choosing exit probability `p_t=2^{−t−2}` gives positive probability of staying bad forever, because `∏_t(1−p_t)>0`. A finite fixed list of kernels with positive lower-bounded exit probabilities behaves differently. “Every edge has positive probability” alone does not license a uniform-progress argument when kernels vary without such a bound.

### Exact finite-controller adversarial stochastic test

If, after each controller action, a perfect-information adversary chooses one member of a **finite declared set of fixed stochastic kernels**, the fixed-controller product is a finite MDP. Almost-sure co-Büchi against every adversary holds exactly when **every reachable end component is target-contained**. A bad end component lets the adversary stay in it and revisit a bad vertex; absent one, the almost-sure set of infinitely recurrent vertices is target-contained. This does not extend to unrestricted time-varying kernels with probabilities tending to zero.

General almost-sure POMDP synthesis must not be claimed solved by D1. Literature distinguishes unrestricted strategies from finite-memory strategies; the former co-Büchi existence problem is undecidable in general, whereas finite-memory qualitative parity synthesis has an exponential decision procedure and may require more than stationary belief policies. Our executable lane will verify finite controllers and synthesize the sure objective, not quietly claim unrestricted almost-sure completeness.

## 6. Source and provenance custody

Deep AS fixes a deterministic intervention-response episode; Deep CQ fixes fully observed switching-standard viability/core entry; Deep CR conditions source restriction on source-relative and world-directed guards; Round 14 separates general co-Büchi restoration from invariant-core entry. D1–D2 address the missing partially observed, continually disturbed control joint while preserving those separate guards.

Persistent root corruption belongs in hidden state. If at most `f` authenticated roots may be corrupt for the whole episode, encode a fixed subset `F` with `|F|≤f`; do not independently choose a new corrupt subset for every report. Copied messages from one root must be generated jointly from the same root event. An observation update may eliminate a configuration only if the received message is impossible under its declared joint root model. Distinct labels or copies do not establish independent roots. Dynamic corruption or new acquisitions require their own explicitly declared state transitions.

A successful policy certifies none of source truth, target correctness, actual-world applicability, independent testimony, recipient authority, human restoration, or metaphysical ascent. Restricting the live model family can change the controller problem only after the inherited-semantics and source/world obligations are met.

## 7. Primary-literature boundary checks

- Chatterjee, Doyen, Henzinger, Raskin, *Algorithms for Omega-Regular Games with Imperfect Information* (2007), [paper](https://arxiv.org/pdf/0706.2619). The basic objectives in §2 are observation-based; importing its belief-arena acceptance result directly for hidden target status would miss H1. Its separation of sure and almost-sure winning remains relevant. We do not use an observation-visible theorem as if it proved hidden-objective belief sufficiency.
- Schewe and Finkbeiner, *Bounded Synthesis* (2007), [paper](https://intranet.csc.liv.ac.uk/~sven/atva07b.pdf), §§3–4. The finite run-graph annotation and counting-function safety construction are the mathematical ancestry of D1/D2. Their remark explicitly separates finite-state implementations, which have bounded annotations, from arbitrary accepted systems, which need not. The licensed menu, hidden state, and public custody compilation above identify this application’s extra contracts.
- Chatterjee, Chmelík, Tracol, *What is Decidable about Partially Observable Markov Decision Processes with ω-Regular Objectives* (2013 full version), [paper](https://arxiv.org/pdf/1309.2802). Its finite-memory results and examples distinguish finite-memory qualitative synthesis from unrestricted synthesis and show that stationary belief policies can fail for co-Büchi even with visible objectives. This supports the stochastic scope boundary; it is not used to reclassify our adversarial sure theorem as an almost-sure theorem.
- Chatterjee, Doyen, Henzinger, *Qualitative Analysis of Partially-observable Markov Decision Processes* (2010), [paper](https://arxiv.org/pdf/0909.1645). The objective and strategy regime matter: almost-sure co-Büchi has a different decidability boundary from almost-sure safety/reachability/Büchi and positive co-Büchi.

## 8. Consolidation status

The originally pending bounded exhaustive checks, permission/custody mutations, stochastic bottom-SCC/end-component fixtures, and temporal migration certificates have now been completed within their declared finite scopes. Later sections preserve the successive results; `README.md` and `INTERFACE_MAP.json` identify the additional Hall, hidden-standard, stochastic, regenerative and private/public-composition returns. The next step is fresh synthesis review, not an unimplemented claim of general parity synthesis or actual-world authority.

## 9. Migrating a sure-restorative controller without losing its temporal memory

The earlier checkpoint transported a rank that decreased on every step before invariant-core entry. Such a rank cannot express H1/H2: a target state may stutter arbitrarily before a final bad visit. The right certificate for a selected finite-memory sure controller is instead a **bad-visit rank** on its concrete closed-loop product.

Let `P_A` be the source's reachable concrete controller-product states. They include hidden plant state, public custody, and controller memory. All source actions have already been selected by an observation-based licensed controller. Every source state is safe, and there is a rank `ρ:P_A→N` satisfying, for every selected source edge `p→p'`,

`ρ(p) ≥ 1[Bad_A(p)] + ρ(p')`.

Such a rank exists exactly when there is no reachable bad cycle; the maximal number of future bad visits is one choice. Target steps may leave the rank unchanged forever.

The destination must independently implement an observation-based finite controller `β`, with its own public memory and actual license checks. Its concrete product is `P_B`. A source witness never chooses a hidden-dependent destination action.

Choose `R⊆P_A×P_B` satisfying:

- **M0 Initial coverage:** every admitted initial destination product state is related to an admitted source product state
- **M1 Destination license/safety:** destination action selection is determined only by destination public/controller memory, is in its own `Γ_B`, and keeps every successor in the certified safe domain
- **M2 Synchronous step match:** for every `pRq` and every selected destination edge `q→q'`, there is a selected source edge `p→p'` with `p'Rq'`
- **M3 Bad-state reflection:** `pRq` and `Bad_B(q)` imply `Bad_A(p)`
- **M4 Task readout:** related pairs satisfy the separately declared task-readout/continuation relation, including any source-version and semantic correspondence required by the application

No stuttering or hidden fairness restriction is silently included in M2. Every destination step receives one source step. Neither safety nor permission is inferred from equal outputs.

### Theorem M1 — synchronous licensed co-Büchi continuation

Under M0–M4, the destination controller wins sure restoration and preserves the declared readout relation along matched runs. For any destination product state with a nonempty source fibre, define

`r_B(q)=min{ρ(p):pRq}`.

Every selected destination edge satisfies

`r_B(q) ≥ 1[Bad_B(q)] + r_B(q')`.

Thus `r_B` bounds the number of future bad visits, without bounding the time of the last one.

**Proof.** Choose a source witness minimizing the finite nonempty fibre. M2 supplies a successor witness for each destination successor. The source rank inequality and M3 give

`r_B(q)=ρ(p) ≥ 1[Bad_A(p)]+ρ(p') ≥ 1[Bad_B(q)]+r_B(q')`.

M0 ensures a starting witness; M2 perpetuates it. A natural-number rank can strictly decrease only finitely often, hence bad destination visits are finite. M1 separately supplies lawful safety, and M4 gives the readout relation. Alternatively, iterating M2 constructs one entire source run matching any destination run; an infinite destination-bad subsequence would force an infinite source-bad subsequence. ∎

### Why the minimum is sound here but was unsound in the checkpoint

These fibres are **simulation witnesses over concrete controller products**, not exact epistemic possibility sets. M3 is pairwise: no related target source can witness a bad destination. The checkpoint used a weaker conservative target rule that only transferred target status when **all** represented information states had reached rank zero. Under that different rule, a convenient rank-zero witness did not establish destination target status and a maximum plus coverage was needed.

There is no contradiction and no authority to replace a belief by a convenient witness. R must not be represented to the controller as evidence that its other actual possibilities disappeared. The controller's license is still computed from its complete real belief. This distinction between a proof witness and accessible knowledge is essential.

### Deletion examples

- **Forget memory:** compress H2's two-phase implementation to one public controller state while preserving the constant current output and full belief. Every stationary destination action loses. The source phase is a future-control resource even though it is absent from current output and belief
- **Delete M3:** a source target self-loop can simulate a destination bad self-loop step for step; the temporal claim fails
- **Allow empty matching steps:** a destination may take infinitely many bad steps while making no source progress. Synchronous M2 does not license this; a stuttering refinement would need a separate well-founded divergence/progress condition
- **Delete destination authorization:** a syntactically matching repair operation can lack the current destination certificate. M1 fails even when all raw actuator edges match

M1 is a sufficient selected-policy continuation contract. It establishes neither necessity nor subject identity, physical realizability, every-future-task equivalence, or an actual migration.

## 10. Almost-sure migration needs probability mass, not just edge matches

### Countermodel M-AS0: support simulation destroys almost-sure restoration

The source chain is geometric repair, `b→b` and `b→g` with probability `1/2` each, and `g→g`. The destination has `q_b→q_b` with probability one. Relate `b` to `q_b`; bad labels agree, outputs may be equal, and every destination support edge has a matching source support edge. The source restores almost surely while the destination never restores.

This does not refute Theorem M1, whose source must be **sure** winning. It refutes transferring an almost-sure claim through an ordinary support simulation: the matched source path staying bad forever has probability zero, while its destination counterpart has probability one.

### A sufficient coupling contract for fixed finite controllers

Compile the selected source and destination controllers and their own license checks into finite, time-homogeneous Markov chains with transition distributions `P_A(p,·)` and `P_B(q,·)`. Preserve M0/M1/M3/M4 and replace M2 by:

**M2-probability:** for each related `pRq`, provide a joint distribution `κ_{p,q}` on next-state pairs such that

- its source marginal is exactly `P_A(p,·)`
- its destination marginal is exactly `P_B(q,·)`
- it assigns probability one to `R`

Initial distributions likewise have a coupling supported in `R`; for a single related initial pair this is immediate. These are model-level distributions; data do not gain an independence or stationarity certificate because a coupling matrix can be solved.

### Theorem M2 — licensed almost-sure continuation by coupling

If the source chain is almost-sure safe/co-Büchi winning and the coupling contract holds, then the destination chain is almost-sure safe/co-Büchi winning. If safety is an independent sure requirement in the task, M1 must establish it on every support path as before.

**Proof.** At each related pair choose the supplied joint successor distribution. This defines a finite Markov chain on R. Its coordinate marginals have exactly the original source and destination path distributions. The relation holds at all times almost surely. By M3, every destination bad visit is also a source bad visit on the coupled path, so destination bad-infinitely-often is a subset of source bad-infinitely-often. The latter event has probability zero. Readout and license remain separate pointwise contracts. ∎

The coupling condition is sufficient, not necessary. For example, geometric repairs with exit probabilities `1/2` and `1/3` both restore almost surely, while the identity relation need not admit an exact one-step coupling. A weaker quantitative/stuttering contract would require its own proof.

### Positive many-to-one stochastic fixture

Source states are `b,g₁,g₂` with

`P_A(b,b)=1/2`, `P_A(b,g₁)=P_A(b,g₂)=1/4`, and absorbing `g₁,g₂`.

Destination states are `q_b,q_g` with probabilities `1/2` each from `q_b` to itself and `q_g`, and absorbing `q_g`. The relation pairs `b` with `q_b` and both `g₁,g₂` with `q_g`. The three nonzero coupling entries at the bad pair are `1/2,1/4,1/4` on those related successors. The destination merges source target branches while preserving almost-sure restoration. Neither side is sure winning.

The ancestry is standard probabilistic simulation via distribution lifting/weight functions, not new general coupling mathematics. See Segala and Lynch, [*Probabilistic Simulations for Probabilistic Processes*](https://profs.sci.univr.it/~segala/www/SL95-NJC.html) (1995). The present contract supplies the otherwise missing restoration, public-memory, and authority obligations rather than claiming that a probability-preserving relation establishes them itself.

## 11. Hidden acceptance can have more complexity than co-Büchi observation labels

### Countermodel H3: an infinitely-often requirement emerges from hidden co-Büchi

Consider a blind plant with states `w,c,d`, initially `w`, and bad state `c` only:

- under `a`: `w→w`, `c→d`, `d→d`
- under `b`: `w→{w,c}`, `c→c`, `d→d`

All actions are licensed and all states are safe. For any infinite action word, every hidden path has finitely many bad visits **if and only if `a` occurs infinitely often**. If a path enters `c`, the next `a` moves it permanently to safe `d`; if there is a last `a`, the adversary can enter `c` afterward and remain there forever.

Thus even a three-state hidden co-Büchi plant can induce a Büchi language on public action words. This language has no equivalent finite deterministic co-Büchi word monitor. To see why, suppose such a monitor has `n` states and rejects exactly by infinitely many rejecting-state visits. From every reachable monitor state, the suffix `b^ω` must be rejected. Hence every sufficiently long block of `b` (length at most `n+1` suffices) must visit a rejecting state; otherwise its repeated-state `b`-cycle would accept a finite-a word. The word `(ab^{n+1})^ω` contains infinitely many `a` yet forces infinitely many rejecting-state visits, a contradiction.

More generally, the dual of any nondeterministic Büchi automaton is a universal co-Büchi monitor. Encoding its transitions as a blind plant shows that the public good-word language can be any ω-regular language. Missing transitions can be completed by a permanently target sink. Therefore a general exact public-language monitor may need full ω-regular acceptance, rather than a simple co-Büchi label on beliefs.

### The sharp policy-quantifier distinction

In H3, the policy emitting `b a b² a b³ a …` is sure winning. Each actual path either stays at `w`, or enters `c` during one finite b-block and leaves at its next `a`. But for every `k` one compatible path has more than `k` bad visits. There is no uniform bad-count bound for this particular infinite-memory policy.

The different policy `a^ω` is sure winning with zero bad visits. This explicitly validates D2's **existence** equivalence without strengthening it to a bound on every winning strategy.

## 12. Provenance timing and repeated controller changes

### Root-level diagnostic timing

A synthetic binary-hypothesis fixture uses three root-indexed reports and then one of two hypothesis-specific repairs; the wrong repair is unsafe. With one **static** substitution among three independently authenticated roots, majority diagnosis yields a safe repair and at most four bad visits (initial state and three diagnostic steps). Three aliases of one actual root do not: homogeneous reports remain compatible with both hypotheses. Under a mobile budget allowing one newly corrupt queried root at each sequential read, every transcript remains compatible with both hypotheses, so no safe repair is available.

A simultaneous three-root read under a one-root budget is a different timing model: at most one coordinate can be corrupted in that vector, restoring majority diagnosis and a two-bad-visit bound. The tool does not certify that simultaneous acquisition is feasible or that roots are independent; those are explicit fixture premises. This extends the modeling interface around Deep AW's static-code and Round 20's static-support boundaries rather than overwriting their exclusions.

### Individually restorative controllers can fail under unlimited switching

Let target `g` be absorbing. Controller A uses `b₀→b₁→g`; controller B uses `b₁→b₀→g`. Each is sure restoring from every state. Switching to A at `b₀` and B at `b₁` yields an infinite bad cycle.

Their individual future-bad ranks are

- A: `r(b₀)=2`, `r(b₁)=1`, `r(g)=0`
- B: `r(b₀)=1`, `r(b₁)=2`, `r(g)=0`

The harmful switches reset rank from one to two. A sufficient repeated-migration/switching contract permits a new mode only when its current-state rank is no greater than the old one, and then executes a plant transition satisfying the new mode's bad-visit inequality. The combined rank never rises and strictly drops on every bad plant step, so arbitrary allowed mode choices remain sure restorative. This statement assumes one mode choice per plant step; an implementation with infinitely many silent zero-time migrations needs a separate non-Zeno/progress contract.

Permission to switch and preservation of progress are separate. An authorized reset can still break liveness. The condition must cover the actual migration transformation and its source/target version, not merely compare unrelated numeric labels.

## 13. Verified executable scope as of this research checkpoint

All scripts are self-contained Python using the standard library and exact rational arithmetic where probabilities appear. Run from the lane directory:

- The original checkpoint had 16 unit tests. The consolidated explicit six-module command in `README.md` now passes 34 tests, including permissions, unsafe outcomes, dead ends, custody expiry, migration reflection, probability-mass preservation, public/private interfaces and composition
- `python probe_exhaustive.py`: 10,935 exhaustive two-state bounded instances plus 2,000 seeded public-custody instances; zero counter/exact-count-subset mismatches; every extracted winner checked on the concrete product; 169 independent random sure controllers also accepted at their direct visit bounds
- The same probe checks 3,000 finite MDPs against brute end-component enumeration; zero mismatches
- `python probe_migration.py`: 256 exhaustive two-by-two transportation instances and 4,000 seeded cases agree with independent weighted Hall inequalities; 27,540 two-state rank certificates include 3,825 accepted certificates, all passing direct bad-cycle checking; 1,000 nontrivial many-to-one stochastic quotients preserve almost-sure restoration and correctly fail sure restoration
- `python probe_provenance.py`: all four static/aliased/mobile/sequential/simultaneous diagnostic expectations match
- `python probe_switching.py`: standalone controllers win, unrestricted switching loses, and rank-nonincreasing switching wins
- `python probe_hidden_acceptance.py`: 3,906 ultimately periodic action words match H3's infinitely-many-a characterization; increasing-block prefixes exhibit growing bad-count maxima through 30

Finite tests check implementations and preserve counterexamples; the proofs carry the unbounded finite-model statements. The general parity determinization/cutoff algorithm is described mathematically, not implemented. No empirical cognitive model, repository integration, or machine-kernel theorem receipt follows from these checks.
