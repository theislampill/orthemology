import TypedCriterionGuard

open TypedCriterionGuard

def target : Target :=
  ("theislampill/orthemology", "19de267cd41d2a5eeeb3eaf0b91562f706e2a916",
   "docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md")

def actor (n : Nat) : String := if n = 0 then "A" else "B"

def draftValue (source : List Nat) (tag : Nat) : List Nat :=
  if tag = 0 then source else if tag = 1 then source ++ [10]
  else [119, 114, 111, 110, 103]

/- Only generated trusted CSV rows enter this replay tool. It is not a
validated external parser or security-facing endpoint. -/
def decode (sourceBytes : List Nat) (row : Array Nat) : State × Command := Id.run do
  let destination := actor row[0]! ++ "/draft"
  let grant := if row[6]! = 1 then
      some (Grant.mk (actor row[7]!) destination target row[2]! 0 row[8]! "replace-derived")
    else none
  let source := Source.mk target sourceBytes ["canonical-github-object"]
  let oldHistory := [114, 101, 116, 97, 105, 110, 101, 100, 45, 101, 97, 114, 108, 105,
                     101, 114, 45, 104, 105, 115, 116, 111, 114, 121]
  let state := State.mk source destination (draftValue sourceBytes row[5]!) row[1]!
    row[2]! grant (row[3]! == 1) row[4]! [oldHistory]
  let command := Command.mk (actor row[9]!) destination target
    (if row[13]! = 0 then "C1-exact" else "C0-normalized") row[10]! row[11]!
    (draftValue sourceBytes row[14]!)
    (if row[12]! = 0 then "replace-derived" else "overwrite-source") row[15]! row[16]!
  return (state, command)

def outputLine (index : Nat) (source : List Nat) (before : State) (result : Outcome) : String :=
  let tag := if result.state.draft == source then 0
    else if result.state.draft == source ++ [10] then 1 else 2
  let applied := if result.applied then 1 else 0
  let sourcePreserved := if result.state.source == before.source then 1 else 0
  s!"{index},{applied},{result.state.revision},{tag},{result.state.history.length},{sourcePreserved}"

def main : IO Unit := do
  let bytes ← IO.FS.readBinFile "sources/proper-function-and-candidate-e.md"
  let source := bytes.toList.map UInt8.toNat
  let lines ← IO.FS.lines "evidence/shared_fixtures.csv"
  IO.FS.withFile "evidence/lean_actual.csv" .write fun output => do
    let mut index := 0
    for line in lines do
      if !line.isEmpty then
        let row := (line.splitOn ",").map String.toNat! |>.toArray
        if row.size != 17 then throw <| IO.userError s!"fixture {index}: expected 17 fields"
        let (state, command) := decode source row
        output.putStrLn (outputLine index source state (execute state command))
        index := index + 1
    IO.println s!"Replayed {index} typed fixtures"
