import Sigma2RowLaw
import LoopPrimrec

/-! The PR matrix premise is discharged for any fixed arity-three program
in the recovered LOOP grammar. The candidate search is still the explicit
mathematical prefix family, not a proof about emitted Python byte codes. -/
namespace P02A2.Sigma2SourceMatrix
open P02A2.ObserverCore P02A2.LoopPrimrec

def tripleInput (p : (ℕ × ℕ) × ℕ) : FinStore 3 :=
  fun i => if i.val = 0 then p.1.1 else if i.val = 1 then p.1.2 else p.2

theorem tripleInput_primrec : Primrec tripleInput := by
  apply Primrec.fin_curry.mpr
  apply Primrec₂.swap
  apply Primrec.fin_curry₁.mpr
  intro i
  fin_cases i
  · simpa [tripleInput] using (Primrec.fst.comp Primrec.fst : Primrec (fun p : (ℕ × ℕ) × ℕ => p.1.1))
  · simpa [tripleInput] using (Primrec.snd.comp Primrec.fst : Primrec (fun p : (ℕ × ℕ) × ℕ => p.1.2))
  · simpa [tripleInput] using (Primrec.snd : Primrec (fun p : (ℕ × ℕ) × ℕ => p.2))

def matrix (body : Stmt) (output : ℕ) (e s t : ℕ) : Prop :=
  exec body (extend (tripleInput ((e,s),t))) output ≠ 0

instance matrix_decidable (body : Stmt) (output e s t : ℕ) :
    Decidable (matrix body output e s t) := inferInstanceAs (Decidable (_ ≠ (0 : ℕ)))

theorem matrix_primrec (body : Stmt) (output : ℕ) :
    PrimrecRel (fun p : ℕ × ℕ => matrix body output p.1 p.2) :=
  (Primrec.eq.comp ((program_denotation_primrec 3 body output).comp tripleInput_primrec)
    (Primrec.const 0)).not

theorem source_prefix_primrec (body : Stmt) (output : ℕ) :
    Primrec₂ (fun p : ℕ × ℕ => P02A2.SurvivorPrimrec.prefixFunction (matrix body output) p.1 p.2) :=
  P02A2.Sigma2RowLaw.joint_prefix_primitive_recursive (matrix body output) (matrix_primrec body output)

theorem source_row_zero_iff (body : Stmt) (output e : ℕ) :
    defect (P02A2.Sigma2RowLaw.rowLaw (matrix body output) e) = 0 ↔
      ∃ s, ∀ t, exec body (extend (tripleInput ((e,s),t))) output ≠ 0 :=
  P02A2.Sigma2RowLaw.defect_zero_iff_witness (matrix body output) e

theorem source_row_one_iff (body : Stmt) (output e : ℕ) :
    defect (P02A2.Sigma2RowLaw.rowLaw (matrix body output) e) = 1 ↔
      ¬ ∃ s, ∀ t, exec body (extend (tripleInput ((e,s),t))) output ≠ 0 :=
  P02A2.Sigma2RowLaw.defect_one_iff_no_witness (matrix body output) e

end P02A2.Sigma2SourceMatrix
