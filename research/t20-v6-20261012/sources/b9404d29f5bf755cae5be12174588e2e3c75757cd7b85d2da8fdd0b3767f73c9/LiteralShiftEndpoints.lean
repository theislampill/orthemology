import LiteralShiftCorrect

namespace P02.LiteralShift
open P02A2.ObserverCore

/-- The scan reads the low observed word, even without the standard sentinel. -/
theorem prefixValue_lowBits (n w k : ℕ) (hk : k ≤ n+1) :
    prefixValue n w k = (w % 2^(n+1)) / 2^(n+1-k) := by
  unfold prefixValue
  rw [← Nat.mod_mul_right_div_self]
  rw [← pow_add, Nat.sub_add_cancel hk]

theorem classify_zero (b n w k : ℕ) (hb : 0 < b) :
    classify 0 b n w k = some true := by
  have hp : 0 < b * (prefixValue n w k + 1) := Nat.mul_pos hb (by omega)
  simp [classify, Nat.not_le_of_gt hp]

theorem classify_one (b n w k : ℕ) :
    classify b b n w k = some false := by
  have hv : prefixValue n w k < 2^k := Nat.mod_lt _ (by positivity)
  have hl : b * (prefixValue n w k+1) ≤ b * 2^k :=
    Nat.mul_le_mul_left b (by omega)
  simp [classify, hl]

theorem scanChoice_zero (b n w : ℕ) (hb : 0 < b) :
    scanChoice 0 b n w (n+1) = some ⟨1,true⟩ := by
  apply (scanChoice_some_iff 0 b n w (n+1) ⟨1,true⟩).mpr
  dsimp only
  exact ⟨by omega,by omega,classify_zero b n w 1 hb,by intro j hj hj'; omega⟩

theorem scanChoice_one (b n w : ℕ) :
    scanChoice b b n w (n+1) = some ⟨1,false⟩ := by
  apply (scanChoice_some_iff b b n w (n+1) ⟨1,false⟩).mpr
  dsimp only
  exact ⟨by omega,by omega,classify_one b n w 1,by intro j hj hj'; omega⟩

/-- The zero shift copies one bit before the base observer begins. -/
theorem compileShift_zero_first (body : Stmt) (output b w : ℕ) (hb : 0 < b) :
    exec (compileShift body output 0 b) (initial 0 w) 2 = w % 2 := by
  rw [compileShift_correct]
  simp [specifiedValue, scanChoice_zero b 0 w hb]

theorem compileShift_zero_tail (body : Stmt) (output b n w : ℕ) (hb : 0 < b) :
    exec (compileShift body output 0 b) (initial (n+1) w) 2 =
      exec body (initial n (2^(n+1) + w % 2^(n+1))) output % 2 := by
  rw [compileShift_correct]
  simp [specifiedValue, scanChoice_zero b (n+1) w hb]

/-- Endpoint one is the identity bit observer, not a base call. -/
theorem compileShift_one (body : Stmt) (output b n w : ℕ) :
    exec (compileShift body output b b) (initial n w) 2 = w % 2 := by
  rw [compileShift_correct]
  simp [specifiedValue, scanChoice_one b n w]

/-- The selector's two inclusive tests cannot both hold at a positive denominator. -/
theorem cell_tests_disjoint (a b n w k : ℕ) (hb : 0 < b)
    (hlo : b * (prefixValue n w k + 1) ≤ a * 2^k) :
    ¬ a * 2^k ≤ b * prefixValue n w k := by
  intro hhi
  nlinarith

/-- Scaling a representation by any positive natural leaves every cell test unchanged. -/
theorem classify_scaled (a b n w k c : ℕ) (hc : 0 < c) :
    classify (c*a) (c*b) n w k = classify a b n w k := by
  simp only [classify, Nat.mul_assoc, Nat.mul_le_mul_left_iff hc]

theorem scanChoice_scaled (a b n w k c : ℕ) (hc : 0 < c) :
    scanChoice (c*a) (c*b) n w k = scanChoice a b n w k := by
  induction k with
  | zero => rfl
  | succ k ih => simp only [scanChoice, ih, classify_scaled a b n w (k+1) c hc]

theorem compileShift_scaled (body : Stmt) (output a b n w c : ℕ) (hc : 0 < c) :
    exec (compileShift body output (c*a) (c*b)) (initial n w) 2 =
      exec (compileShift body output a b) (initial n w) 2 := by
  rw [compileShift_correct, compileShift_correct]
  simp only [specifiedValue, scanChoice_scaled a b n w (n+1) c hc]

/-- Equal valid rational representations give identical finite outputs,
without reducing either denominator. -/
theorem compileShift_sameRatio (body : Stmt) (output a b a' b' n w : ℕ)
    (hb : 0 < b) (hb' : 0 < b') (he : a*b' = a'*b) :
    exec (compileShift body output a b) (initial n w) 2 =
      exec (compileShift body output a' b') (initial n w) 2 := by
  have hn : b'*a = b*a' := by nlinarith [he]
  calc
    _ = exec (compileShift body output (b'*a) (b'*b)) (initial n w) 2 :=
      (compileShift_scaled body output a b n w b' hb').symm
    _ = exec (compileShift body output (b*a') (b*b')) (initial n w) 2 := by
      rw [hn, Nat.mul_comm b' b]
    _ = _ := compileShift_scaled body output a' b' n w b hb

end P02.LiteralShift
