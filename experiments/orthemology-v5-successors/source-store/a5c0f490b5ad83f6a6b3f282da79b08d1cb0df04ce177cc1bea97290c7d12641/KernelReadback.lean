import UArrowAndCompilerControls

open P01AC.ExtensionalRepair.UArrowControl
open P01AC.ExtensionalRepair.CompilerBodyControl
open OrthemologyV2 P01D P01AC
open P01AC.UnaryIdentity.IntensionalBoundary

example : ExtensionalRepair.HasE [] (.atom .i) (.identity P p q) := u_arrow_identity
example : redundantExpr.body = literalPairStateBody := redundant_body_exact
example : redundantExpr.closed = abstract literalPairStateBody := redundant_closed_exact
example : variableExpr.closed = .atom .i := variable_closed_exact

#print axioms P01AC.ExtensionalRepair.UArrowControl.u_arrow_identity
#print axioms P01AC.ExtensionalRepair.CompilerBodyControl.redundant_body_exact
