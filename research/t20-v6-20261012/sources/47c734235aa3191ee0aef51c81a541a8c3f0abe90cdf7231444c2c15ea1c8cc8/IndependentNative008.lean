import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case160_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "bottom")]), (WireValue.natural 0)]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case160_fresh
theorem case161_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "all")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case161_fresh
theorem case162_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "all"), WireValue.null]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case162_fresh
theorem case163_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "universe")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case163_fresh
theorem case164_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case164_fresh
theorem case165_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.natural 0))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case165_fresh
theorem case166_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.object []))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case166_fresh
theorem case167_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array []))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case167_fresh
theorem case168_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "k")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case168_fresh
theorem case169_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])])]))]) = some ((Term.app Term.i Term.i), (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case169_fresh
theorem case170_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "k")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case170_fresh
theorem case171_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])]))]) = some (Term.i, (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case171_fresh
theorem case172_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "unknown")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case172_fresh
theorem case173_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "i"), (WireValue.natural 0)])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case173_fresh
theorem case174_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.text "i")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case174_fresh
theorem case175_fresh : nativeCheck 0 WireValue.null = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case175_fresh
theorem case176_fresh : nativeCheck 0 (WireValue.boolean true) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case176_fresh
theorem case177_fresh : nativeCheck 0 (WireValue.natural 0) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case177_fresh
theorem case178_fresh : nativeCheck 0 (WireValue.array []) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case178_fresh
theorem case179_fresh : nativeCheck 0 (WireValue.array [(WireValue.text "i")]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case179_fresh
