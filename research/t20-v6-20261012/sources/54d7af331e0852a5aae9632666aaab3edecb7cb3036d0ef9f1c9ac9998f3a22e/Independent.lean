import CompletionSeparation
namespace IndependentReview
open P01AC P01D P01AC.ExtensionalRepair
example : SourceRigidity.Rigidity = .pi (arr EffectiveCompleteness.N EffectiveCompleteness.N)
  (arr (SourceRigidity.ZeroAt (.var 0))
    (arr (SourceRigidity.StepAt (.var 0)) (SourceRigidity.ResultAt (.var 0)))) := rfl
example : SigmaTagBoundary.Eta = .pi (.sigma .raw .raw)
  (.identity (.sigma .raw .raw) (.var 0)
    (pairPoly (fstPoly (.var 0)) (sndPoly (.var 0)))) := rfl
example (ρ : HenkinSoundness.REnv) (η : HenkinSoundness.Env) (a b : CaseOperational.T) :
  HenkinSoundness.F .raw ρ η a b := True.intro
example (ρ : TaggedPER.REnv) (η : TaggedPER.Env) (a b : OpenTermStandardness.T) :
  TaggedPER.F .raw ρ η a b ↔ OpenTermStandardness.Conv a b := Iff.rfl
example (p : Poly) : ¬ HasE [] p (arr SigmaTagBoundary.Eta SourceRigidity.Rigidity) :=
  CompletionSeparation.no_eta_to_rigidity p
example (p : Poly) : ¬ HasE [] p (arr SigmaTagBoundary.Eta (arr SourceRigidity.Rigidity .bottom)) :=
  CompletionSeparation.no_eta_to_not_rigidity p
example (ρ : FullPER.REnv) (η : FullPER.Env) :
  ¬ (∀ a b, ¬ FullPER.F SourceRigidity.Rigidity ρ η a b) := by
  intro h
  exact h _ _ (RigidityDiscriminator.rigidity_valid ρ η)
example (p : Poly) : ¬ HasE [] p (arr SourceRigidity.Rigidity SigmaTagBoundary.Eta) :=
  SigmaTagBoundary.no_rigidity_to_eta p
#print axioms CompletionSeparation.no_eta_to_rigidity
#print axioms CompletionSeparation.no_eta_to_not_rigidity
end IndependentReview
