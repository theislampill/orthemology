import CodecIndexPrimrec
import Pi3IndexReduction
open P02.Codec P02A2.ObserverCore P02A2.PRProgram

namespace IndependentBoundaryControls

def firstParameter : Program 3 := ⟨.set 3 (.reg 0),3⟩
def difference : Program 2 := ⟨.set 2 (.sub (.reg 0) (.reg 1)),2⟩

theorem literal_parameter_is_first (a n word : ℕ) :
    evaluateIndex (parameterIndex firstParameter a) n word = a % 2 := by
  rw [parameterIndex_correct]
  simp [firstParameter, denote, exec, evalExpr, P02A2.LoopPrimrec.extend]

theorem binary_input_order (n word : ℕ) :
    evaluateIndex (programIndex (pack difference)) n word = (n-word)%2 := by
  rw [evaluateIndex_programIndex]
  simp [difference, denote, exec, evalExpr, P02A2.LoopPrimrec.extend]

example : evaluateIndex (parameterIndex firstParameter 3) 0 0 = 1 := by
  rw [literal_parameter_is_first]
example : evaluateIndex (programIndex (pack difference)) 1 2 = 0 := by
  rw [binary_input_order]

-- Primitive recursiveness is a numeric function theorem for every fixed p.
example (p : Program 3) : Primrec (parameterIndex p) := parameterIndex_primrec p

-- The byte-domain premise is genuinely necessary for envelope injectivity.
example : encodeNumeric [0,256] = encodeNumeric [1,0] := by decide
example : decodeNumeric (encodeNumeric [256]) ≠ some [256] := by
  intro h
  have hb := (decodeNumeric_sound h).1 256 (by simp)
  omega

-- Correct magic alone does not make a program; malformed codes denote zero.
example : evaluateIndex 0 100 200 = 0 := by decide +kernel
-- The 758 differential checks separately include empty, unary, and n-ary Seq.
example (p : PackedProgram) : decodeBytes (encodeBytes p) = some p :=
  decodeBytes_encodeBytes p

-- Finite parser fuel is structural, independent of execution LOOP iterations.
example : readExpr 0 (exprBytes (.constant 1)) = none := rfl
example : readExpr 1 (exprBytes (.constant 1)) = some (.constant 1,[]) := by
  simpa using readExpr_append (.constant 1) [] 1 (by decide)

#print axioms literal_parameter_is_first
#print axioms binary_input_order
end IndependentBoundaryControls
