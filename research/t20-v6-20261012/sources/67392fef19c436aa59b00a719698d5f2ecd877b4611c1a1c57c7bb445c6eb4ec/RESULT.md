# Exact-support compilation for source-sensitive proof rules

9 October 2026. One bounded T20 applicability question. Inputs preserved; no integration, adoption, programme closure, or historical time credit.

## Result

The proposed extension is valid for finite **tree proofs** when each rule's guard depends only on the ordered exact supports of its premises and fixed metadata. Retain the least checking price separately for every exact `(scoped judgement, support)`. Then synchronous saturation computes all exact-support minima, with actual witnesses, in at most

    |J| (|E| + 1)

rounds. Guards need not be monotone or antitone under support inclusion. The theorem follows because deleting a repeated `(judgement, exact support)` on a branch changes no surviving guard input.

This is a constructive extension of the earlier compiler, whose report already contains the unguarded exact-support pruning observation and this height bound. The increment is proving that exact-support replacement and cost minimization remain valid under support-sensitive guards, and making the resulting finite saturation explicit. It is not a discovery of the support-shrinking problem.

The retained FABLE N5 already identifies that problem for a two-root corroboration guard and restricts its proposed root-tracking cut repair to antitone guards. Those Core B properties are explicitly `DERIVED_BUT_UNVERIFIED`. A bounded source inspection found no corresponding exact-support guarded compiler. Our result supplies a finite compilation method for a declared fragment; it does **not** make unrestricted provenance-changing cut admissible, certify the full Core B calculus, or establish an adopted-system defect.

## 1. What the retained sources actually say

The source inspection is bound in `source-review/SOURCE_BINDINGS.json`, with exact snippets and read ranges in `source-review/RETAINED_SOURCE_FINDING.md`.

1. **Existing compiler.** `certificate-compilation-boundary-20261009/RESULT.md`, §§2–3, requires substitution by any proof of the same fully scoped judgement. Its Pareto step discards larger, dearer supports. It explicitly excludes hidden proof-dependent side conditions. Its final §3 paragraph already proves the equal-judgement/equal-support pruning bound for the unguarded case. We credit that result in full.
2. **Earlier warranted-discrimination report.** Its finite admitted-certificate contract keeps actual proof references and warns that pair-equivalent proofs need not be interchangeable for every provenance question. Its final Pareto theorem is about ordinary support availability and cost, not about using a pruned proof as a premise of a new provenance-sensitive rule.
3. **Retained FABLE N5.** `AR8R-FABLE-R1-NEGATIVE-RESULTS.md:169–182` names a guard requiring at least two distinct roots and the obstruction to root-tracking cut. `AR8R-FABLE-R1-TYPED-CORE-CANDIDATES.md:75–112` supplies provenance-annotated judgements and support-sensitive transport. It also says the listed properties have no committed checking artifact. The governing correction receipt downgrades unsupported proof claims. These are inherited proposed rules and reported arguments, not established source reliability or an adopted implementation.
4. **Provenance discipline.** `SPA-R6_PROVENANCE_ROOT_INVARIANT.md:9–28` says copying preserves acquisition ancestry, while distinct acquisition roots need not establish distinct ultimate sources, evidential independence, or statistical independence.
5. **The T20 authority fixture is already represented.** The actual `OccurrenceControls.lean:29–37` has typed Horn premises for historical directives, testimony, prospective authorization and implementation. These rules already fit the old fixed-premise compiler; they are not evidence of a new support-guard obstruction. The associated grounded-attestation antichain theorem is an ordinary positive-Horn support construction.

The two-root phrase in N5 does not define eligible content or evidential roles well enough to prohibit padding. The illustration in §4 therefore declares that refinement explicitly. It is an instance of the proposed mathematical interface, not an assertion that the retained source already specifies that complete licence. No broad review of all source commitments, or exhaustion of the repository, is claimed.

## 2. Exact guarded-tree contract

Let J be a finite set of fully scoped judgement labels and E a finite set of fixed evidence identities. Set n=|J|, m=|E|. Every context, claim version and other non-support parameter relevant to substitution is retained in J or in fixed rule metadata.

A finite set R of ground rule instances specifies, for each r:

- its head h(r) in J and ordered premise list `(q1,...,qk)`;
- local evidence B(r) contained in E;
- a fixed finite nonnegative additive checking charge w(r);
- a fixed predicate `G_r(S1,...,Sk)` on the exact premise supports.

A finite tree with root r and children T1,...,Tk is admissible exactly when each child is admissible with the indicated scoped judgement, and its support tuple satisfies G_r. Then

    S(T) = B(r) union S(T1) union ... union S(Tk)
    c(T) = w(r) + c(T1) + ... + c(Tk).

Nullary rules are included; their guard is evaluated on the empty tuple. Every occurrence is charged, even if two subtrees are syntactically equal. Evidence is persistent and reusable as a set; checking is this expressly stated tree cost.

A guard can inspect fixed token content/version/role metadata, declared root ancestry, or a fixed authority relation. It can require particular combinations, exclude a source, or impose disjoint root sets between two typed premise packages. The guard may depend on which support occupies which premise position, not just on the union.

It cannot inspect unstated internal proof provenance, proof shape or history, checker price, newly minted identities, changing authority, the current entire external inventory, or hidden semantic facts. If any of those matter, this state is insufficient. Rule admission, metadata correctness, authentication and substantive soundness remain separate obligations. A root-label distinction supplies no theorem of source truth or reliability.

Mathematical existence works for nonnegative real local prices. Effective compilation additionally requires decidable guards and exact effective price addition/comparison; the executable uses immutable finite guard tables and exact integer/rational arithmetic.

## 3. The guarded exact-support theorem

**Theorem.** Under §2:

1. Every finite q-proof with exact support S has an admissible q-proof with that **same** support, no greater checking cost, and height at most `n(|S|+1)`, hence at most `H=n(m+1)`. Height counts rule nodes.
2. For every reachable `(q,S)`, the minimum price over all finite proofs is attained by a tree of height at most H. There are at most `n 2^m` reachable exact states.
3. The recurrence below computes every such minimum and a realizing witness in H synchronous rounds from the empty table. The result is a fixed point. Equality of the complete support/price table after an earlier round is also a sound stopping test.

### Proof of the height bound

Suppose an ancestor node u and a proper descendant v have the same scoped judgement and the same subtree support S. Replace the entire u subtree by the v subtree. The descendant was already a valid proof of that judgement. The rule immediately above u sees exactly the same ordered list of child judgements and exact supports as before. Its guard remains true and its own support is unchanged. Inductively every surviving ancestor sees the same guard inputs and support. If u is the root, the root judgement and support are directly preserved.

The subtree's price weakly decreases because the removed rule occurrences and side subtrees all have nonnegative prices. The complete tree's price therefore weakly decreases. Node count strictly decreases, even if every removed charge is zero. Repeating this operation must terminate.

In the resulting tree, no branch repeats the same `(judgement, support)`. Along a branch, subtree supports are nested by inclusion because support is formed by unions. Starting with root support S, there can be at most |S| strict decreases. In each constant-support block there are at most n nodes, since a repeated judgement would be a removable repetition. Thus the branch has at most `n(|S|+1)` nodes. This argument does not use support monotonicity of the guards. It uses equality of their actual inputs.

### Attainment and recurrence

There are only finitely many trees of height at most H: R is finite and every rule has finite arity. The pruning proof gives a no-dearer representative in this finite family for every exact-support proof. A reachable exact state therefore has an attained global minimum in that family.

Let `D_0(q,S)=infinity` for every q,S. At round h+1, retain the old price and consider every rule r with head q and every ordered support tuple S1,...,Sk whose child prices at round h are finite and whose guard is true. Its candidate is

    S = B(r) union S1 union ... union Sk
    price = w(r) + D_h(q1,S1) + ... + D_h(qk,Sk).

For each **exact** `(q,S)`, keep the smallest candidate price and an immutable realizing tree. Do not delete one support merely because a cheaper or equal-price subset support exists.

Inductively D_h is exactly the minimum among trees of height at most h. For the induction step, replacing a child by the cheapest height-h proof of the same q_i and exact S_i preserves its parent's guard and resulting exact support, while weakly decreasing the additive price. Conversely every candidate constructs an actual admissible height-(h+1) tree. Nullary rules enter at round 1.

The height theorem makes D_H the unrestricted finite-proof minimum table. No following round can improve it, so it is a fixed point. If a complete table is equal at any earlier successive pair of rounds, applying the same deterministic recurrence again changes nothing. Merely finding no new support keys is insufficient: an existing key's price may still decrease. ∎

### The uniform height bound is sharp

For every n≥1 and m≥0, use judgements q1,...,qn and evidence e1,...,em. Let A_j={e1,...,ej}, with A_0 empty. Give q1 a nullary empty-support rule and include the chain rules q_i→q_(i+1). For each j=1,...,m, add a return rule q_n→q1 with local support {e_j}, allowed only when its premise support is exactly A_(j−1). All local prices may be zero.

Every reachable support is a prefix A_j. The only way to obtain q1 at A_j for j>0 is its corresponding return rule, whose child is q_n at A_(j−1). Reaching q_n then requires all n−1 chain edges. By induction, the least height for q_n at A_j is n(j+1). Thus q_n at A_m requires exactly n(m+1) nodes on its sole branch. This is a structural worst-case proof of sharpness for arbitrary fixed guards, not an epistemic example or a proposed extra task. It does not say every source policy needs this many rounds.

### Relation to the previous compiler and to N5

One can also compile the guarded rules into a finite ordinary grammar with refined labels `(q,S)`, instantiating each allowed support tuple and fixing its union at the head. This is finite state refinement, not an arbitrary proof-search oracle. Applying the predecessor theorem to up to `n 2^m` refined labels gives another finiteness argument; nesting supplies the sharper bound above.

The method conservatively retains every reachable exact support, not necessarily the smallest state summary for a particular guard family. It makes no polynomial complexity or minimum-memory claim. With maximum rule arity a, a rule can expose up to `2^(ma)` support tuples. Large proof trees and exponentially many supports remain possible.

N5 concerns substitution/inlining that can change a provenance footprint. This theorem uses only substitutions that leave that footprint **equal** at every surviving guard. It therefore avoids the obstruction without proving the forbidden cut rule. In particular, transport that deletes or relabels support identities violates the union-support contract unless a separately justified fixed encoding restores it. No completeness result for the full FABLE transport/weakening/repair calculus follows.

## 4. A meaningful corroboration example, with padding excluded

Fix a claim version P@v1. Each admitted token carries a content/version, an evidential role, and a declared acquisition-ancestry root. Consider a scoped judgement `packet(P@v1)` for a cited report package, and a separate judgement `two_root_licensed(P@v1)` for passing a declared corroboration policy.

- Token a is a corroborating report about P@v1 with root A.
- Token b is a corroborating report about P@v1 with root B.
- A copy or second review of a still has root A.
- A report about Q, an administrative receipt, and a report about P@v0 do not have the required content/version/role.

The licence requires at least two distinct declared roots among **cited corroborating-report tokens about P@v1**, after filtering by those fields. Tokens are not counted merely because they occur somewhere in the proof. Neither the licence nor the compiler infers that P is true, that A and B have independent ultimate sources, or that their assertions are statistically independent.

The illustrative ground grammar has three rules, each with checking price 1:

1. Read the first report: local support {a}, conclude `packet(P@v1)`.
2. Under an explicitly admitted report-incorporation rule, adjoin the matching corroborating report b to a cited packet: one packet premise and local support {b}, conclude `packet(P@v1)`.
3. Inspect a packet and issue `two_root_licensed(P@v1)` only when its premise support passes the stated guard.

Rule 2 represents citing the second report for corroboration. It is not arbitrary evidence padding: b has the same target/version and required evidential role. The proposed licence is a declared policy assumption inspired by N5, not a derivation of epistemic sufficiency from token counts.

The packet has exact supports {a} at price 1 and {a,b} at price 2. For the standalone packet's ordinary availability/cost observation, the first dominates the second. But only the second passes rule 3, yielding a licensed certificate of price 3 and height 3. There are just two judgement labels, so the old |J|-round bound would also be too short without refinement. Intermediate Pareto pruning removes the necessary packet forever.

Copying a, adding unrelated content, attaching an administrative receipt, or citing an old claim version all fail the guard. The tests check each case. This explicit scoping is stricter than the underspecified N5 phrase; no claim of faithful realization of an adopted collective-warrant rule is made.

The suite also checks a nonmonotone provenance policy: two separately selected nonempty report packages must have disjoint declared root sets. The ordered tuple `({a},{b})` passes, but `({a,b},{b})` fails. Exact-support saturation still works because replacement preserves each selected support, not because adding evidence must preserve the guard.

## 5. Terminal reduction, inventory growth, and the DAG boundary

After every guard needed for a terminal judgement has been discharged, the finite table supplies a finite terminal certificate catalogue. If subsequent observations ask only whether support is contained in an available inventory and what the terminal price is, ordinary Pareto normalization is safe again. The earlier warranted-discrimination frontier and residualization theorems then apply with their existing witness-retention requirements.

This does not permit throwing away exact supports before a later support-sensitive rule, or before a final provenance acceptance test. If the result will be reused that way, keep the exact table or another separately proved sufficient summary.

Even a nonmonotone proof-support guard does not by itself make external inventory growth defeasible. An existing proof cites the same selected support when more unrelated inventory becomes available. A guard that tests all currently available evidence instead of the cited proof support is a different contract and is excluded here.

Everything proved here is about **tree checking**. The predecessor's shared-DAG counterexample already gives the same exact support to a locally cheaper proof and a locally dearer but globally shareable proof. Retaining only the least standalone price for `(q,S)` does not retain the sharing structure needed for DAG optimization. No new DAG compiler, scheduler or proof-fragment reuse theorem is supplied. The prior one-node-per-unrefined-judgement DAG theorem cannot silently be extended to guarded proofs either, because its redirection can change guard supports.

## 6. Verification and limits

The report's theorem is proved in prose. `guarded_compiler.py` implements the exact recurrence for finite immutable guard tables and exact rational costs, keeps tree witnesses, rechecks every selected rule/guard during witness traversal, and implements equal-state pruning. This is structural certificate validation, not authentication or validation of philosophical source commitments.

The deterministic test suite covers the scoped source guard and anti-padding controls, a genuinely nonmonotone binary guard, unsupported and zero-price cycles, exact-support pruning, repeated-premise tree charging, rational prices, and contract rejection. It also exercises every Boolean unary guard over the four supports of a two-token universe, for each of four local-support choices, against an independently written unpruned height oracle. Tests supplement the general proof rather than establish its universal claim by enumeration. The submitted main suite is deterministic. The internal AI reviewer additionally retained a small seeded structural sanity check (100 grammars, 500 round comparisons); it is not empirical source validation or a performance campaign.

The complete replay runs 9 main tests and 5 independently written controls. The latter cover the sharp six-round case, cost improvement despite unchanged support keys, a strictly nonmonotone guard, positive-price side-subtree pruning, and malformed-input rejection. Fresh results, hashes, mutation controls, and the internal AI review are recorded alongside this report. No new Lean certification is claimed. The earlier Lean development certifies the downstream finite terminal support/price reduction only, not this guarded compiler or the substantive licences.

The source applicability remains deliberately bounded: the inherited failure is already known, ordinary authority Horn rules are already covered, and the content-scoped source licence is an explicit illustrative refinement. This result closes only the requested finite-grammar mathematical question. Historical six-hour compliance remains unverified; prospective activity records confer no retroactive time credit.
