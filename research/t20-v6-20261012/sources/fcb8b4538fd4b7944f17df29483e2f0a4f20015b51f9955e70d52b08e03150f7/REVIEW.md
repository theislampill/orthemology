# Independent review: Unit transfer and conditional fold naturality

Verdict: PASS for both frozen phases, with the distinctions below. This is a bounded source-proof review, not a new datatype campaign or a claim of general parametricity.

## Unit: an actual closed internal implication

UnitTy is literally All A. A -> A, and UnitEta is Pi u:UnitTy. Id_UnitTy(u,I). UnitTransfer.rigidity_implies_unit_eta proves the actual unchanged HasE judgment

HasE [] (abstract (abstract I)) (Rigidity -> UnitEta).

The result is not merely a semantic validity statement or a metatheoretic contract. The source polynomial and exact type are checked independently by UnitReview.closed_exact.

The key encoding liftUnit u = K u is genuinely typed at N in original Has. Under type weakening, u is instantiated at the fresh parameter, obtaining an endomorphism, and K makes it constant in the endomorphism/step argument. The actual All introduction then yields the Church N type. The constant recursor K a has source-derived zero and step equations at identity endomorphism I. Previously checked source recursor uniqueness under explicit HasE Rigidity evidence gives n I a = a. For n=K u, raw K/I computations and actual source J symmetry/transitivity give u a = I a.

The extensional closure proof crosses type/term binders with original Has u and original Has r:Rigidity, using original structural lemmas. It applies actual HasE.piExt and HasE.allExt with all formation and scope premises. The final internal implication binds r and u as ordinary source variables, so it does not need arbitrary HasE weakening at this stage. Its explicit hypotheses are then abstracted away into Rigidity -> UnitEta; no proof of Rigidity is asserted.

The author's external application theorem accepts arbitrary HasE Rigidity evidence but original Has Unit evidence. Independent UnitReview.arbitrary_evidence verifies the immediate stronger application interface: in any original well-formed context, arbitrary HasE evidence of BOTH Rigidity and UnitTy suffices. Direct FormE.identity forms the conclusion, and source Pi elimination applies the already proved internal implication. This does not retrospectively enlarge the original-Has binder-crossing helper or infer Has from HasE.

## Fold naturality: exact conditional meta-contract

FoldNaturality.source_naturality_from_rigidity preserves every original premise and the exact conclusion of SourceFoldContract.SourceNaturality, adding explicit HasE Γ r Rigidity. In particular:

- X and Y are arbitrary original Form Γ carriers, including carriers depending on Γ, not just fresh type parameters.
- n, f, g, h, and a have the original Has typings prescribed by the old contract.
- The commuting square is arbitrary HasE evidence in exactly X::Γ, not restricted to old Has or raw conversion.
- The conclusion is existence of an actual HasE proof of the unchanged foldType.

SourceNaturalityUnderRigidity is a separately named metatheoretic contract. It is not an internal closed source type, an assertion of premise-free SourceNaturality, or an inhabitant of Rigidity. Independent FoldReview.closed_R_yields_original_contract proves that a hypothetical closed HasE R proof would yield the literal unchanged SourceNaturality proposition; this checks interface agreement without supplying such a proof.

The stronger fold_transport_from_rigidity also accepts an independently specified target seed b:Y and arbitrary HasE evidence h(a)=b. Its result is h(n f a)=n g b. The exact old-contract specialization chooses b=h(a) and the source reflexivity proof, so it does not alter the old conclusion or hide an additional seed assumption there.

## Construction and structural dependencies

The existing closed source implication Rigidity -> InternalRecursorPrinciple.Uniqueness is weakened into Γ using the previously certified actual-HasE Structural.has_closed and applied to r. unique_at_carrier performs actual All elimination of that literal polymorphic uniqueness formula at arbitrary Y, followed by dependent applications to a, g, u and arbitrary HasE zero/step equation evidence. All target formations and substitutions are checked; no semantic reflection is used.

mappedFold is the explicit original-source abstraction of n ↦ h(n f a). Its zero equation is source computation. The open HasE commuting square is abstracted to a Pi proof, then crosses the new n binder through the previously certified actual-HasE Structural.has_wk. Instantiation at n f a and source successor computation yield its step equation, with J transitivity joining endpoints. Literal recursor uniqueness at carrier Y gives mappedFold(n)=n g b, and source beta conversion supplies the final endpoint h(n f a).

HasEClosedWeakening imports HasEStructuralRename and HasEStructuralBase. These are existing proved structural inductions on the actual mutual source grammar, including the piExt/allExt premises. This review verifies their manifest-pinned sources and their previously replayed object hashes. It reuses them as existing dependencies rather than assuming HasE structural closure from old Has. UnitTransfer itself does not import this structural extension.

## Independent positive and adversarial controls

Fresh controls check literal Unit/UnitEta definitions, the exact closed implication, arbitrary HasE Unit/R application, exact arbitrary-carrier naturality, and compatibility with the prior SourceNaturality contract conditional on closed R evidence.

Three intentionally invalid proofs fail for the expected type mismatches:
1. Treating the proved Rigidity -> UnitEta judgment as an unconditional UnitEta judgment.
2. Passing HasE Rigidity evidence to the intermediate original-Has binder-crossing helper.
3. Treating conditional_source_naturality as the premise-free SourceNaturality proposition.

These failures validate interface boundaries; they are not claims that UnitEta itself is nonderivable or that every stronger interface is impossible. The independent stronger Unit application control demonstrates why that distinction matters.

## Limits

The Unit result is source-internal and conditional on R. Fold naturality is the exact conditional meta-contract over original carriers/endpoints and arbitrary HasE equation evidence. Neither asserts unrestricted parametricity, a new type constructor, unconditional R, source completeness, semantic reflection, Sigma eta, or any physical/ontological consequence. No ancestor or prior-art argument is used as a proof port.

## Replay and preservation

Frozen author hashes:
- UnitTransfer.lean: cd7ea123838e58294a078b1538be8003a022da6623a7f2d8753b2001072ded82
- FoldNaturality.lean: 66abf61f2374a7a782bbdf639d8b36f3cb5ad72e1d1cdae7cd66d373a5812926

The definitive hashes are recorded mechanically in REVIEW_RECEIPT.json. Fresh Lean 4.19.0 --trust=0 replay compiles both author modules and both positive-control modules, and checks the three expected failures. All successful theorem dependencies are at most propext, Classical.choice, and Quot.sound; the inherited structural lemmas use only propext and Quot.sound. The first exploratory Unit copy preceded the author's unused-variable cleanup; final replay uses the exact frozen, warning-free source. Existing retained objects are read-only and hash-verified, with no baseline rebuild or protected mutation.
