import FullControllerSource
import HistorySamplingSemantics

namespace Orthemology.RuntimeBridge.PhaseUpdate.FullController
open P02A2.ObserverCore P02A2.PRProgram P02.Codec
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.CertifiedObserver

/-- Actual decoded explicit-stack evaluation of the entire phase-policy source.
Unlike the callable components, this is the arity-one acquired-history program. -/
theorem actual_policy_call (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) :
    ∃ fuel, callFuel fuel (programIndex (pack (policyProgram c))) ![encodeHistory h] =
      some (bitNat (policy c menu priority h)) := by
  obtain ⟨fuel,hf⟩ := callFuel_complete (policyProgram c) ![encodeHistory h]
  exact ⟨fuel,by simpa only [policy_program_retained_exact c menu priority hc h] using hf⟩

/-- Explicit acquired-history dynamics for the existing two-model rational
fixture environment. Its common policy is now the complete retained controller. -/
noncomputable def retainedStep (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (σ : Bool) (q : HistoryConfig) (b : Bool) : HistoryConfig :=
  if q.2.val = 0 then (q.1,if b then 2 else 1)
  else if proposalAt q.2 b ≤ 2 then
    ((policy c menu priority q.1,receiptAt σ (policy c menu priority q.1) q.2 b)::q.1,0)
  else (q.1,0)

noncomputable def retainedObservation (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (σ : Bool) (q : HistoryConfig) (b : Bool) : Fin 4 → Bool :=
  let accepted := decide (q.2.val ≠ 0 ∧ proposalAt q.2 b ≤ 2)
  ![accepted,HiddenParity.Sufficiency.observedState c.initialState q.1,policy c menu priority q.1,
    accepted && receiptAt σ (policy c menu priority q.1) q.2 b]

theorem retained_step_binding (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority) (σ : Bool) :
    historyStep σ (sourcePolicy c) = retainedStep c menu priority σ := by
  funext q b
  simp only [historyStep,retainedStep,historyPolicy,source_policy_retained_exact c menu priority hc]

theorem retained_observation_binding (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (hinit : c.initialState = false) (σ : Bool) :
    historyObservation σ (sourcePolicy c) = retainedObservation c menu priority σ := by
  funext q b
  simp only [historyObservation,retainedObservation,historyPolicy,
    source_policy_retained_exact c menu priority hc,hinit]

/-- Complete same-tape physical-frame identity, from actual decoded numeric P02
and scheduled stack execution to the retained phase/support/target/statistic
controller. Only finite selector/rational coefficient certificates are supplied.
The environment is the existing 1/3-versus-2/3 fixture, not a general row compiler. -/
theorem runtime_retained_history_frames (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (hinit : c.initialState = false) (σ : Bool) (x : Cantor) (n : ℕ) (j : Fin 4) :
    Indexed.runtimeOutput (runtimeIndex (policyProgram c) σ) x (4*n+j) =
      retainedObservation c menu priority σ
        (state (coreMachine (retainedStep c menu priority σ)) ([],0) (decimateFour x) n) (x (4*n)) j := by
  rw [runtime_observed_history_frames (policyProgram c) (sourcePolicy c) (policy_program_implements c),
    retained_step_binding c menu priority hc,retained_observation_binding c menu priority hc hinit]

end Orthemology.RuntimeBridge.PhaseUpdate.FullController
