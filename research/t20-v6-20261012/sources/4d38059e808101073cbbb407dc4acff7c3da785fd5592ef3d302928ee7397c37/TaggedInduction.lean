import JointSemantics
import TaggedPER

/- Additive soundness of full dependent induction for the retained tagged model.
   The model-independent raw evaluation equations are reused unchanged.
   No Sigma eta or Sigma elimination assumption occurs in this proof. -/
namespace TaggedInduction
open P01AC P01D TaggedPER
open P01AC.EffectiveCompleteness (N)
open SourceRigidity (zero)
open RigidityInitiality
open ImportedOpenTermTransport (interp)
open OpenTermStandardness (T Conv Arrow SatPER churchPER iter successorNumeral zeroTerm succTerm)
open JointCompletion (step_eval seed_eval iter_first run_index section_eval)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem nat_laws (Γ : Tel) : TaggedPER.TypeLaws Γ N where
  per := fun _ _ => per_laws churchPER
  transport := fun _ _ => rfl


theorem successor_family_eval (P : Ty) (ρ : REnv) (η : TaggedPER.Env) (n : T) :
    TaggedPER.F (successorFamily P) ρ (cons n η) = TaggedPER.F P ρ (cons (succTerm ⬝ n) η) := by
  rw [successorFamily,TaggedPER.F_subst]
  apply congrArg (fun η => TaggedPER.F P ρ η)
  funext k; cases k with
  | zero => simp only [P01F.cons,interp_app,RigidityDiscriminator.succ_eval,interp_var,cons]
  | succ k => rfl

theorem step_related {Γ P s} (hc : TaggedPER.ContextLaws Γ) (hP : TaggedPER.TypeLaws (N :: Γ) P)
    (hs : TaggedPER.Fundamental Γ s (dependentStepType P)) {ρ η ξ}
    (r : admissible ρ) (e : TaggedPER.E Γ ρ η ξ) :
    Arrow (TaggedPER.F (total P) ρ η) (TaggedPER.F (total P) ρ η)
      (interp (totalStep (uncurriedStep s)) η) (interp (totalStep (uncurriedStep s)) ξ) := by
  intro z w zw
  have d := (hc.ends r e).1
  have ss := hs ρ η ξ r e (first z) (first w) zw.1
  rw [TaggedPER.F_arr,successor_family_eval] at ss
  have succs : churchPER.rel (succTerm ⬝ first z) (succTerm ⬝ first w) := by
    intro Q f g fg a b ab
    exact Q.saturated (OpenTermStandardness.succ_application _ _ _).symm
      (OpenTermStandardness.succ_application _ _ _).symm
      (fg _ _ (zw.1 Q f g fg a b ab))
  have out := TaggedPER.F_pair hc (nat_laws Γ) hP r d succs (ss _ _ zw.2.1)
  exact ((type_sigma hc (nat_laws Γ) hP).per r d).raw
    (step_eval s η z).symm (step_eval s ξ w).symm out

theorem seed_related {Γ P p} (hc : TaggedPER.ContextLaws Γ) (hP : TaggedPER.TypeLaws (N :: Γ) P)
    (hp : TaggedPER.Fundamental Γ p (inst P zero)) {ρ η ξ}
    (r : admissible ρ) (e : TaggedPER.E Γ ρ η ξ) :
    TaggedPER.F (total P) ρ η (interp (totalSeed p) η) (interp (totalSeed p) ξ) := by
  rw [seed_eval,seed_eval]
  have pp := hp ρ η ξ r e
  rw [TaggedPER.F_inst,RigidityDiscriminator.zero_eval] at pp
  exact TaggedPER.F_pair hc (nat_laws Γ) hP r (hc.ends r e).1
    (OpenTermStandardness.successorNumeral_church 0) pp


/-- Full external induction at arbitrary lawful source-syntax motives, with the
literal retained uniform section polynomial. No old FormE premise is imposed. -/
theorem dependent_induction {Γ P p s} (hc : TaggedPER.ContextLaws Γ)
    (hP : TaggedPER.TypeLaws (N :: Γ) P)
    (hp : TaggedPER.Fundamental Γ p (inst P zero))
    (hs : TaggedPER.Fundamental Γ s (dependentStepType P)) :
    TaggedPER.Fundamental Γ (sectionPoly p s) (.pi N P) := by
  intro ρ η ξ r e n m nm
  have d := (hc.ends r e).1
  let R := ((type_sigma hc (nat_laws Γ) hP).per r d).object
  have run := nm R _ _ (step_related hc hP hs r e) _ _ (seed_related hc hP hp r e)
  have nn := churchPER.trans nm (churchPER.symm nm)
  have tr := hP.transport r (show TaggedPER.E (N :: Γ) ρ
    (cons (first (n ⬝ interp (totalStep (uncurriedStep s)) η ⬝ interp (totalSeed p) η)) η)
    (cons n η) from ⟨hc.refl r d,run_index p s η nn⟩)
  have body := tr ▸ run.2.1
  exact (hP.per (η := cons n η) r ⟨d,nn⟩).raw
    (section_eval p s η n).symm (section_eval p s ξ m).symm body

#print axioms dependent_induction
#print dependent_induction
end TaggedInduction
