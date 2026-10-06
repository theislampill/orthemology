import Fixtures
import Lean.Data.Json
open ComposedExecution
open Lean
namespace Artifacts

def ruleJson (r : CriterionInstallation.Rule) : Json :=
  toJson (match r with | .exact => "exact" | .normalizedLF => "normalizedLF")

def plantJson (p : Plant) : Json := Json.mkObj [
  ("source", Json.mkObj [
    ("target", toJson [p.source.target.1, p.source.target.2.1, p.source.target.2.2]),
    ("content", toJson p.source.content), ("roots", toJson p.source.roots)]),
  ("destination", toJson p.destination), ("standard", toJson p.standard),
  ("draft", toJson p.draft), ("draft_revision", toJson p.draftRevision),
  ("draft_history", toJson p.draftHistory), ("rule", ruleJson p.rule),
  ("rule_version", toJson p.ruleVersion), ("rule_history", toJson (p.ruleHistory.map ruleJson)),
  ("unrelated", toJson p.unrelated)]

def writeArtifacts (bytes : List Nat) (out : System.FilePath) : IO Unit := do
  let p := plant bytes
  let ip := policy "install-criterion"
  let rp := policy "replace-derived" 3
  let actor : Actor := ⟨ip, p, "A", 2, 0⟩
  let predictedInstalled := (localStep actor.observedPlant actor.policy actor.observedTime (.install installCommand)).getD p
  let (installed, _) := runBatch (initialWorld p ip [0]) actor (.install installCommand)
  let nextActor := { actor with observedPlant := predictedInstalled, nonce := 4 }
  let (revoked, cert) := certifyTransition installed [0,1,2] rp
  let certificate := cert.getD ⟨2, rp, [0,1,2]⟩
  let repairActor := receiveActor nextActor certificate 4 3
  let (repaired, _) := runBatch (deliver revoked certificate) repairActor (.repair (repairCommand bytes))
  IO.FS.writeFile (out / "before.json") ((plantJson p).compress ++ "\n")
  IO.FS.writeFile (out / "installed.json") ((plantJson installed.plant).compress ++ "\n")
  IO.FS.writeFile (out / "repaired.json") ((plantJson repaired.plant).compress ++ "\n")
  IO.FS.writeBinFile (out / "preserved-source.bin") (ByteArray.mk (repaired.plant.source.content.map UInt8.ofNat).toArray)
  IO.FS.writeBinFile (out / "repaired-draft.bin") (ByteArray.mk (repaired.plant.draft.map UInt8.ofNat).toArray)

end Artifacts
