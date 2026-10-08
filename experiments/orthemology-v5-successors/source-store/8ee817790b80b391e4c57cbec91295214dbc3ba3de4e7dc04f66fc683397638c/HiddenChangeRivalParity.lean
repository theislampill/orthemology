import HiddenChangeParityBridge

/-! Rival parity from positive original recurrent events with event-local P0
compatibility. Prefix selection is countable at deterministic times. -/
noncomputable section
open MeasureTheory ProbabilityTheory Set Filter
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed HiddenParity.Adaptive
open HiddenParity.ResidualSeed.Continuation

namespace HiddenChange
variable {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]

omit [NeZero n] in
theorem all_zeroCompatible_measurable (I : Input n k) :
    MeasurableSet {H : PairTrace n k | ∀ t, ZeroCompatible I (H t)} := by
  simp only [Set.setOf_forall]
  exact MeasurableSet.iInter (fun t =>
    (Set.to_countable {h : PairHistory n k | ZeroCompatible I h}).measurableSet.preimage
      (measurable_pi_apply t))

/-- A positive event has a positive countable observation fiber. -/
theorem exists_positive_fiber_inter {Ω A : Type*} [MeasurableSpace Ω] [Countable A]
    (μ : Measure Ω) (B : Set Ω) (f : Ω → A) (hp : 0 < μ B) :
    ∃ a, 0 < μ ({ω | f ω = a} ∩ B) := by
  apply exists_measure_pos_of_not_measure_iUnion_null
  have he : (⋃ a, {ω | f ω = a} ∩ B) = B := by
    ext ω
    simp
  rw [he]
  exact hp.ne'

/-- Countable deterministic confinement and finite-prefix decomposition, while
retaining the event-local compatibility needed by the original no-change law. -/
theorem positive_compatible_recurrent_prefix (I : Input n k) (hI : I.Valid)
    (κ : ChangeIndex) (s : State n) (ρ : Measure R) (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (E : PairSet n k) (d : Pair n k)
    (hp : 0 < fixedPhysicalLaw I hI κ s ρ π
      {H | recurrentSet (historyAction d H) = E ∧ ∀ t, ZeroCompatible I (H t)}) :
    ∃ h : PairHistory n k, κ.getD 0 ≤ h.length ∧ ZeroCompatible I h ∧
      PositivePrefix I hI κ s ρ π h ∧
      0 < fixedPhysicalLaw I hI κ s ρ π
        {H | H h.length = h ∧ continuationReadout h H ∈ SurvivingRecurrent E d} := by
  let μ := fixedPhysicalLaw I hI κ s ρ π
  let B : Set (PairTrace n k) := {H | ∀ t, ZeroCompatible I (H t)}
  have hX : ∀ t, Measurable (fun H : PairTrace n k => historyAction d H t) :=
    fun t => (measurable_pi_apply t).comp (historyAction_measurable d)
  have hr : 0 < (μ.restrict B) (exactRecurrentEvent (historyAction d) E) := by
    rw [Measure.restrict_apply (measurable_exactRecurrentEvent _ hX E)]
    exact hp
  obtain ⟨N,hN⟩ := exists_positive_tail_index (μ.restrict B) (historyAction d) E hr
  rw [Measure.restrict_apply (measurable_tailEvent _ hX E N)] at hN
  let L := N + κ.getD 0
  have hL : 0 < μ (tailEvent (historyAction d) E L ∩ B) :=
    hN.trans_le (measure_mono (fun H hH =>
      ⟨⟨hH.1.1,fun t ht => hH.1.2 t (by dsimp [L] at ht; omega)⟩,hH.2⟩))
  obtain ⟨h,hh⟩ := exists_positive_fiber_inter μ (tailEvent (historyAction d) E L ∩ B)
    (fun H => H L) hL
  obtain ⟨H,hH,hcoh⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hh.ne'
    (ae_restrict_of_ae (fixedPhysicalLaw_coherent I hI κ s ρ π hπ))
  have hlen : h.length = L := by rw [← hH.1]; exact coherentTrace_length hcoh L
  have hc : ZeroCompatible I h := by rw [← hH.1]; exact hH.2.2 L
  have hprefix : PositivePrefix I hI κ s ρ π h := by
    unfold PositivePrefix
    rw [hlen]
    exact hh.trans_le (measure_mono Set.inter_subset_left)
  refine ⟨h,by rw [hlen]; dsimp [L]; omega,hc,hprefix,?_⟩
  apply hh.trans_le (measure_mono ?_)
  intro G hG
  refine ⟨by rw [hlen]; exact hG.1,?_,?_⟩
  · change recurrentSet (historyAction d (continuationReadout h G)) = E
    rw [action_continuationReadout_shift,recurrentSet_shift]
    exact hG.2.1.1
  · intro t
    rw [action_continuationReadout_shift]
    exact hG.2.1.2 _ (by rw [hlen]; omega)

/-- The literal conditional laws at a shared positive prefix agree on their
exact surviving recurrent event when their final-mode rows match on E. -/
theorem fixedConditional_surviving_recurrent_eq (I : Input n k) (hI : I.Valid)
    (κ τ : ChangeIndex) (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k) (E : PairSet n k) (d : Pair n k)
    (hp : PositivePrefix I hI κ s ρ π h) (hq : PositivePrefix I hI τ s ρ π h)
    (hκ : ∀ t, h.length ≤ t → fixedMode κ t = finalMode κ)
    (hτ : ∀ t, h.length ≤ t → fixedMode τ t = finalMode τ)
    (hm : Match I.row (finalMode κ) (finalMode τ) E) :
    fixedConditionalLaw I hI κ s ρ π h (SurvivingRecurrent E d) =
      fixedConditionalLaw I hI τ s ρ π h (SurvivingRecurrent E d) := by
  haveI := commonSeedPosterior_probability (pairPolicy s π) ρ h
    ((positive_prefix_factors I hI κ s ρ π hπ h).mp hp).1
  rw [fixedConditionalLaw_eq_restart I hI κ s ρ π hπ h (finalMode κ) hp hκ,
    fixedConditionalLaw_eq_restart I hI τ s ρ π hπ h (finalMode τ) hq hτ]
  have he := markov_history_restrict_eq (I.kernel hI) (finalMode κ) (finalMode τ)
    (currentState s h) (restartPolicy π (erasePairSources h))
    (restartPolicy_measurable π hπ (erasePairSources h))
    (commonSeedPosterior (pairPolicy s π) ρ h) E hm d
  have hv := congrArg (fun μ : Measure (PairTrace n k) => μ (SurvivingRecurrent E d)) he
  dsimp only at hv
  rw [Measure.restrict_apply (survivingRecurrent_measurable E d),
    Measure.restrict_apply (survivingRecurrent_measurable E d)] at hv
  simpa only [SurvivingRecurrent,Set.inter_assoc,Set.inter_self] using hv

/-- Every matching rival has even minimum on a positive recurrent component
of an original fixed-index law, provided only that this positive event has no
P0-incompatible receipt. No whole-law compatibility or safe-region assumption
is used, and the policy retains its complete original history. -/
theorem positive_compatible_recurrent_even (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (d : Pair n k)
    (hWin : ∀ κ, ∀ᵐ H ∂fixedLaw I hI κ s ρ π, TaggedParity I d H)
    (κ : ChangeIndex) (E : PairSet n k)
    (hp : 0 < fixedPhysicalLaw I hI κ s ρ π
      {H | recurrentSet (historyAction d H) = E ∧ ∀ t, ZeroCompatible I (H t)}) :
    ∀ σ, Match I.row (finalMode κ) σ E → EvenMinimum I σ E := by
  obtain ⟨h,hbound,hc,hp,hpos⟩ :=
    positive_compatible_recurrent_prefix I hI κ s ρ π hπ E d hp
  have hκ : ∀ t, h.length ≤ t → fixedMode κ t = finalMode κ := by
    intro t ht
    cases κ with
    | none => rfl
    | some N => simp only [Option.getD_some] at hbound; simp [fixedMode,finalMode,not_lt.mpr (hbound.trans ht)]
  have hp0 := compatible_prefix_noChange I hI κ s ρ π hπ h hp hc
  have hp1 : PositivePrefix I hI (some h.length) s ρ π h := by
    unfold PositivePrefix at hp0 ⊢
    rwa [← prefix_mass_noChange_switchAt I hI s ρ π hπ h]
  have hcond : 0 < fixedConditionalLaw I hI κ s ρ π h (SurvivingRecurrent E d) := by
    rw [fixed_prefix_tail_mass I hI κ s ρ π hπ h _ (survivingRecurrent_measurable E d) hp] at hpos
    exact (CanonicallyOrderedAdd.mul_pos.mp hpos).2
  intro σ hm
  have htarget : ∃ τ : ChangeIndex, finalMode τ = σ ∧
      PositivePrefix I hI τ s ρ π h ∧
      (∀ t, h.length ≤ t → fixedMode τ t = finalMode τ) := by
    fin_cases σ
    · exact ⟨none,rfl,hp0,fun _ _ => rfl⟩
    · exact ⟨some h.length,rfl,hp1,fun t ht => by simp [fixedMode,finalMode,not_lt.mpr ht]⟩
  obtain ⟨τ,hσ,hq,hτ⟩ := htarget
  have htransfer := fixedConditional_surviving_recurrent_eq I hI κ τ s ρ π hπ h E d hp hq hκ hτ
    (by simpa only [hσ] using hm)
  rw [htransfer] at hcond
  have hparity := fixedConditional_ae_parity I hI τ s ρ π h d _
    ((fixedLaw_physical_parity_iff I hI τ s ρ π hπ d).mp (hWin τ))
  obtain ⟨H,hH,hP⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hcond.ne'
    (ae_restrict_of_ae hparity)
  apply (evenMinimum_iff I σ E).mpr
  have hrec : recurrentSet (historyAction d H) = E := hH.1
  simpa only [ParitySuccess,hrec,hσ] using hP

end HiddenChange
