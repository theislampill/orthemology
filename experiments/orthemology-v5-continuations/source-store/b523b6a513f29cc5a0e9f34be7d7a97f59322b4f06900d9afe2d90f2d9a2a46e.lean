import Pi3Law

open Set MeasureTheory
namespace OrthemologyTagged
open P02A2.ObserverCore P02A2.Q8Measure

def readBit (n b j : ℕ) : Bool := decide (b / 2^(n-j) % 2 = 1)

theorem sentinel_prefix_bit_value (x : Cantor) (n j : ℕ) (hj : j ≤ n) :
    sentinel (List.ofFn (fun i : Fin (n+1) => x i.val)) / 2^(n-j) % 2 =
      if x j then 1 else 0 := by
  induction n generalizing j with
  | zero =>
      have he : j = 0 := by omega
      subst j
      simpa using P02A2.Q8Compiler.sentinel_prefix_last x 0
  | succ n ih =>
      by_cases he : j = n+1
      · subst j
        simpa using P02A2.Q8Compiler.sentinel_prefix_last x (n+1)
      · have hjn : j ≤ n := by omega
        have hc : sentinel (List.ofFn (fun i : Fin (n+1+1) => x i.val)) =
            2 * sentinel (List.ofFn (fun i : Fin (n+1) => x i.val)) +
              if x (n+1) then 1 else 0 := by
          rw [List.ofFn_succ', List.concat_eq_append, P02A2.Q8Compiler.sentinel_append_bit]
          simp
        rw [hc]
        have hd : n+1-j = (n-j)+1 := by omega
        rw [hd, pow_succ', ← Nat.div_div_eq_div_mul]
        have hhalf : (2 * sentinel (List.ofFn (fun i : Fin (n+1) => x i.val)) +
            if x (n+1) then 1 else 0) / 2 =
              sentinel (List.ofFn (fun i : Fin (n+1) => x i.val)) := by
          cases h : x (n+1) <;> simp only [h, Bool.false_eq_true, ↓reduceIte] <;> omega
        rw [hhalf]
        exact ih j hjn

theorem readBit_prefix (x : Cantor) (n j : ℕ) (hj : j ≤ n) :
    readBit n (sentinel (List.ofFn (fun i : Fin (n+1) => x i.val))) j = x j := by
  unfold readBit
  rw [sentinel_prefix_bit_value x n j hj]
  cases x j <;> rfl

end OrthemologyTagged
#print axioms OrthemologyTagged.readBit_prefix
