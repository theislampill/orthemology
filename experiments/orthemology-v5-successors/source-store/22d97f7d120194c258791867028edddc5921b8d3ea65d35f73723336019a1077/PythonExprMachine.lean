import PythonExprCore

/-! The source-shaped work/value-stack machine. Stack heads correspond to the
Python list ends. Source guards and their fault kinds precede no extra checks.
The fuel below counts microsteps of this model; it is not the old callFuel.
-/
namespace P02.PythonExpr

structure Config where
  work : List (PyExpr × Bool)
  vals : List ℕ
  meter : Meter
  deriving DecidableEq, Repr

/-- Popped work ticks before tag dispatch, including the ready visit. -/
def step (d : Dictionary) (c : Config) : Result Config :=
  match c.work with
  | [] => .ok c
  | (e,ready)::tail => do
      let m ← tick c.meter
      match e with
      | .constant n =>
          let v ← check m n
          return ⟨tail,v::c.vals,m⟩
      | .reg r => return ⟨tail,dictionaryRead d r::c.vals,m⟩
      | .pow2 a =>
          if ready then
            match c.vals with
            | [] => .error ⟨.valueStackUnderflow,m.steps⟩
            | av::vs =>
                let v ← power m av
                return ⟨tail,v::vs,m⟩
          else return ⟨(a,false)::(e,true)::tail,c.vals,m⟩
      | .binary op a b =>
          if ready then
            match c.vals with
            | bv::av::vs =>
                let v ← check m (binaryValue op av bv)
                return ⟨tail,v::vs,m⟩
            | _ => .error ⟨.valueStackUnderflow,m.steps⟩
          else return ⟨(a,false)::(b,false)::(e,true)::tail,c.vals,m⟩

def runSteps (d : Dictionary) : ℕ → Config → Result Config
  | 0, c => .ok c
  | n+1, c => do
      let c ← step d c
      runSteps d n c

@[simp] theorem runSteps_zero (d : Dictionary) (c : Config) : runSteps d 0 c = .ok c := rfl

@[simp] theorem runSteps_one (d : Dictionary) (c : Config) : runSteps d 1 c = step d c := by
  simp only [runSteps]
  cases step d c <;> rfl

/-- Sequential fuel concatenation, including immediate propagation of faults. -/
theorem runSteps_add (d : Dictionary) (n k : ℕ) (c : Config) :
    runSteps d (n+k) c = (do
      let middle ← runSteps d n c
      runSteps d k middle) := by
  induction n generalizing c with
  | zero => simp
  | succ n ih =>
      rw [Nat.succ_add]
      simp only [runSteps, ih]
      cases step d c <;> rfl

/-- Universal local refinement, valid under arbitrary pending work and preexisting
values. Success adds exactly one value; faults retain the same kind and tick.
This is an algorithm-model theorem, not a verified CPython execution theorem. -/
theorem expression_stack_exact (d : Dictionary) (e : PyExpr) (m : Meter)
    (tail : List (PyExpr × Bool)) (vs : List ℕ) :
    runSteps d (cost e) ⟨(e,false)::tail,vs,m⟩ = (do
      let (v,out) ← reference d e m
      return ⟨tail,v::vs,out⟩) := by
  induction e generalizing m tail vs with
  | constant n =>
      simp only [cost, runSteps_one, step, reference]
      cases tick m <;> simp
  | reg r =>
      simp only [cost, runSteps_one, step, reference]
      cases tick m <;> rfl
  | pow2 a ih =>
      have hc : cost (.pow2 a) = 1 + (cost a + 1) := by simp [cost, Nat.add_assoc]
      rw [hc, runSteps_add]
      simp only [runSteps_one, step, Bool.false_eq_true, ↓reduceIte, reference]
      cases ht : tick m with
      | error err => rfl
      | ok out =>
          simp only [result_bind_ok, result_pure]
          rw [runSteps_add, ih]
          cases ha : reference d a out with
          | error err => rfl
          | ok z =>
              rcases z with ⟨av,am⟩
              simp only [result_bind_ok, result_pure, runSteps_one, step, ↓reduceIte]
              cases tick am with
              | error err => rfl
              | ok bm =>
                  simp only [result_bind_ok, result_pure]
                  cases power bm av <;> rfl
  | binary op a b iha ihb =>
      have hc : cost (.binary op a b) = 1 + (cost a + (cost b + 1)) := by
        simp [cost, Nat.add_assoc]
      rw [hc, runSteps_add]
      simp only [runSteps_one, step, Bool.false_eq_true, ↓reduceIte, reference]
      cases ht : tick m with
      | error err => rfl
      | ok out =>
          simp only [result_bind_ok, result_pure]
          rw [runSteps_add, iha]
          cases ha : reference d a out with
          | error err => rfl
          | ok z =>
              rcases z with ⟨av,am⟩
              simp only [result_bind_ok, result_pure]
              rw [runSteps_add, ihb]
              cases hb : reference d b am with
              | error err => rfl
              | ok z =>
                  rcases z with ⟨bv,bm⟩
                  simp only [result_bind_ok, result_pure, runSteps_one, step, ↓reduceIte]
                  cases tick bm with
                  | error err => rfl
                  | ok cm =>
                      simp only [result_bind_ok, result_pure]
                      cases check cm (binaryValue op av bv) <;> rfl

/-- The wrapper mirrors the final Python value-stack invariant check. Fuel is
chosen from syntax and covers every work pop exactly once before stuttering. -/
def expression (d : Dictionary) (e : PyExpr) (m : Meter) : Result (ℕ × Meter) := do
  let c ← runSteps d (cost e) ⟨[(e,false)],[],m⟩
  match c.work, c.vals with
  | [], [v] => .ok (v,c.meter)
  | _, _ => .error ⟨.stackInvariant,c.meter.steps⟩

theorem expression_eq_reference (d : Dictionary) (e : PyExpr) (m : Meter) :
    expression d e m = reference d e m := by
  unfold expression
  rw [expression_stack_exact]
  cases reference d e m with
  | error err => rfl
  | ok z => rcases z with ⟨v,out⟩; rfl

theorem expression_success_sound (d : Dictionary) (e : PyExpr) (m out : Meter) (v : ℕ)
    (h : expression d e m = .ok (v,out)) :
    v = P02A2.ObserverCore.evalExpr (lower e) (dictionaryRead d) := by
  rw [expression_eq_reference] at h
  exact (reference_spec d e m out v h).1.trans (value_correct e _)

theorem expression_success_ticks (d : Dictionary) (e : PyExpr) (m out : Meter) (v : ℕ)
    (h : expression d e m = .ok (v,out)) : out.steps = m.steps + cost e := by
  rw [expression_eq_reference] at h
  exact congrArg Meter.steps (reference_spec d e m out v h).2

theorem expression_complete_unbounded (d : Dictionary) (e : PyExpr) (steps : ℕ) :
    expression d e ⟨none,none,steps⟩ =
      .ok (P02A2.ObserverCore.evalExpr (lower e) (dictionaryRead d),
        ⟨none,none,steps+cost e⟩) := by
  rw [expression_eq_reference, reference_unbounded, value_correct]

end P02.PythonExpr
