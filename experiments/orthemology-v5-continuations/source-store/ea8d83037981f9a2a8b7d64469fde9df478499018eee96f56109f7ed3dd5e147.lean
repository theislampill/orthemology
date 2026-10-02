import EffectiveAtoms

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory Filter
open scoped ENNReal Topology BigOperators

variable {S : Type*} [Fintype S] [DecidableEq S]

def atomSet (M : Mealy S) (s : S) (n : ℕ) : Set Cantor :=
  match enumerateAtoms M s n with
  | none => ∅
  | some (u, _) => {atomCandidate M s u}

def atomWeightQ (M : Mealy S) (s : S) (n : ℕ) : ℚ :=
  match enumerateAtoms M s n with
  | none => 0
  | some (_, r) => r

noncomputable def atomPointMeasure (M : Mealy S) (s : S) (n : ℕ) : Measure Cantor :=
  match enumerateAtoms M s n with
  | none => 0
  | some (u,r) => ENNReal.ofReal (r : ℝ) • Measure.dirac (atomCandidate M s u)

theorem measurableSet_atomSet (M : Mealy S) (s : S) (n : ℕ) : MeasurableSet (atomSet M s n) := by
  cases h : enumerateAtoms M s n with
  | none => simp [atomSet, h]
  | some p => simp [atomSet, h]

theorem atomSet_subset_positive (M : Mealy S) (s : S) (n : ℕ) :
    atomSet M s n ⊆ P02A2.positive (law M s) := by
  intro y hy
  cases h : enumerateAtoms M s n with
  | none => simp [atomSet, h] at hy
  | some p =>
    rcases p with ⟨u,r⟩
    have he : y = atomCandidate M s u := by simpa [atomSet, h] using hy
    rw [he]
    exact (enumerateAtoms_sound M s n u r h).1

theorem atomSet_disjoint (M : Mealy S) (s : S) : Pairwise (Function.onFun Disjoint (atomSet M s)) := by
  intro n m hnm
  change Disjoint (atomSet M s n) (atomSet M s m)
  cases hn : enumerateAtoms M s n with
  | none => simp [atomSet, hn]
  | some p =>
    cases hm : enumerateAtoms M s m with
    | none => simp [atomSet, hm]
    | some q =>
      rcases p with ⟨u,r⟩
      rcases q with ⟨v,z⟩
      simpa only [atomSet, hn, hm, disjoint_singleton] using
        enumerateAtoms_no_duplicates M s n m u v r z hn hm hnm

theorem iUnion_atomSet [Nonempty S] (M : Mealy S) (s : S) :
    (⋃ n, atomSet M s n) = P02A2.positive (law M s) := by
  apply subset_antisymm
  · exact iUnion_subset (atomSet_subset_positive M s)
  · intro y hy
    obtain ⟨n,u,r,hn,he⟩ := enumerateAtoms_complete M s y hy
    apply mem_iUnion.mpr
    exact ⟨n, by simp [atomSet, hn, he]⟩

theorem atomWeightQ_correct (M : Mealy S) (s : S) (n : ℕ) :
    (atomWeightQ M s n : ℝ) = (law M s (atomSet M s n)).toReal := by
  cases h : enumerateAtoms M s n with
  | none => simp [atomWeightQ, atomSet, h]
  | some p =>
    rcases p with ⟨u,r⟩
    simpa only [atomWeightQ, atomSet, h] using (enumerateAtoms_sound M s n u r h).2

theorem atomWeightQ_nonneg (M : Mealy S) (s : S) (n : ℕ) : 0 ≤ atomWeightQ M s n := by
  have h : (0 : ℝ) ≤ (atomWeightQ M s n : ℝ) := by
    rw [atomWeightQ_correct]
    exact ENNReal.toReal_nonneg
  exact_mod_cast h

theorem atomWeight_measure (M : Mealy S) (s : S) (n : ℕ) :
    ENNReal.ofReal (atomWeightQ M s n : ℝ) = law M s (atomSet M s n) := by
  rw [atomWeightQ_correct, ENNReal.ofReal_toReal (measure_ne_top _ _)]

theorem atomPointMeasure_eq_restrict (M : Mealy S) (s : S) (n : ℕ) :
    atomPointMeasure M s n = (law M s).restrict (atomSet M s n) := by
  cases h : enumerateAtoms M s n with
  | none => simp [atomPointMeasure, atomSet, h]
  | some p =>
    rcases p with ⟨u,r⟩
    simp only [atomPointMeasure, atomSet, h, Measure.restrict_singleton]
    rw [(enumerateAtoms_sound M s n u r h).2, ENNReal.ofReal_toReal (measure_ne_top _ _)]

/-- Actual point-atomic measure reconstruction, not merely an enumeration of its support. -/
theorem atomic_measure_reconstruction [Nonempty S] (M : Mealy S) (s : S) :
    (law M s).restrict (P02A2.positive (law M s)) = Measure.sum (atomPointMeasure M s) := by
  rw [← iUnion_atomSet M s, Measure.restrict_iUnion (atomSet_disjoint M s) (measurableSet_atomSet M s)]
  congr 1
  funext n
  exact (atomPointMeasure_eq_restrict M s n).symm

/-- The exact singleton weights sum to the full atomic mass. Skipped indices contribute zero. -/
theorem atomic_mass_eq_tsum_weights [Nonempty S] (M : Mealy S) (s : S) :
    P02A2.mass (law M s) = ∑' n, ENNReal.ofReal (atomWeightQ M s n : ℝ) := by
  unfold P02A2.mass
  rw [← iUnion_atomSet M s, measure_iUnion (atomSet_disjoint M s) (measurableSet_atomSet M s)]
  congr 1
  funext n
  exact (atomWeight_measure M s n).symm

def partialMassQ (M : Mealy S) (s : S) (N : ℕ) : ℚ :=
  ∑ n ∈ Finset.range N, atomWeightQ M s n

def partialAtomSet (M : Mealy S) (s : S) (N : ℕ) : Set Cantor :=
  ⋃ n ∈ Finset.range N, atomSet M s n

theorem measurableSet_partialAtomSet (M : Mealy S) (s : S) (N : ℕ) :
    MeasurableSet (partialAtomSet M s N) := by
  exact MeasurableSet.iUnion (fun n => MeasurableSet.iUnion (fun _ => measurableSet_atomSet M s n))

theorem partialAtomSet_subset_positive (M : Mealy S) (s : S) (N : ℕ) :
    partialAtomSet M s N ⊆ P02A2.positive (law M s) := by
  exact iUnion_subset (fun n => iUnion_subset (fun _ => atomSet_subset_positive M s n))

theorem measure_partialAtomSet (M : Mealy S) (s : S) (N : ℕ) :
    law M s (partialAtomSet M s N) = ∑ n ∈ Finset.range N, law M s (atomSet M s n) := by
  apply measure_biUnion_finset
  · intro n hn m hm hnm
    exact atomSet_disjoint M s hnm
  · intro n hn
    exact measurableSet_atomSet M s n

theorem partialMassQ_correct (M : Mealy S) (s : S) (N : ℕ) :
    (partialMassQ M s N : ℝ) = (law M s (partialAtomSet M s N)).toReal := by
  rw [measure_partialAtomSet, ENNReal.toReal_sum (fun _ _ => measure_ne_top _ _)]
  simp [partialMassQ, atomWeightQ_correct]

/-- Exact computable rational mass not yet listed after N enumeration indices. -/
def residualMassQ (M : Mealy S) (s : S) (N : ℕ) : ℚ := solveHitting M s - partialMassQ M s N

theorem residualMassQ_correct [Nonempty S] (M : Mealy S) (s : S) (N : ℕ) :
    (residualMassQ M s N : ℝ) =
      (law M s (P02A2.positive (law M s) \ partialAtomSet M s N)).toReal := by
  have he := measure_inter_add_diff (μ := law M s) (P02A2.positive (law M s))
    (measurableSet_partialAtomSet M s N)
  rw [inter_eq_right.mpr (partialAtomSet_subset_positive M s N)] at he
  have hr := congrArg ENNReal.toReal he
  rw [ENNReal.toReal_add (measure_ne_top _ _) (measure_ne_top _ _)] at hr
  rw [← partialMassQ_correct] at hr
  change ↑(partialMassQ M s N) + _ = (P02A2.mass (law M s)).toReal at hr
  simp only [residualMassQ, Rat.cast_sub, solveHitting_correct]
  rw [hittingReal, ← atomic_mass_eq_hitting_probability]
  linarith


theorem residualMassQ_nonneg [Nonempty S] (M : Mealy S) (s : S) (N : ℕ) :
    0 ≤ residualMassQ M s N := by
  have h : (0 : ℝ) ≤ (residualMassQ M s N : ℝ) := by
    rw [residualMassQ_correct]
    exact ENNReal.toReal_nonneg
  exact_mod_cast h


noncomputable def partialPointMeasure (M : Mealy S) (s : S) (N : ℕ) : Measure Cantor :=
  ∑ n ∈ Finset.range N, atomPointMeasure M s n

theorem partialAtomSet_succ (M : Mealy S) (s : S) (N : ℕ) :
    partialAtomSet M s (N+1) = partialAtomSet M s N ∪ atomSet M s N := by
  ext x
  simp [partialAtomSet, Finset.range_succ, or_comm]

theorem partialAtomSet_disjoint_next (M : Mealy S) (s : S) (N : ℕ) :
    Disjoint (partialAtomSet M s N) (atomSet M s N) := by
  apply Set.disjoint_left.mpr
  intro x hx hy
  obtain ⟨n,hn⟩ := mem_iUnion.mp hx
  obtain ⟨hn,hx⟩ := mem_iUnion.mp hn
  exact Set.disjoint_left.mp (atomSet_disjoint M s (ne_of_lt (Finset.mem_range.mp hn))) hx hy

/-- Finite point-mass sums equal restriction to the finite set already enumerated. -/
theorem partialPointMeasure_eq_restrict (M : Mealy S) (s : S) (N : ℕ) :
    partialPointMeasure M s N = (law M s).restrict (partialAtomSet M s N) := by
  induction N with
  | zero => simp [partialPointMeasure, partialAtomSet]
  | succ N ih =>
    rw [partialAtomSet_succ, Measure.restrict_union (partialAtomSet_disjoint_next M s N)
      (measurableSet_atomSet M s N), ← ih, ← atomPointMeasure_eq_restrict]
    simp only [partialPointMeasure, Finset.sum_range_succ]

/-- Exact finite approximation plus the remaining atomic restriction, as measures. -/
theorem finite_atomic_measure_decomposition [Nonempty S] (M : Mealy S) (s : S) (N : ℕ) :
    (law M s).restrict (P02A2.positive (law M s)) = partialPointMeasure M s N +
      (law M s).restrict (P02A2.positive (law M s) \ partialAtomSet M s N) := by
  have he := Set.union_diff_cancel (partialAtomSet_subset_positive M s N)
  calc
    (law M s).restrict (P02A2.positive (law M s)) = (law M s).restrict
        (partialAtomSet M s N ∪ (P02A2.positive (law M s) \ partialAtomSet M s N)) :=
      congrArg (law M s).restrict he.symm
    _ = (law M s).restrict (partialAtomSet M s N) +
        (law M s).restrict (P02A2.positive (law M s) \ partialAtomSet M s N) :=
      Measure.restrict_union Set.disjoint_sdiff_right
        ((P02A2.positive_measurable _).diff (measurableSet_partialAtomSet M s N))
    _ = _ := by rw [← partialPointMeasure_eq_restrict]

end Orthemology.Frontier.MealyMeasure
