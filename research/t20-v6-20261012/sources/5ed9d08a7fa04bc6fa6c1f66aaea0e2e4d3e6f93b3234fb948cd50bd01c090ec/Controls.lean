import Stability
import Mathlib.Tactic.NormNum

namespace GuardedTree.SaturationControls
open Tree Saturation

/-- A sole unary self-cycle has no finite tree witness. -/
abbrev unsupported : Grammar Unit Unit Unit where
  arity _ := 1
  head _ := ()
  premise _ _ := ()
  localSupport _ := ∅
  price _ := 0
  guard _ _ := True

theorem unsupported_no_tree (t : Tree unsupported) : False := by
  induction t with
  | node r child ih => exact ih 0

theorem unsupported_all_rounds (h : ℕ) (q : Unit) (S : Finset Unit) :
    round unsupported h q S = none := by
  apply (round_none_iff unsupported h q S).mpr
  rintro ⟨t, _⟩
  exact unsupported_no_tree t

/-- Boolean rule false is an allowed nullary base; true is a zero self-cycle. -/
abbrev zeroCycle : Grammar Unit Unit Bool where
  arity r := if r then 1 else 0
  head _ := ()
  premise _ _ := ()
  localSupport _ := ∅
  price _ := 0
  guard _ _ := True

def zeroLeaf : Tree zeroCycle := .node false Fin.elim0

theorem zeroLeaf_facts : Bounded zeroCycle 1 zeroLeaf ∧ Valid zeroCycle zeroLeaf ∧
    judgement zeroCycle zeroLeaf = () ∧ support zeroCycle zeroLeaf = ∅ ∧
    cost zeroCycle zeroLeaf = 0 := by
  refine ⟨bounded_node zeroCycle 0 false Fin.elim0 (fun i => Fin.elim0 i), ?_⟩
  simp [zeroLeaf, zeroCycle, Valid, judgement, support, cost]

theorem zero_cycle_minimum (h : ℕ) : round zeroCycle (h + 1) () ∅ = some 0 := by
  apply (round_some_iff zeroCycle (h + 1) () ∅ 0).mpr
  refine ⟨⟨zeroLeaf, bounded_mono zeroCycle (by omega) zeroLeaf_facts.1,
    zeroLeaf_facts.2⟩, ?_⟩
  intro t _ _ _ _
  exact cost_nonneg zeroCycle (fun _ => le_rfl) t

/-- A false nullary guard is checked on the empty tuple and never seeds a key. -/
abbrev blockedNullary : Grammar Unit Unit Unit where
  arity _ := 0
  head _ := ()
  premise _ _ := ()
  localSupport _ := ∅
  price _ := 0
  guard _ _ := False

theorem blocked_nullary (h : ℕ) : round blockedNullary h () ∅ = none := by
  apply (round_none_iff blockedNullary h () ∅).mpr
  rintro ⟨t, _, hv, _⟩
  cases t with
  | node r child => exact hv.2

/-- Both judgements are seeded at round one, but the expensive true key is
improved at round two through the cheap false premise. Extra unary self-rule
for false is harmless. All local prices are nonnegative. -/
abbrev priceDrop : Grammar Bool Unit (Bool × Bool) where
  arity r := if r.1 then 1 else 0
  head r := r.2
  premise _ _ := false
  localSupport _ := ∅
  price r := if r.1 then 0 else if r.2 then 10 else 1
  guard _ _ := True

theorem priceDrop_nonnegative (r : Bool × Bool) : 0 ≤ priceDrop.price r := by
  rcases r with ⟨a, b⟩
  cases a <;> cases b <;> norm_num [priceDrop]

def priceLeaf (q : Bool) : Tree priceDrop := .node (false, q) Fin.elim0
def cheapTrue : Tree priceDrop := .node (true, true) (fun _ => priceLeaf false)

theorem priceLeaf_facts (q : Bool) :
    Bounded priceDrop 1 (priceLeaf q) ∧ Valid priceDrop (priceLeaf q) ∧
    judgement priceDrop (priceLeaf q) = q ∧ support priceDrop (priceLeaf q) = ∅ ∧
    cost priceDrop (priceLeaf q) = (if q then 10 else 1) := by
  refine ⟨bounded_node priceDrop 0 (false, q) Fin.elim0 (fun i => Fin.elim0 i), ?_⟩
  simp [priceLeaf, priceDrop, Valid, judgement, support, cost]

theorem priceDrop_support (t : Tree priceDrop) : support priceDrop t = ∅ := by
  induction t with
  | node r child ih =>
    simp only [support, priceDrop, Finset.empty_union, ih]
    ext e
    simp

theorem priceDrop_cost_ge_one (t : Tree priceDrop) : 1 ≤ cost priceDrop t := by
  induction t with
  | node r child ih =>
    rcases r with ⟨a, b⟩
    cases a
    · have hp : 1 ≤ priceDrop.price (false, b) := by cases b <;> norm_num [priceDrop]
      exact hp.trans (le_add_of_nonneg_right
        (Finset.sum_nonneg (fun i _ => (by norm_num : (0 : ℚ) ≤ 1).trans (ih i))))
    · let i : Fin (priceDrop.arity (true, b)) := ⟨0, by simp [priceDrop]⟩
      have hsingle := Finset.single_le_sum
        (fun j (_ : j ∈ (Finset.univ : Finset (Fin (priceDrop.arity (true, b))))) =>
          (by norm_num : (0 : ℚ) ≤ 1).trans (ih j)) (Finset.mem_univ i)
      simpa only [cost, priceDrop, Bool.true_eq, ↓reduceIte, zero_add] using
        (ih i).trans hsingle

theorem priceDrop_height_one (t : Tree priceDrop) (hb : Bounded priceDrop 1 t) :
    cost priceDrop t = (if judgement priceDrop t then 10 else 1) := by
  cases t with
  | node r child =>
    rcases r with ⟨a, b⟩
    cases a
    · change (if b then 10 else 1) + (∑ i : Fin 0, cost priceDrop (child i)) =
        (if b then 10 else 1)
      simp
    · let i : Fin (priceDrop.arity (true, b)) := ⟨0, by simp [priceDrop]⟩
      have hh := bounded_child priceDrop 0 (true, b) child hb i
      have hf := hh [child i] (.root (child i))
      simp at hf

theorem first_true_price : round priceDrop 1 true ∅ = some 10 := by
  apply (round_some_iff priceDrop 1 true ∅ 10).mpr
  refine ⟨⟨priceLeaf true, (priceLeaf_facts true).1, (priceLeaf_facts true).2⟩, ?_⟩
  intro t hb _ hq _
  have hc := priceDrop_height_one t hb
  simpa only [hq, Bool.true_eq, ↓reduceIte, hc] using (le_refl (10 : ℚ))

theorem cheapTrue_facts : Bounded priceDrop 2 cheapTrue ∧ Valid priceDrop cheapTrue ∧
    judgement priceDrop cheapTrue = true ∧ support priceDrop cheapTrue = ∅ ∧
    cost priceDrop cheapTrue = 1 := by
  refine ⟨bounded_node priceDrop 1 (true, true) (fun _ => priceLeaf false)
    (fun _ => (priceLeaf_facts false).1), ?_⟩
  simp [cheapTrue, priceLeaf, priceDrop, Valid, judgement, support, cost]

theorem second_true_price : round priceDrop 2 true ∅ = some 1 := by
  apply (round_some_iff priceDrop 2 true ∅ 1).mpr
  exact ⟨⟨cheapTrue, cheapTrue_facts⟩, fun t _ _ _ _ => priceDrop_cost_ge_one t⟩

def Reached {J E : Type*} (D : Table (J := J) (E := E)) (q : J) (S : Finset E) : Prop :=
  ∃ c, D q S = some c

theorem priceDrop_keys (h : ℕ) (q : Bool) (S : Finset Unit) :
    Reached (round priceDrop (h + 1)) q S ↔ S = ∅ := by
  constructor
  · rintro ⟨c, hc⟩
    obtain ⟨t, _, _, _, hs, _⟩ := (round_correct priceDrop (h + 1)).1 q S c hc
    exact hs.symm.trans (priceDrop_support t)
  · intro hs
    subst S
    obtain ⟨c, hc, _⟩ := (round_correct priceDrop (h + 1)).2 (priceLeaf q)
      (bounded_mono priceDrop (by omega) (priceLeaf_facts q).1) (priceLeaf_facts q).2.1
    exact ⟨c, by simpa only [(priceLeaf_facts q).2.2.1,
      (priceLeaf_facts q).2.2.2.1] using hc⟩

/-- Key stability is strictly weaker than equality of the numeric table. -/
theorem same_keys_but_price_changes :
    (∀ q S, Reached (round priceDrop 1) q S ↔ Reached (round priceDrop 2) q S) ∧
      round priceDrop 1 ≠ round priceDrop 2 := by
  constructor
  · intro q S
    exact (priceDrop_keys 0 q S).trans (priceDrop_keys 1 q S).symm
  · intro heq
    have h := congrFun (congrFun heq true) ∅
    rw [first_true_price, second_true_price] at h
    norm_num at h

#print axioms unsupported_all_rounds
#print axioms zero_cycle_minimum
#print axioms blocked_nullary
#print axioms same_keys_but_price_changes
end GuardedTree.SaturationControls
