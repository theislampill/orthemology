import Constructive
import HenkinSoundness
namespace HenkinSigmaCompletion
open P01AC P01D HenkinSoundness
open CaseOperational (T Conv)
open HenkinSourceTransport (interp)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000
@[simp] theorem eval_pair (a b : Poly) (η : HenkinSoundness.Env) :
    interp (pairPoly a b) η = pair (interp a η) (interp b η) := rfl
@[simp] theorem eval_fst (z : Poly) (η : HenkinSoundness.Env) :
    interp (fstPoly z) η = first (interp z η) := rfl
@[simp] theorem eval_snd (z : Poly) (η : HenkinSoundness.Env) :
    interp (sndPoly z) η = second (interp z η) := rfl

theorem sigma_eta {Γ A B z} (hc : HenkinSoundness.ContextLaws Γ) (ha : HenkinSoundness.TypeLaws Γ A)
    (hb : HenkinSoundness.TypeLaws (A :: Γ) B) (hz : HenkinSoundness.Fundamental Γ z (.sigma A B)) :
    HenkinSoundness.Fundamental Γ (.atom .i) (.identity (.sigma A B) z (SigmaCompletion.reconstruct z)) := by
  intro ρ η ξ r e
  have d := (hc.ends r e).1
  have zz := hz ρ η η r (hc.refl r d)
  exact ⟨⟨(ha.per r d).raw (.refl _) (HenkinSourceTransport.fst_pair _ _).symm zz.1,
    (hb.per (η := cons (first (interp z η)) η) r ⟨d,(ha.per r d).left zz.1⟩).raw
      (.refl _) (HenkinSourceTransport.snd_pair _ _).symm zz.2⟩,.refl _,.refl _⟩

theorem sigma_elimination {Γ A B P d z} (hc : HenkinSoundness.ContextLaws Γ)
    (ha : HenkinSoundness.TypeLaws Γ A) (hb : HenkinSoundness.TypeLaws (A :: Γ) B)
    (hP : HenkinSoundness.TypeLaws (.sigma A B :: Γ) P)
    (hd : HenkinSoundness.Fundamental (B :: A :: Γ) d (SigmaCompletion.branchType P))
    (hz : HenkinSoundness.Fundamental Γ z (.sigma A B)) :
    HenkinSoundness.Fundamental Γ (SigmaCompletion.branchAt d (fstPoly z) (sndPoly z)) (inst P z) := by
  intro ρ η ξ r e
  have zz := hz ρ η ξ r e
  have branches : HenkinSoundness.E (B :: A :: Γ) ρ
      (cons (second (interp z η)) (cons (first (interp z η)) η))
      (cons (second (interp z ξ)) (cons (first (interp z ξ)) ξ)) := ⟨⟨e,zz.1⟩,zz.2⟩
  have v := hd ρ _ _ r branches
  have pairEnv : (fun n => interp (SigmaCompletion.pairSub n)
      (cons (second (interp z η)) (cons (first (interp z η)) η))) =
      cons (pair (first (interp z η)) (second (interp z η))) η := by
    funext n; cases n <;> rfl
  rw [SigmaCompletion.branchType, HenkinSoundness.F_subst, pairEnv] at v
  have eta := (sigma_eta hc ha hb hz) ρ η ξ r e
  have tr := hP.transport r (show HenkinSoundness.E (.sigma A B :: Γ) ρ
    (cons (interp (SigmaCompletion.reconstruct z) η) η) (cons (interp z η) η) from
    ⟨hc.refl r (hc.ends r e).1,
      (type_sigma hc ha hb).per r (hc.ends r e).1 |>.sym eta.1⟩)
  rw [HenkinSoundness.F_inst]
  simpa only [SigmaCompletion.branchAt, interp_sub, interp_cons, interp_var] using tr ▸ v

/-- A semantic substitution preserves both supported and related environments. -/
structure SemSub (Γ Δ : Tel) (σ : Nat → Poly) : Prop where
  domain : ∀ {ρ η}, admissible ρ → HenkinSoundness.D Δ ρ η →
    HenkinSoundness.D Γ ρ (fun n => interp (σ n) η)
  related : ∀ {ρ η ξ}, admissible ρ → HenkinSoundness.E Δ ρ η ξ →
    HenkinSoundness.E Γ ρ (fun n => interp (σ n) η) (fun n => interp (σ n) ξ)

theorem type_sub {Γ Δ A σ} (h : HenkinSoundness.TypeLaws Γ A) (s : SemSub Γ Δ σ) :
    HenkinSoundness.TypeLaws Δ (subst σ A) where
  eligible := by intro ρ η r d; rw [HenkinSoundness.F_subst]; exact h.eligible r (s.domain r d)
  per := by intro ρ η r d; rw [HenkinSoundness.F_subst]; exact h.per r (s.domain r d)
  transport := by
    intro ρ η ξ r e
    simp only [HenkinSoundness.F_subst]
    exact h.transport r (s.related r e)

theorem SemSub.lift {Γ Δ σ} (s : SemSub Γ Δ σ) (A : Ty) :
    SemSub (A :: Γ) (subst σ A :: Δ) (pup σ) where
  domain := by
    intro ρ η r d
    rw [← cons_head_tail η,interp_pup]
    exact ⟨s.domain r d.1, (HenkinSoundness.F_subst A σ ρ (tail η)) ▸ d.2⟩
  related := by
    intro ρ η ξ r e
    rw [← cons_head_tail η, ← cons_head_tail ξ,interp_pup,interp_pup]
    exact ⟨s.related r e.1,(HenkinSoundness.F_subst A σ ρ (tail η)) ▸ e.2⟩

theorem SemSub.type_lift {Γ Δ σ} (s : SemSub Γ Δ σ) :
    SemSub (twkTel Γ) (twkTel Δ) σ where
  domain := by
    intro ρ η r d
    let ρ' : REnv := fun n => ρ (n+1)
    have hr : admissible ρ' := fun n => r (n+1)
    have eqρ : ρ = cons (ρ 0) ρ' := by funext n; cases n <;> rfl
    rw [eqρ,HenkinSoundness.D_twk] at d ⊢
    exact s.domain hr d
  related := by
    intro ρ η ξ r e
    let ρ' : REnv := fun n => ρ (n+1)
    have hr : admissible ρ' := fun n => r (n+1)
    have eqρ : ρ = cons (ρ 0) ρ' := by funext n; cases n <;> rfl
    rw [eqρ,HenkinSoundness.E_twk] at e ⊢
    exact s.related hr e

/-- Substitution retains every component law required by the original soundness
proof, including beneath term and impredicative type binders. -/
theorem hereditary_sub {Γ A} (h : HenkinSoundness.Hereditary Γ A) {Δ σ} (s : SemSub Γ Δ σ) :
    HenkinSoundness.Hereditary Δ (subst σ A) := by
  induction A generalizing Γ Δ σ with
  | param n | bottom | raw => exact ⟨type_sub h.1 s,trivial⟩
  | pi A B ia ib | sigma A B ia ib =>
    exact ⟨type_sub h.1 s,ia h.2.1 s,ib h.2.2 (s.lift A)⟩
  | identity A p q ia => exact ⟨type_sub h.1 s,ia h.2 s⟩
  | all B ib => exact ⟨type_sub h.1 s,ib h.2 s.type_lift⟩

theorem SemSub.instantiate {Γ A a} (hc : HenkinSoundness.ContextLaws Γ)
    (ha : HenkinSoundness.Fundamental Γ a A) : SemSub (A :: Γ) Γ (P01F.cons a Poly.var) where
  domain := by
    intro ρ η r d
    rw [interp_cons]
    exact ⟨d,ha ρ η η r (hc.refl r d)⟩
  related := by
    intro ρ η ξ r e
    rw [interp_cons,interp_cons]
    exact ⟨e,ha ρ η ξ r e⟩

theorem hereditary_inst {Γ A B a} (hc : HenkinSoundness.ContextLaws Γ)
    (hB : HenkinSoundness.Hereditary (A :: Γ) B) (ha : HenkinSoundness.Fundamental Γ a A) :
    HenkinSoundness.Hereditary Γ (inst B a) := hereditary_sub hB (SemSub.instantiate hc ha)


#print axioms sigma_eta
#print axioms sigma_elimination
#print axioms hereditary_sub
end HenkinSigmaCompletion
