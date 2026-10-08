import SelectorSemanticTransport
import ExactRuntimeCounterexample
set_option autoImplicit false

namespace Orthemology.Ninth.SelectorTransport.Reviewer
open HiddenParity HiddenParity.Sufficiency
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge.PhaseUpdate
open Orthemology.RuntimeBridge.PhaseUpdate.FullController
open Orthemology.RuntimeBridge.HistoryRuntime
open Orthemology.RationalLaw.CanonicalBinding
open Orthemology.RationalLaw.RuntimeBinding
open Orthemology.CertifiedObserver
open Orthemology.Frontier.MealyMeasure
open Orthemology.Ninth.SelectorExtraction
open P02A2.ObserverCore P02A2.PRProgram
open MeasureTheory
open Orthemology.Eighth.SemanticControls
open P02A2.Q8Measure (fairCantor)

/-- The stores used in the domain theorem belong to this exact source syntax. -/
theorem raw_program_boundary_syntax (c : Config) :
    rawPolicyProgram c =
      (⟨.seq (call HistoryFold.reverseProgram 22 HistoryFold.reverseArgs 1)
        (.seq (initialStmt c)
          (.seq (.loop 2 (.reg 0) (HistoryFold.foldBody (controllerStep c)))
            (call (actionProgram c) 22 (HistoryFold.dataArgs 18) 21))),21⟩ : Program 1) := rfl

/-- Register 2 is written immediately before precisely the body entry under review. -/
theorem actual_loop_successor_entry (c : Config) (h : HistoryFold.History) (n : ℕ) :
    runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 (n+1) (foldStart c h) =
      exec (HistoryFold.foldBody (controllerStep c))
        (Function.update (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n
          (foldStart c h)) 2 n) := rfl

/-- Every real collect prefix preserves the whole argument vector, not just its bounds. -/
theorem actual_prefix_argument_identity (c : Config) (σ : Store) (k : ℕ) :
    (fun j => evalExpr (HistoryFold.stepArgs 18 j)
      (exec (HistoryFold.collect (nextPrograms c) (HistoryFold.stepArgs 18)
        ((List.finRange 18).take k)) σ)) =
      (fun j => evalExpr (HistoryFold.stepArgs 18 j) σ) := by
  have hn : ((List.finRange 18).take k).Nodup :=
    List.Nodup.sublist (List.take_sublist k _) (List.nodup_finRange 18)
  have hp := (HistoryFold.collect_correct (nextPrograms c) (HistoryFold.stepArgs 18)
    (HistoryFold.step_args_fresh 18) _ hn σ).1
  funext j
  apply P02A2.LoopRenaming.evalExpr_congr
  intro r hr
  exact hp r (HistoryFold.step_args_fresh 18 j r hr)

/-- All 18 actual component entries, including the LOOP write, are bounded. -/
theorem actual_prefix_numeric_bounds (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (h : HistoryFold.History) (n k : ℕ)
    (e : Bool × Bool) (remaining : HistoryFold.History)
    (hr : ((HistoryFold.consume^[n]) (h.reverse,[])).1 = e::remaining) :
    let σ := exec (HistoryFold.collect (nextPrograms c) (HistoryFold.stepArgs 18)
      ((List.finRange 18).take k))
      (Function.update (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n
        (foldStart c h)) 2 n)
    evalExpr (HistoryFold.stepArgs 18 2) σ < 4 ∧
    evalExpr (HistoryFold.stepArgs 18 3) σ < 2 ∧
    evalExpr (HistoryFold.stepArgs 18 1) σ ≤ 16 ∧
    evalExpr (HistoryFold.stepArgs 18 18) σ < 2 ∧
    evalExpr (HistoryFold.stepArgs 18 19) σ < 2 :=
  actual_ordered_component_domain c menu priority hc h n e remaining hr k

theorem padding_after_clock_update_is_skip (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (h : HistoryFold.History) (n : ℕ) (hn : h.length ≤ n) :
    let σ := Function.update
      (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h)) 2 n
    exec (HistoryFold.foldBody (controllerStep c)) σ = σ :=
  actual_body_entry_padding_noop c menu priority hc h n hn

/-- No tolerance or environment parameter is normalized along with table representation. -/
theorem nonselector_fields_preserved (c : Config) :
    (normalizeConfig c).kernel = c.kernel ∧
    (normalizeConfig c).toleranceNumerator = c.toleranceNumerator ∧
    (normalizeConfig c).toleranceDenominator = c.toleranceDenominator ∧
    (normalizeConfig c).rowDenominator = c.rowDenominator ∧
    (normalizeConfig c).rowNumerator = c.rowNumerator ∧
    (normalizeConfig c).initialSupport = c.initialSupport ∧
    (normalizeConfig c).initialState = c.initialState ∧
    (normalizeConfig c).fallbackModel = c.fallbackModel ∧
    (normalizeConfig c).fallbackAction = c.fallbackAction :=
  ⟨rfl,rfl,rfl,rfl,rfl,rfl,rfl,rfl,rfl⟩

theorem normalized_selectors_are_bounded (c : Config) :
    BoundedData (normalizeConfig c).selectors := normalizeData_bounded c.selectors

/-- This equality is pointwise at arbitrary coordinates on every input tape. -/
theorem all_tape_all_coordinate_output (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (σ : Bool) (x : Cantor) (k : ℕ) :
    Indexed.runtimeOutput (runtimeIndex (policyProgram (normalizeConfig c)) σ) x k =
      Indexed.runtimeOutput (runtimeIndex (policyProgram c) σ) x k :=
  congrFun (congrFun (normalized_runtime_output c menu priority hc σ) x) k

/-- The all-tape claim includes an explicit forever-rejection tape. -/
theorem all_one_output_preserved (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (σ : Bool) (k : ℕ) :
    Indexed.runtimeOutput (runtimeIndex (policyProgram (normalizeConfig c)) σ) (fun _ => true) k =
      Indexed.runtimeOutput (runtimeIndex (policyProgram c) σ) (fun _ => true) k :=
  all_tape_all_coordinate_output c menu priority hc σ (fun _ => true) k

theorem physical_output_law_under_every_input_measure (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (σ : Bool) (μ : Measure Cantor) :
    μ.map (Indexed.runtimeOutput (runtimeIndex (policyProgram (normalizeConfig c)) σ)) =
      μ.map (Indexed.runtimeOutput (runtimeIndex (policyProgram c) σ)) := by
  rw [normalized_runtime_output c menu priority hc σ]

/-- Report extraction remains equal even where report completion fails. -/
theorem proposals_preserved_on_every_tape (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (σ : Bool) :
    runtimeProposal (policyProgram (normalizeConfig c)) σ = runtimeProposal (policyProgram c) σ := by
  unfold runtimeProposal
  rw [normalized_runtime_output c menu priority hc σ]

theorem total_receipt_decoder_preserved (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (σ : Bool) :
    runtimeReceiptPath (policyProgram (normalizeConfig c)) σ = runtimeReceiptPath (policyProgram c) σ := by
  unfold runtimeReceiptPath
  rw [proposals_preserved_on_every_tape c menu priority hc σ]

/-- Independent exact-type control with different execution and decoder certificates. -/
theorem two_configuration_mixed_readout (executed decoder : Config)
    (em dm : Finset Bool → Bool → Finset Bool) (ep dp : Bool → (Bool × Bool) → ℕ)
    (he : Certificate executed em ep) (hd : Certificate decoder dm dp) (σ : Bool) :
    decodedHistory (policyProgram (normalizeConfig executed)) (sourcePolicy (normalizeConfig decoder)) σ =
      decodedHistory (policyProgram executed) (sourcePolicy decoder) σ :=
  normalized_mixed_decodedHistory executed decoder em dm ep dp he hd σ

/-- Actual measure values, not only positivity, are unchanged for the exact mixed failure event. -/
theorem old_computed_failure_measure_exact (c : Config)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate c menu priority) (σ : Bool) (d : Bool × Bool) (μ : Measure Cantor) :
    μ {x : Cantor | ¬ HiddenParity.Stochastic.ParitySuccess (priority σ) (historyAction d
      (decodedHistory (policyProgram (normalizeConfig c))
        (sourcePolicy (withComputedTolerance (normalizeConfig c))) σ x))} =
    μ {x : Cantor | ¬ HiddenParity.Stochastic.ParitySuccess (priority σ) (historyAction d
      (decodedHistory (policyProgram c) (sourcePolicy (withComputedTolerance c)) σ x))} := by
  rw [normalized_old_computed_failure_event c menu priority hc σ d]

/-- Existing positive-measure mixed failure genuinely transports through A2. -/
theorem normalized_inherited_mixed_positive_failure (d : Bool × Bool) :
    0 < fairCantor {x : Cantor | ¬ HiddenParity.Stochastic.ParitySuccess
      (actionPriority initialCandidate) (historyAction d
        (decodedHistory (policyProgram (normalizeConfig oldConfig))
          (sourcePolicy (withComputedTolerance (normalizeConfig oldConfig))) initialCandidate x))} :=
  (normalized_old_computed_positive_failure_iff oldConfig bothMenu actionPriority
    oldConfig_certificate initialCandidate d fairCantor).mpr (exact_runtime_mutant_positive_failure d)

/-- Matching computed execution and decoder retain the inherited positive control. -/
theorem normalized_matching_positive_control (d : Bool × Bool) :
    ∀ᵐ x ∂fairCantor, HiddenParity.Stochastic.ParitySuccess (actionPriority initialCandidate)
      (historyAction d (decodedHistory (policyProgram (withComputedTolerance (normalizeConfig oldConfig)))
        (sourcePolicy (withComputedTolerance (normalizeConfig oldConfig))) initialCandidate x)) := by
  rw [normalizeConfig_computed_commute]
  rw [normalized_mixed_decodedHistory (withComputedTolerance oldConfig) (withComputedTolerance oldConfig)
    bothMenu bothMenu actionPriority actionPriority
    (computed_tolerance_certificate oldConfig bothMenu actionPriority oldConfig_certificate)
    (computed_tolerance_certificate oldConfig bothMenu actionPriority oldConfig_certificate) initialCandidate]
  exact exact_runtime_positive_control d

/-- A2 does not collapse the failed mixed readout into the successful matching one. -/
theorem normalized_mixed_not_matching :
    decodedHistory (policyProgram (normalizeConfig oldConfig))
      (sourcePolicy (withComputedTolerance (normalizeConfig oldConfig))) initialCandidate ≠
    decodedHistory (policyProgram (withComputedTolerance (normalizeConfig oldConfig)))
      (sourcePolicy (withComputedTolerance (normalizeConfig oldConfig))) initialCandidate := by
  intro h
  have hp := normalized_inherited_mixed_positive_failure (false,false)
  rw [h] at hp
  exact hp.ne' (ae_iff.mp (normalized_matching_positive_control (false,false)))

#print axioms normalized_inherited_mixed_positive_failure
#print axioms normalized_matching_positive_control
#print axioms normalized_mixed_not_matching
#print axioms raw_program_boundary_syntax
#print axioms actual_loop_successor_entry
#print axioms actual_prefix_argument_identity
#print axioms actual_prefix_numeric_bounds
#print axioms padding_after_clock_update_is_skip
#print axioms nonselector_fields_preserved
#print axioms normalized_selectors_are_bounded
#print axioms all_tape_all_coordinate_output
#print axioms all_one_output_preserved
#print axioms physical_output_law_under_every_input_measure
#print axioms proposals_preserved_on_every_tape
#print axioms total_receipt_decoder_preserved
#print axioms two_configuration_mixed_readout
#print axioms old_computed_failure_measure_exact
end Orthemology.Ninth.SelectorTransport.Reviewer
