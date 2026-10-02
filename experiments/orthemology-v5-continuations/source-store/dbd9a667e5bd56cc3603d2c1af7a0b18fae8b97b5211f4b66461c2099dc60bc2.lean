import ConditionalKilledContinuation

namespace HiddenParity.ResidualSeed.Continuation.Controls
open Orthemology.Tranche2.PolicyEmbedding
abbrev Two := Fin 2

def policy (r : Bool) (h : History Two Two) : Two :=
  match h with
  | [] => if r then 1 else 0
  | (_,y) :: _ => y

def old : History Two Two := [(1,0)]
def tail : History Two Two := [(0,1)]
def sample : Input Bool Two Two :=
  (true, ((fun _ => 0), (fun n _ => if n = 0 then 0 else 1)))

theorem right_append_tracks_newest_receipt : restartPolicy policy old true tail = 1 := by decide

theorem wrong_append_reads_old_receipt : policy true (old ++ tail) = 0 := by decide

theorem append_direction_matters :
    restartPolicy policy old true tail ≠ policy true (old ++ tail) := by decide

theorem actual_prefix_occurs : sample ∈ PrefixEvent policy old := by
  change historyTrajectory ∅ policy sample old.length = old
  decide

theorem actual_continuation_removes_old_prefix :
    continuationHistory policy old sample 0 = [] ∧
    continuationHistory policy old sample 1 = tail := by decide

theorem actual_extension_is_reconstructed :
    historyTrajectory ∅ policy sample (old.length+1) =
      continuationHistory policy old sample 1 ++ old :=
  actual_history_eq_continuation_append policy old sample actual_prefix_occurs 1

#print axioms right_append_tracks_newest_receipt
#print axioms wrong_append_reads_old_receipt
#print axioms append_direction_matters
#print axioms actual_prefix_occurs
#print axioms actual_continuation_removes_old_prefix
#print axioms actual_extension_is_reconstructed
end HiddenParity.ResidualSeed.Continuation.Controls
