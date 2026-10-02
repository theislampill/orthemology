import FiniteSelector

namespace OrthemologyTagged
open P02A2.ObserverCore P02A2.Q8Measure P02A2.SurvivorCandidates

variable {A : Type*} (R : A → ℕ → ℕ → ℕ → Prop) [∀ a i, DecidableRel (R a i)]

/-- A finite-prefix evaluator. It never searches beyond the supplied n+1 input
bits and does not inspect an infinite source to choose a row. -/
def pi3PrefixValue (a : A) (n word : ℕ) : ℕ :=
  let i := selector n word
  if n ≤ i then word % 2
  else if innovation (R a i) (n-i-1) then word % 2 else 0

theorem tag_before (i : ℕ) (y : Cantor) {n : ℕ} (hn : n < i) : tag i y n = true := by
  simp [tag, appendPrefix, tagWord, show n < i+1 by omega, hn]

theorem tag_at (i : ℕ) (y : Cantor) : tag i y i = false := by
  simp [tag, appendPrefix, tagWord]

theorem tag_after (i : ℕ) (y : Cantor) {n : ℕ} (hn : i < n) :
    tag i y n = y (n-i-1) := by
  simp [tag, appendPrefix, show ¬ (n < i+1) by omega, Nat.sub_sub]

theorem pi3PrefixValue_output (a : A) : output (pi3PrefixValue R a) = pi3Observer R a := by
  funext x n
  rcases exists_tag_or_allTrue x with ⟨i,hx⟩ | rfl
  · have htag : pi3Observer R a x = tag i (P02A2.Sigma2RowLaw.observer (R a) i (tail i x)) :=
      tagged_on _ hx
    by_cases hni : n < i
    · rw [htag, tag_before i _ hni]
      have hsel := selector_before_tag hx hni
      have hbit := ((tagEvent_spec i x).mp hx).1 n hni
      unfold output pi3PrefixValue
      rw [hsel, if_pos (Nat.le_succ n), Nat.mod_mod, P02A2.Q8Compiler.sentinel_prefix_last, hbit]
      rfl
    · have hin : i ≤ n := by omega
      have hsel := selector_on_tag hx hin
      by_cases he : n = i
      · subst n
        rw [htag, tag_at]
        have hbit := ((tagEvent_spec i x).mp hx).2
        unfold output pi3PrefixValue
        rw [hsel, if_pos (le_refl i), Nat.mod_mod, P02A2.Q8Compiler.sentinel_prefix_last, hbit]
        rfl
      · have hit : i < n := by omega
        rw [htag, tag_after i _ hit, P02A2.Sigma2RowLaw.observer_eq_switched]
        have hidx : i+1+(n-i-1) = n := by omega
        unfold output pi3PrefixValue
        rw [hsel]
        simp only [show ¬ (n ≤ i) by omega, ↓reduceIte]
        rw [P02A2.Q8Compiler.sentinel_prefix_last]
        cases hf : innovation (R a i) (n-i-1) <;> cases hb : x n <;>
          simp [hf, hb, switched, tail, dropBits, hidx]
  · change output (pi3PrefixValue R a) allTrue n = tagged _ allTrue n
    rw [tagged_allTrue]
    unfold output pi3PrefixValue
    rw [selector_allTrue, if_pos (Nat.le_succ n), Nat.mod_mod, P02A2.Q8Compiler.sentinel_prefix_last]
    rfl

/-- The semantic Π3 law is realised by an explicitly finite-input prefix function. -/
theorem finite_prefix_zero_defect_iff (a : A) :
    P02A2.defect (fairCantor.map (output (pi3PrefixValue R a))) = 0 ↔
      ∀ i, ∃ s, ∀ t, R a i s t := by
  rw [pi3PrefixValue_output]
  exact pi3_zero_defect_iff R a

end OrthemologyTagged
#print axioms OrthemologyTagged.pi3PrefixValue_output
#print axioms OrthemologyTagged.finite_prefix_zero_defect_iff
