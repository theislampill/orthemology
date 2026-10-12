# Independent review: structured-context Church uniformity

Date: 10 October 2026. Verdict: **PASS within the stated intermediate scope**. No mathematical or proof-premise defect found in the frozen addition. This is a separate review, not integration or an audit/T20 closure decision.

## Frozen target and reproducibility

The reviewed author manifest has SHA-256 `6ddbbc072966baf8c6eaeb1f04023430a0022734257804211d7c1b2a456f6ac6`.

- `StructuredContextUniformity.lean`: `36f2333919d27087ae172190ea02820b35149827ddc76e543aae5ce542ba4203`
- `StructuredContextControls.lean`: `8270747720fe25a7c57bf9f19bf0d7d07026988015badf20518cc4ffe5b0b502`

The complete author directory is copied byte-for-byte under `frozen/`, including historical author diagnostics and its final receipt. `REVIEW_INPUTS.json` pins all 17 frozen files and 168 distinct directly recorded predecessor paths. `replay.py` independently verifies these, the transitive author/source/receipt bindings, the Lean binary, and retained objects, and repeats all verified input hashes after compilation. It never runs the author's mutating replay script or writes into an author/predecessor directory.

Run `bash check.sh` from this review directory, in the supplied workspace. This is a retained-dependency replay, not a standalone rebuild archive. It uses the existing Lean 4.19.0 binary and recorded libraries, and freshly compiles only the two frozen author additions and the new independent review module with `--trust=0`. Four deliberately invalid modules must fail. The 83-module historical baseline is not rebuilt. The replay verifies 92 retained baseline objects, 12 predecessor addition objects (4 scalar, 3 structural, 3 closed-identity, 2 raw-context), and the inherited extractor/source bindings. Hash-check counts include repeated before/after checks rather than distinct dependencies.

## What is actually established

For any finite source telescope Γ whose entries satisfy the newly defined syntactic `Opaque` predicate, every actual `HasE Γ n N` yields one natural number k and an actual source derivation

`HasE Γ I (identity N n (inputNumeral k))`.

The endpoint remains the original open polynomial n. Context opacity is an inductive syntactic assumption; a semantic admissibility contract or the desired source identity is not smuggled into that assumption. `opaque_uniform_substitutions` puts the same k before every polynomial substitution, and `opaque_uniform_evaluation` puts a k before every valuation, iterator and seed. The review additionally proves one joint statement using the same k for source identity, all substitutions and all subsequent evaluations. These latter conclusions are conversion/evaluation claims, not typing preservation under arbitrary substitutions.

The separate `identity_of_observation` theorem has no Opaque premise, no original-grammar `Ctx` premise and no fixed-telescope premise. It requires both actual Church typings and the genuine generic-observation conversion. It therefore works in arbitrary actual `HasE` contexts while providing no observation conversion merely from typing.

## Polarity and semantic induction

The exact retained `FullPER.F` definition was inspected, including dependent Pi/Sigma environments, identity proof representatives and All quantification.

- `Rigid.raw` reflects conversion directly; Bottom is vacuous.
- `Rigid.identity B p q` uses only the two proof-representative conversions to I. It does not extract Raw conversion between p and q from their relation in B.
- `Rigid.all` instantiates the universal premise at one existing orbit PER, then invokes the body induction hypothesis at the shifted relation environment.
- `Opaque.pi` uses a Rigid domain and an Opaque codomain. Domain reflection plus function conversion gives application conversion, and the codomain induction hypothesis applies at the actual dependent environment `cons x η`.
- `Opaque.sigma` converts each projection from conversion of the complete representatives, applying the body hypothesis at the first-projection environment. No reverse projection reflection or pair eta principle is used.
- `Opaque.all` handles every PER. `Opaque.emptyPi` eliminates the empty domain and imposes no codomain restriction.

Both new semantic induction lemmas are kernel-checked without axioms. Neither predicate certifies formation. The independent module exhibits an Opaque type with an out-of-scope identity endpoint and proves that it is not formed in the empty context. It also exhibits a Rigid identity domain with related but Raw-nonconvertible carrier endpoints, checking the intended distinction between endpoint relation and proof-representative reflection. Bottom and a free parameter are independently shown not to be positive Opaque entries.

This is a sufficient syntactic fragment, not a characterization of every possible context where some uniformity theorem might hold.

## Finite telescope, source scope and generic observation

`FullPER.E [] ρ η ξ` requires both environments to be literally zero. The new telescope induction discharges that exact base case and transports tails of truncated environments in its step. It does not use an unrestricted generic valuation directly as an admissible finite environment.

The review proves, for arbitrary Γ, that `E Γ ρ η ξ` implies `η Γ.length = zero`, and consequently that the unrestricted environment `T.var` is never admissible in any finite Γ. It then checks the actual truncated bridge for every Opaque Γ. A rejection control confirms that reflexivity cannot fill the missing zero-tail equality even for `[Raw]`.

Source scoping is derived from the actual HasE derivation. Agreement on the first Γ.length coordinates justifies replacing an arbitrary valuation by its truncated version. The inherited whole-HasE fundamental theorem then gives Church standardness. Generic source reflection uses the shifted environment `j ↦ var (j+2)`, reserving indices 1 and 0 for the iterator and seed. A single k is chosen there, before arbitrary substitutions/evaluations; conversion is transported with both binders correctly lifted.

The review's escaping substitution replaces a genuinely used parameter-sensitive coordinate by `var 100`. Its observation still has the same count, but the source endpoint is independently proved untypable in the original singleton context. This prevents reading arbitrary-substitution conversion as a general HasE substitution theorem.

## Complete source extensionality audit

The unchanged `HasE.allExt` constructor has eleven explicit premises. All are supplied in `identity_of_observation` (author lines 186–201):

1. Body formation in `twkTel Γ`: `formBody hΔ`.
2. All-type formation in Γ: `formN hΓ`.
3. Typing of p at N in Γ: the original hp.
4. Typing of q at N in Γ: the original hq.
5. Body identity formation in `twkTel Γ`: identity formation from the two type-weakened endpoint typings, eliminated to NBody there.
6. One body identity proof in `twkTel Γ`: `body_identity_of_observation hΔ hp' hq' hc`.
7. Result identity formation in Γ: identity formation from hp and hq.
8. Source scope of p: extracted from hp.
9. Source scope of q: extracted from hq.
10. Scope of the witness I: trivial for an atom.
11. Term scope of NBody: all its type components are parameter-only, with no term-variable endpoints.

Here `hΓ : CtxE Γ` is recovered from actual endpoint formation, `hΔ` comes from actual context type weakening, and hp'/hq' come from `Structural.has_twk`. The simplification is `twk N = N`, because N is type-closed; it is not `twkTel Γ = Γ`. Type weakening does not rename the term polynomial, so hc is still exactly the needed observation conversion.

The two `piExt` steps were also checked against all fourteen original premises each. At the inner step the domain and codomain are A; at the outer they are End. Every domain, codomain, Pi type, observation identity, dependent family, family proof and result identity is explicitly formed. The family witness is `abstract I` typed using `piIntro`; endpoint and witness scopes are supplied; the domain/codomain term-scoping obligations are discharged. The starting observation identity uses the actual hp2/hq2 typings and the supplied conversion hc, never conversion alone as typing.

An independent rejection control fails when an unweakened parameter-sensitive context is used where allExt needs `twkTel Γ`. Thus the old shortcut cannot silently pass for the review's discriminating context.

## Discriminating positive and negative controls

The frozen controls already establish that `[Raw→Raw, Sigma Raw Raw, Raw]` is formed, use typed application and a Sigma projection to construct a real open Raw expression, and produce the stated source identity for its erased Church-I endpoint.

The review strengthens the parameter-sensitive example:

- Its whole singleton telescope is proved unequal to its type weakening.
- The hypothesis at `Pi (Id_(A→A) I I) Raw` is actually applied to a correctly typed identity proof I.
- For every k, applying a typed K/numeral combination to that Raw expression gives a real open Church endpoint, its observation count k, and its actual source identity to numeral k.

The higher-order semantic countercontrol is genuine: `u = var 1` and `v = S (K (var 1)) I` are related at Raw→Raw because applications convert pointwise. They are distinct Raw normal forms and hence are not Raw-convertible. A generic variable at `(Raw→Raw)→Raw` would require conversion of the distinct normal forms `g u` and `g v`, which normal-form uniqueness rules out. This justifies the frozen `¬ Rigid RawEnd`, generic nonadmissibility, and `¬ Opaque Higher` theorems.

It does not show Higher is uninhabited. The independent module proves its original source context formed, types its source hypothesis, and constructs the closed inhabitant `K I : Higher`. The four expected elaboration failures discriminate missing observation evidence, positive/negative polarity confusion, omitted zero tail, and the unweakened allExt body context. They are rejection tests, not substitutes for mathematical negation proofs.

The general helper is separately instantiated in the non-Opaque context `[N]` for a reflexive observation identity. The review also freshly checks the stronger prior boundary argument: for every k and every witness r, no `HasE [N] r (identity N (var 0) (inputNumeral k))` exists. Interpreting the free Church variable as numeral k+1 and observing through the orbit PER contradicts iteration injectivity. Thus arbitrary-context numeral canonicity is false, while arbitrary-context observation-to-identity is valid with its actual premise.

## Trust and remaining scope

Fresh successful modules have no warnings, errors or sorryAx; lexical admission/unsafe/native-evaluator escape checks pass. Reported theorem dependencies are contained in `propext`, `Quot.sound`, and `Classical.choice`; the two fragment-semantic induction lemmas require none. Retained dependencies are verified and reused, not newly reproved by this review.

Both original arbitrary-carrier graph projection bridges remain absent. No uniform numeral count for a free Church hypothesis is obtained. Neither `HasE [] c3 (W originalQ)` nor its negation is proved: both remain **OPEN**. The refutation of arbitrary-context numeral canonicity and the higher-order generic-admissibility counterexample must not be presented as a refutation of that original universal judgment.

No protected source edit, source-grammar replacement, conversion-rule change, integration, T20 closure, T21 work, executable extraction claim or field-level novelty claim is made.
