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


theorem cancel_frames_nonroot_controls :
    (cancelSlot F.D F.seeded 0 F.k "A" false).epoch = 11 ∧
    (cancelSlot F.D F.seeded 0 F.k "A" false).pending = true ∧
    (cancelSlot F.D F.seeded 0 F.k "A" false).acks = [6, 2, 6] ∧
    (cancelSlot F.D F.seeded 0 F.k "A" false).certificateRows = F.seeded.certificateRows ∧
    receipts (cancelSlot F.D F.seeded 0 F.k "A" false) F.nonceChanged.val = [2, 3, 4] ∧
    (rootAt (cancelSlot F.D F.seeded 0 F.k "A" false) (some 6)).revoked = [19, 19] ∧
    (cancelSlot F.D F.seeded 0 F.k "A" false).plant = Fixture.before := by decide

#print axioms cancel_frames_nonroot_controls
end IndependentPrimitiveReview
