import LiteralShiftFirstBit
open P02.LiteralShift P02A2.Q8Measure
example : fairCantor.map (compiledOutput .skip 2 0 1) =
    fairCantor.map (P02A2.ObserverCore.output (programValue .skip 2)) := by
  have hn := literal_zero_law_ne_base 1
  simp only [hn]
  decide
