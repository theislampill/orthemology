/- Raw binder/scope equations used by the written schemas.
   None is a conversion generator or an extended-system structural admission. -/
import ExtensionalRepairSyntax
import AllTermAlgebra

namespace P01AC.ExtensionalRepair
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- The fibre of a weakened Pi applied to the new variable is literally B. -/
theorem schema_pi_body_instantiate_shift (B : Ty) :
    inst (subst (pup (fun n => Poly.var (n + 1))) B) (.var 0) = B := by
  rw [inst, subst_comp]
  have e : (fun n => psub (cons (.var 0) Poly.var)
      (pup (fun k => Poly.var (k + 1)) n)) = Poly.var := by
    funext n
    cases n <;> rfl
  rw [e, subst_id]

/-- Entering a term binder removes precisely the external polynomial shift. -/
theorem schema_eval_shift (p : Poly) (x : Term) (η : Env) :
    eval (pren Nat.succ p) (cons x η) = eval p η := by
  rw [eval_ren]
  rfl

theorem schema_eval_application (p : Poly) (x : Term) (η : Env) :
    eval (.app (pren Nat.succ p) (.var 0)) (cons x η) = .app (eval p η) x := by
  change Term.app (eval (pren Nat.succ p) (cons x η)) x = _
  rw [schema_eval_shift]

theorem schema_application_scoped {n : Nat} {p : Poly} (h : Scoped n p) :
    Scoped (n + 1) (.app (pren Nat.succ p) (.var 0)) :=
  ⟨scoped_wk h, Nat.zero_lt_succ n⟩

theorem schema_pi_types_scoped {n : Nat} {A B : Ty} {p q : Poly}
    (a : TyScoped n A) (b : TyScoped (n + 1) B)
    (sp : Scoped n p) (sq : Scoped n q) :
    TyScoped (n + 1) (.identity B (.app (pren Nat.succ p) (.var 0))
      (.app (pren Nat.succ q) (.var 0))) ∧
    TyScoped n (.pi A (.identity B (.app (pren Nat.succ p) (.var 0))
      (.app (pren Nat.succ q) (.var 0)))) ∧
    TyScoped n (.identity (.pi A B) p q) := by
  have m : TyScoped (n + 1) (.identity B (.app (pren Nat.succ p) (.var 0))
      (.app (pren Nat.succ q) (.var 0))) :=
    ⟨b, schema_application_scoped sp, schema_application_scoped sq⟩
  exact ⟨m, ⟨a,m⟩, ⟨⟨a,b⟩,sp,sq⟩⟩

theorem schema_all_types_scoped {n : Nat} {B : Ty} {p q : Poly}
    (b : TyScoped n B) (sp : Scoped n p) (sq : Scoped n q) :
    TyScoped n (.identity B p q) ∧ TyScoped n (.identity (.all B) p q) :=
  ⟨⟨b,sp,sq⟩,⟨b,sp,sq⟩⟩

theorem schema_twk_length (Γ : Tel) : (twkTel Γ).length = Γ.length :=
  List.length_map _

end P01AC.ExtensionalRepair
