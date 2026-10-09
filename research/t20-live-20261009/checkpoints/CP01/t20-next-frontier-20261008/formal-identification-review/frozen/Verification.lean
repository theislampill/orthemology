import CalibratedPanels

open CalibratedIdentification

#check @jointCode_injective
#check @calibrated_five_counts_injective
#check @hit_injective_of_empty_zero
#check @calibrated_panels_identify
#check @calibrated_panels_identify_coefficients
#print axioms jointCode_injective
#print axioms calibrated_five_counts_injective
#print axioms hit_injective_of_empty_zero
#print axioms calibrated_panels_identify
#print axioms calibrated_panels_identify_coefficients

/-- Empty effect type is covered; the theorem has no hidden nonempty-type assumption. -/
example (H K : Histogram Empty) (h : SamePanels H K) : H = K :=
  calibrated_panels_identify H K h

/-- Any finite catalogue size and unbounded natural counts are covered. -/
example (size : ℕ) (H K : Histogram (Fin size)) (h : SamePanels H K) : H = K :=
  calibrated_panels_identify H K h

/-- Numerical normalization check for the actual calibrated rational code. -/
example : jointCode 1 1 1 = (5 / 18 : ℚ) := by norm_num [jointCode]
