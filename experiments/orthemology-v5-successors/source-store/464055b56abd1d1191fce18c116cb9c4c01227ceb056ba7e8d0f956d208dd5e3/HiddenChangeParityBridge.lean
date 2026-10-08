import HiddenChangeConditionalSafety

noncomputable section
open MeasureTheory ProbabilityTheory Set Filter
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed HiddenParity.Adaptive
open HiddenParity.ResidualSeed.Continuation

namespace HiddenChange
variable {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]

omit [NeZero n] in
theorem recurs_constTag_iff (σ : Mode) (x : ℕ → Pair n k) (g : TaggedPair n k) :
    Recurs (fun t => (σ,x t)) g ↔ g.1 = σ ∧ Recurs x g.2 := by
  constructor
  · intro h
    obtain ⟨t,ht⟩ := h.exists
    exact ⟨(congrArg Prod.fst ht).symm,h.mono (fun _ hh => congrArg Prod.snd hh)⟩
  · rintro ⟨hg,hr⟩
    exact hr.mono (fun t ht => Prod.ext hg.symm ht)

omit [NeZero n] in
theorem parity_constTag_iff (I : Input n k) (σ : Mode) (x : ℕ → Pair n k) :
    ParitySuccess (fun g : TaggedPair n k => I.priority g.1 g.2) (fun t => (σ,x t)) ↔
      ParitySuccess (I.priority σ) x := by
  simp only [ParitySuccess,IsMinimum,mem_recurrentSet,recurs_constTag_iff]
  constructor
  · rintro ⟨m,⟨⟨g,⟨hg,hr⟩,hgm⟩,hmin⟩,heven⟩
    refine ⟨m,⟨⟨g.2,hr,?_⟩,?_⟩,heven⟩
    · simpa only [hg] using hgm
    · intro e he
      exact hmin (σ,e) ⟨rfl,he⟩
  · rintro ⟨m,⟨⟨e,he,hem⟩,hmin⟩,heven⟩
    refine ⟨m,⟨⟨(σ,e),⟨rfl,he⟩,hem⟩,?_⟩,heven⟩
    intro g hg
    simpa only [hg.1] using hmin g.2 hg.2

omit [NeZero n] in
theorem parity_finalTag_iff (I : Input n k) (κ : ChangeIndex)
    (x : ℕ → TaggedPair n k) (hx : ∀ t, (x t).1 = fixedMode κ t) :
    ParitySuccess (fun g : TaggedPair n k => I.priority g.1 g.2) x ↔
      ParitySuccess (I.priority (finalMode κ)) (fun t => (x t).2) := by
  let N := κ.getD 0
  have hfinal : ∀ t, fixedMode κ (t+N) = finalMode κ := by
    intro t
    cases κ with
    | none => rfl
    | some j => simp [N,fixedMode,finalMode]
  have he : (fun t => x (t+N)) = (fun t => (finalMode κ,(x (t+N)).2)) := by
    funext t
    exact Prod.ext ((hx _).trans (hfinal t)) rfl
  rw [← paritySuccess_shift_iff _ x N,he,parity_constTag_iff]
  exact paritySuccess_shift_iff _ (fun t => (x t).2) N

omit [MeasurableSpace R] in
theorem fixed_historyAction (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (z : Orthemology.Tranche2.PolicyEmbedding.Input R (TaggedPair n k) (State n))
    (d : Pair n k) (t : ℕ) :
    historyAction (0,d) (historyTrajectory ∅ (fixedPolicy κ s π) z) t =
      (fixedMode κ t, historyAction d (eraseModeTrace (historyTrajectory ∅ (fixedPolicy κ s π) z)) t) := by
  simp only [historyAction,historyTrajectory,observedHistory,eraseModeTrace,eraseMode_cons,List.headD_cons,
    fixedPolicy,observedHistory_length]

/-- Actual governing-tag parity equals physical-pair parity for the final mode.
Only a deterministic finite prefix is discarded; the original policy is unchanged. -/
theorem fixedLaw_physical_parity_iff (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) (d : Pair n k) :
    (∀ᵐ H ∂fixedLaw I hI κ s ρ π, TaggedParity I d H) ↔
      ∀ᵐ H ∂fixedPhysicalLaw I hI κ s ρ π,
        ParitySuccess (I.priority (finalMode κ)) (historyAction d H) := by
  have hP : MeasurableSet {H : PairTrace n k | ParitySuccess (I.priority (finalMode κ)) (historyAction d H)} :=
    (paritySuccess_measurable (I.priority (finalMode κ))).preimage (historyAction_measurable d)
  have hT : MeasurableSet {H : TaggedTrace n k | TaggedParity I d H} :=
    (paritySuccess_measurable (fun g : TaggedPair n k => I.priority g.1 g.2)).preimage
      (historyAction_measurable (0,d))
  have hPE : MeasurableSet {H : TaggedTrace n k |
      ParitySuccess (I.priority (finalMode κ)) (historyAction d (eraseModeTrace H))} :=
    hP.preimage eraseModeTrace_measurable
  unfold fixedPhysicalLaw
  rw [ae_map_iff eraseModeTrace_measurable.aemeasurable hP]
  unfold fixedLaw observedTraceLaw
  rw [ae_map_iff (historyTrajectory_measurable ∅ _ (fixedPolicy_measurable κ s π hπ)).aemeasurable
    hT,
    ae_map_iff (historyTrajectory_measurable ∅ _ (fixedPolicy_measurable κ s π hπ)).aemeasurable
      hPE]
  apply Filter.eventually_congr
  exact Filter.Eventually.of_forall (fun z => by
    have ht : ∀ t, (historyAction (0,d) (historyTrajectory ∅ (fixedPolicy κ s π) z) t).1 = fixedMode κ t :=
      fun t => congrArg Prod.fst (fixed_historyAction κ s π z d t)
    have he : (fun t => (historyAction (0,d) (historyTrajectory ∅ (fixedPolicy κ s π) z) t).2) =
        historyAction d (eraseModeTrace (historyTrajectory ∅ (fixedPolicy κ s π) z)) := by
      funext t
      have hh := congrArg (fun g : TaggedPair n k => g.2) (fixed_historyAction κ s π z d t)
      exact hh
    simpa only [TaggedParity,he] using parity_finalTag_iff I κ _ ht)

theorem fixedConditional_ae_parity (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) (π : Policy R n k) (h : PairHistory n k)
    (d : Pair n k) (priority : Pair n k → ℕ)
    (hAS : ∀ᵐ H ∂fixedPhysicalLaw I hI κ s ρ π, ParitySuccess priority (historyAction d H)) :
    ∀ᵐ H ∂fixedConditionalLaw I hI κ s ρ π h, ParitySuccess priority (historyAction d H) := by
  apply fixedConditional_ae_of_prefix_imp I hI κ s ρ π h _ _
    ((paritySuccess_measurable priority).preimage (historyAction_measurable d)) _ hAS
  intro H _ hB
  rw [action_continuationReadout_shift]
  exact (paritySuccess_shift_iff priority _ h.length).mpr hB

/-- Stationary winning continuation at every positive post-final-mode prefix. -/
theorem fixed_restart_ae_parity (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) (h : PairHistory n k)
    (hp : PositivePrefix I hI κ s ρ π h)
    (hconstant : ∀ t, h.length ≤ t → fixedMode κ t = finalMode κ) (d : Pair n k)
    (hAS : ∀ᵐ H ∂fixedLaw I hI κ s ρ π, TaggedParity I d H) :
    ∀ᵐ H ∂markovHistoryLaw (I.kernel hI) (finalMode κ) (currentState s h)
      (restartPolicy π (erasePairSources h)) (commonSeedPosterior (pairPolicy s π) ρ h),
      ParitySuccess (I.priority (finalMode κ)) (historyAction d H) := by
  rw [← fixedConditionalLaw_eq_restart I hI κ s ρ π hπ h (finalMode κ) hp hconstant]
  exact fixedConditional_ae_parity I hI κ s ρ π h d _
    ((fixedLaw_physical_parity_iff I hI κ s ρ π hπ d).mp hAS)

end HiddenChange
