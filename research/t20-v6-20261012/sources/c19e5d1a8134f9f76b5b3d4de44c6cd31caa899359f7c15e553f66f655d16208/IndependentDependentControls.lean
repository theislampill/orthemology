import P01DependentControls
namespace IndependentDependentAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01DF
open P01F (cons)

def varyingBody : P01DF.Ty := .arrow anchoredIdentity anchoredIdentity

theorem varying_body_inhabited_everywhere (ρ : OEnv) (η : Env) :
    (((P01DF.interpret varyingBody).run η).obj ρ).dom .i :=
  unary_soundness (.i anchoredIdentity) ρ η

theorem varying_body_accepts_at_skk (ρ : OEnv) (η : Env) :
    (((P01DF.interpret varyingBody).run (cons P01DF.skk η)).obj ρ).dom (.app .k P01DF.skk) := by
  intro x y hxy
  exact False.elim (P01Source.I_SKK_not_convertible hxy.1.symm)

theorem varying_body_rejects_at_i (ρ : OEnv) (η : Env) :
    ¬ (((P01DF.interpret varyingBody).run (cons .i η)).obj ρ).dom (.app .k P01DF.skk) := by
  intro h
  have e := h .i .i ⟨Conv.refl _, Conv.refl _, Conv.refl _⟩
  exact P01Source.I_SKK_not_convertible
    (((Conv.step (.k P01DF.skk .i)).symm.trans e.2.1).symm)

theorem varying_body_nonconstant (ρ : OEnv) (η : Env) :
    ((P01DF.interpret varyingBody).run (cons P01DF.skk η)).obj ρ ≠
      ((P01DF.interpret varyingBody).run (cons .i η)).obj ρ := by
  intro he
  have h := varying_body_accepts_at_skk ρ η
  rw [he] at h
  exact varying_body_rejects_at_i ρ η h

theorem varying_pi_typed :
    Has (abstract (.atom .i)) (.pi varyingBody) := .piIntro (.i anchoredIdentity)

theorem varying_pi_nonempty (ρ : OEnv) (η : Env) :
    (((P01DF.interpret (.pi varyingBody)).run η).obj ρ).dom (.app .k .i) := by
  have h := unary_soundness varying_pi_typed ρ η
  simpa only [abstract,freeZero,Bool.false_eq_true,↓reduceIte,drop,pren,psub,eval] using h

-- Both free sorts in the replacement survive nested binders in the target.
theorem nested_two_sort_capture_control :
    substType (fun _ => .arrow (.param 0) (.identity (.var 0) (.atom .i)))
      (.all (.pi (.arrow (.param 1) (.identity (.var 1) (.var 0))))) =
    .all (.pi (.arrow (.arrow (.param 1) (.identity (.var 1) (.atom .i)))
      (.identity (.var 1) (.var 0)))) := rfl

theorem nested_index_capture_control :
    substIndex (cons (.atom .k) Poly.var)
      (.all (.pi (.identity (.var 1) (.var 0)))) =
    .all (.pi (.identity (.atom .k) (.var 0))) := rfl

def twiceI : Poly := .app (.atom .i) (.atom .i)
def thriceI : Poly := .app (.atom .i) twiceI

theorem two_coordinate_j_typed :
    Has (jPoly (.atom .i) twiceI thriceI)
      (motiveAt (.identity (.var 0) (.var 1)) twiceI thriceI) := by
  apply Has.j (x := .atom .i)
  · exact .conv (.identityIntro (.symm (.i (.atom .i))))
      (.symm (.trans (.i twiceI) (.i (.atom .i))))
  · exact .identityIntro (.refl _)

theorem two_coordinate_j_nonempty (ρ : OEnv) (η : Env) :
    (((P01DF.interpret (motiveAt (.identity (.var 0) (.var 1)) twiceI thriceI)).run η).obj ρ).dom
      (eval (jPoly (.atom .i) twiceI thriceI) η) :=
  unary_soundness two_coordinate_j_typed ρ η

-- No typed hypothesis can be smuggled in through a free raw index variable.
theorem raw_variable_not_arbitrary_parameter : ¬ Has (.var 0) (.param 0) := by
  intro h
  have hx := unary_soundness h (fun _ => botPER) emptyIndices
  exact hx

-- Stronger than checking one particular proposed index transport function.
theorem no_unrestricted_link_index_transport :
    ¬ (∀ (P Q : PER) (R : Link P Q) (x y : Term), R.rel x y →
      ∀ p, (IdPER rawPER x .i).dom p → (IdPER rawPER y .i).dom p) := by
  intro h
  obtain ⟨P,Q,R,x,y,hxy,hx,hy⟩ := heterogeneous_index_transport_fails (fun _ => rawPER)
  exact hy (h P Q R x y hxy .i hx)


-- The type-quantifier body contains real index dependency and a bound parameter.
def mixedBody : P01DF.Ty := .pi (.arrow (.param 0) (.arrow anchoredIdentity (.param 0)))
def mixedAll : P01DF.Ty := .all mixedBody

theorem mixed_all_typed : Has (abstract (.atom .k)) mixedAll :=
  .allIntro (.piIntro (.k (.param 0) anchoredIdentity))

theorem mixed_all_nonempty (ρ : OEnv) (η : Env) :
    (((P01DF.interpret mixedAll).run η).obj ρ).dom (eval (abstract (.atom .k)) η) :=
  unary_soundness mixed_all_typed ρ η

theorem mixed_all_self_typed :
    Has (abstract (.atom .k)) (instantiateType mixedBody mixedAll) :=
  .allElim mixed_all_typed

theorem mixed_all_self_nonempty (ρ : OEnv) (η : Env) :
    (((P01DF.interpret (instantiateType mixedBody mixedAll)).run η).obj ρ).dom
      (eval (abstract (.atom .k)) η) :=
  unary_soundness mixed_all_self_typed ρ η

end IndependentDependentAudit
