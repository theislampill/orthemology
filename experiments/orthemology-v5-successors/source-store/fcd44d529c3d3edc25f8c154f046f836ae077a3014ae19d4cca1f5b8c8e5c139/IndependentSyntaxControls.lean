/- Discriminating exact-syntax tests for the two independent binding sorts. -/
import AllSyntax

namespace P01AC.IndependentSyntax
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def openImage : Ty := .identity (.param 0) (.var 0) (.atom .i)

theorem both_sorts_capture_avoided :
    tsubst (cons openImage Ty.param) (.all (.pi .raw (.param 1))) =
      .all (.pi .raw (.identity (.param 1) (.var 1) (.atom .i))) := rfl

theorem nested_term_capture_avoided :
    tsubst (cons openImage Ty.param)
      (.all (.pi .raw (.sigma .raw (.param 1)))) =
      .all (.pi .raw (.sigma .raw
        (.identity (.param 1) (.var 2) (.atom .i)))) := rfl

theorem nested_type_capture_avoided :
    tsubst (cons openImage Ty.param)
      (.all (.all (.pi .raw (.param 2)))) =
      .all (.all (.pi .raw
        (.identity (.param 2) (.var 1) (.atom .i)))) := rfl

theorem newly_bound_parameter_untouched :
    tsubst (cons openImage Ty.param) (.all (.pi .raw (.param 0))) =
      .all (.pi .raw (.param 0)) := rfl

theorem shifted_assumption_is_old_parameter :
    twkTel [.param 0] = [.param 1] := rfl

theorem scoped_finite_parameter_support :
    finSupport (.all (.arrow (.var 0) (.all (.arrow (.var 2) (.var 4))))) = 3 := rfl

theorem closed_finite_parameter_support :
    finSupport (.all (.arrow (.var 0) (.var 0))) = 0 := rfl

theorem type_table_bottom_default (A : Ty) : typeImages [A] 3 = .bottom := rfl

/-- Evaluation equality cannot be mistaken for literal source-polynomial equality. -/
theorem opaque_application_is_not_poly_application (f a : Term) :
    (Poly.atom (.app f a)) ≠ Poly.app (.atom f) (.atom a) := by
  intro h
  cases h

end P01AC.IndependentSyntax
