# A hypothetical atom application conversion bridge

## Status and answer

Adding the single conversion schema

**atom(app(r,s)) ≈ app(atom(r),atom(s))**

for arbitrary raw source terms r and s supports a sound hypothetical extension of P01AC. An ordinary structural proof then gives conversion of every closed polynomial p to atom(eval(p)), and therefore closed packing and typing transfer under literal evaluation equality. The extended polynomial conversion also captures exactly the unchanged raw source Conv between opaque atoms, and consequently between evaluated closed polynomials.

This assesses an already recognized design option. It does **not** modify the delivered P01AC calculus, its accepted source, or the separate accepted counterexample note. The delivered design deliberately excluded an atom/application bridge. The proposal changes that decision and removes the opaque-atom admission boundary on which the new whole-label replacement argument depends. It is not a bug fix already available in the current rules.

The arguments below are written mathematical proofs for a precisely specified hypothetical system. No Lean implementation, new kernel certification, experiment, adoption or new programme version is supplied. They do not establish full semantic completeness, existential representability of arbitrary semantic sections, or open-term packing.

## 1. Exact hypothetical change

Use the raw Term, Poly, Ty and telescope syntax, literal evaluation, substitutions, bracket abstraction, finite typing, source reduction and semantic predicates of the delivered **Dependent_All_Public_Source_v2_20261003** component unchanged.

Define a new inductively generated polynomial conversion relation **PolyConv⁺**. It has exactly the seven existing P01DF.PolyConv constructors, with their recursive conversion premises referring to PolyConv⁺:

- reflexivity;
- symmetry;
- transitivity;
- application congruence;
- the exposed polynomial I contraction;
- the exposed polynomial K contraction;
- the exposed polynomial S contraction.

Add one constructor, **bridge(r,s)**, with the displayed endpoints atom(Term.app r s) and Poly.app(atom r,atom s). The raw r and s range over finite source terms; they are not open polynomial variables. Symmetry already supplies the reverse orientation. No new raw Step, source Conv, evaluation, abstraction, type-equality or semantic-admission rule is added.

Define fresh mutually inductive judgments **Ctx⁺, Form⁺ and Has⁺** by copying the current 2 context, 7 formation and 18 typing constructors, referring recursively to these fresh judgments. Replace the two existing PolyConv premises uniformly by PolyConv⁺:

1. identityIntro still requires formed identity type and both typed endpoints, but its conversion certificate is PolyConv⁺;
2. conv still requires Form⁺ Γ A, Has⁺ Γ p A and Scoped(length Γ,q), but uses PolyConv⁺ p q.

All other premises, source polynomials, finite image tables, binder conventions, scope checks, Raw restrictions and J coordinates are unchanged. In particular, the finite import constructor still requires an actual unchanged FiniteDerives certificate. The additional conversion can nevertheless derive opaque typings that the old finite import alone could not admit.

The structural definitions F, G, D, E and H in AllPredicates remain exactly the old definitions. They are defined on raw types and telescopes independently of whether a formation derivation belongs to the old or hypothetical judgment. Their laws for newly formed types must be proved, not assumed.

## 2. Evaluation soundness of the extended conversion

For every PolyConv⁺ p q derivation and every term valuation η:

**Conv(eval(p,η),eval(q,η)).**

Proof is induction on the conversion derivation. The existing seven cases use precisely the old reflexivity, symmetry, transitivity, raw application congruence and I/K/S source-step arguments. In the new case,

**eval(atom(app(r,s)),η) = app(r,s) = eval(app(atom(r),atom(s)),η)**

by the definition of evaluation. Raw Conv reflexivity proves the goal. No typing, formation, normalization, marker-freeness or valuation-relatedness hypothesis is needed for this case.

This only proves source-conversion soundness of the new polynomial relation. It does not identify polynomial syntax literally: the two bridge endpoints remain distinct Poly values.

## 3. Why the mutual semantic soundness proof extends

The appropriate claims for the new judgments are:

- Ctx⁺ Γ implies the existing semantic ContextLaws Γ;
- Form⁺ Γ A implies the existing hereditary semantic laws for A over Γ;
- Has⁺ Γ p A implies those formation laws and the existing Fundamental Γ p A, namely G A R η ξ (eval(p,η)) (eval(p,ξ)) whenever H Γ R η ξ.

Prove these simultaneously by induction on the new finite derivations, following the mathematical structure of AllSoundness. The syntactic induction is new; the existing theorem with an old Has or Form argument cannot simply be applied to a Has⁺ or Form⁺ argument.

All context and formation cases use their smaller semantic induction conclusions. Identity formation still uses both endpoint fundamental conclusions, so newly admitted dependent identity types are covered by the same mutual proof rather than an assumed old formation certificate.

The variable, I/K/S, finite import, All, Raw, Pi, Sigma, proof-erasure and J cases use the same semantic-rule lemmas. Their relevant helper signatures accept Lookup, ContextLaws, TypeLaws, Fundamental or the unchanged finite source certificate, rather than an old Has/Form derivation. The syntax and raw semantics supplied to those helpers have not changed.

There are exactly two conversion-sensitive cases:

**Typing conversion.** From the smaller Has⁺ premise obtain its fundamental relation. Form⁺ supplies TypeLaws for the same A. The conversion result from Section 2 gives Conv between the evaluations of p and q separately at η and ξ. Apply the existing two-sided raw-saturation law of A to transfer the relation. The conclusion's original scope check remains required.

**Identity introduction.** The existing helper P01AC.fundamental_identity_intro in AllTermLemmas.lean takes the old PolyConv as an argument, so its literal theorem signature is not reusable. Its proof, however, uses that argument only to obtain the two evaluation-Conv facts. Restate and prove the helper with PolyConv⁺ by using Section 2. The typed endpoint p supplies self-membership at both endpoint environments. Each endpoint PER's raw-saturation law transports the second endpoint from eval(p) to eval(q), and reflexive Conv(I,I) supplies the two proof-witness clauses. Both endpoint typing and formation premises of the constructor are retained.

These arguments cover all new mutual constructors. The extra conversion generator is handled by Section 2 rather than by adding a typing constructor. Thus the unchanged F/G model is sound for the hypothetical extended judgments, including newly formed identity types and the recursive All clauses. The conditional semantic-substitution lemmas used in the inherited soundness proof retain their exact semantic premises; no general promise is made that all existing implementation files or exported theorems migrate unchanged.

## 4. Closed polynomial packing

Let ζ be the inherited zeroEnv. Define **Pack(p) = atom(eval(p,ζ))**. This definition alone is meaningful for every polynomial, but the theorem requires **Scoped 0 p**.

**Closed packing conversion.** If Scoped 0 p, then PolyConv⁺ p Pack(p).

Proof by structural induction on p, carrying its scope premise:

- A variable case is impossible, since no natural index is less than zero.
- If p=atom(r), evaluation is r, so the desired conversion is reflexivity.
- If p=app(f,a), scope gives Scoped 0 f and Scoped 0 a. The induction hypotheses and application congruence give conversion from p to app(atom(eval(f,ζ)),atom(eval(a,ζ))). Apply the reverse bridge with raw arguments eval(f,ζ) and eval(a,ζ). Its endpoint is atom(app(eval(f,ζ),eval(a,ζ))), which is definitionally Pack(p). Transitivity completes the step.

The same structural cases also show that a scope-zero polynomial's evaluation is independent of η. Thus ζ selects its unique literal raw meaning, rather than silently substituting for a free term variable.

**Closed packing preserves hypothetical typing.** Assume Form⁺ [] A, Has⁺ [] p A and Scoped 0 p. Pack(p) is an atom and is therefore Scoped 0. Apply the hypothetical conv rule with the preceding conversion to obtain

**Has⁺ [] Pack(p) A.**

The target A is held fixed. Its type parameters need not be closed; the explicit formation premise is the hypothetical judgment's actual premise. No equation identifying A with its own packed or semantically equivalent form is introduced.

**Typing transfer under literal evaluation equality.** Assume Form⁺ [] A, Has⁺ [] p A, Scoped 0 p, Scoped 0 q and eval(p,ζ)=eval(q,ζ). Closed packing gives conversions from p and q to the same atom. Use transitivity and the reverse q conversion to obtain PolyConv⁺ p q, then the conv rule gives Has⁺ [] q A. Equality at every valuation is a sufficient, stronger way to state the literal-evaluation premise; for these closed polynomials it amounts to equality of their unique evaluated raw terms.

This proves the two requested interface properties for the hypothetical system. It does not show that every semantically valid p has any typing derivation. It transfers an already supplied derivation, and only across the displayed literal evaluation equality.

## 5. Exact reflection of raw source conversion

The bridge also gives an exact comparison between the unchanged raw source conversion and the hypothetical conversion of opaque atoms:

**For all raw r and s, Conv r s if and only if PolyConv⁺ atom(r) atom(s).**

This concerns the existing raw source Conv, not equality in an arbitrary PER. The proof uses the actual source constructors. Raw Step has I, K and S contractions plus left and right compatible application contexts. Raw Conv, defined in BoundaryResults.lean, has reflexivity, a Step injection, symmetry and transitivity.

First prove that every **Step r s** induces **PolyConv⁺ atom(r) atom(s)**, by induction on Step.

- **I contraction.** Bridge atom(I x) to app(atom(I),atom(x)); the existing polynomial I rule contracts this to atom(x).
- **K contraction.** Two bridge uses, the inner one under polynomial application congruence, convert atom((K x) y) to app(app(atom(K),atom(x)),atom(y)). The existing polynomial K rule contracts this to atom(x).
- **S contraction.** Three bridge uses expose atom(((S f) g) x) as app(app(app(atom(S),atom(f)),atom(g)),atom(x)). The polynomial S rule gives app(app(atom(f),atom(x)),app(atom(g),atom(x))). Apply the reverse bridge separately to the two inner applications, using application congruence, and then the reverse bridge to the outer application. The result is atom((f x) (g x)), exactly the raw S successor.
- **Left context.** If Step f g has already yielded conversion atom(f) ≈ atom(g), bridge atom(f x) to app(atom(f),atom(x)), use application congruence with the induction hypothesis and reflexivity of atom(x), then use the reverse bridge to obtain atom(g x).
- **Right context.** If Step x y has yielded conversion atom(x) ≈ atom(y), bridge atom(f x) to app(atom(f),atom(x)), use application congruence with reflexivity of atom(f) and the induction hypothesis, then repack to atom(f y).

This exhausts raw Step, including reductions underneath a discarded argument. No normalization assumption is used.

Next induct on raw Conv. Reflexivity, symmetry and transitivity map to the corresponding PolyConv⁺ constructors; its Step-injection case uses the lemma just proved. This establishes the forward implication for every raw source conversion certificate, with no scope or typing restriction on its raw endpoints.

Conversely, PolyConv⁺ atom(r) atom(s) gives Conv r s by Section 2 at any valuation, since the evaluations of the two atoms are r and s. This completes the equivalence.

**Closed polynomial characterization.** For Scoped 0 p and Scoped 0 q:

**PolyConv⁺ p q if and only if Conv(eval(p,ζ),eval(q,ζ)).**

Left to right is evaluation soundness. Right to left uses the atom equivalence to convert Pack(p) to Pack(q), then composes the closed-packing conversion from p to Pack(p) with the reverse closed-packing conversion from Pack(q) to q. Thus the hypothetical polynomial conversion is complete for this precise raw source-conversion relation on closed polynomials. This is a conversion-relation result, not semantic completeness of the typing judgment.

**Typing consequence at a fixed type.** If Form⁺ [] A, Has⁺ [] p A, Scoped 0 p, Scoped 0 q and Conv(eval(p,ζ),eval(q,ζ)), the characterized conversion and the retained scoped conv rule give Has⁺ [] q A. In particular, raw Conv r s transports Has⁺ [] atom(r) A to Has⁺ [] atom(s) A. The d-to-I obstruction of the unchanged calculus is therefore absent in this hypothetical extension, as the earlier packing proof already demonstrated for its concrete witnesses.

This equivalence does not identify different raw normal forms that the old source Conv separates, does not provide an effective conversion decision procedure, and says nothing here about a characterization for arbitrary open polynomial expressions. Nor does it turn membership in some semantic PER into a raw source-conversion certificate.

## 6. Relation to old proofs and the admission tradeoff

Every old PolyConv derivation embeds into PolyConv⁺ by induction. Consequently every old context, formation and typing derivation embeds into the corresponding hypothetical judgment by mutual induction, replacing only conversion certificates where necessary. The source polynomial and type remain literal. This is an inclusion of positive derivations, not a conservativity theorem for the new typing relation.

The extension is not conservative for the supplied opaque representation. Let t=S K (K Ω), A=All(α→α), and p be the accepted application polynomial with eval(p,η)=t. The old Has [] p A derivation embeds. Closed packing now yields **Has⁺ [] atom(t) A**. Likewise the typed polynomial for d=(K I)Ω packs to **Has⁺ [] atom(d) A**. The ordinary counterexample proof shows that neither opaque conclusion is derivable in the unchanged P01AC at A.

The finite source judgments do not change. In particular t and d still have no direct FiniteDerives type under the inherited results. Their newly available opaque typings arise through the added conversion, not through new finite certificates. Therefore the current calculus's necessary direct-finite-typing condition for certain opaque atoms does not carry over to Has⁺.

The broken invariant can be seen in a single generator, without assuming the negative theorem transports to the new theory. Let M replace the whole atom(d) by atom(K), fixing all other whole labels. Take the bridge instance

**atom(d) ≈ app(atom(K I),atom(Ω)).**

The whole labels K I and Ω differ from d. After M, the left side becomes atom(K), while the right side is unchanged. Their evaluations are K and d. If this mapped pair were PolyConv⁺-related, Section 2 would give Conv K d. Since d → I, this would imply Conv K I. K and I are distinct source normal forms, which inherited source confluence forbids. Hence M does **not** preserve this new generator.

This is exactly why the old whole-label replacement argument no longer applies. Its old premise that distinguished non-finite atom labels were accessed only through Raw admission or finite import is no longer true: the bridge exposes their source-application structure to conversion.

## 7. Limits of this assessment

**No open-term packing claim.** Scoped 0 is essential to the displayed induction. At var(0) there is no fixed raw atom with the same valuation-dependent literal value. Even a proposed conversion of var(0) to one fixed atom would conflict with evaluation soundness at valuations assigning I and K, since those source normal forms are not convertible. This does not rule out a separately specified representation of environments or an open syntax-to-syntax translation; none is supplied here.

**No semantic-completeness claim.** Literal equality of evaluated raw terms is much narrower than general semantic validity or equality in a chosen PER. The proof does not reverse the fundamental theorem, recover arbitrary semantic sections, or decide typing or semantic equality. Section 5 characterizes PolyConv⁺ only on closed polynomials using the existing raw source Conv; it does not characterize arbitrary open conversion or replace raw Conv with PER equality.

**No new normalization or backend equality claim.** Raw Term, Step and Conv are unchanged; Ω and the inherited normalization boundaries remain. The bridge does not identify I with S K K as raw terms, introduce source η, or justify arbitrary body-conversion congruence for bracket abstraction. Such conclusions would require separate arguments and are not consequences asserted here.

**No implementation migration claim.** Existing compiled signatures mention the old inductive types and conversion relation. A realization would need fresh definitions or an explicitly authorized change, revised soundness proofs, dependency checks and independent verification. The written argument is evidence for the stated mathematical design, not a ready implementation or permission to alter the delivered calculus.

## 8. Prior ownership and public source locators

The delivered dependent-All design already identified this boundary. In **DEPENDENT_ALL_DESIGN_v5.md**, section 1's finite-import discussion, an earlier proposal to reconstruct opaque finite imports using polynomial I/K/S/application is rejected because Poly.app(atom f,atom a) and Poly.atom(Term.app f a) are distinct and the existing conversion lacks a bridge. That design explicitly directs the retained calculus not to add such a bridge. **PROOF_GUIDE.md** and the accepted review preserve the same exclusion. The current proposal is therefore a hypothetical reconsideration of a known design choice, not discovery of an unrecognized option.

In the bounded retained-source inspection, no completed positive assessment of the exact one-schema extension and its closed-packing proof was located. This is not a literature-wide novelty claim or evidence that no earlier assessment exists elsewhere.

The fixed source component is **Dependent_All_Public_Source_v2_20261003.zip**, SHA-256 **a58e2f510e08d2e2447b15b617cdb85dd1c36a3f04441a75897781c2c8f544db**. Decisive modules are:

- **AllSyntax.lean:** exact old grammar, context/formation/typing constructors, scope and the two PolyConv premise locations.
- **P01DependentFundamental.lean:** old seven-constructor PolyConv and polyConv_sound.
- **P01Polynomials.lean:** Poly, literal eval, abstract and source expressions.
- **AllPredicates.lean:** unchanged F/G and D/E/H definitions.
- **AllSoundness.lean:** old mutual semantic proof and conversion cases.
- **AllTermLemmas.lean:** the old identity-introduction helper and its exact conversion-soundness dependence.
- **P01Confluence.lean:** distinct source normal forms are not Conv-related.
- **InternalPolymorphism.lean:** exact raw Step constructors, including both compatible-context cases.
- **BoundaryResults.lean:** the four constructors of raw source Conv.
- **NormalisationAndNumerals.lean:** the inherited discarded-loop source d.

The separately reviewed **Opaque atoms and fixed polynomial semantic incompleteness**, final counterexample proof SHA-256 **b99fb16058f99ce5db66dd7a02e7515ede5157a002a6e76fc29d0f1bd8d65236**, remains a statement about the unchanged delivered calculus. None of its bytes or accepted scope is altered by this assessment.
