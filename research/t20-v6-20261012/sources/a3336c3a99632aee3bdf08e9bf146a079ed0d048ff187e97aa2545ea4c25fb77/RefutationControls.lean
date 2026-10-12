import RefutationCompleteness
import FullPERBoundaryControls

namespace PRConditionalRefutation
open P01AC P01D P01AC.ExtensionalRepair P01AC.BooleanPrimitive
open FullPERTests

/-- Concrete failed PR tests have actual old-source conditional certificates. -/
theorem one_program_certificate (e : Nat) :
    ∃ q, HasE [] q (arr NoConfusion (arr (programType oneProgram e) .bottom)) := by
  exact refutation_template oneProgram e 0 (by simp [oneProgram,PR.denote])

/-- The certificate direction is discriminating: true tests have no certificate. -/
theorem zero_program_no_certificate (e : Nat) :
    ¬ ∃ q, HasE [] q (arr NoConfusion (arr (programType (.zero 2) e) .bottom)) := by
  intro h
  have hn := (invalid_iff_conditional_refutation (.zero 2) e).mpr h
  exact hn ((program_holds_iff (.zero 2) e).mpr (fun _ => rfl))

#print axioms one_program_certificate
#print axioms zero_program_no_certificate
end PRConditionalRefutation
