import RecursiveCanonicalSufficiency

namespace IndependentCanonicalControls
open Orthemology.Tranche2 Orthemology.Tranche3
open PolicyEmbedding CausalTree CanonicalMicro
open MeasureTheory
open scoped BigOperators ENNReal

def detP (_ y : Bool) : ℝ := if y then 0 else 1
lemma detP_nonneg : ∀ a y, 0 ≤ detP a y := by intro a y; cases y <;> norm_num [detP]
lemma detP_normalized : ∀ a, ∑ y, detP a y = 1 := by intro a; simp [detP]
def π : History Bool Bool → Bool := fun h => if h=[] then false else true

theorem first_history_mass : historyPMF π detP detP_nonneg detP_normalized 1 [(false,false)] = 1 := by
  rw [historyPMF_apply]
  norm_num [π,ActionCompatible,detP,Fin.prod_univ_succ]
theorem second_history_mass : historyPMF π detP detP_nonneg detP_normalized 2 [(true,false),(false,false)] = 1 := by
  rw [historyPMF_apply]
  norm_num [π,ActionCompatible,detP,Fin.prod_univ_succ]
  apply Finset.prod_eq_one
  intro x _
  fin_cases x <;> norm_num
theorem wrong_action_history_mass : historyPMF π detP detP_nonneg detP_normalized 1 [(true,false)] = 0 := by
  rw [historyPMF_apply]
  norm_num [π,ActionCompatible,detP,Fin.prod_univ_succ]
theorem zero_probability_history_mass : historyPMF π detP detP_nonneg detP_normalized 1 [(false,true)] = 0 := by
  rw [historyPMF_apply]
  norm_num [π,ActionCompatible,detP,Fin.prod_univ_succ]
theorem wrong_length_history_mass : historyPMF π detP detP_nonneg detP_normalized 1 [(true,false),(false,false)] = 0 := by
  rw [historyPMF_apply]
  norm_num

def spawn (p : Bool) : NodeState Bool Bool Bool := (p,fun _ => .leaf true)
def charge (a : Bool) : ℝ := if a then 0 else 1
def pot (p : Bool) : ℝ := if p then 0 else 1

theorem seed_blind (r r' : Bool) (h : History Bool Bool) :
    erasedHistoryPolicy id spawn (spawn false) r h = erasedHistoryPolicy id spawn (spawn false) r' h := rfl

theorem first_exit_skips_suffix :
    stopTree (fun (_ _ : Bool) => false) [false,true] (fun _ => ()) =
      (.node false (fun _ => .leaf ()) : ActionTree Bool Bool Unit) := rfl

theorem zero_mass_invalid_child_allowed :
    Valid detP (fun p : Bool => p=true)
      (.node false (fun y => .leaf (!y)) : ActionTree Bool Bool Bool) := by
  intro y hy
  cases y <;> norm_num [detP,Valid] at *

theorem impossible_child_really_invalid : ¬ ((!true : Bool)=true) := by decide

theorem actual_canonical_one_bad_budget :
    (∫⁻ x, ∑' t, ENNReal.ofReal (charge (x t))
      ∂actionLaw (erasedHistoryPolicy id spawn (spawn false) : Unit → History Bool Bool → Bool)
        (Measure.dirac ()) detP detP_nonneg detP_normalized false) ≤ 1 := by
  have hb := actionTreePolicy_total_cost id spawn detP detP_nonneg detP_normalized charge
    (by intro a; cases a <;> norm_num [charge]) pot
    (by intro p; cases p <;> norm_num [pot]) (fun _ => True)
    (by intro q _ y _; trivial)
    (by intro q _; cases q <;> simp [nodeValue,treeValue,spawn,pot,charge])
    false True.intro (Measure.dirac () : Measure Unit) false
  simpa only [pot,Bool.false_eq_true,ite_false,ENNReal.ofReal_one] using hb

-- All other hypotheses of the normalized drift hold in this two-phase model,
-- but an impossible nonempty killed history has zero potential and cannot pay a new charge.
def K (_p : Bool) (_θ _a : Unit) (y : Bool) : ℝ := if y then 0 else 1
def stay (_p : Bool) (_a : Unit) (_y : Bool) : Bool := false
def next (_p : Bool) (_a : Unit) (_y : Bool) : Bool := true
def choose (_p : Bool) (_h : PhaseHistory (Obs := fun (_ : Bool) (_ : Unit) => Bool) _p) : Unit := ()
def macroCost (p : Bool) (_ : Unit) : ℝ := if p then 0 else 1
def V (p : Bool) (h : PhaseHistory (Obs := fun (_ : Bool) (_ : Unit) => Bool) p) : ℝ :=
  if p then 0 else if h=[] then 1 else 0
def D (_p : Bool) : ℝ := 0

theorem K_nonnegative : ∀ p θ a y, 0 ≤ K p θ a y := by
  intro p θ a y; cases y <;> norm_num [K]
theorem K_normalized : ∀ p a, ∑ y, K p () a y = 1 := by intro p a; simp [K]
theorem V_nonnegative : ∀ p h, 0 ≤ V p h := by
  intro p h; unfold V; split_ifs <;> norm_num

theorem unnormalized_drift_all_histories : ∀ p h,
    macroCost p (choose p h) * dHistoryMass (continuingKernel K stay p) () h +
      (∑ y : Bool, if stay p (choose p h) y then V p (⟨choose p h,y⟩::h) else 0) ≤ V p h := by
  intro p h
  cases p <;> cases h <;> simp [macroCost,V,stay,continuingKernel,dHistoryMass]

theorem exit_allowance_valid : ∀ p a y,
    V (next p a y) [] + D (next p a y) ≤ D p := by
  intro p a y; simp [V,next,D]

def impossible : ResetState (Obs := fun (_ : Bool) (_ : Unit) => Bool) :=
  ⟨false,[⟨(),false⟩]⟩

theorem impossible_killed_mass_zero :
    dHistoryMass (continuingKernel K stay impossible.1) () impossible.2 = 0 := by
  simp [impossible,dHistoryMass,continuingKernel,stay]

theorem positive_mass_guard_cannot_be_erased :
    ¬ (macroCost impossible.1 (choose impossible.1 impossible.2) +
      ∑ y : Bool, K impossible.1 () (choose impossible.1 impossible.2) y *
        normalizedResetPotential K stay () V D (resetUpdate stay next choose impossible y) ≤
      normalizedResetPotential K stay () V D impossible) := by
  have hz : normalizedResetPotential K stay () V D impossible = 0 := by
    unfold normalizedResetPotential
    rw [impossible_killed_mass_zero]
    norm_num
  rw [hz]
  norm_num [impossible,macroCost,choose,normalizedResetPotential,V,D,resetUpdate,stay,next,
    dHistoryMass,continuingKernel,K]
end IndependentCanonicalControls
