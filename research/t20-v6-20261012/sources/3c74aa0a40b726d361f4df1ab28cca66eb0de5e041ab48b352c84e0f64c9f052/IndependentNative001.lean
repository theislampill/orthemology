import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case20_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "k"))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case20_fresh
theorem case21_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case21_fresh
theorem case22_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case22_fresh
theorem case23_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case23_fresh
theorem case24_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case24_fresh
theorem case25_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case25_fresh
theorem case26_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case26_fresh
theorem case27_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("B", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case27_fresh
theorem case28_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("trusted", (WireValue.boolean true))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case28_fresh
theorem case29_fresh : nativeCheck 0 (WireValue.object [("rule", WireValue.null), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case29_fresh
theorem case30_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.boolean true)), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case30_fresh
theorem case31_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.natural 0)), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case31_fresh
theorem case32_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "bogus")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case32_fresh
theorem case33_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case33_fresh
theorem case34_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case34_fresh
theorem case35_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case35_fresh
theorem case36_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case36_fresh
theorem case37_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case37_fresh
theorem case38_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case38_fresh
theorem case39_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case39_fresh
