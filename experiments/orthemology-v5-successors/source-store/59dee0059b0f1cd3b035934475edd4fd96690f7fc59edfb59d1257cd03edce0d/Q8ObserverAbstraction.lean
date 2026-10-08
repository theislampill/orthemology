import ObserverAbstraction
import Q8Compiler
import MealyMeasureFixtures

/-! Source-owned operational bridge. The observer is generated from the
recovered Q8 machine step and its recovered LOOP compiler. A source step is
inspected before emitting the current input bit, exactly as boundedFlag does. -/
namespace Orthemology.CertifiedObserver.Q8
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.Q8Machine
open Set MeasureTheory

/-- The actual unbounded two-counter configuration is the concrete state. -/
def observer {n : ℕ} (M : Machine n) : Mealy (Config n) where
  next cfg _ := step M cfg
  out cfg b := if (step M cfg).halted then b else false

theorem state_eq_run {n : ℕ} (M : Machine n) (hn : 0 < n) (x : Cantor) (k : ℕ) :
    state (observer M) (initial n hn) x k = run M hn k := by
  induction k with
  | zero => rfl
  | succ k ih =>
      change step M (state (observer M) (initial n hn) x k) = _
      rw [ih]
      rfl

theorem output_eq_switched {n : ℕ} (M : Machine n) (hn : 0 < n) :
    output (observer M) (initial n hn) = P02A2.Q8Measure.switched (boundedFlag M hn) := by
  funext x k
  change (if (step M (state (observer M) (initial n hn) x k)).halted then x k else false) = _
  rw [state_eq_run]
  rfl

/-- This binds the new Mealy abstraction to the literal recovered compiler's
complete output function, including every synchronous stage. -/
theorem compiled_output {n : ℕ} (M : Machine n) (hn : 0 < n) :
    P02A2.Q8Compiler.compiledObserver M = output (observer M) (initial n hn) := by
  rw [P02A2.Q8Compiler.compiledObserver_eq M hn, output_eq_switched]

theorem compiled_law {n : ℕ} (M : Machine n) (hn : 0 < n) :
    P02A2.Q8Compiler.compiledLaw M = law (observer M) (initial n hn) := by
  unfold P02A2.Q8Compiler.compiledLaw law
  rw [compiled_output M hn]

theorem compiled_finite_solver {n : ℕ} (M : Machine n) (hn : 0 < n)
    {T : Type*} [Fintype T] [DecidableEq T] [Nonempty T] (A : Mealy T)
    (R : Simulation (observer M) A) (t : T)
    (initial_rel : R.relates (initial n hn) t) :
    (solveDefect A t : ℝ) = P02A2.defect (P02A2.Q8Compiler.compiledLaw M) := by
  rw [compiled_law M hn]
  exact certified_defect_exact R initial_rel

namespace Fixtures
open Orthemology.Frontier.MealyMeasure.Fixtures

/-- The finite source program increments counter 0 forever. Its actual
configuration trajectory is infinite, rather than merely typed as infinite. -/
def grow : Machine 1 := fun _ => .inc 0 0

def growSimulation : Simulation (observer grow) zeroMachine where
  relates cfg _ := cfg.halted = false
  out_eq := by intro cfg t h b; simp [observer, step, grow, execute, zeroMachine, h]
  next_rel := by intro cfg t h b; simp [observer, step, grow, execute, h]

theorem grow_run_unbounded (k : ℕ) :
    (run grow (by decide) k).halted = false ∧
      (run grow (by decide) k).counter 0 = k := by
  induction k with
  | zero => exact ⟨rfl,rfl⟩
  | succ k ih =>
      simp only [run, step, ih.1, Bool.false_eq_true, ↓reduceIte, grow, execute]
      exact ⟨True.intro, by simp [ih.2]⟩

theorem grow_compiled_zero :
    P02A2.Q8Compiler.compiledLaw grow = law zeroMachine () := by
  rw [compiled_law grow (by decide)]
  exact simulation_law growSimulation rfl

theorem grow_solver :
    (solveDefect zeroMachine () : ℝ) = P02A2.defect (P02A2.Q8Compiler.compiledLaw grow) :=
  compiled_finite_solver grow (by decide) zeroMachine growSimulation () rfl

def haltNow : Machine 1 := fun _ => .halt

def haltSimulation : Simulation (observer haltNow) copyMachine where
  relates _ _ := True
  out_eq := by
    intro cfg t h b
    cases hh : cfg.halted <;> simp [observer, step, haltNow, execute, copyMachine, hh]
  next_rel := fun _ _ => True.intro

theorem halt_compiled_copy :
    P02A2.Q8Compiler.compiledLaw haltNow = law copyMachine () := by
  rw [compiled_law haltNow (by decide)]
  exact simulation_law haltSimulation True.intro

/-- Reading the old halted flag introduces a real one-tick mismatch. The
scalar defect alone would not expose this implementation error. -/
def wrongClock {n : ℕ} (M : Machine n) : Mealy (Config n) where
  next cfg _ := step M cfg
  out cfg b := if cfg.halted then b else false

theorem wrong_clock_rejected :
    output (wrongClock haltNow) (initial 1 (by decide)) ≠
      P02A2.Q8Compiler.compiledObserver haltNow := by
  intro h
  rw [compiled_output haltNow (by decide)] at h
  have he := congrFun (congrFun h (fun _ => true)) 0
  cases he

#eval solveDefect zeroMachine ()
#eval solveDefect copyMachine ()
#eval P02A2.Q8Compiler.programValue grow 10 255
#eval P02A2.Q8Compiler.programValue haltNow 0 3

end Fixtures
end Orthemology.CertifiedObserver.Q8
