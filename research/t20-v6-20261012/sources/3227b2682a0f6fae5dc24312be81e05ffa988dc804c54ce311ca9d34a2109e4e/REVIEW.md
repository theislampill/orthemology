# Independent review: actual Joint recursor uniqueness

## Finding

PASS within the stated mathematical and source-level scope. No blocking mathematical, binder, implementation, or claim-scope issue found. The formerly explicit comparison-step premise is now genuinely derived from the two sections' shared ordinary recursion laws. This is an ordinary independent review, not a release/adoption decision.

Candidate: `hase-joint-recursor-uniqueness-20261010`.
Frozen `validation/CANDIDATE_FREEZE.json` SHA-256: `6af3c08e7fd1adee842b110a909e02bbbbeb341bb514be3886421f2072bd95d3`.

## Claim-by-claim source review

1. **Actual congruence consumes the identity assumption.** `JointRecursorCongruence.lean:14–35` forms the motive `Id_(wk B)((f x)^+, f^+ var0)`, starts with reflexivity at x, and passes the supplied `he` directly to retained `transport_has_erased`. That retained theorem, `JointInductionComputationLaws.lean:13–30`, passes `he` to actual `HasJ.j` before converting its erased polynomial. This is not congruence inferred from endpoint typing or proof erasure alone. The operation is the same f on both sides. `dependent_step_congr:67–83` specializes this construction to the supplied s at the same n.

2. **The comparison step is derived, not repackaged as an assumption.** The ordinary `successorLawFamily` at `JointRecursorCongruence.lean:38–42` mentions one section u and the supplied s only. The theorem `comparison_step`, `JointRecursorUniqueness.lean:48–96`, assumes typings of s,u,v and their two ordinary law sections, with no comparison law. In context `C :: N :: Γ`, `var0` has the weakened comparison type; it is fed to `compare_algebra_values` at lines 82–84. That theorem passes it to `arrow_congr` at line 25, composes the u law and congruence, then the reversed v law. Two actual Pi introductions abstract the natural and identity binders. The double symmetry makes the evidence polynomial ident without asserting equality of identity proofs.

3. **All family and context binders have the promised scope.** Public uniqueness has arbitrary `Γ`, actual `CtxJ Γ`, arbitrary `FormJ (N :: Γ) P`, actual seed and curried-step typings, and actual u/v section typings. No old-E formation/typing or externally supplied rigidity hypothesis appears. The explicit `wk`, `pren`, shifted-family identities and successor substitution match the nested contexts; they were re-elaborated by Lean. The shared zero seed is constructed by symmetry and transitivity from the two laws at the same p.

4. **Typed dependent-function uniqueness has exactly the advertised premises.** `recursor_unique`, `JointRecursorUniqueness.lean:101–112`, supplies its derived seed and derived comparison step to retained `induction_extensionality`, which uses actual `natInduction` and `piExt`. The conclusion is `HasJ Γ ident (Id_(Πn:N,P(n))(u,v))`. It neither identifies proof paths nor reflects typed identity into Raw conversion.

5. **Ordinary-rule and packaged-law interfaces agree.** `recursor_unique_generic_laws:117–128` takes actual law derivations under the generic natural binder and packages them by Pi introduction, using their actual scoping evidence. Independent `generic_packaged_laws_equivalent` also proves the converse by source application at the generic variable. This does not extract a uniform source term from a meta-level statement only about closed numerals.

6. **The canonical corollary uses the exact retained polynomial.** `canonical_successor_laws`, `JointCanonicalRecursor.lean:43–59`, applies the existing successor theorem once in the generic-variable context, with weakened p and s and shifted P, then abstracts that single source witness. The rename equation identifies the result with the unchanged `sectionPoly p s`. `unique_to_canonical:63–72` uses this law, the actual canonical section, and its zero law, without another comparison premise. Independent `canonical_generic_law` checks the ordinary un-packaged interface too.

7. **The new-family controls are genuine but appropriately limited.** The retained family `Id_E(n I I,n I I)` has actual newly formed carrier E, literal index variation, and old-E exclusions for formation, seed, and step. `JointRecursorControls.lean:19–46` separately supplies direct-section zero and successor laws by actual typing and K-conversion; neither law mentions the canonical recursor or comparison family. `new_family_uniqueness:50–53` applies the new corollary. Independent `new_context_control` additionally weakens this result into the newly formed E context. This is an input-scope discriminator; the family is reflexive and the direct section is already available, so no rule-minimality claim follows.

## Independent negative and boundary controls

- `identity_premise_control` rejects omission of the identity input or substitution of endpoint typing at the congruence interface, then checks the genuine theorem application.
- `shared_operation_control` rejects using a successor law for an arbitrary unrelated operation t as the law for s. These two controls test the exact interfaces, not global nonderivability.
- **Stronger semantic negative control:** `ZeroOnlyControl.lean` constructs `constantZero = K zero` and ident at `NT`, and actual identity witnesses that both return zero at zero. It proves `zero_laws_insufficient : ¬ ∃ e, HasJ [] e (Id_NT constantZero ident)`. An assumed function identity is reversed and evaluated at numeral one via retained source J; the retained typed numeral-count separation then forces `0 = 1`. Thus a shared zero law alone genuinely does not imply uniqueness. Retained soundness is used only for this negative scope control, not the candidate's positive constructions.
- `strict_raw_boundary_preserved` checks together the retained actual typed successor identity and the strict negation of its unrestricted Raw conversion. The new uniqueness result does not collapse this boundary.

## Replay evidence and dependency boundary

All five frozen source modules were copied and independently compiled to a fresh reviewer output directory using Lean 4.19.0, commit `6caaee842e94`, with `--trust=0`. No retained dependency was rebuilt and no candidate or original retained location was written. Candidate existing objects were excluded from the import path. Both independent control modules compiled cleanly, with no warnings, errors, or sorryAx. The environment-inspection module also ran cleanly.

The author's 10 candidate-file entries and all 388 declared retained entries were verified before and after the replay and again after the independent controls. The candidate audit's complete axiom/dependency traversals passed, including its exclusions of semantic shortcuts for positive constructions and its requirements for source J, congruence, natInduction and piExt. General uniqueness depends on standard `propext` and `Quot.sound`; canonical uniqueness additionally inherits standard `Classical.choice`.

The 388 declared entries are **not the whole imported environment**. The existing environment also uses third-party Lean/package-cache support objects. The first reviewer attempt omitted these ambient support objects while copying the declared pins; the missing Mathlib object was found in the existing retained environment, copied without rebuilding, and the replay then passed. This was reviewer isolation setup, not a candidate proof failure. `AMBIENT_SUPPORT_INPUTS.json` records additional copied objects; `ACTUAL_IMPORTED_OBJECTS.json` separately hashes the exact transitive objects seen by the final environment audit, including toolchain/package caches and the two review controls. These observed hashes must not be described as original author-declared pins.

Evidence files:
- `REVIEW_RECEIPT.json`: final machine-readable review/replay receipt
- `REPLAY.json`: five-module replay receipt
- `IndependentControls.lean` and `IndependentControls.log`
- `ZeroOnlyControl.lean` and `ZeroOnlyControl.log`
- `EnvironmentAudit.lean` and `EnvironmentAudit.log`
- `ACTUAL_IMPORTED_OBJECTS.json`: observed imported-object paths and hashes
- `AMBIENT_SUPPORT_INPUTS.json`: separately copied ambient objects
- `candidate/`: immutable copied candidate sources and scripts
- `replay.py`: reviewer-owned isolated replay driver

## Scope conclusion

The valid conclusion is actual typed dependent-recursor uniqueness from shared ordinary zero and successor laws, including exact canonical-section uniqueness for arbitrary newly FormJ families. It does not establish Raw reflection, identity-proof/path uniqueness, full categorical initiality, global completeness, decidability, source-rule adoption, or T20 closure. The author report states these boundaries accurately.
