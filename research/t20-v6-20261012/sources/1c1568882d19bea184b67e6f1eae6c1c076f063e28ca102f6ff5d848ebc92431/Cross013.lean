import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- elim312: nonpoly; Python refuse
theorem source_elim312_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app313: application; Python refuse
theorem source_app313_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim314: nonpoly; Python refuse
theorem source_elim314_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app315: application; Python refuse
theorem source_app315_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim316: nonpoly; Python refuse
theorem source_elim316_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app317: application; Python refuse
theorem source_app317_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim318: nonpoly; Python refuse
theorem source_elim318_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) TypeCode.bottom) = none := by decide
-- app319: application; Python refuse
theorem source_app319_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim320: nonpoly; Python refuse
theorem source_elim320_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.var 0)) = none := by decide
-- app321: application; Python refuse
theorem source_app321_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim322: nonpoly; Python refuse
theorem source_elim322_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.var 1)) = none := by decide
-- app323: application; Python refuse
theorem source_app323_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
-- elim324: nonpoly; Python refuse
theorem source_elim324_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app325: application; Python refuse
theorem source_app325_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim326: nonpoly; Python refuse
theorem source_elim326_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app327: application; Python refuse
theorem source_app327_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim328: nonpoly; Python refuse
theorem source_elim328_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app329: application; Python refuse
theorem source_app329_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim330: nonpoly; Python refuse
theorem source_elim330_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom) = none := by decide
-- app331: application; Python refuse
theorem source_app331_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim332: nonpoly; Python refuse
theorem source_elim332_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.var 0)) = none := by decide
-- app333: application; Python refuse
theorem source_app333_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim334: nonpoly; Python refuse
theorem source_elim334_matches : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.var 1)) = none := by decide
-- app335: application; Python refuse
theorem source_app335_matches : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
