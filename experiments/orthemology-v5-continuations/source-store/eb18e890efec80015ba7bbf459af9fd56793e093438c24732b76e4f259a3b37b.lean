import BernoulliIntervalCoverage

open scoped BigOperators
open Orthemology.Tranche2

namespace Orthemology.Tranche3

/-- Executable reference distribution on actual finite bit words. -/
def rationalMass : (n : ℕ) → ℚ → Bits n → ℚ
  | 0, _, _ => 1
  | n+1, p, w => (if w.1 then p else 1-p)*rationalMass n p w.2

def rationalCount : (n : ℕ) → Bits n → ℕ
  | 0, _ => 0
  | n+1, w => (if w.1 then 1 else 0)+rationalCount n w.2

lemma rationalCount_eq : ∀ n (w : Bits n), rationalCount n w = countOnes n w := by
  intro n
  induction n with
  | zero => intro w; rfl
  | succ n ih => intro w; simp [rationalCount,countOnes,ih]

def rationalUpper (n k : ℕ) (p : ℚ) : ℚ :=
  ∑ w, if k ≤ rationalCount n w then rationalMass n p w else 0
def rationalLower (n k : ℕ) (p : ℚ) : ℚ :=
  ∑ w, if rationalCount n w ≤ k then rationalMass n p w else 0

lemma rationalMass_cast : ∀ n (p : ℚ) (w : Bits n),
    (rationalMass n p w : ℝ) = bernoulliMass n p w := by
  intro n
  induction n with
  | zero => intro p w; simp [rationalMass,bernoulliMass]
  | succ n ih =>
      intro p w
      simp only [rationalMass,bernoulliMass,coinMass]
      push_cast
      rw [ih]
      cases w.1 <;> simp

lemma rationalUpper_cast (n k : ℕ) (p : ℚ) :
    (rationalUpper n k p : ℝ) = bernoulliUpper n k p := by
  simp only [rationalUpper,bernoulliUpper,coinExpectation]
  push_cast
  apply Finset.sum_congr rfl
  intro w _
  rw [rationalCount_eq]
  split_ifs <;> simp [rationalMass_cast]

lemma rationalLower_cast (n k : ℕ) (p : ℚ) :
    (rationalLower n k p : ℝ) = bernoulliLower n k p := by
  simp only [rationalLower,bernoulliLower,coinExpectation]
  push_cast
  apply Finset.sum_congr rfl
  intro w _
  rw [rationalCount_eq]
  split_ifs <;> simp [rationalMass_cast]

/-- Retain a lower endpoint satisfying f(lo) ≤ beta. -/
def lowerBisect (f : ℚ → ℚ) (beta : ℚ) : ℕ → ℚ × ℚ → ℚ × ℚ
  | 0, pair => pair
  | n+1, pair =>
      let mid := (pair.1+pair.2)/2
      lowerBisect f beta n (if f mid ≤ beta then (mid,pair.2) else (pair.1,mid))

/-- Retain an upper endpoint satisfying f(hi) ≤ beta. -/
def upperBisect (f : ℚ → ℚ) (beta : ℚ) : ℕ → ℚ × ℚ → ℚ × ℚ
  | 0, pair => pair
  | n+1, pair =>
      let mid := (pair.1+pair.2)/2
      upperBisect f beta n (if f mid ≤ beta then (pair.1,mid) else (mid,pair.2))

lemma lowerBisect_invariant (f : ℚ → ℚ) (beta : ℚ) : ∀ n (lo hi : ℚ),
    0 ≤ lo → lo ≤ hi → hi ≤ 1 → f lo ≤ beta →
    let r := lowerBisect f beta n (lo,hi)
    0 ≤ r.1 ∧ r.1 ≤ r.2 ∧ r.2 ≤ 1 ∧ f r.1 ≤ beta := by
  intro n
  induction n with
  | zero => intro lo hi hl hm hh hf; exact ⟨hl,hm,hh,hf⟩
  | succ n ih =>
      intro lo hi hl hm hh hf
      simp only [lowerBisect]
      split_ifs with h
      · exact ih _ _ (by linarith) (by linarith) hh h
      · exact ih _ _ hl (by linarith) (by linarith) hf

lemma upperBisect_invariant (f : ℚ → ℚ) (beta : ℚ) : ∀ n (lo hi : ℚ),
    0 ≤ lo → lo ≤ hi → hi ≤ 1 → f hi ≤ beta →
    let r := upperBisect f beta n (lo,hi)
    0 ≤ r.1 ∧ r.1 ≤ r.2 ∧ r.2 ≤ 1 ∧ f r.2 ≤ beta := by
  intro n
  induction n with
  | zero => intro lo hi hl hm hh hf; exact ⟨hl,hm,hh,hf⟩
  | succ n ih =>
      intro lo hi hl hm hh hf
      simp only [upperBisect]
      split_ifs with h
      · exact ih _ _ hl (by linarith) (by linarith) h
      · exact ih _ _ (by linarith) (by linarith) hh hf

end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.rationalUpper_cast
#print axioms Orthemology.Tranche3.lowerBisect_invariant
#eval Orthemology.Tranche3.rationalUpper 4 2 (1/2)

namespace Orthemology.Tranche3

lemma rationalCount_le : ∀ n (w : Bits n), rationalCount n w ≤ n := by
  intro n
  induction n with
  | zero => intro w; rfl
  | succ n ih =>
      intro w
      have h := ih w.2
      cases hb : w.1 <;> simp [rationalCount,hb] <;> omega

lemma rationalMass_zero_of_count_pos : ∀ n (w : Bits n),
    0 < rationalCount n w → rationalMass n 0 w = 0 := by
  intro n
  induction n with
  | zero => intro w h; simp [rationalCount] at h
  | succ n ih =>
      intro w h
      cases hb : w.1
      · simp [rationalCount,hb] at h
        simp [rationalMass,hb,ih w.2 h]
      · simp [rationalMass,hb]

lemma rationalMass_one_of_count_lt : ∀ n (w : Bits n),
    rationalCount n w < n → rationalMass n 1 w = 0 := by
  intro n
  induction n with
  | zero => intro w h; omega
  | succ n ih =>
      intro w h
      cases hb : w.1
      · simp [rationalMass,hb]
      · have ht : rationalCount n w.2 < n := by simp [rationalCount,hb] at h; omega
        simp [rationalMass,hb,ih w.2 ht]

lemma rationalUpper_zero (n k : ℕ) (hk : 0 < k) : rationalUpper n k 0 = 0 := by
  apply Finset.sum_eq_zero
  intro w _
  split_ifs with h
  · exact rationalMass_zero_of_count_pos n w (hk.trans_le h)
  · rfl

lemma rationalLower_one (n k : ℕ) (hk : k < n) : rationalLower n k 1 = 0 := by
  apply Finset.sum_eq_zero
  intro w _
  split_ifs with h
  · exact rationalMass_one_of_count_lt n w (h.trans_lt hk)
  · rfl

def referenceLower (n k : ℕ) (beta : ℚ) (steps : ℕ) : ℚ :=
  if k=0 then 0 else (lowerBisect (rationalUpper n k) beta steps (0,1)).1

def referenceUpper (n k : ℕ) (beta : ℚ) (steps : ℕ) : ℚ :=
  if n≤k then 1 else (upperBisect (rationalLower n k) beta steps (0,1)).2

lemma referenceLower_check (n k : ℕ) (beta : ℚ) (steps : ℕ) (hb : 0 ≤ beta) :
    0 ≤ referenceLower n k beta steps ∧ referenceLower n k beta steps ≤ 1 ∧
    (referenceLower n k beta steps = 0 ∨ rationalUpper n k (referenceLower n k beta steps) ≤ beta) := by
  unfold referenceLower
  split_ifs with h
  · norm_num
  · have hz := rationalUpper_zero n k (by omega)
    have hi := lowerBisect_invariant (rationalUpper n k) beta steps 0 1
      (by norm_num) (by norm_num) (by norm_num) (by rw [hz]; exact hb)
    exact ⟨hi.1,hi.2.1.trans hi.2.2.1,Or.inr hi.2.2.2⟩

lemma referenceUpper_check (n k : ℕ) (beta : ℚ) (steps : ℕ) (hb : 0 ≤ beta) :
    0 ≤ referenceUpper n k beta steps ∧ referenceUpper n k beta steps ≤ 1 ∧
    (referenceUpper n k beta steps = 1 ∨ rationalLower n k (referenceUpper n k beta steps) ≤ beta) := by
  unfold referenceUpper
  split_ifs with h
  · norm_num
  · have hz := rationalLower_one n k (by omega)
    have hi := upperBisect_invariant (rationalLower n k) beta steps 0 1
      (by norm_num) (by norm_num) (by norm_num) (by rw [hz]; exact hb)
    exact ⟨hi.1.trans hi.2.1,hi.2.2.1,Or.inr hi.2.2.2⟩

lemma bernoulli_tails_cover (n k : ℕ) (p : ℝ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    1 ≤ bernoulliUpper n k p+bernoulliLower n k p := by
  rw [← bernoulliMass_sum n p]
  unfold bernoulliUpper bernoulliLower coinExpectation
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_le_sum
  intro w _
  have hm := bernoulliMass_nonneg n p hp0 hp1 w
  dsimp only
  split_ifs <;> simp_all
  all_goals omega

/-- Outer tail checks force the returned real interval to be nonempty. -/
theorem outer_tail_brackets_ordered (n k : ℕ) (beta l u : ℝ)
    (hb : beta < 1/2) (hl0 : 0 ≤ l) (hl1 : l ≤ 1) (hu0 : 0 ≤ u)
    (hl : l=0 ∨ bernoulliUpper n k l ≤ beta)
    (hu : u=1 ∨ bernoulliLower n k u ≤ beta) : l ≤ u := by
  by_contra h
  have hul : u < l := lt_of_not_ge h
  have hgl : bernoulliUpper n k l ≤ beta := by
    rcases hl with h | h
    · linarith
    · exact h
  have hhu : bernoulliLower n k u ≤ beta := by
    rcases hu with h | h
    · linarith
    · exact h
  have hh := (bernoulliLower_antitone n k u l hu0 hul.le hl1).trans hhu
  have hc := bernoulli_tails_cover n k l hl0 hl1
  linarith

/-- The executable outward bisection supplies all finite-sample statistical
bracket premises, at any finite chosen precision. -/
theorem reference_tailBracket (n : ℕ) (beta : ℚ) (steps : ℕ)
    (hb0 : 0 ≤ beta) (hb1 : beta < 1/2) :
    TailBracket n beta
      (fun w => (referenceLower n (rationalCount n w) beta steps : ℝ))
      (fun w => (referenceUpper n (rationalCount n w) beta steps : ℝ)) := by
  have hl := fun w : Bits n => referenceLower_check n (rationalCount n w) beta steps hb0
  have hu := fun w : Bits n => referenceUpper_check n (rationalCount n w) beta steps hb0
  have hl' : ∀ w : Bits n, (referenceLower n (rationalCount n w) beta steps : ℝ)=0 ∨
      bernoulliUpper n (countOnes n w) (referenceLower n (rationalCount n w) beta steps) ≤ beta := by
    intro w
    rcases (hl w).2.2 with h | h
    · exact Or.inl (by exact_mod_cast h)
    · right
      rw [← rationalCount_eq,← rationalUpper_cast]
      exact_mod_cast h
  have hu' : ∀ w : Bits n, (referenceUpper n (rationalCount n w) beta steps : ℝ)=1 ∨
      bernoulliLower n (countOnes n w) (referenceUpper n (rationalCount n w) beta steps) ≤ beta := by
    intro w
    rcases (hu w).2.2 with h | h
    · exact Or.inl (by exact_mod_cast h)
    · right
      rw [← rationalCount_eq,← rationalLower_cast]
      exact_mod_cast h
  refine ⟨?_,hl',hu'⟩
  intro w
  have hl0 : (0:ℝ) ≤ referenceLower n (rationalCount n w) beta steps := by exact_mod_cast (hl w).1
  have hl1 : (referenceLower n (rationalCount n w) beta steps : ℝ) ≤ 1 := by exact_mod_cast (hl w).2.1
  have hu0 : (0:ℝ) ≤ referenceUpper n (rationalCount n w) beta steps := by exact_mod_cast (hu w).1
  have hu1 : (referenceUpper n (rationalCount n w) beta steps : ℝ) ≤ 1 := by exact_mod_cast (hu w).2.1
  have hb1' : (beta:ℝ) < 1/2 := by
    have hx : (beta:ℝ) < ((1/2:ℚ):ℝ) := by exact_mod_cast hb1
    norm_num at hx ⊢
    exact hx
  exact ⟨hl0,outer_tail_brackets_ordered n (countOnes n w) beta _ _ hb1' hl0 hl1 hu0 (hl' w) (hu' w),hu1⟩

end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.reference_tailBracket
#eval Orthemology.Tranche3.referenceLower 8 4 (1/100) 12
#eval Orthemology.Tranche3.referenceUpper 8 4 (1/100) 12
