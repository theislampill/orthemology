import SeededPolicyEquivalence

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2 Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.MicroPolicy
namespace MicroAudit
local instance : MeasurableSpace Bool := ⊤
local instance : MeasurableSingletonClass Bool := ⟨fun _ => trivial⟩

def plan (σ : Bool) : List Bool := if σ then [false] else [false,true]
def choose (h : History Bool Bool) : Bool := match h with | [] => false | (_,y)::_ => y
def fixed (_h : History Bool Bool) := false
def ones (_a : Bool) (_n : ℕ) := true
def changing (_a : Bool) (n : ℕ) : Bool := if n = 0 then false else true
lemma plan_nonempty (σ : Bool) : plan σ ≠ [] := by cases σ <;> simp [plan]

theorem initial_queue : queue plan choose [] = [false,true] := rfl

theorem no_premature_replan :
    choose ([(false,true)] : History Bool Bool) = true ∧
    queue plan choose [(false,true)] = [true] ∧
    plan (choose [(false,true)]) = [false] := by simp [choose,queue,plan]

theorem resets_after_final_observation :
    queue plan choose ([(true,true),(false,true)] : History Bool Bool) = [false] := by
  simp [queue,plan,choose]

theorem first_two_actions_execute_old_plan :
    microRun plan choose false ones [] 2 = [(true,true),(false,true)] := by
  simp [microRun,policy,queue,plan,choose,ones]

theorem variable_block_lengths :
    (macroHistory plan choose ones 1).length = 2 ∧
    (macroHistory plan choose ones 2).length = 3 := by
  simp [macroHistory,feed,plan,choose,ones]

theorem explicit_macro_micro_boundary :
    microRun plan choose false ones [] 3 = macroHistory plan choose ones 2 := by
  simp [microRun,policy,queue,plan,choose,ones,macroHistory,feed]

theorem fresh_indices_on_repeated_blocks :
    microRun plan fixed false changing [] 4 =
      [(true,true),(false,true),(true,false),(false,false)] := by
  norm_num [microRun,policy,queue,plan,fixed,changing,PolicyEmbedding.actionCount]

theorem list_multiplicity_count :
    actionCount false (feed changing ([] : History Bool Bool) [false,false,true]) = 2 := by
  norm_num [feed,changing,PolicyEmbedding.actionCount]

def p (a y : Bool) : ℝ := if a then (if y then 3/4 else 1/4) else (if y then 1/3 else 2/3)

theorem acquired_likelihood_exact :
    historyScore p (microRun plan fixed false changing [] 4) = 1/24 := by
  rw [fresh_indices_on_repeated_blocks]
  norm_num [historyScore,p]

theorem repeated_action_likelihood_exact :
    historyScore p (feed changing ([] : History Bool Bool) [false,false,true]) = 1/18 := by
  norm_num [feed,changing,PolicyEmbedding.actionCount,historyScore,p]

theorem physical_clock_is_not_block_clock :
    policy plan choose false () (microRun plan choose false ones [] 1) = true ∧
    policy plan choose false () (microRun plan choose false ones [] 2) = false := by
  simp [policy,microRun,queue,plan,choose,ones]

theorem fallback_unused {Θ A Y : Type*} [DecidableEq A]
    (as : Θ → List A) (pick : History A Y → Θ) (hn : ∀ σ, as σ ≠ [])
    (h : History A Y) (d e : A) : policy as pick d () h = policy as pick e () h := by
  have hq := queue_nonempty as pick hn h
  cases he : queue as pick h with
  | nil => exact (hq he).elim
  | cons a rest => simp [policy,he]

theorem empty_plan_queue (h : History Bool Bool) :
    queue (fun (_ : Bool) => ([] : List Bool)) choose h = [] := by
  induction h with
  | nil => rfl
  | cons z h ih => simp [queue,ih]

theorem empty_plan_uses_default (h : History Bool Bool) :
    policy (fun (_ : Bool) => ([] : List Bool)) choose true () h = true := by
  simp [policy,empty_plan_queue]

theorem empty_macro_clock (n : ℕ) :
    macroHistory (fun (_ : Bool) => ([] : List Bool)) choose ones n = [] := by
  induction n with
  | zero => rfl
  | succ n ih => simp [macroHistory,feed,ih]

theorem empty_blocks_vacuously_good :
    ∀ᶠ n in atTop, ∀ a ∈ macroBlocks (fun (_ : Bool) => ([] : List Bool)) choose ones n, False := by
  simp [macroBlocks]

def model (σ _a y : Bool) : ℝ := if σ then (if y then 3/4 else 1/4) else (if y then 1/4 else 3/4)

theorem acquired_feedback_changes_unique_mle :
    chooseMLE model false ([(false,true)] : History Bool Bool) = true := by
  have h := chooseMLE_maximizes model false ([(false,true)] : History Bool Bool) true
  cases he : chooseMLE model false ([(false,true)] : History Bool Bool)
  · norm_num [he,historyScore,model] at h
  · rfl

theorem shared_policy_ignores_private_seed (P : Bool → Bool → Bool → ℝ)
    (support : Bool → Finset Bool) (h : History Bool Bool) :
    sharedPolicy P support false false (true : Bool) h =
    sharedPolicy P support false false (false : Bool) h := rfl

def coin (_a _y : Bool) : ℝ := 1/2
lemma coin_nonneg : ∀ a y, 0 ≤ coin a y := by intros; norm_num [coin]
lemma coin_norm : ∀ a, ∑ y, coin a y = 1 := by intro a; norm_num [coin,Fintype.sum_bool]

theorem modelwise_constant_policies_succeed (θ : Bool) :
    ∀ᵐ x ∂actionLaw (fun (_r : Bool) (_h : History Bool Bool) => θ)
      (Measure.dirac false) coin coin_nonneg coin_norm false,
      ∀ᶠ n in atTop, x n ∈ ({θ} : Finset Bool) := by
  apply actionLaw_eventually_good_of_stack _ measurable_const
    (Measure.dirac false) coin coin_nonneg coin_norm false {θ}
  simp [stackActionTrajectory]

theorem identical_models_no_nonempty_support :
    ¬ ∃ U : Finset Bool, U.Nonempty ∧ SelfVerifying (fun θ : Bool => ({θ} : Finset Bool))
      (fun (_η _ζ _a : Bool) => True) false U := by
  rintro ⟨U,⟨a,ha⟩,hs⟩
  have hf : a = false := by simpa using hs.1 ha
  have ht : a = true := by simpa using hs.2 true (fun _ _ => trivial) ha
  cases hf.symm.trans ht

end MicroAudit
