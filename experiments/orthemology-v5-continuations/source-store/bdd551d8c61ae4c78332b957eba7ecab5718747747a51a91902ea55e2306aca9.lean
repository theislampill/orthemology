import GeneratedPolicySafety
import StackPathRegularity

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

def runHistory (z : Unit × FlatStack (State × Action) State) : ℕ → History (State × Action) State :=
  stackHistoryTrajectory (pairPolicy s₀ π) z

def runAction (z : Unit × FlatStack (State × Action) State) : ℕ → State × Action :=
  stackActionTrajectory (pairPolicy s₀ π) z

def runSupport (z : Unit × FlatStack (State × Action) State) (n : ℕ) : Finset Model :=
  liveHistory P B₀ (runHistory P menu priority B₀ s₀ fallback fallbackAction reject z n)

def runMemory (z : Unit × FlatStack (State × Action) State) (n : ℕ) : PhaseMemory State Action :=
  currentMemory P menu priority B₀ s₀ fallback reject
    (erasePairSources (runHistory P menu priority B₀ s₀ fallback fallbackAction reject z n))

local notation "H" => runHistory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "x" => runAction P menu priority B₀ s₀ fallback fallbackAction reject
local notation "b" => runSupport P menu priority B₀ s₀ fallback fallbackAction reject
local notation "m" => runMemory P menu priority B₀ s₀ fallback fallbackAction reject

theorem runHistory_augment (z : Unit × FlatStack (State × Action) State) (n : ℕ) :
    augmentHistory s₀ (erasePairSources (H z n)) = H z n :=
  augmentHistory_compatible s₀ π z.1 _ (stack_history_compatible (pairPolicy s₀ π) z n)

theorem runAction_source (z : Unit × FlatStack (State × Action) State) (n : ℕ) :
    (x z n).1 = currentState s₀ (H z n) := rfl

theorem runSupport_succ (z : Unit × FlatStack (State × Action) State) (n : ℕ) :
    b z (n+1) = liveUpdate P (b z n) (x z n) (x z (n+1)).1 := by
  unfold runSupport runHistory
  rw [stack_history_succ,liveHistory_cons]
  rw [show (x z (n+1)).1 = stackReceipt (pairPolicy s₀ π) z n from stack_pair_source_next s₀ π z n]
  rfl

/-- The generated policy's actual action uses the global source-departure count. -/
theorem runAction_cycle (z : Unit × FlatStack (State × Action) State) (n : ℕ) :
    (x z n).2 = cycleAction (retainedActions (activePairs P menu priority (b z n) (m z n)) (x z n).1)
      fallbackAction (visitsBefore (fun k => (x z k).1) (x z n).1 n) := by
  have hc := stack_historyVisits s₀ (x z n).1 π z n
  change historyVisits s₀ (x z n).1 (erasePairSources (H z n)) =
    visitsBefore (fun k => (x z k).1) (x z n).1 n at hc
  rw [← hc]
  change generatedPhasePolicy P menu priority B₀ s₀ fallback fallbackAction reject z.1
    (erasePairSources (H z n)) = _
  simp only [generatedPhasePolicy,runHistory_augment,observedState_erase]
  rw [runAction_source]
  rfl

/-- Literal transition equation for actual controller memory, including both
row-test and component-exit guards before the next normalization. -/
theorem runMemory_succ (z : Unit × FlatStack (State × Action) State) (n : ℕ) :
    m z (n+1) = normalizeMemory P menu priority fallback (b z (n+1)) (x z (n+1)).1
      (advanceMemory (b z n) (b z (n+1)) (x z (n+1)).1 (m z n)
        (reject (phaseCandidate (b z n) fallback (m z n)) (m z n).index (H z (n+1)))) := by
  have hEr : erasePairSources (H z (n+1)) =
      ((x z n).2,(x z (n+1)).1)::erasePairSources (H z n) := by
    rw [show H z (n+1) = (x z n,stackReceipt (pairPolicy s₀ π) z n)::H z n from stack_history_succ _ z n]
    rw [show (x z (n+1)).1 = stackReceipt (pairPolicy s₀ π) z n from stack_pair_source_next s₀ π z n]
    rfl
  have hAugNew := runHistory_augment P menu priority B₀ s₀ fallback fallbackAction reject z (n+1)
  rw [hEr] at hAugNew
  change normalizeMemory P menu priority fallback
    (liveHistory P B₀ (augmentHistory s₀ (erasePairSources (H z (n+1)))))
    (observedState s₀ (erasePairSources (H z (n+1))))
    (phaseMemory P menu priority B₀ s₀ fallback reject (erasePairSources (H z (n+1)))) = _
  rw [runHistory_augment,observedState_erase,← runAction_source P menu priority B₀ s₀ fallback fallbackAction reject z (n+1)]
  congr 1
  rw [hEr,phaseMemory,hAugNew,runHistory_augment,observedState_erase]
  simp only [runMemory,currentMemory,runHistory_augment,observedState_erase]
  rfl

/-- Actual supported paths satisfy the full generated region/component invariant. -/
theorem run_invariant (hs₀ : s₀ ∈ winningRegion P menu priority B₀)
    (σ : Model) (hσ : σ ∈ B₀) (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < realRows P σ e (z.2 (e,k))) (n : ℕ) :
    σ ∈ b z n ∧ (x z n).1 ∈ winningRegion P menu priority (b z n) ∧
      MemoryValid P menu priority fallback (b z n) (x z n).1 (m z n) := by
  have hLive : σ ∈ b z n := stack_true_model_survives P B₀ σ hσ s₀ π z hSupported n
  have hc := stack_history_compatible (pairPolicy s₀ π) z n
  have hAug := runHistory_augment P menu priority B₀ s₀ fallback fallbackAction reject z n
  have hInv := generated_history_invariant P menu priority B₀ s₀ hs₀ fallback fallbackAction reject
    (erasePairSources (H z n)) (by simpa only [hAug] using (show (b z n).Nonempty from ⟨σ,hLive⟩))
    (by simpa only [hAug] using hc)
  refine ⟨hLive,?_,?_⟩
  · simpa only [hAug,observedState_erase] using hInv.1
  · have hRaw : MemoryValid P menu priority fallback (b z n) (currentState s₀ (H z n))
        (phaseMemory P menu priority B₀ s₀ fallback reject (erasePairSources (H z n))) := by
      simpa only [hAug,observedState_erase] using hInv.2
    change MemoryValid P menu priority fallback (b z n) (currentState s₀ (H z n))
      (currentMemory P menu priority B₀ s₀ fallback reject (erasePairSources (H z n)))
    unfold currentMemory
    rw [hAug,observedState_erase]
    exact normalizeMemory_valid P menu priority fallback _ _ _ hRaw

end HiddenParity.Sufficiency
