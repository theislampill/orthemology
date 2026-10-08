import ScalarFusionReverse
import UnaryCurrentIdentityBoundary
import ClosedProofCanonicalisation

namespace P01AC.ExtensionalRepair.ExactScalarFusion
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness
open P01AC.UnaryIdentity.IntensionalBoundary

def p : Poly := variableExpr.closed
def q : Poly := redundantExpr.closed
def literalB : Ty := .identity (arr N N) p q

theorem p_exact_i : p = i := by
  simp [p, variableExpr, UnaryIdentity.Expr.closed, UnaryIdentity.Expr.body,
    UnaryIdentity.Expr.toPR, BooleanPrimitive.PR.compile, RestrictedIdentity.closeMany,
    abstract, freeZero, i]
theorem q_current : Has [] q T := redundantExpr.closed_has
theorem literalB_exact : literalB = B q := by unfold literalB B T; rw [p_exact_i]

/-- An exact conditional reduction, not an inhabitant of the compiled identity. -/
theorem literal_four_way_iff :
    ((∃ r, HasE [] r literalB) ↔ HasE [] i literalB) ∧
    ((∃ r, HasE [] r literalB) ↔ ∃ h, HasE [] h (W q)) ∧
    ((∃ r, HasE [] r literalB) ↔ HasE [] c3 (W q)) := by
  rw [literalB_exact]
  exact generic_four_way_iff q_current

theorem literal_exists_iff_fixed : (∃ r, HasE [] r literalB) ↔ HasE [] i literalB :=
  literal_four_way_iff.1

theorem literal_exists_iff_scalar : (∃ r, HasE [] r literalB) ↔ ∃ h, HasE [] h (W q) :=
  literal_four_way_iff.2.1

theorem literal_exists_iff_c3 : (∃ r, HasE [] r literalB) ↔ HasE [] c3 (W q) :=
  literal_four_way_iff.2.2

/-- The fixed scalar witness is obtained only when an identity derivation is supplied. -/
theorem literal_forward {r : Poly} (hr : HasE [] r literalB) : HasE [] c3 (W q) := by
  rw [literalB_exact] at hr
  exact forward_fixed q_current hr

/-- Any scalar witness suffices, but no such closed witness is asserted. -/
theorem literal_reverse {h : Poly} (hh : HasE [] h (W q)) : HasE [] i literalB := by
  rw [literalB_exact]
  exact reverse_fixed q_current hh

/-- Independent general proof-polynomial canonicalisation agrees with the finite construction. -/
theorem literal_canonical_by_soundness {r : Poly} (hr : HasE [] r literalB) :
    HasE [] i literalB := ClosedProofCanonicalisation.canonical_identity hr

end P01AC.ExtensionalRepair.ExactScalarFusion
