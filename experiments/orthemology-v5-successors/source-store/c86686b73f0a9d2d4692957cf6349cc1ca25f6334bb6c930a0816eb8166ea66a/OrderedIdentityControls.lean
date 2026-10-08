import SourceController
namespace IndependentControllerReview
open ComposedExecution
open OperationalJoin.Typed

def left (a : Action) (p : Plant) : BoundedEnvelope 2 :=
  ⟨⟨a, p, 7, [0, 1]⟩, by change ([0, 1] : List Nat).Nodup ∧ ∀ i ∈ ([0, 1] : List Nat), i < 2; decide⟩
def right (a : Action) (p : Plant) : BoundedEnvelope 2 :=
  ⟨⟨a, p, 7, [1, 0]⟩, by change ([1, 0] : List Nat).Nodup ∧ ∀ i ∈ ([1, 0] : List Nat), i < 2; decide⟩

theorem same_selection (a : Action) (p : Plant) : path (left a p) = path (right a p) := by
  ext i
  simp [mem_path, left, right, or_comm]

theorem different_identity (a : Action) (p : Plant) : left a p ≠ right a p := by
  intro h
  have paths := congrArg (fun e : BoundedEnvelope 2 => e.val.path) h
  simp [left, right] at paths

theorem different_raw_identity (a : Action) (p : Plant) : (left a p).val ≠ (right a p).val := by
  intro h
  exact different_identity a p (Subtype.ext h)

theorem distinct_commitment (a : Action) (p : Plant) :
    (right a p).val ∉ [(left a p).val] := by
  simpa only [List.mem_singleton] using Ne.symm (different_raw_identity a p)

theorem duplicates_do_not_create_other_command (a : Action) (p : Plant) :
    right a p ∉ memory [(left a p).val, (left a p).val] := by
  simp only [mem_memory, List.mem_cons, List.not_mem_nil, or_false, or_self]
  exact Ne.symm (different_raw_identity a p)

theorem duplicate_memory_quotient (a : Action) (p : Plant) :
    memory (n := 2) [(left a p).val, (left a p).val] = memory (n := 2) [(left a p).val] := by
  ext k
  simp only [mem_memory, List.mem_cons, List.not_mem_nil, or_false, or_self]

#print axioms same_selection
#print axioms different_identity
#print axioms different_raw_identity
#print axioms distinct_commitment
#print axioms duplicates_do_not_create_other_command
#print axioms duplicate_memory_quotient

-- Positive callable control: explicitly ordered values stay executable.
#eval (([0, 1] : List Nat), ([1, 0] : List Nat), decide (([0, 1] : List Nat) ≠ [1, 0]))
end IndependentControllerReview
