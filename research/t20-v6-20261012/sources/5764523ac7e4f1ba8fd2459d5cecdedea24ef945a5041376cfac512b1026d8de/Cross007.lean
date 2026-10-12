import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- elim168: nonpoly; Python refuse
theorem source_elim168_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app169: application; Python refuse
theorem source_app169_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim170: nonpoly; Python refuse
theorem source_elim170_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app171: application; Python refuse
theorem source_app171_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim172: nonpoly; Python refuse
theorem source_elim172_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app173: application; Python refuse
theorem source_app173_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim174: nonpoly; Python refuse
theorem source_elim174_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) TypeCode.bottom) = none := by decide
-- app175: application; Python refuse
theorem source_app175_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim176: nonpoly; Python refuse
theorem source_elim176_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.var 0)) = none := by decide
-- app177: application; Python refuse
theorem source_app177_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim178: nonpoly; Python refuse
theorem source_elim178_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.var 1)) = none := by decide
-- app179: application; Python refuse
theorem source_app179_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
-- elim180: nonpoly; Python refuse
theorem source_elim180_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app181: application; Python refuse
theorem source_app181_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim182: nonpoly; Python refuse
theorem source_elim182_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app183: application; Python refuse
theorem source_app183_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim184: nonpoly; Python refuse
theorem source_elim184_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app185: application; Python refuse
theorem source_app185_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim186: nonpoly; Python refuse
theorem source_elim186_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom) = none := by decide
-- app187: application; Python refuse
theorem source_app187_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim188: nonpoly; Python refuse
theorem source_elim188_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.var 0)) = none := by decide
-- app189: application; Python refuse
theorem source_app189_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim190: nonpoly; Python refuse
theorem source_elim190_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.var 1)) = none := by decide
-- app191: application; Python refuse
theorem source_app191_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
