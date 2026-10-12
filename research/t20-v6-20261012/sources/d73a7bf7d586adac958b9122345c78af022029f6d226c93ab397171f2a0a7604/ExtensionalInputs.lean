import IndependentControls
namespace HasEDependentSubstitutionReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

def rawEnd : Ty := .pi .raw .raw

theorem rawEnd_form {Γ : Tel} (hc : CtxE Γ) : FormE Γ rawEnd :=
  .pi (.raw hc) (.raw (.ext hc (.raw hc)))

/-- This control explicitly constructs the actual source piExt constructor. -/
theorem pi_ext_input {Γ : Tel} {p : Poly} (hc : CtxE Γ) (hp : HasE Γ p rawEnd) :
    HasE Γ (.atom .i) (.identity rawEnd p p) := by
  have hA := FormE.raw hc
  have hcA := CtxE.ext hc hA
  have hB := FormE.raw hcA
  have hpw := Structural.has_wk hp hc hA
  have hv : HasE (.raw :: Γ) (.var 0) .raw := .var hB .zero
  have happ : HasE (.raw :: Γ) (.app (pren Nat.succ p) (.var 0)) .raw :=
    .piElim (rawEnd_form hcA) hB hpw hv
  have hBody := FormE.identity hB happ happ
  have hFam := FormE.pi hA hBody
  have he : HasE (.raw :: Γ) (.atom .i)
      (.identity .raw (.app (pren Nat.succ p) (.var 0)) (.app (pren Nat.succ p) (.var 0))) :=
    .identityIntro hBody happ happ (.refl _)
  have hh := HasE.piIntro hFam he (scoped_abstract (by trivial))
  exact HasE.piExt hA hB (rawEnd_form hc) hp hp hBody hFam hh
    (.identity (rawEnd_form hc) hp hp)
    (Structural.has_scoped hp) (Structural.has_scoped hp) (scoped_abstract (by trivial)) (by trivial) (by trivial)

/-- This control explicitly constructs the actual source allExt constructor. -/
theorem all_ext_input {Γ : Tel} {p : Poly} (hc : CtxE Γ) (hp : HasE Γ p (.all .raw)) :
    HasE Γ (.atom .i) (.identity (.all .raw) p p) := by
  have hcw := Structural.ctx_twk hc
  have hB := FormE.raw hcw
  have hF : FormE Γ (.all .raw) := .all hc hB
  have hFw : FormE (twkTel Γ) (.all .raw) :=
    .all hcw (.raw (Structural.ctx_twk hcw))
  have hpw : HasE (twkTel Γ) p (.all .raw) := Structural.has_twk hp
  have hpb : HasE (twkTel Γ) p .raw := .allElim hFw hB hB hpw
  have hBody := FormE.identity hB hpb hpb
  have hh := HasE.identityIntro hBody hpb hpb (Intensional.Plus.PolyConvPlus.refl p)
  exact HasE.allExt hB hF hp hp hBody hh (.identity hF hp hp)
    (Structural.has_scoped hp) (Structural.has_scoped hp) (by trivial) (by trivial)

/-- Substitute a real piExt-derived input using a non-renaming polynomial image. -/
theorem substitute_pi_ext :
    HasE [] (.atom .i) (.identity rawEnd (.atom .i) (.atom .i)) := by
  have hF := rawEnd_form (Γ := []) .nil
  have hc := CtxE.ext .nil hF
  have hp : HasE [rawEnd] (.var 0) rawEnd := .var (rawEnd_form hc) .zero
  have hi : HasE [] (.atom .i) rawEnd := .i (.raw .nil) hF
  exact Structural.has_subst (pi_ext_input hc hp) .nil (single_map .nil hi)

/-- Substitute a real allExt-derived input; the All branch must use type lifting. -/
theorem substitute_all_ext :
    HasE [] (.atom .i) (.identity (.all .raw) (.atom .i) (.atom .i)) := by
  have hF : FormE [] (.all .raw) := .all .nil (.raw .nil)
  have hc := CtxE.ext .nil hF
  have hp : HasE [.all .raw] (.var 0) (.all .raw) :=
    .var (.all hc (.raw (Structural.ctx_twk hc))) .zero
  have hi : HasE [] (.atom .i) (.all .raw) :=
    .allIntro hF (.rawAtom (.raw .nil))
  exact Structural.has_subst (all_ext_input hc hp) .nil (single_map .nil hi)

#print axioms substitute_pi_ext
#print axioms substitute_all_ext
end HasEDependentSubstitutionReview
