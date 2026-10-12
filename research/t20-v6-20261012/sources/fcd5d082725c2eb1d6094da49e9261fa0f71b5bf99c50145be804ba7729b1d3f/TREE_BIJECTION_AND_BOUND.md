# Exact support tree reduction and support chain bound

This is the written mathematical transport used by `RESULT.md`. It is not a new Lean theorem, a kernel-checked proof, or a claim to have reverified the predecessor implementation.

## Contract

Let `J` be finite, `n = |J|`. Let `R` be a finite set of distinct rule labels. Rule `r` has head `h(r)`, an ordered premise list `(q_1, ..., q_k)`, finite local support `B_r`, fixed nonnegative price `w_r`, and fixed predicate `G_r` on ordered exact premise supports. Let `B` be the union of all `B_r`. The ambient token universe need not be finite.

A valid rule tree has children proving the indicated premises, satisfies `G_r` on their exact supports, and has support and cost

    S(r(T_1,...,T_k)) = B_r union S(T_1) union ... union S(T_k)
    c(r(T_1,...,T_k)) = w_r + c(T_1) + ... + c(T_k).

Every premise occurrence contributes its cost, even when two premise states or entire subtrees coincide. Height counts rule nodes, so a nullary tree has height one. Structural induction gives `S(T) subseteq B` for every finite valid tree.

## Refined grammar

Its nonterminals are the pairs `X(q,S)` with `q in J` and `S subseteq B`. For each rule `r` and each ordered tuple `(S_1,...,S_k)` of subsets of `B` such that `G_r(S_1,...,S_k)` holds, add a production with the distinct label `(r,S_1,...,S_k)`:

    X(h(r), B_r union S_1 union ... union S_k)
      -> r(X(q_1,S_1), ..., X(q_k,S_k)).

Its weight function is `f_r(x_1,...,x_k) = w_r + sum_i x_i`. When `k=0`, this is a nullary production of constant weight `w_r`, present precisely when the nullary guard holds. The label retains `r` even when another rule has identical head, children, support and price.

There are at most `n 2^|B|` nonterminals. Each rule contributes at most `2^(k |B|)` productions. The construction is finite as mathematics. Enumerating admitted productions effectively requires decidable guards; merely having a fixed Prop-valued guard does not provide that algorithm.

## Forward map

Induct on the original valid tree `T`.

For `T=r(T_1,...,T_k)`, let `S_i=S(T_i)`. Apply the induction hypothesis to the ordered children. Validity of `T` gives the precise guard condition that admits the production `(r,S_1,...,S_k)`. Attach those child derivations to that production. Their nonterminal labels match the production's ordered right-hand side. The head support is exactly `S(T)` by its union definition.

This defines `F(T)`. It inserts support annotations and the corresponding refined production label without changing tree shape, premise positions, or rule occurrences.

## Reverse map

Induct on a refined derivation tree `U` rooted at `X(q,S)`.

The root production is labelled `(r,S_1,...,S_k)`. Its presence certifies the fixed guard on that ordered support tuple. By induction, erase each child derivation to a valid original proof of `q_i` with exact support `S_i`. Applying `r` to those ordered children produces an original valid proof with head `q` and support `S`.

This defines `E(U)`. It erases only the auxiliary state and production annotations.

## Inverse and preservation properties

Induction gives `E(F(T))=T`. Conversely, each refined derivation's child annotations equal the supports of its erasure by the reverse-map induction. Reannotation therefore recovers the same support tuple and the same labelled production at every node, proving `F(E(U))=U`.

These equalities give a bijection for each exact root state. Height is unchanged because neither map inserts nor removes a node. Recursive cost is unchanged because each corresponding node contributes the same `w_r` and the same ordered list of child occurrence costs. In particular, two equal child states remain two positions and contribute twice; no DAG sharing discount is introduced. The root's fully scoped judgement and exact support are preserved.

Thus attainable costs, minimum costs when attained, and attaining trees correspond exactly between the original guarded system and this finite weighted grammar.

## Minimum derivation theorem transport

Work over nonnegative finite costs with `infinity` for unreachable states. The valuation `w_r + sum_i x_i` is coordinatewise nondecreasing and is at least each `x_i`, because the other summands and `w_r` are nonnegative. The nullary constant is allowed. These verify the superior-function hypotheses in Knuth's minimum-derivation theorem, also stated explicitly in Nederhof section 4. Rational prices embed into the nonnegative real domain without changing comparisons or sums.

Apply that theorem only after the finite admitted grammar has been specified. It establishes the refined state minima. The bijection transfers them to the original exact states. No monotonicity of `G_r` under support inclusion was used: a guard decided which production exists; it is not being reapplied to a smaller or merged support during optimization.

The global transport does not cover arbitrary negative prices. Additive functions remain monotone in their arguments then, but need not be superior. A negative-price cycle may make minimum attainment or stabilization false.

## Finalization order supplies acyclic witnesses

Consider the finite-valued states in Knuth's construction. At the moment state `v` is finalized, its chosen finite candidate uses an admitted production all of whose antecedent states have already been finalized. Select one candidate production attaining that finite candidate minimum, and retain references to the antecedents' previously retained witnesses. Unreachable states assigned `infinity` do not receive finite witnesses.

Nullary productions are available without antecedents and supply the initial finite witnesses. An unsupported self-cycle supplies no candidate before its own state is finalized, so it cannot seed a proof. Zero-cost cycles cannot create a cyclic retained witness either: a self-reference or reference to a not-yet-finalized state was ineligible at selection. A later zero-cost cycle can tie an existing optimum without invalidating its already selected acyclic witness.

Assign each finite finalized state its distinct finalization index. On every parent-to-child edge of every unfolded retained tree, that index strictly decreases. This is the acyclicity argument. It does not assume strictly positive rule prices, strictly decreasing child prices, unique minima, or strict improvement on a tie. Equal prices are harmless because the index, not the price, decreases.

No branch can repeat the same refined state. The generic bound obtained by counting all refined states is `n 2^|B|` rule nodes per branch. The next argument uses more of the original contract.

## Support chain refinement

For every parent-to-child edge, the child support is a subset of the parent support, since the production head support is the union of the local support and all child supports. Along a branch rooted at exact support `S`, supports therefore form a descending inclusion chain. At most `|S|` edges can strictly decrease that support.

Split the branch into maximal consecutive blocks of equal support. There are at most `|S|+1` blocks. Within any one block, repeating a judgement would repeat the full refined state, which finalization order excludes. A block therefore has at most `n` nodes. It follows that the retained optimum has height at most

    n (|S| + 1) <= n (|B| + 1).

This is an external-theorem-based derivation of the local support-chain bound. An equivalent intrinsic proof repeatedly removes an ancestor subtree in favour of an equal-judgement/equal-support descendant, using nonnegativity to avoid raising cost; that argument is already present in the first local report.

The sharp family in that report is not newly constructed here: its support-prefix guards force exactly `n(m+1)` nodes with `m` evidence tokens, even with all prices zero. This confirms that a strictly increasing-price argument would be the wrong explanation of either the upper bound or its extremal case.

## Relation to the synchronous recurrence

On refined keys, the actual local update takes the minimum of the retained old value and all admitted production valuations on old antecedent values, starting from the all-unreachable table. Ordinary height induction shows that round `h` has the exact attained minima among derivations of height at most `h`: candidates assemble height-bounded witnesses, and replacing a child with the old minimum at its identical refined state cannot raise additive cost.

Combining this independent recurrence semantics with the preceding representative bound gives global correctness by round `n(|B|+1)`. Since no finite proof can improve the global minima, the next update is unchanged. Earlier equality of the entire consecutive numeric tables is preserved by determinism; equality only of reachable keys is insufficient.

This explains how the classical minimum-derivation theorem and support structure relate to the local recurrence. It is not a claim that Knuth's priority algorithm executes these synchronous rounds. The local Lean package independently verifies the stated synchronous recurrence; this file's new cross-framework proof has not been formalized or kernel checked.

