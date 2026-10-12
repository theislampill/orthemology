# Independent review: actual-E weak induction and literal rigidity

Verdict: PASS for the exact candidate source SHA256 `6817015986cf36c0a36bb4affd6f608c432f22215a532e848304be88ac519684` and RESULT.md SHA256 `90a01fd9fd795332c2f35a7e058ebd7ca1d43140784df2799b1306de485e9888`.

## Mathematical and scope review

1. `WeakInductionAt` is genuinely external existential section existence. All three premises are actual-E formation/typing, with no restriction to the original Has calculus. It assumes neither a specified output term nor zero/successor computation laws. Quantification over Ty is metatheoretic; there is no new internal universe or source induction proposition.
2. `EqFamily u` is literally identity over the retained Church N with endpoints `(wk u) (var 0)` and `var 0`; `family_at` confirms its intended substitution. The base premise is exactly ZeroAt. `nat_congr` uses FullE.transport_source, whose body invokes HasE.j, to send identity through successor. `step_point` combines the supplied StepAt proof with this congruence using the retained actual-E identity transitivity. `family_step` introduces n and its induction-hypothesis proof, correctly weakening u/s twice and using var 1 for n and var 0 for its proof.
3. The section is weakened to the generic n. Source J supplies symmetry, then transitivity with the raw I beta identity yields Id_N(I n,u n), matching the orientation of literal ResultAt. HasE.piExt is applied with its explicit formation, endpoint, function-body and scope premises. It yields the erased polynomial I, not raw equality or reflection of u into I.
4. The generic telescope is exactly `[StepAt (var 1), ZeroAt (var 0), NT]`. After extension, u is var 2, its zero proof is var 1, and its successor proof is var 0. The two ZeroAt shifts and one StepAt shift match those indices. The three final Pi introductions discharge successor proof, zero proof, then u. Their resulting type is the literal unchanged SourceRigidity.Rigidity, and their polynomial is exactly three abstractions of ident. The proof of its typing still depends on the hypothetical schema despite the erased term's simple form.
5. The direct converse proof uses no R hypothesis, internal Uniqueness principle, U-to-R theorem, compiler-identity conclusion, computation-law assumption, or semantic completeness route. Imports expose inherited infrastructure, but these routes are not used in the direct argument. Positive converse axioms are only propext and Quot.sound.
6. Forward direction reuses the retained full actual-E section theorem after transporting a closed R derivation to the chosen actual-E context. This is an implication from existence of a source proof, not an assertion that R is inhabited.
7. `weak_induction_iff_generic_context` has precisely one fixed generic context as its restricted schema. The local equivalence is correctly stated with ContextualWeakInduction Γ: induction at every well-formed finite telescope extension of Γ. The reverse uses only the three-assumption extension; forward weakening preserves R through arbitrary finite prefixes. A bare WeakInductionAt Γ gives only rigidity of supplied local endomorphisms by this argument. Neither source nor documentation asserts a strict separation of bare local/empty-context induction from global induction.
8. Negative corollaries transfer the retained RigidityDiscriminator.rigidity_uninhabited theorem through the new converse. They establish metatheoretic nonadmissibility, not an internal negation, source R→bottom witness, fresh independence proof, or new model. The inherited discriminator's compiler-identity route belongs only to this negative consequence and is not circular evidence for the positive converse.
9. No new axiom, sorry, source constructor, UIP, reflection, Sigma eta, computation law, universe, unconditional closed R proof, protected modification, baseline rebuild, integration or programme closure is introduced.

## Independent replay and controls

The exact frozen source was copied into this review directory and compiled with retained Lean 4.19.0, `--trust=0`, into isolated `fresh-lib`. LEAN_PATH begins with that output and excludes the author's new validation directory. Retained dependencies were reused without rebuild. `build.log` and `positive.log` record successful new-module and positive-control compiles. Expanded schema signatures, literal R, exact generic telescope, local extension qualification, negative corollaries, and the equality-family instance are independently checked in PositiveControls.lean.

Printed axiom closures: nat_congr, family_step, endomorphism_rigid, extended/generic induction converse use only propext and Quot.sound. The forward implication, equivalences and inherited negative corollaries additionally use Classical.choice. No sorryAx or custom axiom appears.

Five independent expected-rejection files each exit 1 with the intended type mismatch:
- NegativeBareLocal: bare WeakInductionAt Γ cannot be supplied as ContextualWeakInduction Γ.
- NegativeClosedRigidity: the conditional converse cannot be used as an unconditional closed R proof.
- NegativeGenericAtEmpty: WeakInductionAt [] cannot stand in for WeakInductionAt GenericContext.
- NegativeInternalSchema: the external Prop is not an object-language Ty.
- NegativeOriginalHas: the actual-E result cannot be silently downgraded to original Has.

These rejection controls verify interface boundaries of the attempted terms. They are not independent impossibility/separation theorems. The initial positive-control run had an unqualified N resolving to the wrong namespace in reviewer code; explicitly opening EffectiveCompleteness fixed only the review control. The candidate itself passed its first independent compile. The initial diagnostic is retained for transparency.

REVIEW_RECEIPT.json binds the candidate, inspected documentation/check script, author input manifest, retained directly used inputs, toolchain executable, reviewer controls, and final logs. Review credit is limited to the new module against those retained dependencies.
