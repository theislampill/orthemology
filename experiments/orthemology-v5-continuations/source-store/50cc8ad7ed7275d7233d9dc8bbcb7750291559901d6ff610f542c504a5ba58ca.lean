import NaturalStateCompiler

namespace Orthemology.RuntimeBridge.Natural.Fixture
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.PRProgram P02A2.ObserverCore
open Orthemology.CertifiedObserver

def counter : Mealy ℕ where
  next s b := s + bitNat b
  out s _ := decide (s % 2 = 1)

def nextProgram : Program 2 := ⟨.set 2 (.add (.reg 0) (.reg 1)),2⟩
def outProgram : Program 2 := ⟨.set 2 (.mod (.reg 0) (.constant 2)),2⟩

theorem counter_implemented : Implements nextProgram outProgram counter := by
  constructor
  · intro s b
    simp [nextProgram, denote, exec, evalExpr, P02A2.LoopPrimrec.extend, counter]
  · intro s b
    have hs : s % 2 = 0 ∨ s % 2 = 1 := by omega
    rcases hs with hs | hs <;>
      simp [outProgram, denote, exec, evalExpr, P02A2.LoopPrimrec.extend, counter, bitNat, hs]

theorem literal_unbounded_state (n : ℕ) : state counter 0 (fun _ => true) n = n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [state, ih]
      simp [counter, bitNat]

theorem counter_runtime_exact :
    Indexed.runtimeOutput (index nextProgram outProgram 0) = MealyMeasure.output counter 0 :=
  compiled_runtime_output _ _ counter counter_implemented 0

end Orthemology.RuntimeBridge.Natural.Fixture
