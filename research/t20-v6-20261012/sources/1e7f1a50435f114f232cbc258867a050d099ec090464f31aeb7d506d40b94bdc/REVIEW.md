# Independent internal review: shared proof cost transports

9 October 2026. Review of the corrected, digest-bound research packet. This is an internal mathematical and executable-control review, not external human review, formal certification, source-warrant certification, integration, adoption, or T20 closure.

## Disposition

Accept the corrected packet at its stated scope. No unresolved defect was found in either written Set Cover reduction, the restricted decision-class arguments, or the tree/DAG comparison. Three narrow issues were reported and repaired: the binary forward-witness test built a witness of the original n-ary grammar; the inherited structural replay did not itself check admitted-rule membership; and the all-unit tree formula needed a proof-existence qualification. The original observations and replay remain preserved rather than being overwritten.

This conclusion binds only the final revisions named in `REVIEW_RECEIPT.json`. A future source or predecessor change requires renewed currentness checking.

## Findings and repair verification

### R1. Binary forward-witness grammar mismatch: resolved

In the first script, `check_case(binary=True)` correctly compiled the binary grammar but called a builder that always used the original n-ary goal rule. For three elements covered by one set, that generated `finish` rule was absent from the binary rule list. The inherited structural checker nonetheless returned cost 1. The binary compiler-minimum assertions remained valid, as did the 1,510 advertised forward witnesses from the nonbinary census. The defect concerned the additional binary witness checks, not the written reduction.

The corrected builder takes the binary flag, obtains its rules from `grammar`, and builds the prefix nodes plus unary final reference when appropriate. The new negative control rejects the old n-ary witness against binary rules, and the corresponding true binary witness passes. I inspected the code changes and replayed the repaired script.

### R2. Structural replay versus admission: resolved within this packet

`C.dag_value` verifies node references, ordered premise labels, topological indexing, root reachability, support union, and price. It has no admitted-rule-set argument. An invented nullary zero-price goal rule therefore passes it as a structural object even when absent from the grammar.

The new packet adds `checked_dag` and `checked_tree` membership checks, applies them to returned frontiers and constructed witnesses, and traverses all exact-support tables with the guarded compiler's admission-aware `tree_value`. The invented-axiom control now explicitly fails admission. The inherited compilers were not changed. These checks establish membership in the declared rule list; they do not establish substantive soundness, authenticity, or source authority. The report now states this distinction.

### R3. All-unit feasibility qualifier: resolved

The formula for tree optimum is now `2n+1 whenever a proof exists`. Uncoverable inputs have no proof. The corresponding executable had already treated them correctly. The plural membership-rule wording was also clarified without changing the argument.

## Mathematical review

### 1. Empty-support shared-DAG transport

The rule universe is explicit, finite, unguarded and acyclic, with distinct scoped judgement identities and ordered explicit premise positions. All local supports are empty and costs are 0 or 1. Each paid set judgement is a nullary leaf; each element chooses one containing set; the target requires every element.

A cover yields a legal root-reachable DAG by choosing a containing set for each element and sharing the paid set nodes. Unused cover members are discarded, so DAG cost is at most cover size. Conversely, every valid target DAG contains the required membership witness for every element. Its distinct set indices form a cover, whose size is at most its paid-node cost. Duplicate occurrences of a paid set label cannot defeat this inequality. These two inequalities establish equality of optima and preservation of the budget decision. No bijection of all syntactic witnesses is required or claimed.

The construction has polynomial explicit size. The binary-prefix variant retains all element obligations and exactly the same paid set nodes. The all-unit original construction adds the fixed shared offset `n+1`; every feasible occurrence tree has `2n+1` nodes. These are separate cost-model controls, not processor-time measurements.

Empty universe, no sets, empty sets, duplicate indexed sets, and uncovered elements are handled correctly. With an empty universe the original target is a zero-price axiom. With an uncovered element there is no target proof. Duplicate set contents retain distinct family indices without changing the optimum argument.

### 2. NP membership and what a certificate proves

For the explicit acyclic empty-support class, selecting one original node for each used judgement and redirecting premise references preserves the input topological descent. Removing unreachable selections introduces no new node or cost. Empty support is important: there is no exact nonempty-support preservation obligation hidden in this normalization.

A witness therefore needs at most one node per declared judgement. Its selected rules and premise references have polynomial total length in the explicit rule-list input. Membership, labels, arities, references, reachability, acyclicity, and the unit-price budget can all be checked in polynomial time. Together with Set Cover hardness this supports the stated NP-completeness claim. It does not assert this upper bound for arbitrary compressed grammars, oracle guards, or unrestricted proof search.

Checking a supplied witness establishes validity and its stated cost, not minimality. The packet correctly separates this from proving that no cheaper witness exists. The finite compiler census independently compares values with exhaustive Set Cover enumeration only on the stated small cases.

### 3. Occurrence-tree numeric minimization

In the same empty-support acyclic class, the min/sum recurrence charges every premise occurrence, including equal labels in separate positions. Topological evaluation has polynomial arithmetic and numeric bit complexity for these 0/1 costs. A depth-bounded unfolded tree may nevertheless contain exponentially many nodes; compact rule pointers and its numeric optimum are not a promise of polynomial literal serialization. The sharing objective cannot use scalar child minima alone because internal paid-node overlap matters. Both the local-tie example and the disjoint-leaf counterexample to replacing sum with max are valid.

### 4. Exact-support tree transport

The unary loop version equates support with the union of chosen sets and price with their occurrence count. Removing repeated set choices cannot improve on a minimum cover. The acyclic take/skip construction removes any dependence on loops: its proofs are chains of exactly `m+1` nodes, one distinct judgement per layer, and the take indices specify a family subset. Exact support U is reached precisely by covers, with price equal to subset size.

The restricted acyclic-chain decision problem has a polynomial certificate consisting of the m take/skip bits. Tree and DAG prices coincide because a rooted unary chain has no branches to share. Thus this is a second valid hardness mechanism, independent of shared-node overlap.

Relaxing exact support U to support contained in available inventory U changes the task: the seed or all-skip chain gives empty support at price zero. Pareto pruning would retain that dominating option. The report correctly avoids applying this exact-support reduction to ordinary availability queries or to acquisition prices.

The compact rule list and explicit token-set labels are polynomial in the incidence input. The potentially exponential collection of `(judgement, exact support)` states is a different representation. A polynomial algorithm after that expansion does not supply a polynomial bound in compact input size. A polynomial height bound does not remove the distinction.

## Source and novelty boundaries

I read the complete new report and script, both imported compiler implementations, the source ledger and binding records, relevant predecessor theorem/contract passages, and the local AR3 reconciliation recording RP-T7/RP-T34. I did not independently repeat the author's broader bounded archive screening or claim that the missing RP manuscript has been exhausted by search.

Targeted primary-source text was retrieved for [Sahni, Problem G2 and Theorem 2.3.2](https://www.cise.ufl.edu/~sahni/papers/comp.pdf), printed pages 271–273. Its construction uses 0/1 edge prices and explicitly avoids repaying solved shared subproblems. This supports classical shared-AND/OR ancestry; the packet does not present that historical theorem as newly discovered. I also checked [Nederhof, sections 3–5](https://aclanthology.org/J03-1006.pdf), including the superior-function condition and topological evaluation. That supports the occurrence-weighted scope, not distinct-node optimization.

These were targeted extracted-text reads, not a visual scan audit or a complete-paper proof certification. Karp's Set Cover theorem is a correctly attributed standard imported result; I did not repeat the author's OCR/publisher retrieval. Gallo, Gao, and the unread Italiano/Nanni proof are not needed to validate the new written reductions. The missing full RP proof remains a real internal-priority limit. No historical or programme-wide novelty claim is warranted or taken from this review.

## Execution and currentness evidence

The initial exact-copy replay passed all 689 incidence systems, 1,510 nonbinary cover-to-DAG witnesses, both exact-support encodings on the same 689 systems, and the six binary/all-unit controls. It reproduced the author's result bytes exactly. `REVIEW_EXECUTION.json` records that revision; `REVIEW_INITIAL_FINDINGS.json` records the original defects.

After repair, a fresh exact script copy was executed from a temporary directory with symlinks to the actual predecessor directories. The output was confined to that temporary copy. `REVIEW_FINAL_EXECUTION.json` records the final pass, added admission controls, exact author-output equality, and frozen/current checks of all 15 predecessor bindings before and after execution. No predecessor or author source/output was written by the review.

The final receipt also checks the author's manifest and binds this review and its evidence. Finite execution corroborates the interface maps; the universal reduction and polynomial certificate claims rest on the written arguments reviewed above. No solver campaign, approximation guarantee, new Lean theorem, kernel replay, external human approval, source warrant, or T20 closure is conferred.
