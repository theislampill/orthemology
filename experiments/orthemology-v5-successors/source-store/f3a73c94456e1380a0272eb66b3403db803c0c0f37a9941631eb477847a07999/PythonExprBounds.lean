import PythonExprMachine

/-! Input-dependent sufficient bounds for the exact expression algorithm model.
The required width deliberately excludes register reads and initial values.
-/
namespace P02.PythonExpr

def neededBits (d : Dictionary) : PyExpr → ℕ
  | .constant n => n.size
  | .reg _ => 0
  | .pow2 a => max (neededBits d a) (value a (dictionaryRead d) + 1)
  | .binary op a b => max (max (neededBits d a) (neededBits d b))
      (binaryValue op (value a (dictionaryRead d)) (value b (dictionaryRead d))).size

def Room (m : Meter) (ticks : ℕ) : Prop :=
  ∀ bound, m.limit = some bound → m.steps + ticks ≤ bound

def Width (m : Meter) (bits : ℕ) : Prop :=
  ∀ bound, m.maxBits = some bound → bits ≤ bound

theorem cost_positive (e : PyExpr) : 0 < cost e := by
  cases e <;> simp [cost]

theorem tick_of_room (m : Meter) (h : Room m 1) :
    tick m = .ok {m with steps := m.steps+1} :=
  (tick_ok_iff _ _).mpr ⟨rfl,h⟩

theorem check_of_width (m : Meter) (n : ℕ) (h : Width m n.size) : check m n = .ok n :=
  (check_ok_iff _ _ _).mpr ⟨rfl,h⟩

theorem power_of_width (m : Meter) (a : ℕ) (h : Width m (a+1)) : power m a = .ok (2^a) :=
  (power_ok_iff _ _ _).mpr ⟨rfl,h⟩

/-- Every finite expression succeeds under these input-dependent budgets,
including when dictionary values themselves exceed the specified width. -/
theorem reference_bounded (d : Dictionary) (e : PyExpr) (m : Meter)
    (hs : Room m (cost e)) (hb : Width m (neededBits d e)) :
    reference d e m = .ok (value e (dictionaryRead d), {m with steps := m.steps + cost e}) := by
  induction e generalizing m with
  | constant n =>
      have ht := tick_of_room m hs
      have hc := check_of_width {m with steps := m.steps+1} n hb
      simp [reference, ht, hc, value, cost]
  | reg r =>
      have ht := tick_of_room m hs
      simp [reference, ht, value, cost]
  | pow2 a ih =>
      have ht : Room m 1 := by
        intro bound hbound
        have h := hs bound hbound
        simp only [cost] at h
        omega
      have ha : Room {m with steps := m.steps+1} (cost a) := by
        intro bound hbound
        have h := hs bound hbound
        simp only [cost] at h
        change m.steps + 1 + cost a ≤ bound
        omega
      have hab : Width {m with steps := m.steps+1} (neededBits d a) := by
        intro bound hbound
        have h := hb bound hbound
        exact le_trans (Nat.le_max_left _ _) h
      have ht' : Room {m with steps := m.steps+1+cost a} 1 := by
        intro bound hbound
        have h := hs bound hbound
        simp only [cost] at h
        change m.steps + 1 + cost a + 1 ≤ bound
        omega
      have hp : Width {m with steps := m.steps+1+cost a+1}
          (value a (dictionaryRead d)+1) := by
        intro bound hbound
        have h := hb bound hbound
        exact le_trans (Nat.le_max_right _ _) h
      simp only [reference, tick_of_room m ht, result_bind_ok]
      rw [ih _ ha hab]
      simp only [result_bind_ok]
      rw [tick_of_room _ ht']
      simp only [result_bind_ok]
      rw [power_of_width _ _ hp]
      simp [value, cost, Nat.add_assoc]
  | binary op a b iha ihb =>
      have ht : Room m 1 := by
        intro bound hbound
        have h := hs bound hbound
        simp only [cost] at h
        omega
      have ha : Room {m with steps := m.steps+1} (cost a) := by
        intro bound hbound
        have h := hs bound hbound
        simp only [cost] at h
        change m.steps + 1 + cost a ≤ bound
        omega
      have hab : Width {m with steps := m.steps+1} (neededBits d a) := by
        intro bound hbound
        have h := hb bound hbound
        exact le_trans (le_trans (Nat.le_max_left _ _) (Nat.le_max_left _ _)) h
      have hb' : Room {m with steps := m.steps+1+cost a} (cost b) := by
        intro bound hbound
        have h := hs bound hbound
        simp only [cost] at h
        change m.steps + 1 + cost a + cost b ≤ bound
        omega
      have hbb : Width {m with steps := m.steps+1+cost a} (neededBits d b) := by
        intro bound hbound
        have h := hb bound hbound
        exact le_trans (le_trans (Nat.le_max_right _ _) (Nat.le_max_left _ _)) h
      have ht' : Room {m with steps := m.steps+1+cost a+cost b} 1 := by
        intro bound hbound
        have h := hs bound hbound
        simp only [cost] at h
        change m.steps + 1 + cost a + cost b + 1 ≤ bound
        omega
      have hc : Width {m with steps := m.steps+1+cost a+cost b+1}
          (binaryValue op (value a (dictionaryRead d)) (value b (dictionaryRead d))).size := by
        intro bound hbound
        have h := hb bound hbound
        exact le_trans (Nat.le_max_right _ _) h
      simp only [reference, tick_of_room m ht, result_bind_ok]
      rw [iha _ ha hab]
      simp only [result_bind_ok]
      rw [ihb _ hb' hbb]
      simp only [result_bind_ok]
      rw [tick_of_room _ ht']
      simp only [result_bind_ok]
      rw [check_of_width _ _ hc]
      simp [value, cost, Nat.add_assoc]

theorem expression_bounded (d : Dictionary) (e : PyExpr) (m : Meter)
    (hs : Room m (cost e)) (hb : Width m (neededBits d e)) :
    expression d e m = .ok (P02A2.ObserverCore.evalExpr (lower e) (dictionaryRead d),
      {m with steps := m.steps+cost e}) := by
  rw [expression_eq_reference, reference_bounded d e m hs hb, value_correct]

/-- The displayed bounds are finite naturals for each finite input; this says
nothing about one fixed finite budget serving all expressions and stores. -/
theorem expression_complete_finite (d : Dictionary) (e : PyExpr) (steps : ℕ) :
    expression d e ⟨some (steps+cost e), some (neededBits d e), steps⟩ =
      .ok (P02A2.ObserverCore.evalExpr (lower e) (dictionaryRead d),
        ⟨some (steps+cost e),some (neededBits d e),steps+cost e⟩) := by
  apply expression_bounded
  · intro bound h
    exact le_of_eq (Option.some.inj h)
  · intro bound h
    exact le_of_eq (Option.some.inj h)

end P02.PythonExpr
