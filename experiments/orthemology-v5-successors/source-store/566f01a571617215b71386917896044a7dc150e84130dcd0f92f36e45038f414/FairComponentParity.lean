import InfiniteRecurrence
import StationaryPairChain
import PruningKernel

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open Orthemology.Tranche2 Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Recurrence
variable {State Pair : Type*} [Fintype State] [DecidableEq State]
variable [Fintype Pair] [DecidableEq Pair] [MeasurableSpace Pair] [MeasurableSingletonClass Pair]

/-- Erase only the finite-subtype proof from the actual retained-pair trajectory. -/
def pairReadout (E : Finset Pair) (x : ℕ → E) : ℕ → Pair := fun n => x n

omit [DecidableEq Pair] in
theorem pairReadout_measurable (E : Finset Pair) : Measurable (pairReadout E) := by
  unfold pairReadout
  fun_prop

/-- The actual stationary operating law on the original used-pair alphabet. -/
def operatingPairLaw (source : Pair → State) (E : Finset Pair)
    (P : Pair → State → ℝ) (hP : ∀ e ∈ E, ∀ s, 0 ≤ P e s)
    (hN : ∀ e ∈ E, ∑ s, P e s = 1)
    (hClosed : ∀ e ∈ E, ∀ s, 0 < P e s → s ∈ usedStates source E)
    (choice : StationaryChoices source E) (initial : E) : Measure (ℕ → Pair) :=
  (markovTrajectory (transitionKernel (pairChain source E P hP hN hClosed choice)) initial).map
    (pairReadout E)

instance operatingPairLaw_probability (source : Pair → State) (E : Finset Pair)
    (P : Pair → State → ℝ) (hP : ∀ e ∈ E, ∀ s, 0 ≤ P e s)
    (hN : ∀ e ∈ E, ∑ s, P e s = 1)
    (hClosed : ∀ e ∈ E, ∀ s, 0 < P e s → s ∈ usedStates source E)
    (choice : StationaryChoices source E) (initial : E) :
    IsProbabilityMeasure (operatingPairLaw source E P hP hN hClosed choice initial) :=
  isProbabilityMeasure_map (pairReadout_measurable E).aemeasurable

/-- Every used pair recurs infinitely often almost surely under the actual
positive stationary operating law, with no recurrence hypothesis. -/
theorem stationary_component_all_pairs_recur
    (source : Pair → State) (E : Finset Pair)
    (P : Pair → State → ℝ) (hP : ∀ e ∈ E, ∀ s, 0 ≤ P e s)
    (hN : ∀ e ∈ E, ∑ s, P e s = 1)
    (hEC : IsEndComponent source (positiveSuccessors P) E)
    (choice : StationaryChoices source E) (initial : E) :
    ∀ᵐ x ∂operatingPairLaw source E P hP hN
      (fun e he s hs => hEC.closed e he (by simp [positiveSuccessors, hs])) choice initial,
      recurrentSet x = E := by
  let hc : ∀ e ∈ E, ∀ s, 0 < P e s → s ∈ usedStates source E :=
    fun e he s hs => hEC.closed e he (by simp [positiveSuccessors, hs])
  let K := pairChain source E P hP hN hc choice
  have hStrong : ∀ e f : E, Relation.ReflTransGen (fun e f => 0 < K.prob e f) e f :=
    pairChain_strongly_connected source E P hP hN hEC choice
  have hRec := all_states_recur_almost_surely K initial hStrong
  apply (ae_map_iff (pairReadout_measurable E).aemeasurable
    (measurable_exactRecurrentEvent id (fun n => measurable_pi_apply n) E)).mpr
  filter_upwards [hRec] with x hx
  apply Finset.ext
  intro e
  rw [mem_recurrentSet]
  constructor
  · intro hfreq
    obtain ⟨n, hn⟩ := hfreq.exists
    have hmem := (x n).property
    change (x n : Pair) = e at hn
    exact hn ▸ hmem
  · intro he
    exact (hx ⟨e, he⟩).mono (fun _ hn => congrArg Subtype.val hn)

/-- Parity is genuinely about the minimum recurrent priority, not about all
priorities being even or odd visits eventually stopping. -/
def PairParitySuccess (priority : Pair → ℕ) (x : ℕ → Pair) : Prop :=
  ∃ k, IsMinimum priority (recurrentSet x) k ∧ k % 2 = 0

/-- A checked even-minimum component is parity-winning under any positive
stationary action distribution, including the constructed uniform distribution. -/
theorem stationary_component_parity
    (source : Pair → State) (E : Finset Pair)
    (P : Pair → State → ℝ) (hP : ∀ e ∈ E, ∀ s, 0 ≤ P e s)
    (hN : ∀ e ∈ E, ∑ s, P e s = 1)
    (hEC : IsEndComponent source (positiveSuccessors P) E)
    (choice : StationaryChoices source E) (initial : E) (priority : Pair → ℕ)
    (hEven : ∃ k, IsMinimum priority E k ∧ k % 2 = 0) :
    ∀ᵐ x ∂operatingPairLaw source E P hP hN
      (fun e he s hs => hEC.closed e he (by simp [positiveSuccessors, hs])) choice initial,
      PairParitySuccess priority x := by
  filter_upwards [stationary_component_all_pairs_recur source E P hP hN hEC choice initial] with x hx
  simpa only [PairParitySuccess, hx] using hEven

/-- Explicit uniform-operation specialization. -/
theorem uniform_component_parity
    (source : Pair → State) (E : Finset Pair)
    (P : Pair → State → ℝ) (hP : ∀ e ∈ E, ∀ s, 0 ≤ P e s)
    (hN : ∀ e ∈ E, ∑ s, P e s = 1)
    (hEC : IsEndComponent source (positiveSuccessors P) E)
    (initial : E) (priority : Pair → ℕ)
    (hEven : ∃ k, IsMinimum priority E k ∧ k % 2 = 0) :
    ∀ᵐ x ∂operatingPairLaw source E P hP hN
      (fun e he s hs => hEC.closed e he (by simp [positiveSuccessors, hs]))
      (uniformChoices source E) initial,
      PairParitySuccess priority x :=
  stationary_component_parity source E P hP hN hEC (uniformChoices source E) initial priority hEven

end HiddenParity.Recurrence
