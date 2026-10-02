import FixedIndexPrimrec

namespace P02A2.FiniteOutputTable

/-- The actual two-bit source enumeration gives the uniform identity table. -/
theorem echo_two_bit_probability (w : Fin 2 → Bool) :
    tableProbability (fun _ word => word) 2 w = 1/4 := by
  fin_cases w <;> decide +kernel

theorem zero_two_bit_probability :
    tableProbability (fun _ _ => 0) 2 (fun _ => false) = 1 := by
  decide +kernel

theorem zero_cannot_emit_true :
    tableProbability (fun _ _ => 0) 1 (fun _ => true) = 0 := by
  decide +kernel

/-- Each stage uses only its available prefix, not the complete N-bit word. -/
theorem first_input_then_zero :
    tableProbability (fun n word => if n=0 then word else 0) 2 ![true,false] = 1/2 := by
  decide +kernel

end P02A2.FiniteOutputTable
