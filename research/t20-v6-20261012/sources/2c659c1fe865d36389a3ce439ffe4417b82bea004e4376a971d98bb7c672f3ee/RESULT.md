# Actual-E conditional dependent induction from the literal rigidity hypothesis

## Checked result

The retained total-space construction now applies to arbitrary actual `CtxE`, `FormE`, and `HasE` premises. In namespace `RigidityInitiality.FullE`, `section_has` proves:

- `hc : CtxE Γ`
- `hP : FormE (N :: Γ) P`
- `hp : HasE Γ p (inst P zero)`
- `hs : HasE Γ s (dependentStepType P)`
- `hr : HasE Γ r SourceRigidity.Rigidity`

imply `HasE Γ (sectionPoly p s) (.pi N P)`.

No original `Form`, `Has`, or `Ctx` premise remains. In particular, the rigidity witness itself has arbitrary actual `HasE` typing and is weakened by the certified actual-E theorem. It need not belong to original `Has`.

The pointwise theorem `dependent_section_curried` additionally takes arbitrary `hn : HasE Γ n N` and proves the exact retained polynomial

`sndPoly (n (totalStep (uncurriedStep s)) (totalSeed p))`

at `inst P n`. Its uncurried counterpart is `dependent_section_explicit`. `dependent_section_from_rigidity` retains the existential total-step interface.

`rigidity_implies_section` binds the literal existing rigidity proposition as an ordinary source hypothesis and derives

`HasE Γ (abstract (sectionPoly (pren Nat.succ p) (pren Nat.succ s))) (arr SourceRigidity.Rigidity (.pi N P))`.

Families remain quantified in the Lean metatheorem. No object-language universe or internal family quantifier is added. The result is conditional dependent elimination, not a closed inhabitant of rigidity and not premise-free induction.

## Literal source preservation and construction

The source type/term grammar, `SourceRigidity.Rigidity`, `ZeroAt`, `StepAt`, `ResultAt`, `total`, `totalStep`, `totalSeed`, `projectedFold`, `uncurriedStep`, `dependentStepType`, `sectionBody`, and `sectionPoly` are imported directly from the retained modules. They are not replaced or redefined in this packet. All pure raw-conversion lemmas, including the projection and fold beta equations, are likewise reused.

The proof ports the retained construction rather than inventing another argument: form the actual Sigma total space; instantiate Church N there; build its projected Peano endomorphism; eliminate the exact rigidity hypothesis; evaluate its identity at the input; and use actual source J to transport the second projection. Existing erased-J conversion supplies the same literal second-projection polynomial.

The genuinely strengthened helper judgments include total-space algebra formation/typing, the projected endomorphism, its zero/successor hypotheses, rigidity elimination for an arbitrary actual-E endomorphism, pointwise equality, and dependent transport/coherence. Source scope and formation premises remain explicit.

The certified dependent-term packet supplies `Structural.form_inst`, actual-E weakening, telescope formation and scope. The certified mixed/type-parameter packet supplies `Structural.allElim_formed` for Church instantiation at an arbitrary actual-E total space. It derives result formation from actual-E substitution rather than postulating it. The small support aliases are credited inherited interfaces, not new structural theorems.

## Computation scopes

- `section_zero_law` is an actual `HasE` identity at `P(0)` without a rigidity premise. The existing raw `section_zero_beta` remains valid literally. This generalization does not claim that actual-E-only inputs have original-Has zero evidence.
- `section_successor_law` is an actual `HasE` identity in `P(succ n)` between `sectionBody p s (succ n)` and `s n (sectionBody p s n)`, given the stated actual-E family/data/input and actual-E rigidity evidence.
- That successor result is propositional. The retained raw fold step computes at the folded state's first projection; J-dependent application coherence moves it to n. No unrestricted raw successor equality, equality reflection, UIP, or identification of proof paths is asserted.
- `section_application_beta` is explicitly an alias of the existing raw beta theorem for the identical polynomial. `section_application_identity` additionally checks both endpoints in the actual family and obtains a typed identity from that raw conversion.

## A provably non-original dependent-family control

Let `E = Id_N(I,SKK)`, using the retained actual-E Church identity control and its proved original-Has exclusion. Define

`P(n) = Id_E(n I I, n I I)`.

This family depends on n in both actual identity endpoints. `family_distinct_instances` proves that its zero and successor-zero instances are different literal types. This is syntactic index dependence, not a claim that those instances are semantically distinguishable or nonconvertible.

The packet checks:

1. `family_formed : FormE [N] family`.
2. `family_seed` and `family_step`, with actual-E seed I and curried step `abstract (abstract I)`.
3. `family_not_original : ¬ Form [N] family`.
4. `seed_not_original p : ¬ Has [] p (inst family zero)` for every p.
5. `step_not_original s : ¬ Has [] s (dependentStepType family)` for every s.
6. `actual_only_rigidity_implication`, an actual application of the strengthened theorem to these inputs, binding the unchanged R hypothesis.

The exclusions are proofs, not failed searches or failed typechecks. Original formation of the zero instance would require an original-Has endpoint inhabiting E, contradicting the retained control.

This is an input-scope discriminator, not evidence that rigidity is necessary for this easy reflexive instance. `control_has_direct_section` separately proves its section without rigidity, making that limitation explicit. The substantive generalization is the universal theorem's arbitrary actual-E premises, not a new nontrivial consequence of this particular identity family.

## Ancestry, boundaries and reproduction

The construction is a port of `hase-rigidity-initiality-20261010/{Initiality,SectionCorollaries,UniformSection,ComputationLaws,SectionApplication}.lean`. That packet explicitly restricted its dependent-family metatheorems to original Form/Has; its `section_has` additionally required original-Has rigidity evidence. This packet removes those exact restrictions using the subsequently checked actual-E structural machinery. It does not silently generalize other inherited theorems.

There is no semantic reflection, full-PER completeness appeal, new typing constructor, new axiom, Sigma eta, UIP, full category-level initiality, or premise-free rigidity/induction claim. The inherited independence of the literal rigidity proposition is unaffected. No T21, integration, merge or programme closure follows.

Run `bash hase-full-e-dependent-induction-20261010/check.sh`. It compiles only these seven additive modules with pinned Lean 4.19.0 and `--trust=0`, reusing existing compiled dependencies. The inherited baseline is not rebuilt or modified.

- `FullESupport.lean`: actual-E helpers and Church instantiation
- `FullEInitiality.lean`: total-space construction and rigidity-dependent transport
- `FullESectionCorollaries.lean`: literal section and curried step
- `FullEUniformSection.lean`: uniform section and R implication
- `FullEComputationLaws.lean`: typed dependent coherence, zero and successor laws
- `FullESectionApplication.lean`: literal raw beta and actual typed application identity
- `FullEInductionControls.lean`: proved actual-E-only dependent-family scope discriminator

`validation/build.log` records the clean author replay and printed axiom dependencies. Theorems depend only on standard Lean foundations (`propext`, `Classical.choice`, `Quot.sound`, or subsets); no `sorryAx` or new axiom is present. `validation/SOURCE_HASHES.json` pins the new files and inherited sources. `validation/PRESERVATION_CHECK.json` verifies the retained source manifests. Independent review is maintained separately.
