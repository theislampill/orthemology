import Fixtures
open ComposedExecution

def must (label : String) (b : Bool) : IO Unit := do
  unless b do throw (IO.userError s!"FAIL {label}")
  IO.println s!"PASS independent: {label}"

def main (args : List String) : IO Unit := do
  let input ← IO.FS.readBinFile (args.headD "source.bin")
  let actual := input.data.toList.map UInt8.toNat
  let ip := policy "install-criterion"
  let rp := policy "replace-derived" 3
  let fixtures := [[],[10],[0],[10,10],[255],[0,10],actual]
  let mut cases := 0
  for bytes in fixtures do
    let p := plant bytes
    let a : Actor := ⟨ip,p,"A",2,0⟩
    for bad in [[],[0],[1],[2],[3]] do
      for path in fourPaths do
        let some e := propose a (.install installCommand) path | throw (IO.userError "proposal missing")
        let (prepared, ready) := prepare (initialWorld p ip bad) e "A"
        unless ready do throw (IO.userError "preparation missing")
        let (opened, yes) := attempt prepared e "A" true
        unless yes && opened.plant == { p with rule := .exact, ruleVersion := 4, ruleHistory := [.normalizedLF] } do
          throw (IO.userError "compiled full successor wrong")
        let (withheld, applied) := attempt prepared e "A" false
        let shouldApply := path.all (fun i => !bad.contains i)
        unless applied == shouldApply && withheld.plant == (if shouldApply then e.successor else p) do
          throw (IO.userError "withholding path exact behavior wrong")
        cases := cases + 1
  must "seven source fixtures × five taint sets × four paths, exact open/withhold behavior" (cases == 140)

  let p := plant actual
  let a : Actor := ⟨ip,p,"A",2,0⟩
  let some e := propose a (.install installCommand) [0,1,2] | throw (IO.userError "proposal missing")
  let w := initialWorld p ip [3]
  let prepared := (prepare w e "A").1
  let alteredPlants := [
    { e.successor with source := { e.successor.source with content := [0] } },
    { e.successor with source := { e.successor.source with roots := ["forged"] } },
    { e.successor with source := { e.successor.source with target := ("wrong","wrong","wrong") } },
    { e.successor with destination := "other" },
    { e.successor with standard := "other" },
    { e.successor with draft := [42] },
    { e.successor with draftRevision := 900 },
    { e.successor with draftHistory := [] },
    { e.successor with rule := .normalizedLF },
    { e.successor with ruleVersion := 900 },
    { e.successor with ruleHistory := [] },
    { e.successor with unrelated := [] }]
  let mut boundCases := 0
  for badSuccessor in alteredPlants do
    let badEnvelope := { e with successor := badSuccessor }
    let (badPrepared, ready) := prepare w badEnvelope "A"
    unless !ready && !(attempt badPrepared badEnvelope "A").2 do
      throw (IO.userError "pre-prepare tampered successor admitted")
    boundCases := boundCases + 1
  must "all twelve independently altered successor fields reject before preparation" (boundCases == 12)
  must "wrong recipient identity rejects preparation" (!(prepare w e "B").2)
  must "duplicate path roots cannot inflate threshold" (!(attempt prepared { e with path := [0,0,1] } "A").2)
  must "out-of-domain root cannot inflate threshold" (!(attempt prepared { e with path := [0,1,4] } "A").2)
  must "short path cannot bypass an intact veto" (!(attempt prepared { e with path := [3] } "A").2)

  let atStart := { ip with grant := ip.grant.map (fun g => { g with notBefore := 2 }) }
  let beforeStart := { ip with grant := ip.grant.map (fun g => { g with notBefore := 3 }) }
  must "grant notBefore boundary is inclusive" ((localStep p atStart 2 (.install installCommand)).isSome)
  must "grant before notBefore rejects" ((localStep p beforeStart 2 (.install installCommand)).isNone)
  must "observedAt boundary is inclusive" ((localStep p ip 2 (.install { installCommand with observedAt := 2 })).isSome)
  must "future observedAt rejects" ((localStep p ip 2 (.install { installCommand with observedAt := 3 })).isNone)
  must "leaseEnd boundary is exclusive" ((localStep p ip 90 (.install installCommand)).isNone)
  must "grant expiry boundary is exclusive" ((localStep p ip 100 (.install { installCommand with leaseEnd := 101 })).isNone)
  must "lease cannot extend beyond grant" ((localStep p ip 2 (.install { installCommand with leaseEnd := 101 })).isNone)

  let installed := (attempt prepared e "A").1
  let freshInstall := { installCommand with expectedRule := .exact, expectedVersion := 4 }
  let freshActor := { a with observedPlant := installed.plant, nonce := 4 }
  let some e2 := propose freshActor (.install freshInstall) [0,1,2] | throw (IO.userError "fresh exact reinstall missing")
  let installedTwice := (attempt (prepare installed e2 "A").1 e2 "A").1
  must "fresh authorized exact reinstall advances history; literal idempotence is not claimed"
    (installedTwice.plant.ruleVersion == 5 && installedTwice.plant.ruleHistory == [.normalizedLF,.exact])
  must "old fixed action still rejects after a later lawful install"
    (!(attempt installedTwice e "A").2 && (attempt installedTwice e "A").1.plant == installedTwice.plant)

  let (revoked, cert) := certifyTransition prepared [0,1,2] rp
  let some c3 := cert | throw (IO.userError "certificate missing")
  let delivered := deliver revoked c3
  let policy4 := policy "install-criterion" 4
  let (revokedAgain, cert4) := certifyTransition delivered [1,2,3] policy4
  let some c4 := cert4 | throw (IO.userError "second certificate missing")
  let updated := deliver revokedAgain c4
  let delayed := deliver updated c3
  must "late older certificate cannot regress root policy or revive epoch two"
    ((delayed.roots 0).policy.epoch == 4 && !(attempt delayed e "A").2)
  let uncompleted := { c4 with policy := { c4.policy with epoch := 99 } }
  must "root delivery rejects shape-valid but uncompleted descriptor"
    (((deliver updated uncompleted).roots 0).policy.epoch == 4)
  let bogus := { c3 with policy := { c3.policy with grant := none } }
  let bogusActor := receiveActor a bogus 4 3
  must "actor certificate authenticity is an explicit input premise, not shape verification"
    (bogusActor.policy == bogus.policy && (propose bogusActor (.repair (repairCommand actual)) [0,1,2]).isNone)

  let (closed, cancelled) := cancelWith prepared e "A" [0,1]
  must "exact envelope cancellation completes and blocks the original" (cancelled && !(attempt closed e "A").2)
  let changedAction := .install { installCommand with observedAt := 0 }
  let eSameNonce := { e with action := changedAction }
  must "cancellation is full-envelope scoped; a changed authorized command is not a global nonce ban"
    ((attempt (prepare closed eSameNonce "A").1 eSameNonce "A").2)
  must "revocation after lawful landing does not roll back installed rule"
    ((certifyTransition installed [0,1,2] rp).1.plant == installed.plant)

  let outOfScope :=  { w with q := 1, tainted := fun i => i == 0 }
  let forged := { e with path := [0], successor := { p with unrelated := [] } }
  must "outside large-path premise, an all-tainted path can corrupt custody"
    ((attempt outOfScope forged "A").2 && (attempt outOfScope forged "A").1.plant.unrelated == [])
  let expiredWorld := { w with now := 100 }
  let (expiredResult, _) := runBatch expiredWorld a (.install installCommand)
  must "actor-local stale time creates every envelope without borrowing actual time"
    ((expiredResult.roots 0).cancelled.length == 3 && expiredResult.plant == p)
  must "the same local proposal exists independently of an expired world"
    ((propose a (.install installCommand) [0,1,2]).isSome && !(prepare expiredWorld e "A").2)
  let futureActor := { a with observedTime := 100 }
  must "inadmissible actor-local future time cannot be replaced by earlier world time"
    ((propose futureActor (.install installCommand) [0,1,2]).isNone &&
      ((runBatch w futureActor (.install installCommand)).1.roots 0).cancelled.isEmpty)
  IO.println "INDEPENDENT TERMINAL PASS"
