import UnaryCurrentIdentityBoundary
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.UnaryIdentity P01AC.UnaryIdentity.IntensionalBoundary
example : Has [] (.atom .i) (.identity (arr N N) variableExpr.closed redundantExpr.closed) :=
  (identityCheck_iff_F_identity _ _).mp checker_accepts
