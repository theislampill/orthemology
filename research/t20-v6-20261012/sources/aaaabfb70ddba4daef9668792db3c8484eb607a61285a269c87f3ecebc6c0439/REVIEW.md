# Independent review of the frozen typed-observer core

10 October 2026. **PASS for the bounded original-source construction and explicitly conditional family obstruction.** This is a research review, not integration, audit acceptance, closure, or a claim of field novelty.

## Reviewed increment

The author froze exactly `TypedObserver.lean`, `TypedObservations.lean`, and `TypedFamilyContract.lean` and supplied their source and retained-object hashes before independent replay. The review's frozen copies match those source hashes. The separate later Sigma/ChurchPair cross-typing investigation is outside this review.

Inputs are original `P01AC.Has`, `Form`, and `Ctx` derivations in an arbitrary actual telescope, with arbitrary source type B and n:N, f:B→B, a:B. They are not arbitrary extended-grammar HasE input derivations. The construction embeds into HasE; its displayed 0/1 endpoint identities are actual HasE judgements at B. The author report now makes this boundary explicit.

## Source audit

- `body_has` obtains B's source formation from the typed f, constructs the Sigma state, genuinely term-weakens f and B beneath the state binder, types fst at wk B, and applies f by typed Pi elimination. Its result is wk(Carrier B), as required by the Pi introduction rule. No replacement grammar or formation/scope premise is introduced or dropped.
- `observe_fresh_has` type-weakens the original n, f, a derivations and **reconstructs** the observer under twkTel Γ at twk B. Its fresh End carrier uses parameter 0 while B's old type parameters have shifted. It does not identify twkTel Γ with Γ or assume B is closed.
- `observe_all_has` uses that actual body in allIntro. Every source-formed specialization is recovered at exactly B through tinst_twk. `fixed_reabstract` likewise contains the actual has_twk step.
- Open polynomial conversions for numerals 0 and 1 are combined with formed and typed endpoints to derive HasE identities at B. The constant update K b is derived at B→B by typed K and typed application; its one-observation has the actual HasE identity to b.
- Direct proof-body inspection covers all 78 declarations present in the author typed-observer namespace and finds no use of original or extended Raw typing/erasure constructors. The meaningful source typing paths were also inspected manually. This is deliberately not a claim that the transitive dependency graph omits every Raw constructor: generic inherited structural induction lemmas mention all cases of the unchanged source grammar.

## Independent source controls

`IndependentControls.lean` uses Γ=[param 0] and B=Id_(param 0)(var 0,var 0). This is a formed, inhabited source type with genuine type and term dependencies.

The file proves that wk B has endpoint var 1, twk B has carrier param 1, both changes are nontrivial, and twkTel Γ differs from Γ. It instantiates body typing, fresh-body typing, All(twk B), specialization at every formed T, the zero identity, and the typed-constant one identity for this B.

Two deliberately rejected files attempt to leave the term dependency or type dependency unshifted. Lean rejects each at the expected Has type mismatch. These are source-scoping controls, not merely equalities of rendered syntax.

## Conditional semantics and its sharpness

`FixedAllContract` explicitly requires both compositional reintroduction assembly and equality of the eliminate/weaken/reintroduce cycle with the original value. A separate body_assembly hypothesis ties a result to the actual typed observer's structured-body interpretation. Type-weakening compatibility with the fixed outer environment is an interpretation obligation described in the author report, not a theorem derived for arbitrary semantics here.

Given those laws, the proof is a direct equality argument. No generic parametricity, graph/naturality theorem, scalar fusion principle, full function-space admissibility, or whole-HasE model is imported as an unannounced premise. The typed K update is sufficient for the distinguishing test; all semantic endomaps need not be source-admissible.

Independent controls show the precise limits:

- Full Bool-indexed Bool families have compositional constant-body reintroduction and realize the varying zero/one body, but their erased cycle is not the identity.
- Identity reintroduction satisfies the erased-cycle equation, but fails the compositional assembly equation on varying full families.
- The coherent constant-family contract itself exists and does not assemble the discriminating varying body. Thus coherence and observer-body assembly are distinct obligations.
- If B is singleton, varying zero/one coordinates do assemble. Distinct a,b is essential; a fixture attempting to supply distinct Unit values is rejected.
- Uniform zero coordinates and uniform one coordinates both assemble under the coherent contract.
- Even with B=Bool, the varying candidate is invisible to the identity update. This is an observer-specific constraint, not generic naturality from one observation.
- A fixture asserting coherence of unrestricted Bool families is rejected, while the independent theorem proves the claimed universal erased-cycle equation is false.

The author's Unit-as-Raw conjunction is only a local set-level control. It neither constructs a whole-source model with singleton Raw and nontrivial B nor proves that all singleton-Raw candidates fail. The excluded family is conditional on a fixed discriminating B plus the stated interpretation/assembly/coherence laws.

## Verification and custody

The replay compiles the three frozen core modules plus two independent positive modules with Lean 4.19.0 `--trust=0`, then checks four expected rejection fixtures. Positive logs have no warnings/errors or sorryAx. The dependency audit permits only the inherited propext, Classical.choice, and Quot.sound; the key family constancy proof has no axioms.

93 inherited source/object pairs are bound to historical compilation receipts, in addition to retained prerequisite and Lean binary hashes. No baseline module is rebuilt. Source and object pins are checked before and after compilation. Rebuilt review objects have their own recorded hashes; the author objects and all other pinned original files are read only and unchanged.

Run `python hase-typed-observer-review-20261010/replay.py` from the shared workspace. The review replays its own frozen copies and writes only to its own fresh output directory. It does not run the author's receipt-mutating replay script. `REVIEW_RECEIPT.json` identifies the final checked output and frozen author manifest.

Initial review-work outputs are retained under validation as non-primary diagnostics: an unused-variable warning in a review control, and a source-scanner false positive on the word “axiom” in a diagnostic string, were fixed in review-owned files before the final clean replay. Neither was an author theorem defect.

## Remaining boundary

The original graph projection bridges, arbitrary original universal HasE W, and its negation remain OPEN. There is no arbitrary-HasE input generalization, generic naturality theorem, whole-source model construction/refutation, scalar-fusion conclusion, protected edit, integration, closure, or novelty claim. The set-level uniformity principle already existed polymorphically in the predecessor; the concrete new source contribution is typed B with real weakening and exact typed observations.
