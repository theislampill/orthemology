import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- elim240: nonpoly; Python refuse
theorem source_elim240_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app241: application; Python refuse
theorem source_app241_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim242: nonpoly; Python refuse
theorem source_elim242_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app243: application; Python refuse
theorem source_app243_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 0)) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim244: nonpoly; Python refuse
theorem source_elim244_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 0)) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app245: application; Python refuse
theorem source_app245_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim246: nonpoly; Python refuse
theorem source_elim246_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) TypeCode.bottom) = none := by decide
-- app247: application; Python refuse
theorem source_app247_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim248: nonpoly; Python refuse
theorem source_elim248_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.var 0)) = none := by decide
-- app249: application; Python refuse
theorem source_app249_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim250: nonpoly; Python refuse
theorem source_elim250_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.var 1)) = none := by decide
-- app251: application; Python refuse
theorem source_app251_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
-- elim252: nonpoly; Python refuse
theorem source_elim252_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app253: application; Python refuse
theorem source_app253_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim254: nonpoly; Python refuse
theorem source_elim254_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app255: application; Python refuse
theorem source_app255_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.var 1)) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim256: nonpoly; Python refuse
theorem source_elim256_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.var 1)) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- app257: application; Python refuse
theorem source_app257_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i TypeCode.bottom)) = none := by decide
-- elim258: nonpoly; Python refuse
theorem source_elim258_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom) = none := by decide
-- app259: application; Python refuse
theorem source_app259_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.var 0))) = none := by decide
-- elim260: nonpoly; Python refuse
theorem source_elim260_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.var 0)) = none := by decide
-- app261: application; Python refuse
theorem source_app261_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.var 1))) = none := by decide
-- elim262: nonpoly; Python refuse
theorem source_elim262_matches : sourceCheck 1 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.var 1)) = none := by decide
-- app263: application; Python refuse
theorem source_app263_matches : sourceCheck 1 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) = none := by decide
