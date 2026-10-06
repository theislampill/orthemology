import PRHeadRecursion
import Mathlib.Computability.Primrec

/-! Explicit arity-indexed primitive-recursive derivations and a structural
compiler to the unchanged LOOP grammar. Finite child families are represented
as Fin m → Code n, not by an evaluator/oracle constructor. Numeric serialization
of this typed presentation is a separate obligation. -/
namespace P02A2.PRDerivation
open P02A2.PRProgram P02A2.PRComposition P02A2.PRHeadRecursion

inductive Code : ℕ → Type where
  | zero (n : ℕ) : Code n
  | successor : Code 1
  | projection {n : ℕ} (i : Fin n) : Code n
  | compose {n m : ℕ} (f : Code m) (gs : Fin m → Code n) : Code n
  | prec {n : ℕ} (g : Code n) (h : Code (n+2)) : Code (n+1)

def meaning : {n : ℕ} → Code n → (Fin n → ℕ) → ℕ
  | _, .zero _, _ => 0
  | _, .successor, args => args 0 + 1
  | _, .projection i, args => args i
  | _, .compose f gs, args => meaning f (fun i => meaning (gs i) args)
  | _, .prec g h, args => (args 0).rec (meaning g (fun i => args i.succ))
      (fun j value => meaning h (Fin.cons j (Fin.cons value (fun i => args i.succ))))

def compile : {n : ℕ} → Code n → Program n
  | _, .zero n => zeroProgram n
  | _, .successor => successorProgram
  | _, .projection i => projectionProgram _ i
  | _, .compose f gs => composeProgram (compile f) (fun i => compile (gs i))
  | _, .prec g h => headRecProgram (compile g) (compile h)

theorem compile_correct {n : ℕ} (d : Code n) (args : Fin n → ℕ) :
    denote (compile d) args = meaning d args := by
  induction d with
  | zero n => exact zeroProgram_correct n args
  | successor => exact successorProgram_correct args
  | projection i => exact projectionProgram_correct _ i args
  | compose f gs ihf ihgs =>
      rw [compile, composeProgram_correct, ihf]
      change meaning f (fun i => denote (compile (gs i)) args) = meaning f (fun i => meaning (gs i) args)
      congr 1
      funext i
      exact ihgs i args
  | prec g h ihg ihh =>
      rw [compile, headRecProgram_correct]
      simp only [meaning]
      simp_rw [ihg, ihh]

theorem meaning_primitive_recursive {n : ℕ} (d : Code n) : Primrec (meaning d) := by
  have hp := P02A2.LoopPrimrec.program_denotation_primrec n (compile d).body (compile d).output
  exact hp.of_eq (fun args => compile_correct d args)

end P02A2.PRDerivation
