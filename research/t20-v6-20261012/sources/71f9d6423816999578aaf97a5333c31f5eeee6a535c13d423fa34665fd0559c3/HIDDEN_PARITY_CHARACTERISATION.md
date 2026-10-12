# Support-changing finite-model Markov systems with hidden parity objectives

Fresh ordinary theorem and author qualification, 2026-10-01. This extends the freshly reviewed hidden co-Büchi theorem at the mathematical objective interface. It is not a new Lean theorem, an optimal complexity classification, or a historical-priority claim. The exact scope is almost-sure parity winning. No finite expected count of odd-priority visits is claimed.

## 1. Experiment and objective

Use finite nonempty models Theta, observed states S and actions A, known rational transition rows P_theta(s,a,y), exact live-support update

    B[s,a,y]={sigma in B:P_sigma(s,a,y)>0},

and hard menus Gamma(B,s), possibly empty. The true theta is fixed and remains live almost surely. A common history-dependent policy sees states, actions and the exact support but no hidden model label. Its private randomization, if used, is independent and has the same law across models. Policies may use unbounded memory.

Replace the binary accepted-pair sets by explicit integer priorities

    c_theta:S×A→{0,1,...,d}.

The parity convention is **minimum priority occurring infinitely often is even**. It is a tail objective on the actually used pairs. The priority need not be observation-compatible across models, and it is not supplied as an extra observation. Binary co-Büchi acceptance is the special case priority1 on bad pairs and priority2 on good pairs.

For each nonempty B, compute a winning region W_B⊆S bottom-up in |B|. Assume the proper-support regions are already computed. Given W⊆S, define A_(B,W)(s) as the actions in Gamma(B,s) for which every positive-support successor is safe:

- if C=B[s,a,y] is nonempty and proper, require y∈W_C
- if C=B, require y∈W

The internal successor set I_B(s,a) consists of y with B[s,a,y]=B. Each such edge is positive under every live model. Let q_theta(s,a) be the probability of a nonempty proper support exit under theta.

## 2. Parity self-verifying components

An internal end component D=(C,U) inside W has nonempty C, nonempty U(s)⊆A_(B,W)(s), every used pair's internal successors contained in C, and a strongly connected internal graph. Its used pair set is E(D).

For candidate theta, require q_theta=0 on every used pair. These internal rows are therefore normalized theta-transition rows. Define

    Match_theta(D)={sigma in B: P_sigma(e,·)=P_theta(e,·) for every e∈E(D)}.

D is a parity self-verifying target for theta precisely when

    min { c_sigma(e):e∈E(D) } is even for every sigma∈Match_theta(D).

The set is nonempty and theta itself is a matching model. The equality is of **full rows**, not rows renormalized on no exit. A matching model also has zero exit probability on D.

Let T_theta(W) be the union of these target state sets. Let E_theta(W) be the states admitting some action in A_(B,W) with positive theta-exit probability. Let R_B(W) be the states in W from which every theta∈B has an internal graph path to T_theta(W)∪E_theta(W). Zero-length paths are permitted. Descend from S by this monotone contracting operator; the fixed point is W_B.

Monotonicity holds although parity validity is not monotone under arbitrary enlargement of a component: an existing valid component and its paths remain available when W increases. All operators return subsets of W.

## 3. Main theorem

For every nonempty B and initial state s, the following are equivalent:

1. s∈W_B
2. There exists one common lawful policy from(B,s) that satisfies its actual c_theta parity objective almost surely for every theta∈B

The statement quantifies one policy before all true models. The policy is not permitted to observe c_theta(s,a) as a truth-dependent feedback signal. The conclusion concerns existence of an almost-surely winning policy, not merely supremum success value one.

The proof is simultaneous induction on |B|. It reuses the freshly reviewed support-changing theorem's transition-sampling/navigation lemmas, which depend on rows, safe actions and target reachability rather than on the target's objective label. The changed recurrence and parity steps are proved below.

## 4. Necessity for arbitrary causal policies

Let V_B be the common almost-sure winning region, and suppose lower-support equality is known. A positive finite observed history has positive probability in exactly its surviving models. The conditional residual policy wins in each survivor, since a positive conditional failure would contradict original probability-one success. A common independent seed induces the same behavioral action kernel across surviving models: after an observed action/state history is fixed, the model-dependent transition likelihood cancels from seed conditioning. Thus every selected action has all same-support successors in V_B and all proper successors in their W_C, and is allowed by A_(B,V_B).

Fix theta. A positive exit event supplies a finite internal path to E_theta(V_B). Otherwise a positive no-exit event has an exact recurrent pair set E. On almost every such path, E is nonempty, internally closed and strongly connected, and every pair in E has zero theta-exit probability. Repeated use of a pair with a positive exit or an omitted positive internal successor cannot avoid that event forever. After the finitely used pairs disappear, paths along the run give strong connectivity.

There are finitely many possible E. Select a positive-probability event with one recurrent component D and a finite prefix after which only E is used and every E-pair recurs infinitely. Since the actual parity objective wins, min c_theta(E) is even.

For any sigma∈Match_theta(D), the prefix is still possible because support remains B. Kill the residual process at the first selected pair outside E or at a proper support change. Before killing, the full rows agree and the action kernels are common. Finite cylinder laws, and hence the relevant infinite tail-event probabilities, agree. That recurrent E-event has positive sigma-probability. Almost-sure sigma parity success forces min c_sigma(E) even. Thus D qualifies simultaneously for every matching sigma.

Every theta therefore supplies a path to an exit or a valid target. Hence V_B⊆R_B(V_B). Descending monotone iteration gives V_B⊆W_B. This argument permits arbitrary history dependence and uses only tail invariance of parity; it does not assume finite memory or finite expected errors.

## 5. Why the existing statistical phase construction suffices

Fix W=W_B. Cycle through candidate models. For candidate phi, navigate uniformly among A_(B,W) while testing full transition rows against phi. Stop navigation on rejection, a proper support exit, or entry into T_phi(W). On target entry choose a containing target component and operate uniformly among its used actions with fresh counters. Reject on the same empirical-row tests; a proper support exit immediately invokes the lower-support policy.

The previous theorem's navigation lemma remains applicable. From every state there is an internal path to the candidate target or a candidate-positive exit pair. If that predicted exit is absent under the actual model, its row differs and a completed sample supplies evidence. The completed-event/union-over-deterministic-count argument gives finite mean navigation duration. It does not assume an iid state trajectory or concentration conditional on a selected sample count.

There are three operating cases under actual theta:

1. If full rows match phi on D, then q_theta=0 and theta∈Match_phi(D). The uninterrupted U-uniform finite chain is irreducible, and every state-action pair in E(D) is visited infinitely often almost surely. Its minimum recurrent theta-priority is therefore even. On the event of no rejection, this probability-one recurrence property still holds; the argument does not declare a process conditioned on no rejection to be Markov.
2. If a used pair has positive actual exit probability, the same internal-path block bound forces a proper support exit in finite mean time, unless a test rejects earlier.
3. If actual exit probabilities are zero but some full row differs, an informative pair is recurrent and its sample-count test rejects in finite mean physical time, unless another test rejects earlier.

Matching stages that eventually reject contribute only a finite prefix, irrelevant to parity. Matching stages that continue forever satisfy parity almost surely. No pointwise statement that every pair in such a component has even priority is used.

For the true candidate phi=theta, the same split false-rejection allowance gives probability at least1−epsilon, conditional on every attempt-entry history, of a lower-support handoff or permanent operation in a valid component. Iterated conditioning over candidate cycles makes the number of attempts finite almost surely (indeed its expectation remains at most|B|/(1−epsilon)). Every nonpermanent attempt finishes at a finite physical time almost surely. Strict support changes occur at most|B|−1 times. By induction, almost every run eventually stays in a parity-winning matching component at its final support. Finite preceding phases do not affect parity.

This establishes W_B⊆V_B. Uniform operation is enough for the stated theorem. No deterministic scheduler implementation is required here.

## 6. Exact polynomial target computation

Fix B,W,theta. Start with the allowed pairs having zero theta-exit probability. Repeat:

1. Compute their maximal end components; discard pairs in no MEC
2. For each current MEC D, compute every full-row matching sigma∈B
3. If the minimum sigma-priority on E(D) is odd, say d_sigma, delete every pair of that MEC with sigma-priority d_sigma
4. Recompute until no pair is removed; return the remaining MECs

At least one pair is deleted in each nonterminal deleting round, so there are at most M pair-deleting rounds, where M is the number of initially retained pairs. Priority values are compared as binary integers; the routine does not loop through all integers below the largest priority.

**Preservation lemma.** Let E be any original qualifying end component contained in a current MEC D. A model sigma matching every row of D also matches E. If d_sigma=min c_sigma(D) is odd, there is no pair in D with smaller sigma-priority. Were E to contain a priority-d_sigma pair, its own minimum would be exactly that odd value, contradicting qualification. Therefore none of E's pairs is deleted. Removing pairs outside all MECs also preserves E. Induction shows every original valid component survives.

At termination every returned MEC has even minimum for all its matching models and is therefore valid. Every original valid component is contained in one by preservation. A strictly larger valid extension of a returned component would also survive, contradicting maximality of the returned MEC. Hence the routine computes exactly the maximal qualifying components.

Intersecting valid components have a valid union. Their internal graphs are strongly connected through a shared state, and closure and zero theta-exit are preserved. A model matching the union matches both pieces; the minimum over the union is the smaller of two even minima and is even. Thus distinct maximal qualifying components have disjoint state sets. This supports assigning a target state one containing maximal component.

For the co-Büchi specialization, give each model priority2 on its good pairs and priority1 on its bad pairs. An odd minimum is then exactly1, and deleting its minimum layer removes exactly that matching model’s bad pairs. Thus the parity routine specializes to the accepted co-Büchi pruning. Priority0 on good and1 on bad would instead encode a Büchi condition and is not the intended specialization.

Recomputation is essential: after deleting one minimum layer a different odd layer may become minimal, or removing a row can make a previously distinguishable rival match. Deleting all odd-priority pairs is incorrect; an odd priority larger than a recurrent even minimum can be necessary for connectivity.

For each support, target construction, positivity tests and graph searches are polynomial in the explicit finite system and priority bit lengths. The outer region iteration has at most|S| strict decreases. The complete bottom-up support recursion therefore has a 2^|Theta| times polynomial upper bound, as in the co-Büchi theorem.

## 7. Important countercontrols

- A forced two-state cycle with priorities2 and3 has even minimum2 and wins almost surely, while priority3 is visited infinitely. No policy in that system has finite odd-priority visit count. Thus general parity is not the earlier finite-bad-count equivalence with “bad=odd.”
- A one-state MEC with priorities1,3,4 for one matching rival needs successive deletion of1 and3 before the priority4 action remains. A single deletion pass is insufficient.
- A rival can begin unmatched because of one row that another rival forces the algorithm to delete; it must then be retested and may force another deletion.
- If an unobserved rival has identical rows but odd minimum on the entire recurrent component, checking only the candidate's parity is unsound.
- The policy must actually visit every retained used pair in an infinite matching phase. Merely staying somewhere in the component can realize a smaller, losing recurrent subset.

## 8. Posterior-deterministic POMDP corollary

Use the freshly proved initial-tag descriptor embedding from `PD_INITIAL_TAG_EMBEDDING.md`. For an arbitrary source priority c(q,a), replace its binary target lift by

    c_theta((f,last),a)=c(f(theta),a)

on defined coordinates, and any fixed priority on undefined ones. The consistency invariant makes the latter unreachable for a live actual tag. Both history-policy directions preserve the entire actual priority sequence at the same action indices, so they preserve the parity event. A positive finite initial prior makes almost-sure success equivalent to success under every initially positive tag for the same policy.

With n source states, m observations and k<=n positive initial tags, the descriptor count remains(n+1)^k(m+1). The 2^k times polynomial finite Markov procedure therefore gives an EXPTIME upper bound for almost-sure hidden parity policy existence on finite rational posterior-deterministic POMDPs. This is an upper bound for an attained qualitative objective, not a reachability-value approximation theorem, tight lower bound, finite-memory theorem or finite expected count of odd priorities.

Bordais–Raskin2026, Theorem20, is direct ancestry for the initial-tag/current-state-tuple construction, with an observation-compatible parity objective in its stated reduction. The present result must be compared at its hidden model-dependent priority interface; the construction is not credited as a newly invented model reduction.

## 9. A limited finite-observable-monitor obstruction

Two fixed models emit independent bits with parameters1/4 and3/4 under either of two always-lawful actions. Give action0 priority2 in model0 and priority1 in model1; reverse those priorities for action1. Statistical learning can eventually choose the matching action, hence wins this co-Büchi special case.

Under the constant action0 policy, however, the hidden parity success probabilities are1 and0. No fixed finite deterministic parity monitor of the observed action/bit history can realize both probabilities without new information. Under that fixed action policy, the monitor induces finite Markov chains with the same positive-support graph in both models. Their reachable bottom recurrent classes and their assigned priorities are the same, so their almost-sure parity classification is the same. It cannot be probability1 in one model and0 in the other.

This rules out that direct information-preserving finite-monitor shortcut only. It does not rule out all reductions, infinite-memory monitors, model-dependent target families or transformations that change the observation/objective contract. It supplies a concrete scope guard for comparisons with visible-priority theorems, not a novelty argument.

## 10. Evidence ceiling

The component lemma, all-policy tail transfer and phase argument are ordinary mathematics. Brute-force controls compare the pruning result with exhaustive valid components, and test finite-policy necessary conditions; they do not establish the infinite theorem by themselves. Dependency source bytes, fresh review receipts and current controls are bound before qualification. No old missing audit archive is reused and no canonical source is modified.
