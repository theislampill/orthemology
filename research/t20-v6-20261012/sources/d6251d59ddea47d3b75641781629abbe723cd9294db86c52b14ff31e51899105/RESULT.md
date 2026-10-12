# Exact Nat rigidity transfers to Church unit and generic fold naturality

## Checked results

All statements below are in the unchanged original `Has`/`HasE` syntax. `R` means the literal pre-existing `SourceRigidity.Rigidity`; no inhabitant of R is adopted or asserted.

### 1. A separately encoded polymorphic type

`UnitTy := All A.(A → A)` and `UnitEta := Πu:UnitTy.Id_UnitTy(u,I)`.

`rigidity_implies_unit_eta` is the closed source derivation

`HasE [] (abstract (abstract I)) (R → UnitEta)`.

`rigidity_implies_unit_eta_context` derives that same implication in any original well-formed context. Its elimination, `unit_eta_from_rigidity`, accepts arbitrary original-HasE evidence `r:R` and original-Has `u:UnitTy`, returning the displayed identity at the genuine polymorphic Unit type.

The encoding is literally `liftUnit u := K u`, with checked original-Has type N. Its type application is erased: `(K u) A f a` raw-converts to `u A a`. `nat_identity_fold` gives `Id_A(n A I a,a)` by applying the pre-existing `recursor_unique_source` to `f=I` and constant recursor `n↦a`. Its zero and successor hypotheses are original-Has identities obtained by raw computation. At `n=K u`, this gives the pointwise Unit identity. Actual `piExt` and `allExt`, with all formation, scope, weakening and type-binder premises, give `UnitEta`. R is bound as an ordinary original-Has hypothesis while crossing binders; the completed source implication can then consume arbitrary HasE R.

This is a new checked cross-type corollary, not an independent induction theorem or novel construction. Existing SourceUniqueness supplies its induction content directly. UnitTransfer imports no additional HasE structural module.

### 2. The exact previously retained naturality interface, conditional on R

`source_naturality_from_rigidity` proves:

- Γ is an original well-formed source telescope
- X and Y are arbitrary original-source formed types, including types depending on Γ; neither is restricted to parameter 0
- n:N, f:X→X, g:Y→Y, h:X→Y and a:X have original Has typing
- r:R has arbitrary HasE typing in Γ
- square has arbitrary HasE typing in X::Γ at the literal pre-existing `SourceFoldContract.squareType Y f g h`
- conclusion: some source polynomial e has HasE type `SourceFoldContract.foldType Y n f g h a`, namely `Id_Y(h(n X f a),n Y g(h a))`

`SourceNaturalityUnderRigidity` names precisely this conditional schema, and `conditional_source_naturality` proves it. It does not redefine or prove the old premise-free `SourceNaturality`.

The stronger `fold_transport_from_rigidity` admits an independently specified original-Has target seed b:Y and arbitrary HasE evidence `h(a)=b`, concluding `h(n X f a)=n Y g b`.

## How the missing transfer obligations are discharged

The mapped recursor is the actual source polynomial `mappedFold h f a := λn.h(n f a)`. Its original-Has typing and beta equation are checked. The square is first abstracted with the original HasE Pi rule, then weakened across n with the already certified actual-HasE `Structural.has_wk`, and applied to `n f a`. Raw computation and explicit source J give the recursor's successor equation. The arbitrary HasE seed equality supplies its zero equation.

`unique_at_carrier` instantiates the literal pre-existing All-quantified internal Uniqueness proposition at arbitrary Y. Its explicit dependent All/Pi eliminations handle type weakening under all six binders and accept arbitrary HasE zero/successor evidence. It does not silently use the parameter-0-only standalone SourceUniqueness theorem at an arbitrary carrier. The closed R→Uniqueness proof is moved to Γ by the already certified actual-HasE `Structural.has_closed`, then eliminated with r.

These structural dependencies come from `hase-church-structural-20261010/{HasEStructuralBase,HasEStructuralRename,HasEClosedWeakening}.lean`, whose retained replay/provenance checks all actual HasE rules, including the full Pi/All extensionality premises. This packet credits and reuses those lemmas; it supplies no new general HasE substitution theorem.

## Preserved boundaries and ancestry

The old `original_source_naturality_not_admissible : ¬SourceNaturality` and R/Uniqueness independence results are unchanged and compatible with this conditional theorem. FullPER semantic validity is not used to reflect source proofs. No new source rule, equality reflection, UIP, proof irrelevance, universe resizing, general HasE substitution, full relational parametricity, or Boolean identity theorem is asserted.

The proof ancestry is the reviewed nine-module `hase-rigidity-initiality-20261010` chain, the literal earlier `SourceFoldContract`/`InternalRecursorPrinciple` syntax, and the separately checked structural packet. Generic fusion from recursor uniqueness and Church encodings are standard arguments; no novelty is claimed for them. The inherited total-space route has external categorical/parametricity ancestry. The parent's targeted primary-source comparison is retained separately at `parametricity-ancestry-root-20261010/NOTE.md`: Krishnaswami–Dreyer, CSL 2013, https://www.cl.cam.ac.uk/~nk480/final-csl-internalizing-parametricity.pdf. That comparison supplies historical context only. This proof imports none of that paper's reflection/UIP assumptions or semantic-realizability results.

## Reproduction

Run `bash hase-rigidity-polymorphic-transfer-20261010/check.sh` from the workspace. It compiles both new modules with pinned Lean 4.19.0 and `--trust=0`, reusing existing compiled ancestry. The new modules are not a fresh rebuild of all inherited dependencies. The final clean output is in `validation/build.log`; source and selected immediate inherited hashes are in `validation/SOURCE_HASHES.json`.

All nine printed new theorem dependencies are exactly standard Lean foundations: `propext`, `Classical.choice`, and `Quot.sound`. There are no warnings, new axioms, `sorryAx`, or modified existing source files. Source modules are frozen for independent review.
