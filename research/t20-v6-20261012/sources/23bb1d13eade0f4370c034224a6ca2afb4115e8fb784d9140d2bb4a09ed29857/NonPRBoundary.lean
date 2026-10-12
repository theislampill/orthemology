import CodecProgram

/-! A diagonal sharpness control for the exact numeric evaluator. It does not
assert a runtime bound or change the semantics of invalid indices. -/
namespace P02.Codec.NonPRBoundary
open P02.Codec P02A2.PRProgram

theorem evaluateIndex_lt_two (e n word : ℕ) : evaluateIndex e n word < 2 := by
  unfold evaluateIndex
  cases decodeIndex e with
  | none => simp
  | some p => simp only; split_ifs <;> omega

/-- The actual universal evaluator is computable, but cannot be uniformly
primitive recursive in all three natural inputs. -/
theorem evaluateIndex_not_primrec :
    ¬ Primrec (fun input : ℕ × ℕ × ℕ => evaluateIndex input.1 input.2.1 input.2.2) := by
  intro h
  have h0 : Primrec (fun args : Fin 2 → ℕ => args 0) :=
    Primrec.fin_app.comp Primrec.id (Primrec.const 0)
  have h1 : Primrec (fun args : Fin 2 → ℕ => args 1) :=
    Primrec.fin_app.comp Primrec.id (Primrec.const 1)
  have hd : Primrec (fun args : Fin 2 → ℕ => evaluateIndex (args 0) (args 0) (args 1) + 1) :=
    Primrec.nat_add.comp (Primrec.comp h (h0.pair (h0.pair h1))) (Primrec.const 1)
  obtain ⟨p,hp⟩ := P02A2.PRCoverage.exists_program_of_primrec _ hd
  let e := programIndex (pack p)
  have he := evaluateIndex_programIndex p e 0
  rw [hp] at he
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons] at he
  have hb := evaluateIndex_lt_two e e 0
  change evaluateIndex e e 0 = (evaluateIndex e e 0 + 1) % 2 at he
  omega

end P02.Codec.NonPRBoundary
#print axioms P02.Codec.NonPRBoundary.evaluateIndex_lt_two
#print axioms P02.Codec.NonPRBoundary.evaluateIndex_not_primrec
