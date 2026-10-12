import LiteralShiftScan
import LiteralShiftReplay

namespace P02.LiteralShift
open P02A2.ObserverCore
open P02.Codec (sequenceList)

def specifiedValue (body : Stmt) (output a b n w : ℕ) : ℕ :=
  match scanChoice a b n w (n+1) with
  | none => w % 2
  | some c =>
      if c.above && decide (c.depth ≤ n) then
        exec body (initial (n+1-c.depth-1)
          (2^(n+1-c.depth) + w % 2^(n+1-c.depth))) output % 2
      else w % 2

/-- Literal outer Seq grouping, with no altered selector or replay program. -/
theorem compileShift_exec (body : Stmt) (output a b : ℕ) (σ : Store) :
    exec (compileShift body output a b) σ =
      exec (finish body output) (exec (scan a b) (exec initialise σ)) := rfl

/-- Universal finite-stage equality for the source-faithful generated AST.
The theorem deliberately quantifies every natural numerical word.  The Python
entry-point correspondence additionally requires b>0 and a≤b because Python
rejects the other parameter pairs before constructing its AST. -/
theorem compileShift_correct (body : Stmt) (output a b n w : ℕ) :
    exec (compileShift body output a b) (initial n w) 2 =
      specifiedValue body output a b n w := by
  rw [compileShift_exec]
  change exec (finish body output) (selectedStore a b n w) 2 = _
  obtain ⟨h0,h1,h4,h5,h6⟩ := selectedStore_agrees a b n w
  rw [finish_correct body output n w _ h0 h1, h4, h5, h6]
  cases hc : scanChoice a b n w (n+1) with
  | none => simp [specifiedValue, hc, foundValue, branchValue, stopValue]
  | some c =>
      cases hs : c.above <;>
        simp [specifiedValue, hc, hs, foundValue, branchValue, stopValue]

theorem compileShift_unresolved (body : Stmt) (output a b n w : ℕ)
    (h : ∀ j, 1 ≤ j → j ≤ n+1 → classify a b n w j = none) :
    exec (compileShift body output a b) (initial n w) 2 = w % 2 := by
  rw [compileShift_correct]
  simp [specifiedValue, (scanChoice_none_iff a b n w (n+1)).mpr h]

theorem compileShift_below (body : Stmt) (output a b n w k : ℕ)
    (hk : 1 ≤ k) (hkn : k ≤ n+1)
    (hc : classify a b n w k = some false)
    (hearly : ∀ j, 1 ≤ j → j < k → classify a b n w j = none) :
    exec (compileShift body output a b) (initial n w) 2 = w % 2 := by
  rw [compileShift_correct]
  have hs := (scanChoice_some_iff a b n w (n+1) ⟨k,false⟩).mpr
    ⟨hk,hkn,hc,hearly⟩
  simp [specifiedValue, hs]

theorem compileShift_stopping (body : Stmt) (output a b n w : ℕ) (side : Bool)
    (hc : classify a b n w (n+1) = some side)
    (hearly : ∀ j, 1 ≤ j → j < n+1 → classify a b n w j = none) :
    exec (compileShift body output a b) (initial n w) 2 = w % 2 := by
  rw [compileShift_correct]
  have hs := (scanChoice_some_iff a b n w (n+1) ⟨n+1,side⟩).mpr
    ⟨by dsimp; omega,by dsimp; omega,hc,hearly⟩
  simp [specifiedValue, hs]

theorem compileShift_above (body : Stmt) (output a b n w k : ℕ)
    (hk : 1 ≤ k) (hkn : k ≤ n)
    (hc : classify a b n w k = some true)
    (hearly : ∀ j, 1 ≤ j → j < k → classify a b n w j = none) :
    exec (compileShift body output a b) (initial n w) 2 =
      exec body (initial (n+1-k-1) (2^(n+1-k)+w%2^(n+1-k))) output % 2 := by
  rw [compileShift_correct]
  have hs := (scanChoice_some_iff a b n w (n+1) ⟨k,true⟩).mpr
    ⟨hk,by dsimp; omega,hc,hearly⟩
  simp [specifiedValue, hs, hkn]

theorem compileShift_bit (body : Stmt) (output a b n w : ℕ) :
    exec (compileShift body output a b) (initial n w) 2 < 2 := by
  rw [compileShift_correct]
  unfold specifiedValue
  split
  · exact Nat.mod_lt _ (by omega)
  · split_ifs <;> exact Nat.mod_lt _ (by omega)

end P02.LiteralShift
