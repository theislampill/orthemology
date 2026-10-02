import ConditionalAlmostSure

namespace HiddenParity.ResidualSeed.Continuation.Controls
open MeasureTheory
abbrev Bit := Fin 2

def alternating (n : ℕ) : Bit := ⟨n % 2, Nat.mod_lt _ (by decide)⟩

/-- An original AS property need not be tail stable: the first value is zero. -/
theorem original_first_value_ae :
    ∀ᵐ x ∂Measure.dirac alternating, x 0 = 0 := by simp [alternating]

/-- After deleting one coordinate, that same first-value property fails. The
AS transport theorem must use a proved tail-stability or prefix-relative implication. -/
theorem first_value_not_preserved_after_shift :
    ¬ (∀ᵐ x ∂Measure.dirac alternating, (fun n => x (n+1)) 0 = 0) := by
  simp [alternating]

#print axioms original_first_value_ae
#print axioms first_value_not_preserved_after_shift
end HiddenParity.ResidualSeed.Continuation.Controls
