import SourceAttemptTransport

namespace SharedAlias.OrderTransport.Controls
open OperationalJoin
open OperationalJoin.Typed (BoundedEnvelope interface)
noncomputable section
open Classical

example {m} (A : Profile m) : Function.Involutive (selected A) := selected_involutive A

example {m} (A : Profile m) (k : BoundedEnvelope m) :
    (selected A k).val.action = k.val.action ∧
    (selected A k).val.successor = k.val.successor ∧
    (selected A k).val.nonce = k.val.nonce := ⟨rfl, rfl, rfl⟩

example {m} (A : Profile m) (k : BoundedEnvelope m)
    (same : Progress.labelList (OperationalJoin.Typed.path k) = newLabels A (OperationalJoin.Typed.path k)) :
    selected A k = k := selected_fixed_identical A k same

example {m} (T : Symmetry m) (E : Environment (interface m))
    (C D : SharedAlias.State (interface m)) (es : List (Event (interface m))) :
    SharedAlias.Trace E C es D ↔ SharedAlias.Trace E (state T C) (es.map (event T)) (state T D) :=
  trace_iff T E C D es

example {m} (T : Symmetry m) (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) :
    (state T C).cancelAcks (T.command k) = C.cancelAcks k := state_receipts T C k

example {m} (T : Symmetry m) (i : Fin m) (z : RootState (interface m)) :
    event T (.corrupt i z) = .corrupt i (root T z) := rfl

example {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m)
    (who : String) (time : Nat) (badOpen : Bool) :
    Progress.applied E (state T C) (T.command k) who time badOpen = Progress.applied E C k who time badOpen :=
  applied_eq T E C k who time badOpen

example {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m)
    (who : String) (time : Nat) :
    Progress.applied E (state T C) (T.command k) who time false = Progress.applied E C k who time false :=
  applied_eq T E C k who time false

example {m} (T : Symmetry m) (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m)
    (who : String) (time : Nat) :
    Progress.applied E (state T C) (T.command k) who time true = Progress.applied E C k who time true :=
  applied_eq T E C k who time true

end
end SharedAlias.OrderTransport.Controls
