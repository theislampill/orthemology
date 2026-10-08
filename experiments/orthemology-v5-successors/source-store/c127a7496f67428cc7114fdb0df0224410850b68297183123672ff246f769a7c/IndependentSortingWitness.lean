import IndependentTransportControls

namespace TransportIndependentReview
open SharedAlias SharedAlias.OrderTransport OperationalJoin
open OperationalJoin.Typed (BoundedEnvelope interface path)
noncomputable section
open Classical

def ascending (a : ComposedExecution.Action) (p : ComposedExecution.Plant) (n : Nat) :
    BoundedEnvelope 2 := ⟨⟨a,p,n,[0,1]⟩, by change ([0,1] : List Nat).Nodup; decide, by simp⟩
def descending (a : ComposedExecution.Action) (p : ComposedExecution.Plant) (n : Nat) :
    BoundedEnvelope 2 := ⟨⟨a,p,n,[1,0]⟩, by change ([1,0] : List Nat).Nodup; decide, by simp⟩

theorem opposite_paths_same_support (a : ComposedExecution.Action)
    (p : ComposedExecution.Plant) (n : Nat) :
    path (ascending a p n) = path (descending a p n) := by
  ext i
  simp [path, ascending, descending, or_comm]

theorem opposite_complete_commands_differ (a : ComposedExecution.Action)
    (p : ComposedExecution.Plant) (n : Nat) : ascending a p n ≠ descending a p n := by
  intro h
  have h' := congrArg (fun k : BoundedEnvelope 2 => k.val.path) h
  simp [ascending, descending] at h'

theorem explicit_sorting_collision (a : ComposedExecution.Action)
    (p : ComposedExecution.Plant) (n : Nat) :
    sortCommand (ascending a p n) = sortCommand (descending a p n) := by
  apply Subtype.ext
  change (⟨a,p,n,Progress.labelList (path (ascending a p n))⟩ : ComposedExecution.Envelope) =
    ⟨a,p,n,Progress.labelList (path (descending a p n))⟩
  rw [opposite_paths_same_support]

theorem sorting_is_not_bijection (a : ComposedExecution.Action)
    (p : ComposedExecution.Plant) (n : Nat) : ¬Function.Injective (sortCommand (m := 2)) := by
  intro inj
  exact opposite_complete_commands_differ a p n (inj (explicit_sorting_collision a p n))

end
end TransportIndependentReview
