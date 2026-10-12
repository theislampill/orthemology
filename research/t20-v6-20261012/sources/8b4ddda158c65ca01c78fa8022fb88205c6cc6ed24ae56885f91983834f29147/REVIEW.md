# Independent review: homogeneous Henkin source model

Date: 10 October 2026. Verdict: PASS for the precise source-independence result below. No mathematical or formal blocker found within this reviewed scope. This is not an integration, release, or global T20 closure decision.

## Exact result

Write `q` for the unchanged original `P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed`, and `W` for the unchanged original `P01AC.ExtensionalRepair.ExactScalarFusion.W`.

The checked reviewer theorem `ReviewHenkinSourceModel.literal_syntactic_independence` establishes both:

1. For every original `P01D.Poly` p, there is no `P01AC.ExtensionalRepair.HasE [] p (W q)`.
2. For every original `P01D.Poly` p, there is no `P01AC.ExtensionalRepair.HasE [] p (P01AC.arr (W q) .bottom)`.

The first uses the newly constructed homogeneous Henkin countermodel. The second independently replays the root's `NoInternalNegation.lean`, using the retained full-PER model and its semantic inhabitant of the same W. The two models' originalQ definitions are definitionally equal to the literal original q. These are meta-level nonderivability theorems. Neither provides an internal source proof of W or of its negation. In particular, the first excludes the original fixed c3, not just a chosen altered proof polynomial.

## Replay and provenance

`REPLAY.json` records a fresh independent Lean 4.19.0 `--trust=0` replay of these twelve modules:

- CaseOperational, HomogeneousPER, ConcreteUniverse, GuardControls
- SourceTransport, HenkinSoundness, DependencyAudit
- LiteralCounterexample, OriginalWNoninhabitation
- MixedPERControl, NoInternalNegation, ReviewControls

All exit codes are zero. The fresh output directory was empty before compilation. Every new-model import resolves to a freshly compiled object; no author's cached new-model objects were used. Retained source-theory/full-PER objects and installed package objects were reused read-only. This is deliberately a new-module-only replay, not a new build of the 83-module original source closure.

`INPUT_HASHES.json` records the eleven author/root source snapshots, five directly inspected original sources, and ninety retained top-level baseline object hashes. Every initial hash was rechecked after replay and remained unchanged. `REPLAY.json` additionally records the review-control source hash, all new object/log hashes, exact Lean version, and LEAN_PATH. `REVIEWED_DOCUMENTS.json` binds the mathematical writeup, relevant predecessor proof, and previous baseline verification receipts. The retained source-provenance receipt names repository `theislampill/orthemology`, pin `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`; no fresh remote refetch was performed in this review.

All printed closed theorem dependencies are contained in Lean's standard `propext`, `Classical.choice`, and `Quot.sound`. The final combined independence theorem has only those three axioms. No sorry/admit, custom axiom declaration, unsafe implementation, implemented_by, or native_decide occurs in the reviewed source code. Lexical matches in comments merely say that axioms/native_decide are not used. The one warning is the unused proofErase premise, expected because Raw is top.

Run `python3 review-henkin-source-model-20261010/replay.py` from the workspace to repeat the bounded replay. No protected source, predecessor, repository integration, or baseline object was changed by this review.

## Whole-source audit

The semantic carrier is actual finite syntax containing I/K/S, two atoms, application and ν. `Step.nuF` packages eight syntactic RawFun shapes, not a semantic test or circular conversion premise. Parallel developments prove confluence of this exact enlarged reduction system. Conversion joining, atom separation, atom/function disjointness and application head-origin are then proved. None is a model-contract hypothesis in the final theorem.

The eligible universe U contains all saturated PERs which are universal, atom-supported, or function-supported. It is defined before source interpretation and is not a finite menu or syntax-indexed family. The exact arbitrary-intersection, dependent-Pi and dependent-Sigma closures are proved. The Sigma universal-base case uses dependent-family equality across related inputs, which makes all fibers equal when the base is universal. The Pi argument only selects a supported input with a proper fiber. Existing checked guard controls show that deleting extensionality or strictness really breaks the respective closure argument, and that an empty Pi domain must give the universal relation.

`HenkinSoundness.F` interprets the actual imported Ty. `SourceTransport.interp` interprets the actual imported Poly independently of its type or derivation. All quantifies over the entire subtype `{ R // U R }`; the reviewer proves its equivalence to explicit quantification over every eligible relation. It does not quantify merely over source-definable interpretations. Formation eligibility and related-environment coherence are conclusions of the actual mutual source recursors, not extra source premises.

Both mutual inductions cover all two CtxE, seven FormE and twenty HasE constructors. The separate finite proof covers all seven actual FiniteDerives constructors, including impredicative elimination. All-elimination uses the formation induction's U membership. Pi/Sigma use exact source pairing/projections; identity uses the I-conversion class guarded by endpoint relatedness. J uses the actual two-coordinate theta context and actual motiveAt substitution. Extensionality uses typed pointwise premises, never untyped extensional equality. Source conversion soundness handles all eight original PolyConvPlus constructors, including atom/application bridge by compositional equality. The arbitrary-environment abstraction proof permits ν-valued environments and does not only establish beta for source-term values.

## Literal counterexample and nonvacuity

The imported original compiler theorem binds `LiteralCounterexample.original_q_eval` to literal redundantExpr.closed. The witness chooses n=ν, the eligible discrete atom PER, f=K a1, and a=a0. The scalar left converts to a0. The original compiler's pair-state seed is a function weak-head value, so ν performs one step there; the scalar right converts to a1. Confluence proves these atoms unequal under conversion. `W_empty` excludes every pair of semantic realizers of the actual W, at every environment.

Independent controls establish:

- The literal original q is actually HasE-typed at N→N.
- The actual W(q) is FormE-formed and its interpretation lies in U.
- An admissible empty type environment and a supported empty term context exist.
- ν belongs to the interpretation of the actual Church N.
- The original source c3 really inhabits W(I), and the new model validates it. Thus the model does not indiscriminately reject scalar-fusion types.
- The retained full-PER model still validates W(q).
- ν is not an embedded original Term, and is not the default-environment interpretation of any original Poly. These controls concern literal syntax/evaluation, not a newly claimed conversion-conservativity theorem.

## Essential semantic boundary

Raw is top in the new model. This is essential, not an optional simplification. Actual rawAtom gives support to both the source-mapped atom a0 and source-mapped function I. Any U member with both supports must be universal. Conversion itself is therefore excluded from U. The reviewer formalizes this and also exhibits that Raw relates a0 to a1 although conversion does not.

The adversarial MixedPERControl builds an ordinary proper saturated PER with classes containing a0/I and K a0. It has mixed support, is excluded from U, and rejects ν as a Church member. Consequently the universe restriction is substantive. This is a genuine alternate Henkin interpretation of the same source, not the retained full-PER interpretation with Raw=conversion.

That difference does not invalidate the source-nonderivability inference: the new fundamental theorem is separately proved for the unchanged grammar. It also does not refute W's truth in the retained full-PER interpretation. The two model arguments together establish the exact syntactic independence theorem above.

Inherited closed-source Church canonicity has a premise `HasE [] n N` for a source polynomial n. It does not say every element of every Henkin interpretation of N is a source numeral. The extra semantic ν therefore does not conflict with that theorem. The existing cross-typing observer is respected because identical source pair polynomials have one derivation-independent, function-valued interpretation. The graph invariant need not imply the absent scalar projection bridge when the scalar seed is atom-valued and graph states are function-valued.

## Scope limits

No claim of internal syntactic negation, full-PER counterexample, semantic completeness, all-model agreement, original-calculus modification, arbitrary-target compiler separation, or global T20 closure is made. This review establishes the exact literal original W independence under the unchanged imported HasE grammar and the documented standard Lean metatheory, conditional only on reuse of the already checked pinned baseline artifacts.
