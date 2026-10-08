import CriterionInstallation

open TypedCriterionGuard (Target Source Grant)
open CriterionInstallation

def target : Target :=
  ("theislampill/orthemology", "19de267cd41d2a5eeeb3eaf0b91562f706e2a916",
   "docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md")

def actor (n : Nat) : String := if n = 0 then "A" else "B"
def criterion (n : Nat) : Rule := if n = 0 then .normalizedLF else .exact
def operation (n : Nat) : String := if n = 0 then "install-criterion" else "replace-derived"

def decode (bytes : List Nat) (row : Array Nat) : RuleState × InstallCommand := Id.run do
  let dest := actor row[0]! ++ "/package"
  let source := Source.mk target bytes ["canonical-github-object"]
  let grant := Grant.mk (actor row[0]!) dest target 2 0 10 (operation row[3]!)
  let state := RuleState.mk source dest "exact-source-recovery" (bytes ++ [10]) 8
    (criterion row[1]!) row[2]! 2 (some grant) (row[4]! == 1)
    (if row[11]! = 0 then 4 else 9) [.normalizedLF]
    ["retain-original-source", "no-GitHub-mutation"]
  let command := InstallCommand.mk (actor row[5]!) dest target (criterion row[6]!)
    row[7]! (if row[10]! = 0 then 2 else 3) (criterion row[8]!) (operation row[9]!) 3 9
  return (state, command)

def bit (b : Bool) : Nat := if b then 1 else 0

def project (index : Nat) (before : RuleState) (result : InstallOutcome) : String :=
  let after := result.state
  let source := before.source.content
  let otherWrong := 88 :: source.drop 1
  let fields := [index, bit result.applied, bit (after.rule == .exact), after.ruleVersion,
    bit (after.draft == before.draft), bit (after.source == before.source), after.ruleHistory.length,
    bit (after.unrelated == before.unrelated), bit (accepts after.rule source source),
    bit (accepts after.rule (source ++ [10]) source), bit (accepts after.rule otherWrong source)]
  String.intercalate "," (fields.map toString)

def main : IO Unit := do
  let bytes ← IO.FS.readBinFile "sources/proper-function-and-candidate-e.md"
  let source := bytes.toList.map UInt8.toNat
  let lines ← IO.FS.lines "evidence/rule_install_fixtures.csv"
  IO.FS.withFile "evidence/rule_install_lean.csv" .write fun output => do
    let mut index := 0
    for line in lines do
      if !line.isEmpty then
        let row := (line.splitOn ",").map String.toNat! |>.toArray
        if row.size != 12 then throw <| IO.userError s!"fixture {index}: expected 12 fields"
        let (state, command) := decode source row
        output.putStrLn (project index state (install state command))
        index := index + 1
    IO.println s!"Replayed {index} typed criterion-installation fixtures"
