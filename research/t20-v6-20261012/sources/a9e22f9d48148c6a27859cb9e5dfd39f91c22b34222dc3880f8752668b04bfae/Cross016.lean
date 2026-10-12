import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- trace384: explicit-trace; Python refuse
theorem source_trace384_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [(Term.app Term.i Term.i), Term.zero]) = none := by decide
-- trace385: explicit-trace; Python refuse
theorem source_trace385_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [(Term.app Term.i Term.i), (Term.app Term.i Term.i)]) = none := by decide
-- trace386: explicit-trace; Python refuse
theorem source_trace386_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.i, Term.i]) = none := by decide
-- trace387: explicit-trace; Python refuse
theorem source_trace387_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.i, Term.k]) = none := by decide
-- trace388: explicit-trace; Python refuse
theorem source_trace388_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.i, Term.zero]) = none := by decide
-- trace389: explicit-trace; Python refuse
theorem source_trace389_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.i, (Term.app Term.i Term.i)]) = none := by decide
-- trace390: explicit-trace; Python refuse
theorem source_trace390_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.k, Term.i]) = none := by decide
-- trace391: explicit-trace; Python refuse
theorem source_trace391_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.k, Term.k]) = none := by decide
-- trace392: explicit-trace; Python refuse
theorem source_trace392_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.k, Term.zero]) = none := by decide
-- trace393: explicit-trace; Python refuse
theorem source_trace393_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.k, (Term.app Term.i Term.i)]) = none := by decide
-- trace394: explicit-trace; Python refuse
theorem source_trace394_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.zero, Term.i]) = none := by decide
-- trace395: explicit-trace; Python refuse
theorem source_trace395_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.zero, Term.k]) = none := by decide
-- trace396: explicit-trace; Python refuse
theorem source_trace396_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.zero, Term.zero]) = none := by decide
-- trace397: explicit-trace; Python refuse
theorem source_trace397_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.zero, (Term.app Term.i Term.i)]) = none := by decide
-- trace398: explicit-trace; Python refuse
theorem source_trace398_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, (Term.app Term.i Term.i), Term.i]) = none := by decide
-- trace399: explicit-trace; Python refuse
theorem source_trace399_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, (Term.app Term.i Term.i), Term.k]) = none := by decide
-- trace400: explicit-trace; Python refuse
theorem source_trace400_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, (Term.app Term.i Term.i), Term.zero]) = none := by decide
-- trace401: explicit-trace; Python refuse
theorem source_trace401_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, (Term.app Term.i Term.i), (Term.app Term.i Term.i)]) = none := by decide
-- trace402: explicit-trace; Python refuse
theorem source_trace402_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.i, Term.i]) = none := by decide
-- trace403: explicit-trace; Python refuse
theorem source_trace403_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.i, Term.k]) = none := by decide
-- trace404: explicit-trace; Python refuse
theorem source_trace404_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.i, Term.zero]) = none := by decide
-- trace405: explicit-trace; Python refuse
theorem source_trace405_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.i, (Term.app Term.i Term.i)]) = none := by decide
-- trace406: explicit-trace; Python refuse
theorem source_trace406_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.k, Term.i]) = none := by decide
-- trace407: explicit-trace; Python refuse
theorem source_trace407_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.k, Term.k]) = none := by decide
