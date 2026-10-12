import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- elim168: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app169: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim170: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app171: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim172: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app173: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim174: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) TypeCode.bottom) = none := by decide
-- app175: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim176: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.var 0)) = none := by decide
-- app177: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim178: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.var 1)) = none := by decide
-- app179: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
-- elim180: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app181: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim182: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app183: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim184: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app185: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim186: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom) = none := by decide
-- app187: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim188: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.var 0)) = none := by decide
-- app189: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim190: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.var 1)) = none := by decide
-- app191: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
