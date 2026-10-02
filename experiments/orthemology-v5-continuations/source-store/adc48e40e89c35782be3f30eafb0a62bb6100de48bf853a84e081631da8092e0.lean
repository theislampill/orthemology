import PosteriorFeedbackProduct
import MarkovKilledBridge

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Stochastic

namespace HiddenParity.ResidualSeed
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- A model survives the full observed history exactly when each observed
state/action row gives positive mass to its recorded successor. -/
def SurvivesHistory (P : RationalKernel Model (State × Action) State)
    (σ : Model) (h : History (State × Action) State) : Prop :=
  ∀ i : Fin h.length, 0 < P.row σ h[i].1 h[i].2

def markovSeedPosterior (P : RationalKernel Model (State × Action) State)
    (σ : Model) (s₀ : State) (π : R → History Action State → Action)
    (ρ : Measure R) (h : History (State × Action) State) : Measure R :=
  seedPosterior (pairPolicy s₀ π) ρ (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) h

/-- Actual observed-history probability is the probability of the latent input
prefix event used in the restricted/normalized posterior definition. -/
theorem markov_observed_prefix_mass (P : RationalKernel Model (State × Action) State)
    (σ : Model) (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) (h : History (State × Action) State) :
    markovHistoryLaw P σ s₀ π ρ {H | H h.length = h} =
      CanonicalInput ρ (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ)
        (PrefixEvent (pairPolicy s₀ π) h) :=
  observed_prefix_mass_eq_input (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ)
    ρ (realRows P σ) (realRows_nonnegative P σ) (realRows_normalized P σ) h

/-- Starting with a positive actually observed prefix, every surviving model
has a positive prefix and exactly the same posterior seed probability measure.
No equality of numerical transition probabilities across models is assumed. -/
theorem markov_common_residual_seed
    (P : RationalKernel Model (State × Action) State) (θ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (h : History (State × Action) State)
    (hpos : 0 < markovHistoryLaw P θ s₀ π ρ {H | H h.length = h}) :
    IsProbabilityMeasure (commonSeedPosterior (pairPolicy s₀ π) ρ h) ∧
      ∀ σ, SurvivesHistory P σ h →
        0 < markovHistoryLaw P σ s₀ π ρ {H | H h.length = h} ∧
        markovSeedPosterior P σ s₀ π ρ h = commonSeedPosterior (pairPolicy s₀ π) ρ h := by
  rw [markov_observed_prefix_mass P θ s₀ π hπ ρ h] at hpos
  have hc := positive_prefix_compatible_seeds (pairPolicy s₀ π) ρ (realRows P θ)
    (realRows_nonnegative P θ) (realRows_normalized P θ) h hpos
  refine ⟨commonSeedPosterior_probability (pairPolicy s₀ π) ρ h hc, ?_⟩
  intro σ hs
  have hsReal : ∀ i : Fin h.length, 0 < realRows P σ h[i].1 h[i].2 := by
    intro i
    change (0 : ℝ) < (P.row σ h[i].1 h[i].2 : ℝ)
    exact_mod_cast hs i
  have hpσ := surviving_model_prefix_positive (pairPolicy s₀ π) ρ (realRows P σ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) h hc hsReal
  refine ⟨?_, ?_⟩
  · rwa [markov_observed_prefix_mass P σ s₀ π hπ ρ h]
  · exact seedPosterior_eq_common (pairPolicy s₀ π) ρ (realRows P σ)
      (realRows_nonnegative P σ) (realRows_normalized P σ) h hpσ

omit [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State] [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State] [MeasurableSpace Action] [MeasurableSingletonClass Action] in
/-- The correct state-consistent restart agrees with appending the old pair
history. Histories are newest-first; the prior prefix is appended on the right. -/
theorem restart_pairPolicy_agrees (s₀ : State)
    (π : R → History Action State → Action) (h tail : History (State × Action) State) (r : R) :
    pairPolicy (currentState s₀ h) (restartPolicy π (erasePairSources h)) r tail =
      restartPolicy (pairPolicy s₀ π) h r tail := by
  cases tail <;> simp [pairPolicy, restartPolicy, currentState, erasePairSources, List.map_append]

omit [DecidableEq State] [DecidableEq Action] [Inhabited State] [MeasurableSingletonClass State] [MeasurableSingletonClass Action] in
/-- The common restarted policy is measurable and uses only the seed and
observed continuation history, with the fixed old history as a parameter. -/
theorem markov_restartPolicy_measurable (s₀ : State)
    (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (h : History (State × Action) State) :
    Measurable (fun z : R × History (State × Action) State =>
      pairPolicy (currentState s₀ h) (restartPolicy π (erasePairSources h)) z.1 z.2) :=
  pairPolicy_measurable (currentState s₀ h) (restartPolicy π (erasePairSources h))
    (restartPolicy_measurable π hπ (erasePairSources h))

#print axioms markov_observed_prefix_mass
#print axioms markov_common_residual_seed
#print axioms restart_pairPolicy_agrees
#print axioms markov_restartPolicy_measurable
end HiddenParity.ResidualSeed
