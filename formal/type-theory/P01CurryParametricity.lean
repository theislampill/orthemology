/- A new, separate parametricity theorem for the actual Curry-System-F Has
   judgment in the qualified P01 bridge, realized by its finite SKI polynomial
   compiler. This is typed PER semantics, never raw conversion reflection. -/
import P01RecursiveModel
import P01SystemF
namespace P01R
open OrthemologyV2 OrthemologyV3 P01D
open P01F (cons)

/-- Type annotations are erased. Lambda uses the qualified K-priority tracker. -/
def compile : P01F.LTerm → Poly
  | .var n => .var n
  | .zero => .atom .zero
  | .one => .atom .one
  | .app f x => .app (compile f) (compile x)
  | .lam b => abstract (compile b)

def ValRelated (Γ : P01F.Context) (r : REnv) (θ η : P01D.Env) : Prop :=
  ∀ n, (interpret (Γ n)).rel r (θ n) (η n)

theorem valuations_left {Γ r θ η} (h : ValRelated Γ r θ η) :
    ValRelated Γ (diagEnv r.left) θ θ := by
  intro n
  exact ((interpret (Γ n)).identity _ _ _).mpr ((interpret (Γ n)).endpoints r (h n)).1

theorem valuations_right {Γ r θ η} (h : ValRelated Γ r θ η) :
    ValRelated Γ (diagEnv r.right) η η := by
  intro n
  exact ((interpret (Γ n)).identity _ _ _).mpr ((interpret (Γ n)).endpoints r (h n)).2

theorem valuations_cons {Γ r θ η A x y} (h : ValRelated Γ r θ η)
    (ha : (interpret A).rel r x y) :
    ValRelated (cons A Γ) r (cons x θ) (cons y η) := by
  intro n
  cases n with
  | zero => exact ha
  | succ n => exact h n

theorem valuations_shift {Γ r θ η} (h : ValRelated Γ r θ η)
    {P Q : PER} (R : Link P Q) :
    ValRelated (P01F.shiftContext Γ) (extendEnv R r) θ η := by
  intro n
  change (interpret (rename Nat.succ (Γ n))).rel (extendEnv R r) (θ n) (η n)
  rw [interpret_rename]
  exact h n

/-- The abstraction endpoint proof is semantic and uses related applications.
    It does not assert equality of un-applied bracket compilers in raw Conv. -/
theorem abstraction_endpoint (Γ : P01F.Context) (A B : TypeCode) (b : Poly)
    (ih : ∀ r θ η, ValRelated (cons A Γ) r θ η →
      (interpret B).rel r (eval b θ) (eval b η))
    (ρ : OEnv) (θ : P01D.Env) (hθ : ValRelated Γ (diagEnv ρ) θ θ) :
    (ArrPER ((interpret A).obj ρ) ((interpret B).obj ρ)).dom (eval (abstract b) θ) := by
  intro x y hxy
  have hA : (interpret A).rel (diagEnv ρ) x y := ((interpret A).identity ρ x y).mpr hxy
  have hb := ih (diagEnv ρ) (cons x θ) (cons y θ) (valuations_cons hθ hA)
  have hB := ((interpret B).identity ρ _ _).mp hb
  exact ((interpret B).obj ρ).raw
    (P01Source.red_conv (abstraction_beta b θ x)).symm
    (P01Source.red_conv (abstraction_beta b θ y)).symm hB

/-- Every genuine Has derivation supplies its own All uniformity proof. -/
theorem curry_fundamental {Γ t A} (h : P01F.Has Γ t A) :
    ∀ r θ η, ValRelated Γ r θ η →
      (interpret A).rel r (eval (compile t) θ) (eval (compile t) η) := by
  induction h with
  | var Γ n =>
      intro r θ η hv
      exact hv n
  | @lam Γ b A B h ih =>
      intro r θ η hv
      refine ⟨abstraction_endpoint Γ A B (compile b) ih r.left θ (valuations_left hv),
        abstraction_endpoint Γ A B (compile b) ih r.right η (valuations_right hv), ?_⟩
      intro x y hxy
      have hb := ih r (cons x θ) (cons y η) (valuations_cons hv hxy)
      exact ((interpret B).asLink r).raw
        (P01Source.red_conv (abstraction_beta (compile b) θ x)).symm
        (P01Source.red_conv (abstraction_beta (compile b) η y)).symm hb
  | app hf hx ihf ihx =>
      intro r θ η hv
      exact (ihf r θ η hv).2.2 _ _ (ihx r θ η hv)
  | allI h ih =>
      intro r θ η hv
      refine ⟨?_, ?_, ?_⟩
      · apply (all_domain _ _).mpr
        intro P Q R
        exact ih (extendEnv R (diagEnv r.left)) θ θ (valuations_shift (valuations_left hv) R)
      · apply (all_domain _ _).mpr
        intro P Q R
        exact ih (extendEnv R (diagEnv r.right)) η η (valuations_shift (valuations_right hv) R)
      · intro P Q R
        exact ih (extendEnv R r) θ η (valuations_shift hv R)
  | @allE Γ t B h A ih =>
      intro r θ η hv
      apply (instantiate_rel B A r _ _).mpr
      exact (ih r θ η hv).2.2 ((interpret A).obj r.left) ((interpret A).obj r.right)
        ((interpret A).asLink r)

end P01R
