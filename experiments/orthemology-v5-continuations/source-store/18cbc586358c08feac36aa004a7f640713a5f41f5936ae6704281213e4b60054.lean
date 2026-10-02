import EmpiricalRepairCost
import EmpiricalFourthMoment
import EventualAuditSafety

open MeasureTheory Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2
namespace Orthemology.Tranche3
noncomputable section

def repairRadius (a : ℝ) (e : ℚ) : ℝ := a*(1-a)*(e:ℝ)/4

lemma empirical_good_of_error (a : ℝ) (ha0 : 0<a) (ha1 : a<1)
    (e : ℚ) (he0 : 0<e) (he1 : e≤1/4) (n : ℕ) (w : Bits (n+1))
    (h : |(empiricalWeight n w:ℝ)-a|≤repairRadius a e) :
    LiteralRepairGood a e (empiricalRepair e n w) := by
  have he0' : (0:ℝ)<e := by exact_mod_cast he0
  have he1' : (e:ℝ)≤1/4 := by
    have hh : (e:ℝ)≤((1/4:ℚ):ℝ) := by exact_mod_cast he1
    norm_num at hh ⊢
    exact hh
  have hg := approximate_parameter_strict_repair a e (empiricalWeight n w)
    ha0 ha1 he0' he1' h
  have hq : (empiricalRepair e n w:ℝ)=1/2+(empiricalWeight n w:ℝ)*(e:ℝ) := by
    simp only [empiricalRepair]; push_cast; ring
  have hc := empiricalRepair_coherent e he0.le he1 n w
  refine ⟨by exact_mod_cast hc.1,by exact_mod_cast hc.2,?_,?_⟩
  all_goals rw [hq]; simp only [excessZero,excessOne]
  all_goals linarith [hg.1,hg.2]

lemma empirical_centered_identity (a : ℝ) (n : ℕ) (w : Bits (n+1)) :
    ((n:ℝ)+1)*((empiricalWeight n w:ℝ)-a)=centeredTotal (n+1) a w := by
  simp only [empiricalWeight,centeredTotal]
  push_cast
  have hn : (n:ℝ)+1 ≠ 0 := by positivity
  field_simp

lemma empirical_bad_fourth (a : ℝ) (ha0 : 0<a) (ha1 : a<1)
    (e : ℚ) (he0 : 0<e) (he1 : e≤1/4) (n : ℕ) (w : Bits (n+1))
    (h : ¬ LiteralRepairGood a e (empiricalRepair e n w)) :
    (((n:ℝ)+1)*repairRadius a e)^4≤centeredTotal (n+1) a w^4 := by
  have hr0 : 0≤repairRadius a e := by
    unfold repairRadius
    have : 0≤1-a := by linarith
    positivity
  have hh : repairRadius a e < |(empiricalWeight n w:ℝ)-a| :=
    lt_of_not_ge (fun he => h (empirical_good_of_error a ha0 ha1 e he0 he1 n w he))
  have hm := mul_le_mul_of_nonneg_left hh.le (by positivity : (0:ℝ)≤(n:ℝ)+1)
  have hm' : ((n:ℝ)+1)*repairRadius a e≤|centeredTotal (n+1) a w| := by
    rw [←empirical_centered_identity,abs_mul,abs_of_nonneg (by positivity : (0:ℝ)≤(n:ℝ)+1)]
    exact hm
  have hp := pow_le_pow_left₀ (by positivity : 0≤((n:ℝ)+1)*repairRadius a e) hm' 4
  simpa only [show 4=2*2 from rfl,pow_mul,sq_abs] using hp

/-- A source-derived summable upper bound for every interior parameter. -/
theorem empirical_failure_probability_upper (a : ℝ) (ha0 : 0<a) (ha1 : a<1)
    (e : ℚ) (he0 : 0<e) (he1 : e≤1/4) (n : ℕ) :
    auditSourceLaw a ha0.le ha1.le (EmpiricalFailure a e n) ≤
      ENNReal.ofReal (4/(((n:ℝ)+1)^2*(repairRadius a e)^4)) := by
  classical
  have hr : 0<repairRadius a e := by
    unfold repairRadius
    have : 0<1-a := by linarith
    have : (0:ℝ)<e := by exact_mod_cast he0
    positivity
  have hd : 0<(((n:ℝ)+1)*repairRadius a e)^4 := by positivity
  rw [EmpiricalFailure,auditSource_word_event a ha0.le ha1.le (n+1)
    (fun w => ¬LiteralRepairGood a e (empiricalRepair e n w))]
  apply ENNReal.ofReal_le_ofReal
  calc
    (∑ w, if ¬ LiteralRepairGood a e (empiricalRepair e n w) then bernoulliMass (n+1) a w else 0)
      ≤ ∑ w, (bernoulliMass (n+1) a w*centeredTotal (n+1) a w^4)/
        (((n:ℝ)+1)*repairRadius a e)^4 := by
      apply Finset.sum_le_sum
      intro w _
      have hm := bernoulliMass_nonneg (n+1) a ha0.le ha1.le w
      split_ifs with h
      · positivity
      · apply (le_div_iff₀ hd).mpr
        exact mul_le_mul_of_nonneg_left (empirical_bad_fourth a ha0 ha1 e he0 he1 n w h) hm
    _ = centeredMoment (n+1) 4 a / (((n:ℝ)+1)*repairRadius a e)^4 := by
      rw [←Finset.sum_div]
      rfl
    _ ≤ (4*((n:ℝ)+1)^2)/(((n:ℝ)+1)*repairRadius a e)^4 := by
      apply div_le_div_of_nonneg_right _ hd.le
      simpa only [Nat.cast_add,Nat.cast_one] using centered_fourth_le (n+1) (by omega) a ha0.le ha1.le
    _ = 4/(((n:ℝ)+1)^2*(repairRadius a e)^4) := by
      have hn : (n:ℝ)+1≠0 := by positivity
      field_simp
      ring

lemma empirical_probability_spending (a : ℝ) (ha0 : 0<a) (ha1 : a<1)
    (e : ℚ) (he0 : 0<e) (he1 : e≤1/4) (n : ℕ) :
    auditSourceLaw a ha0.le ha1.le (EmpiricalFailure a e n) ≤
      ENNReal.ofReal (2*tailSpending (8/(repairRadius a e)^4) n) := by
  apply (empirical_failure_probability_upper a ha0 ha1 e he0 he1 n).trans
  apply ENNReal.ofReal_le_ofReal
  have hr : 0<repairRadius a e := by
    unfold repairRadius
    have : 0<1-a := by linarith
    have : (0:ℝ)<e := by exact_mod_cast he0
    positivity
  rw [double_tailSpending]
  apply (div_le_div_iff₀ (by positivity : 0<((n:ℝ)+1)^2*(repairRadius a e)^4)
    (by positivity : 0<((n:ℝ)+1)*((n:ℝ)+2))).mpr
  have hr4 : (repairRadius a e)^4≠0 := by positivity
  have hc : 8/(repairRadius a e)^4 * (((n:ℝ)+1)^2*(repairRadius a e)^4)=8*((n:ℝ)+1)^2 := by
    field_simp
    ring
  rw [hc]
  nlinarith [sq_nonneg (n:ℝ),Nat.cast_nonneg (α := ℝ) n]

/-- This always-issued policy has finite expected total mistakes at every
fixed interior weight, with an explicit nonuniform bound. -/
theorem empirical_expected_failure_upper (a : ℝ) (ha0 : 0<a) (ha1 : a<1)
    (e : ℚ) (he0 : 0<e) (he1 : e≤1/4) :
    (∫⁻ ω, ∑' n, (EmpiricalFailure a e n).indicator 1 ω
      ∂auditSourceLaw a ha0.le ha1.le) ≤ ENNReal.ofReal (8/(repairRadius a e)^4) := by
  rw [lintegral_tsum (f := fun n => (EmpiricalFailure a e n).indicator
      (1 : (ℕ → Bool) → ℝ≥0∞)) (fun n =>
    ((show Measurable (1 : (ℕ → Bool) → ℝ≥0∞) from measurable_const).indicator
      (empiricalFailure_measurable a e n)).aemeasurable)]
  simp_rw [lintegral_indicator_one (empiricalFailure_measurable a e _)]
  exact (ENNReal.tsum_le_tsum (fun n => empirical_probability_spending a ha0 ha1 e he0 he1 n)).trans
    (spending_total_le _ (by positivity))


end
end Orthemology.Tranche3
#print axioms Orthemology.Tranche3.empirical_failure_probability_upper

#print axioms Orthemology.Tranche3.empirical_expected_failure_upper
