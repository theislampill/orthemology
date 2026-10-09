# Dependency audit of plural self explanation

## Result

The proposed shortcut is valid. Given a nonempty total plurality of actual facts, unrestricted plural PSR and the source's **complete** transitivity clause yield an actual fact that fully explains both the total plurality and itself. Neither No Extended Circles, the partial-transitivity clause, nor output distributivity is needed.

This establishes full self-explanation in the relation the source denotes by “explains.” The source defines self-explanation that way and its later usage supports identifying this with “wholly self-explanatory.” It supplies no separate definition making that phrase mean absence of distinct explainers, independence from every other fact, or self-explanation of every part. Those stronger conclusions are not proved.

The proposed countable-chain control is a genuine model of unrestricted plural PSR and No Extended Circles, with partial explanation defined exactly by source-side parthood, when **both** transitivity clauses and output distributivity are omitted. It has no self-explanatory fact. A strengthened atomless-mereology version also supports standard supplementation and unrestricted nonempty fusion. Their status is that of abstract relational counterinterpretations, not metaphysical realizations of facts or explanation.

Source: Robert C. Koons and Alexander R. Pruss, *Skepticism and the principle of sufficient reason*, §2, published online 2020, journal issue 2021. [Publisher](https://doi.org/10.1007/s11098-020-01482-3). Line references below refer to the supplied continuous text witness, not to journal line numbers.

## Definitions fixed before the proof

Write E(x,S) for an actual fact x completely explaining the nonempty plurality S. Write {q} for the admitted singleton plurality of q.

- Unrestricted PSR at L53–54 supplies an **actual** fact explaining every plurality of actual facts.
- Self-explanatory at L61–63 means E(x,{x}). A partially self-explanatory fact x is a **proper part of a fact** that explains x. This is not the same as explaining a part of x.
- Partial explanation at L88–92 uses the source-side sense: PE(x,S) holds exactly when there is a z such that x is part of z and E(z,S). “Part” includes improper parthood here; if proper parthood is taken as primitive, add identity for this inclusive relation.
- No Extended Circles at L93–94 says: if PE(x,S), y belongs to S, and y is neither x nor a part of x, then not PE(y,{x}). Mere inequality does not discharge its nonparthood qualification.
- Complete transitivity at L95–96 says: E(x,S), y in S, and E(y,T) imply E(x,T). The separate clause at L96–97 substitutes PE for E in the first premise and conclusion.
- Output distributivity, displayed only at L132–133, takes an explanation of a plurality to an explanation of any member or part of a member. It is a separate principle.

The relation E is unary in its explaining fact and plural in its explanandum. No fusion of a plurality into one fact is assumed.

## Exact totality and singleton hypotheses

The short proof requires:

1. At least one actual fact exists.
2. The nonempty plurality F of **all** actual facts is admitted. The source explicitly invokes such totality and plural comprehension at L55–58.
3. F has an actual complete explainer Q. This is the first PSR instance.
4. The singleton {Q} is an admitted plurality and has an actual complete explainer R. This is the second PSR instance. The source expressly admits singleton pluralities at L154–156.
5. Complete transitivity applies to F and {Q} in the displayed member-mediated sense.

The source's general comprehension assumption matters here. Its footnote at L64–67 says that the later application needs only comprehension for qualifying wholly particular natural facts. That narrower principle alone does not provide the all-actual-facts F needed by this shortcut. Nor does plural PSR over nonempty pluralities alone establish that any facts exist: on an empty domain, its existential consequences would fail.

There is no assumption that F is finite, that F is itself a fact, that explanations distribute to members, or that some explanation is unique. Since PSR supplies actual explainers, R belongs to F. No separate global axiom saying that every conceivable explanation is actual is needed for this step.

## Short proof and its formal check

Choose Q with E(Q,F). Choose R with E(R,{Q}). Since R is actual, R belongs to F. Complete transitivity applied to x=Q, S=F, y=R and T={Q} gives E(Q,{Q}). Therefore Q fully explains itself and still explains F.

The kernel-checked theorem `total_explainer_self` records exactly the local ingredients: E(Q,F), totality of F, existence of an explainer of {Q}, and complete transitivity. It does not assume global PSR at all. The corollary `unrestricted_has_self_explaining_total_explainer` obtains those ingredients from nonemptiness and two uses of unrestricted PSR.

`DependencyAudit.lean` was checked with the already installed Lean 4.19.0 and `import Std`, without Mathlib or new dependencies. The two positive theorems have no additional Lean axioms in the printed dependency report. Formal checking certifies this inference under its explicit representation; it does not certify the interpretation or truth of its premises.

The formal corollary represents pluralities by predicates on a type of actual facts and permits all nonempty predicates. This is stronger than the comprehension footprint needed for the short proof; the local theorem isolates that footprint so the encoding is not mistaken for an argument for unrestricted comprehension. An abstract Lean type called Fact does not establish that a metaphysically legitimate universe of all actual truths exists. The shortcut does not claim to weaken the source's comprehension commitments.

## Does this prove wholly self explanatory

The safest exact verdict is E(Q,{Q}), **complete** self-explanation rather than merely PE(Q,{Q}). There is positive textual reason to associate this with the theorem's “wholly self-explanatory” phrase:

- L61 explicitly defines self-explanatory by explaining itself.
- L138–139 treats wholly explaining oneself as ruling out membership in the class of not-wholly-self-explanatory facts.
- L151–156 moves between a self-explaining member and a wholly self-explanatory fact's singleton instance.

No separate formal predicate with a stronger condition is introduced in the inspected section. Thus the shortcut supports the intended full-versus-partial contrast, while leaving the terminology's underspecification visible. It does not show that Q has no distinct full or partial explainer. It also does not show uniqueness, necessity, supernatural status, maximal explanatory independence, or that each proper part explains itself. Adding any such reading would require a further definition and proof.

## Relation to the printed proof of Theorem 1

The source labels its theorems conditional on previously displayed principles (L108–110). Its Theorem 1 therefore must not be read as a claim from unrestricted PSR alone.

The printed proof considers the plurality of all not-wholly-self-explanatory facts, PP. Its step from Q explaining PP and R belonging to PP to Q fully explaining R (L116–117) uses a member-projection inference of the sort later displayed as distributivity. Its appeal to No Extended Circles also needs the nonparthood condition, not merely R being distinct from Q. These are dependencies or missing justifications in that particular short presentation; they are not objections to the existence conclusion under the already displayed complete transitivity, because the total-plurality proof above establishes it directly.

This audit does not claim priority for a new philosophical theorem. It removes unnecessary named assumptions from a source-relative derivation and makes the remaining ones explicit. With output distributivity admitted, an even shorter different derivation is available: E(Q,F) and Q in F immediately imply E(Q,{Q}). Consequently, transitivity is not asserted to be logically necessary under every possible alternative package.

## Countable chain control without transitivity

Take distinct actual facts q_0, q_1, q_2, and so on, indexed by all natural numbers. Admit **every nonempty subset** of this domain as a plurality, including infinite subsets and F itself. Thus this interpretation supports full extensional plural comprehension and consequently the narrower comprehension needed by the source's footnote.

Define parthood by:

- q_m is part of q_n exactly when m ≥ n.
- q_m is a proper part of q_n exactly when m > n.

Define complete explanation by precisely these cases:

- E(q_(n+1), {q_n}) holds for every n; these are the only explanations of singleton pluralities.
- E(q_0,S) holds for every plurality S with at least two distinct members; these are the only explanations of such pluralities.

Partial explanation is not freely stipulated: PE(q_m,S) means that q_m is part of some complete explainer of S.

### All relevant checks

1. **Parthood.** The relation is reflexive, transitive and antisymmetric; q_(n+1) is a proper part of q_n.
2. **Unrestricted PSR.** Every nonempty plurality either is {q_n}, explained by q_(n+1), or contains two distinct members, explained by q_0. This covers all infinite pluralities as well as finite ones. There is no omitted limiting or unbounded plurality.
3. **Exact partial-explanation closure.** PE(q_m,{q_n}) holds exactly when m ≥ n+1. For every plurality with two distinct members, PE(q_m,S) holds for every m, because every q_m is part of q_0. Every full explanation is partial via reflexive parthood, and parts of partial explainers remain partial explainers by transitivity of parthood.
4. **No Extended Circles.** If target q_k is neither equal to nor part of q_m, then k < m. A partial explanation back from q_k to {q_m} would require k ≥ m+1. Those inequalities are inconsistent. This proves the displayed prohibition for every plurality, without suppressing any partial explanations.
5. **No self-explanation.** E(q_n,{q_n}) would require n=n+1. It never holds. Indeed, no fact is partially self-explanatory in the source's defined sense either: q_n cannot be a proper part of its unique full explainer q_(n+1).
6. **Failure of complete transitivity.** q_0 explains {q_0,q_1}; its member q_1 explains {q_0}; but q_0 does not explain {q_0}.
7. **Failure of partial transitivity.** The same example starts with PE(q_0,{q_0,q_1}) but has no PE(q_0,{q_0}).
8. **Failure of output projection.** q_0 explains {q_0,q_1} but not its singleton member {q_0}. The source's stronger member-or-part distributivity consequently fails as well.

These checks, including quantification over arbitrary predicate pluralities rather than a finite census, are kernel-checked in `DependencyAudit.lean`. Classical reasoning is used for the singleton-versus-multiple partition; the printed axiom dependencies contain no admitted theorem or `sorryAx`.

### What the control discriminates

Unrestricted plural PSR plus the displayed No Extended Circles principle and source-defined partial explanation do **not** force full self-explanation. A collective explanation need not project to the singleton of an included member unless a bridge such as complete transitivity with further PSR instances, or output distributivity, is supplied.

This is independence from the package with both transitivity clauses omitted, not independence from complete transitivity while retaining partial transitivity. It is not a countermodel to the source's full stated package.

The parthood interpretation supplies only the partial-order structure just verified. It does not satisfy standard weak supplementation: all its facts overlap, so a proper part has no disjoint remainder. The source does not display a supplementation axiom in the inspected passage, but if that or a stronger theory of fact mereology is intended, this control does not establish independence relative to it. Nor does this interpretation realize the source's relevance-entailment account of a being's inclusion in a fact (L144–147), natural/supernatural ontology, or any actual explanatory practice. Those semantic questions cannot be answered by naming the indices “facts.”

## Strengthened control with supplementation and fusion

The chain's weak mereology is not needed for the independence result. The same explanatory pattern works on any atomless bounded mereological partial order: a domain with a top element T and a nonzero proper part below every element. An atomless complete Boolean algebra with its zero element omitted is one such domain.

For all nonempty pluralities S, define:

- E(z,{x}) exactly when z is a nonzero proper part of x.
- E(T,S) for every S containing at least two distinct members; no other complete explanations of multiple-member pluralities hold.
- PE(y,S) exactly when y is part of some z with E(z,S), as the source requires.

Atomlessness supplies each singleton's explainer; T supplies every multiple-member plurality's explainer. If PE(y,{x}), then y is part of z and z is a proper part of x, so y is a proper part of x by transitivity and antisymmetry. Conversely, if y is a proper part of x, take z=y. Hence PE(y,{x}) holds **exactly** when y is a proper part of x. For multiple-member S, every element partially explains S through T.

No Extended Circles now follows directly: its premise that y is not a part of x contradicts the condition for PE(y,{x}). No fact fully explains itself. Choose a proper part a of T. Then T explains {T,a} and a explains {T}, but T does not explain {T}. This refutes complete transitivity and output projection. Since PE(T,{T}) also fails, it refutes the partial-transitivity clause as well.

The generic order-level argument is kernel-checked in `SupplementedControl.lean`, with no algebra or topology library. Its `Frame` explicitly assumes a reflexive, transitive, antisymmetric parthood relation, top, and a proper subelement below every element. It verifies unrestricted PSR, the exact singleton partial-explanation equivalence, source-side closure, No Extended Circles, absence of self-explanation, and failures of both transitivity clauses and member projection. Supplementation and fusion are not axioms needed by those checks. A concrete realization below supplies them; that realization is proved in ordinary mathematics, not claimed to have been formalized in Lean.

### Concrete regular open realization

Let the fact-domain be all nonempty regular open subsets of the real line, with inclusion as parthood and the whole real line as T. An open set U is regular open when U equals the interior of its closure. Every nonempty open interval is regular open.

- **Atomlessness:** every nonempty open U contains two disjoint nonempty open intervals. Either interval is a nonempty proper regular-open part of U.
- **Strong supplementation:** if U is not included in regular open V, then the open set U minus the closure of V is nonempty. Otherwise U, being open, would lie in the interior of the closure of V, which is V. Choose a nonempty open interval inside that difference. It is a part of U disjoint from V.
- **Arbitrary nonempty fusion:** for any nonempty family of these sets, put A equal to their union and J equal to the interior of the closure of A. For every open A, A is included in J, J is included in the closure of A, and the closures of A and J coincide. Consequently J is regular open and nonempty. It contains every family member, and any regular open upper bound V contains J because taking interior of closure preserves inclusion and fixes V. Moreover, any open region overlapping J intersects A, since A is dense in J; thus it overlaps some family member. Conversely, an overlap with a member is an overlap with J. This is the usual fusion overlap condition, not merely a name for a supremum.

Together with extensional inclusion, this gives the standard supplementation and nonempty-fusion behavior absent from the chain. Every nonempty subset of the domain is admitted as a plurality, so comprehension is not restricted to finite, bounded, or specially selected cases. No finite model census is involved.

The associated regular-open Boolean complement is a **mereological** complement, not propositional negation. Two disjoint regions can both exist and the corresponding abstract elements can both be actual facts in the interpretation. Treating every nonzero element as actual therefore does not assert both a proposition and its logical negation. The model does not supply a truth-functional algebra of propositions, the source's relevance-entailment semantics, an explanation of why proper parts would explain their wholes, or a natural-world realization.

The stronger result is robustness of this relational independence control to standard mereological axioms. It remains a control after dropping the entire displayed transitivity bundle and output distributivity, not a counterexample preserving them or a new metaphysical counterexample.

## Separation from the basic natural facts argument

The later argument endorses a **restricted noncircular PSR for basic natural facts** at L162–170 and gives it an epistemological defense beginning in §3. It does not depend on the unrestricted theorem as a premise.

Section 2 also discusses a conditional route from unrestricted PSR to a restricted principle for facts that are not wholly self-explanatory, using additional distributivity and classification premises (L129–158). That route should not be conflated with the later restricted principle's independent endorsement and defense.

For the restricted route, applying its own PSR to a nonempty total plurality of basic natural facts yields an explainer outside that class. Turning this into a supernatural fact invokes the source's definitions and its additional particularity assumption (L171–173). This audit establishes neither that transport nor the epistemological warrant for the restricted PSR. The all-actual-facts totality theorem cannot supply them for free.

## Credit and boundary

The earned positive result is a correct, simpler conditional proof of a full self-explanatory total explainer, together with substantive independence controls for the deliberately weaker relational package, including robustness to standard supplementation and nonempty fusion. No actual-world explanatory warrant, Necessary Being claim, new prior-art theorem, protected repository modification, integration, or programme closure follows from this work.
