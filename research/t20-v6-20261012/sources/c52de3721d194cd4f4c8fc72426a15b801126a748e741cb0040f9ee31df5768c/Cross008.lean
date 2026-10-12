import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- elim192: nonpoly; Python refuse
theorem source_elim192_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app193: application; Python refuse
theorem source_app193_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim194: nonpoly; Python refuse
theorem source_elim194_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app195: application; Python refuse
theorem source_app195_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim196: nonpoly; Python refuse
theorem source_elim196_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app197: application; Python refuse
theorem source_app197_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim198: nonpoly; Python refuse
theorem source_elim198_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) TypeCode.bottom) = none := by decide
-- app199: application; Python refuse
theorem source_app199_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim200: nonpoly; Python refuse
theorem source_elim200_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.var 0)) = none := by decide
-- app201: application; Python refuse
theorem source_app201_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim202: nonpoly; Python refuse
theorem source_elim202_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.var 1)) = none := by decide
-- app203: application; Python refuse
theorem source_app203_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
-- elim204: nonpoly; Python refuse
theorem source_elim204_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app205: application; Python refuse
theorem source_app205_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim206: nonpoly; Python refuse
theorem source_elim206_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app207: application; Python refuse
theorem source_app207_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim208: nonpoly; Python refuse
theorem source_elim208_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app209: application; Python refuse
theorem source_app209_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim210: nonpoly; Python refuse
theorem source_elim210_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) TypeCode.bottom) = none := by decide
-- app211: application; Python refuse
theorem source_app211_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim212: nonpoly; Python refuse
theorem source_elim212_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.var 0)) = none := by decide
-- app213: application; Python refuse
theorem source_app213_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim214: nonpoly; Python refuse
theorem source_elim214_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.var 1)) = none := by decide
-- app215: application; Python refuse
theorem source_app215_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
