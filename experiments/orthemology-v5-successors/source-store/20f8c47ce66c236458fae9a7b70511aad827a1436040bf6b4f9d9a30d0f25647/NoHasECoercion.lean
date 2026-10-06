import UnaryCertificateSoundness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.UnaryIdentity P01AC.UnaryCertificate
example : P01AC.ExtensionalRepair.HasE [] (.atom .i) (.identity (arr N N)
    IntensionalBoundary.variableExpr.closed IntensionalBoundary.redundantExpr.closed) := strict_current_extension.1
