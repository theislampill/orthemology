import NativeExecutionChecks
namespace IndependentOrderedExecutionReview
open SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (interface)

def landingNonces {m} (events : List (OperationalJoin.Event (interface m))) : List Nat :=
  events.filterMap (fun event => match event with | .land k _ _ => some k.val.nonce | _ => none)

def openAnnotations : List (Annotation 7) :=
  Executed.withholding.map (fun a => { a with openGate := true })

def laterActor : Actor :=
  ⟨OperationalJoin.Typed.Examples.source 1, Concrete.installed, "A", 2, 2000⟩
def repairAction : Action := .repair OperationalJoin.Typed.Examples.repairCommand

def checks : List (String × Bool) :=
  [("cancel_reply_short_rejected", (Concrete.execute Executed.worstRouting
      (Executed.withholding.modifyHead (fun a => { a with cancelBits := List.replicate 6 true }))).isNone),
   ("prepare_reply_excess_rejected", (Concrete.execute Executed.worstRouting
      (Executed.withholding.modifyHead (fun a => { a with prepareBits := List.replicate 8 true }))).isNone),
   ("cancel_reply_excess_rejected", (Concrete.execute Executed.worstRouting
      (Executed.withholding.modifyHead (fun a => { a with cancelBits := List.replicate 8 true }))).isNone),
   ("nonzero_valid_repair_proposal_exists", (orderedProgram laterActor repairAction sevenOrderedPaths).isSome),
   ("nonzero_run_entry_explicitly_rejected", (runInitial Executed.worstRouting laterActor repairAction
      sevenOrderedPaths Executed.withholding).isNone),
   ("withholding_land_is_twenty_first_command", decide (landingNonces Executed.full.events = [1021])),
   ("open_gates_land_first_same_public_command", match Concrete.execute Executed.worstRouting openAnnotations with
      | none => false
      | some result => decide (landingNonces result.events = [1001] ∧ result.events.length = 259 ∧
          result.state.plant = Concrete.installed)),
   ("all_decorations_keep_identical_complete_commands", match
      compileOrdered Concrete.actor Concrete.action sevenOrderedPaths openAnnotations with
      | none => false
      | some specs => decide (specs.map (fun s => s.command.val) = Executed.specs.map (fun s => s.command.val)))]

#eval do
  for (name, ok) in checks do
    if !ok then throw (IO.userError ("FAILED: " ++ name))
    IO.println ("PASS: " ++ name)
end IndependentOrderedExecutionReview
