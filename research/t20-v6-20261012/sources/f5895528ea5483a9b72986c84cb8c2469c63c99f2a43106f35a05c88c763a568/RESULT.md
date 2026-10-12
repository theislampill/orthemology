# Type-indexed family semantics: exact coherence tests and a surviving Henkin boundary

10 October 2026. The literal universal `HasE [] c3 (W originalQ)` and its negation remain OPEN. No whole-source countermodel or universal parametricity theorem is claimed.

## Result first

A naive replacement of the shared PER carrier by independent type-indexed families fails an actual-source coherence test, before dependent J is considered. A nontrivial restricted-family repair survives that test. A further source-typed observer imposes a real cross-instance restriction on that repair, but does not supply the original scalar-fusion bridge. Thus the unrestricted-family proposal has an exact failure, while the genuinely Henkin proposal remains an unconstructed candidate, not a refuted class.

Three small new Lean files were checked with Lean 4.19.0 and `--trust=0`, reusing existing objects. They are discriminating controls and mathematical obstructions, not another numerical proof-count campaign. No predecessor source, grammar, compiler endpoint, repository branch, or protected file was changed.

## 1. The erased re-abstraction cycle

Set `P = All Raw`. In the actual context `[P]`, all of the following are checked with the unchanged constructors:

- `constantAll_direct`: `var 0 : P` by the variable rule.
- `constantAll_at_raw`: `var 0 : Raw` by allElim at the formed type Raw.
- `constantAll_reabstract`: `var 0 : P` by allIntro from that instance.
- `same_endpoint_identity`: `I : Id_P(var 0,var 0)`, using the direct and re-abstraction endpoint typings in actual identityIntro.

The original and re-abstracted judgements are literally identical, including the polynomial. The type-weakened telescope is definitionally the same telescope here. No fresh term-level type abstraction or application was inserted.

Now test the PARTICULAR semantic contract that interprets All by a family, allElim by coordinate projection, allIntro by assembly of the interpreted body family, and the same source judgement independently of its typing derivation. A valuation `u : U → Raw` has direct denotation `u`. The other route has denotation `λX. u(Raw)`. Coherence therefore requires

`u = (λX. u(Raw))`.

`reabstract_coherent_iff` proves this is precisely constancy. `full_constant_families_incoherent` rejects the unrestricted Bool-indexed Bool-valued family `u(X)=X`.

This conclusion is conditional on the displayed compositional interpretation contract. It is NOT a theorem that arbitrary unary membership soundness has family-assembly operations, or that every sound interpretation uses one erased applicative carrier. A proposed semantics avoiding this contract must explicitly give its replacement interpretation of allIntro/allElim and substitution; it cannot cite ordinary annotated System F semantics without a coherence translation.

## 2. Restricted families survive the first control

`ConstantFamilies U R r` is the subset of families whose every coordinate equals their r-coordinate. `constantFamiliesEquiv` identifies it with R. The local interpretations of projection, constant-family introduction, and pointwise extensionality are coherent, and `constantFamilies_nontrivial` checks that two different Boolean values remain different.

This is deliberately a local repair, not a whole-HasE model. Its survival prevents the incorrect inference that the preceding control refutes all Henkin or type-indexed semantics.

## 3. An actual structured-carrier observer excludes a further naive repair

The new `StructuredObserver.lean` uses the unchanged Church type N and the actually formed source context

`Γ = [a:Raw, f:Raw, n:N]`.

For a fresh type parameter A, form

`C(A) = Sigma Raw (A → A)`.

The source seed is `(a,I)`. The source step sends a state s to `(f · fst(s), I)`, where the first-coordinate operation uses actual rawApp. This does not coerce any A endpoint or n:N into Raw. The only variable declared Raw are f and a; fst(s) is Raw by actual sigmaFst.

The unchanged source rules derive the actual polynomial

`observe = fst(n step seed) : Raw`.

They then derive `observe : All Raw` by allIntro and `observe : Raw` by allElim, without changing any polynomial. The source proof checks formation, the Church instantiation at C(A), both dependent Sigma introduction premises, the Pi introduction/scoping premise, both applications, and the projection. It permits arbitrary n supplied by the actual context, not only a closed numeral.

The theorem `structured_observer_uniform` makes the conditional semantic argument explicit: it requires a coherent All Raw result and the displayed body-assembly equations. It does not assume or prove a whole-source interpretation. Under that ordinary coherent family contract from section 1, the Raw observation of the n-component at C(A) must therefore be independent of the unused fresh parameter A. This is a concrete cross-instance constraint beyond merely requiring families at All Raw to be constant.

The falsification control uses the ACTUAL retained Raw term algebra. Set a=I and f=K K. `raw_zero_observation` proves that evaluating the literal source observer at the original Church numeral zero converts to I. `raw_one_observation` proves that its evaluation at the original Church numeral one converts to K. `raw_observations_distinct` excludes raw conversion of these observations using inherited confluence and the distinct normal forms I and K.

Consequently, an alleged family choosing zero-like iteration at one C(A) and one-like iteration at another C(B) fails this observer if its Raw interpretation preserves that distinction and it claims the coherent family/assembly contract. The two numeral controls are NOT presented as one nonparametric Church element, a source countermodel, or a proof about all candidate families. No finite two-element interpretation of the full Raw combinatory algebra is used.

Crucially, the probe compares structured carriers C(A). It does not compare `n_A f a` with `n_Raw`, with the original pair-state compiler, or with either missing graph projection. No all-rule naturality theorem follows.

## 4. Impredicative fullness has an independent diagonal obstruction

Let `D = All (α → Raw)`. `discriminator_form_empty`, `discriminator_self_instance`, and `discriminator_diagonal` check actual source formation and the legal source typing `x x : Raw` under `x:D`. Self-instantiation at D is consequently a real obligation of the unchanged grammar.

For a set-indexed family candidate, suppose a universe of codes U has carriers El(i), with code d for D, and that D denotes the FULL product

`El(d) ≃ Πi:U. (El(i) → R)`.

If R has two distinct elements, this is impossible. For any evaluation `ev : El(d) → El(d) → R`, choose a fixed-point-free flip of R and define `δ(x)=flip(ev(x)(x))`. No x can have `ev(x)=δ`. Full-product availability, however, permits installing any function at the d-coordinate, filling all other coordinates by a constant, and hence makes evaluation surjective. Contradiction.

`no_full_impredicative_product` proves the contradiction; `henkin_self_projection_proper` gives the sharper necessary Henkin boundary: for ANY set-family decoding at d, the exact diagonal function is outside the image of the self-coordinate projection. This does not forbid full Pi spaces by themselves; it forbids arbitrary coordinate completion of All-families at the self-instance. A valid Henkin interpretation must omit some such completions.

This is the familiar diagonal/Cantor-style impredicative-size obstruction, specialized to an actually formed source fragment. It is not a new field theorem, and the grammar does not demand full function spaces or full All products. Neither source inconsistency nor source noninhabitation is inferred.

## 5. Exact remaining construction burden

The viable question is therefore about restricted, coherent families. An actual separator must still supply an independent semantic construction with all of the following, rather than define admissibility by existence of the desired source proofs:

- A type-code/carrier interpretation closed under the ACTUAL impredicative finite type substitution. A predicative hierarchy that quantifies over earlier stages fails allElim at the current All type. Merely writing a product over all semantic types is not a construction.
- Admissible families closed under interpretations of actual allIntro proofs, respecting all source term/type substitution equations, while excluding the diagonal completions above.
- One well-defined meaning for raw Poly endpoints at each formed type, coherent across typing derivations, type renaming, term substitution, and conversion. The two erased-cycle controls are mandatory tests of any ordinary family implementation.
- Dependent Pi/Sigma membership, projections, and extensional equality, with actual piExt/allExt premises retained. The local constant-family equivalence alone does not establish these constructors.
- Identity realized by the required I representative and proof erasure into Raw. Actual J's two-coordinate dependent motive must transport coherently. Free independent proof generators are already refuted by the inherited literal-J control; that failed proposal was not retried.
- A semantic n:N satisfying ALL those restrictions, plus evaluation of the exact imported `originalQ`, `W`, and `c3` that falsifies the literal target. No such n is supplied here.

The present work neither proves that these requirements force every cross-type relation nor constructs a family satisfying them that violates scalar fusion. That is the precise unresolved point. The known whole full-PER model validates the target, and the known closed source-identity completeness remains intact; neither answers this Henkin question.

## Inherited-attempt check and verification

Before construction, this pass inspected the inherited failed strict-successor/strict-zero single-application models, the free-proof contextual-model failure, the Raw-endpoint motive boundary, the full-PER construction and review, the exact source continuation and graph assembly, and closed Church source-identity completeness. The new tests do not repeat those candidates. A broader inherited-source search also found `BoundaryResults.no_erased_full_sections`, which already establishes a generic erased/full-section obstruction (and distinguishes it from an insufficient singleton interface). That algebraic obstruction receives no new-result credit here. The additions are the exact HasE re-abstraction/identity-endpoint controls, the actual structured-carrier observer with Raw separation, and the explicit application of the classical self-index diagonal to a source-formed type.

`replay.py` checks the frozen syntax/object bindings listed in INPUTS.json and freshly compiles only the three new files. The original 83-module baseline is not rebuilt. Final positive modules contain no new axioms, admitted proofs, or unsafe/native evaluator shortcuts. Reported dependencies are confined to ordinary Lean `propext`, `Classical.choice`, and `Quot.sound` as recorded in validation/REPLAY.json. No independent review is claimed by this author packet.
