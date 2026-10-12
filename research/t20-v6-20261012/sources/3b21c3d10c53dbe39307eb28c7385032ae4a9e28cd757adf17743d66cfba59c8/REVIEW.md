# Independent written-mathematics review

Reviewed 9 October 2026. This is an internal mathematical review of the hash-bound report and transport, not a new kernel proof, a replay of the predecessor verification, a new source witness, or T20 closure.

## Verdict

**Pass for the declared written-mathematics scope; no outstanding findings.** One nonblocking wording clarification identified during review was corrected by the report's author and rechecked. No substantive error was found in the finite refinement, labelled-tree bijection, cost preservation, superior-function application, finalization-order argument, support-chain bound, sharpness attribution, or comparison with the synchronous recurrence.

The conclusions require the stated finite judgement/rule sets, fixed ordered arities, union support, exact-support-only guards with fixed metadata, and finite nonnegative additive occurrence prices. They do not establish a shared-DAG optimizer, an executable arbitrary-guard compiler, substantive guard soundness, or a new priority algorithm.

## Resolved finding R1: make the generic bound explicitly a height bound

- Severity: low; clarification only, not a failed theorem.
- Location: `TREE_BIJECTION_AND_BOUND.md:67` in the reviewed version.
- The sentence saying that the generic bound is `n 2^|B|` “rule nodes” should say “rule nodes per branch,” or simply “height.” The preceding sentence already concerns branches, and `RESULT.md` explicitly warns that unfolded witness size is not bounded polynomially, so the intended reading is sound.
- A total-size reading would be false: with empty support, three states can have a nullary rule for `a`, a binary rule for `b` with premises `(a,a)`, and a binary rule for `c` with premises `(b,b)`. The retained `c` tree has height three but seven rule occurrences. All charges may be zero.
- Suggested edit: “The generic height bound obtained by counting all refined states is `n 2^|B|` rule nodes per branch.” No change to the mathematical argument is needed.
- Resolution: the author added “per branch” at the indicated sentence. Independently reversing only that insertion reproduces the complete initially reviewed file's SHA-256, establishing that no other mathematical text changed. This review's final input binding is the corrected file.

## 1. Contracts and finite support refinement

The first local `RESULT.md`, sections 2–3, supplies finite fully scoped judgements, finite labelled ground rules, ordered premises, fixed exact-support guards, union support, nonnegative additive occurrence costs, and height counted in rule nodes. The transport retains all of these. In particular, the guard is not allowed to inspect hidden proof history, tree shape, changing metadata, price, or freshly created identities.

The second local `RESULT.md:9–28` permits an infinite ambient evidence type but uses the finite union `B` of finite rule-local supports. The transport correctly adopts this grammar-local universe. A structural induction places every finite tree's support inside `B`; consequently states with support outside `B` are unreachable and need not enter the refined grammar. This conclusion does not require the ambient evidence type to be finite.

The counts are correct: at most `n 2^|B|` refined states and at most `2^(k|B|)` support tuples for a rule of arity `k`. An arbitrary fixed predicate defines a finite mathematical subset of those tuples. It does not furnish effective enumeration or a guard decision procedure, a distinction both reviewed documents preserve. No support-monotonicity assumption is introduced.

## 2. Bijection and preservation

The refinement records both the complete judgement and exact support, and gives every admitted production its rule label and ordered support tuple. This prevents distinct rule labels with identical data from collapsing. The right-hand side is a list, so repeated states remain separate premise occurrences.

The forward induction uses the actual supports of the ordered children. They determine a unique refined production admitted by the original guard. The reverse induction obtains exactly those child supports from the child nonterminal annotations, then reconstructs the same original rule node. The inverse equations follow node by node: erasure loses only annotations that are uniquely recoverable from the tree. This is a bijection of finite valid labelled trees at each exact root state.

No node is inserted or deleted; hence height is preserved. Recursive cost preservation follows from the unchanged node charge and unchanged list of child occurrences. Replacing a child by a minimum at the identical refined state preserves every declared input to the parent guard. Neither a cheaper subset support nor an equal union of a differently ordered tuple can be substituted on that basis. These observations validate the report's position-sensitive-guard example and its restriction of the obstruction to summaries that actually discard that information.

## 3. Superior functions and source check

Knuth's original section 1 defines the domain as nonnegative extended reals and explicitly includes nullary constants. Sections 3–4 provide the all-state algorithm and its correctness argument. The inspected material is the original article's third-party OCR reproduction, whose typography is visibly damaged; no publisher PDF or source-byte identity was verified. [Inspected Knuth article](https://paperzz.com/doc/6873927/a-generalization-of-dijkstra-s-algorithm---1.-the).

Independently, Nederhof's primary PDF, section 4, states coordinatewise monotonicity and dominance over every argument. Section 2 retains ordered antecedent lists and occurrence costs; Figure 4 makes the relevant candidate eligibility explicit. [Nederhof primary PDF](https://aclanthology.org/J03-1006.pdf).

For this instance, define the weight function on `[0,infinity]^k` by the extended nonnegative sum `w_r + sum_i x_i`. It is monotone and at least each argument; if an argument is infinite, the value is infinite. For arity zero it is the finite constant `w_r`. Nonnegative rational charges embed in this domain without changing finite sums or comparisons. The reviewed text's explicit domain restriction therefore discharges the hypothesis; it is not silently assuming superiority on all rational or real inputs.

The bounded-height recurrence may still be meaningful with negative rational charges, but that does not extend this theorem application. The report correctly excludes such an extension. It also does not infer uniqueness of arbitrary algebraic fixed points from the non-strict superior-function result.

## 4. Finalization order, nullary rules, and zero cycles

Knuth section 3 computes a candidate from a production whose antecedents are in the already-finalized set. Nederhof Figure 4, steps 2–5, independently exhibits the same condition and admits arity zero. Thus the finalized-antecedent premise used in the transport is in the cited construction, not an added property of an unspecified optimizer. Knuth's all-state version supports the report's all-state conclusion; Nederhof's goal-stopping presentation need not be mistaken for a complete run over every state.

For a finite candidate, every antecedent value is finite under the additive valuation. Inductively retain a realizing production and the already-retained antecedent witnesses when the state is finalized. Nullary candidates start this induction. Each retained parent-to-child reference then strictly decreases the finalization index, regardless of equal prices. No unsupported cycle can supply its own initial candidate, and no later tie requires replacing a retained witness with a cyclic one.

Repeated occurrences of the same antecedent may share a retained reference operationally, but unfolding copies that witness into each child position and charges every copy. Along a branch the indices strictly decrease, so the same refined state cannot recur. Sibling repetitions are permitted. This proves the required branch property without strict positivity, strict cost improvement, or uniqueness of minima.

## 5. Support-chain bound and sharpness

The union equation makes a child support a subset of the parent support. On a branch rooted at support `S`, there can therefore be at most `|S|` strict support decreases and at most `|S|+1` maximal equal-support blocks. Within a block, more than `n` nodes would repeat a judgement and therefore a refined state, contradicting the preceding index argument. The resulting height bound is exactly `n(|S|+1)`, and hence at most `n(|B|+1)`.

This bounds an optimal representative at every reachable exact state. Since its cost is globally minimal, it is also no dearer than any given proof at that state. The intrinsic equal-state-pruning proof in the first local report establishes the same representative property directly. There is no dependence here on a strictly decreasing price along branches.

The sharp family in the first local report was checked as written. With the prefix supports `A_j`, the base has height one. The `n-1` forward judgement steps make the first `q_n` proof height `n`. Each guarded return to `q_1` adds one node and the subsequent forward chain adds `n-1`, so the forced minimum height at `q_n,A_j` is `n(j+1)`. The only admitted return for prefix `A_(j-1)` introduces its next token. The edge cases `n=1` and `m=0` behave correctly. Zero charges do not shorten any required proof. This establishes sharpness in the declared arbitrary-fixed-guard class, and the reviewed package correctly credits the existing local construction rather than claiming to have originated it.

## 6. Actual recurrence and algorithm schedules

The second local report describes an actual old-table update, starting from all unreachable entries, that retains old values and minimizes enabled rule candidates over old antecedent values. It separately states the height-indexed semantic invariant. The transport accurately uses this distinction; it does not define the recurrence to be its desired semantics.

Height induction aligns its round `h` with minimum costs at height at most `h`. The optimal-representative bound then yields global correctness by round `n(|B|+1)`. The next numeric table is unchanged because all candidates are valid proofs and the existing entries are already global minima. Complete-table equality propagates under the deterministic step. Equality of reachable-key sets alone does not have this implication.

Knuth finalizes one minimum candidate state at a time; the synchronous recurrence consults only the entire preceding table in a round. Their shared optimal cost semantics do not equate intermediate tables, priority steps, or round counts. The reports make that limitation explicit. The Lean package's nonnegative rational stabilization theorem is not represented as a verification of Knuth or of the new written reduction.

## 7. Sharing boundary, credit, and review limits

The grammar bijection is about occurrence-charged trees. The hypergraph discussion restricts its optional set-tail encoding to recursive valuation, retains multiplicity through coefficients, and explicitly separates this from charging a distinct shared hyperarc once. It does not claim the optional auxiliary-source encoding preserves tree height. No sharing-aware minimum is inferred from the tree theorem.

The attribution ledger assigns the minimum-derivation machinery to the established sources, the local height result and sharpness family to their predecessors, and this package only the written cross-framework relationship. No claim of historical novelty follows from not finding the exact support-chain formula in the inspected passages. I found no incorrect novelty credit in this bounded comparison.

Both target documents, both local contract reports, and both ledgers were read. External checking was limited to the exact Knuth and Nederhof materials already listed in the source ledger. Goodman, Gallo et al., Green et al., and unused search leads were not independently reopened in this review; no exhaustive literature conclusion is offered. The tree-versus-sharing assessment above rests on the explicit mathematical objectives and the reviewed text, not a new audit of every hypergraph theorem.

No Lean source, Python implementation, predecessor replay, source-authenticity witness, or integration was attempted. The existing package checksum file was checked successfully. `REVIEW_RECEIPT.json` binds the reviewed inputs and this report; `REVIEW_SHA256SUMS` hashes the report and receipt. Original documents and existing packaging files were not edited by this reviewer. The report's author made the independently checked R1 wording correction and refreshed the packaging receipt and checksum file during review; the final receipt records both the initial and final bindings.
