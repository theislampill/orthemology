import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- elim264: nonpoly; Python refuse
theorem source_elim264_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app265: application; Python refuse
theorem source_app265_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim266: nonpoly; Python refuse
theorem source_elim266_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app267: application; Python refuse
theorem source_app267_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim268: nonpoly; Python refuse
theorem source_elim268_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app269: application; Python refuse
theorem source_app269_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim270: nonpoly; Python refuse
theorem source_elim270_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) TypeCode.bottom) = none := by decide
-- app271: application; Python refuse
theorem source_app271_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim272: nonpoly; Python refuse
theorem source_elim272_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.var 0)) = none := by decide
-- app273: application; Python refuse
theorem source_app273_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim274: nonpoly; Python refuse
theorem source_elim274_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.var 1)) = none := by decide
-- app275: application; Python refuse
theorem source_app275_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
-- elim276: nonpoly; Python refuse
theorem source_elim276_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app277: application; Python refuse
theorem source_app277_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim278: nonpoly; Python refuse
theorem source_elim278_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app279: application; Python refuse
theorem source_app279_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim280: nonpoly; Python refuse
theorem source_elim280_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app281: application; Python refuse
theorem source_app281_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim282: nonpoly; Python refuse
theorem source_elim282_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) TypeCode.bottom) = none := by decide
-- app283: application; Python refuse
theorem source_app283_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim284: nonpoly; Python refuse
theorem source_elim284_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.var 0)) = none := by decide
-- app285: application; Python refuse
theorem source_app285_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim286: nonpoly; Python refuse
theorem source_elim286_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.var 1)) = none := by decide
-- app287: application; Python refuse
theorem source_app287_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
