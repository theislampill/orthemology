import Q8Measure
import Mathlib.Data.ENNReal.Inv

open Set MeasureTheory
open scoped ENNReal
namespace AtomicMembership
open P02A2 P02A2.Q8Measure

def bitsPrefix (n : ℕ) (x : Cantor) : Fin n → Bool := fun i => x i.val
def cylinder (n : ℕ) (w : Fin n → Bool) : Set Cantor := bitsPrefix n ⁻¹' {w}
def cell (n : ℕ) (x : Cantor) : Set Cantor := cylinder n (bitsPrefix n x)

theorem prefix_measurable (n : ℕ) : Measurable (bitsPrefix n) :=
  measurable_pi_lambda _ fun i => measurable_pi_apply i.val

theorem cylinder_measurable (n : ℕ) (w : Fin n → Bool) : MeasurableSet (cylinder n w) :=
  (prefix_measurable n) (measurableSet_singleton w)

theorem cell_antitone (x : Cantor) : Antitone (fun n => cell n x) := by
  intro n m h y hy
  change bitsPrefix n y = bitsPrefix n x
  change bitsPrefix m y = bitsPrefix m x at hy
  funext i
  exact congrFun hy ⟨i.val, lt_of_lt_of_le i.isLt h⟩

theorem cell_inter (x : Cantor) : (⋂ n, cell n x) = {x} := by
  ext y
  simp only [mem_iInter, mem_singleton_iff]
  constructor
  · intro h
    funext n
    have hh : bitsPrefix (n+1) y = bitsPrefix (n+1) x := h (n+1)
    exact congrFun hh ⟨n, Nat.lt_succ_self n⟩
  · intro h n
    subst y
    rfl

theorem singleton_mass (μ : Measure Cantor) [IsFiniteMeasure μ] (x : Cantor) :
    μ {x} = ⨅ n, μ (cell n x) := by
  rw [← cell_inter x]
  exact (cell_antitone x).measure_iInter (fun n => (cylinder_measurable n _).nullMeasurableSet)
    ⟨0, measure_ne_top μ _⟩

noncomputable def heavy (μ : Measure Cantor) (k n : ℕ) : Set Cantor :=
  {x | (2⁻¹ : ℝ≥0∞)^k ≤ μ (cell n x)}
noncomputable def level (μ : Measure Cantor) (k : ℕ) : Set Cantor :=
  {x | (2⁻¹ : ℝ≥0∞)^k ≤ μ {x}}

theorem heavy_measurable (μ : Measure Cantor) (k n : ℕ) : MeasurableSet (heavy μ k n) := by
  have hm : Measurable (fun w : Fin n → Bool => μ (cylinder n w)) := measurable_of_countable _
  exact measurableSet_le measurable_const (hm.comp (prefix_measurable n))

theorem heavy_antitone (μ : Measure Cantor) (k : ℕ) : Antitone (heavy μ k) := by
  intro n m h x hx
  exact hx.trans (measure_mono (cell_antitone x h))

theorem level_inter (μ : Measure Cantor) [IsFiniteMeasure μ] (k : ℕ) :
    level μ k = ⋂ n, heavy μ k n := by
  ext x
  simp only [level, heavy, mem_setOf_eq, mem_iInter, singleton_mass, le_iInf_iff]

theorem level_measurable (μ : Measure Cantor) [IsFiniteMeasure μ] (k : ℕ) :
    MeasurableSet (level μ k) := by
  rw [level_inter]
  exact MeasurableSet.iInter (heavy_measurable μ k)

theorem level_mass (μ : Measure Cantor) [IsFiniteMeasure μ] (k : ℕ) :
    μ (level μ k) = ⨅ n, μ (heavy μ k n) := by
  rw [level_inter]
  exact (heavy_antitone μ k).measure_iInter (fun n => (heavy_measurable μ k n).nullMeasurableSet)
    ⟨0, measure_ne_top μ _⟩

theorem threshold_pos (k : ℕ) : 0 < (2⁻¹ : ℝ≥0∞)^k := by
  exact pos_iff_ne_zero.mpr (pow_ne_zero k (by norm_num))

theorem level_monotone (μ : Measure Cantor) : Monotone (level μ) := by
  intro k l h x hx
  change (2⁻¹ : ℝ≥0∞)^l ≤ μ {x}
  change (2⁻¹ : ℝ≥0∞)^k ≤ μ {x} at hx
  apply le_trans _ hx
  exact pow_le_pow_of_le_one (by positivity) (by norm_num) h

theorem positive_union (μ : Measure Cantor) : positive μ = ⋃ k, level μ k := by
  ext x
  simp only [positive, level, mem_setOf_eq, mem_iUnion]
  constructor
  · intro hx
    obtain ⟨k,hk⟩ := ENNReal.exists_inv_two_pow_lt (ne_of_gt hx)
    exact ⟨k,hk.le⟩
  · rintro ⟨k,hk⟩
    exact (threshold_pos k).trans_le hk

/-- Actual atomic mass from finite cylinder threshold events. This is a hard
threshold alternative to the repository's cylinder excess formula. -/
theorem atomic_mass_formula (μ : Measure Cantor) [IsFiniteMeasure μ] :
    mass μ = ⨆ k, ⨅ n, μ (heavy μ k n) := by
  unfold mass
  rw [positive_union, (level_monotone μ).measure_iUnion]
  congr 1
  funext k
  exact level_mass μ k

noncomputable def heavyWords (μ : Measure Cantor) (k n : ℕ) : Finset (Fin n → Bool) :=
  Finset.univ.filter (fun w => (2⁻¹ : ℝ≥0∞)^k ≤ μ (cylinder n w))

theorem heavy_union (μ : Measure Cantor) (k n : ℕ) :
    heavy μ k n = ⋃ w ∈ heavyWords μ k n, cylinder n w := by
  classical
  ext x
  simp only [mem_iUnion]
  constructor
  · intro hx
    exact ⟨bitsPrefix n x, by simpa [heavyWords, heavy, cell] using hx, rfl⟩
  · rintro ⟨w,hw,hx⟩
    change bitsPrefix n x = w at hx
    change (2⁻¹ : ℝ≥0∞)^k ≤ μ (cylinder n (bitsPrefix n x))
    rw [hx]
    simpa [heavyWords] using hw

theorem cylinders_disjoint (n : ℕ) : Pairwise (fun a b => Disjoint (cylinder n a) (cylinder n b)) := by
  intro a b hab
  apply disjoint_left.mpr
  intro x ha hb
  change bitsPrefix n x = a at ha
  change bitsPrefix n x = b at hb
  exact hab (ha.symm.trans hb)

theorem heavy_finite_sum (μ : Measure Cantor) (k n : ℕ) :
    μ (heavy μ k n) = ∑ w ∈ heavyWords μ k n, μ (cylinder n w) := by
  rw [heavy_union]
  exact measure_biUnion_finset ((cylinders_disjoint n).set_pairwise _) (fun w _ => cylinder_measurable n w)

/-- A rationally indexed forall-exists-forall normal form. The inner finite
sum is exact; effectivity is supplied separately by a program's cylinder table. -/
theorem mass_one_normal_form (μ : Measure Cantor) [IsProbabilityMeasure μ] :
    mass μ = 1 ↔ ∀ q : ℚ, 0 ≤ q → (Real.toNNReal q : ℝ≥0∞) < 1 →
      ∃ k, ∀ n, (Real.toNNReal q : ℝ≥0∞) ≤ μ (heavy μ k n) := by
  constructor
  · intro hm q hq hq1
    have hl : (Real.toNNReal q : ℝ≥0∞) < ⨆ k, ⨅ n, μ (heavy μ k n) := by
      rw [← atomic_mass_formula, hm]
      exact hq1
    obtain ⟨k,hk⟩ := lt_iSup_iff.mp hl
    exact ⟨k, fun n => hk.le.trans (iInf_le _ n)⟩
  · intro h
    apply le_antisymm (by simpa using positive_le_total μ)
    by_contra hnot
    have hlt : mass μ < 1 := lt_of_not_ge hnot
    obtain ⟨q,hq,hleft,hright⟩ := ENNReal.lt_iff_exists_rat_btwn.mp hlt
    obtain ⟨k,hk⟩ := h q hq hright
    have hb : (Real.toNNReal q : ℝ≥0∞) ≤ mass μ := by
      rw [atomic_mass_formula]
      exact (le_iInf hk).trans (le_iSup (fun k => ⨅ n, μ (heavy μ k n)) k)
    exact (not_le_of_gt hleft) hb

end AtomicMembership
