import FiniteOutputTable

namespace P02.Codec

/-- Every fixed valid or invalid numeric index has a primitive-recursive binary
prefix evaluator. This is pointwise in the index and asserts no uniform PR
evaluator over all program codes. -/
theorem evaluateIndex_fixed_primrec (e : ℕ) : Primrec₂ (evaluateIndex e) := by
  cases hd : decodeIndex e with
  | none =>
      apply ((Primrec.const 0 : Primrec (fun _ : ℕ × ℕ => 0)).to₂).of_eq
      intro n word
      simp [evaluateIndex, hd]
  | some p =>
      by_cases ha : p.arity=2
      · have hp := P02A2.LoopPrimrec.binary_program_primrec p.body p.output
        have hm : Primrec₂ (fun n word =>
            (P02A2.ObserverCore.exec p.body (P02A2.LoopPrimrec.binaryStore n word) p.output)%2) :=
          (Primrec.nat_mod.comp hp (Primrec.const 2)).to₂
        apply hm.of_eq
        intro n word
        simp only [evaluateIndex, hd, ha, ↓reduceIte]
        rfl
      · apply ((Primrec.const 0 : Primrec (fun _ : ℕ × ℕ => 0)).to₂).of_eq
        intro n word
        simp [evaluateIndex, hd, ha]

end P02.Codec
