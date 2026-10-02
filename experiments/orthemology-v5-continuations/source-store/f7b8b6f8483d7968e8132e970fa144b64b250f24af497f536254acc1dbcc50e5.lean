import PrefixPrimrec

namespace OrthemologyTagged
open P02A2 P02A2.Q8Measure

theorem selector_zero_first : selector 0 2 = 0 := by decide
theorem selector_no_zero : selector 0 3 = 1 := by decide
theorem selector_middle_zero : selector 2 13 = 1 := by decide
theorem selector_last_zero : selector 3 30 = 3 := by decide

def splitMatrix (_ : Unit) (i _s _t : ℕ) : Prop := i = 0
instance splitMatrix_decidable : ∀ a i, DecidableRel (splitMatrix a i) := by
  intro a i s t
  unfold splitMatrix
  infer_instance

theorem good_row_suppresses_bit : pi3PrefixValue splitMatrix () 1 5 = 0 := by decide
theorem bad_row_copies_bit : pi3PrefixValue splitMatrix () 2 13 = 1 := by decide

def trueMatrix (_ : Unit) (_i _s _t : ℕ) : Prop := True
instance trueMatrix_decidable : ∀ a i, DecidableRel (trueMatrix a i) := by
  intro a i s t
  unfold trueMatrix
  infer_instance

theorem true_matrix_zero_defect :
    defect (fairCantor.map (P02A2.ObserverCore.output (pi3PrefixValue trueMatrix ()))) = 0 := by
  rw [finite_prefix_zero_defect_iff]
  exact fun _ => ⟨0,fun _ => True.intro⟩

theorem split_matrix_positive_defect : 0 < defect (pi3Law splitMatrix ()) := by
  rw [pi3_positive_defect_iff]
  refine ⟨1,fun _ => ⟨0, ?_⟩⟩
  simp [splitMatrix]

end OrthemologyTagged
#print axioms OrthemologyTagged.true_matrix_zero_defect
#print axioms OrthemologyTagged.split_matrix_positive_defect
