import LoopPrimrec
import Q8Compiler

/-! Class membership of the actual generated Q8 prefix function.
This does not assert that evaluation uniformly in the code is primitive
recursive, nor certify a numeric code transformer or hierarchy reduction. -/
namespace P02A2.Q8Primrec
open P02A2.Q8Machine P02A2.Q8Compiler

theorem generated_prefix_function_primrec {n : ℕ} (M : Machine n) :
    Primrec₂ (programValue M) := by
  simpa only [programValue, inputStore, P02A2.LoopPrimrec.binaryStore] using
    P02A2.LoopPrimrec.binary_program_primrec (compiled M) 2

end P02A2.Q8Primrec
