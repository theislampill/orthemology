import SubstitutionAdmissibility

namespace IndependentSubstitutionReview
open P01D P01DF P01DF.Syntactic

-- An inserted image carries its own All and Sigma binders. The surrounding
-- All/Pi/Sigma binders must shift only its free coordinates in both sorts.
def imageWithBinders : Ty :=
  .all (.sigma (.arrow (.param 0)
    (.arrow (.param 2) (.identity (.var 0) (.var 1)))))

theorem nested_image_preserves_internal_binders :
  substType (fun _ => imageWithBinders) (.all (.pi (.sigma (.param 1)))) =
    .all (.pi (.sigma (.all (.sigma (.arrow (.param 0)
      (.arrow (.param 3) (.identity (.var 0) (.var 3)))))))) := rfl

theorem inserted_image_free_index_cannot_be_captured :
  substType (fun _ => imageWithBinders) (.all (.pi (.sigma (.param 1)))) ≠
    .all (.pi (.sigma (.all (.sigma (.arrow (.param 0)
      (.arrow (.param 3) (.identity (.var 0) (.var 1)))))))) := by decide

theorem alternating_binders_keep_both_raw_coordinates :
  substIndex (fun n => .app (.var (n+2)) (.var 0))
    (.all (.pi (.sigma (.identity (.var 0) (.app (.var 1) (.var 2)))))) =
    .all (.pi (.sigma (.identity (.var 0)
      (.app (.var 1) (.app (.var 4) (.var 2)))))) := rfl

def sparseImages (n : Nat) : Ty := if n = 7 then imageWithBinders else .raw

theorem sparse_certificate :
  Has (.atom .k) (.arrow imageWithBinders (.arrow .raw imageWithBinders)) :=
  has_type_substitution (Has.k (.param 7) (.param 2)) sparseImages

theorem sparse_bound_is_not_number_of_occurrences :
  freeTypeBound (.arrow (.all (.param 8)) (.pi (.param 2))) = 8 := rfl

theorem premature_prefix_is_discriminated :
  substType (finitePrefix 7 sparseImages) (.param 7) ≠ substType sparseImages (.param 7) := by decide

theorem sufficient_sparse_prefix :
  substType (finitePrefix 8 sparseImages) (.param 7) = substType sparseImages (.param 7) := rfl

-- Noncommuting substitutions: checking composition order is substantive.
def advanceTypes (n : Nat) : Ty := .param (n+1)
def distinguishEight (n : Nat) : Ty := if n = 8 then .raw else .bottom

theorem type_composition_order_certificate :
  Has (.atom .k) (.arrow .raw (.arrow .bottom .raw)) :=
  has_type_composition (Has.k (.param 7) (.param 2)) advanceTypes distinguishEight

theorem reversed_type_composition_is_different :
  substType distinguishEight (substType advanceTypes (.param 7)) ≠
    substType advanceTypes (substType distinguishEight (.param 7)) := by decide

-- J's two distinguished coordinates occur underneath another raw binder.
def nestedMotive : Ty := .pi (.arrow (.identity (.var 1) (.var 2))
  (.identity (.var 0) (.var 3)))

theorem nested_j_coordinate_equation :
  substIndex (fun _ => .app (.var 0) (.var 1))
    (motiveAt nestedMotive (.atom .s) (.atom .k)) =
    .pi (.arrow (.identity (.atom .k) (.atom .s))
      (.identity (.var 0) (.app (.var 1) (.var 2)))) := rfl

theorem nested_j_coordinates_are_not_exchangeable :
  motiveAt nestedMotive (.atom .s) (.atom .k) ≠
    motiveAt nestedMotive (.atom .k) (.atom .s) := by decide

-- Public contracts stay exactly at the original syntax and judgement.
def indexContract : ∀ {p : Poly} {A : Ty}, Has p A →
    ∀ σ : Nat → Poly, Has (psub σ p) (substIndex σ A) := has_index_substitution

def typeContract : ∀ {p : Poly} {A : Ty}, Has p A →
    ∀ τ : Nat → Ty, Has p (substType τ A) := has_type_substitution

#print indexContract
#print typeContract
#print axioms indexContract
#print axioms typeContract
#print axioms sparse_certificate
#print axioms type_composition_order_certificate
#print axioms nested_image_preserves_internal_binders
#print axioms nested_j_coordinate_equation
end IndependentSubstitutionReview
