import EndpointMoment
open MeasureTheory Set
open scoped ENNReal
open EndpointMoment

example : (∑' n : ℕ,
    if (1/4 : ℝ) ≤ ((n+1 : ℕ):ℝ)⁻¹ then (1 : ℝ≥0∞) else 0) = 4 := by
  rw [count_reciprocal_thresholds (by norm_num : (0:ℝ) < 1/4)]
  norm_num

example : (∑' n : ℕ,
    if (1/4 : ℝ) ≤ ((n+2+1 : ℕ):ℝ)⁻¹ then (1 : ℝ≥0∞) else 0) = 2 := by
  rw [count_reciprocal_thresholds_tail (by norm_num : (0:ℝ) < 1/4) 2]
  norm_num

example : interior (Measure.dirac (0:ℝ) + Measure.dirac (1:ℝ)) = 0 := by
  simpa [EndpointMoment.interior] using interior_add_endpoint_atoms (0 : Measure ℝ) 1 1

example : inverseVarianceMoment (Measure.dirac (1/2 : ℝ)) = 4 := by
  norm_num [inverseVarianceMoment, EndpointMoment.interior, restrict_dirac]

/-- A genuinely infinite interior measure shows why finite-tail equivalence
requires finite measure, even though the unshifted equivalence does not. -/
example : (∑' n, leftMass ((⊤ : ℝ≥0∞) • Measure.dirac (1/2 : ℝ)) (n+2)) = 0 := by
  unfold leftMass
  rw [tsum_profile_tail_eq_lintegral_floor _ _ measurable_id
    ((ae_interior _).mono fun _ h => h.1)]
  norm_num [EndpointMoment.interior, Measure.restrict_smul, restrict_dirac]

example : leftMoment ((⊤ : ℝ≥0∞) • Measure.dirac (1/2 : ℝ)) = ⊤ := by
  norm_num [leftMoment, EndpointMoment.interior, Measure.restrict_smul, restrict_dirac]

#print axioms EndpointMoment.count_reciprocal_thresholds
#print axioms EndpointMoment.count_reciprocal_thresholds_tail
#print axioms EndpointMoment.tsum_profile_eq_lintegral_floor
#print axioms EndpointMoment.tsum_profile_tail_eq_lintegral_floor
#print axioms EndpointMoment.tsum_profile_lt_top_iff
#print axioms EndpointMoment.endpoint_series_lt_top_iff
#print axioms EndpointMoment.endpoint_tail_series_lt_top_iff
#print axioms EndpointMoment.interior_add_endpoint_atoms
#print EndpointMoment.endpoint_tail_series_lt_top_iff
