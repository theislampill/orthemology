# Independent guarded-tree review

9 October 2026. Internal AI review, not external human validation. This is a bounded mathematical and executable review, with no repository integration, source mutation, DAG extension, formal-kernel certification, scientific adoption, or programme closure.

## Verdict

The proposed theorem is correct under its stated extensional, finite, fixed-support tree contract. Exact support is a sufficient interface for the proposed guards. The argument does not require guard monotonicity. The computational and terminal-observation qualifications below should be explicit.

## Proof audit

Let `state(T) = (root judgement, exact support)`.

1. If ancestor subtree A contains proper descendant D with equal state, replace A by D. D was already a valid complete subtree. At the surviving immediate parent, the ordered tuple of child supports is unchanged, so its fixed guard has the same truth value. Its resulting support is also unchanged, and this argument propagates to every surviving ancestor. Thus every surviving guard and the exact root support are preserved. Deleted guard instances need not remain satisfied because their rule occurrences are deleted.
2. The occurrence-additive cost of A is the cost of D plus the costs of deleted occurrences and side subtrees. Nonnegativity gives `cost(D) <= cost(A)`. Node count strictly decreases even for a zero-cost loop.
3. Repeating this operation terminates with no repeated state on a branch. Subtree supports decrease by inclusion along every branch. There are at most m strict decreases, and each constant-support block contains at most n judgements. Height is therefore at most `H = n(m+1)`. For a given root support S, `n(|S|+1)` also suffices. With no judgements there are no derivations, so the zero bound is vacuous.
4. Finite rules, finite arities, and bounded height give finitely many candidate trees. Every finite proof has an exact-support bounded representative with no greater cost. Consequently every realizable `(q,S)` has a minimum-cost representative within height H, even for zero-cost cycles and nonnegative real prices. Unsupported cycles remain unsupported.

## Correct recurrence and stopping test

Initialize `D_0(q,S) = infinity`, with infinity meaning unreachable. For each synchronous round, retain the old value and take the minimum over rules headed by q and ordered child supports `(S_1,...,S_k)` such that:

- every child entry `D_h(q_i,S_i)` is finite;
- the fixed guard `G_r(S_1,...,S_k)` is true;
- `S = B(r) union S_1 union ... union S_k`.

The corresponding candidate cost is `w(r) + sum_i D_h(q_i,S_i)`. Evaluate the empty guard tuple for nullary rules, which enter at round 1. Keep an actual immutable realizing tree for each finite entry.

Induction gives exactly the minimum cost among trees of height at most h. Replacing a child by a cheaper proof of the same exact support changes neither the guard tuple nor the resulting support, and reduces the additive cost. This establishes the induction without any support-inclusion monotonicity assumption. The bounded-tree proof makes `D_H` the global exact-support minimum table, hence a fixed point.

An earlier equality `D_(h+1) = D_h` is sound because the entire recurrence is then stationary. Compare all support-indexed minimum costs, including unreachable states. Equality of reachable support keys alone is insufficient; costs may still improve. Equality of witness identifiers is unnecessary, and mutable cyclic witness pointers are not a substitute for finite trees.

## Controls

The independently written `guarded_tree_checks.py` compares minimum-per-exact-support saturation to an oracle that retains every attainable support/cost pair, without dominance or same-support minimization. All 500 round comparisons passed for 100 seeded grammars with two judgements, one token, eight ground rules, arity zero through two, weights zero through two, and arbitrary Boolean support-tuple guards. Each exact table at H=4 equalled the next table. These finite checks supplement the prose proof; they do not prove the theorem universally.

Two targeted controls also passed:

- With judgements p,t and evidence a,b, give p nullary proofs of empty support and `{a,b}`, a zero-cost self-rule adding a, and a rule `p -> t` whose guard requires support exactly `{a}`. A terminal t proof first appears at round 3, exceeding `|J|=2`. Pareto pruning p to its empty-support proof prevents t forever. The guard rejects both empty support and `{a,b}`. This illustrates the inherited support-shrinking obstruction, not a newly discovered source failure.
- With judgements q0,q1 and evidence a,b, use `q0 <- q1` with no local support, a nullary empty-support q1, `q1 <- q0` adding a only when the child support is empty, and `q1 <- q0` adding b only when the child support is `{a}`. All prices are zero. Exact-support `{a,b}` at q0 first appears at round 6, attaining `|J|(|E|+1)` for this grammar.

## Necessary qualifications

- Effective compilation requires supplied, total, decidable guards and effective exact addition/comparison of represented prices. Merely saying a predicate is fixed does not provide an algorithm for evaluating an unspecified or undecidable description.
- Every dependence relevant to admissibility must be present in the judgement, exact support, or fixed rule metadata. Costs, shape, multiplicity, hidden ancestry, current inventory, minted identities, and cross-child compatibility beyond those declared support guards cannot silently affect acceptance.
- Fixed identity metadata can express source constraints; the compiler does not authenticate identities, establish genuine independence, or prove admitted rules and guards substantively sound.
- Terminal Pareto pruning is safe only after all support-sensitive terminal acceptance tests are resolved and no future guarded context will consume the pruned intermediate catalogue. For observations restricted to cost and ordinary availability `S subset inventory`, a dominating accepted terminal proof remains available whenever the dominated one is. Mandatory-use predicates or later provenance tests require retaining exact-support distinctions.
- This is an occurrence-priced tree theorem. Minimum cost for each exact support still loses useful shared-node structure and does not optimize DAG checking.

## Retained-source boundary

FABLE N5 already states that naive cut fails under transport and that root-tracking cut fails with two-root corroboration. It records a support-locality/guard-antitonicity repair and its remaining tension with corroboration. The typed-core candidate document explicitly labels its derived properties `DERIVED_BUT_UNVERIFIED` and says no committed artifact checks them.

This extension does not repair or vindicate unrestricted cut. Its substitution preserves the exact footprint at every surviving guard; the retained counterexample concerns inlining that changes footprints. It also does not establish that arbitrary FABLE transport or repair rules satisfy union-only support accounting or that the full calculus admits the required finite scoped grammar. Those are separate application obligations.

## Source and artifact bindings

SHA-256 of files directly read:

- `certificate-compilation-boundary-20261009/RESULT.md`: `3d8d11d73055b62913cf36138cc0b3b273d032f8f927a885ee2af11bd8eaf459`
- `user-checkpoints/extracted/P15/source-main/docs/project-closure/ar8r-v11/fable-research/AR8R-FABLE-R1-NEGATIVE-RESULTS.md`: `01fcca5e53a7f097df378ef6d68e1da5a40a750436ab211e1cd92b393d8d2220` (N5 inspected)
- `user-checkpoints/extracted/P15/source-main/docs/project-closure/ar8r-v11/fable-research/AR8R-FABLE-R1-TYPED-CORE-CANDIDATES.md`: `19f1ee22e51db677f2b79e3a1db10923db35189a1cb7bc86bb710164dbd15f4a` (Core B status and cut claims inspected)

Review artifacts:

- `guarded_tree_checks.py`: `4e4bf9f24bf98f620cb1480da7586f212fd41087ce3a5a56427131fa29382c8a`
- `guarded_tree_check_results.json`: `cc1a19b95cf95aef060746a9af580f1ae6fcc8ef2317d189127a8f3ef8fddc0d`

`guarded_tree_activity.jsonl` records prospective worked-operation and source/test boundaries. It begins after the first predecessor read, is not a complete session-time audit, claims no accumulated active duration, and does not credit waiting or packaging as substantive work. A transient suspicion about shell time was checked and corrected: `date -u` agreed with `clock.curr_time`; only `ls` displayed local time.

## Submitted implementation and result review addendum

The submitted compiler's recurrence, immutable witness construction for validated inputs, occurrence-charged traversal, and equal-state pruning implement the proved tree contract. No theorem-level or source-scope blocker was found in `RESULT.md` at SHA-256 `378ca6d1d9ffde10f76e8ab5f47b04b0b7754135d5517661ffa2fb1c4f778994`.

A concrete input-validation defect was found in initial compiler `74f113b0b0c135ecdf999048648bf1801de10448f53c7f94dc288c0b6ac90c16`: a list-valued premise field was accepted, and the compiler emitted a witness its own traversal rejected. The author corrected validation to reject mutable local support/premise containers and malformed guard structures. This review did not edit submitted main files.

Fresh verification of revised compiler `51d1a5daf3ac76952b35b3fcaffb0e3b1838b1d518105a0ac3e78b48e821c3c1`, against submitted test file `72b6f71dcc29a038ac8c4db1b3c26fd568b4eb6b64846354e02f5ac83f62c8e3`, passed all nine submitted tests and all five independent deterministic controls. The latter cover sharp height six, unchanged support keys with improving costs, a strictly nonmonotone terminal guard, removal of a positive-cost side subtree under exact-support pruning, and rejection of the malformed mutable-premise input. Initial failure and revised success logs are both retained.

The submitted general sharpness construction is correct for every n>=1, m>=0, with arrows read premise-to-head and target q_n. Starting with nullary q_1 at empty support, chain rules give q_n at empty support in n nodes. The only way to obtain q_1 at prefix A_j for j>0 is the return rule from q_n at A_(j-1), and q_n then needs the remaining n-1 chain edges. Hence its least height is n(j+1), giving exactly n(m+1) at the full prefix. This includes n=1 and m=0.

A reporting-scope clarification was sent to the author: the submitted main suite is deterministic and not randomized, whereas the optional earlier reviewer sanity check above did use 100 small seeded grammars. Those bounded supplemental checks are explicitly disclosed and are not evidence of an unrestricted theorem, a performance study, or an optimization campaign. This remains internal AI review, not external human validation.

## Final report-only revision binding

Final `RESULT.md` SHA-256: `67392fef19c436aa59b00a719698d5f2ecd877b4611c1a1c57c7bb445c6eb4ec`.

The narrow final revision was inspected. Reversing exactly its two verification/disclosure text replacements reconstructs the previously reviewed report byte-for-byte, verified by SHA-256 `378ca6d1d9ffde10f76e8ab5f47b04b0b7754135d5517661ffa2fb1c4f778994`. Those replacements accurately distinguish the deterministic main suite from the disclosed bounded seeded reviewer check and explicitly list nine main tests plus five independent controls. They introduce no theorem or scope change. The compiler and main test file retain the revised hashes recorded above. No additional campaign was run for this final report binding. Internal AI review only; no external human validation is asserted.
