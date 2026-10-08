import KilledRecurrentTransfer
import MarkovSupportAdapter

noncomputable section
open MeasureTheory ProbabilityTheory Set
open Orthemology.Tranche2.FiniteAlphabetQuery
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Stochastic
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Current observed state is the most recent receipt, or the given initial state. -/
def currentState (s₀ : State) : History (State × Action) State → State
  | [] => s₀
  | (_, y) :: _ => y

/-- Erase redundant source-state labels; retain every selected action and receipt. -/
def erasePairSources (h : History (State × Action) State) : History Action State :=
  h.map (fun z => (z.1.2, z.2))

/-- A genuine causal Markov policy chooses an action from its private seed and
complete action/observed-state history. The source coordinate is imposed by observation. -/
def pairPolicy (s₀ : State) (π : R → History Action State → Action)
    (r : R) (h : History (State × Action) State) : State × Action :=
  (currentState s₀ h, π r (erasePairSources h))

omit [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
    [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
    [MeasurableSpace Action] [MeasurableSingletonClass Action] in
theorem pairPolicy_source (s₀ : State) (π : R → History Action State → Action)
    (r : R) (h : History (State × Action) State) :
    (pairPolicy s₀ π r h).1 = currentState s₀ h := rfl

omit [DecidableEq State] [DecidableEq Action] [Inhabited State]
    [MeasurableSingletonClass State] [MeasurableSingletonClass Action] in
theorem pairPolicy_measurable (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2)) :
    Measurable (fun z : R × History (State × Action) State => pairPolicy s₀ π z.1 z.2) :=
  ((measurable_of_countable (currentState s₀)).comp measurable_snd).prodMk
    (hπ.comp (measurable_fst.prodMk ((measurable_of_countable erasePairSources).comp measurable_snd)))

omit [Fintype State] [Fintype Action] [Inhabited State]
    [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
    [MeasurableSpace Action] [MeasurableSingletonClass Action] in
/-- Every step uses the fresh row indexed by the current observed state and
selected action, and appends its actual observed successor. -/
theorem canonical_markov_history_step (s₀ : State) (π : R → History Action State → Action)
    (oracle : ℕ → (State × Action) → State) (r : R) (X : Stack (State × Action) State) (n : ℕ) :
    observedHistory ∅ (pairPolicy s₀ π) oracle r X (n+1) =
      let h := observedHistory ∅ (pairPolicy s₀ π) oracle r X n
      let e := (currentState s₀ h, π r (erasePairSources h))
      (e, oracle n e) :: h := by
  simp [observedHistory, feedback, outsideCount, pairPolicy, observedHistory_length]

/-- The exact same normalized rational full rows viewed as real probabilities. -/
def realRows (P : RationalKernel Model (State × Action) State) (θ : Model)
    (e : State × Action) (y : State) : ℝ := P.row θ e y

omit [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
    [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
    [MeasurableSpace Action] [MeasurableSingletonClass Action] in
theorem realRows_nonnegative (P : RationalKernel Model (State × Action) State) (θ : Model) :
    ∀ e y, 0 ≤ realRows P θ e y := by
  intro e y
  change (0 : ℝ) ≤ (P.row θ e y : ℝ)
  exact_mod_cast P.nonnegative θ e y

omit [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
    [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
    [MeasurableSpace Action] [MeasurableSingletonClass Action] in
theorem realRows_normalized (P : RationalKernel Model (State × Action) State) (θ : Model) :
    ∀ e, ∑ y, realRows P θ e y = 1 := by
  intro e
  have h := P.normalized θ e
  change ∑ y, (P.row θ e y : ℝ) = 1
  exact_mod_cast h

omit [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
    [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
    [MeasurableSpace Action] [MeasurableSingletonClass Action] in
theorem realRows_match (P : RationalKernel Model (State × Action) State)
    {θ σ : Model} {E : Finset (State × Action)} (hm : Match P.row θ σ E) :
    ∀ e ∈ E, realRows P θ e = realRows P σ e := by
  intro e he
  funext y
  have h := congrFun (hm e he) y
  change (P.row θ e y : ℝ) = (P.row σ e y : ℝ)
  exact_mod_cast h.symm

/-- A normalized finite rational Markov experiment with the actual common
state-consistent history policy, using the proved canonical fresh-row construction. -/
def markovHistoryLaw (P : RationalKernel Model (State × Action) State)
    (θ : Model) (s₀ : State) (π : R → History Action State → Action) (ρ : Measure R) :
    Measure (ℕ → History (State × Action) State) :=
  observedTraceLaw ∅ (pairPolicy s₀ π) ρ (realRows P θ) (realRows P θ)
    (realRows_nonnegative P θ) (realRows_normalized P θ)
    (realRows_nonnegative P θ) (realRows_normalized P θ)

/-- End-to-end full rational-row matching gives equal killed adaptive Markov
history laws. Neither source-state consistency nor a law-equivalence premise is assumed. -/
theorem markov_killed_historyLaw_eq
    (P : RationalKernel Model (State × Action) State) (θ σ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (E : Finset (State × Action)) (hm : Match P.row θ σ E) (d : State × Action) :
    (markovHistoryLaw P θ s₀ π ρ).map (killedHistory E d) =
      (markovHistoryLaw P σ s₀ π ρ).map (killedHistory E d) :=
  canonical_killed_historyLaw_eq E (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ) ρ
    (realRows P θ) (realRows P σ)
    (realRows_nonnegative P θ) (realRows_normalized P θ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) (realRows_match P hm) d

/-- Equality extends to arbitrary measurable observed-history events on the
surviving component, allowing outcome-dependent conditions. -/
theorem markov_history_restrict_eq
    (P : RationalKernel Model (State × Action) State) (θ σ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (E : Finset (State × Action)) (hm : Match P.row θ σ E) (d : State × Action) :
    (markovHistoryLaw P θ s₀ π ρ).restrict (HistoryStays E d) =
      (markovHistoryLaw P σ s₀ π ρ).restrict (HistoryStays E d) :=
  canonical_history_restrict_eq E (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ) ρ
    (realRows P θ) (realRows P σ)
    (realRows_nonnegative P θ) (realRows_normalized P θ)
    (realRows_nonnegative P σ) (realRows_normalized P σ) (realRows_match P hm) d

/-- A positive exact recurrent pair set must pass every full-row-matching live
rival's parity minimum test whenever the common policy wins under that rival.
The end-component graph premise is left explicit; its pathwise derivation is a
separate recurrent-closure obligation. -/
theorem markov_matching_parity_valid
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (E : Finset (State × Action)) (d : State × Action)
    (hEC : IsEndComponent Prod.fst (internalSuccessors P B) E)
    (hAS : ∀ σ ∈ B, ∀ᵐ H ∂markovHistoryLaw P σ s₀ π ρ,
      ParitySuccess (priority σ) (historyAction d H))
    (hPos : 0 < markovHistoryLaw P θ s₀ π ρ (SurvivingRecurrent E d)) :
    Valid (endComponentFamily Prod.fst (internalSuccessors P B)) B P.row priority θ E := by
  refine ⟨hEC, ?_⟩
  intro σ hσ hm
  exact matching_model_even_on_positive_surviving_recurrence E (pairPolicy s₀ π)
    (pairPolicy_measurable s₀ π hπ) ρ (realRows P θ) (realRows P σ)
    (realRows_nonnegative P θ) (realRows_normalized P θ)
    (realRows_nonnegative P σ) (realRows_normalized P σ)
    (realRows_match P hm) d (priority σ) (hAS σ hσ) hPos

end HiddenParity.Stochastic
