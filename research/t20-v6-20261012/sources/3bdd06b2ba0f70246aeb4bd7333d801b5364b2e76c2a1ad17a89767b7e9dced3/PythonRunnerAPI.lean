import PythonRunnerSoundness

namespace P02.PythonRunner
open P02.PythonExpr

structure Program where
  arity : ℕ
  output : ℕ
  body : Command

def inputFrom : List ℕ → ℕ → Dictionary
  | [], _ => []
  | v::vs, start => (start,v) :: inputFrom vs (start+1)

def inputDictionary (args : List ℕ) : Dictionary := inputFrom args 0

def argumentStore : List ℕ → ℕ → ℕ
  | [], _ => 0
  | v::_, 0 => v
  | _::vs, r+1 => argumentStore vs r

theorem read_input_shift (args : List ℕ) (start r : ℕ) :
    dictionaryRead (inputFrom args (start+1)) (r+1) = dictionaryRead (inputFrom args start) r := by
  induction args generalizing start with
  | nil => rfl
  | cons v vs ih => simp [inputFrom, dictionaryRead, ih]

theorem read_inputs (args : List ℕ) : dictionaryRead (inputDictionary args) = argumentStore args := by
  funext r
  induction args generalizing r with
  | nil => rfl
  | cons v vs ih =>
      cases r with
      | zero => simp [inputDictionary, inputFrom, dictionaryRead, argumentStore]
      | succ r =>
          change dictionaryRead (inputFrom vs 1) (r+1) = argumentStore vs r
          rw [read_input_shift vs 0 r]
          exact ih r

inductive Observation where
  | value : ℕ → Observation
  | traced : ℕ → ℕ → List (ℕ × ℕ) → Observation
  deriving DecidableEq, Repr

def Observation.valueOf : Observation → ℕ
  | .value v | .traced v _ _ => v

def observe (trace : Bool) (output : ℕ) (c : Config) : Observation :=
  if trace then .traced (dictionaryRead c.store output) c.meter.steps c.events
  else .value (dictionaryRead c.store output)

@[simp] theorem observe_value (trace : Bool) (output : ℕ) (c : Config) :
    (observe trace output c).valueOf = dictionaryRead c.store output := by
  cases trace <;> rfl

inductive CallError where
  | arityMismatch
  | resource : Failure → CallError
  deriving DecidableEq, Repr

/-- Typed-input API correspondence. The source's strict natural validation is a
precondition on these List Nat inputs. Mathematical fuel pending is separate
from source exceptions and both trace=False/trace=True successful result shapes. -/
def callFuel (trace : Bool) (fuel : ℕ) (p : Program) (args : List ℕ)
    (stepLimit maxBits : Option ℕ) : Except CallError (Option Observation) :=
  if args.length = p.arity then
    match runFuel trace fuel (initial p.body (inputDictionary args) ⟨stepLimit,maxBits,0⟩) with
    | .error err => .error (.resource err)
    | .ok none => .ok none
    | .ok (some out) => .ok (some (observe trace p.output out))
  else .error .arityMismatch

theorem call_arity_mismatch (trace : Bool) (fuel : ℕ) (p : Program) (args : List ℕ)
    (stepLimit maxBits : Option ℕ) (h : args.length ≠ p.arity) :
    callFuel trace fuel p args stepLimit maxBits = .error .arityMismatch := by
  simp [callFuel, h]

theorem call_success_value (trace : Bool) (fuel : ℕ) (p : Program) (args : List ℕ)
    (stepLimit maxBits : Option ℕ) (obs : Observation)
    (h : callFuel trace fuel p args stepLimit maxBits = .ok (some obs)) :
    obs.valueOf = P02A2.ObserverCore.exec (lowerCommand p.body) (argumentStore args) p.output := by
  by_cases ha : args.length = p.arity
  · cases hr : runFuel trace fuel (initial p.body (inputDictionary args) ⟨stepLimit,maxBits,0⟩) with
    | error err => simp [callFuel, ha, hr] at h
    | ok result =>
        cases result with
        | none => simp [callFuel, ha, hr] at h
        | some out =>
            simp [callFuel, ha, hr] at h
            cases h
            rw [observe_value, runner_success_sound trace fuel p.body _ _ out hr, read_inputs]
  · simp [callFuel, ha] at h

theorem call_complete_finite (trace : Bool) (p : Program) (args : List ℕ)
    (ha : args.length = p.arity) :
    let summary := commandSummary trace p.body (inputDictionary args)
    ∃ obs, callFuel trace summary.pops p args (some summary.ticks) (some summary.bits) =
      .ok (some obs) := by
  obtain ⟨out,h⟩ := runner_complete_finite trace p.body (inputDictionary args)
  exact ⟨observe trace p.output out,by simp [callFuel, ha, h]⟩

theorem step_only_resource (trace : Bool) (c : Config) : OnlyResource (step trace c) := by
  rcases c with ⟨work,d,m,events⟩
  cases work with
  | nil => trivial
  | cons task tail =>
      apply onlyResource_bind _ _ (tick_only_resource m)
      intro m
      cases task with
      | «repeat» r count k body =>
          simp only
          split_ifs <;> trivial
      | stmt s =>
          cases s with
          | seq ss => trivial
          | set r e | loop r e body | branch e s t =>
              apply onlyResource_bind _ _
                (by rw [expression_eq_reference]; exact reference_only_resource d e m)
              rintro ⟨v,m⟩
              trivial

theorem runSteps_only_resource (trace : Bool) (fuel : ℕ) (c : Config) :
    OnlyResource (runSteps trace fuel c) := by
  induction fuel generalizing c with
  | zero => trivial
  | succ fuel ih =>
      exact onlyResource_bind _ _ (step_only_resource trace c) (fun next => ih next)

/-- Valid typed runner failures cannot be converted to a semantic result or a
syntax rejection: they are exactly among P1's three modeled resource categories. -/
theorem runFuel_error_is_resource (trace : Bool) (fuel : ℕ) (c : Config) (err : Failure)
    (h : runFuel trace fuel c = .error err) : ResourceFault err.fault := by
  have hh := runSteps_only_resource trace fuel c
  cases hr : runSteps trace fuel c with
  | error e =>
      simp [runFuel, hr] at h
      cases h
      simpa [hr, OnlyResource] using hh
  | ok out =>
      cases hw : out.work <;> simp [runFuel, hr, hw] at h

end P02.PythonRunner
