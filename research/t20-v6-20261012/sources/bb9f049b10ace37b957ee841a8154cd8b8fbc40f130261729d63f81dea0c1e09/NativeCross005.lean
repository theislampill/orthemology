import NativeCheckerBridge
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
theorem case100_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))])), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case101_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))])), ("body", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case102_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))])), ("trusted", (WireValue.boolean true))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case103_matches : nativeCheck 0 (WireValue.object [("rule", WireValue.null), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case104_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.boolean true)), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case105_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.natural 0)), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case106_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "bogus")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case107_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.i, (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case108_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_e")), ("type", (WireValue.array [(WireValue.text "bottom")])), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))]) = some (Term.i, (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case109_matches : nativeCheck 0 (WireValue.object [("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("rule", (WireValue.text "all_e")), ("type", (WireValue.array [(WireValue.text "bottom")]))]) = some (Term.i, (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case110_matches : nativeCheck 0 (WireValue.object [("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "all_e"))]) = some (Term.i, (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case111_matches : nativeCheck 0 (WireValue.object [("type", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))]) = some (Term.i, (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case112_matches : nativeCheck 0 (WireValue.object [("type", (WireValue.array [(WireValue.text "bottom")])), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("rule", (WireValue.text "all_e"))]) = some (Term.i, (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case113_matches : nativeCheck 0 (WireValue.object [("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case114_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "bottom")])), ("rule", (WireValue.text "all_e"))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case115_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "bottom")])), ("rule", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case116_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_e")), ("type", (WireValue.array [(WireValue.text "bottom")]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case117_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "bottom")])), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case118_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))])), ("type", (WireValue.array [(WireValue.text "bottom")])), ("polymorphic", WireValue.null)]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
theorem case119_matches : nativeCheck 0 (WireValue.object [("rule", (WireValue.text "all_e")), ("polymorphic", (WireValue.object [("rule", (WireValue.text "all_i")), ("body", (WireValue.object [("rule", (WireValue.text "i")), ("A", (WireValue.array [(WireValue.text "v"), (WireValue.natural 0)]))]))]))]) = none := by
  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide
