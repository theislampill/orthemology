import RecursiveMacroPotential

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3
open Orthemology.Tranche2 CausalTree
open Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {Θ A Y : Type u} [Fintype Θ] [Fintype Y] [DecidableEq Θ] [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)

/-- The offered stopped block, expanded into literal one-action/one-observation
nodes. Macro likelihood memory and the support phase update only at a leaf. -/
def recursiveSpawnTree (s : RecursiveMacroState P good menu) :
    ActionTree A Y (RecursiveMacroState P good menu) :=
  stopTree (supportStay P s.1.val)
    (phaseActs P good menu s.1 (recursivePolicy P good menu s.1 s.2))
    (resetUpdate (recursiveKeep P good menu) (phaseNext P good menu) (recursivePolicy P good menu) s)

omit [Fintype Θ] [Fintype Y] in
lemma recursiveSpawnTree_nonleaf (s : RecursiveMacroState P good menu) :
    ∃ a k, recursiveSpawnTree P good menu s = .node a k :=
  stopTree_nonleaf _ _ (phaseActs_spec P good menu s.1 _).1 _

def recursiveSpawn (s : RecursiveMacroState P good menu) :
    NodeState A Y (RecursiveMacroState P good menu) :=
  nodeOfTree (recursiveSpawnTree P good menu s) (recursiveSpawnTree_nonleaf P good menu s)

omit [Fintype Θ] [Fintype Y] in
lemma recursiveSpawn_asTree (s : RecursiveMacroState P good menu) :
    ActionTree.node (recursiveSpawn P good menu s).1 (recursiveSpawn P good menu s).2 =
      recursiveSpawnTree P good menu s := nodeOfTree_asTree _ _

/-- Shared physical-history policy. Hidden truth θ is absent from every policy,
queue/tree, action, and update parameter. The private seed is unused. -/
def recursiveHistoryPolicy {R : Type v} (p : WinningPhase P good menu) : R → History A Y → A :=
  erasedHistoryPolicy id (recursiveSpawn P good menu) (recursiveSpawn P good menu ⟨p,[]⟩)

/-- A one-unit real charge for each actual target-bad action. -/
def realBadActionCost (G : Finset A) (a : A) : ℝ := if a ∈ G then 0 else 1

lemma realBadActionCost_nonneg (G : Finset A) (a : A) : 0 ≤ realBadActionCost G a := by
  unfold realBadActionCost
  split_ifs <;> norm_num

lemma ofReal_realBadActionCost (G : Finset A) (a : A) :
    ENNReal.ofReal (realBadActionCost G a) = badActionCost G a := by
  unfold realBadActionCost badActionCost
  split_ifs <;> simp

lemma realListCost_realBadActionCost (G : Finset A) (as : List A) :
    realListCost (realBadActionCost G) as = (plannedBadCount G as : ℝ) := by
  induction as with
  | nil => simp [realListCost,plannedBadCount]
  | cons a as ih =>
    by_cases ha : a ∈ G
    · simpa [realListCost,realBadActionCost,plannedBadCount,ha] using ih
    · simpa [realListCost,realBadActionCost,plannedBadCount,ha,Nat.cast_add,add_comm] using congrArg (fun x : ℝ => 1+x) ih

/-- Every positive-probability leaf of the physical tree is a valid normalized
macro state. No invariant is imposed on an impossible counterfactual branch. -/
theorem recursiveSpawn_valid
    (hP : ∀ θ a y, 0 ≤ P θ a y) (θ : Θ) (s : RecursiveMacroState P good menu)
    (hs : recursiveMacroValid P good menu θ s) :
    Valid (P θ) (recursiveMacroValid P good menu θ)
      (.node (recursiveSpawn P good menu s).1 (recursiveSpawn P good menu s).2) := by
  rw [recursiveSpawn_asTree]
  apply stopTree_valid
  intro w hw
  exact recursiveMacroValid_next P good menu hP θ s hs w hw

/-- Sequential expansion preserves the stopped kernel's quantitative estimate;
the exit-triggering action is counted and the old suffix is not executed. -/
theorem recursiveSpawn_potential_bound
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (s : RecursiveMacroState P good menu) (hs : recursiveMacroValid P good menu θ s) :
    nodeValue (P θ) (realBadActionCost (good θ)) (recursiveMacroPotential P good menu hP θ)
      (recursiveSpawn P good menu s) ≤ recursiveMacroPotential P good menu hP θ s := by
  unfold nodeValue
  rw [recursiveSpawn_asTree]
  have hb := stopTree_value_le_planned (P θ) (supportStay P s.1.val) (realBadActionCost (good θ))
    (recursiveMacroPotential P good menu hP θ) (hP θ) (hN θ) (realBadActionCost_nonneg (good θ))
    (phaseActs P good menu s.1 (recursivePolicy P good menu s.1 s.2))
    (resetUpdate (recursiveKeep P good menu) (phaseNext P good menu) (recursivePolicy P good menu) s)
  have hl : recursivePolicy P good menu s.1 s.2 ∈ s.1.val :=
    greedyMax_live_mem _ _ _ (phaseInitial_mem P good menu s.1)
  have hc : realListCost (realBadActionCost (good θ))
      (phaseActs P good menu s.1 (recursivePolicy P good menu s.1 s.2)) =
        (recursiveBadCharge P good menu θ s.1 (recursivePolicy P good menu s.1 s.2) : ℝ) := by
    rw [realListCost_realBadActionCost,recursiveBadCharge,if_pos hl]
  rw [hc] at hb
  exact hb.trans (recursiveMacroPotential_step P good menu hP hN θ s hs)

section Canonical
variable {R : Type v} [Fintype A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

omit [Fintype Θ] [Inhabited Y] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma recursiveHistoryPolicy_measurable (p : WinningPhase P good menu) :
    Measurable (fun z : R × History A Y => recursiveHistoryPolicy P good menu p z.1 z.2) :=
  (measurable_of_countable (fun h : History A Y =>
    (replayObserved (recursiveSpawn P good menu) (recursiveSpawn P good menu ⟨p,[]⟩) h).1)).comp measurable_snd

/-- Main canonical constructive endpoint. Zeros and changing support menus are
allowed. One explicit shared history-only policy has finite expected total bad
physical action count in the same actionLaw used by the earlier necessity.
No representation, law-equality, progress, rank, drift, or clock premise is supplied. -/
theorem recursiveHistoryPolicy_actionLaw_total_bad_budget
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) :
    (∫⁻ x, ∑' t, badActionCost (good θ) (x t)
      ∂actionLaw (recursiveHistoryPolicy P good menu p) ρ (P θ) (hP θ) (hN θ) d) ≤
        ENNReal.ofReal (recursiveChainBudget P good menu hP θ p) := by
  have hb := actionTreePolicy_total_cost id (recursiveSpawn P good menu) (P θ) (hP θ) (hN θ)
    (realBadActionCost (good θ)) (realBadActionCost_nonneg (good θ))
    (recursiveMacroPotential P good menu hP θ) (recursiveMacroPotential_nonneg P good menu hP hN θ)
    (recursiveMacroValid P good menu θ) (recursiveSpawn_valid P good menu hP θ)
    (recursiveSpawn_potential_bound P good menu hP hN θ) ⟨p,[]⟩
    (show recursiveMacroValid P good menu θ ⟨p,[]⟩ from ⟨hθ,by simp [dHistoryMass]⟩) ρ d
  simpa only [ofReal_realBadActionCost,recursiveMacroPotential_root] using hb

/-- The same literal physical action law is almost surely eventually target-good. -/
theorem recursiveHistoryPolicy_actionLaw_eventually_good
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (θ : Θ) (p : WinningPhase P good menu) (hθ : θ ∈ p.val)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) :
    ∀ᵐ x ∂actionLaw (recursiveHistoryPolicy P good menu p) ρ (P θ) (hP θ) (hN θ) d,
      ∀ᶠ t in atTop, x t ∈ good θ := by
  classical
  let c : A → ℕ := fun a => if a ∈ good θ then 0 else 1
  have he : ∀ a, (c a : ℝ≥0∞) = badActionCost (good θ) a := by
    intro a
    by_cases ha : a ∈ good θ <;> simp [c,badActionCost,ha]
  have hb := recursiveHistoryPolicy_actionLaw_total_bad_budget P good menu hP hN θ p hθ ρ d
  have hf : ∀ n, (∫⁻ x, pathCharge (fun a => (c a : ℝ≥0∞)) 0 n x
      ∂actionLaw (recursiveHistoryPolicy P good menu p) ρ (P θ) (hP θ) (hN θ) d) ≤
        ENNReal.ofReal (recursiveChainBudget P good menu hP θ p) := by
    intro n
    apply le_trans (lintegral_mono ?_) hb
    intro x
    simp only [pathCharge,Nat.zero_add,he]
    exact ENNReal.sum_le_tsum (Finset.range n)
  have ha := (trajectory_nat_charge_eventually_zero _ c _ hf).2
  filter_upwards [ha] with x hx
  filter_upwards [hx] with t ht
  by_contra hbad
  simp [c,hbad] at ht
end Canonical
end Orthemology.Tranche3
