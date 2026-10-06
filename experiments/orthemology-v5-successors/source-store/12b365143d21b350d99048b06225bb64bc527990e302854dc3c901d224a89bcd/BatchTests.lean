import Fixtures
open ComposedExecution
namespace BatchTests

def require (name : String) (condition : Bool) : IO Unit := do
  unless condition do throw (IO.userError s!"FAIL {name}")
  IO.println s!"PASS {name}"

def runBatches (bytes : List Nat) : IO Unit := do
  let p := plant bytes
  let ip := policy "install-criterion"
  let rp := policy "replace-derived" 3
  let expectedInstalled := { p with rule := .exact, ruleVersion := 4, ruleHistory := [.normalizedLF] }
  let expectedRepaired := { expectedInstalled with draft := bytes, draftRevision := 9, draftHistory := [[88], bytes ++ [10]] }
  for bad in [[], [0], [1], [2], [3]] do
    let actor : Actor := ⟨ip, p, "A", 2, 0⟩
    let w := initialWorld p ip bad
    let (installed, installTrace) := runBatch w actor (.install installCommand)
    require s!"install-batch-{bad}: exact full successor" (installed.plant == expectedInstalled)
    require s!"install-batch-{bad}: four safely closed trials" (installTrace.length == 4 && installTrace.all (·.closed))
    require s!"install-batch-{bad}: exactly one version/history change" ((installTrace.filter (·.landed)).length == 1)
    -- No untrusted effect receipt is used for the actor's knowledge. The stable
    -- complete batch theorem warrants this exact predicted observation.
    let actorAfter := { actor with observedPlant := expectedInstalled, nonce := 4 }
    let (revoked, cert) := certifyTransition installed [0,1,2] rp
    require s!"repair-batch-{bad}: external scoped grant transition" cert.isSome
    let certificate := cert.getD ⟨2, rp, [0,1,2]⟩
    let actorRepair := receiveActor actorAfter certificate 4 3
    let (repaired, repairTrace) := runBatch (deliver revoked certificate) actorRepair (.repair (repairCommand bytes))
    require s!"repair-batch-{bad}: exact full successor" (repaired.plant == expectedRepaired)
    require s!"repair-batch-{bad}: four safely closed trials" (repairTrace.length == 4 && repairTrace.all (·.closed))
    require s!"repair-batch-{bad}: exactly one version/history change" ((repairTrace.filter (·.landed)).length == 1)
    require s!"repair-batch-{bad}: original source and custody survive" (repaired.plant.source == p.source && repaired.plant.unrelated == p.unrelated)
    IO.println s!"TRACE bad={bad} install={repr installTrace} repair={repr repairTrace}"

end BatchTests
