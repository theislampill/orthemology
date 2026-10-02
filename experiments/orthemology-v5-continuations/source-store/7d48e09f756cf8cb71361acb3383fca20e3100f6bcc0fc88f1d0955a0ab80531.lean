import Mathlib.Tactic
open scoped BigOperators
namespace Orthemology.ObservationLoss

/-- A nonnegative finite-observation score with zero expectation under a
full-support law vanishes at every observation. -/
theorem zero_score_under_full_support {W : Type*} [Fintype W]
    (p loss : W → ℝ) (hp : ∀ w, 0 < p w) (hl : ∀ w, 0 ≤ loss w)
    (hz : ∑ w, p w*loss w = 0) : ∀ w, loss w = 0 := by
  intro w
  have he : p w*loss w = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => mul_nonneg (hp j).le (hl j))).mp hz w
      (Finset.mem_univ w)
  exact (mul_eq_zero.mp he).resolve_left (hp w).ne'

/-- No parameter-independent nonnegative finite-observation loss can have
zero expected score under a full-support parameter and positive expected score
under another parameter. This is the precise obstruction used in comparing the
literal latent-parameter failure loss with next-symbol prediction losses. -/
theorem no_zero_positive_representation {W : Type*} [Fintype W]
    (p q loss : W → ℝ) (hp : ∀ w, 0 < p w) (hl : ∀ w, 0 ≤ loss w)
    (hz : ∑ w, p w*loss w = 0) : ∑ w, q w*loss w = 0 := by
  simp [zero_score_under_full_support p loss hp hl hz]

/-- Both binary outcomes have positive probability at every interior Bernoulli
parameter. The score must be common across the two parameters. -/
theorem bernoulli_no_zero_positive_score (p q l0 l1 : ℝ)
    (hp : 0 < p) (hp1 : p < 1) (h0 : 0 ≤ l0) (h1 : 0 ≤ l1)
    (hz : (1-p)*l0+p*l1 = 0) : (1-q)*l0+q*l1 = 0 := by
  have ha : 0 ≤ (1-p)*l0 := mul_nonneg (by linarith) h0
  have hb : 0 ≤ p*l1 := mul_nonneg hp.le h1
  have hzero0 : l0=0 := by nlinarith
  have hzero1 : l1=0 := by nlinarith
  simp [hzero0,hzero1]

#print axioms zero_score_under_full_support
#print axioms no_zero_positive_representation
#print axioms bernoulli_no_zero_positive_score
end Orthemology.ObservationLoss

namespace Orthemology.ObservationLoss.Controls
/-- Dropping full support permits zero observed loss at p=0 and positive at p=1/2. -/
theorem endpoint_support_countercontrol :
    ((1-(0:ℝ))*0+0*1=0) ∧ ((1-(1/2:ℝ))*0+(1/2)*1>0) := by norm_num
/-- Signed scoring removes the nonnegative zero-expectation obstruction. -/
theorem signed_loss_countercontrol :
    ((1-(1/4:ℝ))*(-1)+(1/4)*3=0) ∧
      ((1-(1/2:ℝ))*(-1)+(1/2)*3>0) := by norm_num
#print axioms endpoint_support_countercontrol
#print axioms signed_loss_countercontrol
end Orthemology.ObservationLoss.Controls
