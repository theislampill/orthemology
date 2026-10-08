import NativeControls
namespace IndependentPrimitiveReview
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface)
open SharedAlias.Native
namespace F
abbrev k := Fixture.k
abbrev start := Fixture.start
abbrev D := Fixture.routes

def nonceChanged : BoundedEnvelope 7 :=
  ⟨{ k.val with nonce := 1002 }, k.property⟩
def actionChanged : BoundedEnvelope 7 :=
  ⟨{ k.val with action := .install { Fixture.command with leaseEnd := 89 } }, k.property⟩
def highEpoch : FiniteState 7 := { Fixture.preparedGood with epoch := 99 }
def seeded : FiniteState 7 := { start with
  epoch := 11, pending := true, acks := [6, 2, 6],
  certificateRows := [(9, [2, 3]), (9, [0]), (4, [1])],
  cancelRows := [(nonceChanged.val, [2, 3, 4])],
  rootRows := [(some 6, { start.defaultRoot with revoked := [19, 19] })] }
def twiceCancelled : FiniteState 7 := cancelSlot D (cancelSlot D start 0 k "A" false) 0 k "A" false
end F


theorem fresh_nonce_has_no_receipt :
    receipts Fixture.cancelled F.nonceChanged.val = [] ∧
    ComposedExecution.Eligible Fixture.before 2
      (rootAt Fixture.cancelled none) F.nonceChanged.val "A" := by decide

#print axioms fresh_nonce_has_no_receipt
end IndependentPrimitiveReview
