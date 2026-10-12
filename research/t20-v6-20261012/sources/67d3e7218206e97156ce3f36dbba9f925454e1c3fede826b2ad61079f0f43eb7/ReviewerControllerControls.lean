import GlobalControllerControls

noncomputable section
namespace HiddenParity.IndependentController
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Sufficiency
open HiddenParity.Empirical HiddenParity.Sufficiency.ControllerControls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
abbrev T := Fin 2

def retainedZero : Finset (T × T) := {(0,0),(0,1)}
def memorySeven : PhaseMemory T T := ⟨7,some retainedZero⟩

theorem support_change_precedes_test :
    (advanceMemory (Finset.univ : Finset T) ({0} : Finset T) (1 : T) memorySeven true).index = 0 ∧
    (advanceMemory (Finset.univ : Finset T) ({0} : Finset T) (1 : T) memorySeven true).retained = none := by decide

theorem supported_component_exit_increments :
    (advanceMemory (Finset.univ : Finset T) Finset.univ (1 : T) memorySeven false).index = 8 ∧
    (advanceMemory (Finset.univ : Finset T) Finset.univ (1 : T) memorySeven false).retained = none := by decide

theorem no_reject_retains_component :
    (advanceMemory (Finset.univ : Finset T) Finset.univ (0 : T) memorySeven false).index = 7 ∧
    (advanceMemory (Finset.univ : Finset T) Finset.univ (0 : T) memorySeven false).retained = some retainedZero := by decide

theorem positive_test_increments_before_normalization :
    (advanceMemory (Finset.univ : Finset T) Finset.univ (0 : T) memorySeven true).index = 8 ∧
    (advanceMemory (Finset.univ : Finset T) Finset.univ (0 : T) memorySeven true).retained = none := by decide

theorem reconstructed_sources_use_older_receipts :
    augmentHistory (0 : T) ([(1,0),(0,1)] : History T T) =
      [((1,1),0),((0,0),1)] := by decide

theorem acquired_frequency_is_pair_specific :
    historyFrequency ((0 : T),(0 : T)) (1 : T)
      [(((1 : T),(0 : T)),0),(((0 : T),(0 : T)),1)] = 1 := by
  norm_num [historyFrequency, historySymbolMass, symbolIndicator, actionCount]

/-- No unobserved cell or stale low-count deviation is inspected beyond the gate. -/
theorem phase_above_total_history_cannot_reject
    (P : RationalKernel T (T × T) T) (ε : ℝ) (θ : T) (k : Nat)
    (h : History (T × T) T) (hk : h.length ≤ k) : empiricalReject P ε θ k h = false := by
  by_contra hn
  have ht : empiricalReject P ε θ k h = true := by
    cases he : empiricalReject P ε θ k h <;> simp_all
  obtain ⟨e,y,hCount,hBad⟩ := (empiricalReject_iff P ε θ k h).mp ht
  have hb : actionCount e h ≤ h.length := List.countP_le_length
  omega

def surprisingHistory : History (T × T) T := [((0,0),1)]

theorem acquired_surprise_rejects_phase_zero :
    empiricalReject coinKernel (1/8) 0 0 surprisingHistory = true := by
  apply (empiricalReject_iff _ _ _ _ _).mpr
  refine ⟨(0,0),1,by decide,?_⟩
  norm_num [surprisingHistory,historyFrequency,historySymbolMass,symbolIndicator,actionCount,
    realRows,coinKernel,quarter_value,threeQuarters_value]
  norm_num [abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 3/4)]

theorem same_acquired_surprise_stale_at_phase_one :
    empiricalReject coinKernel (1/8) 0 1 surprisingHistory = false :=
  phase_above_total_history_cannot_reject _ _ _ _ _ (by decide)

theorem empty_history_cannot_reject (θ : T) (k : Nat) :
    empiricalReject coinKernel (1/8) θ k [] = false :=
  phase_above_total_history_cannot_reject _ _ _ _ _ (Nat.zero_le _)

/-- Complete lawfulness survives even deliberately adversarial false-positive tests. -/
theorem arbitrary_test_false_positives_preserve_lawfulness :
    Lawful coinKernel menu Finset.univ 0
      (generatedPhasePolicy coinKernel menu oppositePriority Finset.univ 0 0 0
        (fun _ _ _ => true)) (Measure.dirac ()) := by
  apply generatedPhasePolicy_lawful
  rw [coin_full_region]
  exact Finset.mem_univ _

/-- The returned common witness binds both models to one actual history policy. -/
theorem actual_coin_common_success :
    ∀ σ ∈ (Finset.univ : Finset T), ∀ᵐ H ∂markovHistoryLaw coinKernel σ 0
      coinCommonWinningPolicy.policy coinCommonWinningPolicy.seedLaw,
      ParitySuccess (oppositePriority σ) (historyAction (0,0) H) :=
  coinCommonWinningPolicy.parity

theorem actual_coin_common_lawful :
    Lawful coinKernel menu Finset.univ 0 coinCommonWinningPolicy.policy coinCommonWinningPolicy.seedLaw :=
  coinCommonWinningPolicy.lawful

abbrev One := Fin 1

def deterministicKernel : RationalKernel One (One × One) One where
  row := fun _ _ _ => 1
  nonnegative := by intros; norm_num
  normalized := by intros; simp

def deterministicMenu (_ : Finset One) (_ : One) : Finset One := Finset.univ

def afterFirstReceipt (_ : One) (_ : Nat) (h : History (One × One) One) : Bool :=
  decide (h ≠ [])

/-- The first observed receipt is tested before the next phase is selected. -/
theorem actual_memory_tests_post_receipt_history :
    (phaseMemory deterministicKernel deterministicMenu (fun _ _ => 2)
      Finset.univ 0 0 afterFirstReceipt ([(0,0)] : History One One)).index = 1 := by
  simp [phaseMemory,advanceMemory,liveHistory,augmentHistory,observedState,
    deterministicKernel,afterFirstReceipt]

theorem same_test_before_first_receipt_is_false :
    afterFirstReceipt 0 0 [] = false := by decide

end HiddenParity.IndependentController
