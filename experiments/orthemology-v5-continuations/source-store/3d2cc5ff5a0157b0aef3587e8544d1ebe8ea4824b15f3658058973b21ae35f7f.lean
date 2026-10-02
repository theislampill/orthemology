import FiniteSelectorSource
open Orthemology.RuntimeBridge.PhaseUpdate
#check FiniteSelectorSource.Data
#check FiniteSelectorSource.Certificate
#check FiniteSelectorSource.cycle_source_exact
#check FiniteSelectorSource.normalize_retained_source_exact
#check FiniteSelectorSource.active_pairs_source_exact
#check FiniteSelectorSource.action_cycle_source_exact

open P02A2.PRProgram P02.Codec
open FiniteSelectorSource

/-- Literal arithmetic tests only; this value is deliberately not asserted to
certify an arbitrary retained kernel, menu, priority, or classical choice. -/
def literalData : Data := ⟨44812,7*2^70,9*2^12⟩

example : denote (cycleProgram literalData) ![0,0,100001] = 0 := by decide
example : denote (cycleProgram literalData) ![0,1,100000] = 1 := by decide
example : denote (cycleProgram literalData) ![1,1,100001] = 0 := by decide
example : denote (cycleProgram literalData) ![2,0,100000] = 1 := by decide
example : denote (cycleProgram literalData) ![3,0,100000] = 0 := by decide
example : denote (cycleProgram literalData) ![3,1,100001] = 1 := by decide
example : denote (bindProgram literalData) ![3,1,0] = 7 := by decide
example : denote (bindProgram literalData) ![3,1,1] = 0 := by decide
example : denote (normalizeRetainedProgram literalData) ![100001,0,3,0,0] = 7 := by decide
example : denote (normalizeRetainedProgram literalData) ![100000,0,3,0,0] = 0 := by decide
example : denote (normalizeRetainedProgram literalData) ![100001,1,3,0,0] = 1 := by decide
example : denote (normalizeRetainedProgram literalData) ![100001,16,3,0,0] = 16 := by decide
example : denote (activePairsProgram literalData) ![0,3] = 9 := by decide
example : denote (activePairsProgram literalData) ![1,3] = 0 := by decide
example : denote (activePairsProgram literalData) ![16,3] = 15 := by decide
example : denote (actionCycleProgram literalData) ![9,0,1,100001] = 0 := by decide
example : denote (actionCycleProgram literalData) ![9,1,0,100000] = 1 := by decide

#print axioms cycle_mod_two
#print axioms cycle_source_exact
#print axioms normalize_retained_source_exact
#print axioms active_pairs_source_exact
#print axioms action_cycle_source_exact

#eval IO.println ("CYCLE_BYTES=" ++ reprStr (encodeBytes (pack (cycleProgram literalData))))
#eval IO.println ("NORMALIZE_BYTES=" ++ reprStr (encodeBytes (pack (normalizeRetainedProgram literalData))))
#eval IO.println ("ACTION_BYTES=" ++ reprStr (encodeBytes (pack (actionCycleProgram literalData))))
#eval IO.println ("BIND_BYTES=" ++ reprStr (encodeBytes (pack (bindProgram literalData))))
#eval IO.println ("ACTIVE_BYTES=" ++ reprStr (encodeBytes (pack (activePairsProgram literalData))))
