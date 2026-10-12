import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case40_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case40_fresh
theorem case41_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case41_fresh
theorem case42_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case42_fresh
theorem case43_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case43_fresh
theorem case44_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case44_fresh
theorem case45_fresh : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case45_fresh
theorem case46_fresh : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case46_fresh
theorem case47_fresh : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case47_fresh
theorem case48_fresh : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case48_fresh
theorem case49_fresh : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case49_fresh
theorem case50_fresh : nativeCheck 0 (WireValue.object [("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case50_fresh
theorem case51_fresh : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case51_fresh
theorem case52_fresh : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case52_fresh
theorem case53_fresh : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case53_fresh
theorem case54_fresh : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case54_fresh
theorem case55_fresh : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case55_fresh
theorem case56_fresh : nativeCheck 0 (WireValue.object [("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = some (Term.s, (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case56_fresh
theorem case57_fresh : nativeCheck 0 (WireValue.object [("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case57_fresh
theorem case58_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "s"))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case58_fresh
theorem case59_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("rule", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case59_fresh
