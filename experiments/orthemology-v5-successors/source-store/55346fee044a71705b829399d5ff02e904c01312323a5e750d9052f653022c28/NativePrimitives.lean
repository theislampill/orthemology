import NativeData

namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface)

/-- Complete source eligibility, not a nonce-only or unordered-key shortcut. -/
def prepareAllowed {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badReply : Bool) : Bool :=
  decide (i.val ∈ k.val.path) &&
    ComposedExecution.validPath (gateWorld D C time C.defaultRoot.policy) k.val &&
    if faulty D i then badReply
    else decide (ComposedExecution.Eligible C.plant time (rootAt C (rootOf D i)) k.val who)

def prepareUpdate {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : BoundedEnvelope m) : FiniteState m :=
  let z := rootAt C (rootOf D i)
  setRoot C (rootOf D i) { z with commitments := k.val :: z.commitments }

def prepareSlot {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badReply : Bool) : FiniteState m :=
  if prepareAllowed D C i k who time badReply then prepareUpdate D C i k else C

/-- One actual addressed receipt. The alias store update never issues a
receipt for a different label. -/
def cancelAllowed {m} (D : Routing m) (i : Fin m)
    (k : BoundedEnvelope m) (who : String) (badReply : Bool) : Bool :=
  decide (i.val ∈ k.val.path) && if faulty D i then badReply else decide (who = k.val.action.actor)

def cancelUpdate {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : BoundedEnvelope m) : FiniteState m :=
  let R := { C with cancelRows := (k.val, i :: receipts C k.val) :: C.cancelRows }
  if faulty D i then R
  else
    let z := rootAt C (rootOf D i)
    setRoot R (rootOf D i) { z with cancelled := k.val :: z.cancelled }

def cancelSlot {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : BoundedEnvelope m) (who : String) (badReply : Bool) : FiniteState m :=
  if cancelAllowed D i k who badReply then cancelUpdate D C i k else C

/-- Literally call the unchanged executable source attempt. Its policy field
is unused by that live gate; no authority is inferred from defaultRoot. -/
def applied {m} (D : Routing m) (C : FiniteState m)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badOpen : Bool) : Bool :=
  (ComposedExecution.attempt (gateWorld D C time C.defaultRoot.policy) k.val who badOpen).2

def attemptSlot {m} (D : Routing m) (C : FiniteState m)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badOpen : Bool) : FiniteState m :=
  let result := ComposedExecution.attempt (gateWorld D C time C.defaultRoot.policy) k.val who badOpen
  if result.2 then { C with plant := result.1.plant } else C

theorem rejected_identity {m} (D : Routing m) (C : FiniteState m)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badOpen : Bool)
    (failure : applied D C k who time badOpen = false) :
    attemptSlot D C k who time badOpen = C := by
  dsimp only [attemptSlot]
  rw [show (ComposedExecution.attempt (gateWorld D C time C.defaultRoot.policy) k.val who badOpen).2 = false from failure]
  rfl

/-- Exactly the accepted closure guard evaluated on actual label receipts. -/
def closed {m} (D : Routing m) (C : FiniteState m) (k : BoundedEnvelope m) : Bool :=
  decide (D.budget < (receipts C k.val).toFinset.card)

/-- Actual emitted events use precisely the same executable branch as state. -/
def prepareEvent {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badReply : Bool) :
    OperationalJoin.Event (interface m) :=
  if prepareAllowed D C i k who time badReply then .prepare i k who time else .hold

def cancelEvent {m} (D : Routing m) (i : Fin m)
    (k : BoundedEnvelope m) (who : String) (badReply : Bool) :
    OperationalJoin.Event (interface m) :=
  if cancelAllowed D i k who badReply then .cancelAck i k who else .hold

def attemptEvent {m} (D : Routing m) (C : FiniteState m)
    (k : BoundedEnvelope m) (who : String) (time : Nat) (badOpen : Bool) :
    OperationalJoin.Event (interface m) :=
  if applied D C k who time badOpen then .land k who time else .hold

def closeEvent {m} (D : Routing m) (C : FiniteState m) (k : BoundedEnvelope m) :
    OperationalJoin.Event (interface m) :=
  if closed D C k then .close k else .hold

end SharedAlias.Native
