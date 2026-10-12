import OriginalWNoninhabitation

/- Exact downstream original compiler identity, using the already retained
   source-level forward_fixed theorem rather than a semantic reflection rule. -/
namespace HomogeneousOriginalIdentity
open P01AC P01D
open P01AC.EffectiveCompleteness (N)
open P01AC.UnaryIdentity.IntensionalBoundary (variableExpr redundantExpr)
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.ExactScalarFusion (W c3)

def originalIdentity : Ty := .identity (arr N N) variableExpr.closed redundantExpr.closed

/-- Existing original-source typing of the exact unchanged compiler endpoint. -/
theorem originalQ_has : Has [] redundantExpr.closed ExactScalarFusion.T :=
  redundantExpr.closed_has

/-- No proof polynomial inhabits the literal original unary compiler identity. -/
theorem original_identity_uninhabited (p : Poly) : ¬HasE [] p originalIdentity := by
  intro h
  have hi : HasE [] p (.identity ExactScalarFusion.T ExactScalarFusion.i redundantExpr.closed) := by
    simpa only [originalIdentity, CompilerBodyControl.variable_closed_exact,
      ExactScalarFusion.T, ExactScalarFusion.i] using h
  exact HomogeneousOriginalW.original_c3_not_W
    (ExactScalarFusion.forward_fixed originalQ_has hi)

theorem literal_original_identity_uninhabited (p : Poly) :
    ¬HasE [] p (.identity (arr N N) variableExpr.closed redundantExpr.closed) :=
  original_identity_uninhabited p

#print axioms originalQ_has
#print axioms original_identity_uninhabited
#print axioms literal_original_identity_uninhabited
end HomogeneousOriginalIdentity
