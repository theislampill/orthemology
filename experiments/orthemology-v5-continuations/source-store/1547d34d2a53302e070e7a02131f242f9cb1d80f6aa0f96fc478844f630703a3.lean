import ConditionalPrefix

noncomputable section
open MeasureTheory ProbabilityTheory Set Finset Preorder
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.ResidualSeed.Continuation
universe u v
variable {R : Type v} {A Y : Type u}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- The actually observed post-prefix history, with the fixed old prefix removed.
This is a function of the original experiment, not a separately restarted run. -/
def continuationHistory (π : R → History A Y → A) (h : History A Y)
    (z : Input R A Y) (n : ℕ) : History A Y :=
  (historyTrajectory ∅ π z (h.length+n)).take n

theorem continuationHistory_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (h : History A Y) :
    Measurable (continuationHistory π h) := by
  apply measurable_pi_lambda
  intro n
  exact (measurable_of_countable (fun xs : History A Y => xs.take n)).comp
    (historyTrajectory_coordinate_measurable ∅ π hπ (h.length+n))

omit [Fintype A] [Fintype Y] [Inhabited Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem continuationHistory_length (π : R → History A Y → A) (h : History A Y)
    (z : Input R A Y) (n : ℕ) : (continuationHistory π h z n).length = n := by
  simp only [continuationHistory, historyTrajectory, List.length_take, observedHistory_length]
  exact Nat.min_eq_left (by omega)

omit [Fintype A] [Fintype Y] [Inhabited Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- Every acquired continuation history reconstructs its older continuation
prefixes, without any condition on the latent input. -/
theorem continuationHistory_drop (π : R → History A Y → A) (h : History A Y)
    (z : Input R A Y) (n m : ℕ) (hm : m ≤ n) :
    (continuationHistory π h z n).drop (n-m) = continuationHistory π h z m := by
  have hd := observedHistory_drop ∅ π z.2.2 z.1 (fun a k => z.2.1 (a,k))
    (h.length+n) (h.length+m) (by omega)
  change (historyTrajectory ∅ π z (h.length+n)).drop
      ((h.length+n)-(h.length+m)) = historyTrajectory ∅ π z (h.length+m) at hd
  have hsub : (h.length+n)-(h.length+m) = n-m := by omega
  rw [hsub] at hd
  simp only [continuationHistory, List.drop_take]
  rw [hd, Nat.sub_sub_self hm]

omit [Fintype A] [Fintype Y] [Inhabited Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- On the conditioning event, the new continuation and the old prefix recover
the full actual acquired history. -/
theorem actual_history_eq_continuation_append
    (π : R → History A Y → A) (h : History A Y) (z : Input R A Y)
    (hz : z ∈ PrefixEvent π h) (n : ℕ) :
    historyTrajectory ∅ π z (h.length+n) = continuationHistory π h z n ++ h := by
  have hd := observedHistory_drop ∅ π z.2.2 z.1 (fun a k => z.2.1 (a,k))
    (h.length+n) h.length (by omega)
  change (historyTrajectory ∅ π z (h.length+n)).drop
      ((h.length+n)-h.length) = historyTrajectory ∅ π z h.length at hd
  have hsub : (h.length+n)-h.length = n := by omega
  rw [hsub] at hd
  change historyTrajectory ∅ π z h.length = h at hz
  rw [hz] at hd
  have ht := List.take_append_drop n (historyTrajectory ∅ π z (h.length+n))
  rw [hd] at ht
  exact ht.symm

omit [Fintype A] [Fintype Y] [Inhabited Y] [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- Exact finite continuation event on the conditioning domain. -/
theorem continuation_event_inter_prefix
    (π : R → History A Y → A) (h tail : History A Y) :
    {z | continuationHistory π h z tail.length = tail} ∩ PrefixEvent π h =
      PrefixEvent π (tail ++ h) := by
  ext z
  constructor
  · rintro ⟨ht, hh⟩
    have he := actual_history_eq_continuation_append π h z hh tail.length
    rw [ht] at he
    change historyTrajectory ∅ π z (tail ++ h).length = tail ++ h
    simpa only [List.length_append, Nat.add_comm] using he
  · intro hz
    have hh := prefixEvent_append_subset π tail h hz
    refine ⟨?_, hh⟩
    change historyTrajectory ∅ π z (tail ++ h).length = tail ++ h at hz
    change (historyTrajectory ∅ π z (h.length+tail.length)).take tail.length = tail
    have he : h.length+tail.length = (tail ++ h).length := by simp [Nat.add_comm]
    rw [he, hz]
    exact List.take_left

def conditionalContinuationLaw (π : R → History A Y → A) (ρ : Measure R)
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) : Measure (ℕ → History A Y) :=
  (normalizedRestriction (CanonicalInput ρ P hP hN) (PrefixEvent π h)).map
    (continuationHistory π h)

/-- The finite marginal is derived from the actual conditioned original input. -/
theorem conditional_continuation_marginal
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hpos : 0 < CanonicalInput ρ P hP hN (PrefixEvent π h))
    (n : ℕ) (tail : History A Y) :
    ((conditionalContinuationLaw π ρ P hP hN h).map (fun H => H n)) {tail} =
      if n = tail.length then
        commonSeedPosterior π ρ h (CompatibleSeeds (restartPolicy π h) tail) *
          RowLikelihood P tail
      else 0 := by
  rw [conditionalContinuationLaw,
    Measure.map_map (measurable_pi_apply n) (continuationHistory_measurable π hπ h),
    Measure.map_apply ((measurable_pi_apply n).comp (continuationHistory_measurable π hπ h))
      (measurableSet_singleton tail)]
  by_cases hn : n = tail.length
  · subst n
    rw [if_pos rfl]
    have he : normalizedRestriction (CanonicalInput ρ P hP hN) (PrefixEvent π h)
        {z | continuationHistory π h z tail.length = tail} =
        normalizedRestriction (CanonicalInput ρ P hP hN) (PrefixEvent π h)
          (PrefixEvent π (tail ++ h)) := by
      unfold normalizedRestriction
      rw [Measure.smul_apply, Measure.smul_apply,
        Measure.restrict_apply' (prefixEvent_measurable π hπ h),
        Measure.restrict_apply' (prefixEvent_measurable π hπ h),
        continuation_event_inter_prefix,
        Set.inter_eq_left.mpr (prefixEvent_append_subset π tail h)]
    change normalizedRestriction (CanonicalInput ρ P hP hN) (PrefixEvent π h)
        {z | continuationHistory π h z tail.length = tail} = _
    rw [he]
    exact conditional_extension_probability π hπ ρ P hP hN h tail hpos
  · rw [if_neg hn]
    have he : {z : Input R A Y | continuationHistory π h z n = tail} = ∅ := by
      apply Set.eq_empty_iff_forall_not_mem.mpr
      intro z hz
      have hh := congrArg List.length hz
      exact hn ((continuationHistory_length π h z n).symm.trans hh)
    change normalizedRestriction (CanonicalInput ρ P hP hN) (PrefixEvent π h)
      {z | continuationHistory π h z n = tail} = 0
    rw [he, measure_empty]

/-- Every finite continuation-history law is the genuine restarted canonical
law, with the derived common posterior seed. -/
theorem conditional_continuation_marginal_eq_restart
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hpos : 0 < CanonicalInput ρ P hP hN (PrefixEvent π h)) (n : ℕ) :
    (conditionalContinuationLaw π ρ P hP hN h).map (fun H => H n) =
      (observedTraceLaw ∅ (restartPolicy π h) (commonSeedPosterior π ρ h)
        P P hP hN hP hN).map (fun H => H n) := by
  haveI := commonSeedPosterior_probability π ρ h
    (positive_prefix_compatible_seeds π ρ P hP hN h hpos)
  apply Measure.ext_of_singleton
  intro tail
  rw [conditional_continuation_marginal π hπ ρ P hP hN h hpos]
  unfold observedTraceLaw
  rw [Measure.map_map (measurable_pi_apply n)
    (historyTrajectory_measurable ∅ (restartPolicy π h) (restartPolicy_measurable π hπ h))]
  exact (history_marginal_formula ∅ (restartPolicy π h) (restartPolicy_measurable π hπ h)
    (commonSeedPosterior π ρ h) P P hP hN hP hN (fun _ _ => rfl) n tail).symm

/-- Complete continuation prefixes are reconstructible from their last acquired
history under the actual conditional continuation law. -/
theorem conditional_prefix_map_from_last
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) (N : ℕ) :
    (conditionalContinuationLaw π ρ P hP hN h).map (frestrictLe N) =
      ((conditionalContinuationLaw π ρ P hP hN h).map (fun H => H N)).map
        (reconstructPrefix (A := A) (Y := Y) N) := by
  unfold conditionalContinuationLaw
  rw [Measure.map_map (measurable_frestrictLe N) (continuationHistory_measurable π hπ h),
    Measure.map_map (measurable_pi_apply N) (continuationHistory_measurable π hπ h),
    Measure.map_map (measurable_of_countable (reconstructPrefix (A := A) (Y := Y) N))
      ((measurable_pi_apply N).comp (continuationHistory_measurable π hπ h))]
  congr 1
  funext z i
  exact (continuationHistory_drop π h z N i.val (Finset.mem_Iic.mp i.property)).symm

/-- Actual conditional infinite continuation law equals the canonical restarted
observed-history law. This follows from the proved cylinder probabilities and
prefix reconstruction, without assuming any fresh unused-oracle-tail law. -/
theorem conditionalContinuationLaw_eq_restart
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hpos : 0 < CanonicalInput ρ P hP hN (PrefixEvent π h)) :
    conditionalContinuationLaw π ρ P hP hN h =
      observedTraceLaw ∅ (restartPolicy π h) (commonSeedPosterior π ρ h)
        P P hP hN hP hN := by
  haveI := commonSeedPosterior_probability π ρ h
    (positive_prefix_compatible_seeds π ρ P hP hN h hpos)
  haveI : IsFiniteMeasure (observedTraceLaw ∅ (restartPolicy π h)
      (commonSeedPosterior π ρ h) P P hP hN hP hN) := by
    unfold observedTraceLaw
    infer_instance
  apply measure_eq_of_prefix_maps
  intro N
  rw [conditional_prefix_map_from_last π hπ ρ P hP hN h N,
    conditional_continuation_marginal_eq_restart π hπ ρ P hP hN h hpos N,
    observed_prefix_map_from_last ∅ (restartPolicy π h)
      (restartPolicy_measurable π hπ h) (commonSeedPosterior π ρ h) P P hP hN hP hN N]
  unfold observedTraceLaw
  rw [Measure.map_map (measurable_pi_apply N)
    (historyTrajectory_measurable ∅ (restartPolicy π h) (restartPolicy_measurable π hπ h))]
  rfl

/-- The same continuation is a readout of the original observed history path. -/
def continuationReadout (h : History A Y) (H : ℕ → History A Y) (n : ℕ) : History A Y :=
  (H (h.length+n)).take n

omit [DecidableEq A] [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem continuationReadout_measurable (h : History A Y) : Measurable (continuationReadout h) := by
  apply measurable_pi_lambda
  intro n
  exact (measurable_of_countable (fun xs : History A Y => xs.take n)).comp
    (measurable_pi_apply (h.length+n))

/-- Restriction and normalization commute with observing the finite prefix. -/
theorem normalizedRestriction_map_preimage {Ω Ξ : Type*}
    [MeasurableSpace Ω] [MeasurableSpace Ξ]
    (μ : Measure Ω) (f : Ω → Ξ) (hf : Measurable f) (C : Set Ξ) (hC : MeasurableSet C) :
    (normalizedRestriction μ (f ⁻¹' C)).map f = normalizedRestriction (μ.map f) C := by
  unfold normalizedRestriction
  rw [Measure.map_smul, Measure.restrict_map hf hC, Measure.map_apply hf hC]

/-- Exact observable definition: condition the original constructed observed
history law on h, then remove h from the future histories. This equals the latent
finite-event definition used in the cylinder proof. -/
theorem conditionalContinuationLaw_eq_conditioned_observation
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) :
    conditionalContinuationLaw π ρ P hP hN h =
      (normalizedRestriction (observedTraceLaw ∅ π ρ P P hP hN hP hN)
        {H | H h.length = h}).map (continuationReadout h) := by
  have hC : MeasurableSet {H : ℕ → History A Y | H h.length = h} := by
    simpa only [Set.preimage, Set.mem_singleton_iff] using
      (measurableSet_singleton h).preimage (measurable_pi_apply h.length)
  have he := normalizedRestriction_map_preimage (CanonicalInput ρ P hP hN)
    (historyTrajectory ∅ π) (historyTrajectory_measurable ∅ π hπ)
    {H | H h.length = h} hC
  change (normalizedRestriction (CanonicalInput ρ P hP hN) (PrefixEvent π h)).map
      (historyTrajectory ∅ π) =
    normalizedRestriction (observedTraceLaw ∅ π ρ P P hP hN hP hN)
      {H | H h.length = h} at he
  rw [← he, Measure.map_map (continuationReadout_measurable h)
    (historyTrajectory_measurable ∅ π hπ)]
  rfl

#print axioms conditionalContinuationLaw_eq_conditioned_observation
#print axioms conditionalContinuationLaw_eq_restart
#print axioms continuation_event_inter_prefix
#print axioms conditional_continuation_marginal
#print axioms conditional_continuation_marginal_eq_restart
end HiddenParity.ResidualSeed.Continuation
