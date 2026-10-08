import SignedControllerService
import SmallFixtures
open OrthemicCertificate OrthemicCertificate.Signed OrthemicCertificate.Signed.Fixtures

private def returnedAction (I : Input q n k) (B : Support q) (s : Fin n)
    (h : List (Fin k × Fin n)) : Option (Fin k) :=
  match solveCompiled I B s with
  | .positive _ policy => some (policy () h)
  | _ => none

private def returnedBodyChecked (I : Input q n k) (B : Support q) (s : Fin n) : Bool :=
  match solveCompiled I B s with
  | .positive c _ => check I c B s
  | _ => false

private def returnedNegativeChecked (I : Input q n k) (B : Support q) (s : Fin n) : Bool :=
  match solveCompiled I B s with
  | .negative d => negativeCheck I B s d
  | _ => false

#guard returnedAction evenInput {0} 0 [] = some 0
#guard returnedAction evenInput {0} 0 [(0,0)] = some 0
#guard returnedAction evenInput {0} 0 (List.replicate 20 (0,0)) = some 0
#guard returnedBodyChecked evenInput {0} 0
#guard returnedAction oddInput {0} 0 [] = none
#guard returnedNegativeChecked oddInput {0} 0
#guard returnedAction evenInput ∅ 0 [] = none
#guard returnedAction ({evenInput with rows := #[]} : Input 1 1 1) {0} 0 [] = none
#eval (returnedAction evenInput {0} 0 [],returnedNegativeChecked oddInput {0} 0)
#print axioms solveCompiled_correct
#print axioms solveCompiled_positive_iff_semantic
#print axioms solveCompiled_negative_iff_not_semantic
