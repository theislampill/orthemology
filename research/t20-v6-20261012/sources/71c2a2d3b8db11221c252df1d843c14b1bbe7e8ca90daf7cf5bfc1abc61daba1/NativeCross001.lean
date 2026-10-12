import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case20_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "k"))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case21_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case22_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case23_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case24_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case25_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case26_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case27_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("B", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case28_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("trusted", (WireValue.boolean true))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case29_matches : nativeCheck 0 (WireValue.object [("rule", WireValue.null), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case30_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.boolean true)), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case31_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.natural 0)), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case32_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "bogus")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case33_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case34_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case35_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case36_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case37_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case38_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case39_matches : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
