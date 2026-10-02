import AELicensedEquivalence
noncomputable section
namespace IndependentAELicensingControls
open Orthemology.Tranche2 Orthemology.Tranche3 PolicyEmbedding
open MeasureTheory Filter Finset Orthemology.Tranche2.FiniteAlphabetQuery
open scoped ENNReal BigOperators

def fair (_ _a _y : Bool) : ℝ := 1/2
lemma nonneg : ∀ θ a y, 0≤fair θ a y := by intros; norm_num [fair]
lemma norm : ∀ θ a, ∑ y, fair θ a y=1 := by intros; norm_num [fair]
def seedPolicy (r : Bool) (_ : History Bool Bool) : Bool := r
lemma hm : Measurable (fun z : Bool × History Bool Bool => seedPolicy z.1 z.2) := measurable_fst

theorem null_seed_policy_is_ae_licensed :
    ∀ᵐ H ∂observedTraceLaw ∅ seedPolicy (Measure.dirac false)
      (fair false) (fair false) (nonneg false) (norm false) (nonneg false) (norm false),
      LicensedHistoryPath fair (fun _ => {false}) Finset.univ false H := by
  rw [observedTraceLaw_dirac_rows seedPolicy hm false]
  apply (ae_map_iff (rowHistory_measurable seedPolicy hm false).aemeasurable
    (measurableSet_licensedHistoryPath fair (fun _ => {false}) Finset.univ false)).mpr
  exact Filter.Eventually.of_forall (fun ω n => by simp [LicensedHistoryPath,historyAction,rowHistory,seedPolicy])

theorem original_null_seed_is_not_pointwise_safe :
    seedPolicy true [] ∉ ({false} : Finset Bool) := by decide

theorem null_seed_is_measure_zero : (Measure.dirac false : Measure Bool) {true}=0 := by simp

theorem acquired_history_is_positive :
    0 < iidOracle (rowMeasure (fair false) (nonneg false) (norm false))
      {ω | rowHistory seedPolicy false ω 1 = [(false,true)]} := by
  apply feasible_rowHistory_positive fair nonneg norm seedPolicy hm false Finset.univ
    [(false,true)] (by simp [ActionCompatible,seedPolicy]) false
  norm_num [historySupport,supportUpdate,fair]

theorem forged_action_is_incompatible :
    ¬ ActionCompatible seedPolicy false [(true,false)] := by simp [ActionCompatible,seedPolicy]

def reveal (θ _a y : Bool) : ℝ := if y=θ then 1 else 0

theorem acquired_feedback_changes_support :
    historySupport reveal Finset.univ [(false,false)] = {false} ∧
    historySupport reveal Finset.univ [(false,true)] = {true} := by
  constructor <;> ext θ <;> cases θ <;> norm_num [historySupport,supportUpdate,reveal]

def path (y : Bool) : ℕ → History Bool Bool
  | 0 => []
  | n+1 => List.replicate (n+1) (false,y)

theorem same_actions_do_not_determine_feedback (n : ℕ) :
    historyAction false (path false) n = historyAction false (path true) n := by
  simp [historyAction,path,List.replicate_succ]

theorem same_actions_have_different_live_support :
    historySupport reveal Finset.univ (path false 1) ≠
      historySupport reveal Finset.univ (path true 1) := by
  simp only [path,List.replicate_succ,List.replicate_zero]
  rw [acquired_feedback_changes_support.1,acquired_feedback_changes_support.2]
  decide

theorem license_reads_pre_action_support (H : ℕ → History Bool Bool) :
    LicensedHistoryPath reveal (fun B => if B={false} then {false} else {true}) Finset.univ false H ↔
      ∀ n, ((H (n+1)).headD (false,default)).1 ∈
        (if historySupport reveal Finset.univ (H n)={false} then ({false} : Finset Bool) else {true}) := by
  rfl
end IndependentAELicensingControls
