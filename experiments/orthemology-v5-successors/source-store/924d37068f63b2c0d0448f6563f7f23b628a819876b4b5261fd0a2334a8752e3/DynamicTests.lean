import Fixtures
open ComposedExecution
namespace DynamicTests

def expectDynamic (name : String) (condition : Bool) : IO Unit := do
  unless condition do throw (IO.userError s!"FAIL {name}")
  IO.println s!"PASS {name}"

def runDynamic (bytes : List Nat) : IO Unit := do
  let p := plant bytes
  let ip := policy "install-criterion"
  let actor : Actor := ⟨ip, p, "A", 2, 0⟩
  let fallback : Envelope := ⟨.install installCommand, p, 1, [0,1,2]⟩
  let e := (propose actor (.install installCommand) [0,1,2]).getD fallback
  let w := initialWorld p ip [3]
  let (prepared, ready) := prepare w e "A"
  expectDynamic "all-good path prepares" ready
  let (landed, applied) := attempt prepared e "A"
  expectDynamic "live gates consume Lean installation successor" applied
  expectDynamic "landing stores exact Lean successor" (landed.plant == e.successor)
  expectDynamic "landing changes installed interpreter behavior" (!CriterionInstallation.accepts landed.plant.rule p.draft bytes)
  let (again, appliedAgain) := attempt landed e "A"
  expectDynamic "replay has no second history/version effect" (!appliedAgain && again.plant == landed.plant)

  let (cancelled, closed) := cancelWith prepared e "A" [0,1]
  expectDynamic "two selected-root acknowledgers close exact envelope" closed
  let (late, lateApplied) := attempt cancelled e "A"
  expectDynamic "cancelled command cannot land late" (!lateApplied && late.plant == p)
  let (reprepared, reopened) := prepare cancelled e "A"
  expectDynamic "delayed prepare cannot reopen tombstone" (!reopened && !(attempt reprepared e "A").2)
  let fresh := { e with nonce := e.nonce + 1 }
  expectDynamic "fresh nonce survives old cancellation" ((attempt (prepare cancelled fresh "A").1 fresh "A").2)
  let (foreign, foreignClosed) := cancelWith prepared e "B" [0,1]
  expectDynamic "foreign actor cannot cancel A" (!foreignClosed && (attempt foreign e "A").2)
  let (postLanding, postClosed) := cancelWith landed e "A" [0,1]
  expectDynamic "cancellation after landing preserves full successor" (postClosed && postLanding.plant == e.successor)
  let rp := policy "replace-derived" 3
  let (revoked, cert) := certifyTransition prepared [1,2,3] rp
  expectDynamic "certified permission-only epoch completes" cert.isSome
  expectDynamic "effective revocation blocks stale prepared install" (!(attempt revoked e "A").2)
  expectDynamic "actor remains at received old epoch" (actor.policy.epoch == 2)
  let certificate := cert.getD ⟨2, rp, [1,2,3]⟩
  let newActor := receiveActor actor certificate 4 3
  expectDynamic "actor adopts only delivered descriptor" (newActor.policy.epoch == 3)
  let informed := deliver revoked certificate
  expectDynamic "old grant stays unusable after delivery" (!(attempt (prepare informed e "A").1 e "A").2)
  expectDynamic "duplicate acknowledgers never complete revocation" ((certifyTransition prepared [0,0,1] rp).2 == none)
  expectDynamic "duplicate acknowledgers never complete cancellation" (!(cancelWith prepared e "A" [0,0]).2)
  let (revokedCancelled, revokedClosed) := cancelWith revoked e "A" [0,1]
  expectDynamic "cleanup permission survives action revocation" (revokedClosed && !(attempt revokedCancelled e "A").2)

end DynamicTests
