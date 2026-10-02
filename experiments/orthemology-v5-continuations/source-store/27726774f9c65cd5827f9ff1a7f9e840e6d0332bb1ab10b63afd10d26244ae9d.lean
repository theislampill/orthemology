import Mathlib.Tactic
import Mathlib.Data.Finset.Max

open scoped BigOperators

namespace Orthemology.Tranche3
noncomputable section

variable {Ω : Type*} [Fintype Ω]

def upperTail (p : Ω → ℝ) (stat : Ω → ℕ) (x : Ω) : ℝ :=
  ∑ y, if stat x ≤ stat y then p y else 0

def lowerTail (p : Ω → ℝ) (stat : Ω → ℕ) (x : Ω) : ℝ :=
  ∑ y, if stat y ≤ stat x then p y else 0

/-- Inclusive finite upper-tail p-values are superuniform. This result needs
only nonnegative masses; probability normalization is supplied by applications. -/
theorem upperTail_superuniform (p : Ω → ℝ) (stat : Ω → ℕ)
    (hp : ∀ x, 0 ≤ p x) (beta : ℝ) (hb : 0 ≤ beta) :
    (∑ x, if upperTail p stat x ≤ beta then p x else 0) ≤ beta := by
  classical
  let A := Finset.univ.filter (fun x => upperTail p stat x ≤ beta)
  rw [← Finset.sum_filter]
  change (∑ x ∈ A, p x) ≤ beta
  by_cases hA : A.Nonempty
  · obtain ⟨x,hx,hm⟩ := A.exists_min_image stat hA
    have hb' : upperTail p stat x ≤ beta := (Finset.mem_filter.mp hx).2
    have hs : A ⊆ Finset.univ.filter (fun y => stat x ≤ stat y) := by
      intro y hy
      exact Finset.mem_filter.mpr ⟨Finset.mem_univ _,hm y hy⟩
    calc
      (∑ x ∈ A, p x) ≤ ∑ y ∈ Finset.univ.filter (fun y => stat x ≤ stat y), p y :=
        Finset.sum_le_sum_of_subset_of_nonneg hs (fun y _ _ => hp y)
      _ = upperTail p stat x := by simp [upperTail, Finset.sum_filter]
      _ ≤ beta := hb'
  · have he : A = ∅ := Finset.not_nonempty_iff_eq_empty.mp hA
    simpa [he] using hb

/-- The lower-tail analogue retains ties and zero-mass observations. -/
theorem lowerTail_superuniform (p : Ω → ℝ) (stat : Ω → ℕ)
    (hp : ∀ x, 0 ≤ p x) (beta : ℝ) (hb : 0 ≤ beta) :
    (∑ x, if lowerTail p stat x ≤ beta then p x else 0) ≤ beta := by
  classical
  let A := Finset.univ.filter (fun x => lowerTail p stat x ≤ beta)
  rw [← Finset.sum_filter]
  change (∑ x ∈ A, p x) ≤ beta
  by_cases hA : A.Nonempty
  · obtain ⟨x,hx,hm⟩ := A.exists_max_image stat hA
    have hb' : lowerTail p stat x ≤ beta := (Finset.mem_filter.mp hx).2
    have hs : A ⊆ Finset.univ.filter (fun y => stat y ≤ stat x) := by
      intro y hy
      exact Finset.mem_filter.mpr ⟨Finset.mem_univ _,hm y hy⟩
    calc
      (∑ x ∈ A, p x) ≤ ∑ y ∈ Finset.univ.filter (fun y => stat y ≤ stat x), p y :=
        Finset.sum_le_sum_of_subset_of_nonneg hs (fun y _ _ => hp y)
      _ = lowerTail p stat x := by simp [lowerTail, Finset.sum_filter]
      _ ≤ beta := hb'
  · have he : A = ∅ := Finset.not_nonempty_iff_eq_empty.mp hA
    simpa [he] using hb

/-- Tail-inversion certificates yield a finite-sample coverage bound, for an
arbitrary real true parameter. The two implications are checked by the
parameter-monotonicity layer of a concrete statistical family. -/
theorem tail_inversion_coverage (p : Ω → ℝ) (stat : Ω → ℕ)
    (hp : ∀ x, 0 ≤ p x) (beta : ℝ) (hb : 0 ≤ beta)
    (a : ℝ) (lower upper : Ω → ℝ)
    (hl : ∀ x, a < lower x → upperTail p stat x ≤ beta)
    (hu : ∀ x, upper x < a → lowerTail p stat x ≤ beta) :
    (∑ x, if a < lower x ∨ upper x < a then p x else 0) ≤ 2*beta := by
  classical
  calc
    (∑ x, if a < lower x ∨ upper x < a then p x else 0) ≤
        ∑ x, ((if upperTail p stat x ≤ beta then p x else 0) +
              (if lowerTail p stat x ≤ beta then p x else 0)) := by
      apply Finset.sum_le_sum
      intro x _
      by_cases h : a < lower x ∨ upper x < a
      · rw [if_pos h]
        rcases h with h | h
        · rw [if_pos (hl x h)]
          split_ifs <;> linarith [hp x]
        · rw [if_pos (hu x h)]
          split_ifs <;> linarith [hp x]
      · rw [if_neg h]
        split_ifs <;> linarith [hp x]
    _ ≤ 2*beta := by
      rw [Finset.sum_add_distrib]
      linarith [upperTail_superuniform p stat hp beta hb,lowerTail_superuniform p stat hp beta hb]

end
end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.upperTail_superuniform
#print axioms Orthemology.Tranche3.lowerTail_superuniform
#print axioms Orthemology.Tranche3.tail_inversion_coverage
