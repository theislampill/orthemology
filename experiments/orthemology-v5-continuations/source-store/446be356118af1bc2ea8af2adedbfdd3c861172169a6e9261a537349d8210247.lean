import PolynomialBounds

noncomputable section
open scoped BigOperators
open PolynomialBounds

namespace ConstraintBounds
variable {J : Type*} [Fintype J]

def radius (head B : J → ℝ) : ℝ := 1/(1+∑ j, 2*(B j+1)/head j)

lemma radius_pos (head B : J → ℝ) (hh : ∀ j, 0 < head j) (hB : ∀ j, 0 ≤ B j) :
    0 < radius head B := by
  have hs : 0 ≤ ∑ j, 2*(B j+1)/head j := Finset.sum_nonneg (fun j _ => by
    have hj := hh j
    have hb := hB j
    positivity)
  dsimp [radius]
  positivity

lemma radius_le_one (head B : J → ℝ) (hh : ∀ j, 0 < head j) (hB : ∀ j, 0 ≤ B j) :
    radius head B ≤ 1 := by
  have hs : 0 ≤ ∑ j, 2*(B j+1)/head j := Finset.sum_nonneg (fun j _ => by
    have hj := hh j
    have hb := hB j
    positivity)
  have hd : 0 < 1+∑ j, 2*(B j+1)/head j := by positivity
  dsimp [radius]
  exact (div_le_one hd).2 (by linarith)

lemma radius_lt_each (head B : J → ℝ) (hh : ∀ j, 0 < head j) (hB : ∀ j, 0 ≤ B j) (j : J) :
    radius head B  <  head j/(2*(B j+1)) := by
  have hs : 0 ≤ ∑ j, 2*(B j+1)/head j := Finset.sum_nonneg (fun j _ => by
    have hj := hh j
    have hb := hB j
    positivity)
  have hsingle : 2*(B j+1)/head j  ≤  ∑ k, 2*(B k+1)/head k :=
    Finset.single_le_sum (fun (k : J) (_ : k ∈ Finset.univ) =>
      div_nonneg (mul_nonneg (show (0:ℝ) ≤ 2 by norm_num)
        (show 0 ≤ B k+1 by linarith [hB k])) (hh k).le) (Finset.mem_univ j)
  have hd : 0 < 1+∑ k, 2*(B k+1)/head k := by positivity
  have hr : 2*(B j+1)/head j  <  1+∑ k, 2*(B k+1)/head k := by linarith
  have hm := (div_lt_iff₀ (hh j)).mp hr
  have hj : 0 < 2*(B j+1) := by have hbj := hB j; positivity
  apply (lt_div_iff₀ hj).2
  dsimp [radius]
  rw [one_div_mul_eq_div]
  exact (div_lt_iff₀ hd).2 (by nlinarith)

/-- One explicit arithmetic radius handles a finite family of independently
bounded polynomial remainders and positive constant terms. -/
theorem positive_inside_radius (head B : J → ℝ) (rem : J → ℝ → ℝ)
    (hh : ∀ j, 0 < head j) (hB : ∀ j, 0 ≤ B j)
    (hrem : ∀ j eps, 0 ≤ eps → eps ≤ 1 → |rem j eps| ≤ B j)
    (eps : ℝ) (he : 0 < eps) (hsmall : eps < radius head B) :
    ∀ j, 0 < head j+eps*rem j eps := by
  have he1 : eps ≤ 1 := (hsmall.trans_le (radius_le_one head B hh hB)).le
  intro j
  have hg := strict_gain_of_budget (head j) (head j) (rem j eps) (B j) eps
    (hh j) (hB j) le_rfl (hrem j eps he.le he1) he
    (hsmall.trans (radius_lt_each head B hh hB j))
  exact (mul_pos_iff_of_pos_left (pow_pos he 2)).mp hg

#print axioms positive_inside_radius
end ConstraintBounds
