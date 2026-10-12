import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- elim336: nonpoly; Python refuse
theorem source_elim336_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app337: application; Python refuse
theorem source_app337_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim338: nonpoly; Python refuse
theorem source_elim338_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app339: application; Python refuse
theorem source_app339_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim340: nonpoly; Python refuse
theorem source_elim340_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app341: application; Python refuse
theorem source_app341_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim342: nonpoly; Python refuse
theorem source_elim342_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) TypeCode.bottom) = none := by decide
-- app343: application; Python refuse
theorem source_app343_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim344: nonpoly; Python refuse
theorem source_elim344_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.var 0)) = none := by decide
-- app345: application; Python refuse
theorem source_app345_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim346: nonpoly; Python refuse
theorem source_elim346_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.var 1)) = none := by decide
-- app347: application; Python refuse
theorem source_app347_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
-- elim348: nonpoly; Python refuse
theorem source_elim348_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app349: application; Python refuse
theorem source_app349_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim350: nonpoly; Python refuse
theorem source_elim350_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app351: application; Python refuse
theorem source_app351_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim352: nonpoly; Python refuse
theorem source_elim352_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app353: application; Python refuse
theorem source_app353_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim354: nonpoly; Python refuse
theorem source_elim354_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) TypeCode.bottom) = none := by decide
-- app355: application; Python refuse
theorem source_app355_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim356: nonpoly; Python refuse
theorem source_elim356_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.var 0)) = none := by decide
-- app357: application; Python refuse
theorem source_app357_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim358: nonpoly; Python refuse
theorem source_elim358_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.var 1)) = none := by decide
-- app359: application; Python refuse
theorem source_app359_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
