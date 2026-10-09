# Compiling certificate frontiers from finite grounded rules

9 October 2026. A bounded constructive continuation of T20. Existing inputs are read-only. No repository integration, scientific adoption, or programme closure.

## Result

The earlier frontier theorem assumed an already admitted finite proof catalogue. That assumption can be discharged for a finite, fully scoped, grounded positive rule system with persistent reusable evidence and nonnegative additive checking costs, even when its rule graph has cycles.

Every finite derivation tree is dominated in both required evidence and checking cost by a tree with no repeated scoped judgement on any branch. Consequently, if there are n judgements, at most n synchronous support/cost saturation rounds suffice to compile the complete terminal Pareto frontier of **all finite derivations**. The algorithm keeps actual proof witnesses. It neither presupposes a catalogue of useful proofs nor treats a cycle as a proof.

There is also a narrowly matched shared-proof result. If checking charges each node of an acyclic proof DAG once, every DAG is dominated by one with at most one node per scoped judgement. Finite rule-choice enumeration therefore computes its exact frontier too. Its costs generally differ from tree costs, and standalone support/cost pruning of intermediate DAG proofs is unsound. A four-judgement example makes the optimum 5 for DAG checking and 9 for tree checking.

These are constructive theorems about a declared proof grammar. They do not establish that the grammar is faithful to an unrestricted logic, natural-language argument, or the inherited HasE system. The existing Lean certificate proves finite support/cost normalization; it does not certify the new rule-compiler theorems.

## 1. What the inherited package leaves open

The research report, §2.2, fixes a finite admitted catalogue and mentions recursive compilation for an **acyclic** positive rule system. Its §2.3 excludes arbitrary fragment scheduling and reuse. Its frontier theorem then works with extracted support/cost pairs. The companion kernel report explicitly excludes derivation trees, rule checkers, and proof-object realization. Thus the finite cyclic rule-compiler result is not already present in either deliverable.

The present work supplies a sufficient interface between a justified finite rule grammar and that catalogue theorem. It does not replace rule admission with numerical optimization.

The retained representation manuscript distinguishes identity/version, source and scope, and record validity from substantive validity. Its finite-record assumption explicitly warns that a finite handle to an infinite family is not an enumeration of that family. Those distinctions are load-bearing here: the set of judgement labels must actually be finite after the relevant contexts and types have been included.

## 2. Exact contract

Fix finite sets J of fully scoped judgements and E of authenticated evidence-token identities. Let n=|J| and m=|E|. A judgement includes every parameter on which proof substitutability depends: proposition or type, context, claim and rule version, source restrictions, and any relevant resource or independence requirements.

Fix a finite set R of **ground rule instances**. A rule r consists of:

- a head h(r) in J;
- a finite ordered list p(r)=(q1,...,qk) of premise judgements in J, possibly with repetitions;
- a local evidence requirement B(r) contained in E;
- a local checking cost w(r) in the nonnegative natural numbers.

A nullary rule may be an admitted logical axiom, an evidence introduction, or another justified leaf. Its evidence requirement is still explicit. A rule with premises is available exactly when proofs of those precise judgements and its local evidence are supplied. There are no hidden global admissibility tests depending on the proof's shape, history, or the particular proof chosen for a premise. Rule-instance validity is settled at admission, and conditional soundness of the grammar is a separate assumption.

The rules are positive in this operational sense. A judgement whose *content* is a negation can be present, but absence of a proof is not itself an evidence-producing rule. No circular or coinductive proof principle is assumed.

Evidence is persistent, reusable, and combined by set union. Repeated occurrences of a judgement allow reuse of a proof of that same judgement. A demand for two independent sources cannot be encoded merely as two identical P premises: source-labelled judgements or an explicit independently justified relation must retain that demand. If this refinement makes the required judgement universe infinite, this theorem's finiteness assumption has not been met.

All rule premises must be replaceable by any valid proof of the same fully scoped judgement. A context-sensitive typing or assumption-discharge system is covered only after this property is demonstrated for its chosen finite ground interface. Erasing contexts or types to manufacture repeated labels invalidates the pruning proof below.

### Two different cost contracts

In the **tree contract**, every rule occurrence is checked and charged separately. For a tree T with root rule r and children T1,...,Tk,

    support(T) = B(r) union support(T1) union ... union support(Tk)
    tree_cost(T) = w(r) + tree_cost(T1) + ... + tree_cost(Tk).

Thus a syntactically copied premise subtree is charged twice under this expressly declared contract, although its evidence tokens are acquired only once. This is appropriate only when actual checking repeats that work. The price does not infer acquisition cost from the number of leaf uses.

In the **DAG contract**, an actual finite acyclic proof graph has one rule at each node and one outgoing premise reference per premise-list position. All nodes are reachable from its root. Each distinct node is checked and charged once; its local price includes checking its own ordered premise references. Repeated references to the same child do not recheck that child's internal proof. Total support is the union of local B labels; total cost is the sum of w over distinct nodes.

These are specified terminal checking prices, not measured runtime models. Authentication paid at acquisition is not charged again unless explicitly included. Compilation work is separate from terminal checking. A compiler's stored witness still must be reconstructed and checked under the declared contract before reporting a completed proof-bearing result.

For either contract a pair (S,c) dominates (S',c') if S is contained in S' and c is at most c'. At least one strict comparison makes dominance strict. A frontier retains exactly the undominated pairs, with one realizing witness per retained pair. Different witnesses with the same pair need not be equivalent for other provenance questions.

## 3. Finite tree compilation theorem

**Theorem 1.** Under the tree contract:

1. Every finite proof tree of q is dominated by a proof tree of q of height at most n, where height counts rule nodes on a longest root-to-leaf path.
2. Every undominated pair of the possibly infinite family of finite q-proofs has an actual representative of height at most n. Every finite q-proof is dominated by an undominated such representative. In particular the global frontier is finite and has at most 2^m pairs per judgement.
3. The synchronous frontier recurrence below, initialized with no proofs, produces this global frontier after n rounds, with valid realizing proof trees. It is already a fixed point then. Equality at an earlier round is also a sound stopping test.

*Proof of 1.* If two nodes on one branch carry the same scoped judgement q, replace the ancestor's whole subtree by the descendant's subtree. The replacement is legal by the exact premise-substitution contract. The descendant's evidence support is a subset of the ancestor's support, since every node combines evidence by union. Its cost is no greater: the ancestor cost is the descendant cost plus costs of deleted rule occurrences and side subtrees, all nonnegative. The complete tree's support and cost therefore weakly decrease. Its number of nodes strictly decreases, including when the deleted loop has cost zero. Repeat until no branch has a repeated judgement. A branch then has at most n nodes. This terminates by decreasing finite node count, not by an assumption that costs strictly decrease.

*Proof of 2.* The set Hq of proof trees of q of height at most n is finite: R is finite, each rule has finite arity, and the height bound is fixed. Part 1 shows Hq dominates every proof. Normalize the finite pair set of Hq; every member of Hq is dominated by a retained member, so every unrestricted finite proof is too. A retained member cannot be strictly dominated by an unrestricted proof, since part 1 and finite normalization would then provide a strictly dominating member of Hq. Thus this is exactly the unrestricted frontier. Any globally undominated pair must equal the pair of its dominating bounded representative. At most one price survives for any fixed support; there are 2^m supports.

### The constructive recurrence

Let A0(q) be empty for every q. Given Ah, form Ah+1(q) by normalizing the union of Ah(q) and all pairs

    (B(r) union S1 union ... union Sk, w(r) + c1 + ... + ck)

for rules r with head q and choices (Si,ci) from Ah(qi) for every premise-list position. The empty product for a nullary rule yields its own pair (B(r),w(r)). Each candidate stores r and the child witnesses used to construct it. Old witnesses remain immutable when copied into later rounds.

Inductively Ah(q) is the normalized pair set of trees of height at most h. At a rule, replacing any child pair by a dominating pair weakly decreases the union of supports and the sum of prices. Hence discarded child pairs cannot contribute an undominated parent pair. Conversely every generated candidate has an actual rule tree of the promised height. This proves the induction and, with part 2, proves clause 3. If a round changes no pair set, the same recurrence generates no new pairs thereafter; witness identifiers need not be the same for this equality test. ∎

This is monotone saturation in the information order “every old pair is dominated by a new pair,” or equivalently inclusion of the upward sets generated by the antichains. The displayed antichain sets themselves need not grow by ordinary set inclusion: a better pair may replace an old one.

The bound is sharp as a height bound: a chain of n distinct judgements ending at one leaf requires n rule nodes. The theorem says nothing about polynomial complexity. With maximum arity a, even a height-n tree can have 1+a+...+a^(n−1) nodes, and each judgement may have exponentially many nondominated supports.

### What is, and is not, preserved by pruning

An arbitrary tree's *exact* support can shrink. For example a single judgement q has a leaf requiring a and a self-rule additionally requiring b. A two-node derivation has support {a,b}; its one-node dominator has support {a}. The larger support is irrelevant to the Pareto objective, but it is still a genuine possible proof support. The theorem does not claim to enumerate every proof or every exact-support derivation within height n.

If exact support is required for another purpose, repeatedly delete only ancestor–descendant pairs having both the same judgement and the same subtree support. This preserves exact support and weakly reduces cost; node count still decreases when a deleted loop costs zero. Along a branch subtree supports are nested and strictly decrease at most m times; each constant-support block has at most n different judgements after pruning. The finite family bounded by height n(m+1) therefore dominates every proof having that exact support, so it attains the minimum whenever that support occurs. This observation is not needed by the frontier compiler and does not enumerate all support-bearing trees or preserve all derivation structure.

## 4. Shared-DAG compilation and the intermediate-summary obstruction

**Theorem 2.** Under the DAG contract every finite proof DAG is dominated by a proof DAG with at most one node for each fully scoped judgement. Consequently its exact terminal frontier is computable by finite enumeration of one admitted rule or “absent” for each judgement, rejecting missing premises and cycles and retaining the root-reachable subgraph.

*Proof.* Fix a topological order of the original DAG with every premise before its parent. For each judgement appearing in the graph select its earliest node in that order. At its selected node retain the original rule, but redirect each premise reference to the selected earliest node of that premise's judgement. If the original premise node had index i and the selected parent has index j, the selected premise index is at most i, and i<j. Thus redirected edges still point strictly earlier. The resulting graph is acyclic, and every premise has exactly its required scoped judgement. Take the selected node of the original root judgement as root and discard unreachable selected nodes.

Every retained rule node is an original selected occurrence. Its local evidence and cost are unchanged. The retained nodes form a subset of original nodes, so the support is a subset and the sum of nonnegative node costs is no greater. There is at most one node per judgement. As before, normalizing the finite family of all such reduced graphs yields exactly the frontier of all finite DAGs. Enumeration creates a genuine certificate witness for every retained pair. ∎

The enumeration need not assume a topological order in advance. For each partial choice of a rule for each judgement, follow its premise references from the target: reject a referenced absent judgement or a recursion-stack cycle. In the surviving graph count every reachable chosen rule once. Nullary and evidence-introduction rules are included. An unsupported self-loop is rejected, not counted as a zero-cost proof. There are at most the product over q of (1+number of rules headed by q) candidate rule selections. This is a finiteness bound, not a practical scaling claim.

### A terminal frontier is sufficient; an intermediate one can lose sharing

Take J={p,a,b,t}, E={e}, and these rules, with no evidence requirements other than the two stated:

- e gives p, cost 5;
- p gives a, cost 0;
- e gives a directly, cost 4;
- p gives b, cost 0;
- a and b give t, cost 0.

Every proof has support {e}. The standalone a frontier keeps the direct cost-4 proof and removes the cost-5 route through p. Tree checking gives t cost 4+5=9; using p twice would cost 10. DAG checking instead shares the single p node between a and b and costs 5. If one applies standalone support/cost pruning to intermediate DAG proofs before combining them, the globally optimal shared witness may already have been discarded, leaving cost 9.

Thus the tree recurrence is not a DAG optimization algorithm, and local DAG dominance is not a congruence for contexts that share internal checked nodes. A compositional DAG method needs richer sharing-footprint information, or the finite whole-graph enumeration just proved. No scheduling or incremental cache algorithm is asserted here. Once a complete terminal DAG catalogue/frontier is compiled, the inherited final support/cost theorem applies exactly as before.

## 5. Interface to warranted completion

Choose the appropriate cost contract, compile its exact frontier for each declared terminal verdict, and retain its witnesses. For a current authenticated inventory K, residualize each pair to (S minus K,c) and normalize. The previous canonical theorem then gives the same future-cost function as quantifying over **all finite derivations of the admitted ground grammar**:

    F(K,q,U) = minimum checking cost of a finite q-proof
               whose evidence support is contained in K union U.

The finite compiler proves that each finite minimum is attained and supplies a witness. Its empty result means no finite proof in this particular grammar, not falsehood of the proposition and not absence of a proof in an unrestricted logic.

For the earlier finite persistent-test model, its full-transcript completion criterion and Bellman recurrence can now use these compiled witnesses without an independently supplied proof catalogue. Costs still separate offline compilation, acquisition/authentication, and final checking. Soundness still requires the rule licences and evidence-source commitments. The compiler cannot establish those application premises by optimizing them.

## 6. The precise boundary

### Nonnegative real costs do not by themselves break the theorem

The proofs use addition, comparison, and nonnegativity, not the well-ordering of natural numbers. The same finite-height and finite-DAG arguments hold for finite nonnegative rational or real rule prices. A finite set of local real weights cannot create an unattained improving sequence in this model: every proof is dominated by one from the derived finite family.

Effective exact compilation additionally needs effective addition and comparison of the represented prices. Naturals and rationals provide this directly. Arbitrary real-number descriptions need not. This computational qualification is distinct from existence of the finite mathematical frontier.

### What actually fails outside the assumptions

- Allow a negative-price self-rule q→q of cost −1 and a nullary q-rule of cost 0. Finite proofs have costs 0,−1,−2,... with no minimum. The nonnegative pruning argument fails.
- Allow infinitely many nullary rules for one q with the same support and prices 1,1/2,1/3,... . All prices are positive, but no least proof cost is attained, and no finite subcatalogue dominates all proofs. Finiteness of grounded rule instances is indispensable for the stated general result.
- A finite list of schemata may still generate infinitely many formulas, terms, contexts, or rule instances. For example a base P(0) and schema P(x)→P(s(x)) already generate infinitely many scoped judgements. The finite grammar theorem cannot be applied just because the printed rule list is short. No unrestricted-logic decidability theorem or impossibility theorem for the actual HasE problem follows from these examples.
- A proof-shape-dependent total charge, such as 1/(1+number of nodes), is nonnegative but violates the fixed additive local-price contract. A finite looping syntax can then have decreasing unattained costs. The theorem does not cover arbitrary advertised “checking costs.”
- Consumable evidence, freshness/independence conditions not retained in the judgements, order-sensitive authorization, and proof-dependent side conditions can make subtree substitution invalid. They require another justified finite state space if a finite compiler is desired.

### HasE remains outside this instantiated result

The inherited literal-HasE report was read directly. It identifies the unchanged target HasE [] c3 (W q), and explains why the constant raw proof term does not justify introduction inversion: dependent J followed by conversion can erase an evidence subterm while retaining the target type it justified. Its reported outstanding burden is a type-preserving transformation of complete derivations, including impredicative instantiation and typed extensionality.

The retained ScalarFusionCore and LiteralScalarFusion sources were also inspected. Their generic context, type, term and HasE parameters, together with actual uses of HasE.j and conversion, do not supply a finite set of all target-relevant fully scoped judgements or ground rules. The present proof cannot invent that finite interface by identifying raw terms or by deleting their types. It neither proves nor refutes the original HasE target, changes its status, nor supplies the missing full-model or normalization argument.

Similarly, the retained nineteen-line System R derivation is an explicit fixed proof object. Its finite list of instances can be represented by a finite grammar, but that would not prove that all useful System R proofs lie in that grammar. Nor does checking its logical conclusion establish a subject's actual knowing or use of its premises.

## 7. Ancestry and verification status

The construction belongs to established positive provenance, finite Datalog/deduction fixed points, and min-plus/weighted parsing methods. Green, Karvounarakis and Tannen develop provenance annotations, derivation-tree semantics for recursive Datalog, and fixed-point methods. Goodman discusses semiring deduction and explicitly observes that non-improving looping Viterbi derivations can be omitted. The present argument combines support inclusion with additive checking prices and spells out the finite scoped-rule interface and the tree/DAG distinction. No field-wide originality claim is made. [Provenance Semirings, §§3–5](https://www.cs.ucdavis.edu/~green/papers/pods07.pdf); [Semiring Parsing, §§2–3](https://aclanthology.org/J99-4004.pdf).

The general proofs above are mathematical prose. Executable checks, witness validation, source bindings and independent review are recorded alongside this report. They are finite checks of the implementation and sharp controls, not a substitute for the general proofs or a new Lean kernel certification.

The complete `verify.py` suite passes 12 tests. It compares the two-round tree compiler against an independent unpruned four-round pair oracle for all 2,517 grammars formed from at most four rules of a declared sixteen-rule universe. It validates 10,520 compiled tree/DAG witnesses, checks the extra tree round is a fixed point, and checks 250 seeded larger root-reachable DAGs and their tree unfoldings. Direct controls cover unsupported cycles, zero-cost loops, sharp chain depth, support/cost tradeoffs, exact rational prices, exact-support shrinkage, and repeated-premise charging. `CHECK_RESULTS.json` binds the tested implementation and report. The independent review adds a separately implemented exhaustive 41,488-case DAG representative check.

The executable grammar accepts exact natural/rational costs and symbolic scoped labels. Its local witness traversal does not authenticate evidence or prove rule soundness; the compiler emits only its admitted input rule records. The general-real-price extension is proved above, not implemented by floating-point comparison. All inherited source files remain unchanged.
