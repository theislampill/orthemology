import TypeSubstitutionApplications
namespace HasEMixedReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.Structural
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def endTy (k : Nat) : Ty := arr (.param k) (.param k)
theorem end_form {Γ : Tel} (hc : CtxE Γ) (k : Nat) : FormE Γ (endTy k) :=
  .pi (.param hc) (.param (.ext hc (.param hc)))
theorem end_i {Γ : Tel} (hc : CtxE Γ) (k : Nat) : HasE Γ (.atom .i) (endTy k) :=
  .i (.param hc) (end_form hc k)

-- Real piExt input at an open type parameter, not just an assumed derivation.
theorem pi_ext_input (k : Nat) : HasE [] (.atom .i)
    (.identity (endTy k) (.atom .i) (.atom .i)) := by
  have ha : FormE [] (.param k) := .param .nil
  have hc : CtxE [Ty.param k] := .ext .nil ha
  have hb : FormE [Ty.param k] (.param k) := .param hc
  have hi := end_i (Γ := []) .nil k
  have hv : HasE [Ty.param k] (.var 0) (.param k) := .var hb .zero
  have happ : HasE [Ty.param k] (.app (.atom .i) (.var 0)) (.param k) :=
    .piElim (end_form hc k) hb (end_i hc k) hv
  have hbody := FormE.identity hb happ happ
  have hfam := FormE.pi ha hbody
  have he := HasE.identityIntro hbody happ happ (Intensional.Plus.PolyConvPlus.refl _)
  have hh := HasE.piIntro hfam he (scoped_abstract (by trivial))
  exact .piExt ha hb (end_form .nil k) hi hi hbody hfam hh
    (.identity (end_form .nil k) hi hi) (by trivial) (by trivial)
    (scoped_abstract (by trivial)) (by trivial) (by trivial)

-- The allExt input contains the actual piExt input under the type binder.
theorem all_ext_input : HasE [] (.atom .i)
    (.identity (.all (endTy 1)) (.atom .i) (.atom .i)) := by
  have hb := end_form (Γ := []) .nil 1
  have hf : FormE [] (.all (endTy 1)) := .all .nil hb
  have hi : HasE [] (.atom .i) (.all (endTy 1)) := .allIntro hf (end_i .nil 1)
  exact .allExt hb hf hi hi (.identity hb (end_i .nil 1) (end_i .nil 1))
    (pi_ext_input 1) (.identity hf hi hi) (by trivial) (by trivial) (by trivial)
    (by trivial)

def depImage : Ty := .identity .raw (.var 0) (.var 0)
def rawCtx : Tel := [.raw]
theorem raw_ctx : CtxE rawCtx := .ext .nil (.raw .nil)
theorem dep_image_formed : FormE rawCtx depImage :=
  .identity (.raw raw_ctx) (.var (.raw raw_ctx) .zero) (.var (.raw raw_ctx) .zero)

-- Both binders protect the image; the free target term index becomes 1 under Pi.
theorem transport_actual_ext : HasE rawCtx (.atom .i)
    (.identity (.all (.pi depImage (.identity .raw (.var 1) (.var 1))))
      (.atom .i) (.atom .i)) := by
  exact has_closed_tsubst all_ext_input raw_ctx (τ := fun _ => depImage)
    (fun _ => dep_image_formed)

-- Same type image then follows actual dependent term substitution to closed endpoints.
theorem transport_actual_ext_then_term : HasE [] (.atom .i)
    (.identity (.all (.pi (.identity .raw (.atom .i) (.atom .i))
      (.identity .raw (.atom .i) (.atom .i)))) (.atom .i) (.atom .i)) := by
  exact has_subst transport_actual_ext .nil
    (TypedSubstitution.single .nil (HasE.rawAtom (t := .i) (.raw .nil)))

-- Finite type images have genuine target formation; scope alone is insufficient.
theorem no_out_of_scope_type : ¬ FormE rawCtx (.identity .raw (.var 1) (.var 1)) := by
  intro hf
  have hs := form_scoped hf
  change True ∧ 1 < 1 ∧ 1 < 1 at hs
  exact Nat.lt_irrefl 1 hs.2.1

-- The literal two-sort calculation discriminates capture of either sort.
theorem protects_both_indices :
    tsubst (cons (.identity (.param 0) (.var 0) (.var 0)) Ty.param)
      (.all (.pi .raw (.param 1))) =
      .all (.pi .raw (.identity (.param 1) (.var 1) (.var 1))) := rfl

theorem rejects_term_capture :
    tsubst (cons (.identity (.param 0) (.var 0) (.var 0)) Ty.param)
      (.all (.pi .raw (.param 1))) ≠
      .all (.pi .raw (.identity (.param 1) (.var 0) (.var 0))) := by decide

theorem rejects_type_capture :
    tsubst (cons (.identity (.param 0) (.var 0) (.var 0)) Ty.param)
      (.all (.pi .raw (.param 1))) ≠
      .all (.pi .raw (.identity (.param 0) (.var 1) (.var 1))) := by decide

#print axioms transport_actual_ext
#print axioms transport_actual_ext_then_term
#print axioms no_out_of_scope_type
end HasEMixedReview
