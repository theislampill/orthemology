# A bounded new pass after the fixed witness reduction

7 October 2026. The original literal HasE identity remains OPEN. This pass did not produce a target inhabitant or a whole-rule separating model. It tested a proof-theoretic inference from the now-verified fixed witness and two concrete nonparametric semantic elements with a single shared application operation. Each route failed at a specific obligation. These failures are not HasE noninhabitation.

The frozen source, manifests, prior receipts and prior mathematical notes were left unchanged. This directory contains new read-only research records only. No Lean, proof search, dependency build or scientific replay was run in this pass.

## Verified starting point

The supplied `hase-positive-research/README.md` and `FROZEN_SCALAR_HANDOFF.json` report independent verification of the four-way equivalence. The four new source files were read and their bytes compared with the handoff's digests:

- ScalarFusionCore.lean
- ScalarFusionReverse.lean
- ClosedProofCanonicalisation.lean
- LiteralScalarFusion.lean

The exact candidate manifest was also compared with the handoff. These five comparisons pass. The eighteen prior bound T16/candidate source pairs retain their recorded byte identities. `READ_COMPARISON.json` contains exact paths, digests and comparison scope. This pass does not replace independent kernel review with a hash comparison; it uses that review as the supplied starting result and checks which exact source was read.

In particular, the fixed statement is

`HasE [] c3 (W q)`,

where q is the original `redundantExpr.closed`, c3 is `abstract³ I`, and

`W(q) = Πn:N.∀α.Πf:α→α.Πa:α.Id_α(n f a,(q n) f a)`.

No change to the carrier, compiler, q, the source closing operation, or the new reduction theorem was proposed.

## Route one Fixed proof syntax does not give introduction inversion

The tempting inference was: c3 is a constant three-argument proof, so perhaps its only typing route is three introductions terminating in a directly convertible scalar identity. If that were valid, the already identified scalar nonconversion would settle the original target negatively.

The actual new source itself refutes that inference. `ScalarFusionCore.forward_fixed` starts with an arbitrary supplied identity derivation e at `Id_T(I,k)`. It applies the actual HasE.j to the motive M and obtains `jPoly c3 k e : W(k)`. `j_conversion` then uses two existing K contractions to erase the entire e subterm and obtain the exact constant c3 at W(k).

Consequently the raw normal form c3 does not retain the derivation annotation that justified its type. Inverting its outer K applications as if no J or conversion had intervened is invalid. Raw reduction of the proof does not produce a derivation using the introduction rule at the same exact target type.

In particular, replacing the J derivation by its base proof gives W(I), not W(k). Restoring W(k) is precisely where the supplied identity evidence was used. A proof-theoretic negative route would need a new theorem transforming complete HasE derivations while preserving their exact types, including impredicative instantiation, dependent J, and typed extensionality. The fixed witness supplies no such theorem or bound on proof annotations.

This assessment does not rely on reusing the old U-domain or inhabited-final-type controls. It follows directly from the checked fixed-witness construction under examination. No derivation-normalisation theorem was established, and no bounded search was treated as exhaustive.

## Route two Shared application with a strict successor iterator

This is a concrete model-candidate test, rather than independent numeral counts indexed by carrier. Work hypothetically in one applicative semantic domain D with:

- one shared application operation and the ordinary combinatory equations;
- an element ⊥ with ⊥·x=⊥ for all x;
- I distinct from ⊥;
- Raw interpreted by the equality PER on D;
- the ordinary extensional arrow PER;
- identity evidence for the reflexive Raw equality represented by I.

Only this attempted PER/Henkin family is assessed. No assertion is made that these hypotheses describe every possible HasE model.

Consider the single operation

`ν₁(f,a) = ⊥ if a=⊥, and f·a otherwise`.

This is the strict-in-seed successor iterator, often written informally `seq a (f a)`. Its definition does not inspect a carrier tag; the same f and a always receive the same output. Granting its availability as an element of D is already generous to the candidate. The failure below occurs even with that grant.

### It passes the unit probe and separates the desired endpoints as raw operations

ν₁(I,I)=I, so the checked generic unit-probe equation does not immediately reject it.

For the frozen pair-state compiler, z₀ is the ordinary pair of Church zeros. It is nonbottom: applying it to the first selector returns Church zero, which is nonbottom because applying zero to I,I returns I. Similarly Δ is nonbottom because Δ z₀ has nonbottom projections.

Thus ν₁(Δ,z₀)=Δ z₀, and `q ν₁ = snd(Δ z₀)` behaves as Church one. At carrier Raw, choose f=K I and a=⊥. Then

`ν₁(K I,⊥)=⊥`,

whereas

`(q ν₁)(K I)⊥ = I`.

If ν₁ were an admissible semantic N element, this would separate the original p and q, and would falsify W(q) at its Raw scalar instance. This is why the candidate was worth testing rather than dismissing it from the unit probe alone.

### It fails the actual Church arrow relation at a forced carrier

Set

`R = Id_Raw(I,I)`,

`U = R→Raw`,

`g = λr.r⊥`.

R's proof class is I. This is the standard identity interpretation and is also required, for faithful Raw equality, by the checked proof-coordinate/proofErase behaviour: every R proof is Raw-equal to I.

The carrier U is not an arbitrary new type invented for the test. It is formed from the actual Raw, identity and Pi constructors. Any proposed Henkin universe validating the corresponding allElim instances must include it.

At U, ⊥ and g are related. On the sole R class, both return ⊥: `⊥ I=⊥` and `g I=I⊥=⊥`. Yet g is globally distinct from ⊥ because `g(K I)=I`. Also I belongs to U and is not U-related to ⊥, since `I I=I≠⊥`.

The constant operation F=K I is a U→U endomorphism. Apply ν₁ to the same F and the two U-related inputs:

`ν₁(F,⊥)=⊥`,

`ν₁(F,g)=I`.

The outputs are not U-related. Thus ν₁ does not even preserve the unary extensional arrow relation required by N at U. It cannot be assigned membership in the intended interpretation of `∀α.(α→α)→α→α`.

No heterogeneous relational-parametricity axiom, full universe of all PERs, numerical induction, or graph-fusion law was used in this rejection. The small closure forced by the source's own R and U suffices.

## Route three Shared application with a strict zero iterator

The companion attempt changes the point at which definedness is inspected:

`ν₀(f,a)=⊥ if f=⊥, and a otherwise`.

It also has a single shared operation and satisfies ν₀(I,I)=I. Since Δ is nonbottom, q ν₀ behaves as Church zero. At Raw with f=⊥ and a=I, ν₀(f,a)=⊥ but `(q ν₀) f a=I`. Thus this candidate would also separate the literal target if it belonged to N.

Use the same forced carrier U and the same g above. Let F=⊥ and G=K g, regarded as endomorphisms of U. They are related at U→U: F sends every argument to ⊥, G sends every argument to g, and those values are U-related. Both are valid U endomorphisms. G is globally nonbottom because it returns the globally nonbottom g.

With the same U input a=I,

`ν₀(F,I)=⊥`,

`ν₀(G,I)=I`.

Again the outputs are not U-related. This time the failure is preservation of the related endomorphism argument, rather than the seed argument. Hence ν₀ also fails the Church type before full HasE soundness can even be attempted.

## Why the immediate repairs do not work

One might refine U's equality by a definedness tag so that ⊥ and g cease to be related. But their results at every R argument agree at Raw. The piExt schema requires function equality from precisely such pointwise identity evidence. In the corresponding semantic context, the pointwise proof can be the constant I proof. Refusing this function equality therefore invalidates the actual piExt rule. The parent theorem cannot be repaired by silently switching to an intensional arrow relation.

Alternatively, making Raw equality identify ⊥ and I removes the displayed separation of p and q. This observation only defeats the proposed separating observation; it does not exclude all coarser-Raw interpretations or every other separation strategy.

These tests do not exhaust all nonparametric semantic elements. They show that passing n I I=I and using one coherent erased application are necessary but not enough. The nearby higher-order identity carrier already enforces more uniformity. No general theorem that these obligations force full scalar fusion has been derived.

## Other model resources examined without an import

A bounded primary-source lookup considered *Algebraic Types in PER Models* by Hyland, Robinson and Rosolini, and *A Full Continuous Model of Polymorphism* by Barbanera and Berardi. Search-indexed primary text describes, respectively, standardness/initial-algebra results in selected PER models and a model whose polymorphic operations can depend on type input. Full-document retrieval failed in this pass. Neither paper is used as a premise of the arguments above or as a claimed HasE interpretation.

The first does not supply a separator merely by dropping the inherited F/G Link clause. The second does not automatically validate the source's erased allElim, dependent identity/proofErase, or piExt/allExt interface. Without a verified rule translation, either import would repeat the unresolved full-model obligation. No broader literature survey or dependency campaign was started.

Primary locations consulted:

- https://www.dpmms.cam.ac.uk/~jmeh1/Research/Oldpapers/hrr90.pdf
- https://iris.unito.it/handle/2318/2774
- https://citeseerx.ist.psu.edu/document?doi=94dd6d4782000bad4586cb7a4d92cb8d749eeed7&repid=rep1&type=pdf

## Result of this pass

The original target is still OPEN. The fixed-witness result remains useful and intact, but does not confer a syntax-directed decision procedure. The two new nonparametric element candidates were genuinely tested against the same erased application and forced higher-order carrier; both were rejected before being advertised as models.

No complete derivation transformation, admissible separating N element, or full HasE model has been obtained. The remaining burden is still either a faithful target derivation or a coherent whole-rule separator. These method-specific failures supply no noninhabitation theorem, no universal decision claim and no metaphysical or actual-world conclusion.
