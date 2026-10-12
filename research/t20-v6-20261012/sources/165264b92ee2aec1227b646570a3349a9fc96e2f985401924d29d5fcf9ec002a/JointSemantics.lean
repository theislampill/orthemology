import FullEUniformSection
import Constructive
import RigidityDiscriminator

namespace JointCompletion
open P01AC P01D FullPER
open P01AC.EffectiveCompleteness (N)
open P01AC.BooleanPrimitive (succPoly)
open SourceRigidity (zero)
open RigidityInitiality
open ImportedOpenTermTransport (interp)
open OpenTermStandardness (T Conv Arrow SatPER churchPER iter successorNumeral zeroTerm succTerm)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

@[simp] theorem eval_pair (a b : Poly) (η : FullPER.Env) :
    interp (pairPoly a b) η = pair (interp a η) (interp b η) := rfl
@[simp] theorem eval_fst (z : Poly) (η : FullPER.Env) :
    interp (fstPoly z) η = first (interp z η) := rfl
@[simp] theorem eval_snd (z : Poly) (η : FullPER.Env) :
    interp (sndPoly z) η = second (interp z η) := rfl

theorem nat_laws (Γ : Tel) : FullPER.TypeLaws Γ N where
  per := fun _ _ => per_laws churchPER
  transport := fun _ _ => rfl

theorem sigma_eta {Γ A B z} (hc : FullPER.ContextLaws Γ) (ha : FullPER.TypeLaws Γ A)
    (hb : FullPER.TypeLaws (A :: Γ) B) (hz : FullPER.Fundamental Γ z (.sigma A B)) :
    FullPER.Fundamental Γ (.atom .i) (.identity (.sigma A B) z (SigmaCompletion.reconstruct z)) := by
  intro ρ η ξ r e
  have d := (hc.ends r e).1
  have zz := hz ρ η η r (hc.refl r d)
  exact ⟨⟨(ha.per r d).raw (.refl _) (OpenTermStandardness.fst_pair _ _).symm zz.1,
    (hb.per (η := cons (first (interp z η)) η) r ⟨d,(ha.per r d).left zz.1⟩).raw
      (.refl _) (OpenTermStandardness.snd_pair _ _).symm zz.2⟩,.refl _,.refl _⟩

theorem sigma_elimination {Γ A B P d z} (hc : FullPER.ContextLaws Γ)
    (ha : FullPER.TypeLaws Γ A) (hb : FullPER.TypeLaws (A :: Γ) B)
    (hP : FullPER.TypeLaws (.sigma A B :: Γ) P)
    (hd : FullPER.Fundamental (B :: A :: Γ) d (SigmaCompletion.branchType P))
    (hz : FullPER.Fundamental Γ z (.sigma A B)) :
    FullPER.Fundamental Γ (SigmaCompletion.branchAt d (fstPoly z) (sndPoly z)) (inst P z) := by
  intro ρ η ξ r e
  have zz := hz ρ η ξ r e
  have branches : FullPER.E (B :: A :: Γ) ρ
      (cons (second (interp z η)) (cons (first (interp z η)) η))
      (cons (second (interp z ξ)) (cons (first (interp z ξ)) ξ)) := ⟨⟨e,zz.1⟩,zz.2⟩
  have v := hd ρ _ _ r branches
  have pairEnv : (fun n => interp (SigmaCompletion.pairSub n)
      (cons (second (interp z η)) (cons (first (interp z η)) η))) =
      cons (pair (first (interp z η)) (second (interp z η))) η := by
    funext n; cases n <;> rfl
  rw [SigmaCompletion.branchType, FullPER.F_subst, pairEnv] at v
  have eta := (sigma_eta hc ha hb hz) ρ η ξ r e
  have tr := hP.transport r (show FullPER.E (.sigma A B :: Γ) ρ
    (cons (interp (SigmaCompletion.reconstruct z) η) η) (cons (interp z η) η) from
    ⟨hc.refl r (hc.ends r e).1,
      (type_sigma hc ha hb).per r (hc.ends r e).1 |>.sym eta.1⟩)
  rw [FullPER.F_inst]
  simpa only [SigmaCompletion.branchAt, interp_sub, interp_cons, interp_var] using tr ▸ v

theorem step_eval (s : Poly) (η : FullPER.Env) (z : T) :
    Conv (interp (totalStep (uncurriedStep s)) η ⬝ z)
      (pair (succTerm ⬝ first z) (interp s η ⬝ first z ⬝ second z)) := by
  have h := ImportedOpenTermTransport.interp_abstraction_beta
    (pairPoly nextIndex (uncurriedStep s)) η z
  simpa only [totalStep, nextIndex, uncurriedStep, interp_app, interp_ren, interp_var,
    RigidityDiscriminator.succ_eval, eval_pair, eval_fst, eval_snd,
    OpenTermStandardness.cons] using h

theorem seed_eval (p : Poly) (η : FullPER.Env) :
    interp (totalSeed p) η = pair zeroTerm (interp p η) := by
  change pair (interp zero η) (interp p η) = _
  rw [RigidityDiscriminator.zero_eval]

theorem successor_family_eval (P : Ty) (ρ : REnv) (η : FullPER.Env) (n : T) :
    FullPER.F (successorFamily P) ρ (cons n η) = FullPER.F P ρ (cons (succTerm ⬝ n) η) := by
  rw [successorFamily,FullPER.F_subst]
  apply congrArg (fun η => FullPER.F P ρ η)
  funext k; cases k with
  | zero => simp only [P01F.cons,interp_app,RigidityDiscriminator.succ_eval,interp_var,cons]
  | succ k => rfl

theorem step_related {Γ P s} (hc : FullPER.ContextLaws Γ) (hP : FullPER.TypeLaws (N :: Γ) P)
    (hs : FullPER.Fundamental Γ s (dependentStepType P)) {ρ η ξ}
    (r : admissible ρ) (e : FullPER.E Γ ρ η ξ) :
    Arrow (FullPER.F (total P) ρ η) (FullPER.F (total P) ρ η)
      (interp (totalStep (uncurriedStep s)) η) (interp (totalStep (uncurriedStep s)) ξ) := by
  intro z w zw
  have d := (hc.ends r e).1
  have ss := hs ρ η ξ r e (first z) (first w) zw.1
  rw [FullPER.F_arr,successor_family_eval] at ss
  have succs : churchPER.rel (succTerm ⬝ first z) (succTerm ⬝ first w) := by
    intro Q f g fg a b ab
    exact Q.saturated (OpenTermStandardness.succ_application _ _ _).symm
      (OpenTermStandardness.succ_application _ _ _).symm
      (fg _ _ (zw.1 Q f g fg a b ab))
  have out := FullPER.F_pair hc (nat_laws Γ) hP r d succs (ss _ _ zw.2)
  exact ((type_sigma hc (nat_laws Γ) hP).per r d).raw
    (step_eval s η z).symm (step_eval s ξ w).symm out

theorem seed_related {Γ P p} (hc : FullPER.ContextLaws Γ) (hP : FullPER.TypeLaws (N :: Γ) P)
    (hp : FullPER.Fundamental Γ p (inst P zero)) {ρ η ξ}
    (r : admissible ρ) (e : FullPER.E Γ ρ η ξ) :
    FullPER.F (total P) ρ η (interp (totalSeed p) η) (interp (totalSeed p) ξ) := by
  rw [seed_eval,seed_eval]
  have pp := hp ρ η ξ r e
  rw [FullPER.F_inst,RigidityDiscriminator.zero_eval] at pp
  exact FullPER.F_pair hc (nat_laws Γ) hP r (hc.ends r e).1
    (OpenTermStandardness.successorNumeral_church 0) pp

theorem iter_first (p s : Poly) (η : FullPER.Env) (k : Nat) :
    Conv (first (iter (interp (totalStep (uncurriedStep s)) η)
      (interp (totalSeed p) η) k)) (successorNumeral k) := by
  induction k with
  | zero => rw [OpenTermStandardness.iter,seed_eval]; exact OpenTermStandardness.fst_pair _ _
  | succ k ih =>
      exact ((OpenTermStandardness.fst_congr (step_eval s η _)).trans
        (OpenTermStandardness.fst_pair _ _)).trans (.app (.refl _) ih)

theorem run_index (p s : Poly) (η : FullPER.Env) {n : T} (nn : churchPER.rel n n) :
    churchPER.rel
      (first (n ⬝ interp (totalStep (uncurriedStep s)) η ⬝ interp (totalSeed p) η)) n := by
  obtain ⟨k,hk⟩ := OpenTermStandardness.church_standard n nn
  have cv := (OpenTermStandardness.fst_congr (hk _ _)).trans (iter_first p s η k)
  have nk : churchPER.rel n (successorNumeral k) := by
    intro Q f g fg a b ab
    exact Q.saturated (hk f a).symm
      (OpenTermStandardness.successorNumeral_application k g b).symm
      (OpenTermStandardness.iter_related Q fg ab k)
  exact churchPER.saturated cv.symm (.refl _) (churchPER.symm nk)

theorem step_shift (s : Poly) :
    pren Nat.succ (totalStep (uncurriedStep s)) =
      totalStep (uncurriedStep (pren Nat.succ s)) := by
  simp [totalStep,uncurriedStep,nextIndex,fstPoly,sndPoly,pairPoly,pren,
    ← P01D.abstraction_naturality, psub_comp,pup,P01F.cons,psub,
    P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped P01AC.BooleanPrimitive.succ_has)]

theorem section_eval (p s : Poly) (η : FullPER.Env) (n : T) :
    Conv (interp (sectionPoly p s) η ⬝ n)
      (second (n ⬝ interp (totalStep (uncurriedStep s)) η ⬝ interp (totalSeed p) η)) := by
  have h := ImportedOpenTermTransport.interp_abstraction_beta
    (sectionBody (pren Nat.succ p) (pren Nat.succ s) (.var 0)) η n
  simpa only [sectionPoly,sectionBody,eval_snd,interp_app,interp_var,
    ← step_shift,interp_ren,OpenTermStandardness.cons,seed_eval] using h

/-- Full external induction at arbitrary lawful source-syntax motives, with the
literal retained uniform section polynomial. No old FormE premise is imposed. -/
theorem dependent_induction {Γ P p s} (hc : FullPER.ContextLaws Γ)
    (hP : FullPER.TypeLaws (N :: Γ) P)
    (hp : FullPER.Fundamental Γ p (inst P zero))
    (hs : FullPER.Fundamental Γ s (dependentStepType P)) :
    FullPER.Fundamental Γ (sectionPoly p s) (.pi N P) := by
  intro ρ η ξ r e n m nm
  have d := (hc.ends r e).1
  let R := ((type_sigma hc (nat_laws Γ) hP).per r d).object
  have run := nm R _ _ (step_related hc hP hs r e) _ _ (seed_related hc hP hp r e)
  have nn := churchPER.trans nm (churchPER.symm nm)
  have tr := hP.transport r (show FullPER.E (N :: Γ) ρ
    (cons (first (n ⬝ interp (totalStep (uncurriedStep s)) η ⬝ interp (totalSeed p) η)) η)
    (cons n η) from ⟨hc.refl r d,run_index p s η nn⟩)
  have body := tr ▸ run.2
  exact (hP.per (η := cons n η) r ⟨d,nn⟩).raw
    (section_eval p s η n).symm (section_eval p s ξ m).symm body

#print axioms sigma_eta
#print axioms sigma_elimination
#print axioms dependent_induction
end JointCompletion
