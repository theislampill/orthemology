import ChainPhysicalBudget

noncomputable section
set_option linter.unusedSectionVars false
open Finset
open scoped BigOperators
namespace Orthemology.Tranche3.CausalTree
open Orthemology.Tranche2

/-- A finite causal action tree. The action at a node is fixed before its
observation; only the acquired observation chooses the next subtree. -/
inductive ActionTree (A Y S : Type*) where
  | leaf : S → ActionTree A Y S
  | node : A → (Y → ActionTree A Y S) → ActionTree A Y S

abbrev NodeState (A Y S : Type*) := A × (Y → ActionTree A Y S)
variable {A Y S : Type*}

/-- Reset at a leaf, otherwise execute the residual subtree. No next observation
is read during a reset or action choice. -/
def advance (spawn : S → NodeState A Y S) (s : NodeState A Y S) (y : Y) : NodeState A Y S :=
  match s.2 y with
  | .leaf q => spawn q
  | .node a k => (a,k)

/-- A literal acquired-history evaluator; histories are newest first. -/
def replay (spawn : S → NodeState A Y S) (s₀ : NodeState A Y S) : List (A × Y) → NodeState A Y S
  | [] => s₀
  | (_,y)::h => advance spawn (replay spawn s₀ h) y

def historyPolicy {R : Type*} (spawn : S → NodeState A Y S) (s₀ : NodeState A Y S)
    (_ : R) (h : List (A × Y)) : A := (replay spawn s₀ h).1

/-- The next action is determined by the acquired history alone. -/
lemma historyPolicy_seed_independent {R : Type*} (spawn : S → NodeState A Y S)
    (s₀ : NodeState A Y S) (r r' : R) (h : List (A × Y)) :
    historyPolicy spawn s₀ r h = historyPolicy spawn s₀ r' h := rfl

/-- Replay uses only acquired observations; the stored action field may have a
separate public label type, such as the current support paired with an action. -/
def replayObserved {L H : Type*} (spawn : S → NodeState L Y S) (s₀ : NodeState L Y S) :
    List (H × Y) → NodeState L Y S
  | [] => s₀
  | (_,y)::h => advance spawn (replayObserved spawn s₀ h) y

/-- Relabel action nodes without changing branching or macro-state leaves. -/
def mapActions {L : Type*} (f : A → L) : ActionTree A Y S → ActionTree L Y S
  | .leaf q => .leaf q
  | .node a k => .node (f a) (fun y => mapActions f (k y))

/-- Extract the root of a certified nonempty action tree. -/
def nodeOfTree (t : ActionTree A Y S) (h : ∃ a k, t = .node a k) : NodeState A Y S :=
  (Classical.choose h, Classical.choose (Classical.choose_spec h))

lemma nodeOfTree_asTree (t : ActionTree A Y S) (h : ∃ a k, t = .node a k) :
    ActionTree.node (nodeOfTree t h).1 (nodeOfTree t h).2 = t :=
  (Classical.choose_spec (Classical.choose_spec h)).symm

section Value
variable [Fintype Y]

def treeValue (P : A → Y → ℝ) (cost : A → ℝ) (F : S → ℝ) : ActionTree A Y S → ℝ
  | .leaf q => F q
  | .node a k => cost a + ∑ y, P a y * treeValue P cost F (k y)

def nodeValue (P : A → Y → ℝ) (cost : A → ℝ) (F : S → ℝ) (s : NodeState A Y S) : ℝ :=
  treeValue P cost F (.node s.1 s.2)

lemma treeValue_mapActions {L : Type*} (f : A → L) (P : L → Y → ℝ)
    (cost : L → ℝ) (F : S → ℝ) (t : ActionTree A Y S) :
    treeValue P cost F (mapActions f t) = treeValue (fun a => P (f a)) (fun a => cost (f a)) F t := by
  induction t with
  | leaf q => rfl
  | node a k ih => simp only [mapActions,treeValue,ih]

lemma treeValue_nonneg (P : A → Y → ℝ) (cost : A → ℝ) (F : S → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hc : ∀ a, 0 ≤ cost a) (hF : ∀ q, 0 ≤ F q)
    (t : ActionTree A Y S) : 0 ≤ treeValue P cost F t := by
  induction t with
  | leaf q => exact hF q
  | node a k ih => exact add_nonneg (hc a) (sum_nonneg (fun y _ => mul_nonneg (hP a y) (ih y)))

/-- Every leaf that can actually be reached under P satisfies the macro-state
invariant. Zero-mass children do not need fictitious invariant witnesses. -/
def Valid (P : A → Y → ℝ) (I : S → Prop) : ActionTree A Y S → Prop
  | .leaf q => I q
  | .node a k => ∀ y, 0 < P a y → Valid P I (k y)

omit [Fintype Y] in
lemma valid_mapActions {L : Type*} (f : A → L) (P : L → Y → ℝ)
    (I : S → Prop) (t : ActionTree A Y S) :
    Valid P I (mapActions f t) ↔ Valid (fun a => P (f a)) I t := by
  induction t with
  | leaf q => rfl
  | node a k ih => simp only [mapActions,Valid,ih]

omit [Fintype Y] in
lemma advance_valid (P : A → Y → ℝ) (I : S → Prop) (spawn : S → NodeState A Y S)
    (hs : ∀ q, I q → Valid P I (.node (spawn q).1 (spawn q).2))
    (s : NodeState A Y S) (hv : Valid P I (.node s.1 s.2)) (y : Y) (hy : 0 < P s.1 y) :
    Valid P I (.node (advance spawn s y).1 (advance spawn s y).2) := by
  have hh := hv y hy
  cases hk : s.2 y with
  | leaf q => simpa only [advance,hk] using hs q (by simpa only [Valid,hk] using hh)
  | node a k => simpa only [advance,hk] using hh

/-- The block bound becomes a literal one-observation potential decrease.
Reset inequalities are needed only for positive-mass reached leaves. -/
theorem node_step_bound (P : A → Y → ℝ) (cost : A → ℝ) (F : S → ℝ)
    (I : S → Prop) (spawn : S → NodeState A Y S)
    (hP : ∀ a y, 0 ≤ P a y)
    (hspawn : ∀ q, I q → nodeValue P cost F (spawn q) ≤ F q)
    (s : NodeState A Y S) (hv : Valid P I (.node s.1 s.2)) :
    cost s.1 + ∑ y, P s.1 y * nodeValue P cost F (advance spawn s y) ≤
      nodeValue P cost F s := by
  apply add_le_add_left
  apply Finset.sum_le_sum
  intro y _
  by_cases hp : 0 < P s.1 y
  · have hh := hv y hp
    cases hk : s.2 y with
    | leaf q =>
      have hi : I q := by simpa only [hk,Valid] using hh
      exact mul_le_mul_of_nonneg_left (by simpa only [advance,hk,treeValue] using hspawn q hi) (hP _ _)
    | node a k => simp only [advance,hk,nodeValue,le_refl]
  · have hz : P s.1 y = 0 := le_antisymm (le_of_not_gt hp) (hP _ _)
    simp only [hz,zero_mul,le_refl]
end Value

/-- Physical expansion of a stopped block. Only the current observation is
examined; an exit jumps straight to the recorded macro update. -/
def stopTree (stay : A → Y → Bool) :
    (acts : List A) → (StopObs Y acts.length → S) → ActionTree A Y S
  | [], finish => .leaf (finish PUnit.unit)
  | a::as, finish => .node a (fun y => if stay a y then
      stopTree stay as (fun w => finish (Sum.inr (y,w))) else .leaf (finish (Sum.inl y)))

lemma stopTree_nonleaf (stay : A → Y → Bool) (acts : List A)
    (hne : acts ≠ []) (finish : StopObs Y acts.length → S) :
    ∃ a k, stopTree stay acts finish = .node a k := by
  cases acts with
  | nil => exact (hne rfl).elim
  | cons a as => exact ⟨a,_,rfl⟩

/-- A positive stopped record preserves precisely the leaf invariants needed
by the micro-step proof. -/
theorem stopTree_valid (P : A → Y → ℝ) (stay : A → Y → Bool) (I : S → Prop)
    (acts : List A) (finish : StopObs Y acts.length → S)
    (hw : ∀ w, 0 < stoppedMass P stay acts w → I (finish w)) :
    Valid P I (stopTree stay acts finish) := by
  induction acts with
  | nil => exact hw PUnit.unit (by simp [stoppedMass])
  | cons a as ih =>
    intro y hy
    cases hs : stay a y
    · simp only [stopTree,hs,Bool.false_eq_true,↓reduceIte,Valid]
      exact hw (Sum.inl y) (by simpa only [stoppedMass,hs,Bool.false_eq_true,↓reduceIte] using hy)
    · simp only [stopTree,hs,↓reduceIte]
      apply ih
      intro w hw'
      exact hw (Sum.inr (y,w)) (by simpa only [stoppedMass,hs,↓reduceIte] using mul_pos hy hw')

section Mass
variable [Fintype Y]

def realListCost (c : A → ℝ) (as : List A) : ℝ := (as.map c).sum

/-- Unfolding the sequential tree gives exactly the stopped-prefix distribution,
including the cost of the exit-triggering action and no unexecuted suffix. -/
theorem stopTree_value_eq_stopped_sum (P : A → Y → ℝ) (stay : A → Y → Bool)
    (c : A → ℝ) (F : S → ℝ) (hN : ∀ a, ∑ y, P a y = 1)
    (acts : List A) (finish : StopObs Y acts.length → S) :
    treeValue P c F (stopTree stay acts finish) =
      ∑ w, stoppedMass P stay acts w * (realListCost c (stoppedActions acts w) + F (finish w)) := by
  induction acts with
  | nil => simp [stopTree,treeValue,stoppedMass,stoppedActions,StopObs,realListCost]
  | cons a as ih =>
    change c a + (∑ y, P a y * treeValue P c F
      (if stay a y then stopTree stay as (fun w => finish (Sum.inr (y,w))) else .leaf (finish (Sum.inl y)))) =
      ∑ w : Y ⊕ (Y × StopObs Y as.length), _
    rw [Fintype.sum_sum_type,Fintype.sum_prod_type,← Finset.sum_add_distrib]
    have hc : c a = ∑ y, P a y * c a := by rw [← Finset.sum_mul,hN,one_mul]
    rw [hc,← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro y _
    cases hs : stay a y
    · simp [hs,treeValue,stoppedMass,stoppedActions,realListCost,mul_add]
    · simp only [hs,↓reduceIte,ih,stoppedMass,stoppedActions,realListCost,List.map_cons,List.sum_cons]
      have hn := stoppedMass_normalized P stay hN as
      simp only [Bool.true_eq_false,↓reduceIte,zero_mul,zero_add]
      rw [Finset.mul_sum]
      calc
        P a y * c a + ∑ w, P a y * (stoppedMass P stay as w * ((List.map c (stoppedActions as w)).sum + F (finish (Sum.inr (y,w))))) =
          P a y * c a * (∑ w, stoppedMass P stay as w) +
            ∑ w, P a y * (stoppedMass P stay as w * ((List.map c (stoppedActions as w)).sum + F (finish (Sum.inr (y,w))))) := by rw [hn,mul_one]
        _ = _ := by
          rw [Finset.mul_sum,← Finset.sum_add_distrib]
          apply Finset.sum_congr rfl
          intro w _
          ring

omit [Fintype Y] in
lemma realListCost_nonneg (c : A → ℝ) (hc : ∀ a, 0 ≤ c a) (as : List A) :
    0 ≤ realListCost c as := by
  induction as with
  | nil => simp [realListCost]
  | cons a as ih => simpa only [realListCost,List.map_cons,List.sum_cons] using add_nonneg (hc a) ih

omit [Fintype Y] in
lemma realListCost_sublist (c : A → ℝ) (hc : ∀ a, 0 ≤ c a) (as bs : List A)
    (hs : as.Sublist bs) : realListCost c as ≤ realListCost c bs := by
  exact List.Sublist.sum_le_sum (hs.map c) (fun a ha => by
    obtain ⟨b,_,rfl⟩ := List.mem_map.mp ha
    exact hc b)

/-- The analytic block charge overestimates, rather than undercounts, every
actually executed stopped prefix. -/
theorem stopTree_value_le_planned (P : A → Y → ℝ) (stay : A → Y → Bool)
    (c : A → ℝ) (F : S → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (hc : ∀ a, 0 ≤ c a) (acts : List A) (finish : StopObs Y acts.length → S) :
    treeValue P c F (stopTree stay acts finish) ≤
      realListCost c acts + ∑ w, stoppedMass P stay acts w * F (finish w) := by
  rw [stopTree_value_eq_stopped_sum P stay c F hN]
  calc
    _ ≤ ∑ w, stoppedMass P stay acts w * (realListCost c acts + F (finish w)) := by
      apply Finset.sum_le_sum
      intro w _
      exact mul_le_mul_of_nonneg_left
        (add_le_add_right (realListCost_sublist c hc _ _ (stoppedActions_sublist acts w)) _)
        (stoppedMass_nonneg P stay hP acts w)
    _ = _ := by
      simp_rw [mul_add]
      rw [Finset.sum_add_distrib,← Finset.sum_mul,stoppedMass_normalized P stay hN,one_mul]
end Mass
end Orthemology.Tranche3.CausalTree
