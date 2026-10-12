import TaggedInduction
namespace TaggedInduction
open P01AC P01D TaggedPER
open ImportedOpenTermTransport (interp)

/-- A semantic substitution preserves both supported and related environments. -/
structure SemSub (Γ Δ : Tel) (σ : Nat → Poly) : Prop where
  domain : ∀ {ρ η}, admissible ρ → TaggedPER.D Δ ρ η →
    TaggedPER.D Γ ρ (fun n => interp (σ n) η)
  related : ∀ {ρ η ξ}, admissible ρ → TaggedPER.E Δ ρ η ξ →
    TaggedPER.E Γ ρ (fun n => interp (σ n) η) (fun n => interp (σ n) ξ)

theorem type_sub {Γ Δ A σ} (h : TaggedPER.TypeLaws Γ A) (s : SemSub Γ Δ σ) :
    TaggedPER.TypeLaws Δ (subst σ A) where
  per := by intro ρ η r d; rw [TaggedPER.F_subst]; exact h.per r (s.domain r d)
  transport := by
    intro ρ η ξ r e
    simp only [TaggedPER.F_subst]
    exact h.transport r (s.related r e)

theorem SemSub.lift {Γ Δ σ} (s : SemSub Γ Δ σ) (A : Ty) :
    SemSub (A :: Γ) (subst σ A :: Δ) (pup σ) where
  domain := by
    intro ρ η r d
    rw [← cons_head_tail η,interp_pup]
    exact ⟨s.domain r d.1, (TaggedPER.F_subst A σ ρ (tail η)) ▸ d.2⟩
  related := by
    intro ρ η ξ r e
    rw [← cons_head_tail η, ← cons_head_tail ξ,interp_pup,interp_pup]
    exact ⟨s.related r e.1,(TaggedPER.F_subst A σ ρ (tail η)) ▸ e.2⟩

theorem SemSub.type_lift {Γ Δ σ} (s : SemSub Γ Δ σ) :
    SemSub (twkTel Γ) (twkTel Δ) σ where
  domain := by
    intro ρ η r d
    let ρ' : REnv := fun n => ρ (n+1)
    have hr : admissible ρ' := fun n => r (n+1)
    have eqρ : ρ = cons (ρ 0) ρ' := by funext n; cases n <;> rfl
    rw [eqρ,TaggedPER.D_twk] at d ⊢
    exact s.domain hr d
  related := by
    intro ρ η ξ r e
    let ρ' : REnv := fun n => ρ (n+1)
    have hr : admissible ρ' := fun n => r (n+1)
    have eqρ : ρ = cons (ρ 0) ρ' := by funext n; cases n <;> rfl
    rw [eqρ,TaggedPER.E_twk] at e ⊢
    exact s.related hr e

/-- Substitution retains every component law required by the original soundness
proof, including beneath term and impredicative type binders. -/
theorem hereditary_sub {Γ A} (h : TaggedPER.Hereditary Γ A) {Δ σ} (s : SemSub Γ Δ σ) :
    TaggedPER.Hereditary Δ (subst σ A) := by
  induction A generalizing Γ Δ σ with
  | param n | bottom | raw => exact ⟨type_sub h.1 s,trivial⟩
  | pi A B ia ib | sigma A B ia ib =>
    exact ⟨type_sub h.1 s,ia h.2.1 s,ib h.2.2 (s.lift A)⟩
  | identity A p q ia => exact ⟨type_sub h.1 s,ia h.2 s⟩
  | all B ib => exact ⟨type_sub h.1 s,ib h.2 s.type_lift⟩

theorem SemSub.instantiate {Γ A a} (hc : TaggedPER.ContextLaws Γ)
    (ha : TaggedPER.Fundamental Γ a A) : SemSub (A :: Γ) Γ (P01F.cons a Poly.var) where
  domain := by
    intro ρ η r d
    rw [interp_cons]
    exact ⟨d,ha ρ η η r (hc.refl r d)⟩
  related := by
    intro ρ η ξ r e
    rw [interp_cons,interp_cons]
    exact ⟨e,ha ρ η ξ r e⟩

theorem hereditary_inst {Γ A B a} (hc : TaggedPER.ContextLaws Γ)
    (hB : TaggedPER.Hereditary (A :: Γ) B) (ha : TaggedPER.Fundamental Γ a A) :
    TaggedPER.Hereditary Γ (inst B a) := hereditary_sub hB (SemSub.instantiate hc ha)

theorem context_typewk {Γ} (h : TaggedPER.ContextLaws Γ) : TaggedPER.ContextLaws (twkTel Γ) where
  refl := by
    intro ρ η r d
    let ρ' : REnv := fun n => ρ (n+1)
    have hr : admissible ρ' := fun n => r (n+1)
    have eqρ : ρ = cons (ρ 0) ρ' := by funext n; cases n <;> rfl
    rw [eqρ,TaggedPER.D_twk] at d
    rw [eqρ,TaggedPER.E_twk]
    exact h.refl hr d
  ends := by
    intro ρ η ξ r e
    let ρ' : REnv := fun n => ρ (n+1)
    have hr : admissible ρ' := fun n => r (n+1)
    have eqρ : ρ = cons (ρ 0) ρ' := by funext n; cases n <;> rfl
    rw [eqρ,TaggedPER.E_twk] at e
    rw [eqρ,TaggedPER.D_twk,TaggedPER.D_twk]
    exact h.ends hr e
  sym := by
    intro ρ η ξ r e
    let ρ' : REnv := fun n => ρ (n+1)
    have hr : admissible ρ' := fun n => r (n+1)
    have eqρ : ρ = cons (ρ 0) ρ' := by funext n; cases n <;> rfl
    rw [eqρ,TaggedPER.E_twk] at e ⊢
    exact h.sym hr e
  trans := by
    intro ρ η ξ ζ r e f
    let ρ' : REnv := fun n => ρ (n+1)
    have hr : admissible ρ' := fun n => r (n+1)
    have eqρ : ρ = cons (ρ 0) ρ' := by funext n; cases n <;> rfl
    rw [eqρ,TaggedPER.E_twk] at e f ⊢
    exact h.trans hr e f

theorem hereditary_arr {Γ A B} (hc : TaggedPER.ContextLaws Γ)
    (ha : TaggedPER.Hereditary Γ A) (hb : TaggedPER.Hereditary Γ B) :
    TaggedPER.Hereditary Γ (arr A B) := by
  have sub : SemSub Γ (A :: Γ) (fun n => .var (n+1)) := {
    domain := fun _ d => d.1
    related := fun _ e => e.1 }
  have hw := hereditary_sub hb sub
  exact ⟨type_pi hc ha.laws hw.laws,ha,hw⟩

theorem hereditary_nat {Γ} (hc : TaggedPER.ContextLaws Γ) :
    TaggedPER.Hereditary Γ P01AC.EffectiveCompleteness.N := by
  have c := context_typewk hc
  have hparam : TaggedPER.Hereditary (twkTel Γ) (.param 0) := ⟨type_param _ _,trivial⟩
  have a := hereditary_arr c hparam hparam
  have b := hereditary_arr c a a
  exact ⟨type_all b.laws,b⟩

/-- The exact semantic package consumed by a recursive full-induction rule.
    Motive laws are obtained from its recursive formation proof by the caller. -/
theorem dependent_induction_sound {Γ P p s} (hc : TaggedPER.ContextLaws Γ)
    (hP : TaggedPER.Hereditary (P01AC.EffectiveCompleteness.N :: Γ) P)
    (hp : TaggedPER.Fundamental Γ p (inst P SourceRigidity.zero))
    (hs : TaggedPER.Fundamental Γ s (RigidityInitiality.dependentStepType P)) :
    TaggedPER.TermSound Γ (RigidityInitiality.sectionPoly p s)
      (.pi P01AC.EffectiveCompleteness.N P) :=
  ⟨⟨hc,type_pi hc (nat_laws Γ) hP.laws,hereditary_nat hc,hP⟩,
    dependent_induction hc hP.laws hp hs⟩

#print axioms dependent_induction_sound
#print axioms hereditary_nat
#print hereditary_nat
#print axioms hereditary_sub
#print axioms hereditary_inst
end TaggedInduction
