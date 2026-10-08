import UnaryCertificateSoundness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.UnaryIdentity P01AC.UnaryCertificate
example {Γ} (e f : Expr) (c : Certificate) (p q : Poly)
    (hF : FormC Γ (.identity (arr N N) p q)) (h : verifyCertificate e f c = true) :
    HasC Γ (.atom .i) (.identity (arr N N) p q) := .certified e f c hF h
