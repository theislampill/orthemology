p='private-locator:d60ad99e1a4115ab9144'
s=open(p).read(); pos=s.index('/-- A strict threshold')
s=s[:pos]+'''/-- A tied atom approached from above by its diffuse cylinder tail. -/
noncomputable def tiedLaw : Measure Cantor :=
  (1/2 : ℝ≥0∞) • Measure.dirac (fun _ => false) + (1/2 : ℝ≥0∞) • fairCantor

theorem tied_singleton : tiedLaw {fun _ => false} = (1/2 : ℝ≥0∞) := by
  simp [tiedLaw, Measure.add_apply, Measure.smul_apply, fair_singleton_zero]

theorem tied_cell (n : ℕ) :
    tiedLaw (cell n (fun _ => false)) = (1/2 : ℝ≥0∞) + (1/2 : ℝ≥0∞)*(2⁻¹ : ℝ≥0∞)^n := by
  simp only [tiedLaw, Measure.add_apply, Measure.smul_apply, smul_eq_mul, fair_cell]
  rw [Measure.dirac_apply_of_mem (show (fun _ => false) ∈ cell n (fun _ => false) from rfl)]
  simp

theorem tied_cell_strict (n : ℕ) :
    (1/2 : ℝ≥0∞) < tiedLaw (cell n (fun _ => false)) := by
  rw [tied_cell]
  exact ENNReal.lt_add_right (by norm_num) (by positivity)

/-- Strict comparison cannot replace inclusive comparison in level_inter. -/
theorem strict_level_inter_counterexample :
    {x : Cantor | (1/2 : ℝ≥0∞) < tiedLaw {x}} ≠
      ⋂ n, {x : Cantor | (1/2 : ℝ≥0∞) < tiedLaw (cell n x)} := by
  intro he
  have hm : (fun _ => false) ∈ ⋂ n, {x : Cantor | (1/2 : ℝ≥0∞) < tiedLaw (cell n x)} :=
    mem_iInter.mpr tied_cell_strict
  rw [← he] at hm
  change (1/2 : ℝ≥0∞) < tiedLaw {fun _ => false} at hm
  rw [tied_singleton] at hm
  exact lt_irrefl _ hm

'''+s[pos:];open(p,'w').write(s)
