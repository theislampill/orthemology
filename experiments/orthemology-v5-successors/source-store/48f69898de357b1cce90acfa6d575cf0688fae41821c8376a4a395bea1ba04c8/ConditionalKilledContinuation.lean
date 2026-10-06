import ConditionalContinuationLaw
import KilledRecurrentTransfer
import MarkovSeedPosterior

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Stochastic

namespace HiddenParity.ResidualSeed.Continuation
universe u v w
variable {R : Type v} {A Y : Type u}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- Whole conditional killed continuation laws agree after an actual prefix
positive in both models. Old prefix rows need not agree. -/
theorem conditional_killed_continuation_eq
    (D : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P Q : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (h : History A Y) (d : A)
    (hp : 0 < CanonicalInput ρ P hP hPN (PrefixEvent π h))
    (hq : 0 < CanonicalInput ρ Q hQ hQN (PrefixEvent π h))
    (hrows : ∀ a ∈ D, P a = Q a) :
    (conditionalContinuationLaw π ρ P hP hPN h).map (killedHistory D d) =
      (conditionalContinuationLaw π ρ Q hQ hQN h).map (killedHistory D d) := by
  haveI := commonSeedPosterior_probability π ρ h
    (positive_prefix_compatible_seeds π ρ P hP hPN h hp)
  rw [conditionalContinuationLaw_eq_restart π hπ ρ P hP hPN h hp,
    conditionalContinuationLaw_eq_restart π hπ ρ Q hQ hQN h hq]
  exact canonical_killed_historyLaw_eq D (restartPolicy π h) (restartPolicy_measurable π hπ h)
    (commonSeedPosterior π ρ h) P Q hP hPN hQ hQN hrows d

/-- Equality of actual conditional continuation measures restricted to no future
outside pair, preserving all observed outcomes on the surviving tail. -/
theorem conditional_continuation_restrict_eq
    (D : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P Q : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (h : History A Y) (d : A)
    (hp : 0 < CanonicalInput ρ P hP hPN (PrefixEvent π h))
    (hq : 0 < CanonicalInput ρ Q hQ hQN (PrefixEvent π h))
    (hrows : ∀ a ∈ D, P a = Q a) :
    (conditionalContinuationLaw π ρ P hP hPN h).restrict (HistoryStays D d) =
      (conditionalContinuationLaw π ρ Q hQ hQN h).restrict (HistoryStays D d) := by
  haveI := commonSeedPosterior_probability π ρ h
    (positive_prefix_compatible_seeds π ρ P hP hPN h hp)
  rw [conditionalContinuationLaw_eq_restart π hπ ρ P hP hPN h hp,
    conditionalContinuationLaw_eq_restart π hπ ρ Q hQ hQN h hq]
  exact canonical_history_restrict_eq D (restartPolicy π h) (restartPolicy_measurable π hπ h)
    (commonSeedPosterior π ρ h) P Q hP hPN hQ hQN hrows d

/-- The exact adaptive-necessity interface: after the common positive prefix,
the full exact recurrent pair set and never-leaving-tail event has equal
conditional probability under retained full-row matching. -/
theorem conditional_surviving_recurrent_eq
    (D : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P Q : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (h : History A Y) (d : A)
    (hp : 0 < CanonicalInput ρ P hP hPN (PrefixEvent π h))
    (hq : 0 < CanonicalInput ρ Q hQ hQN (PrefixEvent π h))
    (hrows : ∀ a ∈ D, P a = Q a) :
    conditionalContinuationLaw π ρ P hP hPN h (SurvivingRecurrent D d) =
      conditionalContinuationLaw π ρ Q hQ hQN h (SurvivingRecurrent D d) := by
  haveI := commonSeedPosterior_probability π ρ h
    (positive_prefix_compatible_seeds π ρ P hP hPN h hp)
  rw [conditionalContinuationLaw_eq_restart π hπ ρ P hP hPN h hp,
    conditionalContinuationLaw_eq_restart π hπ ρ Q hQ hQN h hq]
  exact canonical_surviving_recurrent_eq D (restartPolicy π h) (restartPolicy_measurable π hπ h)
    (commonSeedPosterior π ρ h) P Q hP hPN hQ hQN hrows d

section Markov
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

def conditionalMarkovContinuationLaw
    (P : RationalKernel Model (State × Action) State) (θ : Model)
    (s₀ : State) (π : R → History Action State → Action) (ρ : Measure R)
    (h : History (State × Action) State) : Measure (ℕ → History (State × Action) State) :=
  conditionalContinuationLaw (pairPolicy s₀ π) ρ (realRows P θ)
    (realRows_nonnegative P θ) (realRows_normalized P θ) h

/-- The actual conditional shifted Markov-history law is identified with the
state-consistent restarted canonical law at the latest observed successor. -/
theorem conditionalMarkovContinuationLaw_eq_restart
    (P : RationalKernel Model (State × Action) State) (θ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (h : History (State × Action) State)
    (hp : 0 < markovHistoryLaw P θ s₀ π ρ {H | H h.length = h}) :
    conditionalMarkovContinuationLaw P θ s₀ π ρ h =
      markovHistoryLaw P θ (currentState s₀ h) (restartPolicy π (erasePairSources h))
        (commonSeedPosterior (pairPolicy s₀ π) ρ h) := by
  rw [markov_observed_prefix_mass P θ s₀ π hπ ρ h] at hp
  rw [conditionalMarkovContinuationLaw,
    conditionalContinuationLaw_eq_restart (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ)
      ρ (realRows P θ) (realRows_nonnegative P θ) (realRows_normalized P θ) h hp]
  have he : restartPolicy (pairPolicy s₀ π) h =
      pairPolicy (currentState s₀ h) (restartPolicy π (erasePairSources h)) := by
    funext r tail
    exact (restart_pairPolicy_agrees s₀ π h tail r).symm
  rw [he]
  rfl

/-- Full-row-matching normalized Markov models have identical killed conditional
continuations after any common positive full observed prefix. -/
theorem conditional_markov_killed_eq
    (P : RationalKernel Model (State × Action) State) (θ σ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (h : History (State × Action) State)
    (E : Finset (State × Action)) (d : State × Action)
    (hp : 0 < markovHistoryLaw P θ s₀ π ρ {H | H h.length = h})
    (hq : 0 < markovHistoryLaw P σ s₀ π ρ {H | H h.length = h})
    (hm : Match P.row θ σ E) :
    (conditionalMarkovContinuationLaw P θ s₀ π ρ h).map (killedHistory E d) =
      (conditionalMarkovContinuationLaw P σ s₀ π ρ h).map (killedHistory E d) := by
  rw [markov_observed_prefix_mass P θ s₀ π hπ ρ h] at hp
  rw [markov_observed_prefix_mass P σ s₀ π hπ ρ h] at hq
  exact conditional_killed_continuation_eq E (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ)
    ρ (realRows P θ) (realRows P σ) (realRows_nonnegative P θ) (realRows_normalized P θ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) h d hp hq (realRows_match P hm)

/-- Positive exact recurrent/no-exit tails transfer through the actual
conditional Markov measures, with no residual-law equality assumption. -/
theorem conditional_markov_surviving_recurrent_eq
    (P : RationalKernel Model (State × Action) State) (θ σ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (h : History (State × Action) State)
    (E : Finset (State × Action)) (d : State × Action)
    (hp : 0 < markovHistoryLaw P θ s₀ π ρ {H | H h.length = h})
    (hq : 0 < markovHistoryLaw P σ s₀ π ρ {H | H h.length = h})
    (hm : Match P.row θ σ E) :
    conditionalMarkovContinuationLaw P θ s₀ π ρ h (SurvivingRecurrent E d) =
      conditionalMarkovContinuationLaw P σ s₀ π ρ h (SurvivingRecurrent E d) := by
  rw [markov_observed_prefix_mass P θ s₀ π hπ ρ h] at hp
  rw [markov_observed_prefix_mass P σ s₀ π hπ ρ h] at hq
  exact conditional_surviving_recurrent_eq E (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ)
    ρ (realRows P θ) (realRows P σ) (realRows_nonnegative P θ) (realRows_normalized P θ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) h d hp hq (realRows_match P hm)
end Markov

#print axioms conditional_killed_continuation_eq
#print axioms conditional_continuation_restrict_eq
#print axioms conditional_surviving_recurrent_eq
#print axioms conditionalMarkovContinuationLaw_eq_restart
#print axioms conditional_markov_killed_eq
#print axioms conditional_markov_surviving_recurrent_eq
end HiddenParity.ResidualSeed.Continuation
