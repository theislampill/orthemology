# One literal Sigma/Pi cross-typing discriminator

10 October 2026. Separate continuation after the frozen fixed-carrier core.

## Result

The stronger test succeeds with the unchanged source encodings. For any original-source formed carrier B and source context providing n:N, a:B, b:B, define

- Product(B) = Sigma B (wk B)
- Selector(B) = B → B → B
- ChurchPair(B) = Selector(B) → B
- seed = pairPoly a a
- step = K (pairPoly b b)
- observe = fstPoly (n step seed).

The SAME pairPoly polynomial has both Product(B) and ChurchPair(B) typings. This is verified directly from its existing SKI encoding, using actual typed I/K/S and Pi application, rather than defining a different Church-pair polynomial or postulating an isomorphism. The two carrier syntaxes have distinct outer constructors, Sigma versus Pi.

The SAME step has the endomap type at both carriers. Church n can therefore be instantiated at either actually formed carrier. For Product(B), the final source rule is sigmaFst. For ChurchPair(B), it is Pi application to typed K:Selector(B). The source definition of fstPoly is literally application to K, so both routes derive precisely the same judgment Γ ⊢ observe:B, including the same polynomial.

`same_endpoint_identity` supplies the two different endpoint derivations to actual HasE.identityIntro, with reflexive source conversion. `probe_same_endpoint` checks a concrete source context [a:param 0,b:param 0,n:N]. There are no Raw declarations in this probe.

## Exact 0/1 controls

The original inputNumeral 0 and 1 give exact open source PolyConv

- observe(0,a,b) ≃ a
- observe(1,a,b) ≃ b.

`zero_source_identity` and `one_source_identity` include all actual endpoint typings and produce the corresponding HasE identities at B. The first uses the Sigma typing; the second uses the Church-pair typing. The constant update is source-typed K applied to a source-typed pair; no arbitrary full endomap-space assumption is used to construct this step.

## What it excludes

Consider a candidate type-indexed interpretation whose values at this fixed environment are conventional products/functions (or another representation that satisfies the same displayed computations on the supplied elements). Let D interpret B, and let ns and nc be the two coordinate operations claimed for one admitted N value, at Product(B) and ChurchPair(B), respectively.

The rule-directed observations are

- Sigma: first(ns (constant (b,b)) (a,a))
- Church: nc (constant (λk. k b b)) (λk. k a a) (λx y. x).

The contract must explain the interpretations of the actual pairPoly and K/S/I and the corresponding Pi/Sigma rules, so these equations hold for this particular source polynomial. If it also supplies derivation independence for this exact judgment, the two displayed values must coincide. With a≠b in D, zero-like ns and one-like nc are impossible; `no_shape_split` proves this. `no_reverse_shape_split` proves the reverse case.

Equivalently, a semantics can supply equality-valued soundness of the specific `same_endpoint_identity` derivation, interpreting its endpoints according to the two supplied endpoint derivations. That specific identity-soundness contract entails equality of these two values. This is an alternative sufficient contract, not an assertion that every unary membership interpretation exposes derivation-indexed endpoint values or equality-valued identity.

Thus the simple proposed family “zero on outer Pi, one on outer Sigma” fails this exact cross-typing test, although it could evade the fresh-phantom-parameter observer by staying constant across all Sigma-shaped instances. The reversed split fails too. Matching zero/zero and one/one observations survive, as the explicit controls verify. The Bool-valued local separating control can coexist with a subsingleton Unit designated Raw; it is not claimed to be a whole-source model.

## Boundaries

The semantic rejection is conditional on the displayed compositional observation equations and exact judgment coherence (or the precisely described identity-soundness alternative). The Lean theorem does not construct an interpretation of the whole grammar or derive these contracts from mere unary typing soundness. The set-level theorem uses ordinary product/function spaces to display these particular operations; an alternative Henkin encoding has to exhibit the corresponding admitted elements and interpretation equations, rather than silently inherit a full-function-space model.

No equality between the two carrier sets is asserted. The leverage is the literal shared polynomial and typing judgment. This provides one source-anchored cross-instance equality, not arbitrary isomorphism naturality, arbitrary graph preservation, all-rule parametricity, either original missing graph projection, scalar fusion, the literal universal W, or source noninhabitation. No such frontier is closed.

The original-source input hypotheses are P01AC.Has, with the resulting identities included into HasE. A general structural-preservation theorem for arbitrary HasE proofs is not assumed.

## Prior work and verification

The predecessor already provided open poly_beta/pair_first and generic conditional family arguments. Those are reused. A bounded search of existing hase continuation Lean modules found no earlier ChurchPair cross-typing test; this is not a comprehensive literature search or a field-novelty claim.

Run `python hase-cross-typing-observer-20261010/replay.py` to verify bound retained inputs and compile only CrossTypedObserver.lean, under Lean 4.19.0 `--trust=0`, into a fresh directory. The frozen core source and objects are read-only dependencies. The 83-module baseline is not rebuilt. The fresh receipt is validation/REPLAY.json, status PASS. Printed axiom dependencies are limited to propext, Classical.choice, and Quot.sound. No new axiom, admission, unsafe implementation, or native evaluator shortcut is present.

Source SHA-256: 10051b9df50fce7fef173bbe1cffe111cdc70529a29386753b8c872bf4789ba8.
Fresh object SHA-256: c3b3addcf23fb3e8b2d6885cf9f3b980dbf793a650125cc914f7c8cd1e46e5ac.

This author packet does not claim independent review. No protected edits, integration, T20 closure, or external publication occurred.
