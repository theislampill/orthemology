/- The fresh raw-Conv-refining relation and literal zero-padded telescopes.
   No claim of arbitrary pointwise-conversion closure of V is made. -/
import IntensionalIdentitySoundness
namespace P01AC.Intensional
open OrthemologyV2 OrthemologyV3 P01D
open P01F (cons)

/-- The independent relation from the written proof, not inherited P01AC.E. -/
def E : Tel → SEnv → Env → Env → Prop
  | [], _, η, ξ => η = zeroEnv ∧ ξ = zeroEnv
  | A :: Γ, ρ, η, ξ => E Γ ρ (tail η) (tail ξ) ∧ R A ρ (tail η) (η 0) (ξ 0)

/-- E is precisely raw pointwise conversion between two admissible valuations. -/
theorem E_characterisation (Γ : Tel) (ρ : SEnv) (η ξ : Env) :
    E Γ ρ η ξ ↔ V Γ ρ η ∧ V Γ ρ ξ ∧ EnvConv η ξ := by
  induction Γ generalizing η ξ with
  | nil =>
    constructor
    · rintro ⟨rfl,rfl⟩
      exact ⟨rfl,rfl,fun _ => .refl _⟩
    · intro h
      exact ⟨h.1,h.2.1⟩
  | cons A Γ ih =>
    constructor
    · intro h
      obtain ⟨vl,vr,tc⟩ := (ih (tail η) (tail ξ)).mp h.1
      refine ⟨⟨vl,h.2.1⟩,⟨vr,?_⟩,?_⟩
      · have hh := h.2.2.1
        unfold mem at hh ⊢
        rw [interp_coherent A ρ (tail η) (tail ξ) tc] at hh
        exact hh
      · intro n
        cases n with
        | zero => exact h.2.2.2
        | succ n => exact tc n
    · intro h
      have tc : EnvConv (tail η) (tail ξ) := fun n => h.2.2 (n+1)
      refine ⟨(ih (tail η) (tail ξ)).mpr ⟨h.1.1,h.2.1.1,tc⟩,
        h.1.2, ?_, h.2.2 0⟩
      have hh := h.2.1.2
      unfold mem at hh ⊢
      rw [interp_coherent A ρ (tail η) (tail ξ) tc]
      exact hh

theorem E_refl {Γ ρ η} (h : V Γ ρ η) : E Γ ρ η η :=
  (E_characterisation Γ ρ η η).mpr ⟨h,h,fun _ => .refl _⟩

theorem E_symm {Γ ρ η ξ} (h : E Γ ρ η ξ) : E Γ ρ ξ η := by
  obtain ⟨a,b,c⟩ := (E_characterisation Γ ρ η ξ).mp h
  exact (E_characterisation Γ ρ ξ η).mpr ⟨b,a,fun n => .symm (c n)⟩

theorem E_trans {Γ ρ η ξ ζ} (h : E Γ ρ η ξ) (k : E Γ ρ ξ ζ) : E Γ ρ η ζ := by
  obtain ⟨a,b,c⟩ := (E_characterisation Γ ρ η ξ).mp h
  obtain ⟨d,e,f⟩ := (E_characterisation Γ ρ ξ ζ).mp k
  exact (E_characterisation Γ ρ η ζ).mpr ⟨a,e,fun n => .trans (c n) (f n)⟩

theorem E_twk (Γ : Tel) (ρ : SEnv) (η ξ : Env) (X : Sat) :
    E (twkTel Γ) (cons X ρ) η ξ ↔ E Γ ρ η ξ := by
  rw [E_characterisation, E_characterisation, V_twk, V_twk]

/-- Both J coordinates are retained: proof at 0, endpoint at 1. -/
theorem V_theta (Γ : Tel) (A : Ty) (x : Poly) (ρ : SEnv) (η : Env) (y e : Term) :
    V (theta Γ A x) ρ (cons e (cons y η)) ↔
      V Γ ρ η ∧ mem A ρ η y ∧ mem A ρ η (eval x η) ∧
      Conv (eval x η) y ∧ Conv e .i := by
  change (V Γ ρ η ∧ mem A ρ η y) ∧
    mem (.identity (wk A) (pren Nat.succ x) (.var 0)) ρ (cons y η) e ↔ _
  change (V Γ ρ η ∧ mem A ρ η y) ∧
    (mem (wk A) ρ (cons y η) (eval (pren Nat.succ x) (cons y η)) ∧
     mem (wk A) ρ (cons y η) y ∧
     Conv (eval (pren Nat.succ x) (cons y η)) y ∧ Conv e .i) ↔ _
  simp only [mem, interp_wk, eval_ren, cons]
  constructor
  · intro h
    exact ⟨h.1.1,h.1.2,h.2.1,h.2.2.2.1,h.2.2.2.2⟩
  · intro h
    exact ⟨⟨h.1,h.2.1⟩,h.2.2.1,h.2.1,h.2.2.2.1,h.2.2.2.2⟩

theorem V_theta_base {Γ A x ρ η} (v : V Γ ρ η) (hx : mem A ρ η (eval x η)) :
    V (theta Γ A x) ρ (cons .i (cons (eval x η) η)) :=
  (V_theta Γ A x ρ η (eval x η) .i).mpr ⟨v,hx,hx,.refl _,.refl _⟩

/-- The base and target J environments are related in their admissible telescope. -/
theorem E_theta {Γ A x ρ η y e} (v : V Γ ρ η)
    (hy : mem A ρ η y) (hx : mem A ρ η (eval x η))
    (xy : Conv (eval x η) y) (ei : Conv e .i) :
    E (theta Γ A x) ρ (cons .i (cons (eval x η) η)) (cons e (cons y η)) := by
  apply (E_characterisation _ _ _ _).mpr
  refine ⟨V_theta_base v hx, (V_theta Γ A x ρ η y e).mpr ⟨v,hy,hx,xy,ei⟩, ?_⟩
  exact envConv_cons (envConv_cons (fun _ => .refl _) xy) (.symm ei)

/-- Unary soundness plus raw evaluation coherence yields the stated relation.
    Both inputs still satisfy the literal zero-padded telescope. -/
theorem semantic_relational {Γ p A} (h : SemanticHas Γ p A) {ρ η ξ}
    (e : E Γ ρ η ξ) : R A ρ η (eval p η) (eval p ξ) := by
  obtain ⟨a,b,c⟩ := (E_characterisation Γ ρ η ξ).mp e
  have right := h ρ ξ b
  unfold mem at right
  rw [←interp_coherent A ρ η ξ c] at right
  exact ⟨h ρ η a,right,eval_coherent p c⟩

theorem relational_fundamental {Γ p A} (h : Has Γ p A) {ρ η ξ}
    (e : E Γ ρ η ξ) : R A ρ η (eval p η) (eval p ξ) :=
  semantic_relational (has_sound h) e

theorem relational_fundamental_plus {Γ p A} (h : Plus.HasPlus Γ p A) {ρ η ξ}
    (e : E Γ ρ η ξ) : R A ρ η (eval p η) (eval p ξ) :=
  semantic_relational (hasPlus_sound h) e

end P01AC.Intensional
