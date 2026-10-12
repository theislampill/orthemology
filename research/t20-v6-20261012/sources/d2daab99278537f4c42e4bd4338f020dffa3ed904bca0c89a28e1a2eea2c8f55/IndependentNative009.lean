import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case180_fresh : nativeCheck 0 (WireValue.text "proof") = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case180_fresh
theorem case181_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case181_fresh
theorem case182_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.boolean true))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case182_fresh
theorem case183_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.natural 0))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case183_fresh
theorem case184_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object []))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case184_fresh
theorem case185_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.array []))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case185_fresh
theorem case186_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("extra", (WireValue.natural 0))]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case186_fresh
theorem case187_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case187_fresh
