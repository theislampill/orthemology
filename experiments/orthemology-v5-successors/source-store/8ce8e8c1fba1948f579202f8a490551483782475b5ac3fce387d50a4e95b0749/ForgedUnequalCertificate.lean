import UnaryCertificateSoundness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.UnaryIdentity P01AC.UnaryCertificate
example : HasC [] (.atom .i) (.identity (arr N N) (Expr.constant 0).closed (Expr.constant 1).closed) :=
  .certified (.constant 0) (.constant 1) (makeCertificate (.constant 0))
    (form_inclusion (identity_formed _ _)) (by decide)
