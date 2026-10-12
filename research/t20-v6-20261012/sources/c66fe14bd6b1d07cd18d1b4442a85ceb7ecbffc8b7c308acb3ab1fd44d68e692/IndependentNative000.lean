import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case0_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.i, (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case0_fresh
theorem case1_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "i"))]) = some (Term.i, (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case1_fresh
theorem case2_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case2_fresh
theorem case3_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "i"))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case3_fresh
theorem case4_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case4_fresh
theorem case5_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "i"))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case5_fresh
theorem case6_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case6_fresh
theorem case7_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("A", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case7_fresh
theorem case8_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("trusted", (WireValue.boolean true))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case8_fresh
theorem case9_fresh : nativeCheck 0 (WireValue.object [("rule", WireValue.null), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case9_fresh
theorem case10_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.boolean true)), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case10_fresh
theorem case11_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.natural 0)), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case11_fresh
theorem case12_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "bogus")), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case12_fresh
theorem case13_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.k, (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case13_fresh
theorem case14_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "k")), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.k, (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case14_fresh
theorem case15_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "k")), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.k, (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case15_fresh
theorem case16_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "k"))]) = some (Term.k, (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case16_fresh
theorem case17_fresh : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "k")), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.k, (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case17_fresh
theorem case18_fresh : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "k"))]) = some (Term.k, (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case18_fresh
theorem case19_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case19_fresh
