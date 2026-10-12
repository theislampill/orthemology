import HeavyCylinders

open Set MeasureTheory Filter
open scoped ENNReal Topology
open P02A2 P02A2.Q8Measure AtomicMembership
namespace AtomicMembershipAudit

theorem fair_cell (n : ℕ) (x : Cantor) :
    fairCantor (cell n x) = (2⁻¹ : ℝ≥0∞)^n := by
  have he : cell n x = Set.pi (↑(Finset.range n) : Set ℕ) (fun i => {x i}) := by
    ext y
    constructor
    · intro hy i hi
      have hy' : bitsPrefix n y = bitsPrefix n x := hy
      exact congrFun hy' ⟨i, Finset.mem_range.mp hi⟩
    · intro hy
      change bitsPrefix n y = bitsPrefix n x
      funext i
      exact hy i.val (Finset.mem_range.mpr i.isLt)
  rw [he, fairCantor_cylinder]
  simp

theorem fair_singleton_zero (x : Cantor) : fairCantor {x} = 0 := by
  apply le_antisymm _ (zero_le _)
  apply ge_of_tendsto' (ENNReal.tendsto_pow_atTop_nhds_zero_of_lt_one
    (by norm_num : (2⁻¹ : ℝ≥0∞) < 1))
  intro n
  rw [← fair_cell n x]
  apply measure_mono
  intro y hy
  rcases hy with rfl
  rfl

theorem fair_mass_zero : mass fairCantor = 0 := by
  have hp : positive fairCantor = ∅ := by
    ext x
    simp [positive, fair_singleton_zero]
  simp [mass, hp]

theorem fair_diagonal_heavy (n : ℕ) : heavy fairCantor n n = univ := by
  ext x
  simp [heavy, fair_cell]

/-- The depth-dependent-threshold mutant declares a diffuse measure atomic. -/
theorem swapped_quantifier_counterexample :
    mass fairCantor ≠ 1 ∧ ∀ n, ∃ k, fairCantor (heavy fairCantor k n) = 1 := by
  constructor
  · rw [fair_mass_zero]
    norm_num
  · intro n
    exact ⟨n, by rw [fair_diagonal_heavy, measure_univ]⟩

/-- Finiteness cannot be dropped even while preserving exact Cantor separation. -/
noncomputable def infiniteFair : Measure Cantor := (∞ : ℝ≥0∞) • fairCantor

theorem infinite_fair_singleton_zero (x : Cantor) : infiniteFair {x} = 0 := by
  simp [infiniteFair, Measure.smul_apply, fair_singleton_zero]

theorem infinite_fair_mass_zero : mass infiniteFair = 0 := by
  have hp : positive infiniteFair = ∅ := by
    ext x
    simp [positive, infinite_fair_singleton_zero]
  simp [mass, hp]

theorem infinite_fair_cell (n : ℕ) (x : Cantor) : infiniteFair (cell n x) = ∞ := by
  simp only [infiniteFair, Measure.smul_apply, smul_eq_mul, fair_cell]
  exact ENNReal.top_mul (ne_of_gt (threshold_pos n))

theorem infinite_fair_heavy (k n : ℕ) : heavy infiniteFair k n = univ := by
  ext x
  simp [heavy, infinite_fair_cell]

theorem finite_measure_hypothesis_counterexample :
    mass infiniteFair = 0 ∧ (⨆ k, ⨅ n, infiniteFair (heavy infiniteFair k n)) = ∞ := by
  refine ⟨infinite_fair_mass_zero, ?_⟩
  simp only [infinite_fair_heavy]
  simp [infiniteFair, Measure.smul_apply]

/-- Prefixes that observe no coordinates measure observation fibres, not points. -/
def blindCell (_n : ℕ) (_x : Cantor) : Set Cantor := univ

theorem separation_hypothesis_counterexample :
    fairCantor {fun _ => false} = 0 ∧
      (⨅ n, fairCantor (blindCell n (fun _ => false))) = 1 := by
  exact ⟨fair_singleton_zero _, by simp [blindCell]⟩

/-- A tied atom approached from above by its diffuse cylinder tail. -/
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
  exact ENNReal.lt_add_right (by norm_num) (mul_ne_zero (by norm_num) (ne_of_gt (threshold_pos n)))

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

/-- A strict threshold does not commute with an infimum at a tied limit. -/
theorem strict_threshold_infimum_counterexample :
    (∀ n : ℕ, (1 / 2 : ℝ) < 1 / 2 + (1 / 2 : ℝ)^(n+1)) ∧
    ¬ ((1 / 2 : ℝ) < 1 / 2) := by
  constructor
  · intro n
    have hp : (0 : ℝ) < (1 / 2 : ℝ)^(n+1) := by positivity
    linarith
  · exact lt_irrefl _

end AtomicMembershipAudit
