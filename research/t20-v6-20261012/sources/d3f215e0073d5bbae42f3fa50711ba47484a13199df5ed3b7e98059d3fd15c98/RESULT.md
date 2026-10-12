# The shared-proof cost boundary: an exact compiler transport

9 October 2026. Additive, bounded T20 computational-epistemology discriminator. Predecessors are read-only. No integration, adoption or T20 closure.

## Result first

There is a precise complexity boundary inside the present finite ground-rule contract. For explicitly listed, **acyclic, unguarded rules with empty evidence supports and prices in {0,1}**, deciding whether a root has a shared proof DAG of cost at most k is NP-complete. On the very same layered rule family, minimum occurrence-charged tree cost is simply the number of element obligations whenever a proof exists. Its shared-DAG minimum is the minimum Set Cover size.

This is a transport of classical Set Cover / AND–OR solution-graph hardness, not a new complexity discovery. Sahni's 1974 Problem G2 and Theorem 2.3.2 already give acyclic 0/1-cost shared-subproblem hardness. The locally useful addition is the exact map into the current compiler's rule objects, its two witness directions, a polynomial certificate argument, and controls identifying the computational guarantee that fails when the declared checking objective changes.

Provability, root judgement and evidence support survive unfolding. The once-per-node price does not. Polynomial numeric minimization for additive occurrence costs therefore cannot be transferred merely by retaining the same logical meaning. Finite exact compilation, minimum attainment and inexpensive validation of a supplied finite witness survive. Unless P=NP, polynomial exact shared-cost optimization for all such explicitly given grammars does not.

A second exact encoding prevents a misleading “trees are easy” conclusion. When the input asks for **exact target evidence support**, minimum occurrence-tree price already encodes Set Cover, even on an acyclic chain of unary rules where DAG sharing makes no difference. Thus support-state expansion and shared-node overlap are separate sources of hardness. Knuth after explicit state refinement is not a polynomial-time guarantee in the original compact support-labelled grammar size.

## 1. Inherited results and the no-rediscovery ceiling

The following actual local material was inspected before this reduction was developed. Paths, hashes, reading depth and search limits are in `SOURCE_LEDGER.json` and `INPUT_BINDINGS.json`.

- `certificate-compilation-boundary-20261009/RESULT.md`, §§2–4, already distinguishes occurrence and shared-node prices, proves a one-node-per-judgement normal form, supplies finite whole-rule-choice enumeration, and gives the strict local-pruning failure with tree cost 9 and DAG cost 5. This report neither originates those statements nor repairs that compiler.
- `guarded-deduction-prior-art-20261009/RESULT.md` and its source ledger already transport guarded exact-support **tree** cost to Knuth's weighted deduction and distinguish recursive hyperpath valuation from distinct-edge cost. They explicitly do not claim a polynomial bound in the original guarded input size or a sharing-aware optimizer.
- `warranted-discrimination-research-20261009/RESULT.md`, §§2.2–2.3 and 4, fixes terminal proof prices and separates offline compilation from acquisition and terminal execution. Arbitrary fragment scheduling/reuse is expressly outside that earlier model.
- `graph-constrained-continuation-20261009/RESULT.md`, §§1–3, already owns the exact Steiner/parity gate-cost transport and credits its prior CNOT ancestry. That is a different permitted-action objective; an existing Steiner formula is not itself a reduction for this proof-checking objective.
- The actual T16 main DOCX's continuation, signed-controller and identity-checker passages, the retained T16 companion reader, and the T16 public evidence/source-recovery archive text members were screened. They establish other computability and certificate/continuation boundaries, not this explicit ground-rule cost comparison in the inspected material. T20's mathematical companion §§on labelled cuts and corpus transfer was also inspected: its cheapest-label-cut counterexample is not silently credited as an NP-hardness proof.
- An older reconciliation **already records** RP-T7, “minimum-cost recheck synthesis is NP-complete,” and RP-T34, a reduction of missing-fragment requests to MIN-RECHECK: `user-checkpoints/extracted/P14/source-main/docs/project-closure/ar8r-v11/post-merge-pmr001-source/AR8R_AR2_AR3_COLLECTIVE_BACKBONE_RECONCILIATION.md`, AR3 table. The corresponding full RP proof was not located in the bounded local search. That summary is an inherited warning, not a proof independently read here. No claim is made that the original RP theorem differs from this construction, or that programme-wide hardness was previously unrepresented.

**Disposition:** no new general hardness boundary is claimed. The exact matched compiler transport is absent from the specifically inspected compiler packets and is useful as a scope clarification. The missing RP manuscript prevents any stronger internal-priority claim. No broad search campaign is warranted by that absence.

## 2. Decision problem and explicit input contract

An instance of **SharedProofBudget** consists of:

1. An explicitly listed finite set J of distinct fully scoped judgement identifiers.
2. An explicitly listed finite set R of admitted ground rules. Each rule has a head in J, an ordered finite premise list in J, empty evidence support, and price 0 or 1.
3. A target q in J and a nonnegative integer budget k, in binary.

The dependency graph has edges from every rule head to each premise and is acyclic. This is an ordinary checkable input restriction; no grounding oracle, rule schema, implicit exponentially large state space, proof-dependent side condition, guard oracle, hidden source test or negative price is included.

A certificate is exactly the predecessor's rooted finite proof DAG: one admitted rule at each node; one correctly labelled child reference for each ordered premise position; acyclic; all nodes root-reachable. Its cost is the sum of local prices over distinct graph nodes. Rules and their application semantics are fixed in advance. The question is whether such a DAG of target q has cost at most k. Rule admission and substantive soundness are application assumptions, not established by optimizing.

### Membership in NP

If a witness exists, one with at most |J| nodes exists. One may use the predecessor's earliest-occurrence redirection lemma. In the present acyclic-input subclass there is an even direct argument: select one occurrence for each used judgement, redirect its premises to the selected occurrences, and remove nodes unreachable from the selected root. Every edge still decreases the input topological rank. Each selected occurrence keeps an admitted rule; every required premise label still exists. No new paid node is introduced, so nonnegative cost cannot increase.

The certificate can thus list at most one chosen rule per judgement plus a root and premise references. Its bit length is polynomial in the explicit rule-list encoding, including all premise positions. A verifier checks rule identities, labels, arities, references, acyclicity and reachability, then sums at most |J| unit prices and compares with k. All checks are polynomial. This proves NP membership for this explicit decision problem, not for arbitrary compressed guarded grammars or unrestricted HasE proof search.

## 3. Set Cover transport, in both directions

Take a finite Set Cover instance with universe U={u1,…,un}, indexed family S1,…,Sm ⊆ U, and budget k. Set Cover asks for C⊆{1,…,m} with |C|≤k and U⊆⋃j∈C Sj. Empty sets and duplicate family members are allowed as distinct indices. Let τ=∞ if no cover exists.

Construct disjoint judgement labels s1,…,sm, x1,…,xn and t, and only these rules:

- For each j, a nullary rule concluding sj, of price 1.
- For each incidence ui∈Sj, the unary rule sj ⇒ xi, of price 0.
- One ordered rule x1,…,xn ⇒ t, of price 0. If n=0, it is nullary.

Every support is empty. The dependency ranks are t above the xi above the sj, so the grammar is acyclic and has proof height at most three. There are m+n+1 judgements, m+Σj|Sj|+1 rules and n+Σj|Sj| premise positions. Construction is polynomial in the explicit incidence input. The budget is unchanged.

**Cover ⇒ DAG.** Given a covering family C, assign each ui one j(i)∈C with ui∈Sj(i). Create one paid sj node for each index actually assigned, one xi node justified by its membership rule and a reference to that shared sj, and the root t with all n references. Discard unused members of C. This is a legal root-reachable DAG with cost at most |C|. The construction is effective and polynomial in the incidence input and supplied cover.

**DAG ⇒ cover.** Any t-proof must use the sole root rule, hence contains a proof of every xi. The only rules concluding xi are membership rules from some sj with ui∈Sj; the only way to prove that sj is its unit-price nullary rule. Collect the distinct indices of all such paid sj nodes. They cover U. Their number is at most the number of paid occurrences, which is exactly the DAG's cost. This remains true if the witness unnecessarily duplicates the same sj label; duplicates cannot help the budget.

Taking minima yields

    minimum shared-DAG cost of t = τ(U,{Sj}).

These are witness-preserving inequalities in both directions and an exact equality of optimum values. They are not a bijection between every cover and every syntactic witness: unused cover sets disappear and duplicate proof nodes can be removed. Reading the incidence relation back from a grammar of this particular layered form gives the converse instance map to Set Cover. No converse structural reduction of every arbitrary ground grammar to a same-sized Set Cover instance is asserted.

Set Cover's standard NP-completeness therefore gives NP-hardness, and §2 gives NP-completeness. Karp's formulation takes the universe to be the union of the input sets. Consequently the hardness already holds on constructed instances in which the goal is provable: the difficult question is the least shared checking price, not whether any proof exists. The extended uncoverable cases above are useful total-definition controls.

### Large conjunctions and zero-price checks are not the cause

For n≥2 replace the final n-premise rule with zero-price binary conjunction rules y2←(x1,x2), yi←(y(i−1),xi), ending in t (or add one zero-price unary renaming). The auxiliary judgement names are fresh and have unique rules. A proof must still contain every xi; the selected paid sj nodes and their price are unchanged. This is a polynomial construction with maximum arity two. Constant proof height is lost, but the NP-hardness remains.

Alternatively assign price 1 to **every** rule in the original three-layer construction. A reduced t-proof has n element nodes and one root in addition to its chosen set nodes. Thus its shared optimum is n+1+τ, while its occurrence-tree optimum is 2n+1 whenever a proof exists. A cover budget k becomes k+n+1. Unnecessary duplicates only add cost. The obstruction does not depend on pretending that all structural checks are free. These are declared cost models, not measured processor-time models.

## 4. The exact tree comparison and surviving guarantee

In the original 0/1 construction, any occurrence-charged proof tree of t has one xi child for each element and one unit-price sj leaf below each xi. Even two equal sj labels in different branches are distinct charged occurrences. Hence, if U is covered,

    minimum tree cost of t = n,

independently of which covering indices each element chooses. If an element is uncovered there is no tree and no DAG; if U is empty both minima are zero.

For arbitrary explicit acyclic unguarded empty-support grammars, additive tree prices obey

    d(q) = min over rules r headed by q of [w(r) + sum over premise positions p of d(p)].

Evaluate in topological order, with the minimum of an empty set equal to ∞. This computes minimum **numeric occurrence cost** and compact optimal rule pointers in polynomial time in the explicit input size. With unit weights and N states, a bounded-depth unfolded witness can be exponentially large, but its cost has polynomial bit length: for maximum arity a, it is bounded by 1+a+…+a^(N−1). Literal expansion/serialization of that tree is not promised in polynomial time. The nonnegative additive functions also satisfy Knuth's superior-function hypotheses; the acyclic case needs only the elementary topological calculation.

Each valid finite DAG unfolds to a tree of the same root and support, and every tree is a DAG if its nodes are kept distinct. Thus provability agrees. What fails is cost preservation under unfolding and the optimal-substructure claim for standalone scalar child costs. The DAG objective depends on overlap between the chosen child witnesses' internal paid-node identities. Empty evidence support does not erase those identities.

For example, with U={a,b} and sets {a}, {b}, {a,b}, every element's standalone minimum is 1. Choosing the two singleton routes gives a valid shared proof of price 2; choosing the common route gives price 1. Even equal-cost local witnesses can require globally coordinated selection. Replacing sum by max is also wrong: with only disjoint singleton sets the actual shared price is 2, while max(1,1)=1. The predecessor's strict 4-versus-5 local pruning example supplies the already-known stronger dominance failure.

The full terminal frontier here contains only (∅,τ) when a proof exists, so exponential numbers of evidence supports or frontier outputs cannot explain away the hardness. With empty support, refining state only to (judgement, exact evidence support) adds no information. A sharing-aware method may keep richer state or enumerate whole graphs, as the predecessor already does. Unless P=NP it cannot guarantee polynomial exact compilation for every instance of the present class. This is not an unconditional exponential lower bound or a prohibition on efficient special cases.

## 4a. Independent discriminator: exact-support tree price

The predecessor's exact-support compiler expressly retains every reachable (q,S), not merely a terminal availability frontier. Its stated at-most-|J|2^|E| state count already warns of exponential expansion. Here is the exact cost consequence for that interface, separately from sharing.

Use the same Set Cover input U,S1,…,Sm. Let the evidence universe be U, encoded by explicit fixed token identities. There is one judgement q, a nullary q-rule of empty support and price zero, and for each j a unary rule q⇒q with local support Sj and price one. All guards are true. Ask for a q-proof whose **exact** support is U.

Every proof is a finite chain ending at the seed. Its support is the union of the sets attached to its unary occurrences, and its price is their number. A cover C gives a chain using each j∈C once, of exact support U and price |C|. Conversely, the distinct indices used by a chain cover its support U and number no more than its price. Repeated choices and empty-set choices cannot improve the minimum. Hence the least exact-U tree price equals τ. This grammar has a cycle, but the obstruction does not require one.

For an **acyclic** version, introduce q0,…,qm. The seed concludes q0 at empty support and zero price. For each j=1,…,m add two rules from q(j−1) to qj: skip with empty local support and price zero; take with local support Sj and price one. The target is (qm,U), meaning q_m with exact support U. The explicit grammar has m+1 judgements, 2m+1 rules and size polynomial in the incidence encoding. Every proof is a chain of precisely m+1 nodes. Its take indices are exactly a subset C of the family, its support is ⋃j∈C Sj and its cost is |C|. Both directions and equality of minima follow immediately.

For this restricted acyclic-chain exact-support budget problem, NP membership is witnessed by the m take/skip bits; union and price can be checked in polynomial time. Thus its budget decision is NP-complete already in this family. No more general exact-support or guarded decision-class upper bound is asserted here. Since the chain has one node of each distinct judgement and only one premise at every nonleaf, it has no reusable common branch: occurrence-tree and once-per-node DAG prices coincide exactly.

Changing the target from exact support U to any support **contained in** available inventory U destroys this reduction. Skipping every set yields the empty-support proof at price zero. Ordinary terminal Pareto normalization likewise retains that dominating empty-support/zero-price option. Therefore this is an exact-support query, or an equivalent explicitly declared final support-acceptance requirement, not the earlier ordinary “some supported proof is available” objective. The tokens are not being priced individually for acquisition; each take-rule has a declared unit checking charge regardless of its local support's size.

The two controls isolate different contracts:

1. Empty support, arbitrary proof branching: numeric tree minimization is polynomial in explicit acyclic input; shared-DAG minimization encodes Set Cover.
2. Compact nonempty support labels, exact terminal support: even unary acyclic tree minimization encodes Set Cover; sharing is irrelevant.

Both are compatible with the inherited finite-height/exact-table theorem and the weighted-deduction transport. Expanding to complete (judgement, support) states can be exponential in the compact input, and a polynomial algorithm in that expanded representation need not be polynomial in the original one. A short height bound does not remove that representational cost. The contribution here is the pair of exact maps and their scope discrimination, with standard hardness credited to Set Cover; no historical novelty for the support-union mechanism is claimed.

## 5. Sources and priority

- Richard M. Karp, *Reducibility among Combinatorial Problems* (1972), Main Theorem, item 6, p.94, and Node Cover→Set Covering reduction, p.98. The imported fact is standard Set Cover NP-completeness. [Publisher record](https://link.springer.com/chapter/10.1007/978-1-4684-2001-2_9); [inspected original-article OCR reproduction](https://studylib.net/doc/27985824/karp1972). The OCR has corrupt inequalities; the budget convention here is explicitly ≤k. This is not a publisher-PDF audit.
- Sartaj Sahni, *Computationally Related Problems* (1974), Problem G2 and Theorem 2.3.2, pp.271–273. The original construction uses shared AND/OR subproblems, unit-priced terminal links and zero-priced other links; the proof expressly discounts a subproblem already solved. This establishes direct classical ancestry. Its historical “P-Complete” terminology must not be confused with today's P-completeness. [Author-hosted primary scan](https://www.cise.ufl.edu/~sahni/papers/comp.pdf).
- Gallo, Longo, Nguyen and Pallottino, *Directed hypergraphs and applications*, revised October 1992 manuscript, §§6.1–6.2, pp.11–12. Distinct-hyperarc sum and recursive valuation are separate; the text credits minimum-cardinality B-path hardness to Italiano and Nanni. That cited proof was not read here and is not the proof basis for §3. [Primary manuscript](https://static.aminer.org/pdf/PDF/000/836/884/directed_hypergraphs_and_applications.pdf).
- Mark-Jan Nederhof, *Weighted Deductive Parsing and Knuth's Algorithm* (2003), §§2–5, especially Figure 4 and the superior-function condition: occurrence-weighted deduction and its acyclic/topological specialization. Knuth's 1977 result is credited through this primary exposition and the predecessor's source comparison. [Primary PDF](https://aclanthology.org/J03-1006.pdf).

Gao's 2021 *On Computation Complexity of True Proof Number Search*, §§2.1–2.4 and the proof-number half of §3, was also inspected as an overlapping AND/OR-DAG lead; it itself points to Sahni. No claim about its disproof-number argument, game-search performance or broader algorithms is required. [Primary preprint](https://arxiv.org/pdf/2102.04907).

## 6. Verification, interpretation and stopping point

`python shared-proof-cost-boundary-20261009/check_transport.py` runs bounded checks against the unchanged predecessor `compiler.py`. Independent Set Cover subset enumeration agrees with its exact tree and whole-DAG compiler on all 689 indexed set systems with 0–3 elements and 0–3 sets. It validates 1,510 cover-to-DAG witnesses. Six additional cases check the binary-root construction and six check the all-unit-price offset. Targeted controls cover empty and uncoverable universes, duplicate paid nodes, locally tied choices losing sharing, the false max repair and deletion of a required element.

The same 689 incidence inputs are separately checked against the unchanged `source-sensitive-proof-compilation-20261009/guarded_compiler.py` for both the one-judgement exact-support loop and the acyclic take/skip chain. All returned compiler witnesses and all constructed witnesses used by these checks are tested for membership in their stated admitted rule set as well as structural validity and price. The inherited unguarded structural traversal alone does not check rule admission. A reviewer found that the first binary forward-witness control still built an n-ary root; the repaired builder uses the actual binary grammar, and explicit rejection controls preserve this finding. Returned exact-support witnesses are traversed again; the chain is also re-encoded as a DAG and its price checked. Relaxing exact support to inventory-subset availability returns zero in every case, as the mathematical countercontrol predicts.

The general theorem is the written reduction and membership argument, not an inference from that finite census. No new Lean theorem, independently reviewed formal certificate, solver, benchmark or approximation result is supplied. Predecessor bindings are rechecked in `INPUT_UNCHANGED.json`; the test deliberately disables Python bytecode writes into predecessor directories.

The epistemic conclusion is bounded: changing the accounting from repeated proof-tree checks to checks reused across one proof can retain the admitted conclusion and all source-support conditions while turning a locally separable price computation into a global combinatorial selection problem. A supplied shared certificate remains polynomially checkable under this contract. Establishing that it is the cheapest is a separate computational obligation. An existing declared terminal frontier can still support the inherited residualization and inquiry-cost theorem; obtaining that frontier is offline work and is not silently priced as terminal checking.

No theorem here supplies faithful finite grounding for unrestricted HasE, authenticates sources, licenses reuse across different scopes, models cache invalidation or scheduling, decides philosophical truth, or closes T20. The bounded discriminator stops at this exact classical transport and the cost-objective boundary.
