import NativeProofSoundness
import SourceExportBoundary
namespace P03NativeControls
open P03Source OrthemologyV2 OrthemologyV3

def bottomTree : WireValue := .array [.text "bottom"]
def validI : WireValue := .object [("rule",.text "i"),("A",bottomTree)]

theorem valid_native_i : nativeCheck 0 validI = some (.i,.arrow .bottom .bottom) := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem reordered_native_i :
    nativeCheck 0 (.object [("A",bottomTree),("rule",.text "i")]) =
      some (.i,.arrow .bottom .bottom) := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem missing_field_refused : nativeCheck 0 (.object [("rule",.text "i")]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem extra_field_refused :
    nativeCheck 0 (.object [("rule",.text "i"),("A",bottomTree),("trusted",.boolean true)]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem duplicate_rule_refused :
    nativeCheck 0 (.object [("rule",.text "i"),("rule",.text "i"),("A",bottomTree)]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem duplicate_type_refused :
    nativeCheck 0 (.object [("rule",.text "i"),("A",bottomTree),("A",bottomTree)]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem boolean_index_refused :
    nativeCheck 1 (.object [("rule",.text "i"),("A",.array [.text "v",.boolean false])]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem negative_index_refused :
    nativeCheck 1 (.object [("rule",.text "i"),("A",.array [.text "v",.negative 0])]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem integer_rule_refused : nativeCheck 0 (.object [("rule",.natural 0),("A",bottomTree)]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem malformed_type_arity_refused :
    nativeCheck 0 (.object [("rule",.text "i"),("A",.array [.text "bottom",.null])]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem malformed_trace_shape_refused :
    nativeCheck 0 (.object [("rule",.text "reduce"),("proof",validI),("trace",.null)]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem malformed_trace_term_refused :
    nativeCheck 0 (.object [("rule",.text "reduce"),("proof",validI),
      ("trace",.array [.array [.text "unknown"]])]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem empty_trace_semantically_refused :
    nativeCheck 0 (.object [("rule",.text "reduce"),("proof",validI),("trace",.array [])]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem wrong_start_trace_semantically_refused :
    nativeCheck 0 (.object [("rule",.text "reduce"),("proof",validI),
      ("trace",.array [.array [.text "k"]])]) = none := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

theorem syntax_success_does_not_prove_trace_correctness :
    decodeNativeProof (.object [("rule",.text "reduce"),("proof",validI),("trace",.array [])]) =
      some (.reduce (.i .bottom) []) := by
  simp [nativeCheck, decodeNativeProof, validI, bottomTree, wireShape,
    wireNodes, wireHeight, wireIntegersFit, shapeFits, decodeProof,
    lookupField, exactFields, noDuplicateFields, List.isPerm,
    decodeType, decodeTrace, decodeTerms, decodeTerm,
    sourceCheck, sourceRun, sourceTrace, sourceTraceTail,
    proofShape, typeShape, termShape, traceShape, finish, outputCost,
    sourceScoped, sourceHeadStep]

#print axioms duplicate_rule_refused
#print axioms syntax_success_does_not_prove_trace_correctness
end P03NativeControls
