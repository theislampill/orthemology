import ConditionalKilledContinuation
import ParityTailInvariance

noncomputable section
open MeasureTheory ProbabilityTheory Set Filter
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity.Stochastic HiddenParity.Adaptive

namespace HiddenParity.ResidualSeed.Continuation
universe u v w
variable {R : Type v} {A Y : Type u}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

omit [Fintype A] [Fintype Y] [DecidableEq A] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- The actual continuation action readout is precisely the finite shift of the
original action readout, not an independently supplied tail process. -/
theorem action_continuationReadout_shift (h : History A Y) (H : ℕ → History A Y) (d : A) :
    historyAction d (continuationReadout h H) = fun n => historyAction d H (n+h.length) := by
  funext n
  simp only [historyAction, continuationReadout]
  have he : h.length+(n+1) = (n+h.length)+1 := by omega
  rw [he]
  cases H ((n+h.length)+1) <;> rfl

/-- General lawful-restart interface: an original almost-sure history property
passes to a continuation property whenever the deterministic prefix-relative
implication is proved. No conditional AS statement is a premise. -/
theorem conditional_ae_of_prefix_imp
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (Before After : (ℕ → History A Y) → Prop)
    (hAfter : MeasurableSet {H | After H})
    (hImp : ∀ H, H h.length = h → Before H → After (continuationReadout h H))
    (hAS : ∀ᵐ H ∂observedTraceLaw ∅ π ρ P P hP hN hP hN, Before H) :
    ∀ᵐ H ∂conditionalContinuationLaw π ρ P hP hN h, After H := by
  rw [conditionalContinuationLaw_eq_conditioned_observation π hπ ρ P hP hN h]
  apply (ae_map_iff (continuationReadout_measurable h).aemeasurable hAfter).mpr
  have hC : MeasurableSet {H : ℕ → History A Y | H h.length = h} := by
    simpa only [Set.preimage, Set.mem_singleton_iff] using
      (measurableSet_singleton h).preimage (measurable_pi_apply h.length)
  have hBefore : ∀ᵐ H ∂normalizedRestriction (observedTraceLaw ∅ π ρ P P hP hN hP hN)
      {H | H h.length = h}, Before H :=
    Measure.ae_smul_measure (ae_restrict_of_ae hAS) _
  have hPrefix : ∀ᵐ H ∂normalizedRestriction (observedTraceLaw ∅ π ρ P P hP hN hP hN)
      {H | H h.length = h}, H h.length = h :=
    Measure.ae_smul_measure (ae_restrict_mem hC) _
  filter_upwards [hBefore, hPrefix] with H hB hH
  exact hImp H hH hB

/-- Every measurable tail-stable almost-sure action property passes from the
original experiment to its actual conditional continuation. Restriction and
normalization, not an AS-preservation assumption, perform the measure step. -/
theorem conditional_ae_tail_property
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) (d : A)
    (F : (ℕ → A) → Prop) (hF : MeasurableSet {x | F x})
    (hTail : ∀ x N, F x → F (fun n => x (n+N)))
    (hAS : ∀ᵐ H ∂observedTraceLaw ∅ π ρ P P hP hN hP hN, F (historyAction d H)) :
    ∀ᵐ H ∂conditionalContinuationLaw π ρ P hP hN h, F (historyAction d H) := by
  rw [conditionalContinuationLaw_eq_conditioned_observation π hπ ρ P hP hN h]
  apply (ae_map_iff (continuationReadout_measurable h).aemeasurable
    (hF.preimage (historyAction_measurable d))).mpr
  have hs : ∀ᵐ H ∂normalizedRestriction (observedTraceLaw ∅ π ρ P P hP hN hP hN)
      {H | H h.length = h}, F (historyAction d H) :=
    Measure.ae_smul_measure (ae_restrict_of_ae hAS) _
  filter_upwards [hs] with H hH
  rw [action_continuationReadout_shift]
  exact hTail (historyAction d H) h.length hH

/-- Actual minimum-recurrent-priority parity is tail invariant by the exact
imported finite-shift theorem. -/
theorem conditional_ae_parity
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) (d : A) (priority : A → ℕ)
    (hAS : ∀ᵐ H ∂observedTraceLaw ∅ π ρ P P hP hN hP hN,
      ParitySuccess priority (historyAction d H)) :
    ∀ᵐ H ∂conditionalContinuationLaw π ρ P hP hN h,
      ParitySuccess priority (historyAction d H) :=
  conditional_ae_tail_property π hπ ρ P hP hN h d (ParitySuccess priority)
    (paritySuccess_measurable priority)
    (fun x N hx => (paritySuccess_shift_iff priority x N).mpr hx) hAS

section Markov
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- The generic prefix-relative implication transports directly to the actual
state-consistent Markov restart, supporting lawful-menu properties as well as
objectives that are invariant under finite prefix deletion. -/
theorem markov_restart_ae_of_prefix_imp
    (P : RationalKernel Model (State × Action) State) (θ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (h : History (State × Action) State)
    (Before After : (ℕ → History (State × Action) State) → Prop)
    (hAfter : MeasurableSet {H | After H})
    (hImp : ∀ H, H h.length = h → Before H → After (continuationReadout h H))
    (hp : 0 < markovHistoryLaw P θ s₀ π ρ {H | H h.length = h})
    (hAS : ∀ᵐ H ∂markovHistoryLaw P θ s₀ π ρ, Before H) :
    ∀ᵐ H ∂markovHistoryLaw P θ (currentState s₀ h) (restartPolicy π (erasePairSources h))
      (commonSeedPosterior (pairPolicy s₀ π) ρ h), After H := by
  rw [← conditionalMarkovContinuationLaw_eq_restart P θ s₀ π hπ ρ h hp]
  exact conditional_ae_of_prefix_imp (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ)
    ρ (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ) h
    Before After hAfter hImp hAS

/-- Concrete residual Markov policy preserves every measurable AS tail property
under the derived common posterior seed, after an actual positive prefix. -/
theorem markov_restart_ae_tail_property
    (P : RationalKernel Model (State × Action) State) (θ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (h : History (State × Action) State)
    (d : State × Action) (F : (ℕ → State × Action) → Prop)
    (hF : MeasurableSet {x | F x}) (hTail : ∀ x N, F x → F (fun n => x (n+N)))
    (hp : 0 < markovHistoryLaw P θ s₀ π ρ {H | H h.length = h})
    (hAS : ∀ᵐ H ∂markovHistoryLaw P θ s₀ π ρ, F (historyAction d H)) :
    ∀ᵐ H ∂markovHistoryLaw P θ (currentState s₀ h) (restartPolicy π (erasePairSources h))
      (commonSeedPosterior (pairPolicy s₀ π) ρ h), F (historyAction d H) := by
  rw [← conditionalMarkovContinuationLaw_eq_restart P θ s₀ π hπ ρ h hp]
  exact conditional_ae_tail_property (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ)
    ρ (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ) h d F hF hTail hAS

theorem markov_restart_ae_parity
    (P : RationalKernel Model (State × Action) State) (θ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (h : History (State × Action) State)
    (d : State × Action) (priority : State × Action → ℕ)
    (hp : 0 < markovHistoryLaw P θ s₀ π ρ {H | H h.length = h})
    (hAS : ∀ᵐ H ∂markovHistoryLaw P θ s₀ π ρ, ParitySuccess priority (historyAction d H)) :
    ∀ᵐ H ∂markovHistoryLaw P θ (currentState s₀ h) (restartPolicy π (erasePairSources h))
      (commonSeedPosterior (pairPolicy s₀ π) ρ h), ParitySuccess priority (historyAction d H) :=
  markov_restart_ae_tail_property P θ s₀ π hπ ρ h d (ParitySuccess priority)
    (paritySuccess_measurable priority)
    (fun x N hx => (paritySuccess_shift_iff priority x N).mpr hx) hp hAS

/-- A matching rival that wins almost surely in the original experiment has an
even minimum on any positive exact recurrent/no-outside conditional tail. Both
restart-law and AS-tail preservation are derived, not premises. -/
theorem matching_rival_even_after_positive_prefix
    (P : RationalKernel Model (State × Action) State) (θ σ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (h : History (State × Action) State)
    (E : Finset (State × Action)) (d : State × Action) (priority : State × Action → ℕ)
    (hp : 0 < markovHistoryLaw P θ s₀ π ρ {H | H h.length = h})
    (hq : 0 < markovHistoryLaw P σ s₀ π ρ {H | H h.length = h})
    (hm : Match P.row θ σ E)
    (hAS : ∀ᵐ H ∂markovHistoryLaw P σ s₀ π ρ, ParitySuccess priority (historyAction d H))
    (hPos : 0 < conditionalMarkovContinuationLaw P θ s₀ π ρ h (SurvivingRecurrent E d)) :
    ∃ k, IsMinimum priority E k ∧ k % 2 = 0 := by
  rw [conditional_markov_surviving_recurrent_eq P θ σ s₀ π hπ ρ h E d hp hq hm] at hPos
  have hConditional : ∀ᵐ H ∂conditionalMarkovContinuationLaw P σ s₀ π ρ h,
      ParitySuccess priority (historyAction d H) :=
    conditional_ae_parity (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ)
      ρ (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) h d priority hAS
  obtain ⟨H, hH, hParity⟩ := Measure.exists_mem_of_measure_ne_zero_of_ae hPos.ne'
    (ae_restrict_of_ae hConditional)
  have hRec : recurrentSet (historyAction d H) = E := hH.1
  simpa only [ParitySuccess, hRec] using hParity
end Markov

#print axioms conditional_ae_of_prefix_imp
#print axioms markov_restart_ae_of_prefix_imp
#print axioms action_continuationReadout_shift
#print axioms conditional_ae_tail_property
#print axioms conditional_ae_parity
#print axioms markov_restart_ae_tail_property
#print axioms markov_restart_ae_parity
#print axioms matching_rival_even_after_positive_prefix
end HiddenParity.ResidualSeed.Continuation
