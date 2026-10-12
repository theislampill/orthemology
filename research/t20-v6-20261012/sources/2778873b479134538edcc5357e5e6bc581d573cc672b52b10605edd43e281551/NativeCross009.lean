import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case180_matches : nativeCheck 0 (WireValue.text "proof") = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case181_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case182_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.boolean true))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case183_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.natural 0))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case184_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object []))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case185_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.array []))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case186_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("extra", (WireValue.natural 0))]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case187_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
