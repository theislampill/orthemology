# Opaque atoms and fixed polynomial semantic incompleteness

## Result

In the P01AC calculus delivered with **Dependent_All_Public_Source_v2_20261003**, a closed polynomial can be universally semantically valid at the polymorphic identity type and still have no typing derivation at that type. There are closed polynomials p and q with the same evaluation in every environment such that Has [] p A but not Has [] q A, where A = All(α → α).

The witness reuses the accepted source term t = S K (K Ω). Its application-shaped polynomial p is typed at A; its opaque representation q = atom(t) is not. The proof replaces only the whole opaque atom t by K in a hypothetical derivation, then uses the singleton conversion-class PER of I to contradict the resulting alleged identity-type derivation for K.

This is an **ordinary written mathematical proof** about the unchanged delivered calculus. It is not a new Lean-certified theorem or a new kernel replay. The normalization, soundness and finite-typing facts used as prerequisites are inherited results. The conclusion refutes completeness for a prescribed polynomial representation and universal closed atom-packing; it does not refute completeness that permits choosing a different representation with the same meaning. A discarded-loop corollary further shows that even a finite-typed representative at the matching target code, equivalent under raw source conversion, need not type the supplied opaque atom.

## 1. Calculus and inherited prerequisites

The syntax and rules are unchanged accepted P01AC, as defined in AllSyntax.lean; polynomial syntax and abstraction are unchanged P01D; conversion is unchanged P01DF.PolyConv. No extra extensionality, evaluation-reflection, atom-expansion, raw source-conversion typing or semantic-admission rule is assumed.

Raw source terms are finite trees with constants I, K, S, zero, one and binary application. Source Step consists of I x → x, K x y → x, S f g x → f x (g x), and compatible left/right application closure. Red is its reflexive-transitive closure and Conv its equivalence closure. A source normal form has no Step successor. Inherited source confluence implies uniqueness of normal forms modulo Conv.

Polynomials are **var(n)**, **atom(r)** for an arbitrary whole raw source term r, and **app(f,a)**. Their evaluation at a total term valuation η sends var(n) to η(n), atom(r) to r, and app to raw application. An atom containing an application-shaped r is a single polynomial node. Polynomial substitution only replaces var nodes; it leaves whole atom labels untouched.

P01AC types have the exact finite grammar:

**param(n) | bottom | raw | all(B) | pi(A,B) | sigma(A,B) | identity(A,p,q).**

Pi and Sigma bind one term variable in their second argument. All binds one type parameter, no term variable. A telescope Γ is a finite list of types. Ctx, Form and Has are the mutually inductive judgments of AllSyntax.lean, with respectively 2, 7 and 18 constructors. The preservation argument below covers every constructor, together with the 2 Lookup and 7 PolyConv constructors. Term scope checks de Bruijn variables only; every atom is scoped at every term depth. TyScoped recursively checks only polynomial occurrences in identity endpoints. The type-parameter environment is not bounded by a finite parameter context.

Write wk for term weakening, twk for type-parameter weakening, arr(A,B) = pi(A,wk(B)), and fin for the recursive translation of finite TypeCode, with finite arrow translated to arr and finite All translated to all. Let

- D = S I I;
- Ω = D D;
- t = S K (K Ω), with application left-associated;
- p = app(app(atom(S),atom(K)),app(atom(K),atom(Ω)));
- q = atom(t);
- C = TypeCode.all(TypeCode.arrow(TypeCode.var(0),TypeCode.var(0)));
- A = fin(C) = all(arr(param(0),param(0)));
- ζ = zeroEnv, the all-zero valuation used for the empty telescope.

A is closed in both sorts and Form [] A. Both p and q are Scoped 0; neither uses raw markers zero/one. The exact inherited positive/negative inputs are:

1. Has [] p A.
2. For every η, eval(p,η) = t = eval(q,η).
3. FiniteDerives I C, so the target is inhabited in the smaller finite calculus.
4. No u and finite code B satisfy FiniteDerives u B and Conv t u. In particular, **for every B, ¬ FiniteDerives t B**, by reflexivity of Conv.

Items 1–4 are already established by P01NormalizationBoundary.new_finite_target, eval_p, target_inhabited and no_finite_source_representative. The present written proof uses these inherited theorems. It does not constitute a new Lean check of them.

## 2. Fixed polynomial completeness

Define the closed fixed-polynomial semantic completeness claim at this one type:

**For every polynomial r, if Scoped 0 r and, for every relational environment R, G A R ζ ζ (eval(r,ζ)) (eval(r,ζ)), then Has [] r A.**

Here R ranges over the actual P01R.REnv: two environments of arbitrary lawful source-Conv-saturated PERs plus a respectful Link at each type parameter. G is exactly the recursively defined heterogeneous predicate in AllPredicates.lean. This is already narrower than completeness at arbitrary contexts, dependent types or arbitrary semantic sections.

The counterexample q satisfies its premises but not its conclusion. A fortiori the usual converse of the heterogeneous fundamental theorem fails when it asks to type the same supplied polynomial. A unary-semantic version also fails because q has the inherited unary validity as well.

## 3. Whole atom replacement

Define a raw-label map h by **h(t) = K**, and **h(r) = r when r ≠ t**. This is a map on *whole atom labels only*. It does not recursively inspect or modify a proper raw subterm of another atom label. The fixed t is different from I, K and S, so h fixes each distinguished primitive constant.

Extend h to a polynomial map M by

- M(var(n)) = var(n);
- M(atom(r)) = atom(h(r));
- M(app(f,a)) = app(M(f),M(a)).

Extend M structurally to types, changing only the polynomials at identity endpoints, and pointwise to telescopes and finite lists of type images. It fixes param, bottom and raw, and commutes with all, pi and sigma.

**Replacement lemma.** For every Γ, B and r in the full unchanged syntax:

- Ctx Γ implies Ctx MΓ;
- Form Γ B implies Form MΓ MB;
- Has Γ r B implies Has MΓ M(r) MB.

No source operational claim about h is part of this lemma. In particular h need not preserve raw source application, Step, Red or Conv on arbitrary raw terms. This does not obstruct the proof because the typing rules access nonprimitive atom labels only through Raw admission or an unchanged finite certificate.

### 3.1 Syntactic commuting facts

All required equalities follow by structural induction on finite syntax:

1. M preserves polynomial free-variable tests and Scoped n. It preserves TyScoped n and telescope length.
2. M commutes with term renaming; more generally M(psub σ r) = psub (M ∘ σ) (M r). Thus it commutes with lifted substitution, wk, inst and motiveAt after mapping their arguments.
3. M commutes with type renaming, twk, twkTel, mixed term/type substitution, tsubst and tinst after mapping the corresponding images. M fixes fin(B) for every finite code B because that translation contains no polynomial endpoints.
4. M preserves Lookup, by its zero/succ constructors and the wk equality. M(theta Γ B x) = theta MΓ MB Mx.
5. freeZero(M r) = freeZero(r). The exact abstract operation branches only on this test and the polynomial constructor, using atom I/K/S. Because those constants are fixed, M(abstract r) = abstract(M r), including the whole-subterm K-priority branch. No abstraction-congruence or η principle is used.
6. M commutes with pairPoly, fstPoly, sndPoly and jPoly: their definitions use only app, their polynomial arguments, and atom I/K/S.
7. For finite type tables τ, M(typeImages τ n) = typeImages (map M τ) n; the Bottom default is fixed. Table length and finSupport are unchanged.
8. PolyConv r s implies PolyConv M(r) M(s), by induction on all seven conversion constructors: refl, symm, trans, app, I, K and S. The three computational constructors are preserved because M fixes their primitive atoms. The induction maps *every* intermediate of a transitivity proof. It needs no extraction of hidden provenance and imposes no extra intermediate-scope restriction.

### 3.2 Preservation of every rule

Perform simultaneous induction on Ctx/Form/Has evidence. The motives are the three statements of the replacement lemma.

**Contexts.** Nil remains nil. Ext uses the transformed context and formation premises.

**Formation.** Param, Bottom and Raw use transformed context evidence. All uses transformed context evidence and the transformed body formation, with M commuting with twkTel. Pi/Sigma use transformed domain and body formation. Identity uses the transformed domain formation and *both* transformed endpoint typings. Thus dependent types referring to the special atom do not escape the map.

**Variable.** Transform formation and Lookup; M fixes the displayed var node.

**I, K, S.** Transform every formation premise. The displayed source primitive is fixed, and M commutes with arr.

**Finite import, the decisive case.** A rule instance has source atom(r), an unchanged proof FiniteDerives r B, a finite table τ with finSupport(B) ≤ length(τ), formed table images, and formed result tsubst(typeImages τ)(fin B). Inherited item 4 excludes r = t. Therefore M(atom(r)) = atom(r). Reuse the same finite derivation, code B and support bound; use table map M τ and the transformed formation premises. Commuting fact 7 and the tsubst/fin facts identify the required result. No transformation of a FiniteDerives proof or of the raw structure inside r is needed.

**All introduction.** Transform all-type formation and the typing in twkTel Γ; the same polynomial M(r) appears in premise and conclusion.

**All elimination.** Transform all-type formation, replacement-type formation, explicit result formation and the polymorphic typing. The result agrees by M commuting with tinst. Open dependent replacement types are included.

**Raw atom.** Every replacement atom is permitted by the original rawAtom rule after transformed Raw formation, including when r = t and h(r) = K. No stronger arbitrary typed-to-Raw coercion is invoked.

**Raw application.** Transform Raw formation and both Raw typings, and apply rawApp to their mapped application.

**Pi introduction.** Transform the Pi formation and body typing in the extended telescope, use preserved scope, and use M(abstract b) = abstract(M b).

**Pi elimination.** Transform function and argument typing, Pi formation and explicit result formation. Use M commuting with inst.

**Sigma introduction.** Transform both element typings, Sigma formation and explicit instantiated-result formation. Use M commuting with pairPoly and inst.

**Sigma first projection.** Transform domain formation, Sigma formation and pair typing. Use the fstPoly equality.

**Sigma second projection.** Transform Sigma formation, its explicitly formed result and pair typing. Use the sndPoly/fstPoly/inst equalities.

**Identity introduction.** Transform identity formation, both endpoint typings and the full PolyConv proof. The proof polynomial atom I is fixed. Semantic PER equality is not an alternative premise of this constructor.

**Proof erasure.** Transform Raw formation, identity formation and proof typing, and reuse proofErase.

**J.** Transform domain formation, the motive formation over theta, identity formation, both explicitly formed motive instances, both endpoint typings, proof typing and base typing. The theta, motiveAt and jPoly equalities align every argument. Endpoint and proof coordinates are retained.

**Conversion.** Transform type formation, the original typing, the full PolyConv proof and the conclusion's scope proof. This is the only Has conversion constructor. It does not take raw source Conv, equality of evaluations or arbitrary semantic equality as a premise.

This exhausts the current rule population. No admitted semantic-equality rule defeats the replacement lemma. Adding such a rule would change the mathematical object being assessed.

## 4. Separation by a singleton conversion class

Assume Has [] q A. Since M[] = [], M(A) = A and M(q) = atom(K), the lemma gives **Has [] atom(K) A**.

Define the lawful singleton-class PER Pᵢ by

**Pᵢ.rel(x,y) iff Conv x I and Conv y I.**

Symmetry swaps the two conjuncts; transitivity keeps the first and last; raw saturation follows from symmetry/transitivity of Conv. Thus Pᵢ is one of the actual PERs quantified over in All, and Pᵢ.rel(I,I) holds.

Apply accepted unary soundness to the alleged K typing at the empty telescope, where E [] ρ ζ ζ holds for any ρ. The All predicate's universal unary-instance conjunct, instantiated at Pᵢ, yields

**F (arr(param(0),param(0))) (Pᵢ :: ρ) ζ K K.**

Since the body contains no term indices, this is exactly: for all x,y, Pᵢ.rel(x,y) implies Pᵢ.rel(K x,K y). Taking x = y = I gives **Conv (K I) I**.

But I and K I are distinct source normal forms. I has no rule successor. K I has only one argument, so the K root rule cannot fire, and neither I nor K has a contextual successor. Source normal-form uniqueness would imply K I = I, contradicting the disjoint Term constructors. Therefore no alleged K typing exists, and hence **¬ Has [] atom(t) A**.

RawPER alone would not establish this contradiction: K is a raw-conversion-respecting function and Raw → Raw is too weak. The singleton-class PER is essential to the test.

## 5. Semantic validity and consequences

Accepted Has [] p A and the heterogeneous fundamental theorem give, for every R,

**G A R ζ ζ (eval(p,ζ)) (eval(p,ζ))**,

because H [] R ζ ζ holds. Literal evaluation equality transfers exactly this proposition to q. The same reasoning gives its unary semantic validity for every parameter environment. No conversion of the polynomial is used.

Thus at one fixed closed formed finite type A there are closed p,q with:

1. Has [] p A;
2. eval(p,η) = eval(q,η) for every η;
3. q is universally heterogeneously and unarily valid at A;
4. ¬ Has [] q A.

This proves three exact consequences:

- **Fixed-polynomial semantic completeness is false**, even at A and the empty telescope. An unrestricted converse with the same polynomial therefore cannot hold in this calculus.
- **Typing is not invariant under literal evaluation equality.** Source term equality after evaluation is insufficient to transfer a P01AC certificate between arbitrary polynomial representations.
- **Universal closed atom-packing is not type-preserving.** The representation map Pack(r) = atom(eval(r,ζ)) on Scoped 0 polynomials sends the accepted p to q, which has no typing derivation at A. A frontend using this universal packing step cannot claim certificate preservation in unchanged P01AC. This is a representation transformation, not a reduction of source t.

## 6. A general necessary condition for opaque typing

The same preservation argument has a uniform form. This corollary concerns the same 18-rule calculus, not an extension of it.

For a raw source term a, write **NoFinite(a)** for the assertion that, for every finite TypeCode C, FiniteDerives a C is false. This hypothesis implies a ≠ I, a ≠ K and a ≠ S: each primitive has a finite typing certificate, for example with all of its displayed type arguments chosen to be Bottom.

For arbitrary raw b, let Mₐᵦ replace only the whole polynomial atom(a) by atom(b), fixing every other whole atom label, variables and the polynomial application structure, and extending structurally to types and telescopes as before. Under NoFinite(a), Mₐᵦ fixes I/K/S and preserves every rule by precisely the proof in Section 3. The finite-import case again reuses its original certificate because no imported source can equal a. No property of b, such as normalization or finite typability, is needed.

The exact type-fixity condition for a chosen b is **Mₐᵦ(A) = A**. A useful uniform sufficient condition is that A contain no occurrence of the whole atom(a) in any identity-endpoint polynomial. Formally, avoidance is true for polynomial variables, is r ≠ a at atom(r), and is conjunctive at application. For types it is true at param, Bottom and Raw; it propagates through All, Pi and Sigma; at identity(B,p,q) it requires avoidance for B, p and q. Raw subterms inside a different opaque label r are not inspected. Every type without identity-endpoint polynomials, including every fin(C), satisfies this condition for every a.

**Uniform opaque replacement.** If NoFinite(a), Form [] A, A satisfies this avoidance condition, and Has [] atom(a) A, then for every raw b:

**Has [] atom(b) A.**

Indeed, apply the same simultaneous preservation lemma for Mₐᵦ to the supplied derivation. The empty context and A are fixed, and its polynomial becomes atom(b).

Now assume A has even one semantic rejection: there exist a raw term b and an object environment ρ such that

**¬ F A ρ ζ b b.**

Every PER in ρ is lawful under the inherited PER definition, and ζ is the empty telescope's zero-padded valuation. Unary soundness forbids Has [] atom(b) A, because E [] ρ ζ ζ holds. Uniform opaque replacement therefore gives the contradiction:

**NoFinite(a) and Has [] atom(a) A cannot both hold.**

Equivalently, in ordinary classical mathematics, the following is a necessary-existence condition: if Form [] A, A avoids whole atom(a), some lawful interpretation rejects some b at A, and Has [] atom(a) A, then **there exists a finite TypeCode C such that FiniteDerives a C**.

The code C need not be A or a translation preimage of A. This condition is necessary, not sufficient, and is not an iff characterization of opaque typing. The classical reformulation supplies no algorithm for extracting a finite certificate from a Prop-valued Has proof. The primary uniform-replacement implication and its contradiction with a displayed rejection do not require this classical reformulation.

For the concrete identity-type result, a = S K (K Ω), A = All(α → α), and b = K; the singleton Conv-class PER of I supplies the rejection. For Raw, no such rejection exists: F raw ρ ζ b b is Conv b b for every b. Thus the corollary does not conflict with universal Raw-atom admission. At a type whose semantic interpretation happens to admit every raw term, this rejection-based necessary condition supplies no conclusion.

This uniform result constrains opaque-atom interfaces at term-independent types and, with the exact avoidance condition, some dependent types. It remains a statement about typing a prescribed polynomial atom(a). It does not constrain the existence of a different well-typed polynomial evaluating to a; the concrete p remains such a representation.

## 7. A finite representative modulo source conversion is insufficient

A second immediate corollary distinguishes direct finite typing from finite representability modulo raw source conversion. It uses the inherited discarded-loop term

**d = discard I Ω = (K I) Ω.**

Let d₁ = (K I) Ω₁ and d₂ = (K I) Ω₂, where Ω₁ and Ω₂ are the exact inherited intermediates in the three-step cycle Ω → Ω₁ → Ω₂ → Ω. The source reduction's right-context rule lifts those three steps to

**d → d₁ → d₂ → d.**

The retained three_cycle_not_SN theorem therefore proves that d is not strongly normalizing. This is the same Acc relation used by P01Candidates.SN: both it and OrthemologyV3.StronglyNormalising (defined in NormalisationAndNumerals.lean) unfold to Acc (fun u t => Step t u) t. P01Candidates.finite_SN consequently implies **NoFinite(d)**. This conclusion follows from an actual infinite-reduction obstruction and a universal finite-typing theorem, not from failure to find a derivation.

At the same time, the source K rule gives **d → I**, hence Red d I and Conv d I. I is normal and has the inherited finite certificate FiniteDerives I identityCode. These facts are consistent: d is weakly normalizing but not strongly normalizing, because full compatible reduction also permits the cycle inside its discarded argument. The retained IndependentBoundaryControls.discarded_identity_has_normal_reduct already records the normal-reduct fact. Neither that fact nor the non-strong-normalization obstruction is a new discovery here.

Take the same closed type A = fin(identityCode) = All(α → α). It has no identity-endpoint polynomials, and Section 4's singleton Conv-class PER of I rejects K at A. Section 6, applied with a=d, therefore gives

**¬ Has [] atom(d) A.**

In contrast, **Has [] atom(I) A** is the inherited P01AC.polyIdentity_has (defined in AllJoinedControls.lean) instance at the empty telescope, and FiniteDerives I identityCode holds. We have thus exhibited the same d and the matched target code with

- **∃ v, FiniteDerives v identityCode and Conv d v**, witnessed by v=I;
- **¬ Has [] atom(d) (fin(identityCode)).**

This refutes sufficiency of a finite representative modulo source Conv even when its finite type is exactly the target identityCode. It is stronger than merely showing that a representative exists at an unrelated finite type.

It also refutes unrestricted raw-source-conversion transport between opaque atoms: the inference from Has [] atom(v) A and Conv v u to Has [] atom(u) A fails for v=I and u=d. The conversion premise here is the inherited raw-source Conv, whose symmetry gives Conv I d from d → I. This is a failure of backward expansion or equivalence transport, **not** a counterexample to forward subject reduction. The construction does not show a typed source reducing to an untyped target.

The polynomial conversion rule remains sound and unchanged. In particular, the application polynomial

**r = app(app(atom(K),atom(I)),atom(Ω))**

is typed at A: polynomial K conversion gives PolyConv r atom(I); use its symmetry with the existing Has [] atom(I) A and the scope-zero check. Its evaluation is d in every environment. Thus this second witness also retains a well-typed representation with exactly the same raw meaning as the rejected opaque atom. No existence-of-some-representation impossibility follows.

This consequence belongs to the same whole-atom preservation argument. The earlier source-normalization and discarded-loop results remain inherited. BoundaryResults also contains an earlier discarded-marker counterexample for the different Derives and FiniteDerives judgments; that earlier result is not a proof of opaque-atom nonderivability in P01AC. No new Lean theorem or operational reduction rule is introduced by this written corollary.

## 8. Scope of the conclusion

The result does **not** refute existential representability or completeness up to choosing another polynomial. In the exhibited case, the same raw term t already has the well-typed representation p. It also does not refute PER-equivalent finite representability: the inherited boundary explicitly leaves that separate. No theorem about all semantic sections, all types or all reification formats is supplied.

Soundness, recursive All uniformity, strong diagonal, heterogeneous preservation, exact substitution and bounded legacy/nucleus comparisons remain intact. The witness uses rules already available in the old raw-index calculus; this note proves its stated nondeducibility in the current P01AC, without claiming to have completed a separate old-calculus replacement proof. The boundary is not caused by a new flaw in recursive All.

The accepted finite import rule remains useful and sound: it permits opaque atoms carrying actual FiniteDerives evidence and formed replacement tables. The excluded t has no such evidence. The result does not say that all application-shaped atoms are untypable, or that opacity itself is unsound.

In particular **Has [] q raw** follows immediately from rawAtom. The proved negative is only **¬ Has [] q A** at the specified polymorphic identity type; q is not untypable at every type. The semantic-validity claim used here is stated at the empty telescope's zero-padded valuations.

No new normalization theorem, universe construction, canonical semantic equality, operational compiler correctness, physical-bearer identity, actual-world warrant or philosophical conclusion is obtained. A new positive restricted-completeness programme would first have to fix its quotient/representation policy; the present counterexample does not select or warrant one.

## 9. Public evidence locators

The calculus is fixed by the public component **Dependent_All_Public_Source_v2_20261003.zip**, SHA-256 **a58e2f510e08d2e2447b15b617cdb85dd1c36a3f04441a75897781c2c8f544db**. Relevant modules are:

- **AllSyntax.lean:** the complete P01AC grammar, mutually inductive judgments, scope, finite image tables and substitution operations.
- **AllPredicates.lean:** unary F, heterogeneous G, zeroEnv and empty-telescope E/H.
- **AllSoundness.lean:** P01AC.fundamental and P01AC.unary_fundamental.
- **P01DependentFundamental.lean:** the exact seven-constructor P01DF.PolyConv relation.
- **P01Polynomials.lean:** polynomial opacity, literal evaluation, freeZero, abstract, pairPoly, fstPoly, sndPoly and jPoly.
- **FiniteBridge.lean:** the unchanged FiniteDerives judgment.
- **P01PER.lean:** the source-conversion-saturated PER structure.
- **P01Confluence.lean:** P01Source.normal_unique and finite_normal_form.
- **P01Candidates.lean:** the exact Acc-based SN predicate and finite_SN.
- **NormalisationAndNumerals.lean:** discard, the three explicit Ω steps, StronglyNormalising and three_cycle_not_SN.
- **AllJoinedControls.lean:** polyIdentity_has at the empty telescope.
- **BoundaryResults.lean:** the inherited discarded-marker results for the older judgments.

The inherited witness is fixed by **Polymorphic_Normalization_Boundary_Source_v1_20261003.zip**, SHA-256 **00b7ab12cab9f390437dcfb6d41b2e6c7bf911b64f348ab2954acbf7e75f9790**:

- **PolymorphicNormalizationBoundary.lean:** wrapper, t, p, new_finite_target, eval_p, target_inhabited, no_finite_source_representative and boundary_control.
- **IndependentBoundaryControls.lean:** matching_is_not_opaque, matching_and_opaque_evaluate and discarded_identity_has_normal_reduct. These earlier controls establish representation inequality and evaluation equality; the present replacement argument establishes the stronger identity-type nonderivability.

The delivered **Orthemology Eleventh Research Report v2**, 3 October 2026, SHA-256 **a399da9fd36a73d5203c1e76dc742d1743550127faf03bfe4bc83a5b972b8dfb**, explains the earlier results in “Dependent All over typed telescopes,” “The original twelve avenues after this investigation,” and “Polymorphic identity and the normalisation boundary.” Those inherited results retain their original scopes. No historical or literature-wide novelty claim is made for the present argument.
