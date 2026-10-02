import Mathlib

open MeasureTheory Filter Set
open scoped ENNReal

namespace Orthemology.Tranche2.RecurrentSupport

variable {A : Type*} [Fintype A]

def Recurs (x : ℕ → A) (a : A) : Prop := ∃ᶠ n in atTop, x n = a

noncomputable def recurrentSet (x : ℕ → A) : Finset A := by
  classical
  exact Finset.univ.filter (Recurs x)

@[simp] lemma mem_recurrentSet (x : ℕ → A) (a : A) :
    a ∈ recurrentSet x ↔ Recurs x a := by
  classical
  simp [recurrentSet]

theorem exists_recurrent (x : ℕ → A) : ∃ a, Recurs x a := by
  by_contra hn
  push_neg at hn
  have he : ∀ a, ∀ᶠ n in atTop, x n ≠ a := fun a => not_frequently.mp (hn a)
  obtain ⟨n, hn⟩ := (eventually_all.mpr he).exists
  exact hn (x n) rfl

theorem recurrentSet_nonempty (x : ℕ → A) : (recurrentSet x).Nonempty := by
  obtain ⟨a, ha⟩ := exists_recurrent x
  exact ⟨a, (mem_recurrentSet x a).mpr ha⟩

/-- Finite actions make every nonrecurrent action disappear after one common
finite time. No stopping-time assertion is involved. -/
theorem eventually_mem_recurrentSet (x : ℕ → A) :
    ∀ᶠ n in atTop, x n ∈ recurrentSet x := by
  classical
  have he : ∀ a, ∀ᶠ n in atTop, x n = a → Recurs x a := by
    intro a
    by_cases h : Recurs x a
    · exact Eventually.of_forall (fun _ _ => h)
    · exact (not_frequently.mp h).mono (fun _ hn hEq => (hn hEq).elim)
  exact (eventually_all.mpr he).mono (fun n hn =>
    (mem_recurrentSet x (x n)).mpr (hn (x n) rfl))

theorem recurrentSet_subset_of_eventually_mem (x : ℕ → A) (G : Finset A)
    (hG : ∀ᶠ n in atTop, x n ∈ G) : recurrentSet x ⊆ G := by
  intro a ha
  obtain ⟨n, hn, hg⟩ := ((mem_recurrentSet x a).mp ha |>.and_eventually hG).exists
  simpa [hn] using hg

variable {Ω : Type*} [MeasurableSpace Ω]

def exactRecurrentEvent (X : Ω → ℕ → A) (U : Finset A) : Set Ω :=
  {ω | recurrentSet (X ω) = U}

def tailEvent (X : Ω → ℕ → A) (U : Finset A) (N : ℕ) : Set Ω :=
  exactRecurrentEvent X U ∩ {ω | ∀ n, N ≤ n → X ω n ∈ U}

omit [MeasurableSpace Ω] in
theorem exact_event_eventually_mem (X : Ω → ℕ → A) (U : Finset A)
    {ω : Ω} (hω : ω ∈ exactRecurrentEvent X U) :
    ∀ᶠ n in atTop, X ω n ∈ U := by
  have he := eventually_mem_recurrentSet (X ω)
  exact hω ▸ he

omit [MeasurableSpace Ω] in
theorem exact_event_finitely_many_outside (X : Ω → ℕ → A) (U : Finset A)
    {ω : Ω} (hω : ω ∈ exactRecurrentEvent X U) :
    {n : ℕ | X ω n ∉ U}.Finite := by
  obtain ⟨N, hN⟩ := eventually_atTop.mp (exact_event_eventually_mem X U hω)
  apply (Set.finite_Iio N).subset
  intro n hn
  exact lt_of_not_ge (fun hge => hn (hN n hge))

theorem exact_event_eq_iUnion_tail (X : Ω → ℕ → A) (U : Finset A) :
    exactRecurrentEvent X U = ⋃ N, tailEvent X U N := by
  ext ω
  constructor
  · intro hω
    obtain ⟨N, hN⟩ := eventually_atTop.mp (exact_event_eventually_mem X U hω)
    exact mem_iUnion.mpr ⟨N, hω, hN⟩
  · intro hω
    obtain ⟨N, hN⟩ := mem_iUnion.mp hω
    exact hN.1

section Measurability
variable [MeasurableSpace A] [MeasurableSingletonClass A]

omit [Fintype A] in
theorem measurable_recurrence (X : Ω → ℕ → A)
    (hX : ∀ n, Measurable (fun ω => X ω n)) (a : A) :
    MeasurableSet {ω | Recurs (X ω) a} := by
  simp only [Recurs, frequently_atTop, setOf_forall, setOf_exists]
  apply MeasurableSet.iInter
  intro N
  apply MeasurableSet.iUnion
  intro n
  by_cases h : N ≤ n
  · convert (measurableSet_singleton a).preimage (hX n) using 1
    ext ω
    simp [h]
  · convert MeasurableSet.empty (α := Ω) using 1
    ext ω
    simp [h]

theorem measurable_exactRecurrentEvent (X : Ω → ℕ → A)
    (hX : ∀ n, Measurable (fun ω => X ω n)) (U : Finset A) :
    MeasurableSet (exactRecurrentEvent X U) := by
  simp only [exactRecurrentEvent, Finset.ext_iff, mem_recurrentSet, setOf_forall]
  apply MeasurableSet.iInter
  intro a
  by_cases h : a ∈ U
  · convert measurable_recurrence X hX a using 1
    ext ω
    simp [h]
  · convert (measurable_recurrence X hX a).compl using 1
    ext ω
    simp [h]

theorem measurable_tailEvent (X : Ω → ℕ → A)
    (hX : ∀ n, Measurable (fun ω => X ω n)) (U : Finset A) (N : ℕ) :
    MeasurableSet (tailEvent X U N) := by
  apply (measurable_exactRecurrentEvent X hX U).inter
  simp only [setOf_forall]
  apply MeasurableSet.iInter
  intro n
  by_cases h : N ≤ n
  · convert U.measurableSet.preimage (hX n) using 1
    ext ω
    simp [h]
  · convert MeasurableSet.univ (α := Ω) using 1
    ext ω
    simp [h]

end Measurability

/-- A finite partition by exact recurrent supports has a positive cell. Almost
sure eventual goodness puts that cell's support inside the supplied target. -/
theorem exists_positive_recurrent_support
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : Ω → ℕ → A) (G : Finset A)
    (hgood : ∀ᵐ ω ∂μ, ∀ᶠ n in atTop, X ω n ∈ G) :
    ∃ U : Finset A, U.Nonempty ∧ U ⊆ G ∧ 0 < μ (exactRecurrentEvent X U) := by
  classical
  have hcover : (⋃ U : Finset A, exactRecurrentEvent X U) = univ := by
    ext ω
    simp [exactRecurrentEvent]
  have hpos : μ (⋃ U : Finset A, exactRecurrentEvent X U) ≠ 0 := by
    rw [hcover]
    simp
  obtain ⟨U, hU⟩ := exists_measure_pos_of_not_measure_iUnion_null hpos
  obtain ⟨ω, hω, hg⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hU.ne'
    (ae_restrict_of_ae hgood)
  have heq : recurrentSet (X ω) = U := hω
  refine ⟨U, ?_, ?_, hU⟩
  · rw [← heq]
    exact recurrentSet_nonempty (X ω)
  · rw [← heq]
    exact recurrentSet_subset_of_eventually_mem (X ω) G hg

theorem exists_positive_tail_index (μ : Measure Ω) (X : Ω → ℕ → A)
    (U : Finset A) (hU : 0 < μ (exactRecurrentEvent X U)) :
    ∃ N, 0 < μ (tailEvent X U N) := by
  apply exists_measure_pos_of_not_measure_iUnion_null
  rw [← exact_event_eq_iUnion_tail]
  exact hU.ne'

theorem exists_measurable_positive_recurrent_support
    [MeasurableSpace A] [MeasurableSingletonClass A]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : Ω → ℕ → A) (hX : ∀ n, Measurable (fun ω => X ω n))
    (G : Finset A) (hgood : ∀ᵐ ω ∂μ, ∀ᶠ n in atTop, X ω n ∈ G) :
    ∃ U : Finset A, U.Nonempty ∧ U ⊆ G ∧
      MeasurableSet (exactRecurrentEvent X U) ∧
      0 < μ (exactRecurrentEvent X U) ∧
      ∀ ω ∈ exactRecurrentEvent X U, {n : ℕ | X ω n ∉ U}.Finite := by
  obtain ⟨U, hne, hsub, hpos⟩ := exists_positive_recurrent_support μ X G hgood
  exact ⟨U, hne, hsub, measurable_exactRecurrentEvent X hX U, hpos,
    fun _ hω => exact_event_finitely_many_outside X U hω⟩

theorem support_subset_of_positive_exact_event
    (μ : Measure Ω) (X : Ω → ℕ → A) (G U : Finset A)
    (hgood : ∀ᵐ ω ∂μ, ∀ᶠ n in atTop, X ω n ∈ G)
    (hU : 0 < μ (exactRecurrentEvent X U)) : U ⊆ G := by
  obtain ⟨ω, hω, hg⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hU.ne'
    (ae_restrict_of_ae hgood)
  have heq : recurrentSet (X ω) = U := hω
  rw [← heq]
  exact recurrentSet_subset_of_eventually_mem (X ω) G hg

/-- Abstract necessity only: the pairwise tail-event transfer is an explicit
hypothesis, not a claimed consequence of an unformalized policy embedding. -/
theorem abstract_self_verifying_support
    {Θ : Type*} (μ : Θ → Measure Ω) [∀ θ, IsProbabilityMeasure (μ θ)]
    (X : Ω → ℕ → A) (G : Θ → Finset A)
    (Agree : Θ → Θ → Finset A → Prop)
    (hgood : ∀ θ, ∀ᵐ ω ∂μ θ, ∀ᶠ n in atTop, X ω n ∈ G θ)
    (htransfer : ∀ θ η U N, Agree θ η U →
      0 < μ θ (tailEvent X U N) → 0 < μ η (tailEvent X U N))
    (θ : Θ) :
    ∃ U : Finset A, U.Nonempty ∧ U ⊆ G θ ∧
      ∀ η, Agree θ η U → U ⊆ G η := by
  obtain ⟨U, hne, hsub, hpos⟩ := exists_positive_recurrent_support (μ θ) X (G θ) (hgood θ)
  obtain ⟨N, hN⟩ := exists_positive_tail_index (μ θ) X U hpos
  refine ⟨U, hne, hsub, fun η hη => ?_⟩
  have hposη := htransfer θ η U N hη hN
  have hexact : 0 < μ η (exactRecurrentEvent X U) :=
    lt_of_lt_of_le hposη (measure_mono inter_subset_left)
  exact support_subset_of_positive_exact_event (μ η) X (G η) U (hgood η) hexact

end Orthemology.Tranche2.RecurrentSupport

#print axioms Orthemology.Tranche2.RecurrentSupport.measurable_recurrence
#print axioms Orthemology.Tranche2.RecurrentSupport.measurable_exactRecurrentEvent
#print axioms Orthemology.Tranche2.RecurrentSupport.measurable_tailEvent
#print axioms Orthemology.Tranche2.RecurrentSupport.eventually_mem_recurrentSet
#print axioms Orthemology.Tranche2.RecurrentSupport.exact_event_finitely_many_outside
#print axioms Orthemology.Tranche2.RecurrentSupport.exists_positive_recurrent_support
#print axioms Orthemology.Tranche2.RecurrentSupport.exists_positive_tail_index
#print axioms Orthemology.Tranche2.RecurrentSupport.exists_measurable_positive_recurrent_support
#print axioms Orthemology.Tranche2.RecurrentSupport.abstract_self_verifying_support
#check Orthemology.Tranche2.RecurrentSupport.exists_positive_recurrent_support
#check Orthemology.Tranche2.RecurrentSupport.exists_measurable_positive_recurrent_support
#check Orthemology.Tranche2.RecurrentSupport.abstract_self_verifying_support
