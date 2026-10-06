import Fixtures
open ComposedExecution
namespace RaceTests

def check (name : String) (condition : Bool) : IO Unit := do
  unless condition do throw (IO.userError s!"FAIL {name}")
  IO.println s!"PASS {name}"

def subsets2 (xs : List Nat) : List (List Nat) :=
  (xs.flatMap fun i => xs.filterMap fun j => if i < j then some [i,j] else none)

def runRaces (bytes : List Nat) : IO Unit := do
  let p := plant bytes
  let ip := policy "install-criterion"
  let rp := policy "replace-derived" 3
  let actor : Actor := ⟨ip, p, "A", 2, 0⟩
  let fallback : Envelope := ⟨.install installCommand, p, 1, [0,1,2]⟩
  let mutablyEmpty : List Nat := []
  let _ := mutablyEmpty
  let mut revokeCases := 0
  let mut cancelCases := 0
  let mut safeCases := 0
  for bad in [[], [0], [1], [2], [3]] do
    for path in fourPaths do
      let e := (propose actor (.install installCommand) path).getD fallback
      let prepared := (prepare (initialWorld p ip bad) e "A").1
      for acknowledgers in fourPaths do
        let (revoked, certificate) := certifyTransition prepared acknowledgers rp
        unless certificate.isSome && !(attempt revoked e "A").2 && (attempt revoked e "A").1.plant == p do
          throw (IO.userError s!"FAIL revoked {bad} {path} {acknowledgers}")
        revokeCases := revokeCases + 1
      for acknowledgers in subsets2 path do
        let (closed, complete) := cancelWith prepared e "A" acknowledgers
        unless complete && !(attempt closed e "A").2 && (attempt closed e "A").1.plant == p do
          throw (IO.userError s!"FAIL cancelled {bad} {path} {acknowledgers}")
        cancelCases := cancelCases + 1
      let (openWorld, applied) := attempt prepared e "A" true
      unless applied && openWorld.plant == e.successor do
        throw (IO.userError "FAIL opened path did not consume source successor")
      let (withheld, _) := attempt prepared e "A" false
      unless withheld.plant == p || withheld.plant == e.successor do
        throw (IO.userError "FAIL path escaped identity/successor envelope")
      safeCases := safeCases + 1
  check "finite revocation interleavings: 80" (revokeCases == 80)
  check "finite cancellation interleavings: 60" (cancelCases == 60)
  check "finite open/withheld envelope effects: 20" (safeCases == 20)

  let e := (propose actor (.install installCommand) [0,1,2]).getD fallback
  let prepared := (prepare (initialWorld p ip [3]) e "A").1
  let original := prepared.plant
  let changedDraft := { prepared with plant := { p with draftRevision := p.draftRevision + 1 } }
  check "install full successor prevents concurrent draft overwrite" (!(attempt changedDraft e "A").2 && (attempt changedDraft e "A").1.plant == changedDraft.plant)
  let tampered := { e with successor := { e.successor with draft := [0] } }
  check "post-prepare successor mutation rejected" (!(attempt prepared tampered "A").2 && (attempt prepared tampered "A").1.plant == original)
  check "foreign requester cannot reuse A commitment" (!(attempt prepared e "B").2)
  check "expired interval at landing defeats old preparation" (!(attempt { prepared with now := 100 } e "A").2)
  let changedSource := { prepared with plant := { p with source := { p.source with content := [0] } } }
  check "changed source content cannot be overwritten by old proposal" (!(attempt changedSource e "A").2)

  let installed := e.successor
  let ra : Actor := ⟨rp, installed, "A", 2, 4⟩
  let re := (propose ra (.repair (repairCommand bytes)) [0,1,2]).getD fallback
  let rprepared := (prepare (initialWorld installed rp [3]) re "A").1
  let changedRule := { rprepared with plant := { installed with ruleVersion := 5, ruleHistory := [.normalizedLF, .exact] } }
  check "repair full successor prevents concurrent rule/history overwrite" (!(attempt changedRule re "A").2 && (attempt changedRule re "A").1.plant == changedRule.plant)
  let changedCriterion := { rprepared with plant := { installed with rule := .normalizedLF } }
  check "actual installed C0 blocks prepared C1-string repair" (!(attempt changedCriterion re "A").2)

  -- These two traces intentionally violate a premise; they are countermodels,
  -- not modes of the positive algorithm.
  let unsignalled := { prepared with effectivePolicy := { ip with allowed := false } }
  let externalCeased := (attempt unsignalled e "A").2
  check "deletion: immediate unseen external consent loss can still land" externalCeased
  let (withBad, _) := prepare (initialWorld p ip [0]) e "A"
  let (tooSmall, completed) := cancelWith withBad e "A" [0]
  check "one tainted cancellation ack is insufficient and leaves landing possible" (!completed && (attempt tooSmall e "A").2)

end RaceTests
