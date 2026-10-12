import GrammarImage
open ExactSyntaxValidity Encodable SourceFamilyComputability CodedScope OrthemologyV2 P01D P01AC
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000
example : valid 0 (encode Term.i) = true := by
  simp only [valid]
  rw [evaluate]
  norm_num [shape, termShape, children, termChildren]
example : valid 0 0 = false := by
  simp only [valid]
  rw [evaluate]
  norm_num [shape, termShape, children, termChildren, tag, first, rest, nullary, leaf, node]
example : valid 2 (unary 1 (leaf 0)) = false := by
  simp only [valid]
  rw [evaluate]
  norm_num [shape, polyShape, children, polyChildren, unary_external_lt]
  rw [evaluate]
  norm_num [shape, termShape, children, termChildren, tag, first, rest, nullary, leaf, node]
#eval valid 3 (encode (Ty.identity .raw (.var 0) (.atom .one)))
