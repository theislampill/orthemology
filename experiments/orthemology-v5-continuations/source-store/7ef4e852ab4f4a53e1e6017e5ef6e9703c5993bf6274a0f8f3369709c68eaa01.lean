import RepairTestingBridge

namespace Orthemology.Tranche2

/-- Accepted score constraints already put this local binary repair in the
interior of the probability simplex. -/
theorem binary_good_is_coherent (a e q : ℝ)
    (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (he0 : 0 ≤ e) (he1 : e ≤ 1/4)
    (hg : BinaryGood a e q) : 0 < q ∧ q < 1 := by
  have hb := RepairObstruction.binary_repair_readout a e q 0
    ha0 ha1 he0 he1 (by rfl) (by simpa using hg.1) (by simpa using hg.2)
  rcases abs_le.mp hb with ⟨hlo,hhi⟩
  have hae := mul_nonneg ha0 he0
  have hbe := mul_nonneg (sub_nonneg.mpr ha1) he0
  have hee := mul_nonneg he0 (sub_nonneg.mpr he1)
  constructor <;> nlinarith

/-- A uniform nonzero interior part of a quadratic dominance cell. -/
theorem sufficient_binary_cell (r D d : ℝ)
    (hr0 : 0 ≤ r) (hr1 : r ≤ 1) (hD0 : 0 < D) (hD1 : D ≤ 1)
    (hd : |d| ≤ D/4) :
    (r+d)^2 < r^2+D ∧ (1-(r+d))^2 < (1-r)^2+D := by
  rcases abs_le.mp hd with ⟨hdlo,hdhi⟩
  have hsq := mul_nonneg (sub_nonneg.mpr hdhi) (by linarith : 0 ≤ d+D/4)
  have hDsq := mul_nonneg hD0.le (sub_nonneg.mpr hD1)
  have hc1 := mul_nonneg hr0 (sub_nonneg.mpr hdhi)
  have hc2 := mul_nonneg (sub_nonneg.mpr hr1) hD0.le
  have hc3 := mul_nonneg (sub_nonneg.mpr hr1) (by linarith : 0 ≤ d+D/4)
  have hc4 := mul_nonneg hr0 hD0.le
  constructor <;> nlinarith

/-- An estimate within a specified shrinking tolerance supplies a genuinely
strict all-state repair, rather than only the necessary decoder tolerance. -/
theorem approximate_parameter_strict_repair (a e estimate : ℝ)
    (ha0 : 0 < a) (ha1 : a < 1) (he0 : 0 < e) (he1 : e ≤ 1/4)
    (hest : |estimate-a| ≤ a*(1-a)*e/4) :
    let q := 1/2+estimate*e
    q^2 < a*(1/2+e)^2+(1-a)*(1/2)^2 ∧
    (1-q)^2 < a*(1/2-e)^2+(1-a)*(1/2)^2 := by
  let r : ℝ := 1/2+a*e
  let D : ℝ := a*(1-a)*e^2
  let d : ℝ := (estimate-a)*e
  have hD0 : 0 < D := mul_pos (mul_pos ha0 (sub_pos.mpr ha1)) (sq_pos_of_pos he0)
  have haq : a*(1-a) ≤ (1:ℝ)/4 := by nlinarith [sq_nonneg (a-1/2)]
  have hae := mul_nonneg ha0.le he0.le
  have hbe := mul_nonneg (sub_nonneg.mpr ha1.le) he0.le
  have hee := mul_nonneg he0.le (sub_nonneg.mpr he1)
  have hD1 : D ≤ 1 := by
    dsimp [D]
    have h := mul_le_mul_of_nonneg_right haq (sq_nonneg e)
    nlinarith
  have hr0 : 0 ≤ r := by dsimp [r]; nlinarith
  have hr1 : r ≤ 1 := by dsimp [r]; nlinarith
  have hd : |d| ≤ D/4 := by
    dsimp [d,D]
    rw [abs_mul, abs_of_pos he0]
    have h := mul_le_mul_of_nonneg_right hest he0.le
    nlinarith
  have h := sufficient_binary_cell r D d hr0 hr1 hD0 hD1 hd
  dsimp [r,D,d] at h
  dsimp
  constructor <;> nlinarith [h.1,h.2]

end Orthemology.Tranche2

#print axioms Orthemology.Tranche2.binary_good_is_coherent
#print axioms Orthemology.Tranche2.sufficient_binary_cell
#print axioms Orthemology.Tranche2.approximate_parameter_strict_repair
#check Orthemology.Tranche2.approximate_parameter_strict_repair
