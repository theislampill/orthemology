import CountableHistoryTower

noncomputable section
open MeasureTheory
open scoped ENNReal BigOperators Function
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation

variable {Ω ι : Type*} [MeasurableSpace Ω]

/-- Multiply a genuine positive-prefix conditional probability bound back by
the original prefix probability. Null prefixes cost zero, not a conditional
assumption about an arbitrarily assigned null-history law. -/
theorem measure_inter_le_of_normalizedRestriction [Countable ι]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (E F : Set Ω) (hE : MeasurableSet E)
    (r : ℝ≥0∞)
    (hb : 0<μ E → normalizedRestriction μ E F≤r) :
    μ (E∩F)≤μ E*r := by
  by_cases hz : μ E=0
  · have hm : μ (E∩F)≤μ E := measure_mono Set.inter_subset_left
    rw [hz] at hm
    simpa only [hz,zero_mul] using hm
  · have hpos : 0<μ E := pos_iff_ne_zero.mpr hz
    have h := mul_le_mul_left' (hb hpos) (μ E)
    unfold normalizedRestriction at h
    rw [Measure.smul_apply,Measure.restrict_apply' hE] at h
    simp only [smul_eq_mul,← mul_assoc,ENNReal.mul_inv_cancel hz (measure_ne_top μ E),one_mul] at h
    simpa only [Set.inter_comm] using h

/-- A countable prefix-free stopping-history family contributes at most one
copy of its uniform conditional tail, regardless of how late it starts. -/
theorem disjoint_history_union_bound [Countable ι]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (E F : ι → Set Ω)
    (hE : ∀ i, MeasurableSet (E i)) (hd : Pairwise (Disjoint on E))
    (r : ℝ≥0∞) (hb : ∀ i, μ (E i∩F i)≤μ (E i)*r) :
    μ (⋃ i,E i∩F i)≤r := by
  calc
    μ (⋃ i,E i∩F i)≤∑' i,μ (E i∩F i) := measure_iUnion_le _
    _ ≤∑' i,μ (E i)*r := ENNReal.tsum_le_tsum hb
    _ =(∑' i,μ (E i))*r := ENNReal.tsum_mul_right
    _ ≤1*r := mul_le_mul_right' (by rw [← measure_iUnion hd hE];exact (measure_mono (Set.subset_univ _)).trans_eq (measure_univ)) r
    _ =r := one_mul r

universe u v
variable {R : Type v} {A Y : Type u}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- Equality of the complete actual stack-history law with the same canonical
law used by positive-prefix continuation, not merely equality of actions. -/
theorem stack_history_law_eq_canonical
    (π : R → History A Y → A) (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y,0≤P a y) (hN : ∀ a,∑ y,P a y=1) :
    (ρ.prod (stackMeasure P hP hN)).map (stackHistoryTrajectory π)=
      observedTraceLaw ∅ π ρ P P hP hN hP hN := by
  rw [← observedTraceLaw_univ_eq_stack π hπ ρ P hP hN]
  exact observedTraceLaw_eq_all_query Finset.univ π hπ ρ P P hP hN hP hN (fun _ _ => rfl)

/-- Restricting the actual stack experiment on a full history and reading its
future gives the already-constructed genuine conditional continuation law. -/
theorem stack_conditional_continuation_eq
    (π : R → History A Y → A) (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y,0≤P a y) (hN : ∀ a,∑ y,P a y=1)
    (h : History A Y) :
    (normalizedRestriction (ρ.prod (stackMeasure P hP hN))
      {z | stackHistoryTrajectory π z h.length=h}).map
      (fun z => continuationReadout h (stackHistoryTrajectory π z))=
      conditionalContinuationLaw π ρ P hP hN h := by
  have hC : MeasurableSet {H : ℕ → History A Y | H h.length=h} :=
    (measurableSet_singleton h).preimage (measurable_pi_apply h.length)
  have hm := normalizedRestriction_map_preimage (ρ.prod (stackMeasure P hP hN))
    (stackHistoryTrajectory π) (stackHistoryTrajectory_measurable π hπ)
    {H | H h.length=h} hC
  rw [stack_history_law_eq_canonical π hπ ρ P hP hN] at hm
  rw [conditionalContinuationLaw_eq_conditioned_observation π hπ ρ P hP hN h,← hm,
    Measure.map_map (continuationReadout_measurable h) (stackHistoryTrajectory_measurable π hπ)]
  rfl

/-- The prefix probability in the stack representation is the actual canonical
prefix probability required by the conditional generated-slice theorem. -/
theorem stack_prefix_probability_eq
    (π : R → History A Y → A) (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y,0≤P a y) (hN : ∀ a,∑ y,P a y=1)
    (h : History A Y) :
    (ρ.prod (stackMeasure P hP hN)) {z | stackHistoryTrajectory π z h.length=h}=
      CanonicalInput ρ P hP hN (PrefixEvent π h) := by
  have hC : MeasurableSet {H : ℕ → History A Y | H h.length=h} :=
    (measurableSet_singleton h).preimage (measurable_pi_apply h.length)
  have hm := congrArg (fun μ : Measure (ℕ → History A Y) => μ {H | H h.length=h})
    (stack_history_law_eq_canonical π hπ ρ P hP hN)
  dsimp only at hm
  rw [Measure.map_apply (stackHistoryTrajectory_measurable π hπ) hC] at hm
  unfold observedTraceLaw at hm
  rw [Measure.map_apply (historyTrajectory_measurable ∅ π hπ) hC] at hm
  exact hm

end HiddenParity.Cost
