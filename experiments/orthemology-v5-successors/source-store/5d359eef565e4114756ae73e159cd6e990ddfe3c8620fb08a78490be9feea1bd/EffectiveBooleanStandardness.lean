/- Original F/G Boolean standardness and its exact two-choice quotient. -/
import EffectiveCanonicalTests
namespace P01AC.BooleanIdentity
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC.EffectiveCompleteness P01AC.IdentityComplexity

def B : Ty := .all (arr (.param 0) (arr (.param 0) (.param 0)))

def pick (b : Bool) (x y : Term) : Term := if b then y else x
def observe (t : Term) : Term := .app (.app t .zero) .one

def choiceLink (x y : Term) : Link rawPER rawPER where
  rel := fun a c => ∃ b : Bool, Conv a (pick b .zero .one) ∧ Conv c (pick b x y)
  endpoints := fun _ => ⟨.refl _, .refl _⟩
  respect := by
    intro a a' c c' ha hc h
    obtain ⟨b, hb, hd⟩ := h
    exact ⟨b, ha.symm.trans hb, hc.symm.trans hd⟩

theorem choices_separate : ¬ Conv Term.zero Term.one := by
  intro h
  have h0 : P01Source.Normal .zero := by intro u hu; cases hu
  have h1 : P01Source.Normal .one := by intro u hu; cases hu
  have e := P01Source.normal_unique h0 h1 h
  cases e

theorem pick_conv_injective {b c : Bool}
    (h : Conv (pick b .zero .one) (pick c .zero .one)) : b = c := by
  cases b <;> cases c
  · rfl
  · exact False.elim (choices_separate h)
  · exact False.elim (choices_separate h.symm)
  · rfl

theorem boolean_graph {t : Term} {ρ : OEnv} {η : Env}
    (ht : F B ρ η t t) (x y : Term) :
    ∃ b : Bool, Conv (observe t) (pick b .zero .one) ∧
      Conv (.app (.app t x) y) (pick b x y) := by
  have h := ht.1 rawPER rawPER (choiceLink x y)
  change G (arr (.param 0) (arr (.param 0) (.param 0)))
    (extendEnv (choiceLink x y) (diagEnv ρ)) η η t t at h
  rw [G_arr] at h
  have hx : G (.param 0) (extendEnv (choiceLink x y) (diagEnv ρ)) η η .zero x :=
    ⟨false, .refl _, .refl _⟩
  have hy : G (.param 0) (extendEnv (choiceLink x y) (diagEnv ρ)) η η .one y :=
    ⟨true, .refl _, .refl _⟩
  have h1 := h.2.2 .zero x hx
  rw [G_arr] at h1
  exact h1.2.2 .one y hy

/-- Applies to arbitrary self-related semantic inhabitants; no MarkerFree premise. -/
theorem boolean_standardness {t : Term} {ρ : OEnv} {η : Env}
    (ht : F B ρ η t t) :
    ∃ b : Bool, ∀ x y, Conv (.app (.app t x) y) (pick b x y) := by
  obtain ⟨b, hb, _⟩ := boolean_graph ht .zero .one
  refine ⟨b, ?_⟩
  intro x y
  obtain ⟨c, hc, hout⟩ := boolean_graph ht x y
  have e : c = b := pick_conv_injective (hc.symm.trans hb)
  exact e ▸ hout

theorem boolean_same_choice_related {left t : Term} {ρ : OEnv} {η : Env} {b : Bool}
    (hs : F B ρ η left left) (ht : F B ρ η t t)
    (cs : ∀ x y, Conv (.app (.app left x) y) (pick b x y))
    (ct : ∀ x y, Conv (.app (.app t x) y) (pick b x y)) :
    F B ρ η left t := by
  refine ⟨hs.1, ht.1, ?_⟩
  intro P
  change F (arr (.param 0) (arr (.param 0) (.param 0))) (P01F.cons P ρ) η left t
  rw [F_arr]
  intro x x' hx
  rw [F_arr]
  intro y y' hy
  change P.rel (.app (.app left x) y) (.app (.app t x') y')
  have h : P.rel (pick b x y) (pick b x' y') := by
    cases b
    · exact hx
    · exact hy
  exact P.raw (cs x y).symm (ct x' y').symm h

theorem boolean_observation {left t : Term} {ρ : OEnv} {η : Env}
    (h : F B ρ η left t) : Conv (observe left) (observe t) := by
  have h1 := h.2.2 rawPER
  change F (arr (.param 0) (arr (.param 0) (.param 0))) (P01F.cons rawPER ρ) η left t at h1
  rw [F_arr] at h1
  have h2 := h1 .zero .zero (Conv.refl .zero)
  rw [F_arr] at h2
  exact h2 .one .one (Conv.refl .one)

theorem boolean_related_iff_observation {left t : Term} {ρ : OEnv} {η : Env}
    (hs : F B ρ η left left) (ht : F B ρ η t t) :
    F B ρ η left t ↔ Conv (observe left) (observe t) := by
  constructor
  · exact boolean_observation
  · intro h
    obtain ⟨b, hb⟩ := boolean_standardness hs
    obtain ⟨c, hc⟩ := boolean_standardness ht
    have e : b = c := pick_conv_injective ((hb .zero .one).symm.trans (h.trans (hc .zero .one)))
    apply boolean_same_choice_related hs ht hb
    exact e ▸ hc

theorem B_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ B := by
  apply Form.all hΓ
  exact form_arr (.param (ctx_twk hΓ))
    (form_arr (.param (ctx_twk hΓ)) (.param (ctx_twk hΓ)))

/-- The index is unique without a MarkerFree or definability premise. -/
theorem unique_boolean {t : Term} {ρ : OEnv} {η : Env}
    (ht : F B ρ η t t) :
    ∃ b : Bool, (∀ x y, Conv (.app (.app t x) y) (pick b x y)) ∧
      ∀ c : Bool, (∀ x y, Conv (.app (.app t x) y) (pick c x y)) → c = b := by
  obtain ⟨b, hb⟩ := boolean_standardness ht
  refine ⟨b, hb, ?_⟩
  intro c hc
  exact pick_conv_injective ((hc .zero .one).symm.trans (hb .zero .one))

end P01AC.BooleanIdentity
