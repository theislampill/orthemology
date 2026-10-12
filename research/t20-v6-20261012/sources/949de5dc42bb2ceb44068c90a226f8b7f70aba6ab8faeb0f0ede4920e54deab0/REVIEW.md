# Independent internal review: guarded shared-DAG normalization and attainment

9 October 2026. Review of the frozen `guarded-shared-dag-attainment-20261009` packet. Reviewer artifacts are separate from the authored packet and the previously sealing research package.

## Disposition

Accept the bounded written transport and supplied-witness normalizer at their stated scope. No mathematical or executable-control defect requiring author repair was found. Independent exact-copy replay passed all 13 deterministic tests, and all seven predecessor hashes matched before and after execution.

The result is the existing unguarded earliest-occurrence DAG argument transported through the already-described finite exact-state refinement. It adds the explicit guarded-DAG support/price preservation and attainment statement at this interface. It is not a new general finiteness method, a cheapest-standalone dynamic program, or a claim of field-wide priority.

This review provides no new Lean theorem, kernel certification, source warrant, external human review, performance guarantee, integration, adoption, or T20 closure. The exact accepted revisions and reviewer evidence are bound in `REVIEW_RECEIPT.json`.

## Actual inherited interface

I read the new report and both Python files in full. I checked the relevant exact-support contract, state-refinement note, and explicit DAG boundary in `source-sensitive-proof-compilation-20261009/RESULT.md`, the actual immutable rule and support-tuple representation in its `guarded_compiler.py`, the predecessor earliest-occurrence theorem and implementation, and the already-reviewed shared-cost boundary/repair record. I inspected `GuardedTree.lean`'s grammar, support, and validity definitions without rerunning a kernel or crediting its tree theorems to DAGs.

The inspected source confirms that a guard has one input support per ordered premise position. The Lean field is a predicate on a finite-indexed tuple of supports; the Python executable uses an immutable finite permitted-tuple set or the always-true sentinel. Guards are not functions of internal child identities, proof shape, standalone cost, mutable inventory, or paid-node overlap. Fully scoped judgement labels retain the other substitution-relevant distinctions.

The guarded-tree report already describes refinement to `(q,S)` and separately says it has not supplied a guarded DAG compiler. The new report credits both that route and the unguarded DAG lemma. Its bounded absence observation is not used to claim an exhaustive programme or literature search.

## Normalization proof

The state of an original node is its head judgement and the exact union support of its reachable sub-DAG. Choose an original premise-first topological order and the earliest original occurrence of each state. For each representative, keep its admitted rule and redirect each ordered child position to the earliest occurrence of that original child's state.

The proof's critical inequality is correct: the new child rank is no later than the original child rank, which is strictly earlier than the representative parent. All redirected edges therefore descend. This works even when the grammar has cycles; only the supplied proof graph must be acyclic. A later arbitrary representative has no such guarantee, as the self-edge countercontrol shows.

Exact-state preservation needs an induction and is not merely assumed from the labels. In increasing representative rank, every redirected child has its original judgement and exact support by the inductive hypothesis. The parent therefore sees precisely its original ordered judgement/support tuple. Its guard remains true, whether monotone, antitone, nonmonotone, or sensitive to position. Its union support remains equal, not just contained. Nullary guards are included because the empty tuple is explicitly checked.

Selecting the representative of the original root state may change the root rule. Restricting afterward to nodes reachable from that selected root removes no child of any retained representative. Thus every retained exact state and guard remains valid, and the target judgement/support pair is preserved. The report correctly disclaims preservation of root-rule identity, certificate history, and a canonical choice independent of topological order.

The retained representatives are distinct original occurrences. Their rule prices are unchanged, so their sum is no greater than the original whole-graph sum when prices are nonnegative. This argument does not compare cheapest standalone subproofs and does not charge a shared child once per incoming reference. At most one node remains per state, giving at most `|J| 2^|E|` nodes. Zero-price deletions cause no termination problem because the construction and its graph traversal are finite.

## Finite refinement and actual attainment

For each original rule and each allowed ordered support tuple, the refined grammar assigns the head state obtained by local-support union and the premise states position by position. The source rule identity and tuple distinguish the refined instances. Finite evidence and finite arity give finitely many tuples; the allowed nullary tuple is handled explicitly.

Lifting a guarded proof to this grammar preserves its nodes, references, and price. In the reverse direction, topological induction on a finite refined proof shows that the actual support at each node equals its declared support coordinate, so erasing the coordinates recovers a guard-valid original proof. This is the necessary semantic bridge; it is present in the report.

One refined rule or absence per exact state gives finitely many assignments. A chosen target's reachable component must contain every referenced state and be acyclic. Irrelevant cycles or missing choices outside that component need not invalidate it. Every normalized supplied proof has such a state-indexed representative, up to renaming node identifiers.

For a reachable exact root state, this catalogue is finite and nonempty. Its least-cost member is itself valid. Every unrestricted valid proof is no cheaper than some normalized catalogue member, so the least catalogue member attains the unrestricted minimum. For an unreachable state no minimizing witness exists; infinity is only the numerical convention. Minimization over finitely many possible root supports is likewise attained whenever any proof exists.

The separation between existence and effective enumeration is correct. Finite fixed nonnegative real prices suffice for mathematical attainment. An executable compiler additionally needs decidable guard evaluation and exact effective arithmetic/comparison. The Python controls use integer/rational prices and immutable tables. Infinite rule supplies or varying occurrence-price sources are outside the finite-catalogue claim.

## Boundaries and negative evidence

The report and tests preserve the important failures rather than overstating the extension:

- Judgement-only merging can change child support and invalidate a guard. Equal exact states are required.
- Ordered duplicate premises remain separate positions. Different supports at equal judgement labels cannot be collapsed; equal-state repeated references may share one charged node.
- Equal total union is insufficient when the ordered child-support tuple changes. The reversed-order and support-enlargement controls reject such changes.
- A false nullary guard supplies no proof. A sole unsupported self-rule supplies no finite acyclic proof, even at zero price. An allowed seed changes that situation.
- An invented rule or altered cheap record under an existing name is rejected by full rule membership, independently of structural traversal.
- Root-reachability, arity, reference validity and premise-first acyclicity are checked. Unreachable charged nodes are not accepted as part of the certificate.
- Earliest-state selection need not be cheapest. The supplied 5/1 leaf example normalizes from cost 6 to 5 while a different normalized proof costs 1.
- The inherited exact-support sharing counterexample still yields scalar tree value 9 and a shared-DAG value 5. A one-node-per-state whole graph does not justify preselecting a cheapest standalone witness at every state.
- Distinct-node identity requirements can fail after normalization and are outside the declared support-only guard contract. Fixed source identities encoded in evidence supports are a different issue.
- A negative-cost self-rule gives finite chains of price `-k` with no least price. Rank and support preservation survive, but the retained-subset price inequality fails. The checker rejects a negative-price grammar.
- Branch height and total node count differ. The one-judgement, three-token example has eight distinct states and branch height two, so the inherited four-node branch bound cannot be substituted for the total-node bound.

No new negative defect was discovered during this review. The author's retained test-first red log records two intentionally failing initial implementation controls. I read that record, but did not reconstruct or claim an independent execution of the unavailable red-stage implementation. The final corrected implementation was independently executed in full.

## Implementation review and replay

`dag_value` first validates the declared grammar, then checks each used rule against its admitted records. It checks ordered premise references, computes exact supports bottom-up, tests each ordered guard including nullary guards, enforces whole-certificate root reachability, and sums each stored reachable node once. It retains the states needed by normalization. The implementation matches the declared finite premise-first encoding; it does not authenticate the rule licences.

`normalize` computes earliest representatives from the original checked states, redirects to those original-state representatives, restricts to the selected root component, and renumbers in original order. It rechecks the result and asserts preservation of exact root state, nonincreasing cost, state uniqueness, and the finite node bound. The source contains no cheapest-proof search.

The small `refine`/`catalogue` helpers in the tests do instantiate finite support tuples and invoke the unchanged whole-DAG compiler on tiny fixtures. Decoded witnesses are rechecked with the new admission/guard checker. At any refined root state all valid decoded proofs have that same exact support, so the inherited terminal support/cost pruning does not silently mix support states.

For the independent replay, exact copies of `guarded_dag.py` and `test_guarded_dag.py` were run in a temporary directory with read-only symlinks to the bound predecessor files. The command was `python -B -m unittest discover -v`. All 13 test outcomes matched the author's final replay. Timing text was not treated as invariant evidence. All seven frozen input hashes matched before and after; no authored file, predecessor, or bytecode cache there was written by the review. `EXECUTION.json` retains the invocation, output, and bindings.

The final receipt checks every authored manifest entry and binds this review. These tests corroborate the implementation and finite interface; the universal normalization and attainment claims rest on the written proof reviewed above. The work stops at that scope, without a performance, sampling, solver, or formalization campaign.
