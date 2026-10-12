import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- scope144: scope-or-depth; Python refuse
example : sourceCheck 101 (SourceProof.i (TypeCode.var 0)) = none := by decide
-- scope145: scope-or-depth; Python refuse
example : sourceCheck 101 (SourceProof.i (TypeCode.var 1)) = none := by decide
-- scope146: scope-or-depth; Python refuse
example : sourceCheck 101 (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- scope147: scope-or-depth; Python refuse
example : sourceCheck 101 (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- scope148: scope-or-depth; Python refuse
example : sourceCheck 101 (SourceProof.i (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app149: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim150: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) TypeCode.bottom) = none := by decide
-- app151: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim152: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.var 0)) = none := by decide
-- app153: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim154: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.var 1)) = none := by decide
-- app155: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
-- elim156: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app157: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim158: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app159: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim160: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app161: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim162: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) TypeCode.bottom) = none := by decide
-- app163: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim164: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.var 0)) = none := by decide
-- app165: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim166: nonpoly; Python refuse
example : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.var 1)) = none := by decide
-- app167: application; Python refuse
example : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
