# Exact-state normalization and attainment for guarded shared proof DAGs

9 October 2026. A narrow T20 compiler-interface clarification. Predecessors remain read-only; no integration, adoption, programme closure, or historical time credit.

## Result and exact credit

**Yes.** Under the actual fixed ordered-support guard contract and nonnegative once-per-node checking prices, every supplied valid finite acyclic proof DAG has a valid DAG of the same root judgement and **exact** support, no greater total checking price, and at most one node per exact state `(q,S)`. It therefore has at most `|J| 2^|E|` distinct nodes. Finite ground rules and evidence yield a finite whole-graph catalogue; every reachable exact root state has an actually attained cheapest shared-DAG proof.

This is an explicit transport of two inherited ingredients, not a new general finiteness method:

- `source-sensitive-proof-compilation-20261009/RESULT.md:90–96` already describes finite ordinary-grammar refinement to `(q,S)`; §5, especially line 131, explicitly withholds a guarded DAG compiler and warns that unrefined redirection changes supports.
- `certificate-compilation-boundary-20261009/RESULT.md`, §4, already proves earliest-occurrence normalization and finite whole-rule-choice enumeration for unguarded DAGs.

The bounded inspection found no existing explicit graph/guard/exact-support/cost-preserving combination in those packets, their inspected guarded tree kernels, or the local textual hits for guarded-DAG/earliest-exact-state terminology. The refinement observation already makes the route apparent. The present increment is spelling out and checking that transport, including the exact support invariant and its limits. No programme-wide or field-wide priority claim follows from this search.

The normalizer transforms a supplied witness. It does **not** find a cheapest witness or make cheapest-standalone-state dynamic programming valid for shared costs.

## 1. The actual interface

Use finite fully scoped judgement labels J, finite fixed evidence identities E, and a finite set R of admitted ground rule instances. Write n=|J| and m=|E|. Each rule r has:

- head h(r) and ordered premise list `(q1,...,qk)`, with repeated judgements allowed;
- fixed local support B(r) contained in E;
- fixed finite nonnegative checking price w(r);
- fixed guard `G_r(S1,...,Sk)` on the **ordered exact child supports**.

The Python predecessor implements precisely this interface: immutable `Rule` records; `allowed` is either an immutable set of permitted support tuples or None, meaning every tuple (`guarded_compiler.py:1–45`). Its witness checker checks rule membership, ordered child judgements, and the exact support tuple (`:80–96`). The actual Lean interface agrees: `GuardedTree.lean:13–19` declares `guard : (r : R) → (Fin (arity r) → Finset E) → Prop`; `:31–43` defines union support and guarded validity. Those Lean sources formalize trees, not the DAG theorem below.

A DAG has finitely many nodes, a distinguished root, an admitted rule at every node, and one child reference for each ordered premise position. References form an acyclic graph; every node is root-reachable. A node's exact support is defined bottom-up:

    S(v) = B(r_v) union S(child_1(v)) union ... union S(child_k(v)).

Every child must have its stated judgement and each guard must hold on that ordered tuple. Repeated references remain repeated **positions**, although they need not designate distinct nodes. The root support equals the union of local B labels across all nodes. The checking cost is

    c(D) = sum over distinct nodes v of w(r_v).

In particular, a shared child is charged once, even when referenced twice. This is the predecessor's declared DAG accounting, not occurrence-tree cost or measured runtime.

No further context is needed in the state **for this interface**: all substitution-relevant non-support information is already part of fully scoped q or fixed rule metadata, and the parent inspects only the child judgement and exact support at each position. The state need not record child price or internal proof choice because these are not guard arguments. If validity instead inspects child node identity, internal rule provenance, proof shape, overlap of paid nodes, freshness, mutable authority, current external inventory, or other hidden context, `(q,S)` may be insufficient. Such predicates are outside the supplied interface; they cannot be silently treated as ordered-support guards. Rule admission, authentication and substantive soundness remain separate obligations.

## 2. Exact-state earliest-occurrence theorem

**Theorem.** For every valid DAG D under §1 there is a valid root-reachable DAG N(D) with the same root judgement and exact support, cost at most c(D), and no two nodes of the same `(q,S)` state.

**Construction.** Choose any premise-first topological ordering of D. Identify nodes with their original ranks. Let

    x(v) = (h(r_v), S(v)).

For every state x occurring in D, let e(x) be its earliest node. Keep this representative's **original rule occurrence**. If v=e(x) originally has its ith child u, replace that ordered reference by e(x(u)). Choose e(x(root)) as the new root, then retain only nodes reachable from it. Relabel the retained ranks if desired.

**Acyclicity.** For each redirected edge from representative v to e(x(u)),

    rank(e(x(u))) ≤ rank(u) < rank(v).

Thus every redirected edge is strictly descending in the original ordering. No cycle is introduced, even if the rule grammar itself contains cycles. Choosing an arbitrary representative instead of an earliest one has no such general rank guarantee.

**Exact states and guards.** Induct through the representative nodes in increasing original rank. For representative v and each original child u, the new child is an earlier representative. By induction it still has judgement h(r_u) and support S(u). Thus v's entire **ordered** child judgement/support tuple is unchanged. Its original rule remains admitted; its original guard remains true, even if nonmonotone, antitone, or sensitive to premise order. Its union support is exactly its old S(v). Nullary representatives satisfy the induction directly, including their guard on the empty tuple. Hence every representative has its original exact state. In particular the selected root has the original root state.

**Root restriction.** If a selected representative is reachable from the new root, all of its redirected children are reachable too. Removing the unreachable representatives therefore removes no child or descendant of a retained node and changes no retained exact state. The output is a valid rooted certificate with the promised exact support, rather than merely a support subset.

**Price and node count.** Every retained node is a distinct original occurrence with its original rule and unchanged local price. The retained occurrence set is a subset of D's node set. Consequently its sum of nonnegative prices is no greater. No comparison between the standalone prices of the selected and discarded subproofs is needed. There is at most one retained node per exact state, hence at most n2^m nodes. ∎

The construction is finite even when deleted nodes cost zero; it does not rely on strictly decreasing prices. The root rule can change when its exact state's earliest occurrence is an earlier subproof. The preserved observations are target judgement, exact support, admitted derivability and no-higher checking price, not original root-rule/certificate identity or every proof-history observable. Different input topological orders can choose different equal-state representatives. No canonical proof, minimum node count, or cheapest normalized output is claimed. For a supplied DAG the subset-price argument only requires each retained occurrence's own nonnegative charge to be unchanged; the finite-catalogue result next uses the actual stronger assumption of fixed rule prices.

## 3. Finite catalogue and actual minimum attainment

Let X=J×P(E). For each admitted r and each ordered support tuple `(S1,...,Sk)` satisfying G_r, create one ordinary ground rule with

    head: (h(r), B(r) union S1 union ... union Sk)
    ordered premises: ((q1,S1),...,(qk,Sk))
    local support: B(r)
    local price: w(r).

Keep the original rule identity and support tuple in the refined rule identity. This is a finite grammar: a rule of arity k has at most `(2^m)^k` tuples. It includes the single empty tuple for an allowed nullary rule and no rule for a false nullary guard.

Every original valid guarded DAG lifts node-for-node by assigning its actual exact states and actual ordered support tuple to each rule occurrence. Conversely, erase the refined labels in any valid acyclic refined-grammar DAG. An induction in topological order shows that a node labelled `(q,S)` actually has support S: the refined rule's head support was defined to be exactly its local support union its child support labels. Every erased node consequently satisfies its original guard. These two translations preserve graph nodes and ordered references, root judgement, exact support and the once-per-node cost. This is the explicit transport behind applying the inherited unguarded DAG theorem to the refined grammar.

For completeness, the finite catalogue can be described without a solver. For each x∈X choose either “absent” or one refined rule with head x. For a target state x0, follow the selected ordered child-state references. Reject any missing referenced choice or reachable cycle. Keep the x0-reachable graph. Check every retained original rule and guard and decode the certificate. This enumerates finitely many canonical state-indexed graphs, up to arbitrary renaming of node identifiers. If d_x is the number of refined rules headed by x, there are at most

    product over x∈X of (1+d_x)

rule-choice assignments. Cyclic or missing choices outside the selected root component need not matter. The normalization theorem puts every supplied original proof at or above a member of this catalogue **at exactly the same root state**.

If x0 is reachable, its catalogue is a finite nonempty family of actual valid DAGs. Take a member D* with least price. For any unrestricted finite original proof D at x0, normalization supplies a catalogue member N(D) with

    c(D*) ≤ c(N(D)) ≤ c(D).

Since D* itself is an original valid proof, it attains the global least price. If the state is unreachable, its family is empty and there is no minimizing witness; infinity is only a numeric unreachable convention. Minimizing over the finitely many supports for a given root judgement is also attained whenever any such proof exists.

Mathematical attainment permits arbitrary fixed finite nonnegative real rule prices. Effective exhaustive compilation additionally requires decidable guards and effective exact price addition/comparison. The executable uses the predecessor's exact integer/rational prices and immutable tables. An infinite supply of differently priced rule instances is not covered simply because the judgement names are finite.

The catalogue is whole-graph enumeration. It may be enormous; even state refinement may be exponential in the compact evidence/rule input. No scalable optimizer, new complexity classification, scheduling policy or approximation guarantee is supplied.

## 4. Distinctions and failure boundaries

### Total node count is not branch height

The bound here is n2^m **distinct DAG nodes**. The inherited n(m+1) bound concerns nodes along a branch under nested supports. They are not interchangeable. The test with one judgement and three evidence tokens has seven nullary leaves, one at each proper support subset, and a root requiring their exact ordered tuple. Its eight distinct states saturate n2^m, while its branch height is two and n(m+1)=4. No total-node bound of four holds for that example.

### Normalization is not minimum-price state selection

An input may contain two empty-support q leaves, with prices 5 and 1, and a t root using both. If the price-5 leaf is first, normalization costs 5, down from 6. A different legal normalized witness costs 1. The theorem guarantees a no-dearer representative, not the optimum from that input.

More importantly, global DAG selection still depends on sharing. The inherited four-judgement fixture has p at price 5, a directly at price 4 or via p at price 5, b via p, and t from a and b. All nonempty proof supports are the same `{e}`. Exact-support scalar tree minimization yields 9; a DAG using the dearer standalone a route shares p and costs 5. One representative per state in a **chosen whole graph** does not license choosing one cheapest standalone proof per state before combination. This normalization does not repair that failure.

### Negative prices

With an allowed nullary q rule costing 0 and an allowed self-rule q←q costing −1, a chain of k self-rule occurrences is a valid finite acyclic witness with exact empty support and price −k. The grammar can be finite while its witness family has no least price. Earliest-state normalization keeps the seed and raises any negative-chain price to 0. The rank and exact-state arguments still work, but the nonnegative retained-subset inequality fails. Our executable rejects a negative-price grammar rather than falsely promising nonincrease.

### Unsupported cycles, admission and extra context

A sole self-rule, even with price zero, supplies no acyclic finite proof. An allowed nullary seed does; a false nullary guard does not. The catalogue rejects reachable cycles and does not convert recurrence into evidence. In a seeded zero-price self-rule chain, choosing the latest same-state loop as representative and redirecting its child to that representative creates a self-edge. Choosing the earliest seed avoids it and legitimately changes the root rule.

The new checker explicitly tests every used rule against the supplied admitted catalogue. The inherited unguarded `dag_value` has no admission-list parameter, a limitation already documented in `shared-proof-cost-boundary-20261009/REVIEW_REPAIRS.md`. A fabricated rule, including a cheaper altered record under an existing name, must be rejected. Checking membership still does not establish that admitting the rule was substantively justified.

A hypothetical guard demanding distinct child **node identities** can hold before normalization and fail when equal-state children are shared. The test preserves this countercontrol without pretending it is an allowed support-only guard. Source-root distinctness represented inside fixed supports is different from physical proof-node distinctness.

## 5. Executable checks and stopping point

`guarded_dag.py` imports unchanged predecessor rule contracts, checks all input nodes, computes their exact states, performs earliest-state redirection and root restriction, then rechecks the output. It asserts exact root-state preservation, nonincreasing once-per-node price, state uniqueness and the total-node bound. It does not enumerate candidate optima.

`test_guarded_dag.py` contains 13 small deterministic tests. They cover duplicate exact states; ordered repeated premises and nonmonotone guards; failure of judgement-only redirection; rule admission; cycle/missing-reference/unreachable-node rejection; seeded and unseeded cyclic grammars; exact support growth; zero-price ties; negative prices; branch-versus-node count; earliest-versus-cheapest and the inherited scalar-DP counterexample; and the extra-context failure boundary. The smallest fixtures literally refine the grammar and reuse the unchanged unguarded whole-DAG compiler, then decode and recheck returned witnesses. This is a bounded integration discriminator, not a random search or optimization campaign.

Reproduce the complete new packet suite from this directory:

    PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -v

The initial missing-normalization/missing-guard-check implementations fail their two first tests in `test-first-red.log`; the implemented complete suite passes in `test-first-green.log`. Final replay and source-preservation receipts accompany the packet. Tests supplement the general written argument; they do not establish it by enumeration. No new Lean DAG theorem is claimed, and the earlier tree-kernel certification is not inherited by this Python extension.

The stopping point is this exact compiler-interface transport and its tested witness normalizer. It does not establish finite grounding or faithful transport for unrestricted HasE, logical truth, epistemic warrant, source reliability, adoption, integration, programme closure, or historical research duration.
