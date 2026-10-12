import AllSyntax
namespace IndependentMixedReview
open P01D P01AC OrthemologyV2 OrthemologyV3
set_option maxRecDepth 8192
set_option maxHeartbeats 2000000
-- This file imports only retained source. It cannot use candidate exactness theorems.
def sigma : Nat → Poly := P01F.cons (.var 5) Poly.var
def image : Ty := .identity (.param 2) (.var 0) (.var 3)
def tau : Nat → Ty := P01F.cons image Ty.param

theorem pi_equation (s : Nat → Poly) (t : Nat → Ty) (A B : Ty) :
  mixed s t (.pi A B) = .pi (mixed s t A) (mixed (pup s) (fun n => wk (t n)) B) := rfl
theorem sigma_equation (s : Nat → Poly) (t : Nat → Ty) (A B : Ty) :
  mixed s t (.sigma A B) = .sigma (mixed s t A) (mixed (pup s) (fun n => wk (t n)) B) := rfl
theorem all_equation (s : Nat → Poly) (t : Nat → Ty) (B : Ty) :
  mixed s t (.all B) = .all (mixed s (tup t) B) := rfl

theorem crossed_binders : mixed sigma tau
  (.all (.pi (.param 1) (.sigma (.param 0) (.identity (.param 1) (.var 2) (.app (.var 1) (.var 0)))))) =
  .all (.pi (.identity (.param 3) (.var 0) (.var 3))
    (.sigma (.param 0) (.identity (.identity (.param 3) (.var 2) (.var 5))
      (.var 7) (.app (.var 1) (.var 0))))) := rfl

theorem bottom_nested : tsubst (typeImages [image])
  (.all (.all (.pi (.param 0) (.pi (.param 2) (.param 4))))) =
  .all (.all (.pi (.param 0) (.pi (.identity (.param 4) (.var 1) (.var 4)) .bottom))) := rfl

theorem shifted_nested : tinst
  (.all (.all (.pi (.param 0) (.pi (.param 2) (.param 4))))) image =
  .all (.all (.pi (.param 0) (.pi (.identity (.param 4) (.var 1) (.var 4)) (.param 3)))) := rfl

theorem empty_bottom : tsubst (typeImages []) (.all (.all (.param 2))) = .all (.all .bottom) := rfl
theorem all_term_unchanged : mixed sigma tau (.all (.identity (.param 0) (.var 0) (.var 1))) =
  .all (.identity (.param 0) (.var 5) (.var 0)) := rfl

theorem trename_two_sorts : trename (fun n => n+3)
  (.pi (.param 0) (.all (.identity (.param 1) (.var 0) (.var 2)))) =
  .pi (.param 3) (.all (.identity (.param 4) (.var 0) (.var 2))) := rfl

theorem twk_stored_image : twk image = .identity (.param 3) (.var 0) (.var 3) := rfl
theorem wk_stored_image : wk image = .identity (.param 2) (.var 1) (.var 4) := rfl

theorem tc_nested_capture : instantiateType
  (.all (.all (.arrow (.var 0) (.arrow (.var 2) (.var 4)))))
  (.arrow (.var 0) (.all (.var 1))) =
  .all (.all (.arrow (.var 0) (.arrow (.arrow (.var 2) (.all (.var 3))) (.var 3)))) := rfl

theorem fin_arrow_source (A B : TypeCode) : fin (.arrow A B) = Ty.pi (fin A) (wk (fin B)) := rfl
theorem arr_requires_term_weakening : arr .raw image = .pi .raw (.identity (.param 2) (.var 1) (.var 4)) := rfl
theorem support_nested : finSupport (.all (.all (.arrow (.var 0) (.var 4)))) = 3 := rfl
theorem support_saturates : finSupport (.all (.all (.var 0))) = 0 := rfl
theorem support_mixed_branch : finSupport (.arrow (.var 1) (.all (.all (.var 4)))) = 3 := rfl
theorem fin_nested : fin (.all (.arrow (.var 0) (.all (.arrow (.var 1) (.var 3))))) =
  .all (.pi (.param 0) (.all (.pi (.param 1) (.param 3)))) := rfl
end IndependentMixedReview
