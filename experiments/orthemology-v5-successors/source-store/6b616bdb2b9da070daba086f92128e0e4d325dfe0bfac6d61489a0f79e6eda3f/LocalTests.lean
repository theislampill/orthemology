import Fixtures
open ComposedExecution
namespace LocalTests
def expect (name : String) (condition : Bool) : IO Unit := do
  unless condition do throw (IO.userError s!"FAIL {name}")
  IO.println s!"PASS {name}"

def runLocal (bytes : List Nat) : IO Unit := do
  let p := plant bytes
  let ip := policy "install-criterion"
  let rp := policy "replace-derived" 3
  expect "C0 accepts the actual extra-LF defect" (CriterionInstallation.accepts p.rule p.draft bytes)
  let result := localStep p ip 2 (.install installCommand)
  expect "compiled install admits successor" result.isSome
  let s := result.getD p
  expect "installed constructor changes actual decision" (!CriterionInstallation.accepts s.rule s.draft bytes)
  expect "installed rule accepts exact source" (CriterionInstallation.accepts s.rule bytes bytes)
  expect "installation full frame" (s == { p with rule := .exact, ruleVersion := 4, ruleHistory := [.normalizedLF] })
  expect "install grant never repairs" (localStep s ip 2 (.repair (repairCommand bytes)) == none)
  expect "C1 token cannot impersonate installed exact rule" (localStep p rp 2 (.repair (repairCommand bytes)) == none)
  let repaired := localStep s rp 2 (.repair (repairCommand bytes))
  expect "separate repair grant restores source" (repaired == some { s with draft := bytes, draftRevision := 9, draftHistory := [[88], bytes ++ [10]] })
  expect "install replay rejected" (localStep s ip 2 (.install installCommand) == none)
  expect "repair replay rejected" (localStep (repaired.getD s) rp 2 (.repair (repairCommand bytes)) == none)
  expect "expired installation rejected" (localStep p ip 100 (.install installCommand) == none)
  expect "copied recipient grant rejected" (localStep p { ip with actor := "B" } 2 (.install { installCommand with actor := "B" }) == none)
  expect "wrong source identity rejected" (localStep { p with source := { p.source with target := ("other", "commit", "path") } } ip 2 (.install installCommand) == none)

end LocalTests
