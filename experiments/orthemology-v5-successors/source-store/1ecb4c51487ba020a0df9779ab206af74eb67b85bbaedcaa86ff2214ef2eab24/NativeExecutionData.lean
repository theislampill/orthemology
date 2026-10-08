import NativeInitialWitness
import ControllerWorstCase

namespace SharedAlias.Native
open ComposedExecution
namespace Executed

def worstRouting : Routing 7 := ⟨[0,1], [none], 2,5,5⟩
def goodAliasRouting : Routing 7 := ⟨[0,1], [some 6], 2,5,5⟩

def withholding : List (Annotation 7) := (List.range 21).map fun n =>
  ⟨2+n, List.replicate 7 true, false, List.replicate 7 true⟩

def specs : List (NativeSpec 7) :=
  (compileOrdered Concrete.actor Concrete.action sevenOrderedPaths withholding).getD []

def full : Outcome 7 :=
  (Concrete.execute worstRouting withholding).getD ⟨Concrete.start, []⟩

def firstTwenty : Outcome 7 :=
  let run := runNative worstRouting Concrete.actor.identity Concrete.start (specs.take 20)
  ⟨run.state, List.replicate 7 .hold ++ run.events⟩

def repeated : Outcome 7 := runNative worstRouting Concrete.actor.identity full.state specs

def expired : List (Annotation 7) := withholding.map fun a => { a with time := 90 }
def expiredResult : Outcome 7 :=
  (Concrete.execute worstRouting expired).getD ⟨Concrete.start, []⟩

def malformedAnnotations : List (Annotation 7) :=
  withholding.modifyHead (fun a => { a with prepareBits := [] })
end Executed


/- Exact compiled-interpreter projection. No independent Python simulator. -/
#eval (Executed.specs.length, Executed.firstTwenty.events.length,
  OperationalJoin.Typed.installCount Executed.firstTwenty.events,
  Executed.full.events.length, OperationalJoin.Typed.installCount Executed.full.events,
  OperationalJoin.Typed.repairCount Executed.full.events,
  Executed.full.state.plant.ruleVersion, Executed.full.state.plant.draftRevision)

end SharedAlias.Native
