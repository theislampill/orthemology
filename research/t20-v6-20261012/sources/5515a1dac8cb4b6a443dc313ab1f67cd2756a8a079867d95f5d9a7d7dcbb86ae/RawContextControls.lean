import RawContextUniformity
import IdentityControls

namespace RawContextUniformity.Controls
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N iterationPoly inputNumeral)
open P01AC.ExtensionalRepair.ExactScalarFusion (i)
open P01AC.Intensional.Plus (PolyConvPlus)
open OpenTermStandardness (T iter)
open ImportedOpenTermTransport (interp)

/-- A real free Raw occurrence, erased by an unchanged K computation. -/
def opaqueInput : Poly := .app (.app (.atom .k) (.atom .i)) (.var 0)

theorem opaqueInput_has : HasE (rawTel 1) opaqueInput N := by
  have hi := Structural.has_closed ClosedChurchIdentity.Controls.iTyping
    (ctx_inclusion (rawTel_ctx 1))
  exact .conv (ClosedChurchIdentity.formN (rawTel_ctx 1)) hi
    (PolyConvPlus.k (.atom .i) (.var 0)).symm ⟨⟨trivial,trivial⟩,Nat.zero_lt_succ 0⟩

theorem opaqueInput_count : PolyConvPlus (observe opaqueInput) (iterationPoly 1) :=
  (PolyConvPlus.app (PolyConvPlus.app (PolyConvPlus.k (.atom .i) (.var 2))
    (.refl (.var 1))) (.refl (.var 0))).trans
      (.app (.i (.var 1)) (.refl (.var 0)))

theorem opaqueInput_identity :
    HasE (rawTel 1) i (.identity N opaqueInput (inputNumeral 1)) :=
  raw_canonicity_at_count opaqueInput_has opaqueInput_count

/-- Any polynomial, including nonnormalizing ones, can replace the erased Raw
    argument in this conversion. This makes no strong-normalization claim. -/
theorem opaqueInput_any_argument (p : Poly) :
    PolyConvPlus (psub (fun _ => p) opaqueInput) (.atom .i) := .k _ _

theorem variable_observation_normal :
    OpenDevelopments.Normal (.app (.app (.var 2) (.var 1)) (.var 0)) := by
  intro u h
  cases h with
  | app hf ha =>
    cases ha
    cases hf with
    | app hf ha => cases hf; cases ha; rfl

theorem variable_no_count :
    ¬ ∃ k, PolyConvPlus (observe (.var 0)) (iterationPoly k) := by
  rintro ⟨k,hk⟩
  have hc := ImportedOpenTermTransport.source_plus_sound hk T.var
  rw [ClosedScalarInstances.iteration_interp] at hc
  have he := OpenDevelopments.normal_unique variable_observation_normal
    (OpenDevelopments.iter_normal k) hc
  cases k with
  | zero => cases he
  | succ k => cases T.app.inj he |>.1

theorem raw_variable_not_church : ¬ HasE (rawTel 1) (.var 0) N := by
  intro h
  exact variable_no_count (raw_uniform_iteration h)

/-- A Church hypothesis really can be a Church variable, so replacing Raw by N
    invalidates the generic-conversion conclusion. -/
theorem church_variable_has : HasE [N] (.var 0) N := by
  have hΓ : Ctx [N] := .ext .nil (EffectiveCompleteness.N_form .nil)
  exact .var (ClosedChurchIdentity.formN hΓ) .zero

theorem general_context_count_is_false :
    ¬ (∀ {Γ n}, HasE Γ n N → ∃ k, PolyConvPlus (observe n) (iterationPoly k)) := by
  intro h
  exact variable_no_count (h church_variable_has)

theorem count_unique {n : Poly} {j k : Nat}
    (hj : PolyConvPlus (observe n) (iterationPoly j))
    (hk : PolyConvPlus (observe n) (iterationPoly k)) : j = k := by
  have hc := ImportedOpenTermTransport.source_plus_sound (hj.symm.trans hk) T.var
  simp only [ClosedScalarInstances.iteration_interp] at hc
  exact OpenDevelopments.iter_conv_injective hc

#print axioms opaqueInput_identity
#print axioms opaqueInput_any_argument
#print axioms raw_variable_not_church
#print axioms church_variable_has
#print axioms general_context_count_is_false
#print axioms count_unique
end RawContextUniformity.Controls
