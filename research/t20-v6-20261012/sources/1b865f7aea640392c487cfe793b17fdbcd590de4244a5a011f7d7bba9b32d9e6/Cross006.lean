import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- scope144: scope-or-depth; Python refuse
theorem source_scope144_matches : sourceCheck 101 (SourceProof.i (TypeCode.var 0)) = none := by decide
-- scope145: scope-or-depth; Python refuse
theorem source_scope145_matches : sourceCheck 101 (SourceProof.i (TypeCode.var 1)) = none := by decide
-- scope146: scope-or-depth; Python refuse
theorem source_scope146_matches : sourceCheck 101 (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- scope147: scope-or-depth; Python refuse
theorem source_scope147_matches : sourceCheck 101 (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- scope148: scope-or-depth; Python refuse
theorem source_scope148_matches : sourceCheck 101 (SourceProof.i (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app149: application; Python refuse
theorem source_app149_matches : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim150: nonpoly; Python refuse
theorem source_elim150_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) TypeCode.bottom) = none := by decide
-- app151: application; Python refuse
theorem source_app151_matches : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim152: nonpoly; Python refuse
theorem source_elim152_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.var 0)) = none := by decide
-- app153: application; Python refuse
theorem source_app153_matches : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim154: nonpoly; Python refuse
theorem source_elim154_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.var 1)) = none := by decide
-- app155: application; Python refuse
theorem source_app155_matches : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
-- elim156: nonpoly; Python refuse
theorem source_elim156_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app157: application; Python refuse
theorem source_app157_matches : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim158: nonpoly; Python refuse
theorem source_elim158_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app159: application; Python refuse
theorem source_app159_matches : sourceCheck 0 (SourceProof.app (SourceProof.i TypeCode.bottom) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim160: nonpoly; Python refuse
theorem source_elim160_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i TypeCode.bottom) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app161: application; Python refuse
theorem source_app161_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim162: nonpoly; Python refuse
theorem source_elim162_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) TypeCode.bottom) = none := by decide
-- app163: application; Python refuse
theorem source_app163_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim164: nonpoly; Python refuse
theorem source_elim164_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.var 0)) = none := by decide
-- app165: application; Python refuse
theorem source_app165_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim166: nonpoly; Python refuse
theorem source_elim166_matches : sourceCheck 0 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.var 1)) = none := by decide
-- app167: application; Python refuse
theorem source_app167_matches : sourceCheck 0 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
