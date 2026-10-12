import ProofUniquenessControls
import Lean
namespace IndependentProofUniquenessReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open JointCompletion JointCompletion.ProofUniqueness JointCompletion.ProofUniqueness.Controls
open P01AC.Intensional.Plus (PolyConvPlus)
/-- Raw conversion of the two proof variables would contradict a checked raw model. -/
theorem source_identity_does_not_imply_raw_conversion :
    P01AC.ExtensionalRepair.HasE [oldProofType,oldProofType] (.atom .i)
      (.identity oldProofType (.var 0) (.var 1)) ∧
    ¬ PolyConvPlus (.var 0) (.var 1) :=
  ⟨original_bound_proofs_identical, bound_proofs_not_raw⟩
/-- Every numerical label, not only 0 and 1, survives pairing with I. -/
theorem label_identity_iff (j k : Nat) :
    (∃ r, HasJ [] r (.identity labelledType (labelled j) (labelled k))) ↔ j = k := by
  constructor
  · rintro ⟨r, h⟩
    exact labels_equal_of_identity h
  · intro h
    subst k
    exact ⟨.atom .i, .identityIntro
      (.identity (labelled_form .nil) (labelled_has j) (labelled_has j))
      (labelled_has j) (labelled_has j) (.refl _)⟩
/-- UIP iterates: witnesses of proof-identity are themselves internally identical. -/
theorem higher_uip {Γ A x y e f p q}
    (hc : CtxJ Γ)
    (hp : HasJ Γ p (.identity (.identity A x y) e f))
    (hq : HasJ Γ q (.identity (.identity A x y) e f)) :
    HasJ Γ (.atom .i) (.identity (.identity (.identity A x y) e f) p q) :=
  identity_proof_unique hc hp hq
end IndependentProofUniquenessReview
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for t in [``P01AC.ExtensionalRepair.ProofUniqueness.identity_proof_unique,
      ``JointCompletion.ProofUniqueness.identity_proof_unique,
      ``JointCompletion.ProofUniqueness.Controls.typed_observer_constant,
      ``IndependentProofUniquenessReview.higher_uip] do
    let (_, r) := ((Lean.CollectAxioms.collect t).run env).run {}
    for a in r.axioms do
      unless [``propext, ``Quot.sound].contains a do
        throwError "Unexpected positive axiom {a} for {t}"
    logInfo m!"INDEPENDENT POSITIVE AXIOM PASS {t}"
  for t in [``IndependentProofUniquenessReview.label_identity_iff,
      ``IndependentProofUniquenessReview.source_identity_does_not_imply_raw_conversion] do
    let (_, r) := ((Lean.CollectAxioms.collect t).run env).run {}
    for a in r.axioms do
      unless [``propext, ``Quot.sound, ``Classical.choice].contains a do
        throwError "Unexpected control axiom {a} for {t}"
    logInfo m!"INDEPENDENT CONTROL PASS {t}"
