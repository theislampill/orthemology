/- Exact theorem-scope contracts for the new finite recursive interpretation. -/
import P01RecursiveModel
namespace P01RAssertions
open OrthemologyV2 OrthemologyV3 P01D

theorem unconditional_recursive_IE : ∀ (A : TypeCode) (ρ : P01R.OEnv) (t u : Term),
    (P01R.interpret A).rel (P01R.diagEnv ρ) t u ↔ ((P01R.interpret A).obj ρ).rel t u :=
  P01R.recursive_identity_extension

theorem original_capture_avoiding_substitution : ∀ (A : TypeCode) (s : Nat → TypeCode),
    P01R.interpret (substitute s A) =
      (P01R.interpret A).substitute (fun n => P01R.interpret (s n)) :=
  P01R.interpret_substitute

theorem all_seven_original_finite_rules : ∀ (t : Term) (A : TypeCode),
    FiniteDerives t A → ∀ r : P01R.REnv, (P01R.interpret A).rel r t t :=
  fun _ _ h => P01R.finite_fundamental h

theorem no_external_uniformity_premise : ∀ (t : Term) (B : TypeCode),
    FiniteDerives t B → ∀ (ρ : P01R.OEnv) (P Q : PER) (R : Link P Q),
      (P01R.interpret B).rel (P01R.extendEnv R (P01R.diagEnv ρ)) t t :=
  fun _ _ h ρ P Q R => P01R.finite_fundamental h (P01R.extendEnv R (P01R.diagEnv ρ))

theorem both_endpoint_memberships : ∀ (t : Term) (A : TypeCode),
    FiniteDerives t A → ∀ r : P01R.REnv,
      ((P01R.interpret A).obj r.left).dom t ∧ ((P01R.interpret A).obj r.right).dom t :=
  fun _ _ h r => P01R.recursive_endpoint_restriction _ r (P01R.finite_fundamental h r)

end P01RAssertions
