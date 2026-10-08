import P02A2.ObserverCore
import Mathlib.Data.Nat.Size

/-! Source-bound mathematical model of prcodec.py:122–159, SHA-256
 dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c.
 Not a checked Python frontend or a physical-resource guarantee. Valid input
 domain: well-formed decoded expression tuples, exact built-in natural ints,
 natural-valued dictionaries, None/natural budgets, natural starting steps.
-/
namespace P02.PythonExpr

abbrev Dictionary := List (ℕ × ℕ)

def dictionaryRead : Dictionary → ℕ → ℕ
  | [], _ => 0
  | (r,v)::ds, j => if j = r then v else dictionaryRead ds j

/-- Overwriting removes older entries; dictionary insertion order is unobserved. -/
def dictionaryWrite (d : Dictionary) (r v : ℕ) : Dictionary :=
  (r,v) :: d.filter (fun p => p.1 != r)

private theorem dictionary_filter_read (d : Dictionary) (r j : ℕ) (h : j ≠ r) :
    dictionaryRead (d.filter (fun p => p.1 != r)) j = dictionaryRead d j := by
  induction d with
  | nil => rfl
  | cons p ds ih =>
      rcases p with ⟨k,v⟩
      by_cases hk : k = r
      · subst k
        simp [dictionaryRead, h, ih]
      · simp [dictionaryRead, hk, ih]

/-- Exact observable finite-map relation required by Python dict assignment. -/
theorem dictionary_read_write (d : Dictionary) (r v : ℕ) :
    dictionaryRead (dictionaryWrite d r v) = Function.update (dictionaryRead d) r v := by
  funext j
  by_cases h : j = r
  · subst j
    simp [dictionaryWrite, dictionaryRead]
  · simp [dictionaryWrite, dictionaryRead, h, dictionary_filter_read d r j h,
      Function.update_apply]

theorem dictionary_read_missing (d : Dictionary) (r : ℕ)
    (h : r ∉ d.map Prod.fst) : dictionaryRead d r = 0 := by
  induction d with
  | nil => rfl
  | cons p ds ih =>
      have hr : r ≠ p.1 := by intro he; apply h; simp [he]
      have ht : r ∉ ds.map Prod.fst := fun hm => h (by simp [hm])
      simp [dictionaryRead, hr, ih ht]

inductive Binary where
  | add | sub | mul | div | mod | le | eq
  deriving DecidableEq, Repr

inductive PyExpr where
  | constant : ℕ → PyExpr
  | reg : ℕ → PyExpr
  | binary : Binary → PyExpr → PyExpr → PyExpr
  | pow2 : PyExpr → PyExpr
  deriving DecidableEq, Repr

def binaryValue : Binary → ℕ → ℕ → ℕ
  | .add, a, b => a + b
  | .sub, a, b => a - b
  | .mul, a, b => a * b
  | .div, a, b => if b = 0 then 0 else a / b
  | .mod, a, b => if b = 0 then a else a % b
  | .le, a, b => if a ≤ b then 1 else 0
  | .eq, a, b => if a = b then 1 else 0

def lowerBinary : Binary → P02A2.ObserverCore.Expr → P02A2.ObserverCore.Expr →
    P02A2.ObserverCore.Expr
  | .add => .add
  | .sub => .sub
  | .mul => .mul
  | .div => .div
  | .mod => .mod
  | .le => .le
  | .eq => .eq

def lower : PyExpr → P02A2.ObserverCore.Expr
  | .constant n => .constant n
  | .reg r => .reg r
  | .binary op a b => lowerBinary op (lower a) (lower b)
  | .pow2 a => .pow2 (lower a)

def ofLean : P02A2.ObserverCore.Expr → PyExpr
  | .constant n => .constant n
  | .reg r => .reg r
  | .add a b => .binary .add (ofLean a) (ofLean b)
  | .sub a b => .binary .sub (ofLean a) (ofLean b)
  | .mul a b => .binary .mul (ofLean a) (ofLean b)
  | .div a b => .binary .div (ofLean a) (ofLean b)
  | .mod a b => .binary .mod (ofLean a) (ofLean b)
  | .le a b => .binary .le (ofLean a) (ofLean b)
  | .eq a b => .binary .eq (ofLean a) (ofLean b)
  | .pow2 a => .pow2 (ofLean a)

@[simp] theorem lower_ofLean (e : P02A2.ObserverCore.Expr) : lower (ofLean e) = e := by
  induction e <;> simp_all [ofLean, lower, lowerBinary]

def value : PyExpr → (ℕ → ℕ) → ℕ
  | .constant n, _ => n
  | .reg r, σ => σ r
  | .binary op a b, σ => binaryValue op (value a σ) (value b σ)
  | .pow2 a, σ => 2 ^ value a σ

theorem binaryValue_correct (op : Binary) (a b : P02A2.ObserverCore.Expr)
    (σ : P02A2.ObserverCore.Store) :
    binaryValue op (P02A2.ObserverCore.evalExpr a σ) (P02A2.ObserverCore.evalExpr b σ) =
      P02A2.ObserverCore.evalExpr (lowerBinary op a b) σ := by
  cases op <;> simp [binaryValue, lowerBinary, P02A2.ObserverCore.evalExpr]
  all_goals intro h; simp [h]

theorem value_correct (e : PyExpr) (σ : P02A2.ObserverCore.Store) :
    value e σ = P02A2.ObserverCore.evalExpr (lower e) σ := by
  induction e with
  | constant n => rfl
  | reg r => rfl
  | pow2 a ih => simp [value, lower, P02A2.ObserverCore.evalExpr, ih]
  | binary op a b iha ihb => simp [value, lower, iha, ihb, binaryValue_correct]

def cost : PyExpr → ℕ
  | .constant _ | .reg _ => 1
  | .binary _ a b => 1 + cost a + cost b + 1
  | .pow2 a => 1 + cost a + 1

structure Meter where
  limit : Option ℕ := none
  maxBits : Option ℕ := none
  steps : ℕ := 0
  deriving DecidableEq, Repr

inductive Fault where
  | stepLimit | integerStorage | exponentStorage | valueStackUnderflow | stackInvariant
  deriving DecidableEq, Repr

structure Failure where
  fault : Fault
  steps : ℕ
  deriving DecidableEq, Repr

abbrev Result (α : Type) := Except Failure α

@[simp] theorem result_bind_ok {α β : Type} (x : α) (f : α → Result β) :
    ((.ok x : Result α) >>= f) = f x := rfl
@[simp] theorem result_bind_error {α β : Type} (err : Failure) (f : α → Result β) :
    ((.error err : Result α) >>= f) = .error err := rfl
@[simp] theorem result_pure {α : Type} (x : α) : (pure x : Result α) = .ok x := rfl

def tick (m : Meter) : Result Meter :=
  let next := {m with steps := m.steps + 1}
  match m.limit with
  | none => .ok next
  | some limit => if next.steps ≤ limit then .ok next
      else .error ⟨.stepLimit, next.steps⟩

def check (m : Meter) (n : ℕ) : Result ℕ :=
  match m.maxBits with
  | none => .ok n
  | some bits => if n.size ≤ bits then .ok n
      else .error ⟨.integerStorage, m.steps⟩

/-- Source pre-check: a+1 precedes 1<<a; there is no generic result check. -/
def power (m : Meter) (a : ℕ) : Result ℕ :=
  match m.maxBits with
  | none => .ok (2 ^ a)
  | some bits => if a + 1 ≤ bits then .ok (2 ^ a)
      else .error ⟨.exponentStorage, m.steps⟩

/-- Recursive reference preserving precisely the source's meter ordering. -/
def reference (d : Dictionary) : PyExpr → Meter → Result (ℕ × Meter)
  | .constant n, m => do
      let m ← tick m
      let v ← check m n
      return (v,m)
  | .reg r, m => do
      let m ← tick m
      return (dictionaryRead d r,m)
  | .binary op a b, m => do
      let m ← tick m
      let (av,m) ← reference d a m
      let (bv,m) ← reference d b m
      let m ← tick m
      let v ← check m (binaryValue op av bv)
      return (v,m)
  | .pow2 a, m => do
      let m ← tick m
      let (av,m) ← reference d a m
      let m ← tick m
      let v ← power m av
      return (v,m)

@[simp] theorem tick_ok_iff (m n : Meter) :
    tick m = .ok n ↔ n = {m with steps := m.steps + 1} ∧
      (∀ bound, m.limit = some bound → m.steps + 1 ≤ bound) := by
  cases hl : m.limit with
  | none => simp [tick, hl, eq_comm]
  | some bound =>
      by_cases h : m.steps + 1 ≤ bound
      · simp [tick, hl, h, eq_comm]
      · simp [tick, hl, h]

@[simp] theorem check_ok_iff (m : Meter) (n v : ℕ) :
    check m n = .ok v ↔ v = n ∧ (∀ bits, m.maxBits = some bits → n.size ≤ bits) := by
  cases hb : m.maxBits with
  | none => simp [check, hb, eq_comm]
  | some bits =>
      by_cases h : n.size ≤ bits <;> simp [check, hb, h, eq_comm]

@[simp] theorem power_ok_iff (m : Meter) (a v : ℕ) :
    power m a = .ok v ↔ v = 2 ^ a ∧ (∀ bits, m.maxBits = some bits → a+1 ≤ bits) := by
  cases hb : m.maxBits with
  | none => simp [power, hb, eq_comm]
  | some bits =>
      by_cases h : a+1 ≤ bits <;> simp [power, hb, h, eq_comm]

/-- The power pre-check is exactly the natural result width, although its fault
kind and allocation order remain different from the generic check. -/
theorem power_width (a : ℕ) : (2 ^ a).size = a + 1 := Nat.size_pow

theorem reference_spec (d : Dictionary) (e : PyExpr) (m out : Meter) (v : ℕ)
    (h : reference d e m = .ok (v,out)) :
    v = value e (dictionaryRead d) ∧ out = {m with steps := m.steps + cost e} := by
  induction e generalizing m out v with
  | constant n =>
      cases ht : tick m with
      | error err => simp [reference, ht] at h
      | ok m' =>
          obtain ⟨rfl,_⟩ := (tick_ok_iff m m').mp ht
          cases hc : check {m with steps := m.steps + 1} n with
          | error err => simp [reference, ht, hc] at h
          | ok w =>
              have hw := (check_ok_iff _ _ _).mp hc
              simp [reference, ht, hc] at h
              rcases h with ⟨rfl,rfl⟩
              exact ⟨hw.1, rfl⟩
  | reg r =>
      cases ht : tick m with
      | error err => simp [reference, ht] at h
      | ok m' =>
          obtain ⟨rfl,_⟩ := (tick_ok_iff m m').mp ht
          simp [reference, ht] at h
          rcases h with ⟨rfl,rfl⟩
          exact ⟨rfl,rfl⟩
  | pow2 a ih =>
      cases ht : tick m with
      | error err => simp [reference, ht] at h
      | ok m' =>
          obtain ⟨rfl,_⟩ := (tick_ok_iff m m').mp ht
          cases ha : reference d a {m with steps := m.steps + 1} with
          | error err => simp [reference, ht, ha] at h
          | ok z =>
              rcases z with ⟨av,am⟩
              obtain ⟨rfl,rfl⟩ := ih _ _ _ ha
              cases ht' : tick {m with steps := m.steps + 1 + cost a} with
              | error err => simp [reference, ht, ha, ht'] at h
              | ok m' =>
                  obtain ⟨rfl,_⟩ := (tick_ok_iff _ _).mp ht'
                  cases hp : power {m with steps := m.steps + 1 + cost a + 1}
                      (value a (dictionaryRead d)) with
                  | error err => simp [reference, ht, ha, ht', hp] at h
                  | ok w =>
                      have hw := (power_ok_iff _ _ _).mp hp
                      simp [reference, ht, ha, ht', hp] at h
                      rcases h with ⟨rfl,rfl⟩
                      constructor
                      · exact hw.1
                      · simp [cost, Nat.add_assoc]
  | binary op a b iha ihb =>
      cases ht : tick m with
      | error err => simp [reference, ht] at h
      | ok m' =>
          obtain ⟨rfl,_⟩ := (tick_ok_iff m m').mp ht
          cases ha : reference d a {m with steps := m.steps + 1} with
          | error err => simp [reference, ht, ha] at h
          | ok z =>
              rcases z with ⟨av,am⟩
              obtain ⟨rfl,rfl⟩ := iha _ _ _ ha
              cases hb : reference d b {m with steps := m.steps + 1 + cost a} with
              | error err => simp [reference, ht, ha, hb] at h
              | ok z =>
                  rcases z with ⟨bv,bm⟩
                  obtain ⟨rfl,rfl⟩ := ihb _ _ _ hb
                  cases ht' : tick {m with steps := m.steps + 1 + cost a + cost b} with
                  | error err => simp [reference, ht, ha, hb, ht'] at h
                  | ok m' =>
                      obtain ⟨rfl,_⟩ := (tick_ok_iff _ _).mp ht'
                      cases hc : check {m with steps := m.steps + 1 + cost a + cost b + 1}
                          (binaryValue op (value a (dictionaryRead d)) (value b (dictionaryRead d))) with
                      | error err => simp [reference, ht, ha, hb, ht', hc] at h
                      | ok w =>
                          have hw := (check_ok_iff _ _ _).mp hc
                          simp [reference, ht, ha, hb, ht', hc] at h
                          rcases h with ⟨rfl,rfl⟩
                          constructor
                          · exact hw.1
                          · simp [cost, Nat.add_assoc]

theorem reference_unbounded (d : Dictionary) (e : PyExpr) (steps : ℕ) :
    reference d e ⟨none,none,steps⟩ =
      .ok (value e (dictionaryRead d), ⟨none,none,steps + cost e⟩) := by
  induction e generalizing steps with
  | constant n => rfl
  | reg r => rfl
  | pow2 a ih => simp [reference, tick, ih, power, value, cost, Nat.add_assoc]
  | binary op a b iha ihb =>
      simp [reference, tick, iha, ihb, check, value, cost, Nat.add_assoc]

end P02.PythonExpr
