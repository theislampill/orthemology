# Exact memory under evidence reset and guarded revision

9 October 2026. Ordinary mathematical proof, not a kernel certificate.

## Contract

Let n be finite, X={0,1}^n, and h:X→Y any fixed output map. Y can be a vector of exact scoped terminal-certificate minimum checking costs, with infinity for no eligible certificate. It may instead be a declared finite tuple of other outputs. All X states are admitted. There are independent total actions R(i,b) setting coordinate i to b, for each i and b in {0,1}. There are also finitely many specified total coupled actions T_a:X→X. All action words are admitted at every state. The same action label has the same interpretation in both compared states. Output is observed initially and after any finite word.

Define x≈y iff h(T_w(x))=h(T_w(y)) for every finite word w, including the empty word. A summary is continuation-complete for these outputs if it decodes h and has a well-defined update for every named action.

For f:X→Z let Ess(f) be the set of i for which some two states differing only at i have different f-values. Start I0=Ess(h). Recursively put

I_(r+1)=I_r ∪ ⋃{Ess((T_a)_j): a a coupled action, j∈I_r}.

Let I* be the stable union. Resets need not be included explicitly; their jth components depend only on j or on no coordinate. This is semantic dependence, not occurrence of a variable in a source expression.

## Theorem 1: exact backward-dependency closure

x≈y if and only if x and y agree on I*.

Consequently projection to I* is the coarsest continuation-complete quotient, there are exactly 2^|I*| equivalence classes, and any fixed-width lossless binary encoding of this control state requires at least |I*| bits. The projection attains that bound. This is not a lower bound of |I*| real coordinates or an active-RAM bound with a free external archive.

### Proof of sufficiency

For any finite-coordinate function f, agreement on Ess(f) implies agreement on f: change all other coordinates one at a time, and each change preserves f by nonessentiality. If x,y agree on I*, they therefore have the same h-value. For every j∈I*, all essential coordinates of (T_a)_j belong to I*, so T_a(x),T_a(y) again agree on I*. Independent resets also preserve this agreement. Induct on any action word. For an explicit implementation, zero-fill the forgotten coordinates of a retained vector z, apply the named action, and restrict its output back to I*. Closure proves independence from the fill values. Decode h using the same zero-filled representative. This proves sufficiency and constructs quotient updates.

### Proof of necessity

Induct on the stages I_r to prove the stronger statement: for every i∈I_r and every x,y with x_i≠y_i, some common action word distinguishes their h-outputs. The other coordinates of x,y may differ.

For i∈I0, choose an essentiality witness u,v differing only at i, with h(u)≠h(v). Reset every coordinate except i to its common value in u,v. This one common reset word takes x,y to u,v in one order or the other. It distinguishes their outputs.

For a newly added i, choose a coupled action T_a and j∈I_r such that i∈Ess((T_a)_j). Pick u,v differing only at i with (T_a(u))_j≠(T_a(v))_j. As before, reset every coordinate except i to the common witness values, then apply T_a. The resulting pair differs at j. The inductive statement supplies a common suffix distinguishing its outputs. Thus every pair differing at any coordinate in I* is distinguishable. Necessity follows.

If coordinate i is first added at depth d, this construction uses at most (d+1)(n−1)+d actions. For a nonempty output support, d≤n−|I0|, so n^2−1 is a universal upper bound when n≥1. If I0 is empty, h is constant, I* is empty and every state is equivalent. The n=0 case has one state. No optimal distinguishing-length claim is made.

Coarseness follows because any summary with output decoding and action updates must assign different summary states to any distinguishable pair. Every assignment on I* is represented in X, giving exactly 2^|I*| classes. ∎

## Corollary 2: reset-only memory

With no coupled actions, I*=Ess(h). Independent grant/withdraw status changes therefore require retaining precisely the currently held values of semantically essential coordinates, even when the present output is identical. This is an exact statement about the independent reset alphabet, not an assertion that actual trust changes or source versions obey it.

## Theorem 3: positive certificate specialization

Fix finitely many scoped verdicts and, for each verdict v, a finite catalogue C_v of support/cost pairs (S,k), S⊆{0,…,n−1}, k finite and nonnegative. At inventory K define

h_v(K)=min{k:(S,k)∈C_v and S⊆K}, with min empty=infinity.

Let A_v be the global antichain obtained by removing duplicates and pairs dominated by (S',k') with S'⊆S and k'≤k, at least one strict. Let E be the union of all supports in all A_v. Then Ess((h_v)_v)=E. Thus, under reset-only transitions, the exact minimal control state is K∩E. With coupled transitions it is K restricted to the backward closure of E in Theorem 1.

### Proof

Global dominance cannot improve any h_v(K), so deleting dominated pairs preserves all outputs. No output depends on a coordinate outside E. Conversely, let i∈S for some undominated (S,k)∈A_v. At K=S the least cost is k: a strictly cheaper feasible pair would dominate (S,k). At K=S\{i} the least cost is strictly larger than k or infinity, since any eligible pair of cost at most k would again dominate it. These inventories differ only at i, proving essentiality. ∎

This theorem concerns terminal eligible costs, not certificate IDs, human knowledge, completed verification or dispatch permission. For a different declared output, recompute h and its dependencies. A retained witness catalogue/reconstruction channel is needed to produce an actual eligible proof and perform the current check. Its storage is not eliminated by this decision-state theorem.

## Source-specific discriminator: why current residual pruning fails

Take one verdict Q and two admitted proofs, support {a} and support {b}, each terminal cost 1. CP23's current missing-support/cost frontiers at K={a} and K'={a,b} both normalize to {(empty,1)}. Their whole acquisition-only continuation-cost functions coincide, as CP23 proves. Clear a. K becomes empty, with cost infinity; K' becomes {b}, with cost 1. No update defined on that one frontier value can implement the same named withdrawal correctly for both inventories.

This does not refute CP23's theorem: clear a was expressly outside its persistent-evidence alphabet. It shows exactly why the old normalized state cannot simply be reused after extending the operator contract. A particular proof reference selected behind the frontier can accidentally distinguish these two inventories, but both can legally select the {a}-proof. CP23's theorem is about the canonical support/cost pairs and permits equal-pair witness references to vary. Retaining one selected proof is still not a general substitute for all future-relevant evidence distinctions.

Global dominance remains safe: if {a} at cost 1 dominates {a,b} at cost 2, the latter cannot improve the output at any inventory, before or after arbitrary status resets. The error is discarding an alternative because currently available evidence made its residual support redundant, not deletion of a globally dominated support/cost pair under fixed semantics.

## Guarded-action discriminator

Let x=(a,b), terminal h(x)=a, and let T(a,b)=(a AND NOT b,b). Here a is current proof eligibility; b is an explicitly supplied guard-status input to a permitted conditional withdrawal, not an inferred truth about a source. I0={a} but I*={a,b}. The states (1,0),(1,1) presently give the same terminal result and have the same a-value; one T action yields different results. A support-only summary fails even when it preserves all current terminal proof dependencies. The action's control dependency is also a future certificate-status/output dependency. This is a model-level statement, not a new claim that the bit controls human warrant.

A chain T_j clearing j conditional on j+1 propagates this burden through coordinates absent from every terminal support. Reset contexts make each chain link's dependency independently exposeable. This is the additional constructive result beyond recording alternative proof supports.

## Limits and material controls

1. Without independent resets the closure can overestimate. For h=a OR b and acquisition-only actions set a/set b, all three nonempty inventories are equivalent, despite both coordinates being essential. There are two continuation classes, not four. General restricted protocols require their actual transition congruence; no lower bound follows from inadmissible distinguishing words.
2. Theorem 1 permits any output and total action maps but requires a finite product of independent Boolean coordinates. Correlated admissible states, monotonic epoch counters, forbidden actions, observable refusals, unbounded source histories and newly appearing rules require another model or a proved abstraction. A true actual permission guard must not be replaced by its desired value.
3. Semantic dependence can be strictly smaller than syntactic support: (a AND b) OR (a AND NOT b) equals a. The exact theorem uses cofactors, not a raw variable-occurrence graph.
4. If negative guards occur, absence of a token is not a certified negation. Each Boolean guard must already have the admitted meaning required by the proof contract. The theorem neither validates a closed-world assumption nor computes undefeatedness from silence.
5. An authenticated artifact's identity is not its truth; a mathematical status reset is not an authority to withdraw trust. Any regained terminal eligibility still requires the current proof check and new authorization when the protocol requires them. It never revives an old version-bound licence across ABA.
6. Objective corrigibility and source commitments remain externally warranted premises. These constructions provide continuation-correct state maintenance, not discovery of true premises, human operative basing, metaphysical possibility, or defeat of the preserved positive philosophical appraisals.
