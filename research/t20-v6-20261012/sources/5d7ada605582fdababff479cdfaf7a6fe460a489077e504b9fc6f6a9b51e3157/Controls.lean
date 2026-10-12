import Attainment
import Mathlib.Tactic.NormNum

/-! Nonvacuity and a sharp finite-rule boundary for minimum attainment.
All constructions use genuine occurrence trees, actual recursive validity,
and exact state equality. No admission predicate or minimum is assumed. -/
namespace GuardedTree.AttainmentControls
open Tree

/-- Infinitely many nullary rules share one state; their positive rational
prices decrease toward zero without attaining it. -/
abbrev infiniteGrammar : Grammar Unit Unit ℕ where
  arity _ := 0
  head _ := ()
  premise _ _ := ()
  localSupport _ := ∅
  price n := 1 / ((n : ℚ) + 1)
  guard _ _ := True

def infiniteLeaf (n : ℕ) : Tree infiniteGrammar := .node n Fin.elim0

theorem infinite_price_pos (n : ℕ) : 0 < infiniteGrammar.price n := by
  have hn : (0 : ℚ) ≤ n := Nat.cast_nonneg n
  exact div_pos (by norm_num) (by linarith)

theorem infinite_price_nonneg (n : ℕ) : 0 ≤ infiniteGrammar.price n :=
  (infinite_price_pos n).le

theorem infinite_price_strict (n : ℕ) :
    infiniteGrammar.price (n + 1) < infiniteGrammar.price n := by
  have hn : (0 : ℚ) ≤ n := Nat.cast_nonneg n
  change 1 / ((↑(n + 1) : ℚ) + 1) < 1 / ((n : ℚ) + 1)
  apply (div_lt_div_iff₀ (by push_cast; linarith) (by linarith)).mpr
  push_cast
  simp only [one_mul]
  linarith

/-- The syntax itself, not merely the valid subfamily, consists of leaves. -/
theorem infinite_every_tree_leaf (t : Tree infiniteGrammar) :
    ∃ n, t = infiniteLeaf n := by
  cases t with
  | node n child =>
    refine ⟨n, ?_⟩
    exact congrArg (Tree.node n) (funext (fun i => Fin.elim0 i))

@[simp] theorem infinite_leaf_valid (n : ℕ) : Valid infiniteGrammar (infiniteLeaf n) := by
  simp [infiniteLeaf, Valid, infiniteGrammar]

@[simp] theorem infinite_leaf_judgement (n : ℕ) :
    judgement infiniteGrammar (infiniteLeaf n) = () := rfl

@[simp] theorem infinite_leaf_support (n : ℕ) :
    support infiniteGrammar (infiniteLeaf n) = ∅ := by
  simp [infiniteLeaf, support, infiniteGrammar]

@[simp] theorem infinite_leaf_cost (n : ℕ) :
    cost infiniteGrammar (infiniteLeaf n) = infiniteGrammar.price n := by
  simp [infiniteLeaf, cost, infiniteGrammar]

/-- Every candidate is valid in exactly the same judgement/support state. -/
theorem infinite_every_tree_exact (t : Tree infiniteGrammar) :
    Valid infiniteGrammar t ∧ judgement infiniteGrammar t = () ∧
      support infiniteGrammar t = ∅ := by
  obtain ⟨n, rfl⟩ := infinite_every_tree_leaf t
  exact ⟨infinite_leaf_valid n, infinite_leaf_judgement n, infinite_leaf_support n⟩

theorem infinite_every_branch_one (t : Tree infiniteGrammar)
    (p : List (Tree infiniteGrammar)) (hp : Branch infiniteGrammar t p) : p.length = 1 := by
  cases hp with
  | root => rfl
  | down n child i p hp => exact Fin.elim0 i

/-- The obstruction survives a uniform height bound of exactly one. -/
theorem infinite_every_tree_height_one (t : Tree infiniteGrammar) :
    Bounded infiniteGrammar 1 t ∧ ¬ Bounded infiniteGrammar 0 t := by
  constructor
  · intro p hp
    exact (infinite_every_branch_one t p hp).le
  · intro h
    have hroot := h [t] (.root t)
    simp at hroot

/-- Every candidate has a strictly cheaper valid leaf with precisely its state. -/
theorem infinite_strictly_cheaper (t : Tree infiniteGrammar) :
    ∃ u : Tree infiniteGrammar, Valid infiniteGrammar u ∧
      judgement infiniteGrammar u = judgement infiniteGrammar t ∧
      support infiniteGrammar u = support infiniteGrammar t ∧
      Bounded infiniteGrammar 1 u ∧ cost infiniteGrammar u < cost infiniteGrammar t := by
  obtain ⟨n, rfl⟩ := infinite_every_tree_leaf t
  refine ⟨infiniteLeaf (n + 1), infinite_leaf_valid _, rfl, ?_,
    (infinite_every_tree_height_one _).1, ?_⟩
  · simp
  · simpa only [infinite_leaf_cost] using infinite_price_strict n

/-- Dropping finite rule labels invalidates minimum attainment, even with
finite J and E, positive prices, empty support, and height-one trees. -/
theorem infinite_no_minimum_exact :
    ¬ ∃ u : Tree infiniteGrammar, Valid infiniteGrammar u ∧
      judgement infiniteGrammar u = () ∧ support infiniteGrammar u = ∅ ∧
      ∀ v : Tree infiniteGrammar, Valid infiniteGrammar v →
        judgement infiniteGrammar v = () → support infiniteGrammar v = ∅ →
        cost infiniteGrammar u ≤ cost infiniteGrammar v := by
  rintro ⟨u, _, hq, hs, hmin⟩
  obtain ⟨v, hv, hqv, hsv, _, hlt⟩ := infinite_strictly_cheaper u
  exact (not_lt_of_ge (hmin v hv (hqv.trans hq) (hsv.trans hs))) hlt

/-- A finite two-rule control with nonempty exact support inside an infinite
ambient evidence type. One leaf costs two and the other costs one. -/
abbrev finiteGrammar : Grammar Unit ℕ Bool where
  arity _ := 0
  head _ := ()
  premise _ _ := ()
  localSupport _ := {0}
  price r := if r then 2 else 1
  guard _ _ := True

def finiteLeaf (r : Bool) : Tree finiteGrammar := .node r Fin.elim0

theorem finite_price_nonneg (r : Bool) : 0 ≤ finiteGrammar.price r := by
  cases r <;> norm_num [finiteGrammar]

@[simp] theorem finite_leaf_valid (r : Bool) : Valid finiteGrammar (finiteLeaf r) := by
  simp [finiteLeaf, Valid, finiteGrammar]

@[simp] theorem finite_leaf_support (r : Bool) :
    support finiteGrammar (finiteLeaf r) = {0} := by
  simp [finiteLeaf, support, finiteGrammar]

theorem finite_cost_lower_bound (t : Tree finiteGrammar) : 1 ≤ cost finiteGrammar t := by
  cases t with
  | node r child => cases r <;> norm_num [cost, finiteGrammar]

/-- This invokes the proved attainment theorem on a valid, nonminimum input.
The resulting exact-state minimum has cost one. No finiteness of E is used. -/
theorem finite_nonvacuity :
    ∃ u : Tree finiteGrammar, Valid finiteGrammar u ∧
      judgement finiteGrammar u = () ∧ support finiteGrammar u = {0} ∧
      Bounded finiteGrammar 2 u ∧ cost finiteGrammar u = 1 ∧
      ∀ v : Tree finiteGrammar, Valid finiteGrammar v →
        judgement finiteGrammar v = () → support finiteGrammar v = {0} →
        cost finiteGrammar u ≤ cost finiteGrammar v := by
  obtain ⟨u, hu, hq, hs, hb, hmin⟩ :=
    exists_minimum_exact finiteGrammar finite_price_nonneg (finiteLeaf true)
      (finite_leaf_valid true)
  have hcost : cost finiteGrammar u ≤ 1 := by
    have h := hmin (finiteLeaf false) (finite_leaf_valid false) rfl (by simp)
    simpa [finiteLeaf, cost, finiteGrammar] using h
  refine ⟨u, hu, hq, ?_, ?_, le_antisymm hcost (finite_cost_lower_bound u), ?_⟩
  · simpa using hs
  · simpa using hb
  · intro v hv hqv hsv
    exact hmin v hv hqv (by simpa using hsv)

#print axioms infinite_every_tree_height_one
#print axioms infinite_strictly_cheaper
#print axioms infinite_no_minimum_exact
#print axioms finite_nonvacuity
end GuardedTree.AttainmentControls
