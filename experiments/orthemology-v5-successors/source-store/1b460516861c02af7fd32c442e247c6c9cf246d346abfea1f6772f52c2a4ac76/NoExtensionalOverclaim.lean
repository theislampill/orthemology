import UnaryCurrentIdentityBoundary
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.UnaryIdentity.IntensionalBoundary
example (r : Poly) : ¬ P01AC.ExtensionalRepair.HasE [] r
    (.identity (arr N N) variableExpr.closed redundantExpr.closed) := no_current_identity r
