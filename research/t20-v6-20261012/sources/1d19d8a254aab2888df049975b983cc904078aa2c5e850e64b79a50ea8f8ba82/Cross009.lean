import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- elim216: nonpoly; Python refuse
theorem source_elim216_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app217: application; Python refuse
theorem source_app217_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim218: nonpoly; Python refuse
theorem source_elim218_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app219: application; Python refuse
theorem source_app219_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim220: nonpoly; Python refuse
theorem source_elim220_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app221: application; Python refuse
theorem source_app221_matches : sourceCheck 1 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim222: nonpoly; Python refuse
theorem source_elim222_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i TypeCode.bottom) TypeCode.bottom) = none := by decide
-- app223: application; Python refuse
theorem source_app223_matches : sourceCheck 1 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim224: nonpoly; Python refuse
theorem source_elim224_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.var 0)) = none := by decide
-- app225: application; Python refuse
theorem source_app225_matches : sourceCheck 1 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim226: nonpoly; Python refuse
theorem source_elim226_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.var 1)) = none := by decide
-- app227: application; Python refuse
theorem source_app227_matches : sourceCheck 1 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
-- elim228: nonpoly; Python refuse
theorem source_elim228_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app229: application; Python refuse
theorem source_app229_matches : sourceCheck 1 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim230: nonpoly; Python refuse
theorem source_elim230_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app231: application; Python refuse
theorem source_app231_matches : sourceCheck 1 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim232: nonpoly; Python refuse
theorem source_elim232_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app233: application; Python refuse
theorem source_app233_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim234: nonpoly; Python refuse
theorem source_elim234_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) TypeCode.bottom) = none := by decide
-- app235: application; Python refuse
theorem source_app235_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim236: nonpoly; Python refuse
theorem source_elim236_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.var 0)) = none := by decide
-- app237: application; Python refuse
theorem source_app237_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim238: nonpoly; Python refuse
theorem source_elim238_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.var 1)) = none := by decide
-- app239: application; Python refuse
theorem source_app239_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
