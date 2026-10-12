# A coherent whole-HasE model extending the open-term full-PER reduct

10 October 2026. **The full model extension now exists and its soundness for all twenty actual HasE rules is Lean checked. The literal source judgement `HasE [] c3 (W q)` and its negation remain OPEN.**

## Result first

The previous open-term standardness and imported-compiler results applied to a reduct, with the existence of a sound whole-HasE extension left conditional. This package discharges that condition for one explicitly constructed interpretation.

`FullPER.lean` imports the unchanged original `Ty`, `Poly`, `CtxE`, `FormE`, `HasE`, finite typing grammar and eight-generator conversion relation. It defines a new unary interpretation on the frozen finite **open** SKI carrier. A fresh mutual induction on the actual formation/typing grammar proves:

- Every formed type denotes a conversion-saturated PER at each admissible context environment.
- Related context environments induce exactly the same type relation. Dependent identity motives are therefore coherent.
- Every actual HasE derivation respects that relation at related environments. This covers all twenty constructors, including finite impredicative instantiation, dependent Pi/Sigma, proof erasure, J, conversion, piExt and allExt.

These are `form_sound`, `formation_per`, `formation_coherent`, `has_sound`, `context_sound` and `fundamental`. The statements quantify over every actual derivation; they are not soundness for a copied or restricted typing grammar. The hereditary law records are induction **conclusions**, never new formation premises.

The construction does not reuse soundness of the inherited F/G model. A transitive Lean-constant dependency audit confirms that the new whole-model theorem does not depend on the old F, G, predicates or old soundness/fundamental theorems.

## The mathematical obstacle that was resolved

The critical issue was dependent coherence, including the interaction of the two kinds of substitution with full impredicative quantification. A relation-valued type environment makes simultaneous term/type substitution an unconditional structural equality (`F_mixed`). Formation then certifies the substituted type relations as actual saturated PERs. Thus allElim really instantiates the full-PER quantifier at the formed argument type; its admissibility is proved, not assumed.

Type variables are interpreted by arbitrary saturated PERs. The actual grammar has external All quantification, not a term-level universe with codes required to represent every PER. There is consequently no assumed raw-term enumeration of all PERs and no unproved universe-closure postulate. Every formed type relation is admitted to the same full class by the formation theorem.

For J, the actual theta context has a varying endpoint and an identity-proof coordinate. The two environments needed in the proof are related because the endpoints are related at their proper type and the proof converts to I. The newly proved formed-motive coherence transports the base case to the target. The actual source `jPoly` computation supplies the final conversion. No raw typing of the endpoint and no unrestricted raw-sensitive motive are assumed.

Identity evidence is represented by the conversion class of I. This validates proofErase: two identity realizers are raw-convertible through I. It does not identify arbitrary related endpoints at Raw. The earlier rejected Raw-motive argument was not repeated or used as a premise.

Both extensionality rules are checked. In piExt, the supplied pointwise identity plus q's function membership gives the full cross-argument relation, rather than equality only on identical inputs. allExt uses every saturated-PER instance of the actual body derivation.

## Exact model contract

The applicative carrier, compatible conversion and polynomial interpretation are the frozen open-term construction and imported-source transport. Raw is compatible raw conversion. Bottom is empty. Pi is the ordinary extensional dependent arrow relation. All is the intersection over **all** saturated PERs, with no extra heterogeneous-link uniformity clauses. Identity is represented equality at the endpoint type, realized by terms convertible to I.

Sigma uses the dependent relation on first and second projections. Unlike the inherited F/G Sigma, this model imposes no additional raw `Represented` predicate. This is an explicit design choice of the new interpretation, and all actual Sigma formation/introduction/elimination rules are proved sound for it. No claim that this is literally the inherited model, or that the earlier represented-pair condition has been derived, is made.

The organization of the mutual-recursion proof follows the source's useful hereditary-conclusion pattern; its semantic definitions and rule lemmas are newly proved for this different interpretation. FiniteDerives is handled by a fresh induction on its actual seven constructors, including All introduction/elimination and reduction. No old semantic fundamental theorem is invoked.

## Consequence for the exact compiler and scalar target

`Application.lean` proves literal equality of the new Church interpretation with the frozen `churchPER`, and of `N → N` with its frozen arrow PER. It then applies the checked original compiler transport:

- The actual imported `variableExpr.closed` and `redundantExpr.closed` are related at `N → N` in this sound whole model.
- Their represented typed identity is inhabited by I in the model.
- They remain nonconvertible at Raw. Typed semantic equality and raw intensional distinction coexist in the same sound interpretation.
- Every finite successor numeral inhabits N; the Church argument is non-vacuous. The empty context is inhabited, and the new model independently yields a no-closed-Bottom consistency control.

The unchanged pinned `ScalarFusionCore.lean` is also imported and compiled. Thus W and c3 are the **actual source definitions**, not formula mirrors. `scalar_target_valid` proves semantic membership of the actual c3 in `W originalQ`, where `originalQ` is explicitly the imported `redundantExpr.closed`; `scalar_target_fundamental` proves the corresponding semantic relation at arbitrary related outer environments. The alias called q in the separately retained LiteralScalarFusion source is exactly that endpoint. That later module and its four-way source equivalence are not claimed to have been rebuilt here.

This is a new-to-project whole-model result, not a claim of mathematical novelty for unary PER semantics. Philosophically, it makes the distinction between extensional identity and raw representation concrete in a coherent dependent calculus, rather than exhibiting it only in an isolated test algebra. It does not establish any metaphysical or actual-world conclusion.

## What remains open

Soundness goes from source derivations to model validity. It does not go backwards. The semantic inhabitation of the exact fixed target therefore supplies neither `HasE [] c3 (W q)` nor semantic completeness. Its negation is not proved either.

The earlier full-PER separator-class exclusion is now supported by a genuine whole-HasE model, so its extension premise is no longer a merely possible or potentially empty condition. This model cannot separate the target. That does not rule out sound Henkin, differently restricted, or otherwise different models, and does not prove that such a separator exists. The next source-level obligation is genuinely syntactic or requires a justified different model; no further reduct-level agreement is being promoted to a proof.

A proposed further canonicity claim was checked against the retained source and deliberately not counted as another result: `EffectiveStandardness.semantic_church_standardness`, together with the inherited `ExtensionalRepair.unary_fundamental`, already gives observational standardness for every closed HasE term of type N. The new full-PER model provides a different route to that corollary; it does not make the old conclusion new. No redundant proof was added for theorem count.

## Verification and preservation

Lean version: 4.19.0, commit 6caaee842e94. New source and application are checked with `--trust=0`; only ordinary `propext`, `Classical.choice` and `Quot.sound` occur. There are no added axioms, admitted proofs or evaluator-oracle proofs.

The 83-module predecessor source closure remains unchanged at repository commit `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`, with pinned Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`. ScalarFusionCore was independently re-read through the connected GitHub plugin at that same immutable commit; its SHA-256 is `975e2220158cf6b285cc994e36c408389a908c77e0f63bfa028c8cb416319618`, and its Git blob is `4fb8ccac2316b5660408017a1ca559fe032a605f`.

`replay.py` validates all three frozen predecessor manifests, the actual scalar-source acquisition and the new source hashes, then compiles into a fresh output directory. It is a fresh replay of the added files against the verified original closure, not a claim that it itself rebuilds all original modules. The independent review separately rebuilds that closure and exercises additional nonvacuous dependent/proof-sensitive controls. No protected source, predecessor source, repository branch or integration state is changed.
