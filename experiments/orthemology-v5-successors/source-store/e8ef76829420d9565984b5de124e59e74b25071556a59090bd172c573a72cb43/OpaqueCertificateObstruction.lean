import SourceController
namespace IndependentControllerReview

/-- An executable first-match, explicit-default table, independent of author code. -/
def readRows {β : Type} (rows : List (Nat × β)) (key : Nat) (fallback : β) : β :=
  match rows with
  | [] => fallback
  | (k, value) :: rest => if key = k then value else readRows rest key fallback

def keySum {β : Type} : List (Nat × β) → Nat
  | [] => 0
  | row :: rest => row.1 + keySum rest

theorem member_key_le_sum {β : Type} (rows : List (Nat × β)) (row : Nat × β)
    (member : row ∈ rows) : row.1 ≤ keySum rows := by
  induction rows with
  | nil => simp at member
  | cons head rest ih =>
    rcases List.mem_cons.mp member with same | later
    · subst row; simp only [keySum]; omega
    · have bound := ih later; simp only [keySum]; omega

theorem read_large_default {β : Type} (rows : List (Nat × β)) (key : Nat) (fallback : β)
    (large : keySum rows < key) : readRows rows key fallback = fallback := by
  induction rows with
  | nil => rfl
  | cons head rest ih =>
    have different : key ≠ head.1 := by simp only [keySum] at large; omega
    simp only [readRows, if_neg different]
    apply ih
    simp only [keySum] at large
    omega

/-- No finite empty-default certificate table represents the arbitrary opaque
function that returns a nonempty certificate at every natural epoch. The key
witness is computed as a finite sum plus one, without an oracle or choice. -/
theorem arbitrary_certificate_function_not_reifiable
    (rows : List (Nat × List (Fin 1))) :
    ∃ epoch, (readRows rows epoch []).toFinset ≠ ({0} : Finset (Fin 1)) := by
  refine ⟨keySum rows + 1, ?_⟩
  rw [read_large_default rows (keySum rows + 1) [] (by omega)]
  intro same
  have sizes := congrArg Finset.card same
  simp at sizes

#print axioms arbitrary_certificate_function_not_reifiable
#eval keySum ([(3, [0]), (8, [0]), (3, [0])] : List (Nat × List (Fin 1))) + 1
#eval readRows ([(3, [0]), (8, [0]), (3, [0])] : List (Nat × List (Fin 1))) 15 []
end IndependentControllerReview
