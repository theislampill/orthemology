import P02A2.MeasureCore
import Mathlib.Probability.ProductMeasure
import Mathlib.Probability.ProbabilityMassFunction.Constructions
import Mathlib.Analysis.SpecificLimits.Basic

/-! Actual fair-Cantor measure semantics for a switch that copies each fresh
input bit once a persistent bounded halt flag is true. The measure lemmas do
not themselves assert a computable numbering or a byte-code compiler theorem. -/
namespace P02A2.Q8Measure
open Set MeasureTheory Filter
open scoped ENNReal Topology BigOperators

abbrev Cantor := ℕ → Bool

noncomputable def fairBit : Measure Bool :=
  (PMF.bernoulli (1 / 2) (by norm_num)).toMeasure

instance fairBit_probability : IsProbabilityMeasure fairBit := by
  unfold fairBit
  infer_instance

theorem fairBit_singleton (b : Bool) : fairBit {b} = (1 / 2 : ℝ≥0∞) := by
  unfold fairBit
  rw [PMF.toMeasure_apply_singleton _ b (measurableSet_singleton b), PMF.bernoulli_apply]
  cases b <;> norm_num

noncomputable def fairCantor : Measure Cantor :=
  Measure.infinitePi (fun _ : ℕ => fairBit)

instance fairCantor_probability : IsProbabilityMeasure fairCantor := by
  unfold fairCantor
  infer_instance

theorem fairCantor_cylinder (s : Finset ℕ) (y : Cantor) :
    fairCantor (Set.pi (s : Set ℕ) (fun n => {y n})) = (1 / 2 : ℝ≥0∞)^s.card := by
  rw [fairCantor, Measure.infinitePi_pi _ (fun n _ => measurableSet_singleton (y n))]
  simp only [fairBit_singleton, Finset.prod_const]

def switched (halted : ℕ → Bool) (x : Cantor) (n : ℕ) : Bool :=
  if halted n then x n else false

theorem switched_measurable (halted : ℕ → Bool) : Measurable (switched halted) := by
  apply measurable_pi_lambda
  intro n
  cases h : halted n
  · simpa only [switched, h, Bool.false_eq_true, ↓reduceIte] using
      (measurable_const : Measurable (fun _ : Cantor => false))
  · simpa only [switched, h, ↓reduceIte] using
      (measurable_pi_apply n : Measurable (fun x : Cantor => x n))

noncomputable def law (halted : ℕ → Bool) : Measure Cantor :=
  fairCantor.map (switched halted)

instance law_probability (halted : ℕ → Bool) : IsProbabilityMeasure (law halted) := by
  constructor
  rw [law, Measure.map_apply (switched_measurable halted) MeasurableSet.univ]
  simp

theorem never_law_dirac (halted : ℕ → Bool) (h : ∀ n, halted n = false) :
    law halted = Measure.dirac (fun _ : ℕ => false) := by
  have he : switched halted = fun _ : Cantor => fun _ : ℕ => false := by
    funext x n
    simp [switched, h]
  rw [law, he, Measure.map_const]
  simp

theorem eventually_singleton_bound (halted : ℕ → Bool) (N : ℕ)
    (hN : ∀ n, N ≤ n → halted n = true) (y : Cantor) (k : ℕ) :
    law halted {y} ≤ (1 / 2 : ℝ≥0∞)^k := by
  rw [law, Measure.map_apply (switched_measurable halted) (measurableSet_singleton y)]
  have hs : switched halted ⁻¹' {y} ⊆
      Set.pi (↑(Finset.Ico N (N+k)) : Set ℕ) (fun n => {y n}) := by
    intro x hx n hn
    change switched halted x = y at hx
    have hnN : N ≤ n := (Finset.mem_Ico.mp hn).1
    have he := congrFun hx n
    simpa [switched, hN n hnN] using he
  have hb := measure_mono (μ := fairCantor) hs
  rw [fairCantor_cylinder] at hb
  simpa only [Nat.card_Ico, Nat.add_sub_cancel_left] using hb

theorem eventually_singleton_zero (halted : ℕ → Bool) (N : ℕ)
    (hN : ∀ n, N ≤ n → halted n = true) (y : Cantor) : law halted {y} = 0 := by
  apply le_antisymm _ (zero_le _)
  apply ge_of_tendsto' (ENNReal.tendsto_pow_atTop_nhds_zero_of_lt_one
    (by norm_num : (1 / 2 : ℝ≥0∞) < 1))
  exact eventually_singleton_bound halted N hN y

theorem never_defect_zero (halted : ℕ → Bool) (h : ∀ n, halted n = false) :
    defect (law halted) = 0 := by
  have hc : ({fun _ : ℕ => false} : Set Cantor).Countable := Set.countable_singleton _
  have hm : mass (law halted) = 1 := countable_carrier_mass_one (law halted) hc
    (by rw [never_law_dirac halted h]; simp) (measure_univ)
  simp [defect, hm]

theorem eventually_defect_one (halted : ℕ → Bool) (N : ℕ)
    (hN : ∀ n, N ≤ n → halted n = true) : defect (law halted) = 1 := by
  have hp : positive (law halted) = ∅ := by
    ext y
    simp [positive, eventually_singleton_zero halted N hN y]
  simp [defect, mass, hp]

end P02A2.Q8Measure
