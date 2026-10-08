import NativeExecutionData

namespace SharedAlias.Native
open ComposedExecution

def executionCloseCount {m} (events : List (OperationalJoin.Event (OperationalJoin.Typed.interface m))) : Nat :=
  events.countP (fun event => match event with | .close _ => true | _ => false)

/- These are clean executable assertions, not kernel theorems or a Python
resimulation. Every Boolean runs the actual new finite controller. -/
def executionChecks : List (String × Bool) :=
  [("program_and_service_counts", decide (Executed.specs.length = 21 ∧ Executed.full.events.length = 259 ∧ Executed.firstTwenty.events.length = 247)),
   ("all_closures_are_real_events", decide (executionCloseCount Executed.full.events = 21 ∧ executionCloseCount Executed.firstTwenty.events = 20)),
   ("failed_prefix_really_changed_stores", decide (0 < Executed.firstTwenty.state.rootRows.length ∧ Executed.firstTwenty.state.cancelRows.length = 100)),
   ("first_twenty_no_effect", decide (OperationalJoin.Typed.installCount Executed.firstTwenty.events = 0 ∧ OperationalJoin.Typed.repairCount Executed.firstTwenty.events = 0 ∧ Executed.firstTwenty.state.plant = Concrete.before)),
   ("twenty_first_exact_full_effect", decide (OperationalJoin.Typed.installCount Executed.full.events = 1 ∧ OperationalJoin.Typed.repairCount Executed.full.events = 0 ∧ Executed.full.state.plant = Concrete.installed)),
   ("repeated_action_no_reinstallation", decide (OperationalJoin.Typed.installCount Executed.repeated.events = 0 ∧ OperationalJoin.Typed.repairCount Executed.repeated.events = 0 ∧ Executed.repeated.state.plant = Concrete.installed)),
   ("expired_service_completes_without_effect", decide (Executed.expiredResult.events.length = 259 ∧ OperationalJoin.Typed.installCount Executed.expiredResult.events = 0 ∧ Executed.expiredResult.state.plant = Concrete.before)),
   ("missing_annotation_rejects", (Concrete.execute Executed.worstRouting (Executed.withholding.take 20)).isNone),
   ("extra_annotation_rejects", (Concrete.execute Executed.worstRouting (Executed.withholding ++ Executed.withholding.take 1)).isNone),
   ("malformed_reply_array_rejects", (Concrete.execute Executed.worstRouting Executed.malformedAnnotations).isNone),
   ("nonadmitting_actor_no_synthetic_trial", (runInitial Executed.worstRouting { Concrete.actor with observedTime := 0 } Concrete.action sevenOrderedPaths Executed.withholding).isNone),
   ("bad_prepare_and_cancel_withholding", match Concrete.execute Executed.worstRouting
      (Executed.withholding.map (fun a => { a with prepareBits := List.replicate 7 false, cancelBits := List.replicate 7 false })) with
      | none => false
      | some result => decide (result.state.plant = Concrete.installed ∧ executionCloseCount result.events = 21)),
   ("good_alias_world_full_effect", match Concrete.execute Executed.goodAliasRouting Executed.withholding with
      | none => false
      | some result => decide (result.state.plant = Concrete.installed ∧ OperationalJoin.Typed.installCount result.events = 1 ∧ result.events.length = 259))]

#eval do
  for (name, passed) in executionChecks do
    if !passed then throw (IO.userError ("FAILED: " ++ name))
    IO.println ("PASS: " ++ name)

end SharedAlias.Native
