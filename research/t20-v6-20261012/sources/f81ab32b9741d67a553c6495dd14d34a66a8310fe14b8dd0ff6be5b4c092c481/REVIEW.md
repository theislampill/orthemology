# Independent review: full actual-E rigidity-to-dependent-induction port

Verdict: PASS for the seven frozen additive modules and their bounded conditional conclusions. No blocking source defect was found. No protected source was edited, no inherited baseline was rebuilt, and no integration or whole-programme closure is authorized by this review.

## Exact improvement and retained syntax

The primary declarations in `RigidityInitiality.FullE` now quantify over arbitrary `CtxE Γ`, `FormE (N :: Γ) P`, actual `HasE` seed and curried/uncurried step evidence, arbitrary actual `HasE` numeral evidence, and actual `HasE Γ r SourceRigidity.Rigidity`. The independently checked elaborated theorem types contain no original `Ctx`, `Form`, or `Has` restriction. Formation and scope obligations are still proved explicitly.

`dependent_section_curried` and `dependent_section_explicit` type the exact retained second-projection polynomial at `P(n)`. `section_has` types the exact retained `sectionPoly p s` at `Pi N P`; `rigidity_implies_section` binds the literal retained Rigidity as an ordinary source hypothesis and gives the source implication `R → Pi n:N.P(n)`. Families remain metatheoretically quantified. There is no added object-language universe or internal family quantifier.

All total-space, fold, section and rigidity definitions are imported from the unchanged `hase-rigidity-initiality-20261010` and `SourceRigidity` sources. There is no shadow replacement of `total`, `totalStep`, `totalSeed`, `projectedFold`, `uncurriedStep`, `dependentStepType`, `sectionBody`, `sectionPoly`, or `Rigidity`. A fresh control checks their literal defining equalities. The new raw application-beta theorem is exactly an alias of the retained theorem, independently checked in the elaborated proof term. Retained syntax source hashes and constructor inventories are unchanged: 2 context, 7 formation, 20 typing and 8 Plus-conversion constructors.

## Construction and correct rigidity dependence

The port forms the actual Sigma total space `Σ n:N.P(n)` and instantiates Church N at this arbitrary actual-E-formed carrier using the checked `Structural.allElim_formed`. It constructs the total-space algebra and its projected endomorphism. Raw algebra calculations provide its zero and successor identities. The actual rigidity hypothesis identifies this typed endomorphism with identity; actual J evaluates that identity at n and transports the dependent second projection back to `P(n)`.

The section polynomial contains no rigidity proof term. This erasure does not remove the hypothesis from its typing derivation: R supplies the typed projection/index identification, and existing J erasure recovers the same literal second-projection polynomial. The independent dependency audit confirms the uniform and pointwise conclusions reach the actual rigidity-elimination construction and the required actual-E structural, Pi and J rules. `MissingRigidityMustFail` fails precisely because the omitted argument leaves a function from a `HasE r Rigidity` premise.

The new support uses the already-reviewed actual-E dependent-term substitution/weakening and mixed/type-parameter substitution interfaces. Fixed inherited zero/successor constructors may use original-source inclusion; the arbitrary family, data, ambient context, R evidence and n premises do not require original-source proofs. The proof-ancestry audit excludes the old restricted dependent-section/uniform-section theorems and semantic `FullPER`, `HomogeneousOriginal`, `RigidityDiscriminator` and unary-fundamental dependencies from the six principal positive results. Imported unrelated semantic material is not used to reflect a conclusion into the source.

## Computation boundary

- The literal raw zero reduction is unconditional. The new actual-E typed zero identity needs the stated formed family and typed data, but no R premise. It is not being relabeled as original-Has evidence for E-only inputs.
- Uniform application raw-converts to the same retained pointwise section polynomial. The new typed application identity additionally uses the conditional section typings.
- The successor theorem concludes an existential actual-E identity in `P(succ n)`, conditional on actual-E R and n evidence. The raw fold step initially computes at the folded state's first projection; the dependent J/application argument identifies that index with n. It does not derive unrestricted raw successor conversion by reflection.
- `RawSuccessorMustFail` independently rejects the attempted use of that typed identity theorem as a `P01DF.PolyConv` proof. This is a precise interface-boundary check, not a new theorem that every such raw equation is nonderivable.

No Sigma eta, UIP, identity reflection, proof-path equality, new typing rule, new axiom or assumed universe is introduced. The standard Lean axiom dependencies are only `propext`, `Classical.choice`, `Quot.sound`, or subsets. The generic zero law uses only `propext` and `Quot.sound`.

## Independent and author controls

1. `IndependentScopeControl` constructs the closed constant family `P = wk D`, where `D = Id_(Id_N(I,SKK))(I,I)` is formed only in actual E. It proves original-Form family exclusion and original-Has seed/step exclusions, invokes the new uniform implication, and exercises the typed zero and conditional successor laws. A separate direct section is proved. This is explicitly an input-scope control; R is not necessary for this constant instance.
2. `IndependentBinderJControl` constructs the actual-E-only ambient context `[D]` and proves it is not an original Ctx. The family refers to the old ambient proof variable. Applying the uniform implication binds R and n while retaining that variable correctly: the separately checked shifted family uses index 2, and the index-1 captured alternative is provably different. A distinct genuinely dependent identity motive over D exercises the new J transport and its erased version in the non-original context. The ambient section family is constant in n, so it too is a contextual/binder scope control, not an R-necessity example.
3. `RetainedBoundaryControl` independently checks the literal polynomial/R equalities and reuses the unchanged discriminator to re-establish the joint closed noninhabitation of R and its internal negation in the enlarged import environment. It also preserves the inherited corresponding Uniqueness boundary. These are external nonderivability statements; they do not produce source negation inhabitants.
4. `FullEDependencyAudit` checks the principal theorem interfaces, source-only proof ancestry, foundation axioms, unchanged grammar inventories, actual mixed/term structural use, Pi binding, J, the exact beta alias and the absence of rigidity elimination from the zero proof.

The author's own family `P(n) = Id_E(n I I,n I I)`, with `E = Id_N(I,SKK)`, has proved original family/seed/step exclusions and unequal literal zero/successor-zero instances. It is syntactically index-dependent. The author explicitly proves a direct section, and correctly presents this as a scope discriminator, not semantic/nonconversion separation or evidence that R is essential for this reflexive family.

Four independently written negative modules reject at the intended type mismatches: missing R, typed successor identity substituted for raw conversion, the old restricted theorem supplied actual-E-only inputs, and capture of the ambient variable when adding a binder. Substantive original-source exclusions are positive kernel-checked negation theorems, not conclusions inferred from these rejected programs.

## Fresh replay and exact bindings

Run `python3 hase-full-e-dependent-induction-independent-review-20261010/replay.py`.

The final replay freshly compiles all seven exact frozen author modules and four independent positive/audit modules with Lean 4.19.0 `--trust=0`, then checks four intended failures. Successful modules have no warnings, errors or `sorryAx`. It checks proof-escape tokens, verifies 591 unique prior source/object/review/manifest bindings before and after, verifies the frozen copies against author files, and binds all fresh sources, objects, commands, logs, direct import resolutions and axiom output. It only reuses retained compiled dependencies, without claiming a new full-baseline rebuild.

`EXACT_BINDINGS.json` indexes the frozen author source digests and the exact review/receipt bindings. `VERIFIED_INPUTS.json` records retained prerequisites; `REVIEW_RECEIPT.json` records the fresh run; `MANIFEST.json` binds the replay implementation, all copied/new Lean sources and this report. `exploratory/` is not final replay evidence.

This PASS removes the prior original-Has premise restriction for the stated conditional dependent-family construction. It does not establish a closed inhabitant of R, premise-free dependent induction, full categorical initiality, full calculus completion, or whole-frontier closure.
