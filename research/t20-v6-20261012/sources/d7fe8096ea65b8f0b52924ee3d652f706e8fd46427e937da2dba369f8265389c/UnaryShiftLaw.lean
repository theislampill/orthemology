import TaggedMass

open Set MeasureTheory
open scoped NNReal ENNReal
namespace OrthemologyRationalShift
open P02A2 P02A2.Q8Measure OrthemologyTagged

/-- An alternative to the Python stopping-cell compiler: preserve a unary tag,
then either copy its fresh tail or apply the base observer to that fresh tail. -/
def mixedRows (digits : ℕ → Bool) (base : Cantor → Cantor) (i : ℕ) : Cantor → Cantor :=
  if digits i then id else base

noncomputable def unaryShift (digits : ℕ → Bool) (base : Cantor → Cantor) :=
  tagged (mixedRows digits base)

theorem mixedRows_measurable (digits : ℕ → Bool) {base : Cantor → Cantor}
    (hb : Measurable base) (i : ℕ) : Measurable (mixedRows digits base i) := by
  unfold mixedRows
  split
  · exact measurable_id
  · exact hb

theorem fair_mass_zero : mass fairCantor = 0 := by
  have hp : positive fairCantor = ∅ := by
    ext x
    change (0 < fairCantor {x}) ↔ False
    rw [OrthemologyMeasure.fairCantor_singleton_zero]
    simp
  simp [mass, hp]

noncomputable def diffuseWeight (digits : ℕ → Bool) : ℝ≥0∞ :=
  ∑' i, if digits i then (weight i : ℝ≥0∞) else 0
noncomputable def baseWeight (digits : ℕ → Bool) : ℝ≥0∞ :=
  ∑' i, if digits i then 0 else (weight i : ℝ≥0∞)

theorem weight_partition (digits : ℕ → Bool) : diffuseWeight digits + baseWeight digits = 1 := by
  rw [diffuseWeight, baseWeight, ← ENNReal.tsum_add]
  convert weights_sum using 1
  apply tsum_congr
  intro i
  cases digits i <;> simp

theorem baseWeight_eq (digits : ℕ → Bool) : baseWeight digits = 1 - diffuseWeight digits := by
  exact ENNReal.eq_sub_of_add_eq (by
    have h := weight_partition digits
    exact ne_top_of_le_ne_top ENNReal.one_ne_top (by calc
      diffuseWeight digits ≤ diffuseWeight digits + baseWeight digits := le_self_add
      _ = 1 := h)) (by simpa [add_comm] using weight_partition digits)

/-- Exact actual output-law atomic mass, with all tags and the null exceptional
input handled by the original tagged_mixture_law. -/
theorem unaryShift_mass (digits : ℕ → Bool) {base : Cantor → Cantor}
    (hb : Measurable base) :
    mass (fairCantor.map (unaryShift digits base)) =
      baseWeight digits * mass (fairCantor.map base) := by
  rw [unaryShift, tagged_mass (mixedRows_measurable digits hb)]
  rw [baseWeight, ← ENNReal.tsum_mul_right]
  apply tsum_congr
  intro i
  cases hd : digits i <;> simp [mixedRows, hd, Measure.map_id, fair_mass_zero]

/-- The affine formula is proved at the actual fair-source law, rather than
postulated as an abstract operation on a real number. -/
theorem unaryShift_defect (digits : ℕ → Bool) {base : Cantor → Cantor}
    (hb : Measurable base) :
    defect (fairCantor.map (unaryShift digits base)) =
      (diffuseWeight digits).toReal + (1 - (diffuseWeight digits).toReal) *
        defect (fairCantor.map base) := by
  have hd : diffuseWeight digits ≠ ∞ := ne_top_of_le_ne_top ENNReal.one_ne_top (by
    calc
      diffuseWeight digits ≤ diffuseWeight digits + baseWeight digits := le_self_add
      _ = 1 := weight_partition digits)
  have hl : diffuseWeight digits ≤ 1 := by
    calc
      diffuseWeight digits ≤ diffuseWeight digits + baseWeight digits := le_self_add
      _ = 1 := weight_partition digits
  unfold defect
  rw [unaryShift_mass digits hb, baseWeight_eq, ENNReal.toReal_mul,
    ENNReal.toReal_sub_of_le hl (by simp)]
  simp only [ENNReal.toReal_one]
  ring

theorem diffuseWeight_toReal (digits : ℕ → Bool) :
    (diffuseWeight digits).toReal =
      ∑' i, if digits i then (1/2 : ℝ)^(i+1) else 0 := by
  unfold diffuseWeight
  rw [ENNReal.tsum_toReal_eq (fun i => by split <;> simp)]
  apply tsum_congr
  intro i
  cases hd : digits i <;> simp [hd, weight]

theorem unaryShift_defect_of_weight (digits : ℕ → Bool) {base : Cantor → Cantor}
    (hb : Measurable base) (q : ℝ)
    (hq : (∑' i, if digits i then (1/2 : ℝ)^(i+1) else 0) = q) :
    defect (fairCantor.map (unaryShift digits base)) =
      q + (1-q) * defect (fairCantor.map base) := by
  rw [unaryShift_defect digits hb, diffuseWeight_toReal, hq]

theorem unaryShift_all_diffuse {base : Cantor → Cantor} (hb : Measurable base) :
    defect (fairCantor.map (unaryShift (fun _ => true) base)) = 1 := by
  have hw : diffuseWeight (fun _ => true) = 1 := by
    simpa [diffuseWeight] using weights_sum
  rw [unaryShift_defect _ hb, hw]
  norm_num

theorem unaryShift_no_diffuse {base : Cantor → Cantor} (hb : Measurable base) :
    defect (fairCantor.map (unaryShift (fun _ => false) base)) =
      defect (fairCantor.map base) := by
  rw [unaryShift_defect _ hb]
  simp [diffuseWeight]

end OrthemologyRationalShift
#print axioms OrthemologyRationalShift.unaryShift_defect
