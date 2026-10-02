import PRRecursion

/-! Input-order adapters connect the source's last-argument recursion macro
with the conventional first-argument presentation used by Nat.Primrec'. -/
namespace P02A2.PRHeadRecursion
open P02A2.ObserverCore P02A2.PRProgram P02A2.PRComposition P02A2.PRRecursion

def permuteProgram {n m : ℕ} (p : Program m) (π : Fin m → Fin n) : Program n :=
  composeProgram p (fun i => projectionProgram n (π i))

theorem permuteProgram_correct {n m : ℕ} (p : Program m) (π : Fin m → Fin n) (args : Fin n → ℕ) :
    denote (permuteProgram p π) args = denote p (fun i => args (π i)) := by
  rw [permuteProgram, composeProgram_correct]
  simp only [projectionProgram_correct]

def inputPermutation (k : ℕ) : Fin (k+1) → Fin (k+1) :=
  Fin.lastCases 0 (fun i => i.succ)

def stepPermutation (k : ℕ) : Fin (k+2) → Fin (k+2) :=
  Fin.cases (Fin.castSucc (Fin.last k))
    (Fin.cases (Fin.last (k+1)) (fun i => i.castSucc.castSucc))

theorem inputPermutation_castSucc (k : ℕ) (i : Fin k) : inputPermutation k i.castSucc = i.succ := by
  simp [inputPermutation]

theorem inputPermutation_last (k : ℕ) : inputPermutation k (Fin.last k) = 0 := by
  simp [inputPermutation]

theorem stepPermutation_values {k : ℕ} (args : Fin k → ℕ) (index value : ℕ) :
    (fun i => appendTwo args index value (stepPermutation k i)) = Fin.cons index (Fin.cons value args) := by
  funext i
  refine Fin.cases ?_ (fun j => Fin.cases ?_ (fun t => ?_) j) i
  · simp [stepPermutation, appendTwo]
  · change appendTwo args index value (stepPermutation k (Fin.succ (0 : Fin (k+1)))) = value
    simp only [stepPermutation, Fin.cases_succ, Fin.cases_zero]
    simp [appendTwo]
  · simp [stepPermutation, appendTwo, t.isLt]

def headRecProgram {k : ℕ} (g : Program k) (h : Program (k+2)) : Program (k+1) :=
  permuteProgram (primitiveRecProgram g (permuteProgram h (stepPermutation k))) (inputPermutation k)

theorem headRecProgram_correct {k : ℕ} (g : Program k) (h : Program (k+2)) (args : Fin (k+1) → ℕ) :
    denote (headRecProgram g h) args =
      (args 0).rec (denote g (fun i => args i.succ))
        (fun j value => denote h (Fin.cons j (Fin.cons value (fun i => args i.succ)))) := by
  rw [headRecProgram, permuteProgram_correct, primitiveRecProgram_correct]
  simp only [inputPermutation_last, inputPermutation_castSucc]
  simp_rw [permuteProgram_correct, stepPermutation_values]

end P02A2.PRHeadRecursion
