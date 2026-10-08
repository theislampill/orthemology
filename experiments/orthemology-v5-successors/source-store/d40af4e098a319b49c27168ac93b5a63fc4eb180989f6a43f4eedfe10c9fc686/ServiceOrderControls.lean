import NativeControls
namespace IndependentServiceOrderReview
open SharedAlias.Native
open ComposedExecution

def leftService : FiniteState 7 :=
  cancelSlot Fixture.routes (cancelSlot Fixture.routes Fixture.start 0 Fixture.k "A" false)
    2 Fixture.k "A" false

def rightService : FiniteState 7 :=
  cancelSlot Fixture.routes (cancelSlot Fixture.routes Fixture.start 2 Fixture.k "A" false)
    0 Fixture.k "A" false

/-- Service permutation may change raw storage order even for the same complete command. -/
theorem different_raw_receipt_order :
    receipts leftService Fixture.k.val = [2, 0] ∧
    receipts rightService Fixture.k.val = [0, 2] := by decide

/-- The accepted projection deliberately forgets this receipt order. -/
theorem same_projected_receipts :
    (view leftService).cancelAcks Fixture.k = (view rightService).cancelAcks Fixture.k := by
  change (receipts leftService Fixture.k.val).toFinset = (receipts rightService Fixture.k.val).toFinset
  rw [different_raw_receipt_order.1, different_raw_receipt_order.2]
  ext i
  simp [or_comm]

theorem different_raw_states : leftService ≠ rightService := by
  intro same
  have eq := congrArg (fun C : FiniteState 7 => receipts C Fixture.k.val) same
  change receipts leftService Fixture.k.val = receipts rightService Fixture.k.val at eq
  rw [different_raw_receipt_order.1, different_raw_receipt_order.2] at eq
  cases eq

#print axioms different_raw_receipt_order
#print axioms same_projected_receipts
#print axioms different_raw_states
#eval ((receipts leftService Fixture.k.val).map Fin.val,
  (receipts rightService Fixture.k.val).map Fin.val)
end IndependentServiceOrderReview
