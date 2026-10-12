import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case140_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case141_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])])), ("trace", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case142_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "reduce")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])])), ("trusted", WireValue.boolean true)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case143_matches : nativeCheck 0 (WireValue.object [("rule", WireValue.null), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case144_matches : nativeCheck 0 (WireValue.object [("rule", WireValue.boolean true), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case145_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.natural 0)), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case146_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "bogus")), ("proof", (WireValue.object [("rule", (WireValue.text "app")), ("function", (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "all"), (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]), (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)])])]))])), ("argument", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))])), ("trace", (WireValue.array [(WireValue.array [(WireValue.text "app"), (WireValue.array [(WireValue.text "i")]), (WireValue.array [(WireValue.text "i")])]), (WireValue.array [(WireValue.text "i")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case147_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case148_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", WireValue.boolean false)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case149_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.negative 0))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case150_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.natural 0))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case151_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.text "bottom"))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case152_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array []))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case153_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "bottom"), (WireValue.natural 0)]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case154_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case155_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.negative 0)]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case156_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), WireValue.boolean true]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case157_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0), (WireValue.natural 0)]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case158_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 115792089237316195423570985008687907853269984665640564039457584007913129639936)]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case159_matches : nativeCheck 1 (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "arr"), (WireValue.array [(WireValue.text "bottom")])]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
