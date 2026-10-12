import CriterionInstallation
import DynamicInterlock

namespace ComposedExecution
open TypedCriterionGuard (Source Target Grant)
open CriterionInstallation (Rule)

structure Plant where
  source : Source
  destination : String
  standard : String
  draft : List Nat
  draftRevision : Nat
  draftHistory : List (List Nat)
  rule : Rule
  ruleVersion : Nat
  ruleHistory : List Rule
  unrelated : List String
  deriving DecidableEq, BEq

structure Policy where
  target : Target
  destination : String
  actor : String
  scope : String
  epoch : Nat
  grant : Option Grant
  allowed : Bool := true
  deriving DecidableEq, BEq

inductive Action where
  | install (command : CriterionInstallation.InstallCommand)
  | repair (command : TypedCriterionGuard.Command)
  deriving DecidableEq, BEq

-- Deliberate RED baseline: missing adapter rejects every operation.
def localStep (_p : Plant) (_policy : Policy) (_now : Nat) (_a : Action) : Option Plant := none

end ComposedExecution
