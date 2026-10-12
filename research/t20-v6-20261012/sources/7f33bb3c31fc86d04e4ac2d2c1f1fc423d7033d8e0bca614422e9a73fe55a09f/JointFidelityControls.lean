import JointNumeralFidelity
import JointDependentControls
import Lean

namespace JointCompletion.ExtractionFidelity.Controls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness (N inputNumeral)
open P01AC.Intensional.Plus (PolyConvPlus)
open JointCompletion.DependentExtraction (extractSigma)
open JointCompletion.DependentExtraction.Controls
  (fiber fiber_form package package_has package_extracts_two)
open SigmaCompletion (etaMotive reconstruct)
set_option maxRecDepth 32768
set_option maxHeartbeats 16000000

/-- The retained genuinely dependent/new-family package is identical to its
numeral-indexed representative at its actual Sigma type. -/
theorem package_identity_at_two : HasJ [] (.atom .i)
    (.identity (.sigma N fiber) package (pairPoly (inputNumeral 2) (sndPoly package))) := by
  simpa only [package_extracts_two] using extracted_package_identity package_has

/-- A formed consumer genuinely mentions its supplied package. The numeral
continuation is returned at its original package-indexed target. -/
theorem original_eta_consumer : HasJ [] (.atom .i)
    (.identity (.sigma N fiber) package (reconstruct package)) := by
  have hR := eta_motive_formed CtxJ.nil (Structural.form_nat .nil) fiber_form
  have hd := canonical_eta_branch CtxJ.nil (Structural.form_nat .nil) fiber_form
  have h := extracted_continuation_original package_has hR hd
  simpa only [SigmaCompletion.branchAt, psub, SigmaCompletion.eta_motive_at] using h

/-- These are literally different target types. Re-establishing the old
repacked target is insufficient to prove the new original-target theorem. -/
private def nodes : Poly → Nat
  | .var _ => 1
  | .atom _ => 1
  | .app f a => nodes f + nodes a + 1

theorem consumer_targets_differ :
    inst (etaMotive (.sigma N fiber)) package ≠
      inst (etaMotive (.sigma N fiber)) (pairPoly (inputNumeral 2) (sndPoly package)) := by
  simp only [SigmaCompletion.eta_motive_at]
  intro h
  have he := (Ty.identity.inj h).2.1
  have hb := (Poly.app.inj (Poly.app.inj he).2).2
  have hn := congrArg nodes hb
  simp only [DependentExtraction.Controls.package, DependentExtraction.Controls.evidence,
    pairPoly, sndPoly, nodes] at hn
  omega

/-- Actual Sigma eta is available at a variable input, including its full
source identity formation and scoping premises. -/
theorem variable_sigma_eta :
    HasJ [SigmaTagBoundary.SigmaRaw] (.atom .i)
      (.identity SigmaTagBoundary.SigmaRaw (.var 0) (reconstruct (.var 0))) := by
  have hS : FormJ [] SigmaTagBoundary.SigmaRaw :=
    .sigma (.raw .nil) (.raw (.ext .nil (.raw .nil)))
  have hc : CtxJ [SigmaTagBoundary.SigmaRaw] := .ext .nil hS
  have hraw := FormJ.raw hc
  have hS' := FormJ.sigma hraw (FormJ.raw (.ext hc hraw))
  have hz : HasJ [SigmaTagBoundary.SigmaRaw] (.var 0) SigmaTagBoundary.SigmaRaw :=
    .var hS' .zero
  exact sigma_eta hc hraw (FormJ.raw (.ext hc hraw)) hz

/-- Typed fidelity does not silently install raw pair eta. Its same variable
endpoints are not source-convertible. -/
theorem variable_raw_eta_false :
    ¬ PolyConvPlus (.var 0) (reconstruct (.var 0)) := by
  intro h
  have hc := ImportedOpenTermTransport.source_plus_sound h
    (fun _ => OpenTermStandardness.T.i)
  exact JointCompletion.Controls.raw_pair_eta_fails hc

#print axioms package_identity_at_two
#print axioms original_eta_consumer
#print axioms consumer_targets_differ
#print axioms variable_sigma_eta
#print axioms variable_raw_eta_false
end JointCompletion.ExtractionFidelity.Controls

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for target in [``JointCompletion.ExtractionFidelity.sigma_eta,
      ``JointCompletion.ExtractionFidelity.dependent_pair_congr,
      ``JointCompletion.ExtractionFidelity.repack_identity,
      ``JointCompletion.ExtractionFidelity.extracted_package_identity,
      ``JointCompletion.ExtractionFidelity.extracted_continuation_original,
      ``JointCompletion.ExtractionFidelity.Controls.package_identity_at_two,
      ``JointCompletion.ExtractionFidelity.Controls.original_eta_consumer,
      ``JointCompletion.ExtractionFidelity.Controls.consumer_targets_differ,
      ``JointCompletion.ExtractionFidelity.Controls.variable_sigma_eta,
      ``JointCompletion.ExtractionFidelity.Controls.variable_raw_eta_false] do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in report.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    logInfo m!"PASS {target}: only standard logical axioms."
  for target in [``JointCompletion.ExtractionFidelity.sigma_eta,
      ``JointCompletion.ExtractionFidelity.dependent_pair_congr,
      ``JointCompletion.ExtractionFidelity.repack_identity] do
    let (_, source) := ((Lean.CollectAxioms.collect target).run env).run {}
    for forbidden in [``FullPER.fundamental, ``JointCompletion.fundamental,
        ``JointCompletion.sigma_elimination, ``JointCompletion.dependent_induction] do
      if source.visited.contains forbidden then
        throwError "Semantic shortcut in source construction {target}: {forbidden}"
    logInfo m!"PASS {target}: no semantic typing shortcut."
  let (_, eta) := ((Lean.CollectAxioms.collect ``JointCompletion.ExtractionFidelity.sigma_eta).run env).run {}
  unless eta.visited.contains ``JointCompletion.HasJ.sigmaElim do
    throwError "Expected actual full Sigma-elimination constructor in eta proof."
  let (_, congruence) := ((Lean.CollectAxioms.collect ``JointCompletion.ExtractionFidelity.dependent_pair_congr).run env).run {}
  unless congruence.visited.contains ``JointCompletion.HasJ.j do
    throwError "Expected actual J constructor in dependent pair congruence."
  logInfo m!"PASS actual Sigma-elimination and J constructors are used."
