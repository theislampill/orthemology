import IdentityChecker
namespace P01AC.RestrictedIdentityV2.Controls
open P01AC.RestrictedIdentity
open P01AC.RestrictedIdentityV2
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

abbrev x : Expr 2 := .variable ⟨0, by decide⟩
abbrev y : Expr 2 := .variable ⟨1, by decide⟩
abbrev c (n : Nat) : Expr 2 := .constant n

def pieceLeft : Expr 2 := .ifZero (.add x y) (c 7) (.mul (.add x (c 1)) (.add y (c 1)))
def pieceRight : Expr 2 := .ifZero x (.ifZero y (c 7) (.add y (c 1)))
  (.add (.add (.mul x y) x) (.add y (c 1)))

theorem genuine_piecewise_identity : identityCheck pieceLeft pieceRight = true := by decide
theorem positive_certificate : verifyCertificate pieceLeft pieceRight (makeCertificate pieceLeft) = true := by decide
theorem unequal_square : identityCheck x (.mul x x) = false := by decide

def omittedZeroMask : Certificate 2 :=
  (makeCertificate pieceLeft).filter (fun row => row.1 0 || row.1 1)
theorem omitted_zero_mask_rejected : verifyCertificate pieceLeft pieceRight omittedZeroMask = false := by decide

def falseConstantTable : Certificate 2 := (masks 2).map (fun s => (s, [(fun _ => 0, 7)]))
theorem forged_coefficients_rejected : verifyCertificate pieceLeft pieceRight falseConstantTable = false := by decide

theorem duplicate_monomials_aggregate :
    coeffEqual ([(fun _ : Fin 2 => 0, 2), (fun _ => 0, 3)] : Sparse 2)
      [(fun _ => 0, 5)] = true := by decide

theorem zero_entries_do_not_change_map :
    coeffEqual ([(fun _ : Fin 2 => 17, 0)] : Sparse 2) [] = true := by decide

theorem incorrect_aggregated_coefficient_rejected :
    coeffEqual ([(fun _ : Fin 2 => 0, 2), (fun _ => 0, 3)] : Sparse 2)
      [(fun _ => 0, 4)] = false := by decide

theorem nested_zero_product :
    identityCheck (.ifZero (.mul x (c 0)) (.ifZero y (c 3) (c 4)) (c 999))
      (.ifZero y (c 3) (c 4)) = true := by decide

theorem zero_arity_equality :
    identityCheck (.ifZero (.constant 0) (.constant 8) (.constant 9) : Expr 0)
      (.constant 8) = true := by decide

theorem zero_arity_inequality : identityCheck (.constant 8 : Expr 0) (.constant 9) = false := by decide

theorem zero_arity_empty_certificate_rejected :
    verifyCertificate (.constant 8 : Expr 0) (.constant 8) [] = false := by decide

theorem zero_arity_certificate :
    verifyCertificate (.constant 8 : Expr 0) (.constant 8) (makeCertificate (.constant 8)) = true := by decide

theorem all_zero_masks_are_included : (masks 0).length = 1 ∧ (masks 3).length = 8 := by decide

theorem absent_middle_variable :
    identityCheck (.add (.variable ⟨0,by decide⟩) (.variable ⟨2,by decide⟩) : Expr 3)
      (.add (.variable ⟨2,by decide⟩) (.variable ⟨0,by decide⟩)) = true := by decide

-- These force actual code generation/execution of the pure checker/certificate verifier.
#eval identityCheck pieceLeft pieceRight
#eval identityCheck x (.mul x x)
#eval verifyCertificate pieceLeft pieceRight (makeCertificate pieceLeft)
#eval verifyCertificate pieceLeft pieceRight omittedZeroMask
#eval match fragmentIdentityDecidable pieceLeft pieceRight with
  | isTrue _ => true
  | isFalse _ => false

end P01AC.RestrictedIdentityV2.Controls
