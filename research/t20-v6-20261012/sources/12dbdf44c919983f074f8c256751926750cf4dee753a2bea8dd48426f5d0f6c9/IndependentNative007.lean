import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case140_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case140_fresh
theorem case141_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])])), ("trace", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case141_fresh
theorem case142_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])])), ("trusted", (WireValue.boolean true))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case142_fresh
theorem case143_fresh : nativeCheck 0 (WireValue.object [("rule", WireValue.null), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case143_fresh
theorem case144_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.boolean true)), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case144_fresh
theorem case145_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.natural 0)), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case145_fresh
theorem case146_fresh : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "bogus")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case146_fresh
theorem case147_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case147_fresh
theorem case148_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.boolean false))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case148_fresh
theorem case149_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.negative 0))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case149_fresh
theorem case150_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.natural 0))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case150_fresh
theorem case151_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.text "bottom"))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case151_fresh
theorem case152_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array []))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case152_fresh
theorem case153_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "bottom"), (WireValue.natural 0)]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case153_fresh
theorem case154_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case154_fresh
theorem case155_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.negative 0)]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case155_fresh
theorem case156_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.boolean true)]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case156_fresh
theorem case157_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0), (WireValue.natural 0)]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case157_fresh
theorem case158_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 115792089237316195423570985008687907853269984665640564039457584007913129639936)]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case158_fresh
theorem case159_fresh : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "bottom")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit, List.map, List.foldl, List.all]
  decide
#print axioms case159_fresh
