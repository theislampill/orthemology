import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- trace408: explicit-trace; Python refuse
theorem source_trace408_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.k, Term.zero]) = none := by decide
-- trace409: explicit-trace; Python refuse
theorem source_trace409_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.k, (Term.app Term.i Term.i)]) = none := by decide
-- trace410: explicit-trace; Python refuse
theorem source_trace410_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.zero, Term.i]) = none := by decide
-- trace411: explicit-trace; Python refuse
theorem source_trace411_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.zero, Term.k]) = none := by decide
-- trace412: explicit-trace; Python refuse
theorem source_trace412_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.zero, Term.zero]) = none := by decide
-- trace413: explicit-trace; Python refuse
theorem source_trace413_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.zero, (Term.app Term.i Term.i)]) = none := by decide
-- trace414: explicit-trace; Python refuse
theorem source_trace414_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, (Term.app Term.i Term.i), Term.i]) = none := by decide
-- trace415: explicit-trace; Python refuse
theorem source_trace415_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, (Term.app Term.i Term.i), Term.k]) = none := by decide
-- trace416: explicit-trace; Python refuse
theorem source_trace416_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, (Term.app Term.i Term.i), Term.zero]) = none := by decide
-- trace417: explicit-trace; Python refuse
theorem source_trace417_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, (Term.app Term.i Term.i), (Term.app Term.i Term.i)]) = none := by decide
-- trace418: explicit-trace; Python refuse
theorem source_trace418_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.i, Term.i]) = none := by decide
-- trace419: explicit-trace; Python refuse
theorem source_trace419_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.i, Term.k]) = none := by decide
-- trace420: explicit-trace; Python refuse
theorem source_trace420_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.i, Term.zero]) = none := by decide
-- trace421: explicit-trace; Python refuse
theorem source_trace421_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.i, (Term.app Term.i Term.i)]) = none := by decide
-- trace422: explicit-trace; Python refuse
theorem source_trace422_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.k, Term.i]) = none := by decide
-- trace423: explicit-trace; Python refuse
theorem source_trace423_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.k, Term.k]) = none := by decide
-- trace424: explicit-trace; Python refuse
theorem source_trace424_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.k, Term.zero]) = none := by decide
-- trace425: explicit-trace; Python refuse
theorem source_trace425_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.k, (Term.app Term.i Term.i)]) = none := by decide
-- trace426: explicit-trace; Python refuse
theorem source_trace426_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.zero, Term.i]) = none := by decide
-- trace427: explicit-trace; Python refuse
theorem source_trace427_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.zero, Term.k]) = none := by decide
-- trace428: explicit-trace; Python refuse
theorem source_trace428_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.zero, Term.zero]) = none := by decide
-- trace429: explicit-trace; Python refuse
theorem source_trace429_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.zero, (Term.app Term.i Term.i)]) = none := by decide
-- trace430: explicit-trace; Python refuse
theorem source_trace430_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, (Term.app Term.i Term.i), Term.i]) = none := by decide
-- trace431: explicit-trace; Python refuse
theorem source_trace431_matches : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, (Term.app Term.i Term.i), Term.k]) = none := by decide
