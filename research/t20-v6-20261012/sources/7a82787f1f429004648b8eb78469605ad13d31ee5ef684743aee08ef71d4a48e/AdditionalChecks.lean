import Controls

namespace GuardedTree.Executable.IndependentReview
open Controls

def noRules : Grammar Unit Nat Empty where
  arity := fun r => nomatch r
  head := fun r => nomatch r
  premise := fun r => nomatch r
  localSupport := fun r => nomatch r
  price := fun r => nomatch r
  guard := fun r => nomatch r
instance : ∀ r s, Decidable (noRules.guard r s) := fun r => nomatch r

def noJudgements : Grammar Empty Nat Empty where
  arity := fun r => nomatch r
  head := fun r => nomatch r
  premise := fun r => nomatch r
  localSupport := fun r => nomatch r
  price := fun r => nomatch r
  guard := fun r => nomatch r
instance : ∀ r s, Decidable (noJudgements.guard r s) := fun r => nomatch r

def negativeSeed : Grammar Unit Nat Unit where
  arity := fun _ => 0
  head := fun _ => ()
  premise := fun _ _ => ()
  localSupport := fun _ => {4}
  price := fun _ => -2/3
  guard := fun _ _ => True
instance : ∀ r s, Decidable (negativeSeed.guard r s) := fun _ _ => isTrue trivial

def runAdditionalChecks : IO Unit := do
  check "review empty rule set" (read (compile noRules) () ∅) none
  unless compile noJudgements == ∅ do
    throw (IO.userError "empty judgements produced a row")
  IO.println "PASS review empty judgement universe"
  check "review negative rational nullary" (read (compileRounds negativeSeed 1) () {4}) (some (-2/3))
  check "review seeded cycle at round four" (read (compileRounds seeded 4) () ∅) (some 0)
  unless (choices seeded).card == 2 do
    throw (IO.userError "nullary and unary enumeration cardinality wrong")
  IO.println "PASS review nullary/unary enumeration cardinality"
  unless (choices blocked).card == 1 do
    throw (IO.userError "nullary enumeration does not contain exactly the empty tuple")
  IO.println "PASS review one empty tuple for nullary rule"
  unless (choices ordered).card == 35 do
    throw (IO.userError "ordered product enumeration cardinality wrong")
  IO.println "PASS review ordered product cardinality 3 + 2 * 4^2 = 35"

#eval runAdditionalChecks

#print GuardedTree.Executable.choices
#print GuardedTree.Executable.candidates
#print GuardedTree.Executable.minimum
#print GuardedTree.Executable.compileStep
#print GuardedTree.Executable.compileRounds
#print GuardedTree.Executable.compile
#print axioms GuardedTree.Executable.mem_choices
#print axioms GuardedTree.Executable.minimum_eq
#print axioms GuardedTree.Executable.step_eq
#print axioms GuardedTree.Executable.mem_materialize
#print axioms GuardedTree.Executable.values_materialize
#print axioms GuardedTree.Executable.minimum_toFinset
#print axioms GuardedTree.Executable.read_materialize
#print axioms GuardedTree.Executable.round_outside
#print axioms GuardedTree.Executable.compile_rows_stable
#print axioms GuardedTree.Executable.choices
#print axioms GuardedTree.Executable.candidates
#print axioms GuardedTree.Executable.minimum
#print axioms GuardedTree.Executable.compileStep
#print axioms GuardedTree.Executable.compileRounds
#print axioms GuardedTree.Executable.compile

end GuardedTree.Executable.IndependentReview
