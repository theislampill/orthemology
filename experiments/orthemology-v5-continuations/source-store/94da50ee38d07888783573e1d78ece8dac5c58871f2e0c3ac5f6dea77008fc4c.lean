import RoundRobinPolicy

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- A nonempty closed subset of a strongly connected component which includes
every retained action at its used states is the entire component. -/
theorem fair_closed_subset_eq (succ : (State × Action) → Finset State)
    (C E : Finset (State × Action)) (hEC : IsEndComponent Prod.fst succ E)
    (hC : C.Nonempty) (hCE : C ⊆ E)
    (hClosed : ∀ e ∈ C, succ e ⊆ usedStates Prod.fst C)
    (hFair : ∀ e ∈ E, e.1 ∈ usedStates Prod.fst C → e ∈ C) : C = E := by
  apply Finset.Subset.antisymm hCE
  obtain ⟨f,hf⟩ := hC
  have hfC : f.1 ∈ usedStates Prod.fst C := Finset.mem_image.mpr ⟨f,hf,rfl⟩
  intro e he
  apply hFair e he
  have hPath := hEC.connected f.1 (Finset.mem_image.mpr ⟨f,hCE hf,rfl⟩)
    e.1 (Finset.mem_image.mpr ⟨e,he,rfl⟩)
  have propagate : ∀ t, Reach Prod.fst succ E f.1 t → t ∈ usedStates Prod.fst C := by
    intro t ht
    induction ht with
    | refl => exact hfC
    | @tail y z hPath hyz ih =>
        obtain ⟨g,hg,hgy,hz⟩ := hyz
        exact hClosed g (hFair g hg (by simpa [hgy] using ih)) hz
  exact propagate e.1 hPath

/-- Actual supported feedback keeps the deterministic cycling policy in a
closed retained component from every retained observed initial state. -/
theorem stack_roundRobin_retained (E : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (hs₀ : s₀ ∈ usedStates Prod.fst E) (P : (State × Action) → State → ℝ)
    (hClosed : ∀ e ∈ E, ∀ y, 0 < P e y → y ∈ usedStates Prod.fst E)
    (z : R × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < P e (z.2 (e,k))) :
    ∀ n, stackActionTrajectory (pairPolicy s₀ (roundRobinPolicy E fallback s₀)) z n ∈ E := by
  intro n
  induction n with
  | zero =>
      exact roundRobin_pair_mem E fallback s₀ z.1 [] hs₀
  | succ n ih =>
      apply roundRobin_pair_mem E fallback s₀ z.1
      change (stackActionTrajectory (pairPolicy s₀ (roundRobinPolicy E fallback s₀)) z (n+1)).1 ∈ _
      rw [stack_pair_source_next]
      exact hClosed _ ih _ (hSupported _ _)

/-- Every retained pair recurs almost surely under this explicit deterministic
observed-history policy. Fairness and transition recurrence are both derived. -/
theorem roundRobin_actionLaw_recurrent
    (E : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (hs₀ : s₀ ∈ usedStates Prod.fst E) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : (State × Action) → State → ℝ) (hP : ∀ e y, 0 ≤ P e y)
    (hN : ∀ e, ∑ y, P e y = 1)
    (hEC : IsEndComponent Prod.fst (supportSuccessors P) E) (d : State × Action) :
    ∀ᵐ x ∂actionLaw (pairPolicy s₀ (roundRobinPolicy E fallback s₀)) ρ P hP hN d,
      recurrentSet x = E := by
  let π : R → History Action State → Action := roundRobinPolicy E fallback s₀
  apply actionLaw_ae_of_stack (pairPolicy s₀ π)
    (pairPolicy_measurable s₀ π (roundRobinPolicy_measurable E fallback s₀)) ρ P hP hN d _
    (measurable_recurrent_predicate (fun C => C = E))
  filter_upwards [seeded_all_tapes_supported ρ P hP hN, seeded_all_tapes_recurrent ρ P hP hN]
    with z hSupported hTape
  let x := stackActionTrajectory (pairPolicy s₀ π) z
  have hRetained : ∀ n, x n ∈ E := stack_roundRobin_retained E fallback s₀ hs₀ P
    (fun e he y hy => hEC.closed e he (by simp [supportSuccessors,hy])) z hSupported
  have hStep : ∀ n, (x (n+1)).1 ∈ supportSuccessors P (x n) := by
    intro n
    simp only [supportSuccessors, Finset.mem_filter, Finset.mem_univ, true_and]
    rw [stack_pair_source_next]
    exact hSupported _ _
  have hC : IsEndComponent Prod.fst (supportSuccessors P) (recurrentSet x) := by
    apply recurrent_pairs_form_end_component Prod.fst (supportSuccessors P) x hStep
    intro e he y hy
    have hAct := (mem_recurrentSet x e).mp he
    have hRec := recurrent_action_observes_recurrent_symbol (pairPolicy s₀ π) z e y hAct
      (hTape e y (Finset.mem_filter.mp hy).2)
    exact hRec.mono (fun n hn => ⟨hn.1, by simpa only [x,stack_pair_source_next] using hn.2⟩)
  exact fair_closed_subset_eq (supportSuccessors P) (recurrentSet x) E hEC hC.nonempty
    (recurrentSet_subset_of_eventually_mem x E (Eventually.of_forall hRetained)) hC.closed
    (stack_roundRobin_fair E fallback s₀ z)

/-- The same conclusion is stated directly on the actual complete observed
Markov history law, with no auxiliary operating-kernel equality premise. -/
theorem roundRobin_markov_recurrent
    (P : RationalKernel Model (State × Action) State) (θ : Model)
    (E : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (hs₀ : s₀ ∈ usedStates Prod.fst E) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (hEC : IsEndComponent Prod.fst (supportSuccessors (realRows P θ)) E) (d : State × Action) :
    ∀ᵐ H ∂markovHistoryLaw P θ s₀ (roundRobinPolicy E fallback s₀) ρ,
      recurrentSet (historyAction d H) = E := by
  have h := roundRobin_actionLaw_recurrent E fallback s₀ hs₀ ρ (realRows P θ)
    (realRows_nonnegative P θ) (realRows_normalized P θ) hEC d
  exact ae_of_ae_map (historyAction_measurable d).aemeasurable h

end HiddenParity.Sufficiency
