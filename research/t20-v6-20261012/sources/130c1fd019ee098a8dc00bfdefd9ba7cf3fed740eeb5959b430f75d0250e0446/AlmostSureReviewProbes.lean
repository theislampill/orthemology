import ConditionalAlmostSure

noncomputable section
open MeasureTheory ProbabilityTheory Set Filter
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation HiddenParity.Stochastic
namespace IndependentASReview
universe u v w
variable {R : Type v} {A Y : Type u}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- A genuinely prefix-relative property, allowing arbitrary old-prefix actions:
the original law is eventually inside D from this fixed prefix length onward. -/
theorem fixed_prefix_stays_becomes_restart_stays
    (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) (D : Finset A) (d : A)
    (hAS : ∀ᵐ H ∂observedTraceLaw ∅ π ρ P P hP hN hP hN,
      ∀ n, historyAction d H (n+h.length) ∈ D) :
    ∀ᵐ H ∂conditionalContinuationLaw π ρ P hP hN h, H ∈ HistoryStays D d := by
  apply conditional_ae_of_prefix_imp π hπ ρ P hP hN h
    (fun H => ∀ n, historyAction d H (n+h.length) ∈ D)
    (fun H => H ∈ HistoryStays D d) (historyStays_measurable D d) ?_ hAS
  intro H _ hH
  change ∀ n, historyAction d (continuationReadout h H) n ∈ D
  rw [action_continuationReadout_shift]
  exact hH

/-- Null conditioning is algebraically zero, so AS claims there are vacuous.
A probability-restart use must retain the positive-prefix hypothesis. -/
theorem null_conditioning_makes_false_ae
    (π : R → History A Y → A) (ρ : Measure R)
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y)
    (hz : CanonicalInput ρ P hP hN (PrefixEvent π h) = 0) :
    ∀ᵐ _H ∂conditionalContinuationLaw π ρ P hP hN h, False := by
  have hr := Measure.restrict_eq_zero.mpr hz
  simp [conditionalContinuationLaw, normalizedRestriction, hr]

section Markov
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Fully expanded original-AS to restarted-AS contract. The policy receives
only the same private seed and complete observed action/state history. -/
theorem original_parity_implies_actual_restart_parity
    (P : RationalKernel Model (State × Action) State) (σ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (h : History (State × Action) State)
    (d : State × Action) (priority : State × Action → ℕ)
    (hp : 0 < markovHistoryLaw P σ s₀ π ρ {H | H h.length = h})
    (hAS : ∀ᵐ H ∂markovHistoryLaw P σ s₀ π ρ, ParitySuccess priority (historyAction d H)) :
    ∀ᵐ H ∂markovHistoryLaw P σ (currentState s₀ h)
      (fun r tail => π r (tail ++ erasePairSources h))
      ((ρ (CompatibleSeeds (pairPolicy s₀ π) h))⁻¹ •
        ρ.restrict (CompatibleSeeds (pairPolicy s₀ π) h)),
      ParitySuccess priority (historyAction d H) :=
  markov_restart_ae_parity P σ s₀ π hπ ρ h d priority hp hAS

/-- An odd matching rival minimum forces the exact conditional recurrent/no-exit
event to have mass zero. This is a contradiction consequence of the terminal
necessity theorem, not an additional lower-bound or transfer premise. -/
theorem odd_matching_rival_forces_zero_recurrence
    (P : RationalKernel Model (State × Action) State) (θ σ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (h : History (State × Action) State)
    (E : Finset (State × Action)) (d : State × Action) (priority : State × Action → ℕ)
    (hp : 0 < markovHistoryLaw P θ s₀ π ρ {H | H h.length = h})
    (hq : 0 < markovHistoryLaw P σ s₀ π ρ {H | H h.length = h})
    (hm : Match P.row θ σ E)
    (hAS : ∀ᵐ H ∂markovHistoryLaw P σ s₀ π ρ, ParitySuccess priority (historyAction d H))
    (k : ℕ) (hmin : IsMinimum priority E k) (hodd : k % 2 = 1) :
    conditionalMarkovContinuationLaw P θ s₀ π ρ h (SurvivingRecurrent E d) = 0 := by
  by_contra hn
  obtain ⟨j,hj,heven⟩ := matching_rival_even_after_positive_prefix P θ σ s₀ π hπ ρ h E d
    priority hp hq hm hAS (pos_iff_ne_zero.mpr hn)
  have heq := minimum_unique hmin hj
  omega
end Markov

/-- Infinite deterministic lasso: deleting a transient odd priority does not
change parity, because recurrent priorities, not finite minima, define it. -/
def transientOdd (n : ℕ) : Fin 2 := if n=0 then 0 else 1
def lassoPriority (a : Fin 2) : Nat := if a=0 then 1 else 2

theorem transient_symbol_not_recurrent : ¬ Recurs transientOdd (0:Fin 2) := by
  simp only [Recurs, frequently_atTop]
  intro h
  obtain ⟨n,hn,he⟩ := h 1
  have hne : n ≠ 0 := by omega
  simp [transientOdd,hne] at he

theorem permanent_symbol_recurrent : Recurs transientOdd (1:Fin 2) := by
  simp only [Recurs, frequently_atTop]
  intro N
  refine ⟨N+1,by omega,?_⟩
  simp [transientOdd]

theorem lasso_actual_recurrent_set : recurrentSet transientOdd = ({1} : Finset (Fin 2)) := by
  ext a
  fin_cases a
  · simp [mem_recurrentSet,transient_symbol_not_recurrent]
  · simp [mem_recurrentSet,permanent_symbol_recurrent]

theorem lasso_parity_after_every_prefix (N : ℕ) :
    ParitySuccess lassoPriority (fun n => transientOdd (n+N)) := by
  apply (HiddenParity.Adaptive.paritySuccess_shift_iff _ _ _).mpr
  change ∃ k, IsMinimum lassoPriority (recurrentSet transientOdd) k ∧ k%2=0
  rw [lasso_actual_recurrent_set]
  exact ⟨2,by simp [IsMinimum,lassoPriority],by decide⟩

set_option pp.explicit true in
#check @conditional_ae_of_prefix_imp
set_option pp.explicit true in
#check @matching_rival_even_after_positive_prefix
#print axioms fixed_prefix_stays_becomes_restart_stays
#print axioms null_conditioning_makes_false_ae
#print axioms original_parity_implies_actual_restart_parity
#print axioms odd_matching_rival_forces_zero_recurrence
#print axioms transient_symbol_not_recurrent
#print axioms permanent_symbol_recurrent
#print axioms lasso_actual_recurrent_set
#print axioms lasso_parity_after_every_prefix
end IndependentASReview
