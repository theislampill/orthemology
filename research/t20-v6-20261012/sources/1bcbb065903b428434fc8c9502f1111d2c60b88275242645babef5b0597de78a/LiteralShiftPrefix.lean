import LiteralShiftCorrect
import LiteralShiftWord

/-! Pointwise stream refinement of the literal `compile_shift` AST.  These
results derive the copied prefix, exact fresh-tail replay, and unresolved
stream directly from finite execution.  No probability law is assumed. -/
namespace P02.LiteralShift
open P02A2.ObserverCore

def programValue (body : Stmt) (output n w : ℕ) : ℕ :=
  exec body (initial n w) output

def compiledOutput (body : Stmt) (output a b : ℕ) : (ℕ → Bool) → (ℕ → Bool) :=
  P02A2.ObserverCore.output (programValue (compileShift body output a b) 2)

/-- A first resolvable source prefix, measured by its number of bits. -/
def FirstCut (a b : ℕ) (x : ℕ → Bool) (k : ℕ) (side : Bool) : Prop :=
  1 ≤ k ∧ streamClassify a b x k = some side ∧
    ∀ j, 1 ≤ j → j < k → streamClassify a b x j = none

/-- First-cut and indefinitely unresolved cases cover every input stream. -/
theorem firstCut_or_unresolved (a b : ℕ) (x : ℕ → Bool) :
    (∃ k side, FirstCut a b x k side) ∨
      (∀ k, 1 ≤ k → streamClassify a b x k = none) := by
  classical
  by_cases h : ∃ k, 1 ≤ k ∧ streamClassify a b x k ≠ none
  · left
    obtain ⟨hk,hne⟩ := Nat.find_spec h
    cases hc : streamClassify a b x (Nat.find h) with
    | none => exact (hne hc).elim
    | some side =>
        refine ⟨Nat.find h, side, hk, hc, ?_⟩
        intro j hj hjk
        by_contra hjc
        have hm := Nat.find_min' h ⟨hj,hjc⟩
        omega
  · right
    intro k hk
    by_contra hc
    exact h ⟨k,hk,hc⟩

theorem compiledOutput_unresolved_at (body : Stmt) (output a b n : ℕ)
    (x : ℕ → Bool)
    (h : ∀ j, 1 ≤ j → j ≤ n+1 → streamClassify a b x j = none) :
    compiledOutput body output a b x n = x n := by
  unfold compiledOutput P02A2.ObserverCore.output programValue
  change decide (exec (compileShift body output a b)
    (initial n (sentinel (streamPrefix x (n+1)))) 2 % 2 = 1) = _
  rw [compileShift_unresolved body output a b n _ (by
    intro j hj hjn
    rw [classify_stream a b n j x hjn]
    exact h j hj hjn), Nat.mod_mod, sentinel_stream_last]
  cases x n <;> rfl

/-- Every bit before and at the first stopping prefix is copied. -/
theorem compiledOutput_copied_prefix (body : Stmt) (output a b k n : ℕ)
    (x : ℕ → Bool) (side : Bool) (h : FirstCut a b x k side) (hn : n < k) :
    compiledOutput body output a b x n = x n := by
  rcases h with ⟨hk,hc,hearly⟩
  by_cases he : n+1 = k
  · unfold compiledOutput P02A2.ObserverCore.output programValue
    change decide (exec (compileShift body output a b)
      (initial n (sentinel (streamPrefix x (n+1)))) 2 % 2 = 1) = _
    rw [compileShift_stopping body output a b n _ side (by
      rw [classify_stream a b n (n+1) x (by omega), he]
      exact hc) (by
      intro j hj hjn
      rw [classify_stream a b n j x (by omega)]
      exact hearly j hj (by omega)), Nat.mod_mod, sentinel_stream_last]
    cases x n <;> rfl
  · apply compiledOutput_unresolved_at
    intro j hj hjn
    exact hearly j hj (by omega)

/-- A below-threshold first cut continues to copy the entire source stream. -/
theorem compiledOutput_below (body : Stmt) (output a b k : ℕ)
    (x : ℕ → Bool) (h : FirstCut a b x k false) :
    compiledOutput body output a b x = x := by
  funext n
  by_cases hn : n < k
  · exact compiledOutput_copied_prefix body output a b k n x false h hn
  · rcases h with ⟨hk,hc,hearly⟩
    unfold compiledOutput P02A2.ObserverCore.output programValue
    change decide (exec (compileShift body output a b)
      (initial n (sentinel (streamPrefix x (n+1)))) 2 % 2 = 1) = _
    rw [compileShift_below body output a b n _ k hk (by omega) (by
      rw [classify_stream a b n k x (by omega)]
      exact hc) (by
      intro j hj hjk
      rw [classify_stream a b n j x (by omega)]
      exact hearly j hj hjk), Nat.mod_mod, sentinel_stream_last]
    cases x n <;> rfl

/-- Above a first cut, the exact original inline body is run from a clean
store on the fresh tail, with stage reset to zero at its first bit. -/
theorem compiledOutput_above_tail (body : Stmt) (output a b k n : ℕ)
    (x : ℕ → Bool) (h : FirstCut a b x k true) (hkn : k ≤ n) :
    compiledOutput body output a b x n =
      P02A2.ObserverCore.output (programValue body output) (dropStream k x) (n-k) := by
  rcases h with ⟨hk,hc,hearly⟩
  unfold compiledOutput P02A2.ObserverCore.output programValue
  change decide (exec (compileShift body output a b)
    (initial n (sentinel (streamPrefix x (n+1)))) 2 % 2 = 1) = _
  rw [compileShift_above body output a b n _ k hk hkn (by
    rw [classify_stream a b n k x (by omega)]
    exact hc) (by
    intro j hj hjk
    rw [classify_stream a b n j x (by omega)]
    exact hearly j hj hjk), Nat.mod_mod, replayWord_stream]
  have hstage : n+1-k-1 = n-k := by omega
  have hlength : n+1-k = n-k+1 := by omega
  rw [hstage, hlength]
  rfl

/-- The complete pointwise splice statement for every first cut. -/
theorem compiledOutput_on_firstCut (body : Stmt) (output a b k : ℕ)
    (x : ℕ → Bool) (side : Bool) (h : FirstCut a b x k side) (n : ℕ) :
    compiledOutput body output a b x n =
      if n < k then x n
      else if side then
        P02A2.ObserverCore.output (programValue body output) (dropStream k x) (n-k)
      else x n := by
  by_cases hn : n < k
  · rw [if_pos hn]
    exact compiledOutput_copied_prefix body output a b k n x side h hn
  · rw [if_neg hn]
    cases side with
    | false => exact congrFun (compiledOutput_below body output a b k x h) n
    | true => exact compiledOutput_above_tail body output a b k n x h (by omega)

/-- An indefinitely unresolved input is copied pointwise, without a
termination assumption or an exceptional-set assumption. -/
theorem compiledOutput_unresolved (body : Stmt) (output a b : ℕ)
    (x : ℕ → Bool)
    (h : ∀ k, 1 ≤ k → streamClassify a b x k = none) :
    compiledOutput body output a b x = x := by
  funext n
  apply compiledOutput_unresolved_at
  intro j hj _
  exact h j hj

end P02.LiteralShift
