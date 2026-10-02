import ObservationLoss
import AnnularLiteral
noncomputable section
namespace Orthemology.ObservationLoss
open AnnularLiteral

lemma literal_accepts_quarter : Accepted (1/4) (1/4) (9/16) := by
  norm_num [Accepted,D0,D1]

lemma literal_rejects_half : ¬ Accepted (1/2) (1/4) (9/16) := by
  norm_num [Accepted,D0,D1]

/-- The exact retained latent-parameter failure indicator at one fixed report
cannot be represented as the expectation of one common nonnegative next-bit
loss table. Both Bernoulli parameters are strictly interior. -/
theorem literal_no_common_next_bit_score :
    ¬ ∃ l0 l1 : ℝ, 0 ≤ l0 ∧ 0 ≤ l1 ∧
      ((1-(1/4:ℝ))*l0+(1/4)*l1 = (failureIndicator (1/4) (9/16) (1/4)).toReal) ∧
      ((1-(1/2:ℝ))*l0+(1/2)*l1 = (failureIndicator (1/4) (9/16) (1/2)).toReal) := by
  rintro ⟨l0,l1,h0,h1,hquarter,hhalf⟩
  have hz : (1-(1/4:ℝ))*l0+(1/4)*l1 = 0 := by
    simpa only [failureIndicator, if_pos literal_accepts_quarter, ENNReal.toReal_zero] using hquarter
  have ho : (1-(1/2:ℝ))*l0+(1/2)*l1 = 1 := by
    simpa only [failureIndicator, if_neg literal_rejects_half, ENNReal.toReal_one] using hhalf
  have hh := bernoulli_no_zero_positive_score (1/4) (1/2) l0 l1
    (by norm_num) (by norm_num) h0 h1 hz
  linarith

#print axioms literal_accepts_quarter
#print axioms literal_rejects_half
#print axioms literal_no_common_next_bit_score
end Orthemology.ObservationLoss
