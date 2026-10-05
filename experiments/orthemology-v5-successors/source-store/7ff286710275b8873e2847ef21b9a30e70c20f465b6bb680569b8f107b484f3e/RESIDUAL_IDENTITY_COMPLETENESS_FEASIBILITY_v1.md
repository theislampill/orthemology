# Residual identity completeness feasibility

## Disposition

**Semantic candidate established; syntactic nonderivability unresolved. Stop at that boundary.**

The hypothetical atom/application bridge does not turn the inherited source relation Conv into arbitrary PER equality. A closed typed identity between I and S K K is therefore a concrete candidate for testing whether semantic typing completeness still fails after that bridge. Its type is formed, and the polynomial atom(I) satisfies the full existing unary and heterogeneous interpretation at that type. The endpoint conversion required by direct identity introduction is impossible.

Those facts do **not** prove that atom(I) lacks a Has⁺ derivation at the candidate type. An argument covering all typing derivations, especially J and the elimination rules, is missing. The retained interfaces do not supply that argument. No incompleteness theorem, impossibility of all derivations, or new complete model is claimed here.

The accepted unchanged-calculus counterexample proof and the separately assessed hypothetical bridge are preserved. This is a source-preserved feasibility finding, with no implementation, experiment, canonical change or additional research programme.

## 1. Exact setting and proposition

Use the raw source Term, Conv, polynomial syntax, P01AC types, F/G predicates and finite code identityCode from the delivered dependent-All component. Let ζ = zeroEnv and set

- k = S K K, the inherited raw source identity-function witness;
- A = fin(identityCode) = all(arr(param(0),param(0)));
- p = atom(I);
- q = atom(k);
- B = identity(A,p,q);
- e = atom(I).

Here k is a raw source term; the notation does not identify its source normal form with I. All displayed polynomials are Scoped 0. A and B contain no free term variables; A is also closed in type parameters, so B is closed in both sorts.

Has⁺, Form⁺ and PolyConv⁺ mean exactly the previously assessed hypothetical system that adds the one atom/application conversion generator and otherwise preserves the P01AC rule shapes. Its semantic predicates remain the original F/G. No further equality reflection, function extensionality, identity rule or semantic admission is assumed.

The specific unresolved statement that would complete this fixed-polynomial counterexample is

**¬ Has⁺ [] e B.**

The stronger statement that B has no closed Has⁺ inhabitant is also not established. Neither statement is inferred merely from a missing identityIntro instance.

## 2. Formation and semantic validity are available

P01R.finite_polymorphic_I and P01R.finite_polymorphic_skk supply unchanged finite certificates for I and k at identityCode. The accepted P01AC.finite_import theorem, with Ctx.nil, yields

**Has [] p A** and **Has [] q A**.

P01AC.form_fin supplies Form [] A. The existing identity formation constructor then gives **Form [] B**, without requiring a proof of equality between its endpoints. Positive inclusion of old derivations into the hypothetical system gives the corresponding Form⁺ and endpoint Has⁺ judgments.

The inherited relational witness P01R.recursive_polymorphic_I_skk states that I and k are related by the recursive identity-code interpretation at every relational environment. At diagEnv ρ, its diagonal identity law and the accepted F_fin comparison give

**F A ρ ζ I k** for every lawful object environment ρ.

This statement is PER equality at A, not raw source Conv. Now unfold the actual identity predicate:

**F B ρ ζ u v** means **F A ρ ζ I k**, together with **Conv u I** and **Conv v I**.

Taking u=v=I proves

**F B ρ ζ I I** for every ρ.

Likewise G at an identity type requires the endpoint equality in each of the two endpoint object environments and the two Conv-to-I proof-witness clauses. It does not require raw Conv of I and k. Applying the same F fact at the two endpoint environments and using Conv reflexivity gives

**G B R ζ ζ I I** for every lawful relational environment R.

Since eval(e,ζ)=I, e meets the full semantic premises of the proposed fixed-polynomial completeness test at B. This conclusion does not rely on weakening heterogeneous validity to a unary-only surrogate.

These are inherited semantic ingredients assembled at an explicitly formed current type. The underlying I/SKK distinction and the failure of general identity-carrier projection were already present in the earlier source record; they are not newly discovered here.

## 3. What the bridge does and does not exclude

The inherited theorem P01Source.I_SKK_not_convertible gives **¬ Conv I k**. The exact hypothetical atom-conversion characterization gives

**PolyConv⁺ atom(I) atom(k) iff Conv I k**.

Consequently **¬ PolyConv⁺ p q**. Direct use of the hypothetical identityIntro constructor at B is therefore blocked, even though B is formed and both endpoints are typed. Adding the bridge has not inserted PER equality as an alternative identity-introduction premise.

This is a local rule obstruction only. Has⁺ also contains type and term eliminations, substitution instances expressed through finite derivations, J with dependent motives and both tracked coordinates, and conversion of the proof polynomial. A derivation whose conclusion has identity type need not end with identityIntro at those displayed endpoints. In particular, J may transport previously obtained identity information, and application or All elimination may expose an identity type as a result.

To rule out every route, one would need a valid invariant, model or normalization/canonicity argument for the full hypothetical mutual syntax. Merely listing the current identityIntro premise does not supply one.

The existing semantic model cannot yield a contradiction here: it positively admits e at B. Its identity proof-witness clause would make any semantically valid proof source Conv-equivalent to I, but that property of the **proof source** does not imply raw Conv of the **identity endpoints** I and k.

## 4. A tempting alternate interpretation fails the existing transport law

An unproved shortcut would redefine typed identity membership to require raw Conv of its endpoints while leaving all other F/G and context relations unchanged. That would reject B, but it is not already a sound alternate model for the full dependent calculus.

The obstruction is explicit. Consider the old formed context Γ=[A] and family

**T(x) = identity(A,var(0),atom(I)).**

The variable has type A because its term weakening is A itself, and the constant I is typed at A in that context by the inherited polymorphic-identity theorem. Thus this is an actual formed family. Fix ρ and let

**η = I :: ζ**, **ξ = k :: ζ**.

The old relation E Γ ρ η ξ holds, because its nonempty component is exactly F A ρ ζ I k, established above. The ordinary TypeLaws.transport requirement would demand invariance of the family's relation along these E-related valuations.

Under the proposed stronger identity interpretation, the proof source I would be admitted in the T fibre at η, since its endpoints are I and I. It would be rejected at ξ, since its endpoints are k and I and these are not raw-convertible. Both endpoints still have their A membership; the failure comes from the extra raw-Conv condition. Thus the unchanged E relation would relate two valuations across which the stronger identity fibre changes its truth value.

This violates the needed hereditary transport law. It blocks the naive change of the identity clause alone and is directly relevant to dependent Pi/Sigma/J soundness. It does not prove that every possible intensional model is impossible: a coherent different treatment of other type/context relations would be a new model requiring a full soundness proof. No such model is provided by this assessment.

## 5. Retained interfaces checked and the precise missing obligation

The relevant inherited interfaces do not close the nonderivability claim:

- **AllSoundness:** fundamental and unary_fundamental return the existing F/G relations. Their result at B is compatible with e, not contradictory.
- **P01AC.formed_identity_exact, in AllBoundaryResults.lean:** packages typed identity as the inherited IdPER, whose endpoint condition is equality in the selected carrier PER. It does not reflect that equality into raw Conv.
- **P01R.recursive_parametric_equality_not_raw_conversion, in P01ModelWitnesses.lean:** explicitly preserves the I/SKK PER-versus-source distinction.
- **P01DF.canonical_identity_admission, in P01CanonicalCarrierProjection.lean:** its Has and identity syntax belong to the older raw-index calculus. Its identity has raw endpoints without the arbitrary typed carrier A. This theorem cannot be applied to a P01AC Has⁺ derivation without a suitable all-rule translation. No such reverse translation is supplied.
- **P01DF.arbitrary_identity_forward_projection_fails:** already shows that general typed IdPER carriers need not project to the canonical raw-equality code, using I/SKK. Simply forgetting the relational semantics cannot provide the needed stronger model.
- **AllNucleus and AllLegacy comparisons:** their accepted directions translate their specified predecessor derivations into P01AC. They do not provide an inverse translation of all current or hypothetical identity derivations into a raw-equality system.
- **The whole-label replacement lemma:** it is unavailable in Has⁺ because the added bridge invalidates its generator-preservation step. Moreover the two distinguished source labels I and k here have actual finite typing evidence, so the old NoFinite premise would not apply even before that change.

A sufficient missing result would be an appropriately justified closed identity-reflection or identity-canonicity theorem covering all Has⁺ constructors and proving raw endpoint convertibility for this candidate. Alternatively, a new sound model that rejects B could establish the needed negative. Neither is among the inspected accepted interfaces, and neither has been proved in this bounded check. Naming either route is not a claim that its proposed general statement is true or that the work is routine.

The stopped outcome is therefore exact: **a formed closed type B and a fully semantically valid closed polynomial e are available; global Has⁺ nonderivability is not.** The candidate must not be presented as a post-bridge semantic-completeness counterexample unless that remaining all-rule obligation is separately resolved.

## 6. Sources and preservation

This assessment uses the unchanged **Dependent_All_Public_Source_v2_20261003.zip**, SHA-256 **a58e2f510e08d2e2447b15b617cdb85dd1c36a3f04441a75897781c2c8f544db**. Decisive source modules are AllSyntax, AllPredicates, AllSoundness, AllFiniteComparison, AllNucleusSyntax, AllJoinedControls, AllInheritedPositiveControls, AllBoundaryResults, P01ModelWitnesses, P01Confluence and P01CanonicalCarrierProjection.

The assessed hypothetical bridge remains fixed at SHA-256 **02f2ba85547a0798288ec5d307f06fa5b239b8cb9e0faa4b7c7a6ba303097bbe**. The unchanged-calculus counterexample proof remains fixed at SHA-256 **b99fb16058f99ce5db66dd7a02e7515ede5157a002a6e76fc29d0f1bd8d65236**. Neither artifact is modified or weakened by this stopped feasibility check.

Absence of a suitable reflection/canonicity theorem is a bounded retained-interface finding, not proof that no such theorem exists elsewhere. No implementation or new model construction is undertaken.
