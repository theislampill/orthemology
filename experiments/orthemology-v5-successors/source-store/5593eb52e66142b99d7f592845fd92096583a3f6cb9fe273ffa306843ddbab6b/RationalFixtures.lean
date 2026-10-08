import TraceControls
import Mathlib.Algebra.Order.Field.Rat

namespace TraceControls.Fixtures
open TraceControls

example : (retention : ℚ) = 1/4 := rfl
example : (1-retention : ℚ) = 3/4 := by norm_num [retention]
example : (mass word00 empty : ℚ) = 9/16 := by
  rw [complete_law00]
  norm_num [law00, empty]
example : (mass word01 empty : ℚ) = 9/16 := by
  rw [complete_law01]
  norm_num [law01, empty]
example : tv (mass word00) (mass word01) = (1/4 : ℚ) := one_trace_tv
example (m : ℕ) (hm : 0 < m) : (copiedTV m : ℚ) = 1/4 := duplicate_tv m hm
example : (copiedTV 0 : ℚ) = 0 := zero_data_tv
example (h : Trace → ℚ) (hh : ∀ t, 0 ≤ h t ∧ h t ≤ 1) : success h ≤ 5/8 :=
  randomized_success_bound h hh
example (m : ℕ) (h : (Fin m → Trace) → ℚ)
    (hh : ∀ z, 0 ≤ h z ∧ h z ≤ 1) : duplicateSuccess m h ≤ 5/8 :=
  duplicate_randomized_success_bound m h hh
example (h : (Fin 0 → Trace) → ℚ) : duplicateSuccess 0 h = 1/2 := zero_data_success h
example : (worldMass (false,word00) : Trace → ℚ) = worldMass (true,word00) :=
  same_content_source_law false true word00
example : (conditionalMaskMass (true,false) : ℚ) = 1/2 :=
  (known_word_mask_ambiguity (K := ℚ)).2.2.2.1
example : (conditionalMaskMass (false,true) : ℚ) = 1/2 :=
  (known_word_mask_ambiguity (K := ℚ)).2.2.2.2

end TraceControls.Fixtures
