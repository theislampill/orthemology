import RepairTestingBridge
import CountableIdentification
import Mathlib.MeasureTheory.Constructions.Polish.Basic

open MeasureTheory Set Filter
open scoped Topology

namespace Orthemology.Tranche2

/-- Literal eventual all-state improvement forces asymptotically exact decoding
of the norm. No assumed convergence of the repair algorithm is used. -/
theorem eventual_binary_good_decodes (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (e q : ℕ → ℝ) (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (he : Tendsto e atTop (𝓝 0))
    (hgood : ∀ᶠ n in atTop, BinaryGood a (e n) (q n)) :
    Tendsto (fun n => (q n - 1/2) / e n) atTop (𝓝 a) := by
  apply tendsto_iff_norm_sub_tendsto_zero.mpr
  have hbound : ∀ᶠ n in atTop, ‖(q n - 1/2) / e n - a‖ ≤ e n / 2 := by
    apply hgood.mono
    intro n hn
    have h := RepairObstruction.binary_parameter_decoder a (e n) (q n) 0
      ha0 ha1 (he0 n) (he1 n) (by rfl) (by simpa using hn.1) (by simpa using hn.2)
    simpa [Real.norm_eq_abs] using h
  have hehalf : Tendsto (fun n => e n / 2) atTop (𝓝 0) := by
    simpa using he.div_const 2
  exact squeeze_zero' (Eventually.of_forall fun n => norm_nonneg _) hbound hehalf

/-- General measurable sequences have positive-measure distinct limit values
at most countably often under an s-finite reference. -/
theorem countable_positive_limit_values
    {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [SFinite μ] (f : ℕ → Ω → ℝ)
    (hf : ∀ n, Measurable (f n)) :
    Set.Countable {a : ℝ | 0 < μ {ω | Tendsto (fun n => f n ω) atTop (𝓝 a)}} := by
  apply Measure.countable_meas_pos_of_disjoint_iUnion
  · intro a
    exact measurableSet_tendsto (𝓝 a) hf
  · intro a b hab
    change Disjoint {ω | Tendsto (fun n => f n ω) atTop (𝓝 a)}
      {ω | Tendsto (fun n => f n ω) atTop (𝓝 b)}
    rw [Set.disjoint_left]
    intro ω ha hb
    exact hab (tendsto_nhds_unique ha hb)

/-- Applied countability theorem with the actual repair-score predicate.
The finite-information trace domination is explicit; the norm readout and
its convergence are derived, not assumed. -/
theorem countable_positive_eventual_binary_repairs
    {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsFiniteMeasure μ] (ν : ℝ → Measure Ω)
    (F : Set Ω) (hF : MeasurableSet F)
    (e : ℕ → ℝ) (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (he : Tendsto e atTop (𝓝 0))
    (q : ℕ → Ω → ℝ) (hq : ∀ n, Measurable (q n))
    (hdom : ∀ a, (ν a).restrict F ≪ μ.restrict F) :
    Set.Countable {a : ℝ | a ∈ Icc 0 1 ∧
      0 < ν a (F ∩ {ω | ∀ᶠ n in atTop, BinaryGood a (e n) (q n ω)})} := by
  let f : ℕ → Ω → ℝ := fun n ω => (q n ω - 1/2) / e n
  have hf : ∀ n, Measurable (f n) := by
    intro n
    exact ((hq n).sub_const (1/2)).div_const (e n)
  apply (countable_positive_limit_values (μ.restrict F) f hf).mono
  intro a ha
  rcases ha with ⟨⟨ha0,ha1⟩,hpos⟩
  have hsub : F ∩ {ω | ∀ᶠ n in atTop, BinaryGood a (e n) (q n ω)} ⊆
      {ω | Tendsto (fun n => f n ω) atTop (𝓝 a)} := by
    intro ω hω
    exact eventual_binary_good_decodes a ha0 ha1 e (fun n => q n ω) he0 he1 he hω.2
  by_contra hz
  have hzero : (μ.restrict F) {ω | Tendsto (fun n => f n ω) atTop (𝓝 a)} = 0 :=
    le_antisymm (le_of_not_gt hz) (zero_le _)
  have hvzero := hdom a hzero
  have hs := measure_mono_null hsub hvzero
  rw [Measure.restrict_apply' hF] at hs
  have hset : (F ∩ {ω | ∀ᶠ n in atTop, BinaryGood a (e n) (q n ω)}) ∩ F =
      F ∩ {ω | ∀ᶠ n in atTop, BinaryGood a (e n) (q n ω)} := by
    ext ω
    simp only [mem_inter_iff]
    tauto
  rw [hset] at hs
  exact (ne_of_gt hpos) hs

end Orthemology.Tranche2

#print axioms Orthemology.Tranche2.eventual_binary_good_decodes
#print axioms Orthemology.Tranche2.countable_positive_limit_values
#print axioms Orthemology.Tranche2.countable_positive_eventual_binary_repairs
#check Orthemology.Tranche2.countable_positive_eventual_binary_repairs
