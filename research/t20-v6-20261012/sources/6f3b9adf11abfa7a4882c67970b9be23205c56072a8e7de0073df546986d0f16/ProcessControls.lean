import GeneratedLiveController
open MeasureTheory ProbabilityTheory Set Filter
open scoped BigOperators ENNReal
namespace ProcessAudit
open Orthemology.Tranche2

lemma empty_live_support_is_vacuous {Θ A Y : Type*} [DecidableEq Θ] [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (live : Finset Θ) (σ : Θ) :
    LiveSelfVerifying P good live σ [] := by simp [LiveSelfVerifying]

lemma empty_plan_charge {A : Type*} [DecidableEq A] (good : Finset A) :
    plannedBadCount good []=0 := rfl

lemma empty_block_is_completed {Y : Type*} :
    stopCompleted (Y:=Y) (n:=0) PUnit.unit=true := rfl

lemma interruption_executes_only_first (y : Bool) :
    stoppedActions [false,true,true] (Sum.inl y : StopObs Bool 3)=[false] := rfl

lemma no_tail_mass_after_exit (p : Bool → Bool → ℝ) (y : Bool) (w : StopObs Bool 2) :
    stoppedMass p (fun _ _ => false) [false,true,true] (Sum.inr (y,w))=0 := rfl

lemma full_exit_mass_is_retained (p : Bool → Bool → ℝ) (y : Bool) :
    stoppedMass p (fun _ _ => false) [false,true,true] (Sum.inl y)=p false y := rfl

lemma duplicate_actions_are_charged : plannedBadCount (∅ : Finset Bool) [true,true]=2 := by
  norm_num [plannedBadCount]

lemma planned_charge_can_strictly_overcount_execution (y : Bool) :
    plannedBadCount ({false} : Finset Bool) [false,true]=1 ∧
    plannedBadCount ({false} : Finset Bool)
      (stoppedActions [false,true] (Sum.inl y : StopObs Bool 2))=0 := by
  norm_num [plannedBadCount,stoppedActions]

abbrev ToyObs (_ : Bool) (_ : Unit) := Bool
def toyPi (p : Bool) (_ : PhaseHistory (Obs:=ToyObs) p) : Unit := ()
def toyNext (_ : Bool) (_ : Unit) (_ : Bool) := false

lemma different_exits_collapse_to_same_state :
    resetUpdate (Obs:=ToyObs) (fun _ _ _ => false) toyNext toyPi ⟨true,[]⟩ false =
      resetUpdate (Obs:=ToyObs) (fun _ _ _ => false) toyNext toyPi ⟨true,[]⟩ true := rfl

lemma reset_forgets_old_history (h : PhaseHistory (Obs:=ToyObs) true) (y : Bool) :
    resetUpdate (Obs:=ToyObs) (fun _ _ _ => false) toyNext toyPi ⟨true,h⟩ y = ⟨false,[]⟩ := rfl

lemma continuation_appends_actual_observation (h : PhaseHistory (Obs:=ToyObs) true) (y : Bool) :
    resetUpdate (Obs:=ToyObs) (fun _ _ _ => true) toyNext toyPi ⟨true,h⟩ y =
      ⟨true,⟨(),y⟩::h⟩ := rfl

lemma one_step_charge_is_current {S : Type*} (c : S → ℝ≥0∞) (x : ℕ → S) :
    pathCharge c 0 1 x=c (x 0) := by simp [pathCharge]

lemma two_step_charge_has_no_extra_terminal {S : Type*} (c : S → ℝ≥0∞) (x : ℕ → S) :
    pathCharge c 0 2 x=c (x 0)+c (x 1) := by norm_num [pathCharge,Finset.sum_range_succ]

lemma zero_history_mass_implies_zero_budget
    {Phase Θ : Type*} {Obs : Phase → Θ → Type*} [∀ p a, Fintype (Obs p a)]
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs:=Obs) p → Θ)
    (cost : Phase → Θ → ℝ) (θ : Θ) (n : ℕ) (p : Phase) (h : PhaseHistory (Obs:=Obs) p)
    (hz : dHistoryMass (continuingKernel K stay p) θ h=0) :
    resetCost K stay next π cost θ n p h=0 := by
  rw [resetCost_eq_mass_future,hz,zero_mul]

lemma deterministic_self_reset_cannot_have_decreasing_rank (rank : Unit → ℕ) :
    ¬ rank () < rank () := Nat.lt_irrefl _

lemma excluding_true_model_violates_retention : true ∉ ({false} : Finset Bool) := by decide

lemma natural_positive_charge_at_least_one (c : ℕ) (hc : 0<c) : (1:ℝ≥0∞)≤c := by
  exact_mod_cast Nat.succ_le_of_lt hc

lemma positive_real_charges_need_not_be_eventually_zero :
    ¬ (∀ᶠ n : ℕ in atTop, (1/2:ℝ)^(n+1)=0) := by
  intro h
  have he : ∀ᶠ n : ℕ in atTop, (1/2:ℝ)^(n+1)≠0 :=
    Eventually.of_forall (fun n => pow_ne_zero _ (by norm_num))
  obtain ⟨n,hn,hn'⟩ := (h.and he).exists
  exact hn' hn

lemma positive_real_charge_prefix_is_bounded (n : ℕ) :
    ∑ i ∈ Finset.range n, (1/2:ℝ)^(i+1) = 1-(1/2:ℝ)^n := by
  induction n with
  | zero => simp
  | succ n ih => rw [Finset.sum_range_succ,ih,pow_succ]; ring

lemma positive_real_charge_prefix_le_one (n : ℕ) :
    ∑ i ∈ Finset.range n, (1/2:ℝ)^(i+1) ≤ 1 := by
  rw [positive_real_charge_prefix_is_bounded]
  have hh : 0 ≤ (1/2:ℝ)^n := pow_nonneg (by norm_num) _
  linarith

-- Exact finite-law interface: an equality of the constructed infinite law's
-- actual prefix integral and the real reset recurrence, not a caller premise.
example {Phase Θ : Type*} {Obs : Phase → Θ → Type*}
    [Fintype Phase] [Fintype Θ] [∀ p a, Fintype (Obs p a)]
    (K : (p : Phase) → (θ a : Θ) → Obs p a → ℝ)
    (stay : (p : Phase) → (a : Θ) → Obs p a → Bool)
    (next : (p : Phase) → (a : Θ) → Obs p a → Phase)
    (π : (p : Phase) → PhaseHistory (Obs:=Obs) p → Θ) (cost : Phase → Θ → ℝ)
    (hK : ∀ p η a y, 0≤K p η a y) (hNorm : ∀ p η a, ∑ y, K p η a y=1)
    (hcost : ∀ p a, 0≤cost p a) (θ : Θ) (n : ℕ) (p : Phase) :
    (∫⁻ x, pathCharge (fun s => ENNReal.ofReal (cost s.1 (π s.1 s.2))) 0 n x
      ∂markovTrajectory (resetTransitionKernel K stay next π hK hNorm θ) ⟨p,[]⟩) =
      ENNReal.ofReal (resetCost K stay next π cost θ n p []) :=
  trajectory_expected_charge_eq_resetCost K stay next π cost hK hNorm hcost θ n p
end ProcessAudit
