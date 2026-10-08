# Dependent All over syntax-generated typed telescopes

Revision v5 retains the finite-instance repair and explicit Type-valued legacy support provenance, and specifies the legacy J proof-coordinate bridge. V1–v4 remain immutable superseded records. The All semantics and mixed-substitution design are unchanged.

## Disposition and dependency

**Proposed bounded completion target; mathematically coherent design, not an implemented or independently accepted result.** It joins the two capabilities that the typed-context nucleus deliberately separates: arbitrary syntax-generated typed telescopes/Pi/Sigma/Id, and genuine impredicative All with dependent replacement types. It does not add universes, Type:Type, normalization, canonical unary equality, or a frontend language.

The nucleus is an active, not yet independently accepted candidate at the observation recorded in `INPUT_IDENTITIES_v1.json`. Its interfaces are observations, not proved premises for this target. Implementation admission must wait for the actual nucleus acceptance packet, reconcile any interface changes, and independently assess this new design. The unchanged-Has substitution owner is independently accepted; it proves neither this new calculus nor its new context laws.

This document is original mathematical design using inherited project sources only. There is no new primary-source exposition, implementation, compilation, canonical mutation, publication, or external contact.

## 1. Change the grammar, rather than hide an adapter

Use the existing finite source `Poly`, evaluation, source Conv, K-priority abstraction, represented pairs/projections and J tracker unchanged. Define a new recursively generated type grammar:

    A ::= Param(n) | Bottom | Raw | Pi(A,B) | Sigma(A,B)
        | Id(A,p,q) | All(B).

Pi/Sigma bind one term variable in B. All binds one type parameter in B and no term variable. The old opaque `AllFinite(C)` constructor is absent. Type parameters continue to range over every lawful source PER; relations range over every respectful Link, not only raw-refining or total/functional links.

Translate the nucleus grammar by identity on its ordinary constructors and

    translate(AllFinite(C)) = All(finRec(C)),
    finRec(var n)=Param(n), finRec(bottom)=Bottom,
    finRec(arrow C D)=Arr(finRec(C),finRec(D)),
    finRec(all C)=All(finRec(C)).

Here Arr(A,B)=Pi(A,wkTerm(B)). This is a grammar translation, **not literal type identity** with the nucleus. Establish equality of unary predicates and heterogeneous predicates for the translated finite fragment, by induction on finite TypeCode using the accepted recursive finite model. The polynomial itself remains literal.

Retain the nucleus's syntax-only Ctx/Form/Has constructors for Pi/Sigma/typed Id/J and its restricted Raw rules, after this translation. Do not assume semantic validity/coherence in any rule. Retain exact closed polynomial imports through a **finite-instance syntax rule**:

    FiniteDerives(t,C), Form Γ (τ n) for each free parameter n of C,
    Form Γ (substType τ (finRec C))
    ---------------------------------------------------------------
       Has Γ (atom t) (substType τ (finRec C)).

Represent τ by a finite table covering C's binder-aware free parameter support (subtracting the depth of each enclosing finite All), with Bottom outside that table; the rule has finitely many syntactic formation premises. Under binders use the capture-avoiding substitution of section 2. A table agreeing with Param(n) on that support recovers the literal nucleus import. No semantic membership or uniformity premise appears.

This small import schema is required for source-code-preserving compatibility. The previous v1/v2 proposal to reconstruct it using polynomial I/K/S/application was incorrect: Poly.app(atom f,atom a) is not Poly.atom(Term.app f a), and the unchanged PolyConv has no atom-application bridge. Equality after evaluation does not repair that syntactic gap. Do not add a bridge to PolyConv or silently change the imported polynomial.

The finite-instance rule is closed under mixed substitution by substituting each table entry and keeping the same FiniteDerives(t,C) proof and literal atom t. Its fundamental case uses the accepted finite fundamental theorem at the replacement REnv constructed from its smaller formation premises, the finite interpretation comparison, and the conditional substitution lemma of section 7. This auxiliary rule preserves imports; it does not supply new All formation/elimination, a semantic witness assumption, or the target synthesis.

## 2. Two sorts of binding, fully explicit

Write W for free type-parameter shift (Param n becomes Param(n+1)); under All it uses the lifted type renaming, and under term binders it is unchanged. It never changes polynomials. Write w for term shift, recursing through typed Id carriers and shifting both endpoints, lifting under Pi/Sigma and not under All. W and w commute literally.

For a simultaneous map with term components σ:Nat→Poly and type components τ:Nat→Ty, define M(σ,τ,A) structurally:

- Param(n) maps to τ(n); Raw/Bottom stay unchanged.
- Id(A,p,q) maps to Id(M(σ,τ,A),psub(σ,p),psub(σ,q)).
- Pi/Sigma domains use M(σ,τ); their bodies use M(pup σ, w∘τ).
- All(B) maps to All(M(σ,τ↑,B)), where τ↑(0)=Param(0) and τ↑(n+1)=W(τ(n)).

The target term context under All is WΓ, with the same indices and length. Under a term binder the target context extends and both old term images and every replacement type must be term-weakened. Under a type binder the source polynomials and their term images do not acquire an index, but every free type parameter of a replacement type shifts.

Pure term substitution is M(σ,Param); pure type substitution is M(var,τ). The top type instance B[A] uses τ=(A,Param(0),Param(1),...), and term images var. For example, replacing free type parameter 0 by Id(Raw,var 0,I) in All(Pi(Raw,Param 1)) yields exactly

    All(Pi(Raw,Id(Raw,var 1,I))).

The var 1 is mandatory: var 0 would capture the new Pi argument. A replacement containing free Param(0) instead becomes Param(1) under the All. Test a replacement containing both sorts at once.

Required literal equations include identity/composition of M, W/w commutation, binder lifts commuting, cancellation of top substitution against W, and the mixed square

    substTerm σ (substType τ B)
      = M(σ, (n ↦ substTerm σ (τ n)), B).

The right side is the simultaneous operation just defined; expressing it as naive composition in the opposite order risks re-substituting polynomial images. The general composition formula is

    M(σ₂,τ₂,M(σ₁,τ₁,B))
      = M((n ↦ psub σ₂ (σ₁ n)), (n ↦ M(σ₂,τ₂,τ₁ n)), B).

The All/term-lift commuting square and the double term lift in Theta/J are explicit cases, not an appeal to informal capture avoidance.

## 3. Formation and erased introduction/elimination

Telescope type weakening applies W to every declaration. Because W does not change term indices, declaration dependencies are preserved.

    Ctx Γ, Form (WΓ) B
    ----------------- All formation
       Form Γ (All B)

    Form Γ (All B), Has (WΓ) p B
    -------------------------- All introduction
         Has Γ p (All B)

    Form Γ (All B), Form Γ A,
    Form Γ (B[A]), Has Γ p (All B)
    ---------------------------- All elimination
             Has Γ p (B[A]).

The explicit result-formation certificate follows the nucleus's finite proof-tree discipline. It is redundant only after proving syntactic substitution/regularity. All is erased: both introduction and elimination keep p literally unchanged. There is no requirement that A be closed, term-independent, finite, or All-free. In particular A=All B is allowed whenever formed in Γ.

The old unconditional context-free allIntro rule is inadmissible here. An assumption x:Param(0) does not become a term of every freshly quantified parameter; its old type shifts to Param(1) in WΓ. The required structural theorems are Ctx Γ⇒Ctx WΓ and preservation of formation/typing under injective type renaming, with p unchanged. They are syntax-only induction theorems.

Keep all nucleus limitations: no arbitrary typed-to-Raw coercion, no universal open Raw rule, no equality reflection through a Link, no new raw conversion. Id proof erasure remains the specific permitted rule.

## 4. Raw semantics: a structural pair, not all F followed by all G

The nucleus's global construction order “define F first, then G” cannot survive genuine All. Define the **pair** (F_A,G_A) by structural recursion on A. Ordinary constructors have exactly the observed nucleus clauses; F_Pi/F_Sigma/F_Id use smaller F, and G_Pi/G_Sigma may use the already-computed F of that same constructor plus smaller G. At All, F uses G of its strictly smaller body. This is well-founded structural recursion, not recursion through a law, Model, PER-construction result, or typing derivation.

At every raw environment, including invalid ones, set:

    U_B(ρ,η;t) := ∀ P Q (R:Link P Q),
                    G_B(R::diag ρ,η,η;t,t).

    F_(All B)(ρ,η;t,u) :=
       U_B(ρ,η;t) ∧ U_B(ρ,η;u)
       ∧ ∀ P, F_B(P::ρ,η;t,u).

    G_(All B)(r,η,ξ;t,u) :=
       F_(All B)(r.left,η;t,t)
       ∧ F_(All B)(r.right,ξ;u,u)
       ∧ ∀ P Q (R:Link P Q), G_B(R::r,η,ξ;t,u).

P,Q range over all lawful PERs, including All PERs. R::r is the accepted REnv extension. These raw clauses mention no desired relation theorem. U is part of the *semantic definition* of the All PER, never a premise of formation or typing. F/G need not satisfy laws for malformed syntax. D/E/H remain the nucleus's raw recursively defined finite zero-padded telescope predicates.

At a formed All type and valid valuation the body law package constructs the needed ParamFamily; F_All agrees extensionally with accepted AllPER for that family. This agreement is a consequence. Defining the raw clauses first avoids pretending that a lawful ParamFamily is already available before proving formation soundness.

## 5. The telescope weakening laws that make introduction possible

First prove raw parameter-renaming equations structurally on the paired predicates. In particular, for every inserted lawful P,Q,R and raw η,ξ:

    F_(W A)(P::ρ,η) = F_A(ρ,η),
    G_(W A)(R::r,η,ξ) = G_A(r,η,ξ).

The All case uses the type-renaming lift and REnv extension/diagonal equations. No replacement-type law or fundamental theorem is needed for these renaming equations. The corresponding telescope equations are then literal predicate equalities:

    D_(WΓ)(P::ρ,η) ↔ D_Γ(ρ,η),
    E_(WΓ)(P::ρ,η,ξ) ↔ E_Γ(ρ,η,ξ),
    H_(WΓ)(R::r,η,ξ) ↔ H_Γ(r,η,ξ).

Thus the same η and ξ remain usable for every new type endpoint and link, despite declarations in Γ being dependent on earlier term coordinates. No valuation is changed and no extra uniformity assumption on its entries is introduced.

All introduction now applies the premise's fundamental IH under R::r for arbitrary R. For each endpoint's own U, apply that *same smaller typing IH* under R::diag(r.left) at (η,η), or under R::diag(r.right) at (ξ,ξ). H endpoint validity, diagonal context agreement, and the weakening equations supply these contexts. Body diagonal identity gives the remaining ∀P unary self-memberships in F_All. This derives semantic uniformity from syntax.

## 6. Strong diagonal identity extension at unequal valuations

Retain the full nucleus law package, including unary F transport along E, Link endpoints/respect, two-sided G invariance under the separate left/right E relations, and

    E_Γ(ρ,η,ξ) ⇒
      G_A(diag ρ,η,ξ;t,u) ↔ F_A(ρ,η;t,u).

For All, body laws apply under WΓ by section 5. First establish unary transport of F_All: transport each F_B instance along E_(WΓ)(P::ρ,η,ξ), and transport each U instance by **both** sides of body G invariance under P::ρ and Q::ρ. This proves F_All(ρ,η)=F_All(ρ,ξ), including uniformity, not just its pointwise intersection.

For diagonal extension, forward direction: G_All supplies endpoint self-memberships. Transport the right one's U from ξ back to η. In its universal cross clause choose Q=P and R=diagonal P; body strong diagonal at E_(WΓ)(P::ρ,η,ξ) yields F_B(P::ρ,η;t,u) for every P. These are exactly the F_All clauses.

Reverse direction: F_All at η supplies Uη(t), Uη(u), and all within-P comparisons. Its PER laws provide self-membership of t; transport self-membership of u to ξ. For arbitrary P,Q,R, Uη(t) gives

    G_B(R::diag ρ,η,η;t,t).

Change its right valuation from η to ξ using body two-sided invariance and the lifted E relation under Q::ρ. Transport the within-Q comparison F_B(Q::ρ,η;t,u) to ξ. Body Link respectfulness then changes the right result t to u, obtaining

    G_B(R::diag ρ,η,ξ;t,u).

This proves the universal cross clause. It does not equate η with ξ or assume the desired All identity law. F_All PER laws use the body PER laws; G_All endpoints are explicit; G_All respect uses each endpoint's ∀P comparison and body respect; G_All two-sided invariance transports endpoint F_All self-memberships and each body G instance separately.

## 7. Dependent elimination: the frozen parameter environment

For Form Γ A and H_Γ(r,η,ξ), derive from A's *smaller formation package*

    P = O_A(r.left,η),
    Q = O_A(r.right,ξ),
    R = L_A(r,η,ξ) : Link P Q.

R is not an interpretation at a single shared valuation. P,Q may differ, and R may be empty or nonfunctional. The All premise's fundamental IH gives its cross clause at R::r. To identify its conclusion with G_(B[A])(r,η,ξ), prove the semantic top-substitution equation

    G_(B[A])(r,η,ξ;t,u)
      ↔ G_B(R::r,η,ξ;t,u),

and at each unary endpoint

    F_(B[A])(ρ,η;t,u)
      ↔ F_B(O_A(ρ,η)::ρ,η;t,u).

Crucially, when recursion descends through Pi/Sigma in B, the inserted P,Q,R remain frozen at the original η,ξ. The replacement becomes wA syntactically, so at extended valuations a::η,b::ξ:

    F_(wA)(ρ,a::η)=F_A(ρ,η),
    G_(wA)(r,a::η,b::ξ)=G_A(r,η,ξ).

Without weakening replacement types, a parameter occurrence under Pi would incorrectly re-evaluate A with a newly bound argument captured as an old variable. Under All, type-shifting A ensures that it ignores the freshly inserted PER/Link. These are the precise mixed term/type squares needed; dependent parameters are allowed because the new bound variables cannot capture them.

### The nontrivial All case of semantic substitution

Unlike the nucleus's raw term-substitution lemma, semantic *type* substitution is not an unconditional theorem for arbitrary malformed replacement types. It must use lawful replacement interpretations and their diagonal identity.

For a replacement family τ formed in a target Γ, let ρτ(n)=O_(τn)(ρ,η), and rτ have endpoints O_(τn)(r.left,η), O_(τn)(r.right,ξ) and relations G_(τn)(r,η,ξ). Formation laws construct these PERs and Links. At the unary U clause under substitution, the induced environment at diag ρ,η,η has relations G_(τn)(diag ρ,η,η). A replacement's diagonal law identifies these with F_(τn)(ρ,η), making this REnv exactly diag(ρτ), up to record extensionality. That equality, plus type weakening, discharges the nested All uniformity clause.

This dependence must be stated in the theorem: structural induction on the *raw target type B*, parameterized by the already available replacement law packages at the original base valuations. Under term binders use the literal weakening equations to keep those same packages at the base; do not require the theorem for a newly enlarged arbitrary family. Under type binders use raw type-renaming equations to remove the fresh parameter. Prove unary and heterogeneous substitution equations together, because F_All calls the smaller G equation. No formation or soundness assumption about B[A] is used to prove these equations, and no call to the fundamental theorem on the current elimination derivation occurs.

A convenient stronger statement treats M(σ,τ,B), with the source valuation equal to evaluation of σ at each target valuation, and the source parameter REnv equal to rτ above. Carry arbitrary finite term-prefix depth in the induction so lifted τ always interprets at the original base valuations. This explicitly separates term reindexing from the frozen parameter environment.

## 8. Noncircular proof schedule and syntactic admissibility

1. Define syntax, paired raw predicates, and D/E/H. Prove literal two-sort algebra, scope, raw term-substitution equations, and raw type-*renaming* equations. Prove the raw finRec/accepted-finite predicate comparison by TypeCode induction before the derivation induction; this comparison is term-valuation-independent and needs no new typing soundness.
2. Prove the conditional semantic mixed-substitution lemma of section 7 by type-structure induction, taking lawful/diagonal replacement packages as hypotheses. These are hypotheses of a metatheorem, not new typing or formation premises.
3. Extend the nucleus's simultaneous finite derivation induction. Context and ordinary type/term cases retain their dependencies. All formation uses the smaller body formation package plus weakening. All introduction uses its smaller typing package as in section 5. All elimination uses smaller A formation, All-premise typing, and the conditional substitution lemma. The finite-instance case likewise uses only its smaller replacement-formation packages, the already accepted finite theorem, and that lemma. Explicit syntax formation certificates remain counted in derivation rank.
4. Package PERs/Links and derive the universal heterogeneous fundamental theorem, strong diagonal/unary theorem, and exact-code interpretation. All's semantic universal properties come from these laws, not constructor assumptions.
5. Prove mutual syntactic preservation for contextual mixed substitutions, separately from semantic soundness. It should be possible by finite syntactic induction plus section 2 algebra; it is a required deliverable, not an assumption used to claim step 3. Establish finite-instance closure and the nucleus/legacy translations; the exact finite atom is retained rather than reconstructed from Poly.app.

For precision, a contextual mixed substitution from source Δ to target Γ consists of a formed replacement type τn in Γ for each used free source parameter, a finite list of term images σ with target scope, and syntax typing of each image at the simultaneous substitution of its declaration using the already supplied tail images. No type replacement is installed into an earlier target declaration. This avoids the invalid operation of replacing a parameter in the source telescope by a type mentioning later variables of that same telescope. All elimination is the special map WΓ→Γ with identity term images and τ=(A,Param0,Param1,...); by top cancellation its declaration images are literally the original Γ declarations.

Lifting this map under a source term declaration extends the target by the translated declaration, replaces τ by wτ and σ by pup σ. Lifting under All uses WΓ, σ unchanged, and τ↑. The All introduction case of substitution therefore has exactly the WΓ context its rule requires. Double term lifting must commute with the literal Theta/J substitution. All form/intro/elim rules must survive this construction with finite syntactic evidence alone.

A proof requiring semantic uniformity in Has, arbitrary coherent family arguments in Form, a source-valuation-only replacement Link, or an unconditional diagonal equation for malformed replacements fails this design and must stop for review.

## 9. Concrete recovered and newly joined derivations

### Exact inherited dependent polymorphism, modulo explicit type translation

The inherited source owner defines

    dependentPolyType = All α. Pi_raw x. (α → Id_raw(x,I) → α)

and proves Has(abstract(atom K),dependentPolyType), followed by self-instantiation. Its new translation is

    D = All( Pi(Raw,
          Arr(Param0, Arr(Id(Raw,var0,atom I),Param0))) ).

Arr expands with the required term weakenings. Under x:Raw the type Id(Raw,x,I) forms syntactically, whether or not inhabited. K has the displayed arrow type. Pi introduction followed by All introduction yields exactly the same polynomial abstract(atom K) at D. Elimination with A=D yields the literal top-substituted dependent body Dbody[D]. This recovers the old non-finite dependent All subtree and self-instantiation deliberately excluded in nucleus design v4 section 8.

### A single derivation requiring both capabilities

Let

    C = Pi(Param0, Sigma(Param0, Id(Param0,var1,var0))),
    Q = All(C),
    q = abstract(pairPoly(var0,atom I)).

The nucleus's typed pair derivation, translated into the new grammar, proves Has [] q C. The new All rule proves Has [] q Q. Eliminating it at Q proves

    Has [] q (Pi(Q, Sigma(Q,Id(Q,var1,var0)))).

The parameter variable and dependent Sigma/typed Id require arbitrary typed domains; genuine All and this impredicative self-instantiation require the added binder. Neither an opaque finite-All adapter nor the old raw-domain calculus can state and derive this complete judgment as written. Its inhabitant is nonempty and keeps the exact nucleus polynomial.

### Genuinely term-dependent replacement control

In Γ=(x:α,y:α), take A=Id(α,x,y). Instantiate a formed polymorphic identity All β.(β→β) at this A to obtain Arr(A,A), with the same identity source polynomial. The two term valuations may produce different endpoint equality conditions; the replacement Link includes each condition separately and may be empty. The rule remains sound because it substitutes that actual Link, not a guessed equality or single endpoint. For a nonempty dependent family use A=Sigma(α,Id(α,w x,var0)) and the available typed pair witness; its literal indices and the changing outer x must be checked under nested All/Pi. These complement, rather than replace, the universal theorem and the inherited I/SKK negative controls.

## 10. Comparisons and bounded acceptance criteria

**Nucleus:** require a full derivation translation of its accepted final grammar, including finite constants through the identity finite-instance table, preservation of literal source polynomials, and F/G equality at corresponding valid valuations. Its AllFinite nodes become recursive All nodes; no claim of literal original type identity is allowed. This is a genuine extension up to the specified translation.

**Inherited raw-index calculus:** translate raw Pi/Sigma to Pi(Raw,-)/Sigma(Raw,-), old identity to Id(Raw,-,-), old arrows to Arr, and old All recursively to new All. State this comparison using an explicit Type-valued old-rule tree indexed by the old polynomial and type, with constructor data recording every intermediate type, replacement type, polynomial, motive, and premise tree. Prove an exact forgetful theorem from such a tree to the unchanged P01DF.Has proposition, including its old allIntro/allElim constructors. Define finite telescope support recursively on that tree, accounting for term-binder depth in all premises and type/motive endpoints. Do not attempt to inspect hidden proof provenance of an arbitrary Prop-valued Has proof or assert a reifier from Prop proofs into Type. For a support-certified old-rule tree, there is now no exclusion of allIntro, allElim, or non-finite All subtrees. W of an all-Raw telescope is itself. Arbitrary scoped old replacement types form in it, so the old All rules translate. Preserve literal source code and prove unary/heterogeneous semantic agreement at pointwise-Conv-related raw valuations. State the whole-derivation support condition; a closed final polynomial alone is not enough. In the legacy J case, the new Theta is not literally all-Raw: its newest proof declaration is Id(Raw,x,y). Form the translated old motive first in an all-Raw telescope of the corresponding length, then use a literal identity-polynomial typed substitution into Theta. The proof coordinate is typed Raw by the restricted proofErase rule; the endpoint and older coordinates use their Raw declarations. This transports motive formation without changing its indices or code. Both J coordinates and the double-lift equations remain mandatory. This comparison is a theorem obligation, not an accomplished embedding.

**Accepted substitution extension:** reuse unchanged raw two-sort algebra only through named translations and checked shape lemmas. The new typed Id carrier, arbitrary Pi/Sigma domains, telescope replacement discipline, and All uniformity diagonal step are additional work. No double credit for the already accepted context-free result.

Completion requires finite syntactic rules; universal heterogeneous soundness and strong diagonal; literal typed mixed-substitution preservation; exact-code interpretation; nucleus translation and full support-bounded raw comparison; the recovered D/self and new Q/self controls; nested two-sort capture tests; and all inherited raw/Id/J negative controls. It does not suffice to demonstrate only D, only Q, a wrapper into semantic Tm, a witness-accepting rule, or another finite adapter.

No full avenue9/U11 closure or research novelty priority is claimed here. Canonical carrier/equality counterexamples remain unchanged. Id is equality in its PER with Conv-I proof witnesses. This target remains proof-irrelevant at that level and entails no raw eta, source equality reflection, normalization, universe decoding, arbitrary JSON frontend, or canonical adoption.

## 11. Exact source observations

`INPUT_IDENTITIES_v1.json` binds every inspected input by path, SHA256, bytes, and observation time. In particular:

- Design v4: `21a1016f067499fc087fe0eed26456517db20e3eb050189c9aa3160d549564f2`.
- Independent design gate REVIEW_v3: `63f3b4803a6d59de4a5aadebd003df9469cd7e77414dc1a384abc8ea8bac3a86`.
- Observed TypedSyntax: `b65b90129c3d5e198f9e9266efb8295cea016b41be541b0dbef7683a6438357c`.
- Observed TypedPredicates: `acc5fa0f14f126988ed995879d6e39475a33ca2766519f6e4cc1fdb6f74da3ae`.
- Observed TypedLaws: `234d778b12696c34cf7d61f5fa0c75b4f3e488d14b29f09aef89ea6a12ac8a12`.
- Observed TypedSoundness: `ba9667b33cb3b6268b3450dbd5a803bb880948d12e2b74f1b3739165ee109143`.
- Observed TypedStructural: `881b63b6e21657c32cdd5347c0e32b7877214836ba6c15c45d3e67048d2f0caf`.

At the recorded observation time, the hash-pinned grammar has no type-parameter weakening/substitution and no All introduction/elimination. The observed soundness source is not independent acceptance. Subsequent mutation does not retroactively update these observations. Final admission must rebind to the actually accepted nucleus packet and name any differences.

Inherited owner source-store pins are P01PER `ee15654a...97c87e` (ParamFamily/AllPER/identity extension), P01RecursiveModel `a53b9b16...74f9` (REnv and finite recursive Model), P01DependentFundamental `82cd316b...66aa` (old allIntro/allElim/self theorem), and P01DependentControls `6f1afe90...56c` (dependentPolyType/self and two-sort control); their full identities are in the manifest. The accepted unchanged-Has substitution source/review pins are also bound there. Inherited claims remain owned by those sources; the present document proposes only the additional synthesis and obligations above.
