import LiteralShiftPrefix

namespace P02.LiteralShift

theorem wordPayload_append (xs ys : List Bool) :
    wordPayload (xs ++ ys) = wordPayload xs * 2^ys.length + wordPayload ys := by
  have h := sentinel_append_payload xs ys
  simp only [sentinel_payload, List.length_append, pow_add] at h
  nlinarith

theorem streamPayload_succ (x : ℕ → Bool) (k : ℕ) :
    wordPayload (streamPrefix x (k+1)) =
      2 * wordPayload (streamPrefix x k) + if x k then 1 else 0 := by
  have h : streamPrefix x (k+1) = streamPrefix x k ++ [x k] := by
    unfold streamPrefix
    rw [List.ofFn_succ', List.concat_eq_append]
    rfl
  rw [h, wordPayload_append]
  simp [wordPayload, Nat.mul_comm]

theorem streamClassify_false_iff (a b k : ℕ) (x : ℕ → Bool) :
    streamClassify a b x k = some false ↔
      b * (wordPayload (streamPrefix x k)+1) ≤ a * 2^k := by
  simp only [streamClassify]
  split <;> simp_all

theorem streamClassify_true_iff (a b k : ℕ) (x : ℕ → Bool) (hb : 0 < b) :
    streamClassify a b x k = some true ↔
      a * 2^k ≤ b * wordPayload (streamPrefix x k) := by
  have hd : b * (wordPayload (streamPrefix x k)+1) ≤ a * 2^k →
      ¬ a * 2^k ≤ b * wordPayload (streamPrefix x k) := by
    intro hl hh
    nlinarith
  simp only [streamClassify]
  split <;> simp_all

/-- Once the literal cell is wholly on one side, every extension stays there. -/
theorem streamClassify_persistent (a b k m : ℕ) (x : ℕ → Bool) (side : Bool)
    (hb : 0 < b) (hkm : k ≤ m) (h : streamClassify a b x k = some side) :
    streamClassify a b x m = some side := by
  induction m, hkm using Nat.le_induction with
  | base => exact h
  | succ m hkm ih =>
      cases side with
      | false =>
          apply (streamClassify_false_iff a b (m+1) x).mpr
          have hi := (streamClassify_false_iff a b m x).mp ih
          rw [streamPayload_succ, pow_succ]
          cases hbit : x m <;> simp only [hbit, Bool.false_eq_true, ↓reduceIte] <;> nlinarith
      | true =>
          apply (streamClassify_true_iff a b (m+1) x hb).mpr
          have hi := (streamClassify_true_iff a b m x hb).mp ih
          rw [streamPayload_succ, pow_succ]
          cases hbit : x m <;> simp only [hbit, Bool.false_eq_true, ↓reduceIte] <;> nlinarith

/-- Eventual resolution on a side is exactly a first cut on that side. -/
theorem exists_firstCut_iff_classified (a b : ℕ) (x : ℕ → Bool) (side : Bool)
    (hb : 0 < b) :
    (∃ k, FirstCut a b x k side) ↔
      ∃ k, 1 ≤ k ∧ streamClassify a b x k = some side := by
  constructor
  · rintro ⟨k,hk,hc,_⟩
    exact ⟨k,hk,hc⟩
  · rintro ⟨k,hk,hc⟩
    rcases firstCut_or_unresolved a b x with ⟨j,t,hj⟩ | hu
    · have hjk : j ≤ k := by
        by_contra hn
        have he := hj.2.2 k hk (by omega)
        rw [hc] at he
        cases he
      have he := streamClassify_persistent a b j k x t hb hjk hj.2.1
      have ht : t = side := Option.some.inj (he.symm.trans hc)
      subst t
      exact ⟨j,hj⟩
    · have he := hu k hk
      rw [hc] at he
      cases he

end P02.LiteralShift
