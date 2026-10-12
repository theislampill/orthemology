# Independent review: actual closed Church identity completeness

10 October 2026.

## Disposition

PASS for the frozen bounded addition. No mathematical or executable blocker remains.

For an arbitrary supplied actual `HasE [] n N`, the new construction derives actual source `HasE [] I (Id_N n (inputNumeral k))` at its generic-open count. For two supplied actual closed Church typings, existence of any source identity witness, canonical witness I, equality of the computably extracted counts, and the unchanged inherited `F N` relation at any fixed type environment are equivalent.

This is genuine source-identity completeness on the promised closed Church input domain. It does not decide membership of arbitrary untyped polynomials, establish completeness at arbitrary types or contexts, prove raw conversion to a numeral, supply the internal universal scalar-fusion judgment, or add a field-level theorem. The universal bound-variable judgment and its negation remain outside this result.

## Frozen inputs and independent execution

The reviewed author identity manifest is `b6e50d551371ecd2b52bc994766274849a19e4b8150c982aaa90eaca139ec6b3`; the structural manifest is `29661fe1d0e20339bfb33e26633e06f0f2bf679dd42418ac5c15adcb0c16715f`. The predecessor complete-development review manifest was verified against the independently supplied digest `c6a199702e0df3ade78b2d84b38dba59f48a2faf2ad621ff84cfbfbd28bdb1bd`.

All six frozen author modules were copied byte-for-byte into this separate review directory and compiled into initially empty reviewer output using Lean 4.19.0 with `--trust=0`. Three additional reviewer modules also passed. The import path uses the independently reviewed closed-scalar and complete-development objects, rather than the author's extractor validation object. The source hash for that extractor is identical to the reviewed source.

The input check rehashes 593 bindings, including predecessor manifest contents, accepted source/object/log bindings, the Lean compiler, 92 inherited main objects, the original 83 pinned source modules, structural and identity manifests, author pins, and the six reviewer source copies. No baseline module was rebuilt. Third-party libraries are reused and the compiler binary is hash-checked, not bootstrap-verified. This is a bounded replay with explicit prerequisite paths, not a universally standalone build.

## Actual structural port

The source and kernel declaration audits confirm the unchanged mutual grammar: two CtxE constructors, seven FormE constructors, and twenty HasE constructors. Both type-parameter renaming and dependent term renaming explicitly cover the actual grammar, including finite imported derivations, universal introduction/elimination, raw terms, Pi and Sigma, identity introduction/erasure, J, conversion, piExt, and allExt.

The key details checked are:

- Type-parameter renaming goes under universal binders using `liftRen`; the term telescope is correspondingly `trenameTel`-renamed. HasE's source polynomial stays unchanged.
- Term renaming uses the actual dependent `Renaming` lookup relation and scoped target context. Pi/Sigma binders use lifted renaming. Universal binders use the type-weakened context and `Renaming.twk`.
- The finite import branch transforms every type image and retains the same original `FiniteDerives` proof. It does not extend finite strong normalization to HasE.
- J builds the exact renamed `theta` context, shifts the original endpoint correctly, and transports both motive specializations and all endpoint/proof typings.
- The piExt branch transports both endpoint typings, the body identity, the Pi family, its proof, the target identity formation, all three term-scope premises, and both type-scope premises. The allExt branch transports the body under the type-weakened telescope and retains every analogous premise.
- Polynomial substitution preserves all eight actual PolyConvPlus constructors, including the packed-atom/application bridge. This is used by identity introduction and conversion without changing the source conversion relation.

`Structural.has_closed` is obtained from the empty-source identity renaming into an arbitrary well-formed actual CtxE telescope, followed by the exact identity-substitution equalities. Its conclusion retains the original polynomial and original type literally. It is not an inference from old Has weakening. A checked transitive declaration audit excludes old `P01AC.has_rename`, old `P01AC.form_rename`, `BooleanPrimitive.closed_has`, unary semantic soundness, full-PER soundness, and generic standardness from this structural theorem. Its only axioms are `propext` and `Quot.sound`.

## Source identity construction and necessity

`identity_of_observation` works at the unchanged original closed endpoints p and q. The fully applied scalar observations are typed in `[A, End]`. Conversion at those observations gives the leaf identity. Once-applied endpoint typings in `[End]` then support the inner Pi extensionality step; the original closed N typings support the outer Pi step after universal elimination. Finally universal extensionality returns identity at N.

The direct proof expression was checked to contain exactly two uses of actual HasE.piExt and one use of actual HasE.allExt. The shifts of p, q, and their once-applied forms are justified by their supplied closed scope, not silently erased for arbitrary open inputs. The A, End, NBody and N formation premises and all term/type scoping premises are present. Type-parameter universality is handled under the actual empty type-weakened telescope.

The final `canonicity_at_count` and two-endpoint equivalence discharge the once-applied lifting premise using the new actual `Structural.closed_church_weaken`. The earlier explicitly conditional and old-Has lemmas remain valid bounded helpers; the new final theorem no longer has the lifting hypothesis. Literal bracket numerals are related to the generic observation by the inherited abstraction semantics plus the already reviewed literal source reflection bridge.

The necessary direction is independently sound: an arbitrary actual witness r yields the unchanged inherited endpoint relation through `ExtensionalRepair.unary_fundamental`. `observation_uniform` evaluates the two finite source observation conversions at arbitrary raw f and a, using closed evaluation invariance. Inherited `IdentityComplexity.related_same_index` then separates their counts through its raw marker test. The dependency audit verifies those two inherited theorems and excludes the positive identity construction, new closed weakening, and effective extractor from this necessary direction. Thus a negative equality result rules out every source witness, not only I.

The semantic equivalence in EffectiveChurchIdentity is specifically at unchanged inherited F, for any supplied fixed rho. It is not an assertion that arbitrary full-PER semantic validity can be reflected into source syntax at every type.

## Effective decision and discriminating controls

Both decision definitions branch on equality of the actual computable `extractIteration` values. Their proof obligations reuse the proved equivalences. The transitive dependency audit confirms executable Nat.find and the reviewed iteration readback. The ordinary proof dependencies include `Classical.choice`, `propext`, and `Quot.sound`; no admitted proof or unexpected axiom is present. Proof arguments are erased from runtime computation; the reviewer also proves that replacing a supplied typing proof with another proof of the same judgment leaves the extracted count unchanged.

The author supplies five executable guards, a theorem excluding every witness between numeral 2 and numeral 3, and the existing I/SKK raw-nonconversion separation. The reviewer adds six executable guards and the following kernel-checked controls:

1. The exact nonliteral source endpoints `K (inputNumeral 2) Omega` and a packed atom containing the evaluated numeral 2 have actual source identity. The former is not strongly normalizing, both in the original raw relation and in the exact open Step already checked by the predecessor. This uses the same supplied HasE typing; no typing of Omega is presumed.
2. Replacing the packed endpoint with count 3 excludes every identity witness. Runtime decisions return positive for the count-2 pair and negative for the count-2/count-3 pair, for both canonical identity and witness existence. Executed count readback returns 2, 2, 3.
3. An explicit proof polynomial `K I Omega`, syntactically different from I, inhabits the positive identity. The theorem relating existential and canonical witnesses is checked for arbitrary supplied closed endpoints.
4. The actual structural theorem weakens extensional identity proofs, the noncanonical witness, and the non-SN source input into a telescope whose formation itself consumes the I/SKK piExt/allExt identity. Type-parameter renaming and ordinary term weakening are also checked on that actual extensional proof.
5. An additional Church input is built by actual HasE.J using the extensional I/SKK proof and a constant Church motive. Its source polynomial is `jPoly (padded 2) SKK I`. The declaration audit checks one direct J use and dependence on actual piExt/allExt. Its exact typing derivation, closed lift, identity to numeral 2, extracted count 2, positive decision against packed2, and negative existential decision against packed3 all pass. This exercises an input derivation using the new grammar rather than merely supplying an old-Has embedding at the top level. It does not claim no alternate old-Has derivation of that polynomial exists.
6. The raw-nonconversion boundary is reused without reproving the baseline: literal I and packed literal SKK have actual typed source identity at N, but no actual PolyConvPlus conversion between the endpoints. The reviewer packages this with an existential witness. Consequently none of these canonicity claims can be read as raw endpoint conversion.

## Findings and scope

No author proof change was requested. A stale file-header comment describing lifting as still outstanding was corrected before the author froze the package; final signatures and documentation agree. A reviewer-only use of a nonexistent Lean environment helper was corrected to the supported optional lookup API; the final dependency audit passes and no failed output is accepted or imported.

The accepted evidence has zero-exit trust-zero replays, no warnings, no sorryAx, no native-decide shortcut, and no axiom beyond the documented standard set. The evidence receipt binds the exact final sources, objects, logs, input verification, and author manifests. No protected repository files were changed, and no publication, integration, or programme closure was performed.

Replay in the same prerequisite workspace: `python3 hase-closed-church-completeness-review-20261010/run_review.py`. It verifies the pinned inputs and replays only the nine new review modules.
