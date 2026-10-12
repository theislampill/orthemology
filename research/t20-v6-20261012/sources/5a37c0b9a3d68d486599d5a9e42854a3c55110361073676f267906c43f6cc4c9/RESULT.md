# Uniform Church source identity under opaque Raw hypotheses

Status: isolated constructive extension; no integration or T20/#9 closure.

## New checked result

For every finite telescope Γ whose entries are literally the unchanged source Raw type, and every actual derivation `HasE Γ n N`, there is a finite count k and an actual source derivation

`HasE Γ I (Id_N n (inputNumeral k))`.

The original source polynomial n remains the endpoint, including any free Raw variables. This is one open-context identity, not merely an identity for each chosen closed instantiation. `all_raw_canonicity` states the result for any all-Raw list; `raw_canonicity` uses its canonical representation `rawTel m`.

`raw_uniform_substitutions` proves more precise uniformity: the same k supports that source identity and, for every source-polynomial substitution σ, the generic two-argument observation of `psub σ n` converts by the original `PolyConvPlus` to `iterationPoly k`. `raw_uniform_evaluation` places one k before all open-term valuations η and arguments f,a. Thus opaque Raw inputs cannot change the observed iteration count in this grammar. No interpretation about actual cognitive input or metaphysical information follows.

## Interface correction and source bridge

The suggested unbounded generic valuation was not directly admissible: FullPER's empty-context contract requires zeroEnv, so the tail beyond the finite telescope must be zero. `truncate_admissible` proves the exact finite environment obligation. `interp_agree` then uses the actual derivation's scoping theorem to recover the full symbolic valuation.

Existing whole-HasE soundness supplies Church membership. Existing open-term standardness supplies a count at a symbolic valuation shifted by two, reserving source indices 1 and 0 for f and a. Existing generic conversion reflection converts that compatible-open-SKI proof into actual source `PolyConvPlus`, preserving packed atoms through the existing packing bridge.

The source identity is separately assembled from actual HasE typing and extensionality: structural weakening gives the once- and twice-applied endpoints in their extended contexts; conversion gives the leaf identity; two piExt rules and one allExt produce the open identity at N. Every formation, scope, typing and family premise of the original constructors is retained. The all-Raw context is literally fixed by type-parameter weakening.

## Controls and boundary

- `opaqueInput = (K I) rawVariable` contains a genuine free Raw coordinate and has a checked source identity to numeral 1. Replacing the erased coordinate by any polynomial still converts to I; this asserts no strong-normalization property of the replacement.
- A bare variable in `[Raw]` cannot have type N.
- A bare variable in `[N]` does have type N but its symbolic observation has no numeral count. Hence the corresponding arbitrary-context reflection theorem is false. The Raw restriction cannot be dropped.
- The reflected observation count is unique, via the inherited open-term confluence/normal-form theorem.

## Inherited versus new

The full-PER model, open-term standardness, generic conversion reflection, complete-development confluence, original grammar and structural weakening are inherited. The finite Raw environment bridge, generic-context source identity assembly, all-Raw canonicity and uniform Raw-substitution conclusion are new additions here. The predecessor's closed canonicity theorem is used only for helper lemmas and controls; it is not misreported as having already covered arbitrary contexts.

## Scope limits

This is typed Church canonicity under opaque Raw hypotheses, not a completeness theorem for arbitrary types or contexts. It does not prove raw conversion of n itself to a numeral. It does not decide whether arbitrary polynomials inhabit N, prove general HasE substitution admissibility, or claim that an arbitrary substituted polynomial has a typing merely because its observations convert. The source identity already exists under the whole Raw telescope; arbitrary subsequent substitutions are explicitly certified at the observation-conversion level. It neither proves nor refutes `HasE [] c3 (W q)` and does not introduce an internal n:N scalar proof.

## Verification

`python3 replay.py` verifies all pinned predecessor sources/manifests/receipts, Lean 4.19.0, 92 baseline objects, four scalar objects, three structural objects, three closed-identity objects and the frozen extractor object. It freshly compiles only the two new modules with `--trust=0` into a new output directory. No baseline rebuild or predecessor mutation is performed.

The dependency reports contain only propext, Classical.choice and Quot.sound. There are no new axioms, admitted proofs, native-evaluator proof escapes or altered source grammars.
