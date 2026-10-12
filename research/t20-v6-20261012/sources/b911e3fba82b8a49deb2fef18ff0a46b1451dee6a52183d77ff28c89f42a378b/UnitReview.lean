import UnitTransfer
namespace IndependentUnitReview
open P01AC P01D P01AC.ExtensionalRepair
open RigidityPolymorphicTransfer SourceRigidity

-- Freeze the exact target, including its All carrier and bound identity endpoints.
theorem exact_unit_type : UnitTy = .all (arr (.param 0) (.param 0)) := rfl
theorem exact_unit_eta : UnitEta = .pi UnitTy (.identity UnitTy (.var 0) (.atom .i)) := rfl

theorem closed_exact :
    HasE [] (abstract (abstract (.atom .i)))
      (arr SourceRigidity.Rigidity (.pi UnitTy (.identity UnitTy (.var 0) (.atom .i)))) :=
  rigidity_implies_unit_eta

-- Arbitrary HasE Unit inputs can be used in the closed implication in any original
-- context, with explicit FormE target formation. No Has-to-HasE reflection.
theorem arbitrary_evidence {Γ : Tel} {r u : Poly} (hc : Ctx Γ)
    (hr : HasE Γ r Rigidity) (hu : HasE Γ u UnitTy) :
    HasE Γ (.app (.app (abstract (abstract ident)) r) u) (.identity UnitTy u ident) := by
  have hR := form_inclusion (rigidity_formed hc)
  have hU := form_inclusion (unitEta_form hc)
  have first := HasE.piElim
    (form_inclusion (form_arr (rigidity_formed hc) (unitEta_form hc)))
    ((inst_wk UnitEta r).symm ▸ hU) (rigidity_implies_unit_eta_context hc) hr
  have first' : HasE Γ (.app (abstract (abstract ident)) r) UnitEta := by
    simpa only [inst_wk] using first
  have ht := FormE.identity (form_inclusion (unit_form hc)) hu
    (has_inclusion (ident_unit hc))
  have at_eq : inst (.identity UnitTy (.var 0) ident) u = .identity UnitTy u ident := by
    simp [inst, subst, unit_subst, ident, psub, P01F.cons]
  exact at_eq ▸ HasE.piElim hU (at_eq.symm ▸ ht) first' hu

#print axioms closed_exact
#print axioms arbitrary_evidence
#check RigidityPolymorphicTransfer.unit_ext_from_original_rigidity
end IndependentUnitReview
