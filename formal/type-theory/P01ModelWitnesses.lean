/- Concrete nonvacuity and exact boundary witnesses for the new recursive model. -/
import P01CurryParametricity
import P01Translation
namespace P01R
open OrthemologyV2 OrthemologyV3 P01D

def emptyLink (P Q : PER) : Link P Q where
  rel := fun _ _ => False
  endpoints := fun h => False.elim h
  respect := fun _ _ h => False.elim h

theorem finite_polymorphic_I : FiniteDerives .i identityCode :=
  .allI (.i (.var 0))

theorem recursive_polymorphic_I_nonempty (ρ : OEnv) :
    ((interpret identityCode).obj ρ).dom .i := finite_new_model_member finite_polymorphic_I ρ

theorem recursive_polymorphic_I_uniform (r : REnv) :
    (interpret identityCode).rel r .i .i := finite_fundamental finite_polymorphic_I r

theorem recursive_polymorphic_I_self_instance (ρ : OEnv) :
    (ArrPER ((interpret identityCode).obj ρ) ((interpret identityCode).obj ρ)).dom .i :=
  recursive_all_self_instance finite_polymorphic_I ρ

/-- All over the variable itself is genuinely empty: unrestricted quantification
    includes the empty relation at empty endpoints. -/
theorem all_variable_empty (ρ : OEnv) (t : Term) :
    ¬ ((interpret (.all (.var 0))).obj ρ).dom t := by
  intro h
  exact h.1 botPER botPER (emptyLink botPER botPER)

/-- A fixed type-variable assumption cannot be generalized as the fresh bound
    variable. This directly stress-tests the shifted-context Has.allI rule. -/
theorem fixed_assumption_cannot_generalise :
    ¬ P01F.Has (fun _ => TypeCode.var 0) (.var 0) (.all (.var 0)) := by
  intro h
  let ρ : OEnv := fun _ => rawPER
  let θ : P01D.Env := fun _ => .i
  have hv : ValRelated (fun _ => TypeCode.var 0) (diagEnv ρ) θ θ := by
    intro n
    exact Conv.refl .i
  have hp := curry_fundamental h (diagEnv ρ) θ θ hv
  exact all_variable_empty ρ .i ((interpret (.all (.var 0))).endpoints (diagEnv ρ) hp).1

theorem unrestricted_allI_is_not_admissible :
    ¬ (∀ (Γ : P01F.Context) (t : P01F.LTerm) (B : TypeCode),
      P01F.Has Γ t B → P01F.Has Γ t (.all B)) := by
  intro h
  exact fixed_assumption_cannot_generalise (h (fun _ => .var 0) (.var 0) (.var 0) (.var _ 0))

theorem typing_excludes_markers {Γ t A} (h : P01F.Has Γ t A) :
    t ≠ .zero ∧ t ≠ .one := by
  induction h with
  | var Γ n => constructor <;> intro e <;> cases e
  | lam h ih => constructor <;> intro e <;> cases e
  | app hf hx ihf ihx => constructor <;> intro e <;> cases e
  | allI h ih => exact ih
  | allE h A ih => exact ih

theorem original_finite_markers_untypable (A : TypeCode) :
    ¬ FiniteDerives .zero A ∧ ¬ FiniteDerives .one A := by
  constructor
  · intro h
    exact (typing_excludes_markers (P01F.typing_preservation h (fun _ => .bottom))).1 rfl
  · intro h
    exact (typing_excludes_markers (P01F.typing_preservation h (fun _ => .bottom))).2 rfl

def skk : Term := .app (.app .s .k) .k

theorem skk_application (x : Term) : Red (.app skk x) x :=
  .tail (.s .k .k x) (.tail (.k x (.app .k x)) (.refl _))

theorem skk_per (P : PER) : (ArrPER P P).dom skk := by
  intro x y hxy
  exact P.raw (P01Source.red_conv (skk_application x)).symm
    (P01Source.red_conv (skk_application y)).symm hxy

theorem identity_skk_link {P Q : PER} (R : Link P Q) :
    (arrowLink R R).rel .i skk := by
  refine ⟨identity_rel P,skk_per Q,?_⟩
  intro x y hxy
  exact R.raw (.symm (.step (.i x))) (P01Source.red_conv (skk_application y)).symm hxy

theorem finite_skk_identity (A : TypeCode) : FiniteDerives skk (.arrow A A) :=
  .app (.app (.s A (.arrow A A) A) (.k A (.arrow A A))) (.k A A)

theorem finite_polymorphic_skk : FiniteDerives skk identityCode :=
  .allI (finite_skk_identity (.var 0))

theorem recursive_polymorphic_I_skk (r : REnv) :
    (interpret identityCode).rel r .i skk := by
  refine ⟨finite_new_model_member finite_polymorphic_I r.left,
    finite_new_model_member finite_polymorphic_skk r.right, ?_⟩
  intro P Q R
  exact identity_skk_link R

/-- Even at a nonempty polymorphic type, the new relational equality does not
    reflect raw source Conv. This is not an empty-domain-only counterexample. -/
theorem recursive_parametric_equality_not_raw_conversion :
    (∀ r : REnv, (interpret identityCode).rel r .i skk) ∧ ¬ Conv .i skk :=
  ⟨recursive_polymorphic_I_skk,P01Source.I_SKK_not_convertible⟩

end P01R
