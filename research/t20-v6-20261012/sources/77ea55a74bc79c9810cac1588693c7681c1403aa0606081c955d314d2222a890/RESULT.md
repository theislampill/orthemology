# From guarded proof compilation to live inquiry: checked caches, commitment, and controller memory

11 October 2026 UTC. Additive research in a separate workspace. Existing v2/v3 material and every inherited source remain unchanged. Ordinary mathematical proofs and exact executable diagnostics; no new Lean certification, repository adoption, physical-cost calibration, source authentication, or change to the affirmative foundational judgments.

## Result in brief

There is a constructive bridge between the guarded shared-proof compiler and adaptive inquiry, but its exact boundary is the **cost and validity of already performed checking**.

1. The actual inherited normalizer can reduce the static cost of a proof from 14 to 12 while raising its *remaining* checking cost from 2 to 12. It redirects a cached parent's premise, thereby changing the very node identity whose earlier check could be reused. This does not contradict the inherited fixed-charge theorem.
2. At a fixed source/version snapshot, the correct remaining-cost optimum is obtained by adding each currently valid checked node as a zero-price, exact-support macro. The inherited finite whole-DAG compiler then applies. Expanding its result supplies a genuine proof with at most `|J| 2^|E|` newly checked nodes, besides the retained cache. This closes a concrete cache-relative compilation gap without inventing scalar child-cost optimization.
3. Under explicit non-interference and terminal-reproducibility conditions, arbitrary interleaving of successful proof checks with adaptive acquisition cannot beat acquisition followed by this cache-relative terminal compiler. Checking can be postponed, pathwise. Thus the static *terminal compilation method* survives a substantial adaptive extension. It does not mean a single proof chosen before the observations stays optimal.
4. Source revision requires a separate cache-validity dependency profile. A zero-cost exact-state availability table is sufficient at one snapshot; it need not remain sufficient after a rule/source withdrawal. An antichain of complete dependency sets per exact state restores the stated all-revision availability contract. This is a specialization of the inherited positive-support/frontier machinery, not a new minimal-sidecar theorem.
5. The older restorative controllers impose another boundary: under the full-support CIRS contract, a stationary finite-memory common controller can restore all standards exactly when their good-action sets have a common member. CIRS can succeed with unbounded likelihood memory when that intersection is empty. Finite typed sidecar realization therefore cannot be substituted for the older controller. A simple rational-integer implementation, and the inherited primitive-recursive source compiler, identify a positive unbounded-data route instead.

The costs of a complete committed policy must still be combined under the same hidden source model. ET-17 already proves the required policy-vector construction. Neither a correct cache nor an actual typed table licenses independent worst-model selection on different branches. Timed reuse additionally needs ET-19's complete timing contract.

## 1. Actual owners and the gap that remains

The investigation followed `proofs/SOURCE_REGISTRY.json`, `evidence/SOURCE_MAP.json`, and the restored baseline source map to the actual owner texts and selected source files. `SOURCE_BINDINGS.json` records the exact objects and reading scope. Reports are not silently counted as fresh Lean execution.

- PT-01/02's **Warranted completion with proof-sensitive memory and inquiry cost**, §§2–4, fixes a terminal proof price, distinguishes availability from an executed check, and explicitly excludes arbitrary fragment scheduling/reuse. Its finite inquiry theorem minimizes worst *realized path* cost with persistent evidence and fixed one-use tests.
- PT-03's **Compiling certificate frontiers from finite grounded rules**, §§2–5, separately prices occurrence trees and shared DAGs. It already transports a complete terminal DAG catalogue into that inquiry theorem. It does not prove that interleaved checking or a pre-existing cache can be erased.
- PT-04/05's **Exact-support compilation for source-sensitive proof rules** and actual `guarded_compiler.py` preserve the ordered exact support tuple. Intermediate subset-Pareto pruning can destroy a needed nonmonotone guard. Tree minima are not shared-DAG minima.
- PT-07's **Exact-state normalization and attainment for guarded shared proof DAGs**, together with the actual `guarded_dag.py`, preserves the root's exact state and lowers a sum of fixed nonnegative occurrence charges. The code literally redirects references. The owner explicitly excludes node-identity-sensitive guards and does not preserve original certificate identity.
- PT-06's **Shared proof cost and retained overlap information**, §2, permits cross-branch reuse only with globally aligned identities denoting the same rule, ordered references, scope, and price. Its final paragraph expressly excludes cache invalidation. Full node incidence already determines fixed-bundle cost; the tensor/intersection discussion is not an optimizer.
- ET-14's dependency replay theorem requires a current cache, complete dependencies, and unchanged definitions or definitions represented as changed inputs. Its separate survival theorem concerns the supplied witness family. Neither turns a formerly valid source binding into a current one merely by retaining its identifier.
- ET-17 owns fixed-model expected policy vectors and the ex ante commitment distinction. ET-19 owns the joint holding-time/outcome/next-state repair.
- PT-19/20 actually realize finite tables in original Has and transport rational joint kernels under the stated seed-fibre condition. Their source carriers are naturals; their *finite represented domain* and legal-action/policy interface remain separate. They do not implement arbitrary history policies.
- The restored CIRS owner explicitly uses unbounded likelihood memory. The actual restored Sixteenth reader's direct-controller account, §§1,4,12–13, has one common policy before quantifying the model, and unbounded history/counts. Its finite certificate is not a finite-state controller.

The new obligations addressed here are thus neither another proof of finite DAG attainment nor another generic Bellman algorithm. They are (a) transporting that attainment through executed, reusable checks; (b) identifying when the interleaving of acquisition/checking changes nothing; and (c) separating finite typed-state realization from inherited unbounded restorative control. No exhaustive programme-wide priority claim follows from the selected reading.

## 2. The exact cache contract

Keep the inherited finite guarded grammar `(J,E,R)`:

- fully scoped judgments `J`;
- evidence identities `E`;
- finite immutable admitted rules with ordered premises, local support, fixed nonnegative price, and a guard of the ordered exact child supports;
- finite acyclic proof DAGs whose support is the union of local evidence, and whose static checking price is the sum over distinct nodes.

For this extension, give proof nodes globally aligned immutable identities. Equal identities mean the same rule record, same ordered child identities, and same scope/version metadata. Renumbering storage indices alone need not change identity; changing a premise identity does. The reference code uses complete structural records as collision-free mathematical identities. It does not assert that every production proof store must use this representation.

Let `C` be a finite **currently valid checked cache**, downward closed under premise references. Each cached node denotes a recoverable previously checked proof. A cache receipt is usable only under the present source, interpretation, rule, and version contract. Its children are included in `C`; this prevents an opaque “free” parent from omitting a required paid dependency.

Let `K⊆E` be the current live inventory. Cache validity and proof eligibility are separate from historical payments. If a cache node loses validity, its earlier cost remains sunk. Revocation does not refund it, prove its conclusion false, or erase its historical certificate.

For a valid candidate proof `D`, write `F(D)` for its aligned node footprint. With node weight `w(v)` fixed by its immutable rule record, define the additional checking charge

\[
 c_C(D)=\sum_{v\in F(D)\setminus C}w(v).
\tag{1}
\]

Every referenced noncached node must actually be checked. Cache lookup, storage, authentication, and revalidation are free only within this declared model; a nonzero such price must be included explicitly and may require a different reuse rule. No measured-runtime claim is made.

This is a new cost contract applied to the old proof syntax. In particular `(judgment, exact support)` remains sufficient for the old parent's *guard*, but need not identify which concrete parent application was already paid for.

## 3. A source-executed negative transport

Use one evidence token `e` and these admitted rules:

- `qa`: `e` proves `q`, charge 1.
- `qb`: `e` proves the same `q`, charge 2.
- `rq`: from `q`, prove `r`, charge 10.
- `tqr`: from ordered premises `(q,r)`, prove `t`, charge 1.

All guards accept their declared exact supports. Let `qa`, `qb` also denote the two concrete leaf nodes, and let `rb = rq(qb)`. The current checked cache is `{qb,rb}`; its historical checking cost is 12.

Consider the supplied DAG

\[
 D=tqr(qa,rq(qb)).
\]

Its static charge is `1+2+10+1=14`. Its remaining charge is 2: only `qa` and the terminal node are new. Give the supplied DAG the premise-first order `qa,qb,rb,t`.

The actual unchanged inherited normalizer picks `qa` as the earliest exact `q,{e}` state and redirects `rb`'s child. Its output is

\[
 N(D)=tqr(qa,rq(qa)).
\]

The root and every guard support are preserved. Its static charge is 12, just as PT-07 promises. But `rq(qa)` is a different node from `rq(qb)`. It has not been checked. Its remaining charge is also 12, up from 2.

The true cache-relative optimum is instead `tqr(qb,rb)`, with remaining charge 1 and static charge 13. Thus even the globally cheapest static proof (charge 12) can be worse than a statically more expensive one when previous work is committed.

`test_actual_inherited_normalizer_loses_cached_identity` executes the pinned normalizer itself. No variant of the normalizer is substituted. The finding is not a bug in its stated objective: the cache identity contract is additional, and the owner already distinguishes identity-sensitive semantics.

For a fixed family of candidate proofs and a static minimizer `D*`, equation (1) gives an exact retained-optimality check:

\[
D^*\text{ remains optimal from }C
\iff
W(F(D)\cap C)-W(F(D^*)\cap C)
\le c(D)-c(D^*)\quad\forall D.
\tag{2}
\]

This merely rearranges the marginal-cost inequality; it is not a new optimizer. It identifies what must be compared: a competitor's cached-work advantage against its static disadvantage. A static value alone cannot supply that comparison.

## 4. Cache-cut compilation theorem

**Theorem 1.** Under §2, every attainable exact root state has an attained minimum additional checking charge. It can be found by a finite guarded whole-DAG compilation in which each valid checked node is added as a zero-price nullary macro with that node's original judgment and **exact support**. A minimizing expanded witness has at most `|J| 2^|E|` newly checked nodes, in addition to nodes from `C`.

This is a reduction to the inherited PT-07 theorem, not a new solution of general shared-proof synthesis. Effective enumeration additionally requires decidable guards and exactly computable price addition/comparison, as with the reference implementation’s rational prices. Arbitrary fixed nonnegative real prices support the mathematical attainment statement without an automatic executable comparison procedure.

### Construction

For each `v∈C`, add a distinct admitted *representation macro*

\[
 m_v:\quad\varnothing\longrightarrow (q_v,S_v),\qquad
 B(m_v)=S_v,\quad w(m_v)=0,
\]

with an expansion pointer to the actual cached proof rooted at `v`. The macro is nullary only at this representation layer: it does not turn the cached conclusion into an unauthenticated axiom. Its exact local support makes every downstream guard see the old support. Macro names cannot collide with original rule names.

The enlarged guarded grammar is finite, retains the original judgment/evidence sets, and has nonnegative prices. Compile exact states using PT-07's whole-graph method. Do not substitute the exact-support *tree* table or scalar cheapest-child selection.

### Forward inequality: cut a genuine proof at cached nodes

Take any actual proof `D`. Traverse from its root, stopping at every node in `C`; replace that stopped subproof by its macro. Keep all remaining noncached nodes and their original sharing. Since `C` is downward closed, every removed descendant is cached. Thus the cut graph's static charge is exactly `c_C(D)`.

The exact support of each stopped subproof is unchanged. Induction through the remaining graph preserves every ordered child-support tuple, each rule guard, and the root state. The cut graph is acyclic and valid in the enlarged grammar. Therefore the enlarged grammar's minimum is no greater than `c_C(D)` for every `D`.

### Reverse inequality: expand a compiled witness

Expand each macro by its recoverable cached proof, with globally aligned identities. Distinct macros may share cached dependencies; count those only once, at zero additional charge. Build ordinary nodes in premise-first order. Their ordered support tuples remain identical, so guards and root state are preserved.

For structural identities, the expansion is an ordinary finite term DAG and hence acyclic. Equivalently one can allocate genuinely fresh noncached application identities after all their children and reuse a cached identity only when its entire application matches. A cached proof cannot acquire a dependency on a newly allocated node by this expansion.

Each charged ordinary macro-graph node produces at most one new checked node. If expansion coincides with an already cached node or another identical ordinary node, the additional charge can only decrease. Consequently the expanded witness's additional charge is no greater than the macro witness's static charge.

Apply the forward inequality to that expanded proof. Together the two inequalities imply equality of the optimum values. PT-07 supplies a minimizing macro witness, so this also proves original minimum attainment; it is not only an equality of infima.

Finally PT-07 normalizes the *macro graph* to at most one node per exact state, hence at most `|J| 2^|E|` nodes. Expanding its macros adds only cached nodes. Thus no more than this many nodes need a fresh check. The expanded graph can contain many cached nodes of the same exact state; the theorem does not demand their destructive identity normalization.

### A useful positive compression, and its limit

At a single fixed snapshot, the *set of exact states represented somewhere in the valid cache* suffices to determine all minimum remaining terminal prices: equal-state zero-price macros are equivalent for that numerical objective. One need not retain every node identity in the planner's active numeric summary. A reconstruction channel must still retain a real cached witness for each selected macro.

This does not contradict §3. Computing the cost of one already specified proof requires its real node incidence. Synthesizing some cheapest valid proof can replace an eligible cached proof by an abstract zero-cost macro and later reconstruct it. These are different observation contracts. Nor does snapshot availability predict which macros survive later source revisions.

## 5. Revalidation profiles and the source-revision boundary

Take two caches from the same grammar:

\[
 C_0=\{qa,rq(qa)\},\qquad C_1=\{qb,rq(qb)\}.
\]

They expose the same exact cached states `q,{e}` and `r,{e}`. Each currently gives terminal minimum 1. Withdraw the admission of rule `qa`, leaving `qb` and the other rules admitted. The first cache loses both nodes, while the second retains both. The new remaining minima are 13 and 1. Evidence token `e` can remain present throughout.

This is why the full rule/source-version dependencies of a checked node cannot be replaced by its conclusion, its present validity bit, or its evidence-leaf support alone when admission revisions are permitted. It is also why a corrected source must not be silently transplanted into an old certificate while retaining that old certificate's identity.

For one precisely bounded revision model, the old support-frontier machinery already gives a constructive repair. Let `Δ` be a finite dependency universe, including every material evidence, rule, interpretation, scope, and version condition. Each previously checked node `v` has a complete fixed dependency set `d(v)⊆Δ`, with parent dependencies including child dependencies. Let `L⊆Δ` be the currently live conditions. **Stipulate and justify**

\[
 v\text{ is reusable now}\iff d(v)\subseteq L.
\tag{3}
\]

Equation (3) is not a theorem of authentication. Non-conjunctive defeat, changing meanings, expiry clocks, and missing dependencies require a richer validity model.

For each exact guarded state `x`, retain the inclusion-minimal sets

\[
\mathcal A_C(x)=\min_{\subseteq}\{d(v):v\in C,\; (q_v,S_v)=x\}.
\tag{4}
\]

Then a zero-price macro at `x` is available iff some `D∈A_C(x)` satisfies `D⊆L`. The profile is sufficient for every live-condition set `L` and every sequence of declared condition activations/withdrawals. It is the coarsest profile preserving those *macro-availability* observations: the inclusion-minimal `L` at which availability becomes true recover exactly the antichain. This is PT-01's finite support-continuation argument with zero prices and exact-state-indexed outputs, combined with ET-14's complete-dependency requirement.

The small `dependency_frontier` helper implements the special case of declared rule-local dependency factors, unioned with child dependencies. Arbitrary occurrence-specific dependencies in equation (3), such as receipt-specific validity conditions, require a node-indexed dependency input; that broader extraction is not implemented by the helper.

It is not necessarily the coarsest profile preserving only optimized terminal values: a zero-price original rule might make a cache distinction numerically redundant. Nor does it preserve full historical proof identity, sunk costs, or arbitrary future workflows. For all-revision terminal compilation under (3), it supplies exactly the currently eligible macros; Theorem 1 then applies to the current grammar.

Do not Pareto-prune the *exact evidence supports* before a later nonmonotone guard. Equation (4) prunes external validity dependency sets **within the same exact guarded state**. That distinction is essential.

## 6. When interleaved checking can be postponed

The previous theorem is about a snapshot. The acquisition question is whether it remains enough when checks and queries can be scheduled adaptively.

Fix an observation-history acquisition process, possibly with externally specified source revisions. Let a policy be allowed to interleave queries and proof-check operations before producing one terminal proof. Impose the following conditions:

1. Every permitted check is an admitted, deterministic, successful check of an available proof node. It emits no new observation and does not reveal source reliability or candidate validity. A possibly failing validation is instead an outcome-bearing inquiry.
2. Queries, query permissions, their conditional joint outcomes, and their acquisition charges are independent of which checks have already run. Their policy may depend on the same public history and independent private coins. No query requires a previously produced certificate as an access credential.
3. Checks do not change physical inquiry time or the event law, consume evidence, reserve resources, lock an interpretation, or affect later prices. Alternatively the application supplies an explicit commutation/dominance argument covering those effects. A bare permission guard is not a timing semantics.
4. Any terminal proof actually produced is reproducible from the terminal evidence/source snapshot, its recoverable node records, and the still-valid part `C_h` of the initial cache. Every terminal noncached node can be checked at the terminal snapshot for its same fixed nonnegative price. No earlier check obtains an irreplaceable time-limited entitlement.
5. The declared objective is the sum of nonnegative query/check charges and the same terminal outcome, ending after that single certificate. Earlier checks cannot provide an additional externally valued deliverable. Offline simulation and reconstruction are outside this execution-charge model, just as in the inherited compiler.

**Theorem 2 (postponement).** Every successful interleaved policy has a lawful policy with the same query/outcome behavior that checks only at termination and has no greater charge on every coupled realized history. The delayed policy may use the cache-cut optimum at each terminal history, again without increasing charge.

**Proof.** Fix the policy's private random realization when one is used. Simulate its check choices internally, maintaining the same virtual cache and internal decision state, but execute none of those checks. By conditions 1–3 this simulation introduces no missing observation and does not change a query's availability, law, price, or chosen action. Thus it produces the same external query history, including the same source revisions, on the coupled run.

At a terminal history `h`, take the actual proof the original policy would return. Condition 4 makes every node outside `C_h` checkable now. Check just those nodes, in topological order, once each. The original policy must have paid for each such node at least once: it is neither a still-valid initially checked node nor an unchecked premise. It may additionally have checked abandoned alternatives, invalidated nodes, or the same node more than once. Nonnegative fixed prices therefore give a pathwise no-larger checking sum. The query charges and terminal outcome are unchanged. Finally Theorem 1 selects a no-dearer valid terminal proof. ∎

The construction is a dominance argument, not a polynomial policy compiler. An original policy may have arbitrarily complicated internal computations. It does not assume those computations are free in reality, only that the declared objective has the inherited acquisition/checking boundary.

### Consequences and sharp failures

- With no initial cache and no source revisions, the existing terminal DAG catalogue is sufficient even against the newly allowed class of non-informative interleaved checking schedules. The actual adaptive acquisition policy can still choose different terminal proofs after different observations.
- Source revision is allowed if conditions 1–4 hold and the terminal compiler uses the current grammar and surviving cache. PT-02's *full-transcript union feasibility test* does not follow: evidence can expire or be withdrawn. The theorem concerns delayed checking, not the false union of all historically seen tokens.
- A query unlocked only by a checked credential breaks condition 2. A terminal-only policy may then be unable to acquire the evidence at all.
- An informative validation breaks condition 1. Its response must be included in the inquiry law, rather than simulated as certain success.
- An early-only price discount, an expiry deadline, or a proof that must be checked before a source disappears breaks condition 3 or 4. Delaying can cost more or become impossible.
- Several sequential service obligations can make early reusable work instrumentally valuable. Their end-to-end policy needs a declared multi-goal state/cost contract; this theorem does not collapse that service into one terminal certificate.

A sufficient transparent commutation contract has been proved. These conditions are not asserted necessary for every individual instance: an excluded feature may be harmless in a special case. Equation (2) is an exact test for a chosen static proof, while Theorem 2 is a structural sufficient condition for the scheduling reduction. Keeping those quantifiers separate avoids a misleading general “if and only if.”

## 7. Costs, fixed source models, and actual typed execution

Postponement is pathwise. Hence it preserves or improves expected charge under each fixed model and the supremum over any stated model family. It does not justify selecting a new worst model at each hypothetical branch.

For an actual committed finite policy, the additional check bill along a realization is the weighted union of the node identities actually checked, with the explicitly authorized reuse convention. Distinct mutually exclusive branches are not a simultaneous proof bundle. Their contingent checks are charged only on the branch executed, and then averaged under that model's probabilities. Conversely work performed before the branch is a sunk common-prefix charge, not refundable when the other branch occurs.

ET-17's existing `L` fixture already proves why whole-policy model coordinates are required. Its common audit masses are `(1/4,3/4)` and the two conditional-cost vectors are `(9/10,1/10)` and `(3/10,7/10)`. Keeping a single model yields total vector `(9/20,11/20)`, maximum `11/20`. Independent branchwise maximization yields `3/4`, corresponding to a pasted law outside the declared segment. These numbers are inherited; the diagnostic recomputes them to show the cache bridge does not relax that interface.

A finite declared cache/revision/inquiry state can feed the existing D1/ET-09 refinement only after all its labels, menus, costs, and joint transitions have been supplied. PT-20 then gives an exact finite-uniform-seed implementation when that joint kernel is rational. A source-table code does not discover complete dependencies, enforce the menu, choose a lawful information policy, or generate calibrated randomness. An out-of-range source fallback is not an authorized state.

PT-28/29 do not fill this gap by their stronger literal probability proof. They establish a different source-lowered observer's actual fair-input stopping-prefix law and atomic-defect formula, while preserving the explicit Python/serialization/host boundary. Neither finite proof-check cost nor authority is an atomic defect. The correct crosswalk preserves the distinct source, probability, policy, and cost assertions instead of treating “kernel checked” as a universal transport licence.

If checking duration affects source expiry, response timing, or a cost rate, ET-19 requires the complete joint holding-time/event/next-state law. Equality of untimed cache updates and separate time marginals is insufficient. The present code is an untimed exact-charge diagnostic.

## 8. CIRS is not a finite-sidecar controller theorem

CIRS has a fixed hidden standard `θ`, finite actions and observations, strictly positive conditional observation laws `Pθ,a(y)`, common lawful actions, and model-specific target-good sets `Gθ`. It asks for only finitely many target-bad actions, almost surely under every standard, using one common history policy. Its accepted constructive argument uses likelihoods and candidate-specific cyclic pointers, allowing unbounded memory.

Consider instead a **time-homogeneous finite-memory behavioral controller**. Its finite memory state includes every controller-visible retained quantity. At each state it chooses an action by a fixed distribution, then updates memory according to that state, action, and receipt with model-independent private randomness. Its initial memory distribution is common to all standards. There is no uncounted clock, external archive, growing integer, or seed that encodes the standard.

**Proposition 3.** In the strictly positive CIRS model, such a controller restores under every standard iff

\[
\bigcap_\theta G_\theta\ne\varnothing.
\tag{5}
\]

**Proof.** The induced finite memory-chain transition has a positive edge exactly when some controller-enabled action, some observation, and some controller update allow it. Every observation has positive probability under every standard. The reachable directed graph, and all its reachable bottom strongly connected components, therefore are the same under every standard.

Every reachable bottom component is entered with positive probability under every standard. Within that finite irreducible component, each recurrent memory state is visited infinitely often almost surely, and every action given positive probability there occurs infinitely often. Let `U_B` be the nonempty union of those action supports. It is independent of the standard. Almost-sure restoration for every standard requires `U_B⊆Gθ` for every `θ`; otherwise a bad action recurs on an event of positive probability. Any member of `U_B` is therefore in the intersection in (5). Conversely, a constant common-good action is a one-state restoring controller. ∎

This is an elementary finite-chain/support corollary, not a new general POMDP theorem. Its value is the exact bridge obstruction to the current finite typed-sidecar architecture. Allowing a time-dependent controller without counting its clock, or feeding it the old unbounded likelihood state externally, changes the finite-memory premise.

For CIRS's positive D2 pattern, use two standards, two actions `a0,a1`, target sets `{a0}` and `{a1}`, and under either action let the receipt be Bernoulli `1/3` under standard 0 and Bernoulli `2/3` under standard 1. Each singleton target support distinguishes the rival, so inherited CIRS supplies a common unbounded-memory restorative policy. But the intersection is empty, so Proposition 3 rules out every finite-memory controller of the stated kind, even randomized ones. Finite-memory failure and a finite *description* of a successful algorithm coexist.

### A positive unbounded-data source route

For any fixed finite rational CIRS instance choose a common denominator `D` for all kernel entries and write `Pθ,a(y)=nθ,a,y/D`. Starting from `wθ=1`, maintain integer weights

\[
 w_\theta(t+1)=w_\theta(t)\,n_{\theta,a_t,y_t}.
\]

Then exactly `L_t(θ)=wθ(t)/D^t`. All likelihood comparisons, including a fixed tie rule, are unchanged. The candidate pointers remain bounded by their finite support sizes; the weights do not.

The one-step update is primitive recursive: multiplication is inherited `mulPR`; finite kernel lookup is the actual `lookupPR`/`tablePR` mechanism; comparison is constructed from `reverseSubPR` and zero branching; a finite argmax is a fixed finite comparison fold; bounded pointer cycling is a finite lookup. Consequently the already proved `PR.compile_has` and `PR.compile_obs` supply typed original-Has numeric realizations of these one-step functions. Their pointwise correctness can be composed along every finite supplied observation history. This is a representability corollary of the actual inspected source interfaces, not a claim that the included Python program has been compiled to Has or that a new Lean controller/law theorem has been checked.

The inherited CIRS probability proof applies when execution really follows that same action policy and the environment satisfies its controlled conditional law. Repeated copies of one source bit do not satisfy it; source typing cannot repair the missing acquisition premise. The fixed-size tag theorem is avoided by retaining unbounded ordinary numeric data, not by hiding a growing likelihood inside the trivial identity-proof slot.

This makes the connection constructive without overclaiming: the source language already has the relevant arithmetic expressivity; the finite-table result alone does not establish this application, and a complete literal source-controller composition/probability audit remains a separate implementation task.

## 9. Verification, ownership, and what remains open

The standalone reference adapter preserves the three inherited Python files byte-for-byte. Its tests call the actual normalizer and whole-DAG compiler, recheck expanded admitted rules and guards, compare cache-relative minima against direct finite proof-object enumeration, and reject invalid/stale/non-dependency-closed caches. Exact arithmetic is used throughout.

The control suite also checks the scheduling reduction on a small explicit action system, the fixed-model versus pasted-branch calculation, the finite-memory CIRS obstruction on all deterministic controllers with one through three memory states, and integer likelihood histories against their rational definition. General theorems rest on the written proofs, not these finite checks. Commands, case counts, negative controls, source hashes, and observed outputs are in `VERIFICATION.json` and the run logs.

New-to-this-selected-interface contributions are Theorem 1's cache-cut transport, §3's actual-normalizer counterexample, and Theorem 2's explicitly scoped interleaving reduction. The revalidation antichain is an inherited frontier specialization. Proposition 3 is standard finite-chain reasoning applied to the source's CIRS/finite-sidecar boundary. Clearing rational likelihood denominators and primitive-recursive representability are standard constructive steps, here tied to actual source interfaces. ET-17's numerical fixture and policy-vector theorem, PT-07's static attainment, CIRS restoration, and restored T16 controller extraction keep their original owners.

The adapter is not a scalable optimizer or a deployed proof store. Complete real source dependencies, warranted rule admission, calibrated costs/likelihoods, hidden-state information policies, timing, and identity-preserving physical execution remain application obligations. The philosophical record remains affirmative at its established source-specific scopes: a lost route does not defeat surviving grounds, a proof record does not establish a person's operative basing, and a typed identity proof does not authenticate evidence or furnish metaphysical warrant.

A concrete handoff is now available: use cache macros to instantiate one bounded proof-producing inquiry with complete version dependencies; check the postponement premises before using the terminal compiler; and retain one fixed source model through the policy's full cost evaluation. The work does not require re-proving the old finite attainment theorem or claiming that every restorative controller fits a finite sidecar.
