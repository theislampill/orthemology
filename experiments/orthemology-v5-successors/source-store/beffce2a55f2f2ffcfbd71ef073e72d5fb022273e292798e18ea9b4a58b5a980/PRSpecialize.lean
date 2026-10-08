import PRCoverage

/-! A concrete parameter specializer for a fixed program. The parameter becomes
an actual constant expression in finite generated syntax; no evaluation oracle
is introduced. Numeric serialization/computability is separate. -/
namespace P02A2.PRSpecialize
open P02A2.ObserverCore P02A2.PRProgram

def parameterArgs (n a : ℕ) : Fin (n+1) → Expr :=
  Fin.cons (.constant a) (fun i => .reg i.val)

theorem parameterArgs_fresh (n a : ℕ) :
    ∀ i r, r ∈ P02A2.LoopRenaming.exprRegs (parameterArgs n a i) → r < n+1 := by
  intro i
  refine Fin.cases ?_ (fun j => ?_) i
  · intro r hr
    simp [parameterArgs, P02A2.LoopRenaming.exprRegs] at hr
  · intro r hr
    simp only [parameterArgs, Fin.cons_succ, P02A2.LoopRenaming.exprRegs, Finset.mem_singleton] at hr
    subst r
    omega

def specialize {n : ℕ} (p : Program (n+1)) (a : ℕ) : Program n :=
  ⟨call p (n+1) (parameterArgs n a) n, n⟩

theorem specialize_correct {n : ℕ} (p : Program (n+1)) (a : ℕ) (args : Fin n → ℕ) :
    denote (specialize p a) args = denote p (Fin.cons a args) := by
  unfold denote specialize
  rw [call_value p (n+1) (parameterArgs n a) n (parameterArgs_fresh n a)]
  congr 1
  funext i
  refine Fin.cases ?_ (fun j => ?_) i
  · simp [parameterArgs, evalExpr]
  · simp [parameterArgs, evalExpr, P02A2.LoopPrimrec.extend, j.isLt]

theorem compile_specialize_correct {n : ℕ} (d : P02A2.PRDerivation.Code (n+1))
    (a : ℕ) (args : Fin n → ℕ) :
    denote (specialize (P02A2.PRDerivation.compile d) a) args =
      P02A2.PRDerivation.meaning d (Fin.cons a args) := by
  rw [specialize_correct, P02A2.PRDerivation.compile_correct]

end P02A2.PRSpecialize
