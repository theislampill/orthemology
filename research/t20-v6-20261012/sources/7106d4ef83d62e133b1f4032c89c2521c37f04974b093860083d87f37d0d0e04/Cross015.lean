import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- elim360: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = none := by decide
-- app361: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) = none := by decide
-- elim362: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- app363: application; Python refuse
example : sourceCheck 2 (SourceProof.app (SourceProof.i (TypeCode.all (TypeCode.var 1))) (SourceProof.i (TypeCode.all (TypeCode.var 1)))) = none := by decide
-- elim364: nonpoly; Python refuse
example : sourceCheck 2 (SourceProof.allE (SourceProof.i (TypeCode.all (TypeCode.var 1))) (TypeCode.all (TypeCode.var 1))) = none := by decide
-- trace365: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) []) = none := by decide
-- trace366: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i]) = none := by decide
-- trace367: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k]) = none := by decide
-- trace368: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero]) = none := by decide
-- trace369: explicit-trace; Python accept
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [(Term.app Term.i Term.i)]) = some ((Term.app Term.i Term.i), (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
-- trace370: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.i]) = none := by decide
-- trace371: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.k]) = none := by decide
-- trace372: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, Term.zero]) = none := by decide
-- trace373: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.i, (Term.app Term.i Term.i)]) = none := by decide
-- trace374: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.i]) = none := by decide
-- trace375: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.k]) = none := by decide
-- trace376: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, Term.zero]) = none := by decide
-- trace377: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.k, (Term.app Term.i Term.i)]) = none := by decide
-- trace378: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.i]) = none := by decide
-- trace379: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.k]) = none := by decide
-- trace380: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, Term.zero]) = none := by decide
-- trace381: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [Term.zero, (Term.app Term.i Term.i)]) = none := by decide
-- trace382: explicit-trace; Python accept
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [(Term.app Term.i Term.i), Term.i]) = some (Term.i, (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
-- trace383: explicit-trace; Python refuse
example : sourceCheck 0 (SourceProof.reduce (SourceProof.app (SourceProof.allE (SourceProof.allI (SourceProof.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (SourceProof.allI (SourceProof.i (TypeCode.var 0)))) [(Term.app Term.i Term.i), Term.k]) = none := by decide
