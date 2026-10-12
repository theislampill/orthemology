# Independent review: actual Joint induction computation

## Verdict

PASS for the frozen packet's stated, bounded claims. No blocking correctness or scope issue was found. This is a source-computation advance in the existing unadopted Joint calculus, not a change to its rules or a closure/adoption claim.

Reviewed candidate: `hase-joint-induction-computation-20261010/`.
Candidate freeze SHA-256: `49d7f606de4991e1cde787e986e84ee6f9a824a69efc659422b9eaa6f4ac427a`.
Candidate RESULT.md SHA-256: `98caa77fb706546d5e13b7e720aa652545f16ee539fbef0260cd06c0621d2b9c`.

## Findings

1. **Actual source interfaces and literal output.** `JointInductionLaws.lean:34–68` proves zero and successor identity for the exact `sectionPoly p s` returned by the retained `HasJ.natInduction` constructor. All context, formation, seed, step and input assumptions use `CtxJ`, `FormJ` or `HasJ`. No hidden old-E formation or typing premise restricts the public interface. The successor fiber is literally `inst P (succPoly n)`.

2. **Rigidity is internally discharged.** The public successor theorem obtains the already-derived closed Joint rigidity witness and applies actual Joint weakening into arbitrary new contexts (`JointInductionLaws.lean:17–19`). The retained `PositiveTransfer.joint_rigidity` is sourced by `CompletionIndependence.into_joint`, a constructor-by-constructor syntactic transfer from the induction-enabled selective calculus. It does not infer a source derivation from semantic validity. The ported helpers honestly retain their explicitly supplied Joint-rigidity premise; the public computation result does not.

3. **The dependent successor argument is substantive.** The fold's projected index is first proved source-identical to the input. Actual J transport then changes the dependent action's index. Raw beta conversions only connect the uniform section application to its body and close congruent endpoints; they do not substitute for index identity or reflect semantic equality. Formation and scoping are supplied explicitly throughout the transport, application, and Pi-extensionality paths.

4. **New-family controls are strict about source scope.** `JointInductionControls.lean:36–105` establishes an actual index-dependent Joint family, seed, step, and computation instance while excluding old-E formation and every old-E inhabitant at the displayed seed and step types. The variation theorem distinguishes literal source types, not semantic fibers. The direct section at line 108 confirms that this reflexive example is only an input-scope discriminator, not evidence that induction is minimally necessary for that example. RESULT.md states this limitation accurately.

5. **Typed identity does not become Raw conversion.** `JointInductionRawBoundary.lean:57–77` proves typed identity and failure of `PolyConvPlus` for exactly the same endpoints in context `[N]`, with P=N, seed zero, step K, and variable input. The retained CaseOperational valuation mapping the variable to ν is used solely under soundness of raw conversion. It is never supplied as a Joint context realizer. Its observations separate the endpoints by distinct inert atoms. This does not revive the failed interpretation of ν as a natural in a sound Joint model.

6. **Compatibility with the retained positive model is direct.** The independent check applies the unchanged `JointCompletion.fundamental` to the exact new typed successor identity and obtains its FullPER fundamental judgment. It also reuses the unchanged no-closed-bottom theorem. Separately, the same endpoint pair proves that unrestricted reflection from `HasJ` natural identity to `PolyConvPlus` is false. These checks preserve the distinction between the positive faithful-Raw FullPER model, the raw operational separator, and the older negative old-E model.

7. **Function identity is explicitly conditional.** `induction_extensionality` (`JointInductionLaws.lean:93–105`) requires a seed and a complete induction step for the actual comparison family `Id_(P n)(u n,v n)`. It builds its pointwise identity section by induction and uses actual Pi extensionality. It does not derive that comparison step from arbitrary algebra laws, establish categorical initiality, prove identity-proof uniqueness, or give an unconditional uniqueness theorem for recursors. The report is accurate about this remaining obligation.

## Independent validation

- Copied all ten frozen candidate Lean modules into a separate reviewer-owned directory.
- Compiled all ten with Lean 4.19.0 (`6caaee842e94`) and `--trust=0`, writing every new `.olean` into an initially fresh output directory.
- Removed the candidate validation directory from the import search path. All candidate dependencies came from the fresh reviewer outputs; baseline dependencies were reused without rebuilding.
- Verified all 14 frozen candidate files, 130 retained source pins, and 232 retained object pins before and after replay.
- All ten modules passed without error, warning, or `sorryAx` output. The candidate's public/control dependency audit passed.
- Independently traversed dependency closures of all 50 positive helper/public theorems in `JointCompletion.InductionComputation`, allowing only `propext`, `Classical.choice`, and `Quot.sound`, and rejecting semantic fundamental/soundness or completion-rule soundness shortcuts. All passed.
- Compiled `IndependentChecks.lean` at trust 0: explicit failure of unrestricted typed-to-Raw reflection; exact successor identity accepted by retained FullPER; retained Joint no-closed-bottom.
- No candidate, protected source, retained object, or baseline artifact was edited by this review. All review output is in this separate directory.

The replay is intentionally narrow: retained dependency objects are hash-pinned inputs, not a newly rebuilt baseline. No choice-free or axiom-free foundational claim is made.

## Non-blocking documentation note

The opening comment of `JointInductionSectionApplication.lean` still says “actual-E typings”; its statements use actual Joint typing throughout. This is a copied comment, not a theorem/interface defect. No source change is required for the verdict, and the reviewed freeze was left untouched.

## Evidence

- `REPLAY_RECEIPT.json`: independent ten-module replay result.
- `replay.log`: all commands and outputs for that replay.
- `IndependentChecks.lean` and `independent-checks.log`: additional scope/model/dependency checks.
- `BASELINE_PINS.json`: exact reviewed candidate and retained pins.
- `REVIEW_RECEIPT.json`: final hashes and integrity check.
