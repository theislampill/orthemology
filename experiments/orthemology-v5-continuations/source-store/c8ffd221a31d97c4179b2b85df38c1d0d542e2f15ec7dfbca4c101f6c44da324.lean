import RationalRepairCertificate
import CertifiedRepairCoverage

namespace IndependentRobustControls
open Orthemology.Tranche3

theorem boundary_01 : rationalCertificate 0 1 0 0 = some (1/2) := by norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]
theorem boundary_02 : rationalCertificate (1/2) (1/2) (1/4) (-1/64) = some (5/8) := by norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]
theorem boundary_03 : rationalCertificate 0 1 (1/4) 0 = none := by norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]
theorem boundary_04 : rationalCertificate 0 1 (1/4) (105/1024) = some (19/32) := by norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]
theorem boundary_05 : rationalCertificate 0 1 (1/4) (104/1024) = none := by norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]
theorem boundary_06 : rationalCertificate 1 0 (1/10) 100 = none := by norm_num [rationalCertificate, RationalValid]
theorem boundary_07 : ∃ q : ℝ, RobustGood 1 0 (1/10) 100 q := by
  refine ⟨1/2, by norm_num, by norm_num, ?_⟩
  intro a h1 h0
  linarith
theorem boundary_08 : rationalCertificate 0 0 (1/2) 0 = none := by norm_num [rationalCertificate, RationalValid]
theorem boundary_09 : RobustGood 0 0 (1/2) 0 (1/2) := by
  refine ⟨by norm_num, by norm_num, ?_⟩
  intro a h0 h1
  have ha : a=0 := le_antisymm h1 h0
  subst a
  norm_num [excessZero, excessOne]
theorem boundary_10 : rationalCertificate 0 1 0 (-1/100) = none := by norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]
theorem boundary_11 : rationalCertificate 0 0 (1/4) 0 = some (1/2) := by norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]
theorem boundary_12 : rationalCertificate 1 1 (1/4) 0 = some (3/4) := by norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]
theorem boundary_13 : rationalCertificate 0 1 (-1/4) 100 = none := by norm_num [rationalCertificate, RationalValid]

-- The lower endpoint for vertex zero and upper endpoint for vertex one differ.
theorem boundary_14 : excessZero 0 (1/4) (1/2) > excessZero 1 (1/4) (1/2) := by norm_num [excessZero]
theorem boundary_15 : excessOne 1 (1/4) (1/2) > excessOne 0 (1/4) (1/2) := by norm_num [excessOne]

-- A falsely narrow interval can issue an unsound report for an uncovered alpha.
theorem boundary_16 : rationalCertificate 0 0 (1/4) 0 = some (1/2) ∧
    ¬ (excessOne 1 (1/4) (1/2) ≤ 0) := by
  norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport, excessOne]

-- Positive tolerance is an allowed harm bound, not automatically non-worsening.
theorem boundary_17 : RobustGood 0 1 (1/4) (105/1024) (19/32) ∧
    0 < excessZero 0 (1/4) (19/32) := by
  constructor
  · convert rationalCertificate_sound 0 1 (1/4) (105/1024) (19/32)
      (by norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport]) using 1 <;> norm_num
  · norm_num [excessZero]

-- Real alpha, with no rationality premise, is covered by the emitted certificate.
theorem boundary_18 (a : ℝ) (ha : (49/100:ℝ) ≤ a) (hb : a ≤ (51/100:ℝ)) :
    excessZero a (1/10) (robustReport (49/100) (51/100) (1/10)) ≤ 0 ∧
    excessOne a (1/10) (robustReport (49/100) (51/100) (1/10)) ≤ 0 := by
  have h := rationalCertificate_sound (49/100) (51/100) (1/10) 0 (5499/10000)
    (by norm_num [rationalCertificate, RationalValid, rationalValue, rationalReport])
  have hi := h.2.2 a (by norm_num at ha ⊢; exact ha) (by norm_num at hb ⊢; exact hb)
  norm_num [robustReport] at hi ⊢
  exact hi

#eval rationalCertificate 0 1 0 0
#eval rationalCertificate (1/2) (1/2) (1/4) (-1/64)
#eval rationalCertificate 0 1 (1/4) (105/1024)
#eval rationalCertificate 0 1 (1/4) (104/1024)
#eval rationalCertificate (49/100) (51/100) (1/10) 0
end IndependentRobustControls
