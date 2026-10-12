import JointSyntax
namespace JointCompletion.Structural
open P01AC P01D OrthemologyV2 OrthemologyV3 P01R
open P01AC.ExtensionalRepair.Structural

theorem form_ctx {Γ A} (h : FormJ Γ A) : CtxJ Γ := by
  induction h using FormJ.rec
    (motive_1 := fun _ _ => True) (motive_3 := fun _ _ _ _ => True) with
  | formBase h => exact .ctxBase (P01AC.ExtensionalRepair.Structural.form_ctx h)
  | param h _ => exact h
  | bottom h _ => exact h
  | raw h _ => exact h
  | all h _ _ _ => exact h
  | pi _ _ ih _ => exact ih
  | sigma _ _ ih _ => exact ih
  | identity _ _ _ ih _ _ => exact ih
  | _ => trivial

theorem form_pi_inv {Γ A B} (h : FormJ Γ (.pi A B)) :
    FormJ Γ A ∧ FormJ (A :: Γ) B := by
  cases h with
  | formBase h => cases h with | pi hA hB => exact ⟨.formBase hA, .formBase hB⟩
  | pi hA hB => exact ⟨hA,hB⟩

theorem form_identity_inv {Γ A p q} (h : FormJ Γ (.identity A p q)) :
    FormJ Γ A ∧ HasJ Γ p A ∧ HasJ Γ q A := by
  cases h with
  | formBase h => cases h with | identity hA hp hq => exact ⟨.formBase hA,.hasBase hp,.hasBase hq⟩
  | identity hA hp hq => exact ⟨hA,hp,hq⟩
end JointCompletion.Structural
