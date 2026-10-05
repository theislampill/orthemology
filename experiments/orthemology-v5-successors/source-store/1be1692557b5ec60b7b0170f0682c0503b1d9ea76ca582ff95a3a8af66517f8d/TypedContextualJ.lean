/- The new literal J rule represented by the accepted contextual J operation. -/
import TypedRepresentation
namespace P01TC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

theorem contextual_related {Γ A x} (hx : Has Γ x A) (ρ : OEnv)
    {γ δ : (P01D.idContext (representedTerm hx ρ)).Val}
    (h : (P01D.idContext (representedTerm hx ρ)).eqv γ δ) :
    E (theta Γ A x) ρ
      ((P01D.idContext (representedTerm hx ρ)).environment γ)
      ((P01D.idContext (representedTerm hx ρ)).environment δ) := by
  refine ⟨⟨h.1.1,h.1.2⟩,?_⟩
  change F (Ty.identity (wk A) (pren Nat.succ x) (.var 0)) ρ
    (cons γ.val.1.val.2 γ.val.1.val.1.val) γ.val.2 δ.val.2
  simp only [F,F_wk,eval_ren,eval,cons]
  simpa only [P01D.idBody,P01D.identityTy,IdPER,P01D.Tm.at,P01D.Tm.subst,
    P01D.weaken,P01D.variable,P01D.extend,eval_sub,representedTerm,
    representedType,objectOf,RelLaws.per,representedContext,eval,cons]
    using h.2

theorem contextual_valid {Γ A x} (hx : Has Γ x A)
    (hθ : Ctx (theta Γ A x)) (ρ : OEnv)
    (γ : (P01D.idContext (representedTerm hx ρ)).Val) :
    D (theta Γ A x) ρ ((P01D.idContext (representedTerm hx ρ)).environment γ) :=
  ((context_sound hθ).ends (contextual_related hx ρ ((P01D.idContext (representedTerm hx ρ)).refl γ))).1

noncomputable def contextualMotive {Γ A x B} (hx : Has Γ x A)
    (hθ : Ctx (theta Γ A x)) (hB : Form (theta Γ A x) B) (ρ : OEnv) :
    P01D.Ty (P01D.idContext (representedTerm hx ρ)) where
  obj := fun γ => objectOf (form_sound hB).2.laws (contextual_valid hx hθ ρ γ)
  coherent := by
    intro γ δ h
    exact per_ext ((form_sound hB).2.laws.transport (contextual_related hx ρ h))

noncomputable def contextualProof {Γ A x y e} (hx : Has Γ x A) (hy : Has Γ y A)
    (he : Has Γ e (.identity A x y)) (ρ : OEnv) :
    P01D.Tm _ (P01D.instanceTy (P01D.idBody (representedTerm hx ρ)) (representedTerm hy ρ)) where
  code := e
  valid := by
    intro γ δ h
    have v := unary_fundamental he h
    simpa only [P01D.instanceTy,P01D.Ty.pull,P01D.instanceSub,P01D.Sub.extend,P01D.Sub.id,
      P01D.idBody,P01D.identityTy,IdPER,P01D.Tm.at,P01D.Tm.subst,eval_sub,
      P01D.weaken,P01D.variable,P01D.extend,representedTerm,representedType,
      objectOf,RelLaws.per,representedContext,eval,cons,F] using v

noncomputable def contextualBase {Γ A x B d} (hx : Has Γ x A)
    (hθ : Ctx (theta Γ A x)) (hB : Form (theta Γ A x) B)
    (hd : Has Γ d (motiveAt B x (.atom .i))) (ρ : OEnv) :
    P01D.Tm _ ((contextualMotive hx hθ hB ρ).pull (P01D.baseSub (representedTerm hx ρ))) where
  code := d
  valid := by
    intro γ δ h
    have v := unary_fundamental hd h
    rw [F_motiveAt] at v
    exact v

noncomputable def representedContextualJ {Γ A x y e B d} (hx : Has Γ x A) (hy : Has Γ y A)
    (he : Has Γ e (.identity A x y)) (hθ : Ctx (theta Γ A x)) (hB : Form (theta Γ A x) B)
    (hd : Has Γ d (motiveAt B x (.atom .i))) (ρ : OEnv) :=
  P01D.j (representedTerm hx ρ) (representedTerm hy ρ) (contextualProof hx hy he ρ)
    (contextualMotive hx hθ hB ρ) (contextualBase hx hθ hB hd ρ)

@[simp] theorem representedContextualJ_code {Γ A x y e B d} (hx : Has Γ x A) (hy : Has Γ y A)
    (he : Has Γ e (.identity A x y)) (hθ : Ctx (theta Γ A x)) (hB : Form (theta Γ A x) B)
    (hd : Has Γ d (motiveAt B x (.atom .i))) (ρ : OEnv) :
    (representedContextualJ hx hy he hθ hB hd ρ).code = jPoly d y e := rfl

theorem contextual_target_exact {Γ A x y e B} (hx : Has Γ x A) (hy : Has Γ y A)
    (he : Has Γ e (.identity A x y)) (hθ : Ctx (theta Γ A x)) (hB : Form (theta Γ A x) B)
    (ht : Form Γ (motiveAt B y e)) (ρ : OEnv) :
    (contextualMotive hx hθ hB ρ).pull
      (P01D.pointSub (representedTerm hx ρ) (representedTerm hy ρ) (contextualProof hx hy he ρ)) =
      representedType ht ρ := by
  apply intrinsic_type_ext
  intro γ
  apply per_ext
  intro t u
  exact (Iff.of_eq (F_motiveAt B y e ρ γ.val t u)).symm

end P01TC
