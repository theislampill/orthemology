import EventualCycling

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
universe u v w
variable {State Action : Type u} {R : Type v} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Every true-positive successor of a recurrent selected pair recurs on the
actual path, for an arbitrary policy consuming recurrent raw row tapes. -/
theorem stack_positive_successors_recur
    (P : RationalKernel Model (State × Action) State) (σ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (z : R × FlatStack (State × Action) State)
    (hTape : ∀ e y, 0 < realRows P σ e y → ∃ᶠ k in atTop, z.2 (e,k) = y) :
    ∀ e ∈ recurrentSet (stackActionTrajectory (pairPolicy s₀ π) z), ∀ y, 0 < P.row σ e y →
      ∃ᶠ n in atTop, stackActionTrajectory (pairPolicy s₀ π) z n = e ∧
        (stackActionTrajectory (pairPolicy s₀ π) z (n+1)).1 = y := by
  intro e he y hy
  have hAct := (mem_recurrentSet _ e).mp he
  have hPos : 0 < realRows P σ e y := by
    change (0 : ℝ) < (P.row σ e y : ℝ)
    exact_mod_cast hy
  have hBoth := recurrent_action_observes_recurrent_symbol (pairPolicy s₀ π) z e y hAct (hTape e y hPos)
  exact hBoth.mono (fun n hn => ⟨hn.1,by simpa only [stack_pair_source_next] using hn.2⟩)

/-- Pointwise recurrent-component regularity extracted directly from actual raw
support and recurrence. It is available for the generated switching controller. -/
theorem stack_actual_recurrent_component
    (P : RationalKernel Model (State × Action) State) (σ : Model)
    (s₀ : State) (π : R → History Action State → Action)
    (z : R × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < realRows P σ e (z.2 (e,k)))
    (hTape : ∀ e y, 0 < realRows P σ e y → ∃ᶠ k in atTop, z.2 (e,k) = y) :
    IsEndComponent Prod.fst (supportSuccessors (realRows P σ))
      (recurrentSet (stackActionTrajectory (pairPolicy s₀ π) z)) := by
  let x := stackActionTrajectory (pairPolicy s₀ π) z
  apply recurrent_pairs_form_end_component Prod.fst (supportSuccessors (realRows P σ)) x
  · intro n
    simp only [supportSuccessors,Finset.mem_filter,Finset.mem_univ,true_and]
    rw [stack_pair_source_next]
    exact hSupported _ _
  · intro e he y hy
    apply stack_positive_successors_recur P σ s₀ π z hTape e he y
    have hh := (Finset.mem_filter.mp hy).2
    change (0 : ℝ) < (P.row σ e y : ℝ) at hh
    exact_mod_cast hh

/-- Supported raw feedback retains the true model in every exact observed live
support. This handles arbitrary changes of policy mode. -/
theorem stack_true_model_survives
    (P : RationalKernel Model (State × Action) State) (B₀ : Finset Model) (σ : Model) (hσ : σ ∈ B₀)
    (s₀ : State) (π : R → History Action State → Action)
    (z : R × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < realRows P σ e (z.2 (e,k))) :
    ∀ n, σ ∈ liveHistory P B₀ (stackHistoryTrajectory (pairPolicy s₀ π) z n) := by
  intro n
  induction n with
  | zero => simpa only [stackHistoryTrajectory,observedHistory,liveHistory_nil] using hσ
  | succ n ih =>
      rw [stack_history_succ,liveHistory_cons]
      apply (mem_liveUpdate P _ _ _ σ).mpr
      refine ⟨ih,?_⟩
      have hPos := hSupported (stackActionTrajectory (pairPolicy s₀ π) z n)
        (countBefore (pairPolicy s₀ π) z (stackActionTrajectory (pairPolicy s₀ π) z n) n)
      change (0 : ℝ) < (P.row σ (stackActionTrajectory (pairPolicy s₀ π) z n)
        (stackReceipt (pairPolicy s₀ π) z n) : ℝ) at hPos
      exact_mod_cast hPos

/-- Any decreasing sequence of finite supports eventually becomes constant. -/
theorem finite_support_stabilizes {M : Type*} [DecidableEq M] (B : ℕ → Finset M)
    (hB : ∀ n, B (n+1) ⊆ B n) : ∃ C, ∀ᶠ n in atTop, B n = C := by
  classical
  have hAnti : Antitone B := antitone_nat_of_succ_le hB
  have hex : ∃ k, ∃ n, (B n).card = k := ⟨(B 0).card,0,rfl⟩
  obtain ⟨N,hN⟩ := Nat.find_spec hex
  refine ⟨B N,eventually_atTop.mpr ⟨N,?_⟩⟩
  intro n hn
  have hSub := hAnti hn
  apply Finset.eq_of_subset_of_card_le hSub
  by_contra hNot
  have hLt : (B n).card < Nat.find hex := by omega
  exact Nat.find_min hex hLt ⟨n,rfl⟩

theorem stack_liveSupport_stabilizes
    (P : RationalKernel Model (State × Action) State) (B₀ : Finset Model)
    (s₀ : State) (π : R → History Action State → Action)
    (z : R × FlatStack (State × Action) State) :
    ∃ C, ∀ᶠ n in atTop, liveHistory P B₀ (stackHistoryTrajectory (pairPolicy s₀ π) z n) = C := by
  apply finite_support_stabilizes
  intro n
  rw [stack_history_succ,liveHistory_cons]
  exact Finset.filter_subset _ _

end HiddenParity.Sufficiency
