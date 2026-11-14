/- Based J in the actual two-coordinate context extension, not just a standalone
   transport postulate. New proof candidate; UNCOMPILED at 4.19.0. -/
import P01DependentCore
namespace P01D
open OrthemologyV2 OrthemologyV3

noncomputable def idBody {Γ A} (x : Tm Γ A) : Ty (extend Γ A) :=
  identityTy (x.subst (weaken Γ A)) («variable» Γ A)

noncomputable def idContext {Γ A} (x : Tm Γ A) : Context := extend (extend Γ A) (idBody x)

noncomputable def baseProof {Γ A} (x : Tm Γ A) : Tm Γ (instanceTy (idBody x) x) where
  code := .atom .i
  valid := by
    intro γ δ hγ
    simpa only [instanceTy,Ty.pull,instanceSub,Sub.extend,Sub.id,idBody,identityTy,
      Tm.at,Tm.subst,eval_sub,weaken,«variable»,extend,eval,P01F.cons]
      using id_intro (x.member γ)

noncomputable def baseSub {Γ A} (x : Tm Γ A) : Sub Γ (idContext x) :=
  (instanceSub x).extend (idBody x) (baseProof x)

noncomputable def pointSub {Γ A} (x y : Tm Γ A)
    (p : Tm Γ (instanceTy (idBody x) y)) : Sub Γ (idContext x) :=
  (instanceSub y).extend (idBody x) p

theorem identity_at {Γ A} (x y : Tm Γ A)
    (p : Tm Γ (instanceTy (idBody x) y)) (γ) :
    (A.obj γ).rel (x.at γ) (y.at γ) ∧ Conv (p.at γ) .i := by
  have h := p.member γ
  simpa only [instanceTy,Ty.pull,instanceSub,Sub.extend,Sub.id,idBody,identityTy,
    IdPER,PER.dom,Tm.at,Tm.subst,eval_sub,weaken,«variable»,extend,eval,P01F.cons,and_self]
    using h

/-- Equality-proof coordinates are part of the context relation, so a motive
    cannot inspect I versus a convertible proof and silently change fibre. -/
theorem base_point_related {Γ A} (x y : Tm Γ A)
    (p : Tm Γ (instanceTy (idBody x) y)) (γ) :
    (idContext x).eqv ((baseSub x).map γ) ((pointSub x y p).map γ) := by
  have h := identity_at x y p γ
  refine ⟨⟨Γ.refl γ,h.1⟩,?_⟩
  simpa only [baseSub,pointSub,Sub.extend,instanceSub,Sub.id,idBody,identityTy,
    IdPER,baseProof,Tm.at,Tm.subst,eval_sub,weaken,«variable»,extend,eval,P01F.cons]
    using (show (A.obj γ).rel (x.at γ) (x.at γ) ∧ Conv Term.i Term.i ∧
      Conv (p.at γ) Term.i from ⟨x.member γ,.refl _,h.2⟩)

noncomputable def j {Γ A} (x y : Tm Γ A)
    (p : Tm Γ (instanceTy (idBody x) y)) (M : Ty (idContext x))
    (d : Tm Γ (M.pull (baseSub x))) : Tm Γ (M.pull (pointSub x y p)) where
  code := jPoly d.code y.code p.code
  valid := by
    intro γ δ hγ
    have hd := d.valid hγ
    have e := M.coherent (base_point_related x y p γ)
    have hm : (M.obj ((pointSub x y p).map γ)).rel (d.at γ) (d.at δ) := e ▸ hd
    exact (M.obj ((pointSub x y p).map γ)).raw
      (P01Source.red_conv (eval_j d.code y.code p.code (Γ.environment γ))).symm
      (P01Source.red_conv (eval_j d.code y.code p.code (Γ.environment δ))).symm hm

theorem j_computation {Γ A} (x y : Tm Γ A)
    (p : Tm Γ (instanceTy (idBody x) y)) (M : Ty (idContext x))
    (d : Tm Γ (M.pull (baseSub x))) (γ) : Red ((j x y p M d).at γ) (d.at γ) :=
  eval_j d.code y.code p.code (Γ.environment γ)

def inspectProof (p : Term) : PER := if p = .i then rawPER else botPER

theorem proof_inspection_not_coherent :
    ¬ (∀p q, Conv p q → inspectProof p = inspectProof q) := by
  intro h
  have e := h .i (.app .i .i) (.symm (.step (.i .i)))
  have hi : (inspectProof .i).rel .i .i := by simp only [inspectProof,if_pos rfl]; exact .refl _
  have hf := congrArg (fun P : PER => P.rel .i .i) e
  have bad : (inspectProof (.app .i .i)).rel .i .i := Eq.mp hf hi
  simpa [inspectProof,botPER] using bad
end P01D
