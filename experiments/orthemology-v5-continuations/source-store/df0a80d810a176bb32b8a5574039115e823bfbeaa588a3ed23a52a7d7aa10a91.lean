import GeneratedPhaseDynamics
import EmpiricalTestLaw
import PhaseStabilization

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
open HiddenParity.PhaseArithmetic
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]
variable (P : RationalKernel Model (State × Action) State)
variable (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
variable (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action) (ε : ℝ)
local notation "reject" => empiricalReject P ε
local notation "π" => generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject
local notation "H" => runHistory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "x" => runAction P menu priority B₀ s₀ fallback fallbackAction reject
local notation "b" => runSupport P menu priority B₀ s₀ fallback fallbackAction reject
local notation "m" => runMemory P menu priority B₀ s₀ fallback fallbackAction reject

/-- Actual finite support descent and the genuine gated true-row test derive
phase/mode stabilization for the generated controller. The row-test regularity
input is proved almost surely by EmpiricalTestLaw, not a termination premise. -/
theorem generated_phase_and_mode_stable
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < realRows P σ e (z.2 (e,k)))
    (hTrue : ∃ K : ℕ, ∀ k, K ≤ k → ∀ n, reject σ k (H z n) = false) :
    ∃ B : Finset Model, ∃ j : ℕ, σ ∈ B ∧ B ⊆ B₀ ∧
      (∀ᶠ n in atTop, b z n = B) ∧ (∀ᶠ n in atTop, (m z n).index = j) ∧
      ((∀ᶠ n in atTop, (m z n).retained = none) ∨
        ∃ E, ∀ᶠ n in atTop, (m z n).retained = some E) := by
  obtain ⟨B,hB⟩ := stack_liveSupport_stabilizes P B₀ s₀ π z
  obtain ⟨N,hN⟩ := eventually_atTop.mp hB
  have hMember := stack_true_model_survives P B₀ σ hσ s₀ π z hSupported N
  have hσB : σ ∈ B := by simpa only [hN N le_rfl] using hMember
  have hSub : B ⊆ B₀ := by
    rw [← hN N le_rfl]
    exact liveHistory_subset P B₀ _
  obtain ⟨K,hK⟩ := hTrue
  have hStep : ∀ n, N ≤ n → (m z (n+1)).index = (m z n).index ∨
      (m z (n+1)).index = (m z n).index+1 := by
    intro n hn
    apply run_phase_increment_cases P menu priority B₀ s₀ fallback fallbackAction reject z n
    exact (hN (n+1) (by omega)).trans (hN n hn).symm
  have hStop : ∀ n, N ≤ n → K ≤ (m z n).index → cycleAction B fallback (m z n).index = σ →
      (m z (n+1)).index = (m z n).index := by
    intro n hn hk hc
    apply run_true_candidate_no_increment P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported n
    · exact (hN (n+1) (by omega)).trans (hN n hn).symm
    · have hbn : b z n = B := hN n hn
      simpa only [phaseCandidate,hbn] using hc
    · exact hK _ hk (n+1)
  have hp := cycling_phase_eventually_constant (fun n => (m z n).index) N K B fallback σ hσB hStep hStop
  obtain ⟨j,hj,hMode⟩ := eventual_phase_and_mode_stable (fun n => (m z n).index)
    (fun n => (m z n).retained) N hp (by
      intro n hn hIndex E he
      apply run_constant_phase_mode_persists P menu priority B₀ s₀ fallback fallbackAction reject z n
        ((hN (n+1) (by omega)).trans (hN n hn).symm) hIndex E he)
  exact ⟨B,j,hσB,hSub,hB,hj,hMode⟩

end HiddenParity.Sufficiency
