import PRSpecialize

namespace P02A2.PRWitnesses
open P02A2.PRProgram P02A2.PRDerivation P02A2.PRRecursion

/-- Recursive first argument plus the fixed second argument. -/
def addition : Code 2 := .prec (.projection 0) (.compose .successor (fun _ => .projection 1))

theorem addition_meaning (a b : ℕ) : meaning addition ![a,b] = b+a := by
  change Nat.rec b (fun _ value => value+1) a = b+a
  induction a with
  | zero => simp
  | succ a ih => simp only [Nat.rec_add_one, ih]; omega

theorem compiled_addition (a b : ℕ) : denote (compile addition) ![a,b] = b+a := by
  rw [compile_correct, addition_meaning]

/-- This recursor returns the last iteration index, exposing argument order. -/
def previousIndex : Code 2 := .prec (.zero 1) (.projection 0)

theorem compiled_previousIndex : denote (compile previousIndex) ![3,7] = 2 := by
  rw [compile_correct]
  rfl

theorem specialized_addition (a b : ℕ) :
    denote (P02A2.PRSpecialize.specialize (compile addition) a) ![b] = b+a := by
  rw [P02A2.PRSpecialize.specialize_correct]
  exact compiled_addition a b

theorem zero_arity_compiles : denote (compile (.zero 0)) Fin.elim0 = 0 := by
  exact compile_correct (.zero 0) Fin.elim0

theorem missing_order_adapter_changes_result :
    denote (primitiveRecProgram (compile (.zero 1)) (compile (.projection (0 : Fin 3)))) ![3,7] = 3 := by
  rw [primitiveRecProgram_correct]
  simp only [compile_correct, meaning]
  rfl

end P02A2.PRWitnesses
