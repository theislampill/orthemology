import PythonRunnerSemantics

namespace P02.PythonRunner
open P02.PythonExpr

structure Config where
  work : List Task
  store : Dictionary
  meter : Meter
  events : List (ℕ × ℕ)

/-- Precisely one source outer-task pop. Embedded expression work is the
accepted P1 stack algorithm, sharing the same meter. -/
def step (trace : Bool) (c : Config) : Result Config :=
  match c.work with
  | [] => .ok c
  | task::tail => do
      let m ← tick c.meter
      match task with
      | .repeat r count k body =>
          if k < count then
            return ⟨.stmt body :: .repeat r count (k+1) body :: tail,
              dictionaryWrite c.store r k,m,c.events⟩
          else return ⟨tail,c.store,m,c.events⟩
      | .stmt s =>
          match s with
          | .set r e =>
              let (v,m) ← expression c.store e m
              return ⟨tail,dictionaryWrite c.store r v,m,
                c.events ++ (if trace then [(r,v)] else [])⟩
          | .seq ss => return ⟨schedule ss tail,c.store,m,c.events⟩
          | .loop r e body =>
              let (count,m) ← expression c.store e m
              return ⟨.repeat r count 0 body :: tail,c.store,m,c.events⟩
          | .branch e s t =>
              let (v,m) ← expression c.store e m
              return ⟨.stmt (if v = 0 then t else s) :: tail,c.store,m,c.events⟩

def runSteps (trace : Bool) : ℕ → Config → Result Config
  | 0, c => .ok c
  | n+1, c => do
      let next ← step trace c
      runSteps trace n next

/-- `ok none` is pending mathematical task fuel, never a semantic zero or source
resource exception. Source resource failures retain their P1 fault category. -/
def runFuel (trace : Bool) (fuel : ℕ) (c : Config) : Result (Option Config) := do
  let out ← runSteps trace fuel c
  match out.work with
  | [] => .ok (some out)
  | _ => .ok none

def remaining (trace : Bool) (c : Config) : Summary := tasksSummary trace c.work c.store

def StepAccounting (trace : Bool) (c out : Config) : Prop :=
  (remaining trace c).store = (remaining trace out).store ∧
  c.events ++ (remaining trace c).events = out.events ++ (remaining trace out).events ∧
  c.meter.steps + (remaining trace c).ticks = out.meter.steps + (remaining trace out).ticks ∧
  (remaining trace out).pops + 1 = (remaining trace c).pops ∧
  (remaining trace out).bits ≤ (remaining trace c).bits ∧
  out.meter.limit = c.meter.limit ∧ out.meter.maxBits = c.meter.maxBits

def prependEvents (events : List (ℕ × ℕ)) (s : Summary) : Summary :=
  {s with events := events ++ s.events}

theorem account_of_local (trace : Bool) (c out : Config) (ticks bits : ℕ)
    (events : List (ℕ × ℕ))
    (hs : remaining trace c = prependEvents events (charge ticks bits (remaining trace out)))
    (hm : out.meter = {c.meter with steps := c.meter.steps+ticks})
    (he : out.events = c.events++events) : StepAccounting trace c out := by
  unfold StepAccounting
  rw [hs, hm, he]
  simp [prependEvents, charge, List.append_assoc, Nat.add_assoc]

theorem expression_state (d : Dictionary) (e : PyExpr) (m out : Meter) (v : ℕ)
    (h : expression d e m = .ok (v,out)) :
    v = value e (dictionaryRead d) ∧ out = {m with steps := m.steps+cost e} := by
  apply reference_spec d e m out v
  rw [← expression_eq_reference]
  exact h

/-- Successful source task steps preserve final semantic/store/trace observations,
account for exact meter work and remove exactly one outer task-pop obligation. -/
theorem step_accounting (trace : Bool) (c out : Config) (hne : c.work ≠ [])
    (h : step trace c = .ok out) : StepAccounting trace c out := by
  rcases c with ⟨work,d,m,events⟩
  cases work with
  | nil => exact (hne rfl).elim
  | cons task tail =>
      cases ht : tick m with
      | error err => simp [step, ht] at h
      | ok m' =>
          obtain ⟨rfl,_⟩ := (tick_ok_iff m m').mp ht
          cases task with
          | stmt s =>
              cases s with
              | set r e =>
                  cases he : expression d e {m with steps := m.steps+1} with
                  | error err => simp [step, ht, he] at h
                  | ok z =>
                      rcases z with ⟨v,em⟩
                      obtain ⟨rfl,rfl⟩ := expression_state _ _ _ _ _ he
                      simp [step, ht, he] at h
                      cases h
                      apply account_of_local trace _ _ (1+cost e) (neededBits d e)
                        (if trace then [(r,value e (dictionaryRead d))] else [])
                      · simp [remaining, tasksSummary, taskSummary, commandSummary, follow,
                          prependEvents, charge, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]
                      · simp [Nat.add_assoc]
                      · rfl
              | seq ss =>
                  simp [step, ht] at h
                  cases h
                  apply account_of_local trace _ _ 1 0 []
                  · simp [remaining, tasksSummary, taskSummary, commandSummary,
                      follow_charge, scheduled_summary, prependEvents]
                  · rfl
                  · simp
              | loop r e body =>
                  cases he : expression d e {m with steps := m.steps+1} with
                  | error err => simp [step, ht, he] at h
                  | ok z =>
                      rcases z with ⟨v,em⟩
                      obtain ⟨rfl,rfl⟩ := expression_state _ _ _ _ _ he
                      simp [step, ht, he] at h
                      cases h
                      apply account_of_local trace _ _ (1+cost e) (neededBits d e) []
                      · simp [remaining, tasksSummary, taskSummary, commandSummary,
                          follow_charge, prependEvents]
                      · simp [Nat.add_assoc]
                      · simp
              | branch e s t =>
                  cases he : expression d e {m with steps := m.steps+1} with
                  | error err => simp [step, ht, he] at h
                  | ok z =>
                      rcases z with ⟨v,em⟩
                      obtain ⟨rfl,rfl⟩ := expression_state _ _ _ _ _ he
                      simp [step, ht, he] at h
                      cases h
                      apply account_of_local trace _ _ (1+cost e) (neededBits d e) []
                      · by_cases hz : value e (dictionaryRead d) = 0 <;>
                          simp [remaining, tasksSummary, taskSummary, commandSummary,
                            hz, follow_charge, prependEvents]
                      · simp [Nat.add_assoc]
                      · simp
          | «repeat» r count k body =>
              by_cases hk : k < count
              · simp [step, ht, hk] at h
                cases h
                have hr : count-k = (count-(k+1))+1 := by omega
                apply account_of_local trace _ _ 1 0 []
                · simp [remaining, tasksSummary, taskSummary, hr, repeatSummary,
                    follow_charge, follow_assoc, prependEvents]
                · rfl
                · simp
              · simp [step, ht, hk] at h
                cases h
                have hr : count-k = 0 := by omega
                apply account_of_local trace _ _ 1 0 []
                · simp [remaining, tasksSummary, taskSummary, hr, repeatSummary,
                    follow, charge, prependEvents, Nat.add_comm]
                · rfl
                · simp

end P02.PythonRunner
