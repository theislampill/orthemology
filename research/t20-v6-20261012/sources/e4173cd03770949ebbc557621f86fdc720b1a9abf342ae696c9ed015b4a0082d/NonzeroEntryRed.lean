import NativeExecutionData
namespace EntryRed
open SharedAlias.Native ComposedExecution
def laterActor : Actor := ⟨OperationalJoin.Typed.Examples.source 1, Concrete.installed, "A", 23, 2000⟩
def repairAction : Action := .repair OperationalJoin.Typed.Examples.repairCommand
#eval do
  if !(orderedProgram laterActor repairAction sevenOrderedPaths).isSome then
    throw (IO.userError "SETUP: expected valid epoch-one proposal")
  if !(runInitial Executed.worstRouting laterActor repairAction sevenOrderedPaths Executed.withholding).isSome then
    throw (IO.userError "EXPECTED RED: accepted entry rejects valid epoch-one repair")
  IO.println "GREEN: nonzero entry accepted"
end EntryRed
