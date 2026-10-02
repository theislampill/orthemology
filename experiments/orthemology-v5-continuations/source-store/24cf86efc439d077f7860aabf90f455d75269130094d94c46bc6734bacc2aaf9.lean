import RawTapeRecurrence
import SequentialTapeConsumption
import RecurrentGraph
import MarkovKilledBridge

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Adaptive
open HiddenParity.Stochastic
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

omit [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
    [MeasurableSpace Action] [MeasurableSingletonClass Action] in
/-- In the real state-consistent stack policy, the next pair source is exactly
the current pair's observed receipt. -/
theorem stack_pair_source_next (s₀ : State) (π : R → History Action State → Action)
    (z : R × FlatStack (State × Action) State) (n : ℕ) :
    (stackActionTrajectory (pairPolicy s₀ π) z (n+1)).1 = stackReceipt (pairPolicy s₀ π) z n := by
  simp [stackActionTrajectory, pairPolicy, currentState, stackHistoryTrajectory,
    observedHistory, feedback, stackReceipt, countBefore]

/-- The actual positive-support graph, derived directly from the numerical full rows. -/
def supportSuccessors (P : (State × Action) → State → ℝ) (e : State × Action) : Finset State :=
  Finset.univ.filter (fun s => 0 < P e s)

/-- Arbitrary measurable adaptive Markov policies have end-component recurrent
pair sets almost surely. Actual iid tape support and recurrence are proved;
no fairness, finite memory, stationary policy, or conditioned-iid premise is assumed. -/
theorem canonical_markov_recurrent_end_component
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : (State × Action) → State → ℝ)
    (hP : ∀ e y, 0 ≤ P e y) (hN : ∀ e, ∑ y, P e y = 1) (d : State × Action) :
    ∀ᵐ x ∂actionLaw (pairPolicy s₀ π) ρ P hP hN d,
      IsEndComponent Prod.fst (supportSuccessors P) (recurrentSet x) := by
  apply actionLaw_ae_of_stack (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ) ρ P hP hN d _
    (measurable_recurrent_predicate (IsEndComponent Prod.fst (supportSuccessors P)))
  filter_upwards [seeded_all_tapes_supported ρ P hP hN, seeded_all_tapes_recurrent ρ P hP hN] with z hSupported hRecur
  let x := stackActionTrajectory (pairPolicy s₀ π) z
  apply recurrent_pairs_form_end_component Prod.fst (supportSuccessors P) x
  · intro n
    apply Finset.mem_filter.mpr
    refine ⟨Finset.mem_univ _, ?_⟩
    have hp := hSupported (x n) (countBefore (pairPolicy s₀ π) z (x n) n)
    change 0 < P (x n) (stackReceipt (pairPolicy s₀ π) z n) at hp
    simpa only [x, stack_pair_source_next] using hp
  · intro e he y hy
    have hAct : ∃ᶠ n in atTop, stackActionTrajectory (pairPolicy s₀ π) z n = e :=
      (mem_recurrentSet x e).mp he
    have hTape : ∃ᶠ k in atTop, z.2 (e,k) = y :=
      hRecur e y (Finset.mem_filter.mp hy).2
    have hBoth := recurrent_action_observes_recurrent_symbol (pairPolicy s₀ π) z e y hAct hTape
    exact hBoth.mono (fun n hn => ⟨hn.1, by simpa only [x, stack_pair_source_next] using hn.2⟩)

/-- Almost surely, the initial pair has the supplied observed source and every
consecutive pair follows a positive-probability actual transition. -/
theorem canonical_markov_supported_path
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : (State × Action) → State → ℝ)
    (hP : ∀ e y, 0 ≤ P e y) (hN : ∀ e, ∑ y, P e y = 1) (d : State × Action) :
    ∀ᵐ x ∂actionLaw (pairPolicy s₀ π) ρ P hP hN d,
      (x 0).1 = s₀ ∧ ∀ n, 0 < P (x n) (x (n+1)).1 := by
  have hMeas : MeasurableSet {x : ℕ → State × Action |
      (x 0).1 = s₀ ∧ ∀ n, 0 < P (x n) (x (n+1)).1} := by
    change MeasurableSet ({x : ℕ → State × Action | (x 0).1 = s₀} ∩
      {x | ∀ n, 0 < P (x n) (x (n+1)).1})
    apply MeasurableSet.inter
    · exact (measurableSet_singleton s₀).preimage (measurable_pi_apply 0).fst
    · simp only [Set.setOf_forall]
      apply MeasurableSet.iInter
      intro n
      have hc : Measurable (fun x : ℕ → State × Action => (x n, x (n+1))) :=
        (measurable_pi_apply n).prodMk (measurable_pi_apply (n+1))
      exact (Set.toFinite {z : (State × Action) × (State × Action) | 0 < P z.1 z.2.1}).measurableSet.preimage hc
  apply actionLaw_ae_of_stack (pairPolicy s₀ π) (pairPolicy_measurable s₀ π hπ) ρ P hP hN d _ hMeas
  filter_upwards [seeded_all_tapes_supported ρ P hP hN] with z hSupported
  refine ⟨?_, ?_⟩
  · simp [stackActionTrajectory, stackHistoryTrajectory, observedHistory, pairPolicy, currentState]
  · intro n
    rw [stack_pair_source_next]
    exact hSupported _ _

/-- Normalized rational-row specialization on the actual complete observed-history
law already used by the killed-law and residual-seed bridges. -/
theorem markov_recurrent_end_component
    (P : RationalKernel Model (State × Action) State) (θ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (hπ : Measurable (fun z : R × History Action State => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : State × Action) :
    ∀ᵐ H ∂markovHistoryLaw P θ s₀ π ρ,
      IsEndComponent Prod.fst (supportSuccessors (realRows P θ))
        (recurrentSet (historyAction d H)) := by
  have h := canonical_markov_recurrent_end_component s₀ π hπ ρ (realRows P θ)
    (realRows_nonnegative P θ) (realRows_normalized P θ) d
  exact ae_of_ae_map (historyAction_measurable d).aemeasurable h

end HiddenParity.Adaptive
