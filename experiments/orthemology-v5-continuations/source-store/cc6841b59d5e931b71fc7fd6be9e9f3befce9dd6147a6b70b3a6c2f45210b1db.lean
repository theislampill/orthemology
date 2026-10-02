/- Classical countable-cocountable counterexample; see Fremlin, Measure Theory 211R.
This guards the meaning of positive-singleton mass on general measurable spaces. -/
import TotalVariation
import Mathlib.Data.Real.Cardinality

open Set MeasureTheory
open scoped ENNReal
namespace OrthemologyMeasure
namespace CoCountable

variable (X : Type*)
def space : MeasurableSpace X where
  MeasurableSet' s := s.Countable ∨ sᶜ.Countable
  measurableSet_empty := Or.inl countable_empty
  measurableSet_compl := by
    intro s hs
    simpa only [compl_compl, or_comm] using hs
  measurableSet_iUnion := by
    intro f hf
    classical
    by_cases hc : ∀ n, (f n).Countable
    · exact Or.inl (Set.countable_iUnion hc)
    · obtain ⟨n, hn⟩ := not_forall.mp hc
      have hcomp := (hf n).resolve_left hn
      exact Or.inr (hcomp.mono (compl_subset_compl.mpr (subset_iUnion f n)))

local instance : MeasurableSpace X := space X

local instance : MeasurableSingletonClass X := ⟨fun x => Or.inl (countable_singleton x)⟩

noncomputable def value (s : Set X) : ℝ≥0∞ := by
  classical
  exact if s.Countable then 0 else 1

theorem value_iUnion {f : ℕ → Set X} (hf : ∀ n, MeasurableSet (f n))
    (hd : Pairwise (fun i j => Disjoint (f i) (f j))) : value X (⋃ n, f n) = ∑' n, value X (f n) := by
  classical
  by_cases hc : ∀ n, (f n).Countable
  · simp [value, Set.countable_iUnion hc, hc]
  · obtain ⟨n, hn⟩ := not_forall.mp hc
    have hu : ¬ (⋃ n, f n).Countable := fun h => hn (h.mono (subset_iUnion f n))
    have hcomp : (f n)ᶜ.Countable := (hf n).resolve_left hn
    have hothers : ∀ k, k ≠ n → (f k).Countable := by
      intro k hkn
      apply hcomp.mono
      intro x hx hxn
      exact Set.disjoint_left.mp (hd hkn) hx hxn
    rw [tsum_eq_single n (fun k hk => by simp [value, hothers k hk])]
    simp [value, hu, hn]

noncomputable def law : Measure X :=
  Measure.ofMeasurable (fun s _ => value X s) (by simp [value])
    (fun {f} hf hd => value_iUnion X hf hd)

theorem law_apply {s : Set X} (hs : MeasurableSet s) : law X s = value X s :=
  Measure.ofMeasurable_apply s hs

instance law_probability [Uncountable X] : IsProbabilityMeasure (law X) := by
  constructor
  rw [law_apply X MeasurableSet.univ]
  simp [value, Set.not_countable_univ]

theorem singleton_zero (x : X) : law X {x} = 0 := by
  rw [law_apply X (measurableSet_singleton x)]
  simp [value]

theorem measurable_zero_or_one {s : Set X} (hs : MeasurableSet s) :
    law X s = 0 ∨ law X s = 1 := by
  rw [law_apply X hs]
  unfold value
  split <;> simp

/-- The entire probability space is a measure-algebra atom: every measurable
subset has either zero mass or the same mass as the whole space. -/
theorem whole_space_atom [Uncountable X] :
    law X univ = 1 ∧ ∀ s : Set X, MeasurableSet s → law X s = 0 ∨ law X s = law X univ := by
  constructor
  · exact measure_univ
  · intro s hs
    simpa only [measure_univ] using measurable_zero_or_one X hs

/-- Nonetheless its positive-singleton defect is one. -/
theorem point_defect_one [Uncountable X] : P02A2.defect (law X) = 1 := by
  have hp : P02A2.positive (law X) = ∅ := by
    ext x
    change (0 < law X {x}) ↔ False
    rw [singleton_zero]
    simp
  simp [P02A2.defect, P02A2.mass, hp]

/-- A concrete inhabited uncountable carrier, not a free existence assumption. -/
theorem real_counterexample :
    law ℝ univ = 1 ∧ @P02A2.defect ℝ (space ℝ) (law ℝ) = 1 :=
  ⟨(whole_space_atom ℝ).1, point_defect_one ℝ⟩

end CoCountable
end OrthemologyMeasure
#print axioms OrthemologyMeasure.CoCountable.whole_space_atom
#print axioms OrthemologyMeasure.CoCountable.point_defect_one
#print axioms OrthemologyMeasure.CoCountable.real_counterexample
