import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case40_matches : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case41_matches : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case42_matches : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case43_matches : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case44_matches : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case45_matches : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case46_matches : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case47_matches : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case48_matches : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case49_matches : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case50_matches : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case51_matches : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case52_matches : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case53_matches : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case54_matches : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case55_matches : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case56_matches : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case57_matches : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case58_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case59_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
