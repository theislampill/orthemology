import Sigma2RowLaw

namespace P02A2.Sigma2Witnesses
open P02A2.Sigma2RowLaw

def trueMatrix (_ : Unit) (_ _ : ℕ) : Prop := True
def falseMatrix (_ : Unit) (_ _ : ℕ) : Prop := False
def swappedMatrix (_ : Unit) (s t : ℕ) : Prop := t ≤ s

instance trueMatrix_decidable (u : Unit) (s t : ℕ) : Decidable (trueMatrix u s t) := inferInstanceAs (Decidable True)
instance falseMatrix_decidable (u : Unit) (s t : ℕ) : Decidable (falseMatrix u s t) := inferInstanceAs (Decidable False)
instance swappedMatrix_decidable (u : Unit) (s t : ℕ) : Decidable (swappedMatrix u s t) := inferInstanceAs (Decidable (t ≤ s))

theorem trueMatrix_primitive_recursive : PrimrecRel (fun p : Unit × ℕ => trueMatrix p.1 p.2) :=
  Primrec.const true

theorem falseMatrix_primitive_recursive : PrimrecRel (fun p : Unit × ℕ => falseMatrix p.1 p.2) :=
  Primrec.const false

theorem swappedMatrix_primitive_recursive : PrimrecRel (fun p : Unit × ℕ => swappedMatrix p.1 p.2) :=
  Primrec.nat_le.comp Primrec.snd (Primrec.snd.comp Primrec.fst)

theorem trueMatrix_defect_zero : defect (rowLaw trueMatrix ()) = 0 :=
  (defect_zero_iff_witness trueMatrix ()).mpr ⟨0, fun _ => trivial⟩

theorem falseMatrix_defect_one : defect (rowLaw falseMatrix ()) = 1 :=
  (defect_one_iff_no_witness falseMatrix ()).mpr (by rintro ⟨s,hs⟩; exact hs 0)

theorem swappedMatrix_forall_exists : ∀ t, ∃ s, swappedMatrix () s t :=
  fun t => ⟨t, le_rfl⟩

theorem swappedMatrix_not_exists_forall : ¬ ∃ s, ∀ t, swappedMatrix () s t := by
  rintro ⟨s,hs⟩
  have h := hs (s+1)
  change s+1 ≤ s at h
  omega

theorem swappedMatrix_defect_one : defect (rowLaw swappedMatrix ()) = 1 :=
  (defect_one_iff_no_witness swappedMatrix ()).mpr swappedMatrix_not_exists_forall

end P02A2.Sigma2Witnesses
