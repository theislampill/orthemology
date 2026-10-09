# Independent review: plural explanation and the particular-explanans bridge

## Verdict

The four formal files and their accompanying mathematical arguments withstand this bounded review. I found no invalid inference in the short total-explainer proof, no missed relational obligation in either weakened unrestricted control or the three-fact restricted control, and no mismatch between the positive bridge proofs and their explicit local hypotheses.

The retained result should remain **displayed-axiom independence in a reduced relational/classificatory signature**. The finite control is not a complete interpretation of the source's ontology, relevant-entailment definition of supernatural facts, or intended standard of adequate explanation. In particular, its assigned edge `Full(c,{b})` is not evidence that a mixed fact containing b genuinely explains b. The supplied reports already make this essential limitation explicit. Do not drop it in a shorter presentation.

Two qualifications deserve emphasis before polish:

1. “Preserves the full displayed classification package” is safe only if it means the audited predicate-level abstraction. `Supernatural := False` does not itself formalize the source's biconditional in terms of concrete beings and relevant entailment. The control verifies the basic-natural definition and the no-universal-part classification; the rest remains an interpretation boundary.
2. The positive bridge proofs need a **wholly particular constituent**. The source says “a particular fact” at L171–173, which is less explicit. Granting the stronger reading strengthens the independence control, so this ambiguity does not defeat that negative result. The repairs and unrestricted positive route should continue to state the stronger reading as an assumption. Also, the proposed “exact repairs” are explicit sufficient repairs; no theorem here establishes their necessity, uniqueness, or weakestness.

Neither qualification is a discovered failure of the existing Lean proofs. No source commitment inspected supplies an unambiguous additional relational axiom that rules out the finite control while retaining only the advertised restricted PSR. The intended meaning of explanation may rule out its assigned edge, but establishing that is additional semantic work.

## Scope and evidence

The reviewed versions are bound by SHA-256 in `INPUTS.json`. They comprise the supplied continuous source witness, both `RESULT.md` reports, all four Lean files, and the root replay receipt. Every Lean input hash agrees with the corresponding hash in that receipt.

I read full §2 (source labels L49–175), its abstract/introduction framing, the relevant restricted-PSR and causal framing in §§3–4, and the later summary/conclusion. I inspected each formal definition and proof and checked the regular-open realization directly as written mathematics. No Lean replay was performed or credited as new science. The root's exact-input Lean 4.19 replay remains the supplied kernel-check evidence. No new literature, framework, protected-source change, integration, or closure was undertaken.

Line references below are the witness's embedded L-labels, not physical file line numbers or journal line numbers.

## 1. Total explanation to complete self-explanation

The short inference preserves the source's member-mediated complete transitivity exactly:

- Let F be an admitted plurality containing every actual fact.
- Let Q completely explain F.
- Let an actual R completely explain the admitted singleton {Q}.
- Since R belongs to F, complete transitivity gives that Q completely explains {Q}.

There is no reversal of explanatory direction: the composition is Q → F, membership of R in F, and R → {Q}. This is precisely the first clause at L95–97. Neither explanation of each member of F nor an inference from collective explanation to individual explanation is silently inserted.

`total_explainer_self` takes just these local hypotheses. The unrestricted corollary explicitly assumes a nonempty fact type and uses PSR twice, once for the total predicate and once for Q's singleton. The type consists of actual facts, so R's actuality and totality membership are preserved. F need not itself be a fact. No conjunction or fusion construction is assumed. Once Q and totality are supplied, F's nonemptiness follows; the global corollary separately ensures that its first PSR application is nonvacuous.

The general predicate representation supplies more comprehension than this local proof needs. The report correctly distinguishes it from the source footnote's weaker later commitment to comprehending qualifying wholly particular natural facts (L64–67). That restricted comprehension alone cannot supply all-facts F. Singletons are expressly used by the source at L154–156.

The conclusion is exactly complete self-explanation, E(Q,{Q}), together with E(Q,F). The source defines self-explanatory at L61 and shifts between “self” and “wholly self” at L119 and L148–156. Thus the report's carefully qualified full-versus-partial reading is reasonable. No definition or theorem here yields absence of distinct explainers, necessity, uniqueness, self-explanation of each proper part, or exhaustive explanatory independence.

The report also correctly avoids claiming complete transitivity is indispensable under every package: member projection would itself yield E(Q,{Q}) immediately. The criticisms of the printed proof concern its particular short presentation and do not invalidate the corrected conclusion under the named local premises.

## 2. The weakened unrestricted controls

### Countable chain

The actual domain is all natural indices, the plurality domain admits every nonempty subset, inclusive parthood is reverse numerical order, and the only singleton explainer of n is n+1. Every plurality with two distinct members is explained by 0.

The singleton/multiple partition covers arbitrary infinite subsets and the total domain. It is not a finite enumeration, bounded-subset argument, or omitted-limit construction. Source-side partial explanation is derived, not independently assigned:

- PE(m,{n}) iff m ≥ n+1.
- Every m partially explains every multiple-member plurality through the full explainer 0.

No Extended Circles is satisfied in its displayed, qualified form. If target k is not part of partial explainer m, then k < m; a reverse PE(k,{m}) would require k ≥ m+1. Distinctness alone is not substituted for the crucial nonparthood premise.

No n fully explains itself, and none is a proper part of its singleton's full explainer. The exhibited pair {0,1} separately refutes complete transitivity, partial transitivity, and member projection. Thus the stronger member-or-part distributivity also fails. The control preserves unrestricted plural PSR, source-side partial explanation and its downward closure, No Extended Circles, and partial-order mereology **after dropping both transitivity clauses and distributivity**. It cannot be advertised as retaining partial transitivity, or as a countermodel to the source's whole package.

The report correctly identifies the lack of supplementation: all elements overlap. This does not affect the weaker displayed-axiom result but precludes claiming this chain realizes standard supplemented mereology.

### Atomless topped order

`SupplementedControl.Frame` assumes a partial order, a top, and a strict subelement of every element. It does not assume supplementation or fusion. The argument proves, under those order hypotheses, that singleton full and partial explanation are each equivalent to strict parthood. Atomlessness supplies singleton explainers; the top supplies all multiple-member explainers.

This equivalence gives No Extended Circles immediately: its forbidden reverse partial explanation would make the target a part of the partial explainer, contrary to the displayed antecedent. A strict part a of the top T then produces the advertised failures using {T,a}. All three failures are separate, explicit checks. There is no retained transitivity hidden in the construction.

For precision, “topped partial order” is a less ambiguous description than “bounded partial order”: the frame has no bottom and cannot have a bottom in its nonzero domain while every element has a strict subelement. The report's explicit definition already prevents a substantive ambiguity.

### Regular-open realization, checked as ordinary mathematics

The nonempty regular open subsets of the real line, ordered by inclusion, do instantiate that frame and support the extra mereological claims:

- Every nonempty open U contains two disjoint nonempty intervals, so it has a nonempty proper regular-open subpart.
- If U is not included in regular open V, U cannot be included in closure(V). Otherwise openness gives U ⊆ interior(closure(V)) = V. Hence U minus closure(V) is a nonempty open set and contains a nonempty interval disjoint from V. This proves strong supplementation, with overlap understood as sharing a nonempty regular-open subpart.
- For a nonempty family, its union A is nonempty open. Set J = interior(closure(A)). Then A ⊆ J ⊆ closure(A), so closure(J) = closure(A), and J is regular open. Any regular-open upper bound of A contains J.
- The overlap characterization also holds, not merely the least-upper-bound property. If a nonempty regular open W overlaps J, the nonempty open set W ∩ J meets dense A and thus meets some family member. The intersection contains a nonempty interval, giving overlap in the mereological sense. The converse follows from each member's inclusion in J.

No supplementation/fusion defect was found. This concrete realization is **not kernel-verified** by the supplied Lean file. Its Boolean/mereological complement is not propositional negation, and the construction is not a semantics of all actual truths or genuine explanation.

## 3. The restricted three-fact control

### Exact finite representation

The eight masks represent every subset of {b,u,c}, including the empty mask; the restricted PSR excludes exactly that empty mask. Singleton membership and the equivalence between nonzero masks and nonempty membership are independently checked. All three facts are actual within the interpretation.

Inclusive parthood has b and u as disjoint atoms and c as their fusion/top. Proper parthood is inclusive parthood plus inequality. This agrees with the source's explicit use of “proper part” for partial self-explanation at L61–63. Using inclusive “part” in the L88–92 definition is a reasonable convention, made explicit in the reports and formal files; it is not a covert switch between source-side and target-side partial explanation.

The only basic fact is b. The universal fact u is a part of c; accordingly c contains a universal generalization and is not wholly particular. The theorem `particular_exactly_no_universal_part` checks the source's L166–167 classification at the intended predicate level. Mixed c is neither basic nor supernatural. The report does not incorrectly infer supernatural from non-basic.

### Explanatory obligations

With only Full(c,{b}), and also in the optional version adding Full(u,{u}), every listed relational check is satisfied:

- Restricted PSR is nonvacuous: {b} is the only nonempty all-basic plurality, and c is neither b nor a part of b.
- The particular-constituent requirement has the witness b ≤ c. The finite theorem actually grants the stronger condition whenever an explained plurality has even one particular member; it does not exploit a weakened all-targets-particular antecedent.
- There is no basic complete self-explainer. The stronger source formulation that every explainer of a basic plurality is distinct from its members is also satisfied here.
- b is a **proper** part of a fact completely explaining b. Thus the exact source-defined partially self-explanatory pattern is present, rather than only a mislabelled explanatory edge.
- Complete and partial transitivity hold because the intermediate b completely explains nothing. The optional u self-edge composes only with itself.
- Distributivity holds for every member and part of an explained target. The targets b and, optionally, u are atoms; required projected edges already exist.
- For No Extended Circles on target b, partial explainer b is exempt by identity and c is exempt because b ≤ c. For partial explainer u, the prohibition genuinely applies, and PE(b,{u}) is absent, even with u's optional self-edge. No forbidden cycle is hidden by forgetting a partial explainer.
- Strong supplementation, nonempty fusion, and parthood-minimality of full explainers hold. For example, neither proper part b nor u of c fully explains b, including in the optional version.

Accordingly there is no missing finite relational obligation that defeats the control. Its failure of unrestricted PSR, e.g. for {c}, is explicit and essential.

### What the source may intend beyond those checks

The finite structure also respects the source's informal assertion that basic facts are atomic (L157), because b has no proper part. That cannot defeat this example. Nor does the text's entity-inclusion account at L144–147 itself forbid a mixed conjunction containing a basic fact: it is an account of a being's relevant inclusion in a fact, not a displayed ban on reverse fact-parthood in explanations.

The genuine remaining issue is explanatory adequacy. The “removal of mystery” discussion at L75–87 and the later sustained causal framing are meaningful semantic motivations, not decorations. A reader may reasonably deny that c containing b genuinely explains b. The control does not answer that objection by merely assigning Full(c,{b}), and the report properly says so. Conversely, those passages do not mechanically add the missing reverse-parthood exclusion to the displayed axioms. The supported conclusion is that an additional explanatory constraint must be specified if that semantic objection is to carry the formal inference.

The control does not supply a concrete-beings domain, intrinsic measures, a relevance logic, quantifier semantics for universal facts, or a fact ontology containing all actual truths. It therefore should not be described as a full source interpretation or a metaphysically possible wholly natural world. Interpreting Supernatural as false is compatible with a predicate-level no-supernatural interpretation; it is not by itself verification of the source's complete definitional semantics.

Finally, the source's footnote that theorems inherit earlier principles (L108–110) creates a genuine reading ambiguity. But the abstract, §2 summary at L162–175, restricted formulations at L304–305 and L327–328, and conclusion at L820–823 support the reports' decision to audit the advertised restricted route without silently restoring unrestricted PSR. If unrestricted totality explanation is restored, the finite control is inapplicable and the separately proved stronger route governs.

## 4. Exact positive repairs and unrestricted route

Repair A uses a selected total-basic explainer y, a wholly particular part p of y, member projection, source externality's inequality y ≠ p, and the added ban on basic proper-part self-explanation. If p is not supernatural, it is basic, so y explains p; p ≤ y and p ≠ y then contradict the added ban. This matches `bridge_with_no_basic_proper_partial_self` exactly. The original externality's additional not-y≤p clause is not needed for this proof. Neither transitivity nor No Extended Circles is used.

Repair B uses only a wholly particular part p of y and added reverse externality forbidding every basic p ≤ y. If p were not supernatural it would be basic, contradicting that condition. `bridge_with_reverse_externality` is appropriately local: it does not claim to obtain the selected explainer or particular part from no premises. Distributivity may be needed upstream to obtain that part via an explained particular singleton, but not after it is supplied.

The reports correctly explain upstream nonemptiness: an actual wholly particular fact either already is supernatural or supplies a basic target. The total basic plurality must be admitted to invoke restricted PSR on it. No actual particular target is conjured by a vacuous restricted universal statement.

The stronger unrestricted proof is also sound. Given an all-actual-facts total explainer Q, member projection and No Extended Circles force every part p of Q to equal Q: otherwise antisymmetry gives not Q ≤ p, while PE(p,F), Q ∈ F, and PE(Q,{p}) form the expressly forbidden pattern. Reflexive inclusive parthood supplies the latter partial explanation from Q's full explanation of p. A wholly particular constituent therefore makes Q wholly particular; projection makes Q fully self-explanatory; the ban on basic full self-explanation makes Q supernatural.

This route uses no transitivity, but it does require the all-facts total-explainer premise, member projection, inclusive reflexivity, antisymmetry, the particular constituent, and the basic full-self prohibition. The formal theorem exposes them. It does not establish the restricted route from its weaker comprehension and PSR. The final passage from a supernatural fact to a concrete supernatural being is source-definitional prose, not an extra Lean theorem about entities.

## Recommended retained wording

“The displayed restricted relational axioms, together with the audited basic-natural and particularity predicates, admit a three-fact control with no supernatural predicate instance. The control identifies a missing reverse-parthood exclusion in that formal package; it does not establish that its assigned explanation is metaphysically adequate. Two explicit sufficient additions close the bridge. A separate unrestricted-totality route succeeds under its stronger premises.”

The short total-explainer proof and the supplemented weakened controls can likewise be retained with their current nonemptiness, comprehension, omitted-axiom, and written-versus-formal qualifications. No mathematical correction or further replay is requested by this review.
