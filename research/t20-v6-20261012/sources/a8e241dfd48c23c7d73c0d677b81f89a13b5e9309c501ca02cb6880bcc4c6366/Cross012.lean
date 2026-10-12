import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- elim288: nonpoly; Python refuse
example : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app289: application; Python refuse
example : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim290: nonpoly; Python refuse
example : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app291: application; Python refuse
example : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim292: nonpoly; Python refuse
example : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app293: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim294: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i TypeCode.bottom) TypeCode.bottom) = none := by decide
-- app295: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim296: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.var 0)) = none := by decide
-- app297: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim298: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.var 1)) = none := by decide
-- app299: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
-- elim300: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app301: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim302: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app303: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim304: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app305: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim306: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) TypeCode.bottom) = none := by decide
-- app307: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim308: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.var 0)) = none := by decide
-- app309: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim310: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.var 1)) = none := by decide
-- app311: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
