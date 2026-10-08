import GeneratedRun
import MemoryTransitions

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport

namespace HiddenParity.Sufficiency
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]
variable (P : RationalKernel Model (State × Action) State)
variable (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
variable (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
variable (reject : Model → ℕ → History (State × Action) State → Bool)
local notation "π" => generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject
local notation "H" => runHistory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "x" => runAction P menu priority B₀ s₀ fallback fallbackAction reject
local notation "b" => runSupport P menu priority B₀ s₀ fallback fallbackAction reject
local notation "m" => runMemory P menu priority B₀ s₀ fallback fallbackAction reject

theorem runAction_mem_active (hs₀ : s₀ ∈ winningRegion P menu priority B₀)
    (σ : Model) (hσ : σ ∈ B₀) (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < realRows P σ e (z.2 (e,k))) (n : ℕ) :
    x z n ∈ activePairs P menu priority (b z n) (m z n) := by
  have hInv := run_invariant P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported n
  have hActive := valid_activePairs P menu priority fallback (b z n) ⟨σ,hInv.1⟩ _ hInv.2.1 _ hInv.2.2
  have hMem := cycleAction_mem (retainedActions (activePairs P menu priority (b z n) (m z n)) (x z n).1)
    fallbackAction (retainedActions_nonempty _ _ hActive.2)
    (visitsBefore (fun k => (x z k).1) (x z n).1 n)
  have hh := (mem_retainedActions _ _ _).mp hMem
  rw [← runAction_cycle P menu priority B₀ s₀ fallback fallbackAction reject z n] at hh
  exact hh

theorem run_phase_increment_cases (z : Unit × FlatStack (State × Action) State) (n : ℕ)
    (hStable : b z (n+1) = b z n) :
    (m z (n+1)).index = (m z n).index ∨ (m z (n+1)).index = (m z n).index+1 := by
  rw [runMemory_succ,normalizeMemory_index,hStable]
  exact advanceMemory_index_cases _ _ _ _

theorem run_constant_phase_test_false (z : Unit × FlatStack (State × Action) State) (n : ℕ)
    (hStable : b z (n+1) = b z n) (hIndex : (m z (n+1)).index = (m z n).index) :
    reject (phaseCandidate (b z n) fallback (m z n)) (m z n).index (H z (n+1)) = false := by
  rw [runMemory_succ,normalizeMemory_index,hStable] at hIndex
  by_contra hNot
  have ht : reject (phaseCandidate (b z n) fallback (m z n)) (m z n).index (H z (n+1)) = true := by
    cases he : reject (phaseCandidate (b z n) fallback (m z n)) (m z n).index (H z (n+1)) <;> simp_all
  rw [ht,advanceMemory_reject_index] at hIndex
  omega

theorem run_constant_phase_mode_persists (z : Unit × FlatStack (State × Action) State) (n : ℕ)
    (hStable : b z (n+1) = b z n) (hIndex : (m z (n+1)).index = (m z n).index)
    (E : Finset (State × Action)) (he : (m z n).retained = some E) :
    (m z (n+1)).retained = some E := by
  have hi := hIndex
  rw [runMemory_succ,normalizeMemory_index,hStable] at hi
  have hAdvance := advanceMemory_equal_index_retained _ _ _ _ hi
  rw [runMemory_succ,hStable,hAdvance,normalizeMemory_some P menu priority fallback _ _ _ E he]
  exact he

/-- In a true-candidate phase with a negative row test, actual supported feedback
cannot trigger the component-exit guard. Therefore its phase index freezes. -/
theorem run_true_candidate_no_increment (hs₀ : s₀ ∈ winningRegion P menu priority B₀)
    (σ : Model) (hσ : σ ∈ B₀) (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < realRows P σ e (z.2 (e,k))) (n : ℕ)
    (hStable : b z (n+1) = b z n)
    (hCandidate : phaseCandidate (b z n) fallback (m z n) = σ)
    (hTest : reject σ (m z n).index (H z (n+1)) = false) :
    (m z (n+1)).index = (m z n).index := by
  have hInv := run_invariant P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported n
  have hChosen := runAction_mem_active P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported n
  have hStay : ∀ E, (m z n).retained = some E → (x z (n+1)).1 ∈ usedStates Prod.fst E := by
    intro E he
    have hQ := (hInv.2.2 E he).1
    rw [hCandidate] at hQ
    have hXE : x z n ∈ E := by simpa only [activePairs,he,Option.getD_some] using hChosen
    have hp : 0 < P.row σ (x z n) (x z (n+1)).1 := by
      have hr := hSupported (x z n) (countBefore (pairPolicy s₀ π) z (x z n) n)
      change (0 : ℝ) < (P.row σ (x z n) (stackReceipt (pairPolicy s₀ π) z n) : ℝ) at hr
      rw [show (x z (n+1)).1 = stackReceipt (pairPolicy s₀ π) z n from stack_pair_source_next s₀ π z n]
      exact_mod_cast hr
    exact hQ.2.2.1.closed _ hXE (hQ.2.1 _ hXE _ hp)
  rw [runMemory_succ,normalizeMemory_index,hStable,hCandidate,hTest,advanceMemory_no_reject _ _ _ hStay]

end HiddenParity.Sufficiency
