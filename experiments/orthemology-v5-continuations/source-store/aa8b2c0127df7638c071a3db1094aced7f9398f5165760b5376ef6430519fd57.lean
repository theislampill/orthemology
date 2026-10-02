import GroupedBinomialTails

open scoped BigOperators

namespace Orthemology.Tranche3

def binomialTerm (n i : ℕ) (p : ℚ) : ℚ :=
  (n.choose i:ℚ)*p^i*(1-p)^(n-i)

def nextBinomialTerm (n i : ℕ) (p term : ℚ) : ℚ :=
  term*(↑(n-i):ℚ)*p/((↑(i+1):ℚ)*(1-p))

lemma binomialTerm_next (n i : ℕ) (p : ℚ) (hp : p ≠ 1) :
    nextBinomialTerm n i p (binomialTerm n i p) = binomialTerm n (i+1) p := by
  have hip : (i:ℚ)+1 ≠ 0 := by positivity
  have hpp : 1-p ≠ 0 := sub_ne_zero.mpr (Ne.symm hp)
  by_cases hin : i<n
  · have hsub : n-i=n-(i+1)+1 := by omega
    have hc : (n.choose (i+1):ℚ)*((i:ℚ)+1) = (n.choose i:ℚ)*(n-i:ℕ) := by
      exact_mod_cast Nat.choose_succ_right_eq n i
    unfold nextBinomialTerm binomialTerm
    rw [hsub,pow_succ,pow_succ]
    push_cast
    field_simp
    calc
      _ = ((n.choose i:ℚ)*(n-i:ℕ))*(p^i*p)*((1-p)^(n-(i+1))*(1-p)) := by
        rw [hsub]
        push_cast
        ring
      _ = ((n.choose (i+1):ℚ)*((i:ℚ)+1))*(p^i*p)*((1-p)^(n-(i+1))*(1-p)) := by rw [hc]
      _ = _ := by ring
  · have hsub : n-i=0 := by omega
    have hab : n < i+1 := by omega
    simp [nextBinomialTerm,binomialTerm,hsub,Nat.choose_eq_zero_of_lt hab]

/-- A single linear sweep maintains the exact current binomial term. -/
def tailSweep (n : ℕ) (p : ℚ) (keep : ℕ → Bool) : ℕ → ℕ → ℚ → ℚ → ℚ
  | 0, _, _, acc => acc
  | remaining+1, i, term, acc =>
      tailSweep n p keep remaining (i+1) (nextBinomialTerm n i p term)
        (if keep i then acc+term else acc)

lemma tailSweep_correct (n : ℕ) (p : ℚ) (hp : p ≠ 1) (keep : ℕ → Bool) :
    ∀ remaining i acc,
    tailSweep n p keep remaining i (binomialTerm n i p) acc =
      acc+∑ j ∈ Finset.range remaining, if keep (i+j) then binomialTerm n (i+j) p else 0 := by
  intro remaining
  induction remaining with
  | zero => intro i acc; simp [tailSweep]
  | succ r ih =>
      intro i acc
      simp only [tailSweep,binomialTerm_next n i p hp]
      rw [ih,Finset.sum_range_succ']
      simp only [Nat.add_zero]
      have hsum : (∑ j ∈ Finset.range r, if keep (i+1+j) then binomialTerm n (i+1+j) p else 0) =
          ∑ j ∈ Finset.range r, if keep (i+(j+1)) then binomialTerm n (i+(j+1)) p else 0 := by
        apply Finset.sum_congr rfl
        intro j _
        have h : i+1+j=i+(j+1) := by omega
        rw [h]
      rw [hsum]
      split_ifs <;> ring

/-- The p=1 branch avoids division by zero; p=0 is valid in the sweep. -/
def sequentialTail (n : ℕ) (p : ℚ) (keep : ℕ → Bool) : ℚ :=
  if p=1 then (if keep n then 1 else 0)
  else tailSweep n p keep (n+1) 0 ((1-p)^n) 0

lemma binomialTerm_at_one (n i : ℕ) :
    binomialTerm n i 1 = if i=n then 1 else 0 := by
  by_cases h : i=n
  · subst i; simp [binomialTerm]
  · by_cases hin : i<n
    · have hpos : n-i ≠ 0 := by omega
      simp [binomialTerm,h,hpos]
    · have hni : n < i := by omega
      simp [binomialTerm,h,Nat.choose_eq_zero_of_lt hni]

theorem sequentialTail_eq (n : ℕ) (p : ℚ) (keep : ℕ → Bool) :
    sequentialTail n p keep =
      ∑ i ∈ Finset.range (n+1), if keep i then binomialTerm n i p else 0 := by
  unfold sequentialTail
  by_cases hp : p=1
  · rw [if_pos hp]
    subst p
    simp_rw [binomialTerm_at_one]
    have he : ∀ i, (if keep i then (if i=n then (1:ℚ) else 0) else 0) =
        if i=n then (if keep n then 1 else 0) else 0 := by
      intro i
      by_cases h : i=n <;> simp [h]
    simp_rw [he]
    simp
  · rw [if_neg hp]
    have h0 : (1-p)^n = binomialTerm n 0 p := by simp [binomialTerm]
    rw [h0,tailSweep_correct n p hp]
    simp

def sequentialUpper (n k : ℕ) (p : ℚ) : ℚ := sequentialTail n p (fun i => decide (k ≤ i))
def sequentialLower (n k : ℕ) (p : ℚ) : ℚ := sequentialTail n p (fun i => decide (i ≤ k))

theorem sequentialUpper_eq (n k : ℕ) (p : ℚ) : sequentialUpper n k p = rationalUpper n k p := by
  rw [← efficientUpper_eq]
  simp [sequentialUpper,sequentialTail_eq,efficientUpper,binomialTerm]

theorem sequentialLower_eq (n k : ℕ) (p : ℚ) : sequentialLower n k p = rationalLower n k p := by
  rw [← efficientLower_eq]
  simp [sequentialLower,sequentialTail_eq,efficientLower,binomialTerm]

end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.sequentialTail_eq
#print axioms Orthemology.Tranche3.sequentialUpper_eq
#print axioms Orthemology.Tranche3.sequentialLower_eq
#eval Orthemology.Tranche3.sequentialUpper 128 64 (1/2)
