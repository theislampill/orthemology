import Q8Measure
import Mathlib.Data.Set.Finite.Lattice
import Mathlib

/-! Exact finite/infinite deterministic fresh-bit revelation under fair Cantor
input. The predicate is about the locations where input coordinates are copied;
it is not a claim about arbitrary observers or target-specific learnability. -/
namespace P02A2.InnovationMeasure
open Set MeasureTheory Filter
open P02A2.Q8Measure
open scoped ENNReal Topology

def copied (flag : ℕ → Bool) : Set ℕ := {n | flag n = true}

theorem singleton_bound_of_copied (flag : ℕ → Bool) (s : Finset ℕ)
    (hs : ↑s ⊆ copied flag) (y : Cantor) :
    law flag {y} ≤ (1 / 2 : ℝ≥0∞)^s.card := by
  rw [law, Measure.map_apply (switched_measurable flag) (measurableSet_singleton y)]
  have hp : switched flag ⁻¹' {y} ⊆ Set.pi (↑s : Set ℕ) (fun n => {y n}) := by
    intro x hx n hn
    change switched flag x = y at hx
    have he := congrFun hx n
    simpa [switched, show flag n = true from hs hn] using he
  exact (measure_mono hp).trans_eq (fairCantor_cylinder s y)

theorem infinite_copied_singleton_zero (flag : ℕ → Bool) (h : (copied flag).Infinite)
    (y : Cantor) : law flag {y} = 0 := by
  apply le_antisymm _ (zero_le _)
  apply ge_of_tendsto' (ENNReal.tendsto_pow_atTop_nhds_zero_of_lt_one
    (by norm_num : (1 / 2 : ℝ≥0∞) < 1))
  intro k
  obtain ⟨s, hs, hcard⟩ := h.exists_subset_card_eq k
  simpa only [hcard] using singleton_bound_of_copied flag s hs y

theorem infinite_copied_defect_one (flag : ℕ → Bool) (h : (copied flag).Infinite) :
    defect (law flag) = 1 := by
  have hp : positive (law flag) = ∅ := by
    ext y
    change (0 < law flag {y}) ↔ False
    rw [infinite_copied_singleton_zero flag h y]
    simp only [lt_self_iff_false]
  simp [defect, mass, hp]

def finiteOutput (flag : ℕ → Bool) (N : ℕ) (bits : Fin N → Bool) : Cantor :=
  fun n => if hn : n < N then (if flag n then bits ⟨n,hn⟩ else false) else false

theorem eventually_false_finite_carrier (flag : ℕ → Bool) (N : ℕ)
    (hN : ∀ n, N ≤ n → flag n = false) :
    ∃ C : Set Cantor, C.Finite ∧ law flag Cᶜ = 0 := by
  let C := Set.range (finiteOutput flag N)
  have hC : C.Finite := Set.finite_range _
  refine ⟨C, hC, ?_⟩
  rw [law, Measure.map_apply (switched_measurable flag) hC.measurableSet.compl]
  have he : switched flag ⁻¹' Cᶜ = ∅ := by
    apply Set.eq_empty_iff_forall_not_mem.mpr
    intro x hx
    apply hx
    refine ⟨fun i : Fin N => x i.val, ?_⟩
    funext n
    by_cases hn : n < N
    · simp [finiteOutput, switched, hn]
    · simp [finiteOutput, switched, hn, hN n (by omega)]
  rw [he, measure_empty]

theorem eventually_false_defect_zero (flag : ℕ → Bool) (N : ℕ)
    (hN : ∀ n, N ≤ n → flag n = false) : defect (law flag) = 0 := by
  obtain ⟨C, hC, hfull⟩ := eventually_false_finite_carrier flag N hN
  have hm : mass (law flag) = 1 := countable_carrier_mass_one (law flag)
    hC.countable hfull (measure_univ)
  simp [defect, hm]

theorem finite_copied_iff_eventually_false (flag : ℕ → Bool) :
    (copied flag).Finite ↔ ∃ N, ∀ n, N ≤ n → flag n = false := by
  constructor
  · intro h
    obtain ⟨b, hb⟩ := h.bddAbove
    refine ⟨b+1, ?_⟩
    intro n hn
    cases hf : flag n
    · rfl
    · have hnb := hb (show n ∈ copied flag from hf)
      omega
  · rintro ⟨N, hN⟩
    apply (Set.finite_Iio N).subset
    intro n hn
    change flag n = true at hn
    change n < N
    by_contra h
    have hz := hN n (by omega)
    simp_all

theorem finite_copied_defect_zero (flag : ℕ → Bool) (h : (copied flag).Finite) :
    defect (law flag) = 0 := by
  obtain ⟨N,hN⟩ := (finite_copied_iff_eventually_false flag).mp h
  exact eventually_false_defect_zero flag N hN

theorem defect_zero_iff_finite_copied (flag : ℕ → Bool) :
    defect (law flag) = 0 ↔ (copied flag).Finite := by
  constructor
  · intro hz
    by_contra h
    have ho := infinite_copied_defect_one flag h
    linarith
  · exact finite_copied_defect_zero flag

theorem defect_one_iff_infinite_copied (flag : ℕ → Bool) :
    defect (law flag) = 1 ↔ (copied flag).Infinite := by
  constructor
  · intro ho hfin
    have hz := finite_copied_defect_zero flag hfin
    linarith
  · exact infinite_copied_defect_one flag

end P02A2.InnovationMeasure
