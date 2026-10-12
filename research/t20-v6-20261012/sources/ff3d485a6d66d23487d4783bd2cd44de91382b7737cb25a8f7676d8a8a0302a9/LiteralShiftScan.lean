import LiteralShiftSyntax

namespace P02.LiteralShift
open P02A2.ObserverCore
open P02.Codec (sequenceList)

/-- One actual scan body step updates exactly the abstract first-cut state. -/
theorem scanBody_step (a b n w k : ℕ) (σ : Store)
    (h : ScanAgrees σ n w (scanChoice a b n w k)) :
    ScanAgrees (exec (scanBody a b) (Function.update σ 3 k)) n w
      (scanChoice a b n w (k+1)) := by
  rcases h with ⟨h0,h1,h4,h5,h6⟩
  cases hc : scanChoice a b n w k with
  | none =>
      simp only [hc, foundValue, branchValue, stopValue] at h4 h5 h6
      by_cases hlo : b * (prefixValue n w (k+1)+1) ≤ a * 2^(k+1)
      · simp_all [ScanAgrees, scanChoice, classify, prefixValue, scanBody,
          sequenceList, exec, evalExpr, lengthExpr, depthExpr, C, V,
          foundValue, branchValue, stopValue, Function.update_apply]
      · by_cases hhi : a * 2^(k+1) ≤ b * prefixValue n w (k+1)
        · simp_all [ScanAgrees, scanChoice, classify, prefixValue, scanBody,
            sequenceList, exec, evalExpr, lengthExpr, depthExpr, C, V,
            foundValue, branchValue, stopValue, Function.update_apply]
          split_ifs
          all_goals simp_all
          all_goals omega
        · simp_all [ScanAgrees, scanChoice, classify, prefixValue, scanBody,
            sequenceList, exec, evalExpr, lengthExpr, depthExpr, C, V,
            foundValue, branchValue, stopValue, Function.update_apply]
          split_ifs
          all_goals simp_all
          all_goals omega
  | some c =>
      simp_all [ScanAgrees, scanChoice, scanBody, sequenceList, exec, evalExpr,
        lengthExpr, depthExpr, C, V, foundValue, branchValue, stopValue,
        Function.update_apply]

theorem runLoop_scan_agrees (a b n w : ℕ) (σ : Store)
    (h : ScanAgrees σ n w none) (k : ℕ) :
    ScanAgrees (runLoop (exec (scanBody a b)) 3 k σ) n w
      (scanChoice a b n w k) := by
  induction k with
  | zero => exact h
  | succ k ih => exact scanBody_step a b n w k _ ih

theorem initialise_agrees (n w : ℕ) :
    ScanAgrees (exec initialise (initial n w)) n w none := by
  simp [ScanAgrees, initialise, initial, sequenceList, exec, evalExpr,
    foundValue, branchValue, stopValue, C, V, Function.update_apply]

def selectedStore (a b n w : ℕ) : Store :=
  exec (scan a b) (exec initialise (initial n w))

/-- Universal selector invariant in the unchanged operational semantics. -/
theorem selectedStore_agrees (a b n w : ℕ) :
    ScanAgrees (selectedStore a b n w) n w (scanChoice a b n w (n+1)) := by
  have hi := initialise_agrees n w
  have hn := hi.1
  simpa only [selectedStore, scan, exec, lengthExpr, evalExpr, C, V, hn] using
    runLoop_scan_agrees a b n w _ hi (n+1)

/-- The unresolved case quantifies every inspected prefix, not a bounded test. -/
theorem scanChoice_none_iff (a b n w k : ℕ) :
    scanChoice a b n w k = none ↔
      ∀ j, 1 ≤ j → j ≤ k → classify a b n w j = none := by
  induction k with
  | zero =>
      constructor
      · intro _ j hj hj0; omega
      · intro _; rfl
  | succ k ih =>
      constructor
      · intro h j hj hjk
        have hk : scanChoice a b n w k = none := by
          cases hc : scanChoice a b n w k with
          | none => rfl
          | some c => simp [scanChoice, hc] at h
        have hlast : classify a b n w (k+1) = none := by
          cases hd : classify a b n w (k+1) with
          | none => rfl
          | some side => simp [scanChoice, hk, hd] at h
        by_cases he : j = k+1
        · simpa [he] using hlast
        · exact ih.mp hk j hj (by omega)
      · intro h
        have hk := ih.mpr (fun j hj hjk => h j hj (by omega))
        have hlast := h (k+1) (by omega) (by omega)
        simp [scanChoice, hk, hlast]

/-- A selected cut is exactly the first resolvable prefix. -/
theorem scanChoice_some_iff (a b n w k : ℕ) (c : Cut) :
    scanChoice a b n w k = some c ↔
      1 ≤ c.depth ∧ c.depth ≤ k ∧
      classify a b n w c.depth = some c.above ∧
      ∀ j, 1 ≤ j → j < c.depth → classify a b n w j = none := by
  induction k with
  | zero => simp [scanChoice]; omega
  | succ k ih =>
      constructor
      · intro h
        cases hc : scanChoice a b n w k with
        | some old =>
            have he : old = c := by simpa [scanChoice, hc] using h
            subst old
            obtain ⟨hp,hu,hd,hearly⟩ := ih.mp hc
            exact ⟨hp, by omega, hd, hearly⟩
        | none =>
            cases hd : classify a b n w (k+1) with
            | none => simp [scanChoice, hc, hd] at h
            | some side =>
                have he : (⟨k+1,side⟩ : Cut) = c := by
                  simpa [scanChoice, hc, hd] using h
                subst c
                dsimp only
                refine ⟨by omega, by omega, hd, ?_⟩
                intro j hj hjk
                exact (scanChoice_none_iff a b n w k).mp hc j hj (by omega)
      · rintro ⟨hp,hu,hd,hearly⟩
        by_cases hck : c.depth ≤ k
        · have hk := ih.mpr ⟨hp,hck,hd,hearly⟩
          simp [scanChoice, hk]
        · have he : c.depth = k+1 := by omega
          have hk := (scanChoice_none_iff a b n w k).mpr
            (fun j hj hjk => hearly j hj (by omega))
          rcases c with ⟨depth,side⟩
          simp only at he
          subst depth
          simp_all [scanChoice]

end P02.LiteralShift
