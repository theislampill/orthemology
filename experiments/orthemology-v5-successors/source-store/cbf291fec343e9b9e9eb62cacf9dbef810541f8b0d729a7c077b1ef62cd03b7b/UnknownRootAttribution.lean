import CoveringCore

/-!
One unknown correlated label class. This file formalizes the pulled-back
tainted-label budget, the resulting sound overlap/cancellation witnesses,
cardinal resource arithmetic, and the realization of a maximal label-fault set
by one class-root plus singleton roots. The sharp cross-image iff and arbitrary
fixed-family lower bound are ordinary proofs in the frozen theorem text.
-/

namespace UnknownRootAttribution
open ChargedInterlock

def rootOf (a : Nat → Bool) (representative i : Nat) : Nat :=
  if a i then representative else i

def pulledFault (a : Nat → Bool) (representative : Nat) (fault : Nat → Bool) : Nat → Bool :=
  fun i => fault (rootOf a representative i)

theorem card_congr (n : Nat) (p q : Nat → Bool)
    (same : ∀ i, i < n → p i = q i) : card n p = card n q := by
  induction n with
  | zero => rfl
  | succ n ih =>
    have hprev : ∀ i, i < n → p i = q i := by
      intro i hi
      exact same i (by omega)
    have hn := same n (by omega)
    simp [card, hn, ih hprev]

theorem card_positive (n : Nat) (p : Nat → Bool) (i : Nat)
    (bound : i < n) (member : p i = true) : 1 ≤ card n p := by
  induction n with
  | zero => omega
  | succ n ih =>
    by_cases hi : i < n
    · have h := ih hi
      cases hn : p n <;> simp [card, hn] <;> omega
    · have heq : i = n := by omega
      subst i
      simp [card, member]

theorem card_union_inter (n : Nat) (p q : Nat → Bool) :
    card n (fun i => p i || q i) + card n (fun i => p i && q i) =
      card n p + card n q := by
  induction n with
  | zero => rfl
  | succ n ih =>
    cases hp : p n <;> cases hq : q n <;> simp_all [card] <;> omega

theorem card_singleton (n r : Nat) :
    card n (fun i => decide (i = r)) = if r < n then 1 else 0 := by
  induction n with
  | zero => simp [card]
  | succ n ih =>
    by_cases hr : r < n
    · have hne : n ≠ r := by omega
      have hrs : r < n+1 := by omega
      simp [card, ih, hr, hrs, hne]
    · by_cases heq : r = n
      · subst r
        simp [card, ih]
      · have hne : n ≠ r := by omega
        have hnot : ¬r < n+1 := by omega
        simp [card, ih, hr, hne, hnot]

theorem tainted_label_budget (m b c representative : Nat)
    (a fault : Nat → Bool)
    (repBound : representative < m) (repMember : a representative = true)
    (classSize : card m a = c) (classPositive : 0 < c)
    (rootBudget : card m fault ≤ b) :
    card m (pulledFault a representative fault) ≤ b+c-1 := by
  cases repFault : fault representative with
  | false =>
    have included : ∀ i, i < m → pulledFault a representative fault i = true → fault i = true := by
      intro i _hi hf
      cases ha : a i <;> simp_all [pulledFault, rootOf]
    have bound := card_mono m (pulledFault a representative fault) fault included
    omega
  | true =>
    have included : ∀ i, i < m → pulledFault a representative fault i = true →
        (a i || fault i) = true := by
      intro i _hi hf
      cases ha : a i <;> simp_all [pulledFault, rootOf]
    have bound := card_mono m (pulledFault a representative fault)
      (fun i => a i || fault i) included
    have overlap : 1 ≤ card m (fun i => a i && fault i) :=
      card_positive m (fun i => a i && fault i) representative repBound (by simp [repMember, repFault])
    have total := card_union_inter m a fault
    omega

theorem sound_unknown_map_overlap (m b c representative : Nat)
    (a fault l s : Nat → Bool)
    (repBound : representative < m) (repMember : a representative = true)
    (classSize : card m a = c) (classPositive : 0 < c)
    (rootBudget : card m fault ≤ b)
    (largeOverlap : m+(b+c-1) < card m l+card m s) :
    ∃ i, i < m ∧ l i = true ∧ s i = true ∧ fault (rootOf a representative i) = false := by
  have labelBudget := tainted_label_budget m b c representative a fault
    repBound repMember classSize classPositive rootBudget
  exact honest_overlap m (b+c-1) l s (pulledFault a representative fault)
    labelBudget largeOverlap

theorem sound_unknown_map_cancellation (m b c representative : Nat)
    (a fault acknowledgers : Nat → Bool)
    (repBound : representative < m) (repMember : a representative = true)
    (classSize : card m a = c) (classPositive : 0 < c)
    (rootBudget : card m fault ≤ b)
    (enoughLabels : b+c-1 < card m acknowledgers) :
    ∃ i, i < m ∧ acknowledgers i = true ∧ fault (rootOf a representative i) = false := by
  have labelBudget := tainted_label_budget m b c representative a fault
    repBound repMember classSize classPositive rootBudget
  exact honest_on_large_path m (b+c-1) acknowledgers
    (pulledFault a representative fault) labelBudget enoughLabels

def realizingFault (taint a : Nat → Bool) (representative : Nat) : Nat → Bool :=
  fun i => (taint i && !a i) || decide (i = representative)

theorem realization_labelwise (m representative : Nat) (taint a : Nat → Bool)
    (repMember : a representative = true)
    (subset : ∀ i, i < m → a i = true → taint i = true) :
    ∀ i, i < m → pulledFault a representative (realizingFault taint a representative) i = taint i := by
  intro i hi
  cases ha : a i with
  | true =>
    have ht := subset i hi ha
    simp [pulledFault, rootOf, realizingFault, ha, ht]
  | false =>
    have hne : i ≠ representative := by
      intro heq
      subst i
      simp_all
    simp [pulledFault, rootOf, realizingFault, ha, hne]

theorem realization_root_cardinality (m b c representative : Nat) (taint a : Nat → Bool)
    (repBound : representative < m) (repMember : a representative = true)
    (subset : ∀ i, i < m → a i = true → taint i = true)
    (classSize : card m a = c) (taintSize : card m taint = b+c-1)
    (classPositive : 0 < c) (_budgetPositive : 0 < b) :
    card m (realizingFault taint a representative) = b := by
  let difference : Nat → Bool := fun i => taint i && !a i
  have disjointClass : ∀ i, i < m → difference i = true → a i = false := by
    intro i _hi hd
    cases ha : a i <;> simp_all [difference]
  have sameUnion : ∀ i, i < m → (difference i || a i) = taint i := by
    intro i hi
    have sub := subset i hi
    cases ha : a i <;> cases ht : taint i <;> simp_all [difference]
  have unionCount := card_congr m (fun i => difference i || a i) taint sameUnion
  have differenceCount := card_disjoint_union m difference a disjointClass
  have disjointSingleton : ∀ i, i < m → difference i = true → decide (i=representative) = false := by
    intro i hi hd
    have ha := disjointClass i hi hd
    have hne : i ≠ representative := by
      intro heq
      subst i
      simp_all
    simp [hne]
  have faultCount := card_disjoint_union m difference
    (fun i => decide (i=representative)) disjointSingleton
  have singletonCount := card_singleton m representative
  have single : card m (fun i => decide (i=representative)) = 1 := by
    simpa [repBound] using singletonCount
  change card m (fun i => difference i || decide (i=representative)) =
    card m difference + card m (fun i => decide (i=representative)) at faultCount
  rw [single] at faultCount
  change card m (fun i => difference i || decide (i=representative)) = b
  rw [faultCount]
  omega

theorem exact_minimum_actual_root_count (b c : Nat)
    (hb : 0 < b) (hc : 0 < c) :
    (3*(b+c-1)+1)-c+1 = 3*b+2*c-1 := by omega

theorem threshold_actual_root_lower_bound (m b c q r : Nat)
    (_hb : 0 < b) (hc : 0 < c)
    (h : ThresholdContract m (b+c-1) q r) :
    3*b+2*c-1 ≤ m-c+1 := by
  have minimum := minimum_roots h
  omega

#print axioms tainted_label_budget
#print axioms sound_unknown_map_overlap
#print axioms sound_unknown_map_cancellation
#print axioms realization_labelwise
#print axioms realization_root_cardinality
#print axioms exact_minimum_actual_root_count
#print axioms threshold_actual_root_lower_bound

end UnknownRootAttribution
