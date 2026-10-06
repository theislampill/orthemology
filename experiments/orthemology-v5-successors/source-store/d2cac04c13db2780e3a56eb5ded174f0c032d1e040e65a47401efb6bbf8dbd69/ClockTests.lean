import Fixtures
open ComposedExecution
namespace ClockTests

def check (name : String) (condition : Bool) : IO Unit := do
  unless condition do throw (IO.userError s!"FAIL {name}")
  IO.println s!"PASS {name}"

def runClocks (bytes : List Nat) : IO Unit := do
  let p := plant bytes
  let ip := policy "install-criterion"
  let actor : Actor := ⟨ip, p, "A", 2, 0⟩
  let world := initialWorld p ip [3]
  -- The actor's authentic old observation remains 2. Hidden actual time is 100.
  -- It still proposes; the live roots reject, then exact-envelope cleanup runs.
  let expiredWorld := { world with now := 100 }
  let (expiredResult, expiredTrace) := runBatch expiredWorld actor (.install installCommand)
  check "stale actor time still proposes without a current-time oracle" (!(expiredResult.roots 0).cancelled.isEmpty)
  check "actual expired root time blocks every stale-clock landing" (expiredResult.plant == p && expiredTrace.all (fun t => !t.landed))
  let futureActor := { actor with observedTime := 100 }
  let (futureResult, futureTrace) := runBatch world futureActor (.install installCommand)
  check "future actor clock cannot borrow earlier actual time to propose" ((futureResult.roots 0).cancelled.isEmpty && futureTrace.all (fun t => !t.landed))
  check "future actor clock rejection preserves full plant" (futureResult.plant == p)

end ClockTests
