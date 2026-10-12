import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case60_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case60_fresh
theorem case61_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("A", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case61_fresh
theorem case62_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("A", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case62_fresh
theorem case63_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case63_fresh
theorem case64_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case64_fresh
theorem case65_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("B", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case65_fresh
theorem case66_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case66_fresh
theorem case67_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case67_fresh
theorem case68_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("C", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case68_fresh
theorem case69_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "s")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")])), ("trusted", (WireValue.boolean true))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case69_fresh
theorem case70_fresh : nativeCheck 0 (WireValue.object [("rule", WireValue.null), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case70_fresh
theorem case71_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.boolean true)), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case71_fresh
theorem case72_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.natural 0)), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case72_fresh
theorem case73_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "bogus")), ("A", (WireValue.array [(WireValue.text "bottom")])), ("B", (WireValue.array [(WireValue.text "bottom")])), ("C", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case73_fresh
theorem case74_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))]) = some ((Term.app Term.i Term.i), (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case74_fresh
theorem case75_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "app")), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))]))]) = some ((Term.app Term.i Term.i), (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case75_fresh
theorem case76_fresh : nativeCheck 0 (WireValue.object [("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("rule", (WireValue.text "app")), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))]) = some ((Term.app Term.i Term.i), (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case76_fresh
theorem case77_fresh : nativeCheck 0 (WireValue.object [("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("rule", (WireValue.text "app"))]) = some ((Term.app Term.i Term.i), (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case77_fresh
theorem case78_fresh : nativeCheck 0 (WireValue.object [("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))]))]) = some ((Term.app Term.i Term.i), (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case78_fresh
theorem case79_fresh : nativeCheck 0 (WireValue.object [("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("rule", (WireValue.text "app"))]) = some ((Term.app Term.i Term.i), (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case79_fresh
