/- Independent, review-only checks. No accepted source is changed. -/
import InhabitedEndpointControl

open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InhabitedControl
open P01AC.Intensional.Plus (PolyConvPlus)

namespace InhabitedIndependentReview

theorem both_ordinary_endpoints :
    Has [] (.app InhabitedControl.H (.app (.atom .k) (.atom .i))) (arr N N) ∧
    Has [] (.app InhabitedControl.H (.app (.atom .k) (.atom .k))) (arr N N) :=
  ⟨Fp_has, Fq_has⟩

theorem direct_j_readback :
    HasE [] (jPoly (.atom .i) q (.atom .i)) (.identity Q Fp Fq) := by
  rw [← target_substitution]
  exact P01AC.ExtensionalRepair.HasE.j
    (Γ := []) (A := E) (B := motive) (x := p) (y := q)
    (e := .atom .i) (d := .atom .i)
    (form_inclusion (E_form .nil)) (form_inclusion motive_form)
    (form_inclusion (.identity (E_form .nil) p_has q_has)) base_form target_form
    (has_inclusion p_has) (has_inclusion q_has) UArrowControl.u_arrow_identity base_has

/-- The rejected wrong-endpoint cast is not an uninhabited proposition:
    even that same literal J-shaped witness has the reflexive identity type. -/
theorem reflexive_control_is_inhabited :
    HasE [] (jPoly (.atom .i) q (.atom .i)) (.identity Q Fp Fp) := by
  have hf : FormE [] (.identity Q Fp Fp) :=
    form_inclusion (.identity (Q_form .nil) Fp_has Fp_has)
  have hi : HasE [] (.atom .i) (.identity Q Fp Fp) :=
    .identityIntro hf (has_inclusion Fp_has) (has_inclusion Fp_has) (.refl Fp)
  have hc : PolyConvPlus (jPoly (.atom .i) q (.atom .i)) (.atom .i) :=
    .trans (.app (.k (.app (.atom .k) (.atom .i)) q) (.refl (.atom .i)))
      (.k (.atom .i) (.atom .i))
  exact .conv hf hi hc.symm (by
    exact ⟨⟨⟨trivial, ⟨trivial, trivial⟩⟩, ⟨trivial, trivial⟩⟩, trivial⟩)

#print P01AC.ExtensionalRepair.HasE.j
#print P01AC.ExtensionalRepair.InhabitedControl.inhabited_endpoint_identity
#print axioms both_ordinary_endpoints
#print axioms direct_j_readback
#print axioms reflexive_control_is_inhabited
end InhabitedIndependentReview
