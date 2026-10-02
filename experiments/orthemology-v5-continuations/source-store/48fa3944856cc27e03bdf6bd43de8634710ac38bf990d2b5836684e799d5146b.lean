import RobustBinaryRepair

namespace Orthemology.Tranche3

/-- Literal one-model correctness, retaining coherent admissibility. -/
def LiteralRepairGood (a e q : ℝ) : Prop :=
  0 ≤ q ∧ q ≤ 1 ∧ excessZero a e q ≤ 0 ∧ excessOne a e q ≤ 0

/-- Positive-weight successful reports occupy a shrinking punctured
neighbourhood of the zero-weight oracle report. -/
theorem positive_weight_punctured_cell (a e q : ℝ)
    (ha : 0 < a) (he0 : 0 < e) (he1 : e ≤ 1/4)
    (h : LiteralRepairGood a e q) :
    1/2 < q ∧ q ≤ 1/2+a*e*(1+e) := by
  rcases h with ⟨hq0,hq1,hz,ho⟩
  rw [excessZero_expand] at hz
  rw [excessOne_expand] at ho
  have hp : 0 < a*e*(1-e) := mul_pos (mul_pos ha he0) (by linarith)
  constructor
  · nlinarith [sq_nonneg (q-1/2)]
  · nlinarith [sq_nonneg (q-1/2)]

/-- The closed-family endpoint has exactly one coherent weak repair. -/
theorem zero_weight_unique (e q : ℝ) : LiteralRepairGood 0 e q ↔ q=1/2 := by
  constructor
  · rintro ⟨hq0,hq1,hz,ho⟩
    simp only [excessZero,excessOne] at hz ho
    nlinarith [sq_nonneg (q-1/2)]
  · rintro rfl
    norm_num [LiteralRepairGood,excessZero,excessOne]

/-- The opposite endpoint has the analogous unique repair. -/
theorem one_weight_unique (e q : ℝ) (he0 : 0 ≤ e) (he1 : e ≤ 1/4) :
    LiteralRepairGood 1 e q ↔ q=1/2+e := by
  constructor
  · rintro ⟨hq0,hq1,hz,ho⟩
    simp only [excessZero,excessOne] at hz ho
    rcases le_total q (1/2+e) with h | h <;> nlinarith [sq_nonneg (q-(1/2+e))]
  · rintro rfl
    constructor
    · linarith
    constructor
    · linarith
    constructor <;> simp [excessZero,excessOne]
    all_goals ring_nf
    all_goals norm_num

/-- At weights below one, the other endpoint is also approached through a
punctured cell. Its width is controlled directly, with epsilon fixed. -/
theorem below_one_punctured_cell (a e q : ℝ)
    (ha : a < 1) (he0 : 0 < e) (he1 : e ≤ 1/4)
    (h : LiteralRepairGood a e q) :
    1/2+e-2*e*(1-a) ≤ q ∧ q < 1/2+e := by
  rcases h with ⟨hq0,hq1,hz,ho⟩
  rw [excessZero_expand] at hz
  rw [excessOne_expand] at ho
  have hgap : 0 < (1-a)*e*(1+e) := mul_pos (mul_pos (by linarith) he0) (by linarith)
  have hq : q < 1/2+e := by nlinarith
  have hd : 0 ≤ 1/2+e-q := by linarith
  have hprod := mul_nonneg (by linarith : 0 ≤ 1/2-2*e) hd
  have hpositive := mul_nonneg (sub_nonneg.mpr ha.le) (sq_nonneg e)
  constructor
  · nlinarith [sq_nonneg (1/2+e-q)]
  · exact hq

end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.positive_weight_punctured_cell
#print axioms Orthemology.Tranche3.zero_weight_unique
#print axioms Orthemology.Tranche3.one_weight_unique
#print axioms Orthemology.Tranche3.below_one_punctured_cell
