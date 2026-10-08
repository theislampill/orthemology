import HiddenChangePrefix

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed
open HiddenParity.ResidualSeed.Continuation

namespace HiddenChange
variable {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]

theorem prefix_likelihood_noChange_switchAt (I : Input n k) (h : PairHistory n k) :
    fixedPrefixLikelihood I none h = fixedPrefixLikelihood I (some h.length) h := by
  unfold fixedPrefixLikelihood
  apply Finset.prod_congr rfl
  intro i _
  have hi : h.length - 1 - i.val < h.length := by have := i.isLt; omega
  simp only [fixedMode, hi, if_true]

theorem prefix_mass_noChange_switchAt (I : Input n k) (hI : I.Valid) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) (h : PairHistory n k) :
    fixedPhysicalLaw I hI none s ρ π {H | H h.length = h} =
      fixedPhysicalLaw I hI (some h.length) s ρ π {H | H h.length = h} := by
  rw [fixed_prefix_probability I hI none s ρ π hπ,
    fixed_prefix_probability I hI (some h.length) s ρ π hπ,
    prefix_likelihood_noChange_switchAt]

/-- Multiplication recovers the actual unconditioned prefix-and-tail mass.
The conditioned law remains a normalized restriction of the original law. -/
theorem fixed_prefix_tail_mass (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k) (C : Set (PairTrace n k)) (hC : MeasurableSet C)
    (hp : 0 < fixedPhysicalLaw I hI κ s ρ π {H | H h.length = h}) :
    fixedPhysicalLaw I hI κ s ρ π
      {H | H h.length = h ∧ continuationReadout h H ∈ C} =
      fixedPhysicalLaw I hI κ s ρ π {H | H h.length = h} *
        fixedConditionalLaw I hI κ s ρ π h C := by
  haveI := fixedPhysicalLaw_probability I hI κ s ρ π hπ
  rw [fixedConditionalLaw, Measure.map_apply (continuationReadout_measurable h) hC,
    normalizedRestriction, Measure.smul_apply,
    Measure.restrict_apply (hC.preimage (continuationReadout_measurable h))]
  simp only [smul_eq_mul]
  rw [← mul_assoc, ENNReal.mul_inv_cancel (ne_of_gt hp) (measure_ne_top _ _), one_mul]
  congr 1
  ext H
  simp only [Set.mem_setOf_eq, Set.mem_inter_iff, Set.mem_preimage]
  tauto

set_option maxHeartbeats 800000 in
/-- Genuinely changed forward transport: both laws use P0 on the selected
prefix, then matched rows while confined to E. No stationary-P1 prefix
positivity premise occurs. Generic stationary killed-law equality is inherited. -/
theorem noChange_switchAt_prefix_tail_eq (I : Input n k) (hI : I.Valid) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k) (E : PairSet n k) (d : Pair n k)
    (hm : Match I.row 0 1 E) (C : Set (PairTrace n k)) (hC : MeasurableSet C) :
    fixedPhysicalLaw I hI none s ρ π
      {H | H h.length = h ∧ continuationReadout h H ∈ C ∩ HistoryStays E d} =
    fixedPhysicalLaw I hI (some h.length) s ρ π
      {H | H h.length = h ∧ continuationReadout h H ∈ C ∩ HistoryStays E d} := by
  have he := prefix_mass_noChange_switchAt I hI s ρ π hπ h
  by_cases hp : 0 < fixedPhysicalLaw I hI none s ρ π {H | H h.length = h}
  · have hq : 0 < fixedPhysicalLaw I hI (some h.length) s ρ π {H | H h.length = h} := by
      rw [← he]; exact hp
    have hc : 0 < ρ (CompatibleSeeds (pairPolicy s π) h) := by
      rw [fixed_prefix_probability I hI none s ρ π hπ] at hp
      by_contra hh
      have hz : ρ (CompatibleSeeds (pairPolicy s π) h) = 0 := le_antisymm (not_lt.mp hh) (zero_le _)
      rw [hz, zero_mul] at hp
      exact (lt_irrefl 0) hp
    haveI := commonSeedPosterior_probability (pairPolicy s π) ρ h hc
    have hEC : MeasurableSet (C ∩ HistoryStays E d) := hC.inter (historyStays_measurable E d)
    rw [fixed_prefix_tail_mass I hI none s ρ π hπ h _ hEC hp,
      fixed_prefix_tail_mass I hI (some h.length) s ρ π hπ h _ hEC hq,
      fixedConditionalLaw_eq_restart I hI none s ρ π hπ h 0 hp (fun _ _ => rfl),
      fixedConditionalLaw_eq_restart I hI (some h.length) s ρ π hπ h 1 hq
        (fun t ht => by simp only [fixedMode, if_neg (not_lt.mpr ht)]), he]
    apply congrArg (fun v : ℝ≥0∞ =>
      fixedPhysicalLaw I hI (some h.length) s ρ π {H | H h.length = h} * v)
    have hk := markov_history_restrict_eq (I.kernel hI) 0 1 (currentState s h)
      (restartPolicy π (erasePairSources h)) (restartPolicy_measurable π hπ (erasePairSources h))
      (commonSeedPosterior (pairPolicy s π) ρ h) E hm d
    have hx := congrArg (fun μ : Measure (PairTrace n k) => μ C) hk
    simpa only [Measure.restrict_apply hC] using hx
  · have hz : fixedPhysicalLaw I hI none s ρ π {H | H h.length = h} = 0 :=
      le_antisymm (not_lt.mp hp) (zero_le _)
    have hz' : fixedPhysicalLaw I hI (some h.length) s ρ π {H | H h.length = h} = 0 := by
      rw [← he]; exact hz
    have hleft : fixedPhysicalLaw I hI none s ρ π
        {H | H h.length = h ∧ continuationReadout h H ∈ C ∩ HistoryStays E d} = 0 :=
      measure_mono_null (fun _ hh => hh.1) hz
    have hright : fixedPhysicalLaw I hI (some h.length) s ρ π
        {H | H h.length = h ∧ continuationReadout h H ∈ C ∩ HistoryStays E d} = 0 :=
      measure_mono_null (fun _ hh => hh.1) hz'
    rw [hleft, hright]

/-- The late-switch equality covers the exact recurrent-E/no-exit event, not
only finite tail cylinders. Measurability of this event is inherited. -/
theorem noChange_switchAt_exact_recurrent_eq (I : Input n k) (hI : I.Valid) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k) (E : PairSet n k) (d : Pair n k)
    (hm : Match I.row 0 1 E) :
    fixedPhysicalLaw I hI none s ρ π
      {H | H h.length = h ∧ continuationReadout h H ∈ SurvivingRecurrent E d} =
    fixedPhysicalLaw I hI (some h.length) s ρ π
      {H | H h.length = h ∧ continuationReadout h H ∈ SurvivingRecurrent E d} := by
  have he := noChange_switchAt_prefix_tail_eq I hI s ρ π hπ h E d hm
    (SurvivingRecurrent E d) (survivingRecurrent_measurable E d)
  simpa only [SurvivingRecurrent, Set.inter_assoc, Set.inter_self] using he

end HiddenChange
