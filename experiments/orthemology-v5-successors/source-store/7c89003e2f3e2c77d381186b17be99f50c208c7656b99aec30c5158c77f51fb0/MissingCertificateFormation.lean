import UnaryCertificateSoundness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.UnaryIdentity P01AC.UnaryCertificate
example {Γ} (e f : Expr) (c : Certificate) (h : verifyCertificate e f c = true) :
    HasC Γ (.atom .i) (.identity (arr N N) e.closed f.closed) := .certified e f c h
