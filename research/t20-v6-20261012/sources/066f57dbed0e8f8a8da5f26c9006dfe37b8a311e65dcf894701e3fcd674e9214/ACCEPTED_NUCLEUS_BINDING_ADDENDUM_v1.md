# Binding the dependent-All design to the accepted typed nucleus

## Status and controlling records

This is an interface-reconciliation addendum to the immutable `DEPENDENT_ALL_DESIGN_v5.md`, SHA256 `f4eb382dc54e142b14d943affe8602b8dbb2f3097eaea8f6e630f6d182e83545`. It satisfies v5's requirement to reconcile against actual independent nucleus acceptance rather than an anticipated candidate. It does not implement dependent All, authorize implementation, or convert design admission into theorem acceptance.

The nucleus now has an actual independent bounded acceptance:

- `tranche11/reviews/typed-context-nucleus/REVIEW.md`: `6e1832ad33853ba245c46ef65e7eb560bfb79f76ea5c566b5488a1b223a856c5`.
- `tranche11/reviews/typed-context-nucleus/VERIFICATION.json`: `e9a883c382814585fe1c47188e5df7e63e321e04d5f7490e0d9908ddfc488720`, status `ACCEPTED_BOUNDED_TYPED_TELESCOPE_NUCLEUS`.
- `tranche11/reviews/typed-context-nucleus/SOURCE_IDENTITIES.json`: `729e8924409dde299ebb0a9a57e4d59ca3ba8162ae71e877fbaf108023883490`.
- Acceptance-bound `tranche11/research/typed-context-nucleus/CHECKED_SCOPE.md`: `a8dac2778a7e2bcc4014868679c2c6bba79807fba6d5c4f302b1cae495772f26`.

The acceptance report records separate source-only compilation of all 47 manifest modules and a transitive axiom/readback gate over 300 declarations. This addendum did not rerun compilation. It independently rehashed all 47 research source copies and all 47 review source copies against the acceptance source manifest; every copy matched. The exact read/hash checks are bound in `ACCEPTED_NUCLEUS_BINDING_v1.json`.

The candidate's older pending-review labels and v5's historical observations remain unchanged. Current acceptance derives from the independent records above, not those historical labels. The acceptance is automated source/kernel qualification, not human-specialist validation, canonical adoption, full avenue9/U11 closure, or acceptance of the proposed dependent-All extension.

## Unchanged observed interfaces

All five nucleus files observed in v5 are byte-identical to the independently accepted files: TypedSyntax, TypedPredicates, TypedLaws, TypedSoundness, and TypedStructural. Therefore no change is needed to the proposed recursive All grammar, the paired raw F/G construction, weakened-context introduction, conditional semantic mixed substitution, or unequal-valuation diagonal proof.

The accepted syntax still has Param/Bottom/AllFinite/Raw/Pi/Sigma/typed Id, with no genuine All binder or type-parameter substitution. Its F-then-G order still requires replacement by a structural pair for the proposed extension. Its Hereditary/FormSound/TermSound conclusions retain smaller formation results; these are conclusions of the mutual syntactic induction, not semantic premises of rules. Adding an All hereditary child at WΓ and finite-instance replacement formation subtrees remains new work, as specified in v5.

The translation of AllFinite(C) to recursively generated All(finRec(C)) remains necessary and is not literal type identity. The v5 finite-instance schema is still required to preserve literal atom(t); neither nucleus acceptance nor its legacy theorem adds an atom-application PolyConv bridge.

## Exact zero-padded substitution convention

The accepted TypedStructural and TypedRepresentation contracts are:

    images [] n = atom zero
    images (a :: σ) = cons a (images σ)
    subEnv σ η n = eval (images σ n) η
    subEnv [] η = zeroEnv
    subEnv (a :: σ) η = cons (eval a η) (subEnv σ η).

A finite TypedSub Δ Γ σ contains exactly Γ.length images. Each component is typed in Δ at its declaration substituted by the already supplied tail images. Its unused tail is constant atom zero, **not** Poly.var. This is necessary for D on finite contexts and for intrinsic Sub.tracks at every index, including indices beyond the source telescope.

The accepted preservation endpoints are literally:

    Form Γ A ⇒ Form Δ (subst (images σ) A),
    Has Γ p A ⇒ Has Δ (psub (images σ) p) (subst (images σ) A).

Composition maps each real list entry, with the accepted global equation

    images (σ.map (psub τ)) n = psub τ (images σ n).

It holds beyond the list because atom zero is unchanged by polynomial substitution. The accepted represented substitution uses exactly images σ as its code and subEnv σ as its map; it is not represented by a function with an identity tail.

Apply this convention to v5's contextual mixed substitutions. The term component is a finite list with zero padding; its type-image table is separately finite, binder-aware, and Bottom-default as specified in v5. The two padding conventions concern different syntactic sorts and must not be conflated.

V5's total-function M algebra can still use Poly.var for the raw identity law. However, a finite identity-context list agrees with Poly.var only on the source telescope's support. Do not claim global equality images(identityList n)=Poly.var. Its preservation/cancellation results for scoped polynomials and types follow by support extensionality. For valid zero-padded valuations, evaluation of that finite identity list yields the same valuation, including its zero tail. Thus the All elimination map WΓ→Γ has identity term action on all scoped syntax, not an unpadded global identity function. V5's phrase “declaration images are literally the original Γ declarations” is to be read as the resulting syntactic equality proved using their established scope.

Under a term binder, the lifted finite list is var0 followed by term-weakened old entries. Its unused tail remains atom zero, agreeing with pup(images σ) there as well. Under All, no term coordinate is added, so the list and its padding remain unchanged while replacement types are type-lifted. Both J coordinates use the corresponding two finite lifts. These refinements preserve v5's proposed mathematics and eliminate an invalid total-environment identity shortcut.

## Complete accepted legacy provenance contract

The accepted `P01TC.Legacy.Derivation : Poly → P01DF.Ty → Type` is a constructor-faithful retained tree. It includes every original old rule: raw, finite, I/K/S, allIntro, allElim, app, piIntro/piElim, sigmaIntro/sigmaSnd, identityIntro, J, and conv. Its exact forgetful operation is named

    Derivation.erase : Derivation p A → P01DF.Has p A.

It preserves both indices p and A. There is no reifier from an arbitrary Prop-valued Has proof and no claim that proof-irrelevant constructor history can be inspected.

The accepted predicate is

    Restricted : (n : Nat) → {p : Poly} → {A : P01DF.Ty}
                   → Derivation p A → P01TC.Ty → Prop.

It certifies the actual retained tree together with a translated type. Its constructors exclude allIntro and allElim at every depth; old All subtrees translate only through their entire finite embedding image. It bounds source typing syntax at the appropriate binder depth and carries type/motive translation certificates. Accepted Restricted.raw_embed preserves the literal polynomial in the n-entry all-Raw telescope. Restricted.object_agrees and Restricted.heterogeneous_agrees supply unary PER equality and heterogeneous agreement at pointwise-Conv-related valuations. RawContext is an internal syntactic Raw-access interface and can handle J's Id-typed proof coordinate using proofErase; it does not mean that Theta is literally all-Raw.

V5's broader comparison should reuse this retained Derivation interface and exact erase theorem, or provide an explicitly equal counterpart. Its new support/translation certificate must add recursive allIntro/allElim cases and recursive non-finite All type translation; it cannot rename the accepted Restricted predicate and pretend those cases already exist. Type weakening leaves an all-Raw telescope unchanged, while top type substitution uses formed dependent replacement images. The already accepted exclusion controls must remain valid for the old nucleus Restricted predicate. This separates preserved inherited credit from the new All comparison obligation.

## Exact scope census

For both the accepted comparison and v5's proposed broadened comparison, “whole-tree support” means support of:

- polynomials displayed by the retained typing-rule tree and its explicit constructor arguments;
- type/motive subexpressions, including displayed identity endpoints and All replacement types;
- displayed source and target endpoints of a typing-rule conversion premise;
- recursively retained typing premises, with the appropriate term-binder depth.

The unchanged `P01DF.PolyConv` certificate is Prop-valued. Its internal transitivity witnesses or intermediate proof-internal polynomials are not inspected, reified, or required to have recoverable provenance. Conversion soundness uses the unchanged accepted theorem for that certificate. In particular, a certificate may contain proof-internal witnesses outside the displayed support census without changing the typing-tree restriction. Do not add a new Type-valued conversion calculus or strengthen the proposed result to require inspection of all hidden PolyConv terms.

This clarifies v5's references to “every intermediate polynomial” as intermediate **typing-tree** syntax, not hidden conversion-proof history. The correction does not remove support checks from displayed conversion endpoints or from any retained typing premise. The complete displayed support condition still prevents a closed final conclusion from concealing an unscoped Raw typing premise.

## Scope and next gate

No mathematical capability, All rule, semantic clause, witness, or theorem target in v5 is weakened or enlarged. The added precision binds v5 to the actual accepted finite-substitution and retained-tree interfaces. The independent dependent-All challenger must assess this reconciliation; if it changes mathematical scope, a renewed mathematical gate is required before implementation.

Separate implementation approval remains required. No dependent-All source, compilation, canonical edit, publication, external contact, or new primary-source exposition was performed for this addendum. Nucleus acceptance supplies only its exact bounded results; the new universal All fundamental theorem, mixed substitution, finite-instance closure, full translated nucleus compatibility, broadened support-tree comparison, and D/self and Q/self witnesses remain unimplemented obligations.
