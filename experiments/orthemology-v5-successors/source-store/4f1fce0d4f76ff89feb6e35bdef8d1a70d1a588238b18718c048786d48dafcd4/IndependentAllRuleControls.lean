/- An unshifted context assumption must not be universally generalized. -/
import AllSoundness
import P01DependentControls

namespace P01AC.IndependentRules
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

theorem parameter_assumption_has : Has [.param 0] (.var 0) (.param 0) :=
  .var (.param (.ext .nil (.param .nil))) .zero

theorem unshifted_parameter_generalization_fails :
    ¬ Has [.param 0] (.var 0) (.all (.param 0)) := by
  intro h
  let ρ : OEnv := fun _ => P01DF.totalPER
  have e : E [.param 0] ρ (cons .i zeroEnv) (cons .i zeroEnv) :=
    ⟨⟨rfl,rfl⟩,trivial⟩
  have u := unary_fundamental h e
  exact u.2.2 botPER

end P01AC.IndependentRules
