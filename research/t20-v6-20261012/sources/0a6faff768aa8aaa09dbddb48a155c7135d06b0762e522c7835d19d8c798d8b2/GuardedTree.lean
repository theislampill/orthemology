import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Tauto
import Mathlib.Tactic.Linarith

/-! Structural core of exact-support guarded tree compilation. No semantic
interpretation, source authentication, or admission soundness is asserted. -/
namespace GuardedTree

universe u v w

structure Grammar (J : Type u) (E : Type v) (R : Type w) where
  arity : R → ℕ
  head : R → J
  premise : (r : R) → Fin (arity r) → J
  localSupport : R → Finset E
  price : R → ℚ
  guard : (r : R) → (Fin (arity r) → Finset E) → Prop

inductive Tree {J E R : Type*} (G : Grammar J E R) : Type _
  | node (r : R) (child : Fin (G.arity r) → Tree G) : Tree G

variable {J E R : Type*} [DecidableEq E] (G : Grammar J E R)

namespace Tree

def judgement : Tree G → J
  | .node r _ => G.head r

def support : Tree G → Finset E
  | .node r child => G.localSupport r ∪ Finset.univ.biUnion (fun i => support (child i))

def cost : Tree G → ℚ
  | .node r child => G.price r + ∑ i, cost (child i)

def nodes : Tree G → ℕ
  | .node _ child => 1 + ∑ i, nodes (child i)

def Valid : Tree G → Prop
  | .node r child =>
    (∀ i, Valid (child i) ∧ judgement G (child i) = G.premise r i) ∧
    G.guard r (fun i => support G (child i))

end Tree
open Tree

/-- A context retains rule labels, ordered sibling positions, and all siblings.
Only its unique distinguished occurrence is filled. -/
inductive Context : Type _
  | hole : Context
  | step (r : R) (i : Fin (G.arity r))
      (siblings : Fin (G.arity r) → Tree G) (inner : Context) : Context

namespace Context

def fill : Context G → Tree G → Tree G
  | .hole, t => t
  | .step r i siblings inner, t =>
    .node r (Function.update siblings i (fill inner t))

end Context

/-- Extensional node congruence uses each premise position separately. -/
theorem node_replacement (r : R) (a b : Fin (G.arity r) → Tree G)
    (ha : Valid G (.node r a)) (hb : ∀ i, Valid G (b i))
    (hq : ∀ i, judgement G (b i) = judgement G (a i))
    (hs : ∀ i, support G (b i) = support G (a i)) :
    Valid G (.node r b) ∧ support G (.node r b) = support G (.node r a) := by
  have ht : (fun i => support G (b i)) = (fun i => support G (a i)) := funext hs
  constructor
  · exact ⟨fun i => ⟨hb i, (hq i).trans (ha.1 i).2⟩, ht ▸ ha.2⟩
  · simp only [support, ht]

/-- Replacing a valid subtree with the same state preserves every surviving
ordered guard, rather than assuming validity of the resulting tree. -/
theorem context_replacement (C : Context G) (a b : Tree G)
    (hC : Valid G (C.fill G a)) (hb : Valid G b)
    (hq : judgement G b = judgement G a) (hs : support G b = support G a) :
    Valid G (C.fill G b) ∧
      judgement G (C.fill G b) = judgement G (C.fill G a) ∧
      support G (C.fill G b) = support G (C.fill G a) := by
  induction C with
  | hole => exact ⟨hb, hq, hs⟩
  | step r i siblings inner ih =>
    have hi : Valid G (inner.fill G a) := by
      simpa [Context.fill] using (hC.1 i).1
    obtain ⟨hv, hj, hs'⟩ := ih hi
    have hnew := node_replacement G r
      (Function.update siblings i (inner.fill G a))
      (Function.update siblings i (inner.fill G b)) hC
      (fun j => by
        by_cases hji : j = i
        · subst j; simpa using hv
        · simpa [Function.update_of_ne hji] using (hC.1 j).1)
      (fun j => by
        by_cases hji : j = i
        · subst j; simpa using hj
        · simp [Function.update_of_ne hji])
      (fun j => by
        by_cases hji : j = i
        · subst j; simpa using hs'
        · simp [Function.update_of_ne hji])
    exact ⟨hnew.1, rfl, hnew.2⟩

theorem valid_hole (C : Context G) (a : Tree G)
    (h : Valid G (C.fill G a)) : Valid G a := by
  induction C with
  | hole => exact h
  | step r i siblings inner ih =>
    apply ih
    simpa [Context.fill] using (h.1 i).1

omit [DecidableEq E] in
/-- Any subtree improvement propagates to the whole occurrence-additive tree. -/
theorem context_cost_mono (C : Context G) (a b : Tree G)
    (h : cost G b ≤ cost G a) : cost G (C.fill G b) ≤ cost G (C.fill G a) := by
  induction C with
  | hole => exact h
  | step r i siblings inner ih =>
    apply add_le_add_left
    apply Finset.sum_le_sum
    intro j _
    by_cases hji : j = i
    · subst j; simpa using ih
    · simp [Function.update_of_ne hji]

omit [DecidableEq E] in
theorem cost_nonneg (hw : ∀ r, 0 ≤ G.price r) (a : Tree G) : 0 ≤ cost G a := by
  induction a with
  | node r child ih =>
    exact add_nonneg (hw r) (Finset.sum_nonneg (fun i _ => ih i))

omit [DecidableEq E] in
/-- Nonnegative occurrence prices imply every retained descendant is no dearer. -/
theorem hole_cost_le (hw : ∀ r, 0 ≤ G.price r) (C : Context G) (a : Tree G) :
    cost G a ≤ cost G (C.fill G a) := by
  induction C with
  | hole => exact le_rfl
  | step r i siblings inner ih =>
    have hi : cost G (inner.fill G a) ≤
        ∑ j, cost G (Function.update siblings i (inner.fill G a) j) := by
      simpa using (Finset.single_le_sum
        (fun j (_ : j ∈ (Finset.univ : Finset (Fin (G.arity r)))) =>
          cost_nonneg G hw (Function.update siblings i (inner.fill G a) j))
        (Finset.mem_univ i))
    exact ih.trans (hi.trans (le_add_of_nonneg_left (hw r)))

omit [DecidableEq E] in
theorem hole_nodes_le (C : Context G) (a : Tree G) :
    nodes G a ≤ nodes G (C.fill G a) := by
  induction C with
  | hole => exact le_rfl
  | step r i siblings inner ih =>
    have hi : nodes G (inner.fill G a) ≤
        ∑ j, nodes G (Function.update siblings i (inner.fill G a) j) := by
      simpa using (Finset.single_le_sum
        (fun j (_ : j ∈ (Finset.univ : Finset (Fin (G.arity r)))) =>
          Nat.zero_le (nodes G (Function.update siblings i (inner.fill G a) j)))
        (Finset.mem_univ i))
    exact ih.trans (hi.trans (Nat.le_add_left _ 1))

omit [DecidableEq E] in
theorem proper_hole_nodes_lt (C : Context G) (a : Tree G) (hC : C ≠ .hole) :
    nodes G a < nodes G (C.fill G a) := by
  cases C with
  | hole => exact False.elim (hC rfl)
  | step r i siblings inner =>
    have hi : nodes G (inner.fill G a) ≤
        ∑ j, nodes G (Function.update siblings i (inner.fill G a) j) := by
      simpa using (Finset.single_le_sum
        (fun j (_ : j ∈ (Finset.univ : Finset (Fin (G.arity r)))) =>
          Nat.zero_le (nodes G (Function.update siblings i (inner.fill G a) j)))
        (Finset.mem_univ i))
    exact (hole_nodes_le G inner a).trans_lt
      (hi.trans_lt (by simp [Context.fill, nodes, Nat.add_comm]))

/-- One genuine pruning step: descendant validity is derived from ancestor
validity; cost and strict size decrease are proved structurally. -/
theorem prune_equal_state (hw : ∀ r, 0 ≤ G.price r)
    (C : Context G) (d : Tree G) (hC : C ≠ .hole)
    (hv : Valid G (C.fill G d))
    (hq : judgement G d = judgement G (C.fill G d))
    (hs : support G d = support G (C.fill G d)) :
    Valid G d ∧ judgement G d = judgement G (C.fill G d) ∧
    support G d = support G (C.fill G d) ∧
    cost G d ≤ cost G (C.fill G d) ∧ nodes G d < nodes G (C.fill G d) :=
  ⟨valid_hole G C d hv, hq, hs, hole_cost_le G hw C d, proper_hole_nodes_lt G C d hC⟩

omit [DecidableEq E] in
theorem context_nodes_strict_mono (C : Context G) (a b : Tree G)
    (h : nodes G b < nodes G a) : nodes G (C.fill G b) < nodes G (C.fill G a) := by
  induction C with
  | hole => exact h
  | step r i siblings inner ih =>
    apply Nat.add_lt_add_left
    apply Finset.sum_lt_sum
    · intro j _
      by_cases hji : j = i
      · subst j; simpa using ih.le
      · simp [Function.update_of_ne hji]
    · exact ⟨i, Finset.mem_univ i, by simpa using ih⟩

/-- No proper ancestor/descendant pair, anywhere in this tree, has equal state. -/
def Reduced (t : Tree G) : Prop :=
  ∀ (outer inner : Context G) (d : Tree G), inner ≠ .hole →
    t = outer.fill G (inner.fill G d) →
    ¬ (judgement G d = judgement G (inner.fill G d) ∧
       support G d = support G (inner.fill G d))

/-- Well-founded occurrence minimization derives a no-repeat normal form. It
assumes neither a finite catalogue nor an already normalized input family. -/
theorem exists_reduced_representative (hw : ∀ r, 0 ≤ G.price r)
    (t : Tree G) (ht : Valid G t) :
    ∃ u : Tree G, Valid G u ∧ judgement G u = judgement G t ∧
      support G u = support G t ∧ cost G u ≤ cost G t ∧ Reduced G u := by
  classical
  let P : ℕ → Prop := fun n => ∃ u : Tree G,
    Valid G u ∧ judgement G u = judgement G t ∧ support G u = support G t ∧
      cost G u ≤ cost G t ∧ nodes G u = n
  have hex : ∃ n, P n := ⟨nodes G t, t, ht, rfl, rfl, le_rfl, rfl⟩
  obtain ⟨u, hu, hq, hs, hc, hn⟩ := Nat.find_spec hex
  refine ⟨u, hu, hq, hs, hc, ?_⟩
  intro outer inner d hinner heq hstate
  have hOuter : Valid G (outer.fill G (inner.fill G d)) := heq ▸ hu
  have hInner := valid_hole G outer (inner.fill G d) hOuter
  have hD := valid_hole G inner d hInner
  obtain ⟨hv, hqv, hsv⟩ := context_replacement G outer (inner.fill G d) d
    hOuter hD hstate.1 hstate.2
  have hcv : cost G (outer.fill G d) ≤ cost G u := by
    rw [heq]
    exact context_cost_mono G outer (inner.fill G d) d (hole_cost_le G hw inner d)
  have hnv : nodes G (outer.fill G d) < nodes G u := by
    rw [heq]
    exact context_nodes_strict_mono G outer (inner.fill G d) d
      (proper_hole_nodes_lt G inner d hinner)
  have hvP : P (nodes G (outer.fill G d)) :=
    ⟨outer.fill G d, hv, hqv.trans ((congrArg (judgement G) heq).symm.trans hq),
      hsv.trans ((congrArg (support G) heq).symm.trans hs), hcv.trans hc, rfl⟩
  exact (Nat.not_lt_of_ge (Nat.find_min' hex hvP)) (hn ▸ hnv)

#print axioms context_replacement
#print axioms prune_equal_state
#print axioms exists_reduced_representative
end GuardedTree
