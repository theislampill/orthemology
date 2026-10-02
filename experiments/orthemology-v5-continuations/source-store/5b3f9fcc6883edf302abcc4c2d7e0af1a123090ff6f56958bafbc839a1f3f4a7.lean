import CodecProgram

namespace P02.Codec
open P02A2.PRProgram P02A2.PRSpecialize P02A2.PRDerivation

/-- Actual P02-L1 numeric code obtained by literal specialization of a fixed
ternary program to the binary observer inputs n, word. -/
def parameterIndex (p : Program 3) (a : ℕ) : ℕ := programIndex (pack (specialize p a))

theorem parameterIndex_correct (p : Program 3) (a n word : ℕ) :
    evaluateIndex (parameterIndex p a) n word = denote p ![a,n,word] % 2 := by
  rw [parameterIndex, evaluateIndex_programIndex, specialize_correct]
  rfl

theorem derivation_parameterIndex_correct (d : Code 3) (a n word : ℕ) :
    evaluateIndex (parameterIndex (compile d) a) n word = meaning d ![a,n,word] % 2 := by
  rw [parameterIndex_correct, compile_correct]

/-- A fixed joint PR family has one fixed program whose numeric literal sections
realise that family. The numeric map's Primrec proof is a separate theorem. -/
theorem exists_parameterIndex_of_primrec (f : (Fin 3 → ℕ) → ℕ) (hf : Primrec f) :
    ∃ p : Program 3, ∀ a n word, evaluateIndex (parameterIndex p a) n word = f ![a,n,word] % 2 := by
  obtain ⟨p,hp⟩ := P02A2.PRCoverage.exists_program_of_primrec f hf
  exact ⟨p, fun a n word => (parameterIndex_correct p a n word).trans (congrArg (· % 2) (hp _))⟩

end P02.Codec
